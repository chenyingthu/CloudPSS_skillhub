"""Tests for cloudpss_skills_v2.poweranalysis.renewable_integration."""

from __future__ import annotations

import pytest

from cloudpss_skills_v2.core.skill_result import SkillStatus
from cloudpss_skills_v2.poweranalysis.renewable_integration import (
    RenewableIntegrationAnalysis,
    classify_grid_strength,
    compute_scr,
)
from cloudpss_skills_v2.powerapi.base import SimulationResult, SimulationStatus


class FakeAdapter:
    engine_name: str = "fake"


class FakeHandle:
    pass


class FakePowerFlow:
    adapter: FakeAdapter = FakeAdapter()

    def __init__(self) -> None:
        self.model_rid: str = ""

    def get_model_handle(self, model_rid: str) -> FakeHandle:
        self.model_rid = model_rid
        return FakeHandle()

    def run_power_flow(self, model_handle: FakeHandle) -> SimulationResult:
        return SimulationResult(status=SimulationStatus.COMPLETED, data={"buses": []})


def test_classify_grid_strength_boundaries():
    assert classify_grid_strength(3.0) == "strong"
    assert classify_grid_strength(2.0) == "moderate"
    assert classify_grid_strength(1.99) == "weak"


def test_compute_scr_uses_renewable_capacity_denominator():
    assert compute_scr(400.0, 100.0) == 4.0
    assert compute_scr(400.0, 0.0) == 0.0


def test_validate_requires_model_capacity_and_short_circuit_capacity():
    skill = RenewableIntegrationAnalysis()

    valid, errors = skill.validate({"model": {"rid": "case14"}, "renewable": {}})

    assert valid is False
    assert any("capacity_mw" in error for error in errors)
    assert any("short_circuit_mva" in error for error in errors)


def test_validate_requires_explicit_measurement_series():
    skill = RenewableIntegrationAnalysis()
    config = skill.get_default_config()
    config["renewable"].pop("capacity_series_mw", None)

    valid, errors = skill.validate(config)

    assert valid is False
    assert any("capacity_series_mw" in error for error in errors)


def test_scr_analysis_classifies_and_checks_threshold():
    skill = RenewableIntegrationAnalysis()

    result = skill._analyze_scr({"capacity_mw": 100, "short_circuit_mva": 250}, {"min_scr": 3.0})

    assert result["scr"] == 2.5
    assert result["grid_strength"] == "moderate"
    assert result["passed"] is False


def test_harmonic_analysis_computes_thd():
    skill = RenewableIntegrationAnalysis()

    result = skill._analyze_harmonics(
        {"fundamental_voltage": 1.0, "orders": {"5": 0.03, "7": 0.04}, "limit_thd": 0.06}
    )

    assert result["thd"] == 0.05
    assert result["passed"] is True


def test_lvrt_analysis_detects_low_voltage_violation():
    skill = RenewableIntegrationAnalysis()

    result = skill._analyze_lvrt(
        {
            "profile": [
                {"time_s": 0.0, "voltage_pu": 1.0},
                {"time_s": 0.1, "voltage_pu": 0.1},
                {"time_s": 2.0, "voltage_pu": 0.92},
            ],
            "min_voltage_pu": 0.15,
            "max_recovery_time_s": 1.5,
        }
    )

    assert result["passed"] is False
    assert result["minimum_voltage_observed"] == 0.1


def test_capacity_factor_uses_series_average():
    skill = RenewableIntegrationAnalysis()

    result = skill._analyze_capacity(
        {"capacity_mw": 100, "capacity_series_mw": [20, 30, 40, 50]},
        {"target_capacity_factor": 0.3},
    )

    assert result["average_output_mw"] == 35.0
    assert result["capacity_factor"] == 0.35
    assert result["passed"] is True


def test_calculate_scr_at_buses_uses_per_bus_short_circuit_capacity():
    skill = RenewableIntegrationAnalysis()

    results = skill._calculate_scr_at_buses(
        [{"name": "B1", "sc_mva": 500}, {"name": "B2", "sc_mva": 150}], 100
    )

    assert results[0]["scr"] == 5.0
    assert results[0]["strength"] == "strong"
    assert results[1]["strength"] == "weak"


def test_run_returns_standardized_success_payload(monkeypatch: pytest.MonkeyPatch):
    skill = RenewableIntegrationAnalysis()
    monkeypatch.setattr(
        "cloudpss_skills_v2.poweranalysis.renewable_integration.Engine.create_powerflow",
        lambda engine: FakePowerFlow(),
    )

    result = skill.run(skill.get_default_config())

    assert result.status == SkillStatus.SUCCESS
    assert result.data["skill_name"] == "renewable_integration"
    assert result.data["success"] is True
    assert result.data["results"]["scr"]["scr"] == 3.5
    assert result.data["model_info"]["power_flow_converged"] is True
    assert result.data["data_source"]["lvrt"] == "lvrt.profile"
    assert "capacity-factor" in result.data["standard_basis"]
    assert result.data["assumptions"]
    assert result.data["limitations"]


def test_run_fails_when_thd_exceeds_limit(monkeypatch: pytest.MonkeyPatch):
    skill = RenewableIntegrationAnalysis()
    config = skill.get_default_config()
    config["harmonics"]["orders"] = {"5": 0.08}
    monkeypatch.setattr(
        "cloudpss_skills_v2.poweranalysis.renewable_integration.Engine.create_powerflow",
        lambda engine: FakePowerFlow(),
    )

    result = skill.run(config)

    assert result.status == SkillStatus.FAILED
    assert result.data["summary"]["failed_checks"] == ["harmonics"]
    assert result.error
