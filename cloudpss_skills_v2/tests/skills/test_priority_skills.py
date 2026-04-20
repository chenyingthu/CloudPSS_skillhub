"""Tests for v2 skills: PowerFlowSkill, EMTSimulationSkill, N1SecuritySkill."""

import json
import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
import tempfile
import os

from cloudpss_skills_v2.core.skill_result import SkillResult, SkillStatus
from cloudpss_skills_v2.skills.power_flow import PowerFlowSkill
from cloudpss_skills_v2.skills.emt_simulation import EMTSimulationSkill
from cloudpss_skills_v2.skills.n1_security import N1SecuritySkill


class TestPowerFlowSkill:
    def test_name_and_description(self):
        skill = PowerFlowSkill()
        assert skill.name == "power_flow"
        assert "潮流" in skill.description

    def test_default_config(self):
        skill = PowerFlowSkill()
        config = skill.get_default_config()
        assert config["skill"] == "power_flow"
        assert "model" in config
        assert "algorithm" in config

    def test_config_schema(self):
        skill = PowerFlowSkill()
        schema = skill.config_schema
        assert schema["required"] == ["skill", "model"]
        assert "engine" in schema["properties"]

    def test_validate_missing_rid(self):
        skill = PowerFlowSkill()
        valid, errors = skill.validate({"auth": {"token": "test"}})
        assert not valid
        assert any("model.rid" in e for e in errors)

    def test_validate_missing_auth(self):
        skill = PowerFlowSkill()
        valid, errors = skill.validate({"model": {"rid": "test"}})
        assert not valid
        assert any("auth" in e for e in errors)

    def test_validate_valid_config(self):
        skill = PowerFlowSkill()
        valid, errors = skill.validate(
            {
                "model": {"rid": "model/test/IEEE39"},
                "auth": {"token": "test_token"},
            }
        )
        assert valid
        assert errors == []

    def test_run_validation_failure(self):
        skill = PowerFlowSkill()
        result = skill.run({})
        assert result.status == SkillStatus.FAILED
        assert result.error is not None

    @patch("cloudpss_skills_v2.skills.power_flow.APIFactory")
    def test_run_success(self, mock_factory_cls):
        mock_api = MagicMock()
        mock_api.adapter.engine_name = "cloudpss"
        mock_api.run_power_flow.return_value = MagicMock(
            is_success=True,
            data={
                "buses": [{"name": "B1", "voltage_pu": 1.02}],
                "branches": [{"name": "L1", "power_loss_mw": 0.5}],
                "bus_count": 1,
                "branch_count": 1,
                "converged": True,
            },
        )
        mock_factory_cls.create_powerflow_api.return_value = mock_api

        with tempfile.TemporaryDirectory() as tmpdir:
            skill = PowerFlowSkill()
            result = skill.run(
                {
                    "model": {"rid": "model/test/IEEE39"},
                    "auth": {"token": "test"},
                    "output": {"path": tmpdir, "format": "json"},
                }
            )

            assert result.status == SkillStatus.SUCCESS
            assert result.data["bus_count"] == 1
            assert result.data["branch_count"] == 1
            assert len(result.artifacts) >= 1

    @patch("cloudpss_skills_v2.skills.power_flow.APIFactory")
    def test_run_simulation_failure(self, mock_factory_cls):
        mock_api = MagicMock()
        mock_api.adapter.engine_name = "cloudpss"
        mock_api.run_power_flow.return_value = MagicMock(
            is_success=False,
            errors=["Power flow failed to converge"],
        )
        mock_factory_cls.create_powerflow_api.return_value = mock_api

        skill = PowerFlowSkill()
        result = skill.run(
            {
                "model": {"rid": "model/test/IEEE39"},
                "auth": {"token": "test"},
            }
        )
        assert result.status == SkillStatus.FAILED

    @patch("cloudpss_skills_v2.skills.power_flow.APIFactory")
    def test_run_empty_result(self, mock_factory_cls):
        mock_api = MagicMock()
        mock_api.adapter.engine_name = "cloudpss"
        mock_api.run_power_flow.return_value = MagicMock(
            is_success=True,
            data={"buses": [], "branches": []},
        )
        mock_factory_cls.create_powerflow_api.return_value = mock_api

        skill = PowerFlowSkill()
        result = skill.run(
            {
                "model": {"rid": "model/test/IEEE39"},
                "auth": {"token": "test"},
            }
        )
        assert result.status == SkillStatus.FAILED


class TestEMTSimulationSkill:
    def test_name_and_description(self):
        skill = EMTSimulationSkill()
        assert skill.name == "emt_simulation"
        assert "EMT" in skill.description

    def test_validate_missing_rid(self):
        skill = EMTSimulationSkill()
        valid, errors = skill.validate({"auth": {"token": "test"}})
        assert not valid

    def test_validate_negative_duration(self):
        skill = EMTSimulationSkill()
        valid, errors = skill.validate(
            {
                "model": {"rid": "test"},
                "auth": {"token": "test"},
                "simulation": {"duration": -1},
            }
        )
        assert not valid

    def test_validate_valid(self):
        skill = EMTSimulationSkill()
        valid, errors = skill.validate(
            {
                "model": {"rid": "model/test/IEEE3"},
                "auth": {"token": "test"},
            }
        )
        assert valid

    @patch("cloudpss_skills_v2.skills.emt_simulation.APIFactory")
    def test_run_success(self, mock_factory_cls):
        mock_api = MagicMock()
        mock_api.adapter.engine_name = "cloudpss_emt"
        mock_api.run_emt.return_value = MagicMock(
            is_success=True,
            data={
                "plots": [
                    {
                        "index": 0,
                        "key": "voltage",
                        "name": "Bus Voltages",
                        "channel_count": 3,
                        "channels": ["V_bus1", "V_bus2", "V_bus3"],
                        "channel_data": {
                            "V_bus1": {"x": [0, 0.1, 0.2], "y": [1.0, 0.95, 1.0]},
                            "V_bus2": {"x": [0, 0.1, 0.2], "y": [1.0, 0.9, 1.0]},
                        },
                    }
                ],
                "model_name": "IEEE3",
                "model_rid": "model/test/IEEE3",
                "job_id": "emt-123",
                "plot_count": 1,
            },
        )
        mock_factory_cls.create_emt_api.return_value = mock_api

        with tempfile.TemporaryDirectory() as tmpdir:
            skill = EMTSimulationSkill()
            result = skill.run(
                {
                    "model": {"rid": "model/test/IEEE3"},
                    "auth": {"token": "test"},
                    "output": {"path": tmpdir, "format": "csv"},
                }
            )

            assert result.status == SkillStatus.SUCCESS
            assert result.metrics["plot_count"] == 1


class TestN1SecuritySkill:
    def test_name_and_description(self):
        skill = N1SecuritySkill()
        assert skill.name == "n1_security"
        assert "N-1" in skill.description

    def test_validate_missing_rid(self):
        skill = N1SecuritySkill()
        valid, errors = skill.validate({})
        assert not valid

    def test_validate_valid(self):
        skill = N1SecuritySkill()
        valid, errors = skill.validate(
            {
                "model": {"rid": "model/test/IEEE39"},
                "auth": {"token": "test"},
            }
        )
        assert valid

    def test_summarize_violations_empty(self):
        skill = N1SecuritySkill()
        assert skill._summarize_violations([]) is None

    def test_summarize_violations_voltage_only(self):
        skill = N1SecuritySkill()
        violations = [{"type": "voltage", "message": "low voltage"}]
        summary = skill._summarize_violations(violations)
        assert summary["severity"] == "low"
        assert summary["voltage_violations"] == 1

    def test_summarize_violations_thermal_only(self):
        skill = N1SecuritySkill()
        violations = [{"type": "thermal", "message": "overload"}]
        summary = skill._summarize_violations(violations)
        assert summary["severity"] == "medium"

    def test_summarize_violations_convergence(self):
        skill = N1SecuritySkill()
        violations = [{"type": "convergence", "message": "did not converge"}]
        summary = skill._summarize_violations(violations)
        assert summary["severity"] == "critical"

    def test_summarize_violations_mixed(self):
        skill = N1SecuritySkill()
        violations = [
            {"type": "voltage", "message": "low"},
            {"type": "thermal", "message": "overload"},
        ]
        summary = skill._summarize_violations(violations)
        assert summary["severity"] == "high"

    def test_run_validation_failure(self):
        skill = N1SecuritySkill()
        result = skill.run({})
        assert result.status == SkillStatus.FAILED
