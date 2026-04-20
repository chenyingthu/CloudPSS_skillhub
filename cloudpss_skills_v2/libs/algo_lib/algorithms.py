from __future__ import annotations
import math
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
import numpy as np
from cloudpss_skills_v2.libs.data_lib import (
    BranchData,
    BusData,
    BusType,
    FaultData,
    FaultType,
    GeneratorData,
)


class SolverStatus(Enum):
    CONVERGED = "converged"
    NOT_CONVERGED = "not_converged"
    DIVERGED = "diverged"
    FAILED = "failed"


@dataclass
class PowerFlowResult:
    converged: bool = False
    buses: list[BusData] = field(default_factory=list)
    branches: list[BranchData] = field(default_factory=list)
    iterations: int = 0
    max_mismatch_pu: float = 0.0
    status: SolverStatus = SolverStatus.NOT_CONVERGED
    error: str | None = None

    @property
    def is_success(self) -> bool:
        return self.converged and self.status == SolverStatus.CONVERGED

    def to_dict(self) -> dict[str, Any]:
        return {
            "converged": self.converged,
            "iterations": self.iterations,
            "max_mismatch_pu": self.max_mismatch_pu,
            "status": self.status.value
            if isinstance(self.status, Enum)
            else self.status,
            "bus_count": len(self.buses),
            "branch_count": len(self.branches),
            "error": self.error,
        }


@dataclass
class ShortCircuitResult:
    fault_bus: str = ""
    fault_type: FaultType = FaultType.THREE_PHASE
    ikss_ka: float = 0.0
    ip_ka: float = 0.0
    ith_ka: float = 0.0
    skss_mva: float = 0.0
    buses: list[BusData] = field(default_factory=list)
    error: str | None = None

    @property
    def is_success(self) -> bool:
        return self.error is None and self.ikss_ka > 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "fault_bus": self.fault_bus,
            "fault_type": self.fault_type.value
            if isinstance(self.fault_type, Enum)
            else self.fault_type,
            "ikss_ka": self.ikss_ka,
            "ip_ka": self.ip_ka,
            "ith_ka": self.ith_ka,
            "skss_mva": self.skss_mva,
        }


class PowerFlowSolver(ABC):
    @abstractmethod
    def solve(
        self,
        buses: list[BusData],
        branches: list[BranchData],
        generators: list[GeneratorData] | None = None,
        base_mva: float = 100.0,
        tolerance: float = 1e-6,
        max_iterations: int = 100,
    ) -> PowerFlowResult: ...


def _build_y_bus(buses: list[BusData], branches: list[BranchData]) -> np.ndarray:
    n = len(buses)
    bus_idx = {b.name: i for i, b in enumerate(buses)}
    y_bus = np.zeros((n, n), dtype=complex)
    for branch in branches:
        if not branch.in_service:
            continue
        f_idx = bus_idx.get(branch.from_bus)
        t_idx = bus_idx.get(branch.to_bus)
        if f_idx is None or t_idx is None:
            continue
        z = complex(branch.resistance_pu, branch.reactance_pu)
        if abs(z) < 1e-20:
            z = complex(1e-20, 0.0)
        y_series = 1.0 / z
        y_shunt = complex(0.0, branch.susceptance_pu or 0.0) / 2.0
        y_bus[f_idx, f_idx] += y_series + y_shunt
        y_bus[t_idx, t_idx] += y_series + y_shunt
        y_bus[f_idx, t_idx] -= y_series
        y_bus[t_idx, f_idx] -= y_series
    return y_bus


class NewtonRaphsonSolver(PowerFlowSolver):
    def solve(
        self,
        buses: list[BusData],
        branches: list[BranchData],
        generators: list[GeneratorData] | None = None,
        base_mva: float = 100.0,
        tolerance: float = 1e-6,
        max_iterations: int = 100,
    ) -> PowerFlowResult:
        if not buses:
            return PowerFlowResult(
                converged=False,
                buses=[],
                branches=list(branches),
                status=SolverStatus.FAILED,
                error="No buses provided",
            )
        if not any(b.bus_type == BusType.SLACK for b in buses):
            return PowerFlowResult(
                converged=False,
                buses=list(buses),
                branches=list(branches),
                status=SolverStatus.FAILED,
                error="No slack bus found",
            )
        generators = generators or []
        n = len(buses)
        y_bus = _build_y_bus(buses, branches)
        g = y_bus.real
        b = y_bus.imag
        v = np.array([b.voltage_pu if b.voltage_pu is not None else 1.0 for b in buses])
        theta = np.array([math.radians(b.angle_deg) for b in buses])
        p_sched = np.zeros(n)
        q_sched = np.zeros(n)
        for i, bus in enumerate(buses):
            p_sched[i] = -bus.load_mw / base_mva
            q_sched[i] = -bus.load_mvar / base_mva
        for gen in generators:
            if not gen.in_service:
                continue
            for i, bus in enumerate(buses):
                if bus.name == gen.bus:
                    p_sched[i] += gen.p_mw / base_mva
                    break
        p_indices = [i for i, bus in enumerate(buses) if bus.bus_type != BusType.SLACK]
        q_indices = [i for i, bus in enumerate(buses) if bus.bus_type == BusType.PQ]
        n_p = len(p_indices)
        n_q = len(q_indices)
        converged = False
        iterations = 0
        max_mismatch = float("inf")
        for iteration in range(max_iterations):
            p_calc = np.zeros(n)
            q_calc = np.zeros(n)
            for j in range(n):
                for k in range(n):
                    theta_jk = theta[j] - theta[k]
                    p_calc[j] += (
                        v[j]
                        * v[k]
                        * (g[j, k] * math.cos(theta_jk) + b[j, k] * math.sin(theta_jk))
                    )
                    q_calc[j] += (
                        v[j]
                        * v[k]
                        * (g[j, k] * math.sin(theta_jk) - b[j, k] * math.cos(theta_jk))
                    )
            dp = p_sched - p_calc
            dq = q_sched - q_calc
            dp_vec = dp[p_indices]
            dq_vec = dq[q_indices]
            mismatch = np.concatenate([dp_vec, dq_vec])
            max_mismatch = max(abs(mismatch)) if len(mismatch) > 0 else 0.0
            if max_mismatch < tolerance:
                converged = True
                iterations = iteration + 1
                break
            jacobian = np.zeros((n_p + n_q, n_p + n_q))
            for pi, j in enumerate(p_indices):
                for pj, k in enumerate(p_indices):
                    if j == k:
                        jacobian[pi, pj] = -q_calc[j] - v[j] ** 2 * b[j, j]
                    else:
                        theta_jk = theta[j] - theta[k]
                        jacobian[pi, pj] = (
                            v[j]
                            * v[k]
                            * (
                                g[j, k] * math.sin(theta_jk)
                                - b[j, k] * math.cos(theta_jk)
                            )
                        )
            for qi, j in enumerate(q_indices):
                for pj, k in enumerate(p_indices):
                    if j == k:
                        jacobian[n_p + qi, pj] = p_calc[j] - v[j] ** 2 * g[j, j]
                    else:
                        theta_jk = theta[j] - theta[k]
                        jacobian[n_p + qi, pj] = (
                            v[j]
                            * v[k]
                            * (
                                g[j, k] * math.cos(theta_jk)
                                + b[j, k] * math.sin(theta_jk)
                            )
                        )
            for pi, j in enumerate(p_indices):
                for qi, k in enumerate(q_indices):
                    if j == k:
                        jacobian[pi, n_p + qi] = p_calc[j] / v[j] + v[j] * g[j, j]
                    else:
                        jacobian[pi, n_p + qi] = v[j] * (
                            g[j, k] * math.cos(theta[j] - theta[k])
                            + b[j, k] * math.sin(theta[j] - theta[k])
                        )
            for qi, j in enumerate(q_indices):
                for qi2, k in enumerate(q_indices):
                    if j == k:
                        jacobian[n_p + qi, n_p + qi2] = (
                            q_calc[j] / v[j] - v[j] * b[j, j]
                        )
                    else:
                        jacobian[n_p + qi, n_p + qi2] = v[j] * (
                            g[j, k] * math.sin(theta[j] - theta[k])
                            - b[j, k] * math.cos(theta[j] - theta[k])
                        )
            try:
                correction = np.linalg.solve(jacobian, mismatch)
            except np.linalg.LinAlgError:
                return PowerFlowResult(
                    converged=False,
                    buses=list(buses),
                    branches=list(branches),
                    iterations=iteration + 1,
                    status=SolverStatus.FAILED,
                    error="Jacobian singular",
                )
            for i, idx in enumerate(p_indices):
                theta[idx] += correction[i]
            for i, idx in enumerate(q_indices):
                v[idx] += correction[n_p + i]
                v[idx] = np.clip(v[idx], 0.5, 1.5)
        if not converged:
            status = (
                SolverStatus.DIVERGED
                if max_mismatch > 10.0
                else SolverStatus.NOT_CONVERGED
            )
            return PowerFlowResult(
                converged=False,
                buses=list(buses),
                branches=list(branches),
                iterations=iterations,
                max_mismatch_pu=max_mismatch,
                status=status,
            )
        result_buses = NewtonRaphsonSolver._build_result_buses(buses, v, theta)
        result_branches = NewtonRaphsonSolver._build_result_branches(
            buses, branches, v, theta, base_mva
        )
        return PowerFlowResult(
            converged=True,
            buses=result_buses,
            branches=result_branches,
            iterations=iterations,
            max_mismatch_pu=max_mismatch,
            status=SolverStatus.CONVERGED,
        )

    @staticmethod
    def _build_result_buses(buses, v, theta):
        result = []
        for i, bus in enumerate(buses):
            result.append(
                BusData(
                    name=bus.name,
                    voltage_kv=bus.voltage_kv,
                    bus_type=bus.bus_type,
                    voltage_pu=float(v[i]),
                    angle_deg=float(math.degrees(theta[i])),
                    load_mw=bus.load_mw,
                    load_mvar=bus.load_mvar,
                    generation_mw=bus.generation_mw,
                    generation_mvar=bus.generation_mvar,
                    v_min_pu=bus.v_min_pu,
                    v_max_pu=bus.v_max_pu,
                    zone=bus.zone,
                    area=bus.area,
                    engine_id=bus.engine_id,
                )
            )
        return result

    @staticmethod
    def _build_result_branches(buses, branches, v, theta, base_mva):
        bus_idx = {b.name: i for i, b in enumerate(buses)}
        result = []
        for branch in branches:
            f_idx = bus_idx.get(branch.from_bus)
            t_idx = bus_idx.get(branch.to_bus)
            if f_idx is None or t_idx is None or not branch.in_service:
                continue
            z_br = complex(branch.resistance_pu or 0, branch.reactance_pu or 0)
            if abs(z_br) < 1e-20:
                z_br = complex(1e-20, 0)
            v_f = v[f_idx] * np.exp(1j * theta[f_idx])
            v_t = v[t_idx] * np.exp(1j * theta[t_idx])
            i_from = (v_f - v_t) / z_br + v_f * complex(
                0, branch.susceptance_pu or 0
            ) / 2
            i_to = (v_t - v_f) / z_br + v_t * complex(0, branch.susceptance_pu or 0) / 2
            s_from = v_f * np.conj(i_from) * base_mva
            s_to = v_t * np.conj(i_to) * base_mva
            loading = None
            if branch.rating_mva and branch.rating_mva > 0:
                s_mva = max(abs(s_from), abs(s_to))
                loading = s_mva / branch.rating_mva * 100.0
            result.append(
                BranchData(
                    name=branch.name,
                    from_bus=branch.from_bus,
                    to_bus=branch.to_bus,
                    branch_type=branch.branch_type,
                    resistance_pu=branch.resistance_pu,
                    reactance_pu=branch.reactance_pu,
                    susceptance_pu=branch.susceptance_pu,
                    rating_mva=branch.rating_mva,
                    loading_pct=loading,
                    p_from_mw=float(s_from.real),
                    q_from_mvar=float(s_from.imag),
                    p_to_mw=float(s_to.real),
                    q_to_mvar=float(s_to.imag),
                    tap_ratio=branch.tap_ratio,
                    phase_shift_deg=branch.phase_shift_deg,
                    in_service=branch.in_service,
                    engine_id=branch.engine_id,
                )
            )
        return result


class FastDecoupledSolver(PowerFlowSolver):
    def solve(
        self,
        buses: list[BusData],
        branches: list[BranchData],
        generators: list[GeneratorData] | None = None,
        base_mva: float = 100.0,
        tolerance: float = 1e-6,
        max_iterations: int = 100,
    ) -> PowerFlowResult:
        if not buses:
            return PowerFlowResult(
                converged=False,
                buses=[],
                branches=list(branches),
                status=SolverStatus.FAILED,
                error="No buses provided",
            )
        if not any(b.bus_type == BusType.SLACK for b in buses):
            return PowerFlowResult(
                converged=False,
                buses=list(buses),
                branches=list(branches),
                status=SolverStatus.FAILED,
                error="No slack bus found",
            )
        generators = generators or []
        n = len(buses)
        bus_idx_map = {b.name: i for i, b in enumerate(buses)}
        y_bus = _build_y_bus(buses, branches)
        b_prime = np.zeros((n, n))
        for branch in branches:
            if not branch.in_service:
                continue
            f = bus_idx_map.get(branch.from_bus)
            t = bus_idx_map.get(branch.to_bus)
            if f is None or t is None:
                continue
            x = abs(branch.reactance_pu) if abs(branch.reactance_pu) > 1e-14 else 1e-14
            b_prime[f, f] -= 1.0 / x
            b_prime[t, t] -= 1.0 / x
            b_prime[f, t] += 1.0 / x
            b_prime[t, f] += 1.0 / x
        b_double_prime = -y_bus.imag.copy()
        p_indices = [i for i, b in enumerate(buses) if b.bus_type != BusType.SLACK]
        q_indices = [i for i, b in enumerate(buses) if b.bus_type == BusType.PQ]
        b_p = b_prime[np.ix_(p_indices, p_indices)]
        b_q = b_double_prime[np.ix_(q_indices, q_indices)]
        try:
            b_p_inv = np.linalg.inv(b_p)
            b_q_inv = np.linalg.inv(b_q)
        except np.linalg.LinAlgError:
            return PowerFlowResult(
                converged=False,
                buses=list(buses),
                branches=list(branches),
                status=SolverStatus.FAILED,
                error="B-matrix singular",
            )
        v = np.array([b.voltage_pu if b.voltage_pu is not None else 1.0 for b in buses])
        theta = np.array([math.radians(b.angle_deg) for b in buses])
        g = y_bus.real
        p_sched = np.zeros(n)
        q_sched = np.zeros(n)
        for i, bus in enumerate(buses):
            p_sched[i] = -bus.load_mw / base_mva
            q_sched[i] = -bus.load_mvar / base_mva
        for gen in generators:
            if not gen.in_service:
                continue
            for i, bus in enumerate(buses):
                if bus.name == gen.bus:
                    p_sched[i] += gen.p_mw / base_mva
                    break
        converged = False
        iterations = 0
        max_mismatch = float("inf")
        for iteration in range(max_iterations):
            p_calc = np.zeros(n)
            q_calc = np.zeros(n)
            for j in range(n):
                for k in range(n):
                    theta_jk = theta[j] - theta[k]
                    p_calc[j] += (
                        v[j]
                        * v[k]
                        * (
                            g[j, k] * math.cos(theta_jk)
                            + y_bus.imag[j, k] * math.sin(theta_jk)
                        )
                    )
                    q_calc[j] += (
                        v[j]
                        * v[k]
                        * (
                            g[j, k] * math.sin(theta_jk)
                            - y_bus.imag[j, k] * math.cos(theta_jk)
                        )
                    )
            dp = p_sched - p_calc
            dq = q_sched - q_calc
            dp_vec = dp[p_indices] / v[p_indices]
            dq_vec = dq[q_indices] / v[q_indices]
            mismatch = np.concatenate([dp_vec, dq_vec])
            max_mismatch = max(abs(mismatch)) if len(mismatch) > 0 else 0.0
            if max_mismatch < tolerance:
                converged = True
                iterations = iteration + 1
                break
            d_theta = b_p_inv @ dp_vec
            for idx, pi in enumerate(p_indices):
                theta[pi] += d_theta[idx]
            d_v = b_q_inv @ dq_vec
            for idx, qi in enumerate(q_indices):
                v[qi] += d_v[idx]
                v[qi] = np.clip(v[qi], 0.5, 1.5)
        if not converged:
            status = (
                SolverStatus.DIVERGED
                if max_mismatch > 10.0
                else SolverStatus.NOT_CONVERGED
            )
            return PowerFlowResult(
                converged=False,
                buses=list(buses),
                branches=list(branches),
                iterations=iterations,
                max_mismatch_pu=max_mismatch,
                status=status,
            )
        result_buses = NewtonRaphsonSolver._build_result_buses(buses, v, theta)
        result_branches = NewtonRaphsonSolver._build_result_branches(
            buses, branches, v, theta, base_mva
        )
        return PowerFlowResult(
            converged=True,
            buses=result_buses,
            branches=result_branches,
            iterations=iterations,
            max_mismatch_pu=max_mismatch,
            status=SolverStatus.CONVERGED,
        )


class IEC60909Calculator:
    def calculate(
        self,
        fault: FaultData,
        buses: list[BusData],
        branches: list[BranchData],
        generators: list[GeneratorData] | None = None,
        base_mva: float = 100.0,
        frequency_hz: float = 50.0,
    ) -> ShortCircuitResult:
        generators = generators or []
        bus_idx = {b.name: i for i, b in enumerate(buses)}
        y_bus = _build_y_bus(buses, branches)
        for gen in generators:
            if not gen.in_service or gen.xd_tr_pu is None:
                continue
            g_idx = bus_idx.get(gen.bus)
            if g_idx is not None:
                y_bus[g_idx, g_idx] += complex(0.2, 0.0) / complex(0.0, gen.xd_tr_pu)
        fault_idx = bus_idx.get(fault.bus)
        if fault_idx is None:
            return ShortCircuitResult(
                fault_bus=fault.bus,
                fault_type=fault.fault_type,
                error=f"Fault bus '{fault.bus}' not found in model",
            )
        z_fault_pu = complex(fault.r_f_ohm, fault.x_f_ohm)
        if fault_idx < y_bus.shape[0]:
            y_bus[fault_idx, fault_idx] += (
                1.0 / z_fault_pu if abs(z_fault_pu) > 0 else complex(0.0, -1.0)
            )
        try:
            z_th = 1.0 / y_bus[fault_idx, fault_idx]
        except (IndexError, ZeroDivisionError):
            return ShortCircuitResult(
                fault_bus=fault.bus,
                fault_type=fault.fault_type,
                error="Total impedance too small",
            )
        v_kv = buses[fault_idx].voltage_kv
        base_z = v_kv**2 / base_mva
        if fault.fault_type == FaultType.THREE_PHASE:
            c_factor = 1.1
        elif fault.fault_type in (
            FaultType.SINGLE_LINE_TO_GROUND,
            FaultType.LINE_TO_LINE,
        ):
            c_factor = 1.02
        else:
            c_factor = 0.98
        v_source_pu = c_factor
        ikss_pu = v_source_pu / abs(z_th)
        base_ka = base_mva / (v_kv * math.sqrt(3)) if v_kv > 0 else 0
        ikss_ka = ikss_pu * base_ka
        r_over_x = z_th.real / abs(z_th.imag) if abs(z_th.imag) > 0 else 0
        kappa = 1.0 + 0.02 * math.exp(-0.3 * r_over_x)
        if r_over_x >= 0:
            kappa = min(kappa, 1.8 + 0.1)
            kappa = max(kappa, 1.0)
        ip_ka = math.sqrt(2) * kappa * ikss_ka
        t_k = 0.05
        m = (
            math.exp(-2 * math.pi * frequency_hz * t_k * r_over_x)
            if r_over_x > 0
            else 0
        )
        ith_ka = ikss_ka * math.sqrt(1 + 2 * (kappa - 1) ** 2)
        skss_mva = math.sqrt(3) * v_kv * ikss_ka
        return ShortCircuitResult(
            fault_bus=fault.bus,
            fault_type=fault.fault_type,
            ikss_ka=ikss_ka,
            ip_ka=ip_ka,
            ith_ka=ith_ka,
            skss_mva=skss_mva,
        )


__all__ = [
    "SolverStatus",
    "PowerFlowResult",
    "ShortCircuitResult",
    "PowerFlowSolver",
    "NewtonRaphsonSolver",
    "FastDecoupledSolver",
    "IEC60909Calculator",
]
