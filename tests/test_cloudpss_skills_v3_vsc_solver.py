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
