from dataclasses import dataclass
import math
from typing import Literal

import numpy as np
from numpy.typing import NDArray

ModeName = Literal["USS", "PSS", "FSS"]
ControlMode = Literal["PQ", "PV", "GS", "GFM"]


@dataclass(frozen=True)
class VSCConverterSpec:
    bus: int
    p_ref: float
    q_ref: float
    i_max: float
    saturation_preference: Literal["PSS", "FSS"] = "PSS"
    control_mode: ControlMode = "PQ"
    u_ref: float = 1.0
    k_isp: float = 0.0
    u_ref_gs: float = 1.0


@dataclass(frozen=True)
class NewtonStateLayout:
    bus_count: int
    reference_bus: int
    non_reference_buses: tuple[int, ...]
    active_converter_indices: tuple[int, ...]
    voltage_real_slice: slice
    voltage_imag_slice: slice
    current_real_slice: slice
    current_imag_slice: slice


@dataclass(frozen=True)
class InnerSolveResult:
    voltages: NDArray[np.complex128]
    current_injections: NDArray[np.complex128]
    converged: bool
    iterations: int
    max_residual: float
    internal_state_vector: NDArray[np.float64] | None = None


@dataclass(frozen=True)
class SolverResult:
    voltages: NDArray[np.complex128]
    converged: bool
    outer_iterations: int
    inner_iterations: int
    iterations: int
    max_residual: float
    converter_states: dict[int, ModeName]
    mode_history: list[dict[int, ModeName]]
    current_injections: dict[int, complex]
    fault_current: complex


class PaperFaithfulShortCircuitSolver:
    tolerance: float
    max_iter: int
    max_outer_iter: int
    exit_tolerance: float

    def __init__(
        self,
        tolerance: float = 1e-8,
        max_iter: int = 30,
        max_outer_iter: int = 12,
        exit_tolerance: float = 1e-4,
        damping_factor: float = 0.5,
        use_damping: bool = True,
    ) -> None:
        self.tolerance = tolerance
        self.max_iter = max_iter
        self.max_outer_iter = max_outer_iter
        self.exit_tolerance = exit_tolerance
        self.damping_factor = damping_factor  # Damped Newton: x_new = x_old + damping * delta
        self.use_damping = use_damping

    def solve(
        self,
        admittance_matrix: NDArray[np.complex128],
        slack_bus: int,
        fault_bus: int,
        fault_impedance: complex,
        converters: list[VSCConverterSpec],
        slack_voltage: complex = 1.0 + 0.0j,
    ) -> SolverResult:
        network_matrix = np.array(admittance_matrix, dtype=np.complex128, copy=True)
        network_matrix[fault_bus, fault_bus] += 1.0 / complex(fault_impedance)
        bus_count = int(network_matrix.shape[0])
        layout = self._build_layout(bus_count, slack_bus, converters)
        modes = self._initial_modes(converters)
        mode_history: list[dict[int, ModeName]] = []
        seen_modes: set[tuple[ModeName, ...]] = set()
        last_inner = InnerSolveResult(
            voltages=np.ones(bus_count, dtype=np.complex128),
            current_injections=np.zeros(len(converters), dtype=np.complex128),
            converged=False,
            iterations=0,
            max_residual=float("inf"),
        )

        last_state_vector = None
        for outer_iteration in range(1, self.max_outer_iter + 1):
            mode_history.append({converter.bus: mode for converter, mode in zip(converters, modes)})
            mode_key = tuple(modes)
            if mode_key in seen_modes:
                break
            seen_modes.add(mode_key)
            last_inner = self._solve_given_modes_nr(
                network_matrix=network_matrix,
                slack_bus=slack_bus,
                slack_voltage=slack_voltage,
                converters=converters,
                modes=modes,
                layout=layout,
                previous_state=last_state_vector,
            )
            if last_inner.converged:
                last_state_vector = last_inner.internal_state_vector  # Save for warm-start
            updated_modes = self._classify_modes(converters, last_inner.voltages, last_inner.current_injections, modes)
            if updated_modes == modes:
                return self._build_result(
                    outer_iterations=outer_iteration,
                    inner_result=last_inner,
                    converters=converters,
                    modes=modes,
                    mode_history=mode_history,
                    fault_bus=fault_bus,
                    fault_impedance=fault_impedance,
                )
            modes = updated_modes

        return self._build_result(
            outer_iterations=len(mode_history),
            inner_result=last_inner,
            converters=converters,
            modes=modes,
            mode_history=mode_history,
            fault_bus=fault_bus,
            fault_impedance=fault_impedance,
        )

    def _build_layout(self, bus_count: int, slack_bus: int, converters: list[VSCConverterSpec]) -> NewtonStateLayout:
        # State vector layout:
        # - All bus voltages (including slack): 2 * bus_count variables
        #   This allows V[slack] to be adjusted when reference converter enters FSS/PSS mode
        # - Non-reference converter currents: 2 * (n_conv - 1) variables
        #   Reference converter current is computed from network balance, not a state variable
        # Total variables: 2 * bus_count + 2 * (n_conv - 1) = 2 * (bus_count + n_conv - 1)
        non_reference_buses = tuple(bus for bus in range(bus_count) if bus != slack_bus)
        # All converters at non-slack buses need current state variables
        # Reference converter (GFM@slack) current is computed from network, not a state variable
        active_converter_indices = tuple(
            index
            for index, converter in enumerate(converters)
            if converter.bus != slack_bus  # Non-slack converters need current variables
        )
        voltage_count = bus_count  # Include ALL buses, including slack
        converter_count = len(active_converter_indices)
        return NewtonStateLayout(
            bus_count=bus_count,
            reference_bus=slack_bus,
            non_reference_buses=non_reference_buses,
            active_converter_indices=active_converter_indices,
            # Voltage state variables: all bus voltages (real and imag)
            voltage_real_slice=slice(0, voltage_count),
            voltage_imag_slice=slice(voltage_count, 2 * voltage_count),
            # Converter current state variables: only non-reference converters
            current_real_slice=slice(2 * voltage_count, 2 * voltage_count + converter_count),
            current_imag_slice=slice(2 * voltage_count + converter_count, 2 * voltage_count + 2 * converter_count),
        )

    def _initial_modes(self, converters: list[VSCConverterSpec]) -> list[ModeName]:
        return ["USS" for _ in converters]

    def _control_row_count(self, layout: NewtonStateLayout) -> int:
        return 2 + 2 * len(layout.active_converter_indices)

    def _solve_given_modes_nr(
        self,
        network_matrix: NDArray[np.complex128],
        slack_bus: int,
        slack_voltage: complex,
        converters: list[VSCConverterSpec],
        modes: list[ModeName],
        layout: NewtonStateLayout,
        previous_state: NDArray[np.float64] | None = None,
    ) -> InnerSolveResult:
        if previous_state is not None:
            state_vector = previous_state.copy()
            # Warm-start fix: PSS/FSS converters may have I~0 from previous USS solution.
            # Project them onto the limit circle |I|=I_max to avoid Jacobian singularity.
            voltages, active_currents = self._decode_solution(state_vector, layout)
            modified = False
            for position, converter_index in enumerate(layout.active_converter_indices):
                mode = modes[converter_index]
                if mode not in ("PSS", "FSS"):
                    continue
                current = active_currents[position]
                if abs(current) < 1e-6:
                    converter = converters[converter_index]
                    voltage = voltages[converter.bus]
                    angle = np.angle(voltage) if abs(voltage) > 1e-9 else 0.0
                    active_currents[position] = converter.i_max * np.exp(1j * angle)
                    modified = True
            if modified:
                state_vector[layout.current_real_slice] = active_currents.real
                state_vector[layout.current_imag_slice] = active_currents.imag
        else:
            state_vector = self._initial_guess(network_matrix, slack_bus, slack_voltage, converters, layout, modes)

        for iteration in range(1, self.max_iter + 1):
            residual = self._evaluate_residual(
                state_vector=state_vector,
                network_matrix=network_matrix,
                slack_bus=slack_bus,
                slack_voltage=slack_voltage,
                converters=converters,
                modes=modes,
                layout=layout,
            )
            max_residual = float(np.max(np.abs(residual))) if residual.size else 0.0
            if iteration <= 3 or iteration % 10 == 0:  # Debug output
                voltages_debug, active_currents_debug = self._decode_solution(state_vector, layout)
                debug_msg = f"  Iter {iteration}: |res|={max_residual:.6f}, V[0]={voltages_debug[0]:.6f}"
                if len(voltages_debug) > 5:
                    debug_msg += f", V[5]={voltages_debug[5]:.6f}"
                print(debug_msg)
            if max_residual <= self.tolerance:
                voltages, active_currents = self._decode_solution(state_vector, layout)
                currents = self._expand_currents(voltages, active_currents, network_matrix, converters, layout)
                return InnerSolveResult(
                    voltages=voltages,
                    current_injections=currents,
                    converged=True,
                    iterations=iteration,
                    max_residual=max_residual,
                    internal_state_vector=state_vector,
                )
            jacobian = self._assemble_jacobian(
                state_vector=state_vector,
                network_matrix=network_matrix,
                slack_bus=slack_bus,
                slack_voltage=slack_voltage,
                converters=converters,
                modes=modes,
                layout=layout,
            )
            try:
                delta = np.linalg.solve(jacobian, -residual)
            except np.linalg.LinAlgError:
                # Jacobian is singular - try smaller step or restart
                delta = np.zeros_like(state_vector)
                step_scale = 0.5
                candidate_state = state_vector + step_scale * delta
                candidate_residual = self._evaluate_residual(
                    state_vector=candidate_state,
                    network_matrix=network_matrix,
                    slack_bus=slack_bus,
                    slack_voltage=slack_voltage,
                    converters=converters,
                    modes=modes,
                    layout=layout,
                )
                candidate_max_residual = float(np.max(np.abs(candidate_residual))) if candidate_residual.size else 0.0
                while candidate_max_residual >= max_residual and step_scale > 1e-3:
                    step_scale *= 0.5
                    candidate_state = state_vector + step_scale * delta
                    candidate_residual = self._evaluate_residual(
                        state_vector=candidate_state,
                        network_matrix=network_matrix,
                        slack_bus=slack_bus,
                        slack_voltage=slack_voltage,
                        converters=converters,
                        modes=modes,
                        layout=layout,
                    )
                    candidate_max_residual = float(np.max(np.abs(candidate_residual))) if candidate_residual.size else 0.0
                state_vector = candidate_state
                continue

            # Check for NaN/Inf in delta
            if np.any(np.isnan(delta)) or np.any(np.isinf(delta)):
                # Numerical overflow - restart with small step
                delta = np.zeros_like(state_vector)
                step_scale = 0.1
            else:
                step_scale = 1.0

            # Limit step size to prevent divergence
            delta_norm = np.linalg.norm(delta)
            if delta_norm > 10.0:  # Arbitrary large step threshold
                delta = delta * (10.0 / delta_norm)  # Cap the step
                step_scale = 10.0 / delta_norm

            candidate_state = state_vector + step_scale * delta

            # Check for NaN/Inf before evaluating residual
            if np.any(np.isnan(candidate_state)) or np.any(np.isinf(candidate_state)):
                # Numerical overflow - refuse this step, try smaller
                step_scale *= 0.5
                candidate_state = state_vector + step_scale * delta

            candidate_residual = self._evaluate_residual(
                state_vector=candidate_state,
                network_matrix=network_matrix,
                slack_bus=slack_bus,
                slack_voltage=slack_voltage,
                converters=converters,
                modes=modes,
                layout=layout,
            )
            candidate_max_residual = float(np.max(np.abs(candidate_residual))) if candidate_residual.size else 0.0

            # Line search with better convergence
            while candidate_max_residual > max_residual and step_scale > 1e-4:
                step_scale *= 0.5
                candidate_state = state_vector + step_scale * delta
                # Safety check
                if np.any(np.isnan(candidate_state)) or np.any(np.isinf(candidate_state)):
                    step_scale *= 0.1  # More aggressive reduction
                    continue
                candidate_residual = self._evaluate_residual(
                    state_vector=candidate_state,
                    network_matrix=network_matrix,
                    slack_bus=slack_bus,
                    slack_voltage=slack_voltage,
                    converters=converters,
                    modes=modes,
                    layout=layout,
                )
                candidate_max_residual = float(np.max(np.abs(candidate_residual))) if candidate_residual.size else 0.0

            # Accept step only if it improved residual
            if candidate_max_residual < max_residual:
                state_vector = candidate_state
            else:
                # Line search failed - keep current state
                pass

        final_residual = self._evaluate_residual(
            state_vector=state_vector,
            network_matrix=network_matrix,
            slack_bus=slack_bus,
            slack_voltage=slack_voltage,
            converters=converters,
            modes=modes,
            layout=layout,
        )
        voltages, active_currents = self._decode_solution(state_vector, layout)
        currents = self._expand_currents(voltages, active_currents, network_matrix, converters, layout)
        return InnerSolveResult(
            voltages=voltages,
            current_injections=currents,
            converged=False,
            iterations=self.max_iter,
            max_residual=float(np.max(np.abs(final_residual))) if final_residual.size else 0.0,
            internal_state_vector=state_vector,
        )

    def _initial_guess(
        self,
        network_matrix: NDArray[np.complex128],
        slack_bus: int,
        slack_voltage: complex,
        converters: list[VSCConverterSpec],
        layout: NewtonStateLayout,
        modes: list[ModeName] | None = None,
    ) -> NDArray[np.float64]:
        bus_count = layout.bus_count
        # Initialize ALL bus voltages (including slack) as state variables
        voltages = np.ones(bus_count, dtype=np.complex128) * slack_voltage
        # Solve for non-slack bus voltages using reduced network matrix
        # Account for converter current injections at non-reference buses
        # KCL: Y[i,:] @ V = I_injected[i] for i != slack
        # For USS: I_injected = conj(S_ref / V[i])
        # For FSS/PSS: I_injected = I_max * exp(j * angle(V[i]))
        reduced_matrix = network_matrix[np.ix_(layout.non_reference_buses, layout.non_reference_buses)]
        # Right-hand side: -Y[i,slack]*V[slack] - I_injected[i]
        slack_column = network_matrix[np.ix_(layout.non_reference_buses, (slack_bus,))][:, 0]
        rhs = -slack_column * slack_voltage
        # Add converter current injections
        current_injections = {}
        for position, converter_index in enumerate(layout.active_converter_indices):
            converter = converters[converter_index]
            mode = modes[converter_index] if modes is not None else "USS"
            bus = converter.bus
            if bus == slack_bus:
                continue
            bus_voltage = voltages[bus]  # Initial guess: slack_voltage
            if mode in ("PSS", "FSS"):
                current_injections[bus] = converter.i_max * np.exp(1j * np.angle(bus_voltage))
            else:
                # USS: I = conj(S_ref / V)
                s_ref = complex(converter.p_ref, converter.q_ref)
                current_injections[bus] = np.conj(s_ref / bus_voltage)
        # Adjust RHS for buses with converter injections
        for position, bus in enumerate(layout.non_reference_buses):
            if bus in current_injections:
                rhs[position] -= current_injections[bus]
        solved_non_reference = np.linalg.solve(reduced_matrix, rhs)
        for position, bus in enumerate(layout.non_reference_buses):
            voltages[bus] = solved_non_reference[position]
        # Re-compute converter currents with solved voltages
        currents = np.zeros(len(layout.active_converter_indices), dtype=np.complex128)
        for position, converter_index in enumerate(layout.active_converter_indices):
            converter = converters[converter_index]
            mode = modes[converter_index] if modes is not None else "USS"
            bus_voltage = voltages[converter.bus]
            if abs(bus_voltage) <= 1e-9:
                currents[position] = 0.0 + 0.0j
                continue
            if mode in ("PSS", "FSS"):
                voltage_angle = np.angle(bus_voltage)
                currents[position] = converter.i_max * np.exp(1j * voltage_angle)
            else:
                complex_power = complex(converter.p_ref, converter.q_ref)
                currents[position] = np.conj(complex_power / bus_voltage)
        # Handle reference converter in FSS mode: V[slack] magnitude must collapse
        ref_idx = self._reference_converter_index(converters, slack_bus)
        if ref_idx is not None and modes is not None and modes[ref_idx] == "FSS":
            ref_conv = converters[ref_idx]
            y_row = network_matrix[slack_bus, :]
            y_diag = y_row[slack_bus]
            if abs(y_diag) > 1e-12:
                v_mag = ref_conv.i_max / abs(y_diag)
                voltages[slack_bus] = complex(v_mag, 0.0)
        # Build state vector: all bus voltages + non-reference converter currents
        state_vector = np.zeros(int(layout.current_imag_slice.stop or 0), dtype=np.float64)
        state_vector[layout.voltage_real_slice] = voltages.real
        state_vector[layout.voltage_imag_slice] = voltages.imag
        state_vector[layout.current_real_slice] = currents.real
        state_vector[layout.current_imag_slice] = currents.imag
        return state_vector

    def _decode_solution(
        self,
        state_vector: NDArray[np.float64],
        layout: NewtonStateLayout,
    ) -> tuple[NDArray[np.complex128], NDArray[np.complex128]]:
        # Decode ALL bus voltages from state vector (including slack)
        voltage_real = state_vector[layout.voltage_real_slice]
        voltage_imag = state_vector[layout.voltage_imag_slice]
        voltages = np.array(voltage_real + 1j * voltage_imag, dtype=np.complex128)
        # Decode non-reference converter currents from state vector
        current_real = state_vector[layout.current_real_slice]
        current_imag = state_vector[layout.current_imag_slice]
        currents = np.array(current_real + 1j * current_imag, dtype=np.complex128)
        return voltages, currents

    def _expand_currents(
        self,
        voltages: NDArray[np.complex128],
        active_currents: NDArray[np.complex128],
        network_matrix: NDArray[np.complex128],
        converters: list[VSCConverterSpec],
        layout: NewtonStateLayout,
    ) -> NDArray[np.complex128]:
        full_currents = np.zeros(len(converters), dtype=np.complex128)
        current_by_bus = np.zeros(layout.bus_count, dtype=np.complex128)
        for position, converter_index in enumerate(layout.active_converter_indices):
            converter = converters[converter_index]
            current = active_currents[position]
            full_currents[converter_index] = current
            current_by_bus[converter.bus] += current
        for converter_index, converter in enumerate(converters):
            if converter_index in layout.active_converter_indices:
                continue
            full_currents[converter_index] = (network_matrix @ voltages - current_by_bus)[converter.bus]
        return full_currents

    def _reference_converter_index(self, converters: list[VSCConverterSpec], slack_bus: int) -> int | None:
        for index, converter in enumerate(converters):
            if converter.control_mode == "GFM" and converter.bus == slack_bus:
                return index
        return None

    def _evaluate_residual(
        self,
        state_vector: NDArray[np.float64],
        network_matrix: NDArray[np.complex128],
        slack_bus: int,
        slack_voltage: complex,
        converters: list[VSCConverterSpec],
        modes: list[ModeName],
        layout: NewtonStateLayout,
    ) -> NDArray[np.float64]:
        voltages, active_currents = self._decode_solution(state_vector, layout)
        currents = self._expand_currents(voltages, active_currents, network_matrix, converters, layout)
        # Network balance: I_injected = Y @ V
        current_by_bus = np.zeros(layout.bus_count, dtype=np.complex128)
        for index, converter in enumerate(converters):
            current_by_bus[converter.bus] += currents[index]
        network_balance = network_matrix @ voltages - current_by_bus
        # Residual structure:
        # - Network equations for non-slack buses: 2*(n_bus-1) equations
        # - Slack bus: NO network equation (replaced by reference converter equations)
        # - All converter equations: 2*n_conv equations
        # Total: 2*(n_bus-1) + 2*n_conv = 2*(n_bus + n_conv - 1) ✓
        residual = np.zeros(2 * len(layout.non_reference_buses) + self._control_row_count(layout), dtype=np.float64)
        # Network equations for non-slack buses
        row = 0
        for bus in layout.non_reference_buses:
            residual[row] = network_balance[bus].real
            residual[row + len(layout.non_reference_buses)] = network_balance[bus].imag
            row += 1
        # Reference converter equations (replaces slack bus network equations)
        row = 2 * len(layout.non_reference_buses)
        reference_converter_index = self._reference_converter_index(converters, slack_bus)
        if reference_converter_index is None:
            # No reference converter: fix V[slack] = slack_voltage
            residual[row] = voltages[slack_bus].real - slack_voltage.real
            residual[row + 1] = voltages[slack_bus].imag - slack_voltage.imag
        else:
            ref_conv = converters[reference_converter_index]
            I_ref = currents[reference_converter_index]
            if modes[reference_converter_index] == "USS":
                # Fix V[slack] magnitude = u_ref (angle free, defaults to 0)
                residual[row] = abs(voltages[slack_bus]) - ref_conv.u_ref
            else:
                # FSS/PSS: |I_ref| = I_max
                residual[row] = I_ref.real**2 + I_ref.imag**2 - ref_conv.i_max**2
            # Second equation for slack bus with GFM converter
            if ref_conv.control_mode == "GFM" and modes[reference_converter_index] == "FSS":
                # GFM-FSS: P = 0 (gives up active power), angle fixed at 0
                v_slack = voltages[slack_bus]
                residual[row + 1] = v_slack.real * I_ref.real + v_slack.imag * I_ref.imag  # P = 0
            else:
                # For non-GFM or USS: fix angle at 0 (slack reference)
                residual[row + 1] = voltages[slack_bus].imag  # V_imag = 0
        row += 2
        # Non-reference converter equations
        for position, converter_index in enumerate(layout.active_converter_indices):
            converter = converters[converter_index]
            del position
            voltage = voltages[converter.bus]
            current = currents[converter_index]
            active_power = voltage.real * current.real + voltage.imag * current.imag
            reactive_power = voltage.imag * current.real - voltage.real * current.imag
            current_square = current.real**2 + current.imag**2
            mode = modes[converter_index]
            if mode == "USS":
                residual[row] = active_power - converter.p_ref
                row += 1
                if converter.control_mode == "PV":
                    residual[row] = abs(voltage) - converter.u_ref
                elif converter.control_mode == "GS":
                    residual[row] = reactive_power - (converter.q_ref + converter.k_isp * (converter.u_ref_gs - abs(voltage)))
                else:
                    residual[row] = reactive_power - converter.q_ref
                row += 1
            elif mode == "PSS":
                # PSS: |I| = I_max, P = P_ref
                residual[row] = current_square - converter.i_max**2
                residual[row + 1] = active_power - converter.p_ref  # P = P_ref
                row += 2
            else:  # FSS
                # FSS: |I| = I_max, P = 0 (give up active power)
                residual[row] = current_square - converter.i_max**2
                if converter.control_mode == "PV":
                    residual[row + 1] = active_power  # P = 0 for PV-FSS
                else:
                    # GFM-FSS: Q = 0 (pure active, power factor = 1.0)
                    residual[row + 1] = reactive_power  # Q = 0
                row += 2
        return residual

    def _assemble_jacobian(
        self,
        state_vector: NDArray[np.float64],
        network_matrix: NDArray[np.complex128],
        slack_bus: int,
        slack_voltage: complex,
        converters: list[VSCConverterSpec],
        modes: list[ModeName],
        layout: NewtonStateLayout,
    ) -> NDArray[np.float64]:
        del slack_voltage
        voltages, active_currents = self._decode_solution(state_vector, layout)
        currents = self._expand_currents(voltages, active_currents, network_matrix, converters, layout)
        residual_count = 2 * len(layout.non_reference_buses) + self._control_row_count(layout)
        variable_count = int(layout.current_imag_slice.stop or 0)
        jacobian = np.zeros((residual_count, variable_count), dtype=np.float64)
        vr_start = layout.voltage_real_slice.start
        vi_start = layout.voltage_imag_slice.start
        ir_start = layout.current_real_slice.start
        ii_start = layout.current_imag_slice.start
        non_reference_count = len(layout.non_reference_buses)
        bus_row_position = {bus: position for position, bus in enumerate(layout.non_reference_buses)}

        for row_bus in layout.non_reference_buses:
            row_position = bus_row_position[row_bus]
            for col_bus in range(layout.bus_count):
                admittance = network_matrix[row_bus, col_bus]
                jacobian[row_position, vr_start + col_bus] = admittance.real
                jacobian[row_position, vi_start + col_bus] = -admittance.imag
                jacobian[non_reference_count + row_position, vr_start + col_bus] = admittance.imag
                jacobian[non_reference_count + row_position, vi_start + col_bus] = admittance.real

        for position, converter_index in enumerate(layout.active_converter_indices):
            converter = converters[converter_index]
            if converter.bus == slack_bus:
                continue
            row_position = bus_row_position[converter.bus]
            jacobian[row_position, ir_start + position] -= 1.0
            jacobian[non_reference_count + row_position, ii_start + position] -= 1.0

        row = 2 * non_reference_count
        reference_converter_index = self._reference_converter_index(converters, slack_bus)
        if reference_converter_index is None:
            jacobian[row, vr_start + slack_bus] = 1.0
            jacobian[row + 1, vi_start + slack_bus] = 1.0
        else:
            reference_converter = converters[reference_converter_index]
            if modes[reference_converter_index] == "USS":
                # |V[slack]| - u_ref = 0
                # d|V|/dV_real = V_real / |V|, d|V|/dV_imag = V_imag / |V|
                v_mag = max(abs(voltages[slack_bus]), 1e-12)
                jacobian[row, vr_start + slack_bus] = voltages[slack_bus].real / v_mag
                jacobian[row, vi_start + slack_bus] = voltages[slack_bus].imag / v_mag
            else:
                # FSS for reference converter: |I_ref|² - I_max² = 0
                # I_ref = Y[slack, :] @ V (computed from network, not a state variable)
                # d|I_ref|²/dV_r[j] = 2*(I_r*Y[slack,j].real + I_i*Y[slack,j].imag)
                ref_current = currents[reference_converter_index]
                for col_bus in range(layout.bus_count):
                    y = network_matrix[slack_bus, col_bus]
                    jacobian[row, vr_start + col_bus] = 2.0 * (ref_current.real * y.real + ref_current.imag * y.imag)
                    jacobian[row, vi_start + col_bus] = 2.0 * (ref_current.imag * y.real - ref_current.real * y.imag)
            # Second row: GFM-FSS: P=0 (gives up active power); non-GFM: V_imag=0
            if reference_converter.control_mode == "GFM" and modes[reference_converter_index] == "FSS":
                ref_current = currents[reference_converter_index]
                ref_voltage = voltages[slack_bus]
                for col_bus in range(layout.bus_count):
                    y = network_matrix[slack_bus, col_bus]
                    jacobian[row + 1, vr_start + col_bus] = (
                        (ref_current.real if col_bus == slack_bus else 0.0) + ref_voltage.real * y.real + ref_voltage.imag * y.imag
                    )
                    jacobian[row + 1, vi_start + col_bus] = (
                        (ref_current.imag if col_bus == slack_bus else 0.0) + ref_voltage.real * (-y.imag) + ref_voltage.imag * y.real
                    )
            else:
                jacobian[row + 1, vi_start + slack_bus] = 1.0
        row += 2

        for position, converter_index in enumerate(layout.active_converter_indices):
            converter = converters[converter_index]
            voltage = voltages[converter.bus]
            current = currents[converter_index]
            vr_col = vr_start + converter.bus
            vi_col = vi_start + converter.bus
            ir_col = ir_start + position
            ii_col = ii_start + position
            mode = modes[converter_index]
            if mode == "USS":
                jacobian[row, vr_col] = current.real
                jacobian[row, vi_col] = current.imag
                jacobian[row, ir_col] = voltage.real
                jacobian[row, ii_col] = voltage.imag
                row += 1
                if converter.control_mode == "PV":
                    voltage_magnitude = max(abs(voltage), 1e-12)
                    jacobian[row, vr_col] = voltage.real / voltage_magnitude
                    jacobian[row, vi_col] = voltage.imag / voltage_magnitude
                elif converter.control_mode == "GS":
                    voltage_magnitude = max(abs(voltage), 1e-12)
                    support_slope = converter.k_isp
                    jacobian[row, vr_col] = -current.imag + support_slope * voltage.real / voltage_magnitude
                    jacobian[row, vi_col] = current.real + support_slope * voltage.imag / voltage_magnitude
                    jacobian[row, ir_col] = voltage.imag
                    jacobian[row, ii_col] = -voltage.real
                else:
                    jacobian[row, vr_col] = -current.imag
                    jacobian[row, vi_col] = current.real
                    jacobian[row, ir_col] = voltage.imag
                    jacobian[row, ii_col] = -voltage.real
                row += 1
            elif mode == "PSS":
                # PSS = Power-Supporting System: maintain P = P_ref, |I| = I_max
                eps = 1e-8
                jacobian[row, vr_col] = 2.0 * max(abs(current.real), eps)
                jacobian[row, vi_col] = 2.0 * max(abs(current.imag), eps)
                # Second equation: P = P_ref (maintain active power)
                # P = V_r*I_r + V_i*I_i
                jacobian[row + 1, vr_col] = current.real
                jacobian[row + 1, vi_col] = current.imag
                jacobian[row + 1, ir_col] = voltage.real
                jacobian[row + 1, ii_col] = voltage.imag
                row += 2
            else:  # FSS
                # Residual: |I|^2 - I_max^2 = 0
                # Jacobian: d/dvr = 0, d/dvi = 0, d/dir = 2*I_r, d/dii = 2*I_i
                eps = 1e-8
                jacobian[row, vr_col] = 0.0
                jacobian[row, vi_col] = 0.0
                jacobian[row, ir_col] = 2.0 * max(abs(current.real), eps)
                jacobian[row, ii_col] = 2.0 * max(abs(current.imag), eps)
                # Second equation
                if converter.control_mode == "PV":
                    # P = 0: dP/dvr = current.real, dP/dvi = current.imag
                    jacobian[row + 1, vr_col] = current.real
                    jacobian[row + 1, vi_col] = current.imag
                    jacobian[row + 1, ir_col] = voltage.real
                    jacobian[row + 1, ii_col] = voltage.imag
                elif converter.control_mode == "GFM":
                    # Q = 0: dQ/dvr = -current.imag, dQ/dvi = current.real
                    jacobian[row + 1, vr_col] = -current.imag
                    jacobian[row + 1, vi_col] = current.real
                    jacobian[row + 1, ir_col] = -voltage.imag
                    jacobian[row + 1, ii_col] = voltage.real
                else:
                    # Default: Q = 0
                    jacobian[row + 1, vr_col] = -current.imag
                    jacobian[row + 1, vi_col] = current.real
                    jacobian[row + 1, ir_col] = -voltage.imag
                    jacobian[row + 1, ii_col] = voltage.real
                row += 2
        return jacobian

    def _classify_modes(
        self,
        converters: list[VSCConverterSpec],
        voltages: NDArray[np.complex128],
        current_injections: NDArray[np.complex128],
        previous_modes: list[ModeName],
    ) -> list[ModeName]:
        classified_modes: list[ModeName] = []
        for index, converter in enumerate(converters):
            current_magnitude = abs(current_injections[index])
            if converter.control_mode == "GFM":
                classified_modes.append("USS" if current_magnitude <= converter.i_max + self.exit_tolerance else "FSS")
                continue
            if current_magnitude <= converter.i_max - self.exit_tolerance:
                classified_modes.append("USS")
                continue
            if previous_modes[index] != "USS" and current_magnitude <= converter.i_max + self.exit_tolerance:
                classified_modes.append(previous_modes[index])
                continue
            # Saturated: current > i_max, need to decide PSS vs FSS
            # Paper logic: PSS = active-power priority, FSS = reactive/fault-support priority
            # For PV converter (VSC2): when saturated, it gives up P and enters FSS
            # For GS converter (VSC3): when saturated, it maintains P with modified Q (PSS)
            if converter.control_mode == "PV":
                # PV converter: saturated -> FSS (gives up active power)
                classified_modes.append("FSS")
            elif converter.control_mode == "GS":
                # GS converter: can be PSS or FSS depending on preference
                classified_modes.append(converter.saturation_preference)
            else:
                # PQ converter: use saturation_preference or default to PSS
                bus_voltage = abs(voltages[converter.bus])
                safe_voltage = max(bus_voltage, 1e-9)
                reactive_threshold = abs(converter.q_ref) / safe_voltage
                if converter.saturation_preference == "FSS" or reactive_threshold >= converter.i_max - self.exit_tolerance:
                    classified_modes.append("FSS")
                else:
                    classified_modes.append("PSS")
        return classified_modes

    def _build_result(
        self,
        outer_iterations: int,
        inner_result: InnerSolveResult,
        converters: list[VSCConverterSpec],
        modes: list[ModeName],
        mode_history: list[dict[int, ModeName]],
        fault_bus: int,
        fault_impedance: complex,
    ) -> SolverResult:
        converter_states: dict[int, ModeName] = {converter.bus: mode for converter, mode in zip(converters, modes)}
        current_injections = {converter.bus: complex(inner_result.current_injections[index]) for index, converter in enumerate(converters)}
        fault_current = inner_result.voltages[fault_bus] / complex(fault_impedance)
        return SolverResult(
            voltages=inner_result.voltages,
            converged=inner_result.converged,
            outer_iterations=outer_iterations,
            inner_iterations=inner_result.iterations,
            iterations=inner_result.iterations,
            max_residual=inner_result.max_residual,
            converter_states=converter_states,
            mode_history=mode_history,
            current_injections=current_injections,
            fault_current=complex(fault_current),
        )


IterativeShortCircuitSolver = PaperFaithfulShortCircuitSolver
VSCConverter = VSCConverterSpec
