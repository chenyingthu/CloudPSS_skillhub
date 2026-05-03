"""Golden config artifact tests.

These tests keep a hard line between reusable skill configs and true engine
benchmark cases. A case must not claim CloudPSS or pandapower engine capability
unless the repository contains a verified engine-runnable artifact.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import pytest

import cloudpss_skills_v2  # noqa: F401 - populate registry
from cloudpss_skills_v2 import SkillRegistry
from cloudpss_skills_v2.core import SkillStatus
from cloudpss_skills_v2.powerapi.base import SimulationResult, SimulationStatus


GOLDEN_CONFIG_DIR = Path(__file__).parent / "golden_configs"


class FakeAdapter:
    engine_name = "fake"


class FakeHandle:
    def get_components(self):
        return []

    def get_components_by_type(self, component_type):
        del component_type
        return []


class FakePowerFlow:
    adapter = FakeAdapter()

    def get_model_handle(self, model_rid):
        del model_rid
        return FakeHandle()

    def run_power_flow(self, model_handle):
        del model_handle
        return SimulationResult(status=SimulationStatus.COMPLETED, data={"bus_results": []})


@pytest.fixture(autouse=True)
def avoid_engine_claims(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(
        "cloudpss_skills_v2.powerskill.Engine.create_powerflow_for_skill",
        lambda **kwargs: FakePowerFlow(),
    )
    monkeypatch.setattr(
        "cloudpss_skills_v2.powerskill.Engine.create_powerflow",
        lambda engine, **kwargs: FakePowerFlow(),
    )


def _load_configs() -> list[dict[str, Any]]:
    configs = []
    for path in sorted(GOLDEN_CONFIG_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        data["_path"] = path
        configs.append(data)
    return configs


def _run_skill(skill_name: str, config: dict[str, Any]):
    skill_class = SkillRegistry.get(skill_name)
    assert skill_class is not None, f"{skill_name} is not registered"
    skill = skill_class()
    valid, errors = skill.validate(config)
    assert valid, f"{skill_name} rejected golden config: {errors}"
    result = skill.run(config)
    assert result.status == SkillStatus.SUCCESS, result.error
    return result


def _assert_trusted_output_metadata(data: dict[str, Any], case_id: str) -> None:
    missing = []
    for key in (
        "data_source",
        "confidence_level",
        "assumptions",
        "limitations",
        "standard_basis",
    ):
        if not data.get(key):
            missing.append(key)

    assert missing == [], f"{case_id} missing trusted-output metadata: {missing}"
    assert isinstance(data["assumptions"], list) and data["assumptions"], case_id
    assert isinstance(data["limitations"], list) and data["limitations"], case_id
    assert data["confidence_level"] in {
        "formula_derived_from_explicit_input",
        "measurement_derived",
        "screening_design_from_explicit_inputs",
    }


def test_golden_config_artifacts_exist_for_all_current_cases():
    paths = {path.name for path in GOLDEN_CONFIG_DIR.glob("*.json")}

    assert paths == {
        "power_quality_balanced_harmonic.skill.json",
        "power_quality_borderline_fair.skill.json",
        "protection_iec_standard_inverse.skill.json",
        "protection_iec_very_inverse.skill.json",
        "reactive_compensation_weak_bus.skill.json",
        "renewable_integration_passing.skill.json",
        "thevenin_weak_grid.skill.json",
        "two_bus_pv_model.workflow.json",
    }


def test_golden_configs_declare_capability_without_false_engine_claims():
    for artifact in _load_configs():
        capability = artifact.get("capability")
        assert isinstance(capability, dict), artifact["_path"].name
        assert capability.get("skill_runnable") is True, artifact["_path"].name
        assert capability.get("engine_runnable") is False, artifact["_path"].name
        assert capability.get("engine_claim") == "none", artifact["_path"].name
        assert capability.get("engine_notes"), artifact["_path"].name


def test_skill_golden_configs_run_against_declared_skill_inputs():
    for artifact in _load_configs():
        if "workflow" in artifact:
            continue
        result = _run_skill(artifact["skill"], copy.deepcopy(artifact["config"]))
        expected = artifact["expected"]

        if artifact["case_id"] == "thevenin_weak_grid":
            assert result.data["z_th_pu"]["magnitude"] == pytest.approx(expected["z_th_magnitude"])
            assert result.data["short_circuit_capacity_mva"] == pytest.approx(
                expected["short_circuit_capacity_mva"]
            )
            assert result.data["short_circuit_ratio"] == pytest.approx(
                expected["short_circuit_ratio"]
            )
        elif artifact["case_id"] == "power_quality_balanced_harmonic":
            assert result.data["thd"] == pytest.approx(expected["thd"])
            assert result.data["unbalance"] == pytest.approx(expected["unbalance"])
            assert result.data["quality_classification"] == expected["quality_classification"]
        elif artifact["case_id"] == "power_quality_borderline_fair":
            assert result.data["thd"] == pytest.approx(expected["thd"])
            assert result.data["unbalance"] == pytest.approx(expected["unbalance"])
            assert result.data["quality_classification"] == expected["quality_classification"]
        elif artifact["case_id"] == "protection_iec_standard_inverse":
            setting = result.data["settings"][0]
            assert setting["pickup_current"] == pytest.approx(expected["pickup_current"])
            assert setting["time_delay"] == pytest.approx(expected["operating_time_s"], abs=1e-4)
        elif artifact["case_id"] == "protection_iec_very_inverse":
            setting = result.data["settings"][0]
            assert setting["pickup_current"] == pytest.approx(expected["pickup_current"])
            assert setting["time_delay"] == pytest.approx(expected["operating_time_s"], abs=1e-4)
        elif artifact["case_id"] == "reactive_compensation_weak_bus":
            recommendation = result.data["compensation_recommendations"][0]
            assert recommendation["required_q_mvar"] == pytest.approx(expected["required_q_mvar"])
            assert recommendation["recommended_size_mvar"] == pytest.approx(
                expected["recommended_size_mvar"]
            )
        elif artifact["case_id"] == "renewable_integration_passing":
            assert result.data["results"]["scr"]["scr"] == pytest.approx(expected["scr"])
            assert result.data["results"]["harmonics"]["thd"] == pytest.approx(expected["thd"])
            assert result.data["results"]["capacity"]["capacity_factor"] == pytest.approx(
                expected["capacity_factor"]
            )
            assert result.data["summary"]["overall_passed"] is expected["overall_passed"]
        else:
            raise AssertionError(f"unexpected golden config: {artifact['case_id']}")


def test_formula_golden_configs_expose_trusted_output_metadata():
    for artifact in _load_configs():
        if "workflow" in artifact:
            continue

        result = _run_skill(artifact["skill"], copy.deepcopy(artifact["config"]))
        _assert_trusted_output_metadata(result.data, artifact["case_id"])


def test_two_bus_workflow_config_runs_builder_then_validator():
    artifact = json.loads(
        (GOLDEN_CONFIG_DIR / "two_bus_pv_model.workflow.json").read_text(encoding="utf-8")
    )
    builder_step, validator_step = artifact["workflow"]

    built = _run_skill(builder_step["skill"], copy.deepcopy(builder_step["config"]))
    validator_config = copy.deepcopy(validator_step["config"])
    validator_config["model"] = built.data["model"]
    validated = _run_skill(validator_step["skill"], validator_config)

    assert validated.data["status"] == artifact["expected"]["validation_status"]
    assert validated.data["component_count"] == artifact["expected"]["component_count"]
