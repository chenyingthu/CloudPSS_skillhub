import json
import importlib.util
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

    def build_ieee14_admittance_matrix(self) -> tuple[NDArray[Any], int]: ...


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


def run_test_system_1_regression():
    print("=" * 60)
    print("Test System 1 Regression Against Paper Tables")
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

    print(f"\nAdmittance matrix: {ybus.shape}, slack_bus={slack_bus} (bus1, islanded mode)")
    print(f"Converters: {len(converters)}")
    for i, c in enumerate(converters):
        print(f"  VSC{i+1}: bus={c.bus}, p_ref={c.p_ref}, q_ref={c.q_ref}, i_max={c.i_max}")

    targets = PAPER_VALIDATION_TARGETS["test_system_1"]
    solver = PaperFaithfulShortCircuitSolver(tolerance=1e-8, max_iter=100, max_outer_iter=20)

    all_pass = True

    for scenario in targets["moderate_fault_table"]["iterations"]:
        fault_str = targets["moderate_fault_table"]["fault_impedance_pu"]
        fault_impedance = complex(0, float(fault_str[1:])) if fault_str.startswith("j") else complex(fault_str)

        print(f"\n--- Moderate fault (z_ft={fault_str}) ---")
        print(f"Paper iteration {scenario['iteration']}: states={scenario['vsc_states']}")

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
            print(f"  [FAIL] Solver error: {exc}")
            all_pass = False
            continue

        print(f"  Converged: {result.converged}, outer={result.outer_iterations}, inner={result.inner_iterations}")
        print(f"  Mode history: {result.mode_history}")

        if not result.converged:
            print("  [FAIL] Solver did not converge")
            all_pass = False
            continue

        for bus_id, mode in result.converter_states.items():
            print(f"  Bus {bus_id}: {mode}")

        if scenario["iteration"] == 2 and scenario["feasible"]:
            i_vsc1 = abs(result.current_injections.get(converter_bus_by_id["VSC1"], 0.0))
            i_vsc2 = abs(result.current_injections.get(converter_bus_by_id["VSC2"], 0.0))
            i_vsc3 = abs(result.current_injections.get(converter_bus_by_id["VSC3"], 0.0))
            u1 = result.voltages[converter_bus_by_id["VSC1"]]
            u12 = result.voltages[fault_bus]

            print(f"\n  Comparing to paper Table 2 iteration 2 (feasible):")
            ok = _compare_current(2.204, i_vsc1, "i_vsc1")
            all_pass = ok and all_pass
            ok = _compare_current(1.0, i_vsc2, "i_vsc2")
            all_pass = ok and all_pass
            ok = _compare_current(1.0, i_vsc3, "i_vsc3")
            all_pass = ok and all_pass

            print(f"  u1: paper=1∠0°, got={abs(u1):.4f}∠{np.angle(u1, deg=True):.1f}°")
            print(f"  u12: paper=0.700∠-0.1°, got={abs(u12):.4f}∠{np.angle(u12, deg=True):.1f}°")

    for scenario in targets["severe_fault_table"]["iterations"]:
        fault_str = targets["severe_fault_table"]["fault_impedance_pu"]
        fault_impedance = complex(0, float(fault_str[1:])) if fault_str.startswith("j") else complex(fault_str)

        print(f"\n--- Severe fault (z_ft={fault_str}) ---")
        print(f"Paper iteration {scenario['iteration']}: states={scenario['vsc_states']}")

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
            print(f"  [FAIL] Solver error: {exc}")
            all_pass = False
            continue

        print(f"  Converged: {result.converged}, outer={result.outer_iterations}, inner={result.inner_iterations}")
        print(f"  Mode history: {result.mode_history}")

        if not result.converged:
            print("  [FAIL] Solver did not converge")
            all_pass = False
            continue

        for bus_id, mode in result.converter_states.items():
            print(f"  Bus {bus_id}: {mode}")

        if scenario["iteration"] == 2 and scenario["feasible"]:
            i_vsc1 = abs(result.current_injections.get(converter_bus_by_id["VSC1"], 0.0))
            u1 = result.voltages[converter_bus_by_id["VSC1"]]
            i_vsc2 = abs(result.current_injections.get(converter_bus_by_id["VSC2"], 0.0))
            u6 = result.voltages[converter_bus_by_id["VSC2"]]
            i_vsc3 = abs(result.current_injections.get(converter_bus_by_id["VSC3"], 0.0))
            u12 = result.voltages[fault_bus]

            print(f"\n  Comparing to paper severe fault Table iteration 2 (feasible):")
            ok = _compare_current(2.5, i_vsc1, "i_vsc1 (FSS limit)")
            all_pass = ok and all_pass
            ok = _compare_current(1.0, i_vsc2, "i_vsc2 (FSS limit)")
            all_pass = ok and all_pass
            ok = _compare_current(1.0, i_vsc3, "i_vsc3 (FSS limit)")
            all_pass = ok and all_pass

            print(f"  u1: paper=0.556∠0°, got={abs(u1):.4f}∠{np.angle(u1, deg=True):.1f}°")
            print(f"  u6: paper=0.454∠-2.7°, got={abs(u6):.4f}∠{np.angle(u6, deg=True):.1f}°")
            print(f"  u12: paper=0.222∠10.4°, got={abs(u12):.4f}∠{np.angle(u12, deg=True):.1f}°")

    print(f"\n{'=' * 60}")
    print(f"Overall: {'ALL PASS' if all_pass else 'SOME FAILURES'}")
    print(f"{'=' * 60}")
    return all_pass


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
        "limitations": [
            "Paper-native regression tables are now embedded in the package, but the benchmark network definitions remain incomplete for blind end-to-end reproduction.",
            "This runner verifies a paper-faithful solver structure with an outer mode loop and an inner Newton-Raphson solve, but it still does not claim numerical agreement with the paper benchmarks.",
            "Mode switching rules are derived from recoverable paper structure and local assumptions, not from a complete machine-readable copy of every paper equation and table.",
        ],
    }
    print(json.dumps(report, indent=2, sort_keys=True))

    _ = run_test_system_1_regression()


if __name__ == "__main__":
    main()
