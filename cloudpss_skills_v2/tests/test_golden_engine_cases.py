"""Engine-runnable golden benchmark cases.

These tests are intentionally separate from skill-level golden configs. Cases
in this lane must provide a repository model artifact and must be executed by
the declared engine adapter before comparing expected outputs.
"""

from __future__ import annotations

import json
from pathlib import Path
import socket
from typing import Any
from urllib.parse import urlparse

import pytest

from cloudpss_skills_v2.powerapi import EngineConfig
from cloudpss_skills_v2.powerapi import SimulationStatus
from cloudpss_skills_v2.core.skill_result import SkillStatus
from cloudpss_skills_v2.powerapi.adapters.pandapower import (
    PandapowerPowerFlowAdapter,
    PandapowerShortCircuitAdapter,
)
from cloudpss_skills_v2.poweranalysis.contingency_analysis import ContingencyAnalysis
from cloudpss_skills_v2.poweranalysis.n1_security import N1SecurityAnalysis
from cloudpss_skills_v2.poweranalysis.voltage_stability import VoltageStabilityAnalysis
from cloudpss_skills_v2.powerskill.presets.power_flow import PowerFlowPreset
from cloudpss_skills_v2.powerskill import Engine


GOLDEN_ENGINE_CASE_DIR = Path(__file__).parent / "golden_engine_cases"
LOCAL_CLOUDPSS_BASE_URL = "http://166.111.60.76:50001"


def _load_case(case_name: str) -> dict[str, Any]:
    return json.loads((GOLDEN_ENGINE_CASE_DIR / f"{case_name}.json").read_text(encoding="utf-8"))


def _run_power_flow(case: dict[str, Any]):
    adapter = PandapowerPowerFlowAdapter()
    adapter.connect()
    try:
        config = dict(case["power_flow_config"])
        config["model_file"] = str(GOLDEN_ENGINE_CASE_DIR / f"{case['case_id']}.json")
        return adapter.run_simulation(config)
    finally:
        adapter.disconnect()


def _run_short_circuit(case: dict[str, Any]):
    adapter = PandapowerShortCircuitAdapter()
    adapter.connect()
    try:
        config = dict(case["short_circuit_config"])
        config["model_file"] = str(GOLDEN_ENGINE_CASE_DIR / f"{case['case_id']}.json")
        return adapter.run_simulation(config)
    finally:
        adapter.disconnect()


def _cloudpss_skip_reason(case: dict[str, Any]) -> str | None:
    server = case["server"]
    base_url = server["base_url"]
    if base_url != LOCAL_CLOUDPSS_BASE_URL:
        return f"unexpected CloudPSS golden server: {base_url}"

    token_path = Path(server["token_file"])
    if not token_path.exists() or not token_path.read_text().strip():
        return f"CloudPSS token file is unavailable: {token_path}"

    parsed = urlparse(base_url)
    if not parsed.hostname or not parsed.port:
        return f"invalid CloudPSS base URL: {base_url}"

    try:
        with socket.create_connection((parsed.hostname, parsed.port), timeout=3):
            return None
    except OSError as exc:
        return f"CloudPSS local server is unreachable: {exc}"


def _run_cloudpss_power_flow(case: dict[str, Any]):
    reason = _cloudpss_skip_reason(case)
    if reason:
        pytest.skip(reason)

    server = case["server"]
    token = Path(server["token_file"]).read_text().strip()
    auth = {"token": token, "base_url": server["base_url"]}
    config = EngineConfig(
        engine_name="cloudpss",
        base_url=server["base_url"],
        extra={"auth": auth},
    )
    pf = Engine.create_powerflow(engine="cloudpss", config=config)
    return pf.run_power_flow(**case["power_flow_config"], auth=auth)


def _assert_cloudpss_ieee39_expected(data: dict[str, Any], case: dict[str, Any]) -> None:
    expected = case["expected"]
    tolerances = case["tolerances"]

    assert data["model_rid"] == expected["model_rid"]
    assert data["converged"] is expected["converged"]
    assert data["bus_count"] == expected["bus_count"]
    assert data["branch_count"] == expected["branch_count"]

    summary = data["summary"]
    expected_summary = expected["summary"]
    assert summary["total_generation"]["p_mw"] == pytest.approx(
        expected_summary["total_generation_p_mw"], abs=tolerances["power_mw"]
    )
    assert summary["total_generation"]["q_mvar"] == pytest.approx(
        expected_summary["total_generation_q_mvar"], abs=tolerances["power_mvar"]
    )
    assert summary["total_load"]["p_mw"] == pytest.approx(
        expected_summary["total_load_p_mw"], abs=tolerances["power_mw"]
    )
    assert summary["total_load"]["q_mvar"] == pytest.approx(
        expected_summary["total_load_q_mvar"], abs=tolerances["power_mvar"]
    )
    assert summary["total_loss_mw"] == pytest.approx(
        expected_summary["total_loss_mw"], abs=tolerances["loss_mw"]
    )
    assert summary["voltage_range"]["min_pu"] == pytest.approx(
        expected_summary["min_voltage_pu"], abs=tolerances["voltage_pu"]
    )
    assert summary["voltage_range"]["max_pu"] == pytest.approx(
        expected_summary["max_voltage_pu"], abs=tolerances["voltage_pu"]
    )

    buses = {bus["name"]: bus for bus in data["buses"]}
    for sentinel in expected["sentinel_buses"]:
        bus = buses[sentinel["name"]]
        assert bus["voltage_pu"] == pytest.approx(
            sentinel["voltage_pu"], abs=tolerances["voltage_pu"]
        )
        assert bus["generation_mw"] == pytest.approx(
            sentinel["generation_mw"], abs=tolerances["power_mw"]
        )
        assert bus["load_mw"] == pytest.approx(sentinel["load_mw"], abs=tolerances["power_mw"])

    branches = {branch["name"]: branch for branch in data["branches"]}
    for sentinel in expected["sentinel_branches"]:
        branch = branches[sentinel["name"]]
        assert branch["branch_type"] == sentinel["branch_type"]
        assert branch["power_loss_mw"] == pytest.approx(
            sentinel["power_loss_mw"], abs=tolerances["loss_mw"]
        )


def test_engine_golden_case_artifacts_declare_verified_engine_capability():
    paths = sorted(GOLDEN_ENGINE_CASE_DIR.glob("*.json"))
    assert [path.name for path in paths] == [
        "cloudpss_ieee39_powerflow.json",
        "pandapower_parallel_lines_n1.json",
        "pandapower_two_bus_radial.json",
    ]

    for path in paths:
        case = json.loads(path.read_text(encoding="utf-8"))
        capability = case["capability"]
        assert capability["engine_runnable"] is True
        assert capability["engine"] in {"cloudpss", "pandapower"}
        if capability["engine"] == "pandapower":
            assert capability["engine_claim"] in {
                "pandapower_powerflow_and_short_circuit",
                "pandapower_powerflow_short_circuit_and_contingency",
                "pandapower_powerflow_short_circuit_n1_and_contingency",
                "pandapower_powerflow_short_circuit_and_voltage_stability",
            }
            assert case["model"]["format"] == "pandapower_network_spec_v1"
            assert case["expected"]["power_flow"]["converged"] is True
            assert case["expected"]["short_circuit"]["standard"] == "IEC 60909"
            if capability["skill_runnable"]:
                configs = case.get("skill_configs") or {
                    case["skill_config"]["skill"]: case["skill_config"]
                }
                assert configs
                for config in configs.values():
                    assert config["engine"] == "pandapower"
                    assert config["model"]["source"] == "local"
        else:
            assert capability["engine_claim"] == "cloudpss_live_powerflow"
            assert case["server"]["base_url"] == LOCAL_CLOUDPSS_BASE_URL
            assert case["model"]["rid"].startswith("model/chenying/")
            assert case["expected"]["converged"] is True
            assert case["skill_config"]["skill"] == "power_flow"
            assert case["skill_config"]["engine"] == "cloudpss"


@pytest.mark.integration
@pytest.mark.pandapower
def test_pandapower_two_bus_radial_power_flow_engine_golden_case():
    case = _load_case("pandapower_two_bus_radial")
    expected = case["expected"]["power_flow"]
    tolerances = case["tolerances"]

    result = _run_power_flow(case)

    assert result.status == SimulationStatus.COMPLETED, result.errors
    assert result.data["converged"] is True
    assert result.data["bus_count"] == expected["bus_count"]
    assert result.data["branch_count"] == expected["branch_count"]

    buses = {bus["name"]: bus for bus in result.data["buses"]}
    line = result.data["branches"][0]
    summary = result.data["summary"]

    assert buses["Source"]["voltage_pu"] == pytest.approx(
        expected["source_bus_voltage_pu"], abs=tolerances["voltage_pu"]
    )
    assert buses["Load"]["voltage_pu"] == pytest.approx(
        expected["load_bus_voltage_pu"], abs=tolerances["voltage_pu"]
    )
    assert buses["Load"]["angle_deg"] == pytest.approx(
        expected["load_bus_angle_degree"], abs=tolerances["angle_degree"]
    )
    assert line["loading_pct"] == pytest.approx(
        expected["line_loading_percent"], abs=tolerances["percent"]
    )
    assert line["pl_mw"] == pytest.approx(expected["line_loss_mw"], abs=tolerances["power_mw"])
    assert summary["total_generation"]["p_mw"] == pytest.approx(expected["grid_p_mw"], abs=1e-4)
    assert summary["total_generation"]["q_mvar"] == pytest.approx(expected["grid_q_mvar"], abs=1e-4)


@pytest.mark.integration
@pytest.mark.pandapower
def test_pandapower_parallel_lines_n1_power_flow_engine_golden_case():
    case = _load_case("pandapower_parallel_lines_n1")
    expected = case["expected"]["power_flow"]
    tolerances = case["tolerances"]

    result = _run_power_flow(case)

    assert result.status == SimulationStatus.COMPLETED, result.errors
    assert result.data["converged"] is True
    assert result.data["bus_count"] == expected["bus_count"]
    assert result.data["branch_count"] == expected["branch_count"]

    buses = {bus["name"]: bus for bus in result.data["buses"]}
    summary = result.data["summary"]
    for line in result.data["branches"]:
        assert line["loading_pct"] == pytest.approx(
            expected["line_loading_percent"], abs=tolerances["percent"]
        )
        assert line["pl_mw"] == pytest.approx(expected["line_loss_mw"], abs=tolerances["power_mw"])

    assert buses["Source"]["voltage_pu"] == pytest.approx(
        expected["source_bus_voltage_pu"], abs=tolerances["voltage_pu"]
    )
    assert buses["Load"]["voltage_pu"] == pytest.approx(
        expected["load_bus_voltage_pu"], abs=tolerances["voltage_pu"]
    )
    assert buses["Load"]["angle_deg"] == pytest.approx(
        expected["load_bus_angle_degree"], abs=tolerances["angle_degree"]
    )
    assert summary["total_generation"]["p_mw"] == pytest.approx(expected["grid_p_mw"], abs=1e-4)
    assert summary["total_generation"]["q_mvar"] == pytest.approx(expected["grid_q_mvar"], abs=1e-4)


@pytest.mark.integration
@pytest.mark.pandapower
def test_pandapower_two_bus_radial_short_circuit_engine_golden_case():
    case = _load_case("pandapower_two_bus_radial")
    expected = case["expected"]["short_circuit"]
    tolerances = case["tolerances"]

    result = _run_short_circuit(case)

    assert result.status == SimulationStatus.COMPLETED, result.errors
    assert result.data["standard"] == expected["standard"]
    assert result.data["summary"]["fault_type"] == expected["fault_type"]
    assert result.data["summary"]["bus_count"] == expected["bus_count"]
    assert result.data["summary"]["max_ikss_ka"] == pytest.approx(expected["max_ikss_ka"], abs=1e-4)

    buses = {bus["bus"]: bus for bus in result.data["bus_results"]}
    assert buses["Source"]["ikss_ka"] == pytest.approx(
        expected["source_bus_ikss_ka"], abs=tolerances["current_ka"]
    )
    assert buses["Load"]["ikss_ka"] == pytest.approx(
        expected["load_bus_ikss_ka"], abs=tolerances["current_ka"]
    )


@pytest.mark.integration
@pytest.mark.pandapower
def test_pandapower_two_bus_radial_voltage_stability_skill_golden_case(tmp_path: Path):
    case = _load_case("pandapower_two_bus_radial")
    expected = case["expected"]["voltage_stability"]
    tolerances = case["tolerances"]
    config = dict(case["skill_configs"]["voltage_stability"])
    config["model"] = {
        **config["model"],
        "file": str(GOLDEN_ENGINE_CASE_DIR / "pandapower_two_bus_radial.json"),
    }
    config["output"] = {**config["output"], "path": str(tmp_path)}

    result = VoltageStabilityAnalysis().run(config)

    assert result.status == SkillStatus.SUCCESS
    assert result.error is None
    assert result.data["total_cases"] == expected["total_cases"]
    assert result.data["converged_cases"] == expected["converged_cases"]
    assert result.data["collapse_threshold"] == expected["collapse_threshold"]
    assert result.data["collapse_point"] == expected["collapse_point"]
    assert result.data["max_loadability"] == expected["max_loadability"]
    assert result.data["monitored_buses"] == expected["monitored_buses"]

    assert len(result.data["results"]) == expected["total_cases"]
    for expected_point, result_point in zip(
        expected["pv_curve"], result.data["pv_curve"], strict=True
    ):
        assert result_point["scale"] == expected_point["scale"]
        assert result_point["bus"] == expected_point["bus"]
        assert result_point["voltage"] == pytest.approx(
            expected_point["voltage"], abs=tolerances["voltage_pu"]
        )

    load_voltages = [point["voltage"] for point in result.data["pv_curve"]]
    assert load_voltages == sorted(load_voltages, reverse=True)
    assert load_voltages[-1] < expected["collapse_threshold"]
    assert len(result.artifacts) == 2
    assert all(Path(artifact.path).exists() for artifact in result.artifacts)


@pytest.mark.integration
@pytest.mark.pandapower
def test_pandapower_parallel_lines_n1_short_circuit_engine_golden_case():
    case = _load_case("pandapower_parallel_lines_n1")
    expected = case["expected"]["short_circuit"]
    tolerances = case["tolerances"]

    result = _run_short_circuit(case)

    assert result.status == SimulationStatus.COMPLETED, result.errors
    assert result.data["standard"] == expected["standard"]
    assert result.data["summary"]["fault_type"] == expected["fault_type"]
    assert result.data["summary"]["bus_count"] == expected["bus_count"]
    assert result.data["summary"]["max_ikss_ka"] == pytest.approx(expected["max_ikss_ka"], abs=1e-4)

    buses = {bus["bus"]: bus for bus in result.data["bus_results"]}
    assert buses["Source"]["ikss_ka"] == pytest.approx(
        expected["source_bus_ikss_ka"], abs=tolerances["current_ka"]
    )
    assert buses["Load"]["ikss_ka"] == pytest.approx(
        expected["load_bus_ikss_ka"], abs=tolerances["current_ka"]
    )


@pytest.mark.integration
@pytest.mark.pandapower
def test_pandapower_parallel_lines_n1_contingency_skill_golden_case(tmp_path: Path):
    case = _load_case("pandapower_parallel_lines_n1")
    expected = case["expected"]["contingency"]
    tolerances = case["tolerances"]
    config = dict(case["skill_configs"]["contingency_analysis"])
    config["model"] = {
        **config["model"],
        "file": str(GOLDEN_ENGINE_CASE_DIR / "pandapower_parallel_lines_n1.json"),
    }
    config["output"] = {**config["output"], "path": str(tmp_path)}

    result = ContingencyAnalysis().run(config)

    assert result.status == SkillStatus.FAILED
    assert result.error is None
    summary = result.data["summary"]
    assert summary["total_cases"] == expected["total_cases"]
    assert summary["passed"] == expected["passed"]
    assert summary["failed"] == expected["failed"]
    assert summary["errors"] == expected["errors"]
    assert summary["pass_rate"] == expected["pass_rate"]
    assert summary["severe_cases"] == expected["severe_cases"]
    assert result.data["base_case"] == {"bus_count": 2, "branch_count": 2}

    by_component = {
        tuple(case_result["components"]): case_result for case_result in result.data["all_results"]
    }
    assert set(by_component) == {("line:0",), ("line:1",)}
    for case_result in by_component.values():
        assert case_result["status"] == expected["case_status"]
        assert case_result["min_voltage"] == pytest.approx(
            expected["post_contingency_load_voltage_pu"],
            abs=tolerances["voltage_pu"],
        )
        assert case_result["max_voltage"] == pytest.approx(
            expected["post_contingency_source_voltage_pu"],
            abs=tolerances["voltage_pu"],
        )
        assert case_result["severity"] == pytest.approx(
            expected["severity"], abs=tolerances["severity"]
        )
        assert [v["type"] for v in case_result["violations"]] == [expected["violation_type"]]
        assert case_result["violations"][0]["details"]["loading"] == pytest.approx(
            expected["remaining_line_loading_percent"], abs=1e-2
        )

    assert [case_result["components"] for case_result in result.data["top_severe_cases"]] == [
        ["line:0"],
        ["line:1"],
    ]
    assert {p["component"] for p in result.data["weak_points"]} == set(expected["weak_points"])
    assert len(result.artifacts) == 2
    assert all(Path(artifact.path).exists() for artifact in result.artifacts)


@pytest.mark.integration
@pytest.mark.pandapower
def test_pandapower_parallel_lines_n1_security_skill_golden_case(tmp_path: Path):
    case = _load_case("pandapower_parallel_lines_n1")
    expected = case["expected"]["n1_security"]
    tolerances = case["tolerances"]
    config = dict(case["skill_configs"]["n1_security"])
    config["model"] = {
        **config["model"],
        "file": str(GOLDEN_ENGINE_CASE_DIR / "pandapower_parallel_lines_n1.json"),
    }
    config["output"] = {**config["output"], "path": str(tmp_path)}

    result = N1SecurityAnalysis().run(config)

    assert result.status == SkillStatus.FAILED
    assert result.error is None
    assert result.metrics == {
        "total_branches": expected["total_scenarios"],
        "passed": expected["passed"],
        "failed": expected["failed"],
    }

    typed = result.data["_typed"]
    summary = typed["summary"]
    assert summary["total_scenarios"] == expected["total_scenarios"]
    assert summary["passed"] == expected["passed"]
    assert summary["failed"] == expected["failed"]
    assert summary["overall_severity"] == expected["overall_severity"]

    by_key = {contingency["branch_key"]: contingency for contingency in typed["contingencies"]}
    assert set(by_key) == {"line:0", "line:1"}
    for contingency in by_key.values():
        assert contingency["converged"] is True
        assert contingency["severity"] == expected["case_severity"]
        assert contingency["min_vm_pu"] == pytest.approx(
            expected["post_contingency_min_voltage_pu"],
            abs=tolerances["voltage_pu"],
        )
        assert contingency["max_loading_pct"] == pytest.approx(
            expected["remaining_line_loading_percent"],
            abs=tolerances["percent"],
        )
        assert len(contingency["violations"]) == 1
        violation = contingency["violations"][0]
        assert violation["violation_type"] == expected["violation_type"]
        assert violation["value"] == pytest.approx(
            expected["remaining_line_loading_ratio"],
            abs=tolerances["percent"],
        )
        assert violation["severity"] == expected["case_severity"]

    assert len(typed["violations"]) == expected["failed"]
    assert len(result.artifacts) == 1
    assert Path(result.artifacts[0].path).exists()


@pytest.mark.integration
@pytest.mark.cloudpss
def test_cloudpss_ieee39_power_flow_live_engine_golden_case():
    case = _load_case("cloudpss_ieee39_powerflow")
    result = _run_cloudpss_power_flow(case)

    assert result.status == SimulationStatus.COMPLETED, result.errors
    _assert_cloudpss_ieee39_expected(result.data, case)


@pytest.mark.integration
@pytest.mark.cloudpss
def test_cloudpss_ieee39_power_flow_skill_live_golden_case(tmp_path: Path):
    case = _load_case("cloudpss_ieee39_powerflow")
    reason = _cloudpss_skip_reason(case)
    if reason:
        pytest.skip(reason)

    config = dict(case["skill_config"])
    config["output"] = {**config["output"], "path": str(tmp_path)}
    valid, errors = PowerFlowPreset().validate(config)
    assert valid, errors

    result = PowerFlowPreset().run(config)

    assert result.status.name == "SUCCESS", result.error
    _assert_cloudpss_ieee39_expected(result.data, case)
    assert result.artifacts
    assert Path(result.artifacts[0].path).exists()
