"""Tests for cloudpss_skills_v2.poweranalysis.protection_coordination."""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from cloudpss_skills_v2.poweranalysis.protection_coordination import (
    ProtectionCoordinationAnalysis,
    ProtectionType,
)
from cloudpss_skills_v2.powerapi.base import SimulationResult, SimulationStatus
from cloudpss_skills_v2.core.skill_result import SkillStatus


@dataclass
class FakeComponent:
    key: str
    name: str
    component_type: str = "branch"


class FakeHandle:
    def get_components(self):
        return [FakeComponent("line1", "Line 1"), FakeComponent("line2", "Line 2")]


class FakeAdapter:
    engine_name: str = "fake"


class FakePowerFlow:
    adapter: FakeAdapter = FakeAdapter()

    def __init__(self) -> None:
        self.model_rid: str = ""

    def get_model_handle(self, model_rid: str) -> FakeHandle:
        self.model_rid = model_rid
        return FakeHandle()

    def run_power_flow(self, model_handle: FakeHandle) -> SimulationResult:
        return SimulationResult(status=SimulationStatus.COMPLETED, data={"buses": []})


def test_validate_rejects_missing_model_rid():
    skill = ProtectionCoordinationAnalysis()

    valid, errors = skill.validate({"skill": "protection_coordination", "model": {}})

    assert valid is False
    assert "model.rid" in errors[0]


def test_validate_rejects_bad_margin_order():
    skill = ProtectionCoordinationAnalysis()

    valid, errors = skill.validate(
        {
            "skill": "protection_coordination",
            "model": {"rid": "case14"},
            "analysis": {
                "min_coordination_margin_s": 0.5,
                "max_coordination_margin_s": 0.3,
            },
        }
    )

    assert valid is False
    assert any("max_coordination" in error for error in errors)


def test_validate_requires_explicit_relays():
    skill = ProtectionCoordinationAnalysis()

    valid, errors = skill.validate({"skill": "protection_coordination", "model": {"rid": "case14"}})

    assert valid is False
    assert any("relays" in error for error in errors)


def test_relay_settings_use_load_and_fault_current_limits():
    skill = ProtectionCoordinationAnalysis()
    setting = skill._calculate_relay_settings(
        {
            "id": "R1",
            "type": ProtectionType.OVERCURRENT.value,
            "load_current": 200,
            "fault_current": 3000,
            "time_dial": 0.1,
        },
        {"load_multiplier": 1.25, "fault_current_safety_factor": 0.5},
    )

    assert setting.pickup_current == 250.0
    assert setting.time_delay > 0
    assert setting.time_delay < 1


def test_coordination_detects_invalid_margin():
    skill = ProtectionCoordinationAnalysis()
    primary = skill._calculate_relay_settings(
        {"id": "R1", "load_current": 200, "fault_current": 3000, "time_dial": 0.1},
        {},
    )
    backup = skill._calculate_relay_settings(
        {"id": "R2", "load_current": 200, "fault_current": 3000, "time_dial": 0.11},
        {},
    )

    result = skill._check_coordination(
        {"R1": primary, "R2": backup},
        {"coordination_pairs": [{"primary": "R1", "backup": "R2"}]},
        {"min_coordination_margin_s": 0.3},
    )

    assert len(result) == 1
    assert result[0].is_valid is False


def test_tcc_curves_are_monotonic_decreasing_with_current():
    skill = ProtectionCoordinationAnalysis()
    setting = skill._calculate_relay_settings(
        {"id": "R1", "load_current": 200, "fault_current": 3000, "time_dial": 0.1},
        {},
    )

    curves = skill._generate_tcc_curves([setting], {"curve_multiples": [2, 5, 10]})
    times = [point["time_s"] for point in curves[0]["points"]]

    assert times == sorted(times, reverse=True)


def test_zone_validation_checks_relay_and_reach():
    skill = ProtectionCoordinationAnalysis()
    setting = skill._calculate_relay_settings(
        {"id": "R1", "load_current": 200, "fault_current": 3000},
        {},
    )

    zones = skill._validate_zones(
        [
            {"relay": "R1", "zone": 1, "reach_percent": 80, "expected_reach_percent": 80},
            {"relay": "missing", "zone": 2, "reach_percent": 120},
        ],
        {"R1": setting},
    )

    assert zones[0]["is_valid"] is True
    assert zones[1]["is_valid"] is False


def test_run_returns_standardized_success_payload(monkeypatch: pytest.MonkeyPatch):
    skill = ProtectionCoordinationAnalysis()
    monkeypatch.setattr(
        "cloudpss_skills_v2.poweranalysis.protection_coordination.Engine.create_powerflow",
        lambda engine: FakePowerFlow(),
    )

    result = skill.run(
        {
            "skill": "protection_coordination",
            "engine": "pandapower",
            "model": {"rid": "case14"},
            "relays": [
                {"id": "R1", "load_current": 200, "fault_current": 3000, "time_dial": 0.1},
                {"id": "R2", "load_current": 200, "fault_current": 3000, "time_dial": 0.5},
            ],
            "coordination_pairs": [{"primary": "R1", "backup": "R2"}],
        }
    )

    assert result.status == SkillStatus.SUCCESS
    assert result.data["skill_name"] == "protection_coordination"
    assert result.data["success"] is True
    assert result.data["relay_count"] == 2
    assert result.data["coordination_results"][0]["is_valid"] is True
    assert result.data["data_source"] == "explicit_relay_settings"
    assert "IEC 60255" in result.data["standard_basis"]
    assert result.data["assumptions"]
    assert result.data["limitations"]


def test_run_fails_when_coordination_margin_is_invalid(monkeypatch: pytest.MonkeyPatch):
    skill = ProtectionCoordinationAnalysis()
    monkeypatch.setattr(
        "cloudpss_skills_v2.poweranalysis.protection_coordination.Engine.create_powerflow",
        lambda engine: FakePowerFlow(),
    )

    result = skill.run(
        {
            "skill": "protection_coordination",
            "engine": "pandapower",
            "model": {"rid": "case14"},
            "relays": [
                {"id": "R1", "load_current": 200, "fault_current": 3000, "time_dial": 0.1},
                {"id": "R2", "load_current": 200, "fault_current": 3000, "time_dial": 0.12},
            ],
            "coordination_pairs": [{"primary": "R1", "backup": "R2"}],
        }
    )

    assert result.status == SkillStatus.FAILED
    assert result.data["success"] is False
    assert result.error
