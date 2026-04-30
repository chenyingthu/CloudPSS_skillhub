import importlib.util
from pathlib import Path
from typing import Any


VSC_SKILL_SCRIPTS = (
    Path(__file__).resolve().parents[1]
    / "cloudpss_skills_v3"
    / "skills"
    / "paper2skill-v0.0.1"
    / "vsc-short-circuit-nr"
    / "scripts"
)


def _load_script_module(module_name: str, file_name: str) -> Any:
    module_path = VSC_SKILL_SCRIPTS / file_name
    module_spec = importlib.util.spec_from_file_location(module_name, module_path)
    if module_spec is None or module_spec.loader is None:
        raise ImportError(f"Unable to load module from {module_path}")
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module


def test_v3_vsc_local_validation_scenario_converges():
    scenarios = _load_script_module("v3_vsc_scenarios_test", "scenarios.py")
    solver_module = _load_script_module("v3_vsc_solver_test", "vsc_nr_solver.py")

    admittance_matrix, slack_bus = scenarios.build_ieee14_admittance_matrix()
    scenario = scenarios.LOCAL_VALIDATION_SCENARIOS["single_vsc_pss_fault"]
    solver = solver_module.PaperFaithfulShortCircuitSolver()

    result = solver.solve(
        admittance_matrix=admittance_matrix,
        slack_bus=slack_bus,
        fault_bus=scenario["fault_bus"],
        fault_impedance=scenario["fault_impedance"],
        converters=[
            solver_module.VSCConverter(**converter_definition)
            for converter_definition in scenario["converters"]
        ],
    )

    assert result.converged
    assert result.max_residual < 1e-8
    assert result.fault_current != 0
    assert result.mode_history


def test_v3_vsc_test_system_1_strict_regression_stays_red_until_network_is_recovered():
    validation = _load_script_module("v3_vsc_validation_test", "run_validation.py")

    report = validation.evaluate_test_system_1_regression(verbose=False)

    assert report["passed"] is False
    assert "paper-exact Test System 1 network/base data" in report["blocking_reason"]
    assert {case["case"] for case in report["cases"]} == {"moderate_fault", "severe_fault"}
    assert any(not case["passed"] for case in report["cases"])


def test_v3_vsc_load_impedance_option_uses_paper_equation_5():
    reconstruction = _load_script_module("v3_vsc_reconstruction_test", "test_system_1_reconstruction.py")

    base_ybus, _, bus_index = reconstruction.build_test_system_1_admittance_matrix()
    loaded_ybus, _, _ = reconstruction.build_test_system_1_admittance_matrix(
        include_load_impedances=True,
        load_base_mva=25.0,
        pre_fault_voltage_pu_by_bus={"bus1": 0.95},
    )
    artifact = reconstruction.load_test_system_1_artifact()
    expected_bus1_delta = sum(
        complex(load["p_mw"] / 25.0, -load["q_mvar"] / 25.0) / (0.95**2)
        for load in artifact["model"]["loads"]
        if load["bus"] == "bus1"
    )

    actual_bus1_delta = loaded_ybus[bus_index["bus1"], bus_index["bus1"]] - base_ybus[bus_index["bus1"], bus_index["bus1"]]

    assert abs(actual_bus1_delta - expected_bus1_delta) < 1e-12


def test_v3_vsc_grid_support_reactive_reference_matches_equation_2():
    solver_module = _load_script_module("v3_vsc_solver_equation_test", "vsc_nr_solver.py")
    solver = solver_module.PaperFaithfulShortCircuitSolver()
    converter = solver_module.VSCConverter(
        bus=0,
        p_ref=-0.8,
        q_ref=-0.023,
        i_max=1.0,
        control_mode="GS",
        k_isp=2.0,
        u_ref_gs=1.0,
    )

    assert abs(solver._reactive_power_reference(converter, 0.722 + 0.0j) - 0.384826) < 1e-6


def test_v3_vsc_test_system_2_probe_uses_figure_4_ieee14_assumptions():
    scenarios = _load_script_module("v3_vsc_scenarios_ts2_test", "scenarios.py")
    validation = _load_script_module("v3_vsc_validation_ts2_test", "run_validation.py")

    assert [bus + 1 for bus in scenarios.TEST_SYSTEM_2_VSC_BUSES] == [2, 3, 6, 8, 10, 12, 13, 14]
    assert scenarios.TEST_SYSTEM_2_FAULT_BUS + 1 == 11
    assert scenarios.PAPER_VALIDATION_TARGETS["test_system_2"]["explicit_fault"] == {
        "location": "bus 11",
        "type": "bolted three-phase-to-ground",
        "u_ft": 0.0,
    }

    report = validation.evaluate_test_system_2_probe(verbose=False)

    assert report["passed"] is True
    assert len(report["cases"]) == 3
    assert all(case["converged"] for case in report["cases"])
    assert all(1.5 < case["fault_current_ka"] < 2.1 for case in report["cases"])
    assert report["acceptance"]["max_error_percent"] == 5.0
    assert report["acceptance"]["max_observed_error_percent"] < 5.0
    assert report["blocking_reason"] is None
    assert "PowerFactory transformer data" in report["strict_reproduction_gap"]
