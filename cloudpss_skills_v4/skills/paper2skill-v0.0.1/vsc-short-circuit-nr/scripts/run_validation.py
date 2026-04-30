import json
import importlib.util
import sys
from pathlib import Path
from typing import Any, Protocol, cast

import numpy as np
from numpy.linalg import LinAlgError
from numpy.typing import NDArray


def _load_local_module(module_name: str, file_name: str):
    module_path = Path(__file__).resolve().with_name(file_name)
    module_spec = importlib.util.spec_from_file_location(module_name, module_path)
    if module_spec is None or module_spec.loader is None:
        raise ImportError(f"Unable to load module from {module_path}")
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module


class ScenariosModule(Protocol):
    PAPER_VALIDATION_TARGETS: dict[str, Any]
    LOCAL_VALIDATION_SCENARIOS: dict[str, Any]
    MISSING_REPRODUCTION_PARAMETERS: dict[str, Any]
    TEST_SYSTEM_2_FAULT_BUS: int
    TEST_SYSTEM_2_FAULT_BUS_KV_ASSUMPTION: float
    TEST_SYSTEM_2_SYSTEM_BASE_MVA: float
    TEST_SYSTEM_2_VSC_BUSES: list[int]

    def build_ieee14_admittance_matrix(self) -> tuple[NDArray[Any], int]: ...
    def build_ieee14_full_admittance_matrix(self) -> tuple[NDArray[Any], int]: ...
    def get_test_system_2_converters(self, penetration_capacity_mva: float, system_base_mva: float = ...) -> list[dict[str, Any]]: ...
    def per_unit_current_to_ka(self, current_pu: float, system_base_mva: float, voltage_base_kv: float) -> float: ...


class SolverModule(Protocol):
    VSCConverter: type[Any]
    PaperFaithfulShortCircuitSolver: type[Any]


class ReconstructionModule(Protocol):
    def load_test_system_1_artifact(self) -> dict[str, Any]: ...
    def build_test_system_1_admittance_matrix(self, islanded: bool = True) -> tuple[NDArray[Any], int, dict[str, int]]: ...
    def get_paper_vsc_converters(self, bus_index: dict[str, int] | None = None) -> list[dict[str, Any]]: ...
    def summarize_test_system_1_artifact(self) -> dict[str, Any]: ...


_scenarios = cast(ScenariosModule, cast(object, _load_local_module("vsc_sc_scenarios", "scenarios.py")))
_solver_module = cast(SolverModule, cast(object, _load_local_module("vsc_sc_solver", "vsc_nr_solver.py")))
_reconstruction_module = cast(
    ReconstructionModule,
    cast(object, _load_local_module("vsc_sc_ts1_reconstruction", "test_system_1_reconstruction.py")),
)

PAPER_VALIDATION_TARGETS = _scenarios.PAPER_VALIDATION_TARGETS
LOCAL_VALIDATION_SCENARIOS = _scenarios.LOCAL_VALIDATION_SCENARIOS
MISSING_REPRODUCTION_PARAMETERS = _scenarios.MISSING_REPRODUCTION_PARAMETERS
build_ieee14_admittance_matrix = _scenarios.build_ieee14_admittance_matrix
build_ieee14_full_admittance_matrix = _scenarios.build_ieee14_full_admittance_matrix
get_test_system_2_converters = _scenarios.get_test_system_2_converters
per_unit_current_to_ka = _scenarios.per_unit_current_to_ka
TEST_SYSTEM_2_FAULT_BUS = _scenarios.TEST_SYSTEM_2_FAULT_BUS
TEST_SYSTEM_2_FAULT_BUS_KV_ASSUMPTION = _scenarios.TEST_SYSTEM_2_FAULT_BUS_KV_ASSUMPTION
TEST_SYSTEM_2_SYSTEM_BASE_MVA = _scenarios.TEST_SYSTEM_2_SYSTEM_BASE_MVA
TEST_SYSTEM_2_VSC_BUSES = _scenarios.TEST_SYSTEM_2_VSC_BUSES
PaperFaithfulShortCircuitSolver = _solver_module.PaperFaithfulShortCircuitSolver
VSCConverter = _solver_module.VSCConverter
build_test_system_1_admittance_matrix = _reconstruction_module.build_test_system_1_admittance_matrix
get_paper_vsc_converters = _reconstruction_module.get_paper_vsc_converters
summarize_test_system_1_artifact = _reconstruction_module.summarize_test_system_1_artifact
load_test_system_1_artifact = _reconstruction_module.load_test_system_1_artifact


def _compare_current(target_pu: float, actual_pu: float, label: str, tolerance: float = 0.05) -> bool:
    error_pct = abs(actual_pu - target_pu) / max(target_pu, 1e-9) * 100
    status = "PASS" if error_pct <= tolerance * 100 else "FAIL"
    print(f"  [{status}] {label}: target={target_pu:.4f} pu, got={actual_pu:.4f} pu, error={error_pct:.1f}%")
    return error_pct <= tolerance * 100


def _parse_fault_impedance(value: str) -> complex:
    return complex(0, float(value[1:])) if value.startswith("j") else complex(value)


def _format_voltage(voltage: complex) -> str:
    return f"{abs(voltage):.4f}∠{np.angle(voltage, deg=True):.1f}°"


def evaluate_test_system_1_regression(verbose: bool = True) -> dict[str, Any]:
    if verbose:
        print("=" * 60)
        print("Test System 1 Strict Regression Against Paper Tables")
        print("=" * 60)

    ybus, slack_bus, bus_index = build_test_system_1_admittance_matrix(islanded=True)
    artifact = load_test_system_1_artifact()
    paper_converters = get_paper_vsc_converters(bus_index)
    converters = [VSCConverter(**spec) for spec in paper_converters]
    fault_bus = bus_index[artifact["test_system_1"]["fault_bus"]]
    converter_bus_by_id = {
        converter["id"]: bus_index[converter["bus"]]
        for converter in artifact["test_system_1"]["converters"]
    }

    if verbose:
        print(f"\nAdmittance matrix: {ybus.shape}, slack_bus={slack_bus} (bus1, islanded mode)")
        print(f"Converters: {len(converters)}")
        for i, c in enumerate(converters):
            print(f"  VSC{i+1}: bus={c.bus}, p_ref={c.p_ref}, q_ref={c.q_ref}, i_max={c.i_max}")

    targets = PAPER_VALIDATION_TARGETS["test_system_1"]
    solver = PaperFaithfulShortCircuitSolver(tolerance=1e-8, max_iter=100, max_outer_iter=20)
    strict_cases = [
        ("moderate_fault", "moderate_fault_table"),
        ("severe_fault", "severe_fault_table"),
    ]
    case_results = []
    all_pass = True

    for case_name, table_key in strict_cases:
        table = targets[table_key]
        fault_str = table["fault_impedance_pu"]
        fault_impedance = _parse_fault_impedance(fault_str)
        feasible_target = next(scenario for scenario in table["iterations"] if scenario["feasible"])

        if verbose:
            print(f"\n--- {case_name} (z_ft={fault_str}) ---")
            print(f"Paper feasible iteration {feasible_target['iteration']}: states={feasible_target['vsc_states']}")

        try:
            result = solver.solve(
                admittance_matrix=ybus,
                slack_bus=slack_bus,
                fault_bus=fault_bus,
                fault_impedance=fault_impedance,
                converters=converters,
                slack_voltage=1.0 + 0.0j,
            )
        except LinAlgError as exc:
            if verbose:
                print(f"  [FAIL] Solver error: {exc}")
            case_results.append({"case": case_name, "passed": False, "error": str(exc)})
            all_pass = False
            continue

        if verbose:
            print(f"  Converged: {result.converged}, outer={result.outer_iterations}, inner={result.inner_iterations}")
            print(f"  Mode history: {result.mode_history}")

        if not result.converged:
            if verbose:
                print("  [FAIL] Solver did not converge")
            case_results.append(
                {
                    "case": case_name,
                    "passed": False,
                    "converged": False,
                    "max_residual": result.max_residual,
                    "mode_history": result.mode_history,
                }
            )
            all_pass = False
            continue

        mode_checks = {}
        mode_pass = True
        for converter_id, expected_mode in feasible_target["vsc_states"].items():
            bus_id = converter_bus_by_id[converter_id]
            actual_mode = result.converter_states.get(bus_id)
            passed = actual_mode == expected_mode
            mode_checks[converter_id] = {"expected": expected_mode, "actual": actual_mode, "passed": passed}
            mode_pass = mode_pass and passed
            if verbose:
                status = "PASS" if passed else "FAIL"
                print(f"  [{status}] {converter_id} mode: expected={expected_mode}, got={actual_mode}")

        current_checks = {}
        current_pass = True
        for converter_id in ("VSC1", "VSC2", "VSC3"):
            target_key = f"i_{converter_id.lower()}_pu"
            target_current = float(feasible_target[target_key])
            actual_current = abs(result.current_injections.get(converter_bus_by_id[converter_id], 0.0))
            error_pct = abs(actual_current - target_current) / max(target_current, 1e-9) * 100.0
            passed = error_pct <= 5.0
            current_checks[converter_id] = {
                "expected_pu": target_current,
                "actual_pu": actual_current,
                "error_percent": error_pct,
                "passed": passed,
            }
            current_pass = current_pass and passed
            if verbose:
                status = "PASS" if passed else "FAIL"
                print(
                    f"  [{status}] {converter_id} current: "
                    f"target={target_current:.4f} pu, got={actual_current:.4f} pu, error={error_pct:.1f}%"
                )

        voltage_summary = {
            "u1": _format_voltage(result.voltages[converter_bus_by_id["VSC1"]]),
            "u6": _format_voltage(result.voltages[converter_bus_by_id["VSC2"]]),
            "u12": _format_voltage(result.voltages[fault_bus]),
        }
        if verbose:
            print(f"  Voltages: {voltage_summary}")

        case_pass = result.converged and mode_pass and current_pass
        all_pass = all_pass and case_pass
        case_results.append(
            {
                "case": case_name,
                "passed": case_pass,
                "converged": result.converged,
                "max_residual": result.max_residual,
                "mode_checks": mode_checks,
                "current_checks": current_checks,
                "voltage_summary": voltage_summary,
                "mode_history": result.mode_history,
            }
        )

    if verbose:
        print(f"\n{'=' * 60}")
        print(f"Overall: {'ALL PASS' if all_pass else 'SOME FAILURES'}")
        print(f"{'=' * 60}")

    return {
        "passed": all_pass,
        "cases": case_results,
        "blocking_reason": None
        if all_pass
        else "paper-exact Test System 1 network/base data are not yet reconstructed well enough for numerical reproduction",
    }


def run_test_system_1_regression() -> bool:
    return bool(evaluate_test_system_1_regression(verbose=True)["passed"])


def evaluate_test_system_2_probe(verbose: bool = True) -> dict[str, Any]:
    if verbose:
        print("=" * 60)
        print("Test System 2 IEEE14 Probe Against Paper Tables")
        print("=" * 60)

    ybus, slack_bus = build_ieee14_full_admittance_matrix()
    solver = PaperFaithfulShortCircuitSolver(tolerance=1e-8, max_iter=200, max_outer_iter=20)
    targets = PAPER_VALIDATION_TARGETS["test_system_2"]
    max_error_percent = float(targets["method_level_acceptance"]["max_error_percent"])
    cases = []
    for label, capacity_mva in targets["table_10_parameters"]["penetration_capacity_mva"].items():
        converters = [
            VSCConverter(**converter_definition)
            for converter_definition in get_test_system_2_converters(float(capacity_mva))
        ]
        result = solver.solve(
            admittance_matrix=ybus,
            slack_bus=slack_bus,
            fault_bus=TEST_SYSTEM_2_FAULT_BUS,
            fault_impedance=1e-6j,
            converters=converters,
            slack_voltage=1.0 + 0.0j,
        )
        fault_current_pu = abs(result.fault_current)
        fault_current_ka = per_unit_current_to_ka(
            fault_current_pu,
            TEST_SYSTEM_2_SYSTEM_BASE_MVA,
            TEST_SYSTEM_2_FAULT_BUS_KV_ASSUMPTION,
        )
        target_ka = float(targets["short_circuit_tables"][label]["this_paper_ka"])
        error_percent = abs(fault_current_ka - target_ka) / max(target_ka, 1e-9) * 100.0
        case = {
            "case": label,
            "penetration_capacity_mva": float(capacity_mva),
            "converged": result.converged,
            "fault_current_pu": fault_current_pu,
            "fault_current_ka": fault_current_ka,
            "paper_fault_current_ka": target_ka,
            "error_percent": error_percent,
            "converter_states": {str(bus + 1): state for bus, state in result.converter_states.items()},
            "mode_history": [
                {str(bus + 1): state for bus, state in mode_by_bus.items()}
                for mode_by_bus in result.mode_history
            ],
        }
        cases.append(case)
        if verbose:
            print(
                f"  {label}: got={fault_current_ka:.3f} kA, paper={target_ka:.3f} kA, "
                f"error={error_percent:.1f}%, converged={result.converged}"
            )

    all_converged = all(case["converged"] for case in cases)
    max_observed_error = max(case["error_percent"] for case in cases)
    passed = bool(all_converged and max_observed_error <= max_error_percent)

    return {
        "passed": passed,
        "cases": cases,
        "acceptance": {
            "scope": targets["method_level_acceptance"]["scope"],
            "max_error_percent": max_error_percent,
            "max_observed_error_percent": max_observed_error,
        },
        "assumptions": {
            "ieee14_source": "standard MATPOWER/pandapower IEEE 14 branch data with taps and line charging",
            "vsc_buses_from_figure_4": [bus + 1 for bus in TEST_SYSTEM_2_VSC_BUSES],
            "fault_bus_from_paper": TEST_SYSTEM_2_FAULT_BUS + 1,
            "fault_impedance_pu": "approximated as j1e-6 for bolted u_ft = 0",
            "system_base_mva": TEST_SYSTEM_2_SYSTEM_BASE_MVA,
            "fault_current_voltage_base_kv": TEST_SYSTEM_2_FAULT_BUS_KV_ASSUMPTION,
        },
        "blocking_reason": None
        if passed
        else "Test System 2 method-level reproduction exceeded the documented error bound",
        "strict_reproduction_gap": "PowerFactory transformer data, voltage-base convention, and exact commercial-model setup remain unrecovered",
    }


def main() -> None:
    admittance_matrix, slack_bus = build_ieee14_admittance_matrix()
    solver = PaperFaithfulShortCircuitSolver()
    baseline_definition = LOCAL_VALIDATION_SCENARIOS["baseline_ieee14_fault"]
    vsc_definition = LOCAL_VALIDATION_SCENARIOS["single_vsc_pss_fault"]
    ts1_ybus, ts1_slack_bus, ts1_bus_index = build_test_system_1_admittance_matrix(islanded=True)
    ts1_artifact_summary = summarize_test_system_1_artifact()
    ts1_artifact = load_test_system_1_artifact()
    ts1_target = PAPER_VALIDATION_TARGETS["test_system_1"]

    baseline_result = solver.solve(
        admittance_matrix=admittance_matrix,
        slack_bus=slack_bus,
        fault_bus=baseline_definition["fault_bus"],
        fault_impedance=baseline_definition["fault_impedance"],
        converters=[],
    )
    vsc_result = solver.solve(
        admittance_matrix=admittance_matrix,
        slack_bus=slack_bus,
        fault_bus=vsc_definition["fault_bus"],
        fault_impedance=vsc_definition["fault_impedance"],
        converters=[VSCConverter(**converter_definition) for converter_definition in vsc_definition["converters"]],
    )
    test_system_1_reconstruction = {
        "artifact_summary": ts1_artifact_summary,
        "bus_index": ts1_bus_index,
        "fault_target_tables": {
            "moderate": ts1_target["moderate_fault_table"],
            "severe": ts1_target["severe_fault_table"],
        },
        "direct_solver_ready": {
            "admittance_shape": list(ts1_ybus.shape),
            "slack_bus": ts1_slack_bus,
            "fault_bus_index": ts1_bus_index[ts1_artifact["test_system_1"]["fault_bus"]],
            "converter_buses": {
                converter["id"]: ts1_bus_index[converter["bus"]]
                for converter in ts1_artifact["test_system_1"]["converters"]
            },
        },
        "reconstruction_status": "network skeleton recovered with switch-aware islanded pruning and bus-id-based solver mapping",
    }

    report = {
        "package_validation_scope": "standalone paper-oriented scenario replay",
        "paper_targets": PAPER_VALIDATION_TARGETS,
        "missing_reproduction_parameters": MISSING_REPRODUCTION_PARAMETERS,
        "baseline_case": {
            "converged": baseline_result.converged,
            "outer_iterations": baseline_result.outer_iterations,
            "inner_iterations": baseline_result.inner_iterations,
            "iterations": baseline_result.iterations,
            "fault_current_pu": [baseline_result.fault_current.real, baseline_result.fault_current.imag],
            "fault_current_magnitude_pu": abs(baseline_result.fault_current),
            "max_residual": baseline_result.max_residual,
        },
        "vsc_case": {
            "converged": vsc_result.converged,
            "outer_iterations": vsc_result.outer_iterations,
            "inner_iterations": vsc_result.inner_iterations,
            "converter_states": vsc_result.converter_states,
            "mode_history": vsc_result.mode_history,
            "fault_current_pu": [vsc_result.fault_current.real, vsc_result.fault_current.imag],
            "fault_current_magnitude_pu": abs(vsc_result.fault_current),
            "max_residual": vsc_result.max_residual,
        },
        "test_system_1_reconstruction": test_system_1_reconstruction,
        "test_system_2_probe": evaluate_test_system_2_probe(verbose=False),
        "limitations": [
            "Paper-native regression tables are now embedded in the package, but the benchmark network definitions remain incomplete for blind end-to-end reproduction.",
            "This runner verifies a paper-faithful solver structure with an outer mode loop and an inner Newton-Raphson solve, but it still does not claim numerical agreement with the paper benchmarks.",
            "Mode switching rules are derived from recoverable paper structure and local assumptions, not from a complete machine-readable copy of every paper equation and table.",
        ],
    }
    print(json.dumps(report, indent=2, sort_keys=True))

    strict_regression = evaluate_test_system_1_regression(verbose=True)
    if not strict_regression["passed"]:
        print(json.dumps({"strict_paper_regression": strict_regression}, indent=2, sort_keys=True))
        sys.exit(1)


if __name__ == "__main__":
    main()
