import importlib.util
import argparse
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray


def _load_local_module(module_name: str, file_name: str):
    module_path = Path(__file__).resolve().with_name(file_name)
    module_spec = importlib.util.spec_from_file_location(module_name, module_path)
    if module_spec is None or module_spec.loader is None:
        raise ImportError(f"Unable to load module from {module_path}")
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module


scenarios = _load_local_module("vsc_sc_scenarios_ts2_sensitivity", "scenarios.py")
solver_module = _load_local_module("vsc_sc_solver_ts2_sensitivity", "vsc_nr_solver.py")


IEEE14_LOADS_MVA_ON_100_BASE = {
    1: (21.7, 12.7),
    2: (94.2, 19.0),
    3: (47.8, -3.9),
    4: (7.6, 1.6),
    5: (11.2, 7.5),
    8: (29.5, 16.6),
    9: (9.0, 5.8),
    10: (3.5, 1.8),
    11: (6.1, 1.6),
    12: (13.5, 5.8),
    13: (14.9, 5.0),
}


def add_ieee14_load_impedances(
    ybus: NDArray[np.complex128],
    load_scale: float,
    voltage_pu: float = 1.0,
) -> NDArray[np.complex128]:
    loaded = np.array(ybus, dtype=np.complex128, copy=True)
    for bus, (p_mw, q_mvar) in IEEE14_LOADS_MVA_ON_100_BASE.items():
        load_power_pu = complex(p_mw / 100.0, q_mvar / 100.0) * load_scale
        loaded[bus, bus] += np.conj(load_power_pu) / (voltage_pu**2)
    return loaded


def add_converter_transformer_nodes(
    ybus: NDArray[np.complex128],
    transformer_impedance: complex,
) -> tuple[NDArray[np.complex128], dict[int, int]]:
    base_size = int(ybus.shape[0])
    expanded_size = base_size + len(scenarios.TEST_SYSTEM_2_VSC_BUSES)
    expanded = np.zeros((expanded_size, expanded_size), dtype=np.complex128)
    expanded[:base_size, :base_size] = ybus
    converter_bus_map: dict[int, int] = {}

    branch_admittance = 1.0 / transformer_impedance
    for offset, grid_bus in enumerate(scenarios.TEST_SYSTEM_2_VSC_BUSES):
        converter_bus = base_size + offset
        converter_bus_map[grid_bus] = converter_bus
        expanded[grid_bus, grid_bus] += branch_admittance
        expanded[converter_bus, converter_bus] += branch_admittance
        expanded[grid_bus, converter_bus] -= branch_admittance
        expanded[converter_bus, grid_bus] -= branch_admittance

    return expanded, converter_bus_map


def _converter_definitions(capacity_mva: float, converter_bus_map: dict[int, int] | None = None) -> list[dict[str, Any]]:
    definitions = scenarios.get_test_system_2_converters(capacity_mva)
    if converter_bus_map is None:
        return definitions
    return [
        {**definition, "bus": converter_bus_map[int(definition["bus"])]}
        for definition in definitions
    ]


def evaluate_assumption_set(
    *,
    load_scale: float,
    transformer_x_pu: float,
    fault_x_pu: float,
    voltage_base_kv: float,
) -> dict[str, Any]:
    ybus, slack_bus = scenarios.build_ieee14_full_admittance_matrix()
    if load_scale:
        ybus = add_ieee14_load_impedances(ybus, load_scale)

    converter_bus_map = None
    if transformer_x_pu:
        ybus, converter_bus_map = add_converter_transformer_nodes(ybus, complex(0.0, transformer_x_pu))

    solver = solver_module.PaperFaithfulShortCircuitSolver(tolerance=1e-8, max_iter=200, max_outer_iter=20)
    targets = scenarios.PAPER_VALIDATION_TARGETS["test_system_2"]
    cases = []
    for label, capacity_mva in targets["table_10_parameters"]["penetration_capacity_mva"].items():
        result = solver.solve(
            admittance_matrix=ybus,
            slack_bus=slack_bus,
            fault_bus=scenarios.TEST_SYSTEM_2_FAULT_BUS,
            fault_impedance=complex(0.0, fault_x_pu),
            converters=[
                solver_module.VSCConverter(**converter_definition)
                for converter_definition in _converter_definitions(float(capacity_mva), converter_bus_map)
            ],
            slack_voltage=1.0 + 0.0j,
        )
        fault_current_pu = abs(result.fault_current)
        fault_current_ka = scenarios.per_unit_current_to_ka(
            fault_current_pu,
            scenarios.TEST_SYSTEM_2_SYSTEM_BASE_MVA,
            voltage_base_kv,
        )
        target_ka = float(targets["short_circuit_tables"][label]["this_paper_ka"])
        error_percent = abs(fault_current_ka - target_ka) / max(target_ka, 1e-9) * 100.0
        cases.append(
            {
                "case": label,
                "converged": result.converged,
                "fault_current_pu": fault_current_pu,
                "fault_current_ka": fault_current_ka,
                "paper_fault_current_ka": target_ka,
                "error_percent": error_percent,
                "states": {str(bus + 1): state for bus, state in result.converter_states.items()},
            }
        )

    errors = [case["error_percent"] for case in cases if case["converged"]]
    return {
        "load_scale": load_scale,
        "transformer_x_pu": transformer_x_pu,
        "fault_x_pu": fault_x_pu,
        "voltage_base_kv": voltage_base_kv,
        "all_converged": all(case["converged"] for case in cases),
        "mean_abs_error_percent": float(np.mean(errors)) if errors else float("inf"),
        "max_abs_error_percent": float(np.max(errors)) if errors else float("inf"),
        "cases": cases,
    }


def rank_assumptions(extended: bool = False) -> list[dict[str, Any]]:
    if extended:
        load_scales = (0.0, 0.5, 1.0)
        transformer_x_values = (0.0, 0.005, 0.01, 0.03, 0.05, 0.08, 0.1)
        fault_x_values = (1e-6, 0.0005, 0.001, 0.002, 0.005, 0.01)
        voltage_bases = (100.0, 105.0, 110.0, 115.0, 120.0)
    else:
        load_scales = (0.0, 1.0)
        transformer_x_values = (0.0, 0.03, 0.05, 0.08)
        fault_x_values = (1e-6, 0.002, 0.005)
        voltage_bases = (105.0, 110.0, 115.0)

    ranked = []
    for load_scale in load_scales:
        for transformer_x_pu in transformer_x_values:
            for fault_x_pu in fault_x_values:
                for voltage_base_kv in voltage_bases:
                    result = evaluate_assumption_set(
                        load_scale=load_scale,
                        transformer_x_pu=transformer_x_pu,
                        fault_x_pu=fault_x_pu,
                        voltage_base_kv=voltage_base_kv,
                    )
                    if result["all_converged"]:
                        ranked.append(result)
    return sorted(ranked, key=lambda item: (item["mean_abs_error_percent"], item["max_abs_error_percent"]))


def _case_line(case: dict[str, Any]) -> str:
    return (
        f"{case['case']}: got={case['fault_current_ka']:.4f} kA "
        f"paper={case['paper_fault_current_ka']:.4f} kA "
        f"err={case['error_percent']:.2f}%"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Rank recoverable Test System 2 reproduction assumptions.")
    parser.add_argument("--extended", action="store_true", help="Run a wider grid; slower than the default screening scan.")
    args = parser.parse_args()

    baseline = evaluate_assumption_set(
        load_scale=0.0,
        transformer_x_pu=0.0,
        fault_x_pu=1e-6,
        voltage_base_kv=scenarios.TEST_SYSTEM_2_FAULT_BUS_KV_ASSUMPTION,
    )
    print("Baseline documented TS2 probe")
    print(
        f"  mean={baseline['mean_abs_error_percent']:.2f}% "
        f"max={baseline['max_abs_error_percent']:.2f}%"
    )
    for case in baseline["cases"]:
        print(f"  {_case_line(case)}")

    print("\nTop assumption sets")
    for index, result in enumerate(rank_assumptions(extended=args.extended)[:12], start=1):
        print(
            f"{index:02d}. mean={result['mean_abs_error_percent']:.2f}% "
            f"max={result['max_abs_error_percent']:.2f}% "
            f"load={result['load_scale']} "
            f"x_tr={result['transformer_x_pu']} "
            f"x_fault={result['fault_x_pu']} "
            f"kv={result['voltage_base_kv']}"
        )
        for case in result["cases"]:
            print(f"    {_case_line(case)}")


if __name__ == "__main__":
    main()
