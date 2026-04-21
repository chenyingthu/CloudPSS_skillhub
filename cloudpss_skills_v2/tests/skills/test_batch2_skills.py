"""Tests for v2 skills: ShortCircuitAnalysis, ContingencyAnalysis, LossAnalysis, VoltageStabilityAnalysis."""

import json
import pytest
from unittest.mock import MagicMock, patch, PropertyMock
from pathlib import Path
import tempfile
import os

from cloudpss_skills_v2.core.skill_result import SkillResult, SkillStatus
from cloudpss_skills_v2.poweranalysis.short_circuit import ShortCircuitAnalysis
from cloudpss_skills_v2.poweranalysis.contingency_analysis import ContingencyAnalysis
from cloudpss_skills_v2.poweranalysis.loss_analysis import (
    LossAnalysis,
    BranchLoss,
    TransformerLoss,
    _as_float as loss_as_float,
)
from cloudpss_skills_v2.poweranalysis.voltage_stability import VoltageStabilityAnalysis


def _make_mock_api(sim_data=None):
    """Create a mock PowerFlow/ShortCircuit that returns given data."""
    mock_api = MagicMock()
    mock_adapter = MagicMock()
    mock_adapter.engine_name = "mock_engine"
    type(mock_api).adapter = PropertyMock(return_value=mock_adapter)

    if sim_data is None:
        sim_data = MagicMock()

    mock_result = MagicMock()
    mock_result.is_success = True
    mock_result.errors = []
    mock_result.data = sim_data
    mock_api.run_power_flow.return_value = mock_result
    mock_api.run_short_circuit.return_value = mock_result

    return mock_api, mock_result


class TestShortCircuitAnalysis:
    def test_name_and_description(self):
        skill = ShortCircuitAnalysis()
        assert skill.name == "short_circuit"
        assert "短路" in skill.description

    def test_default_config(self):
        skill = ShortCircuitAnalysis()
        config = skill.get_default_config()
        assert config["skill"] == "short_circuit"
        assert "fault" in config
        assert config["fault"]["type"] == "three_phase"

    def test_config_schema(self):
        skill = ShortCircuitAnalysis()
        schema = skill.config_schema
        assert schema["required"] == ["skill", "model", "fault"]
        assert "fault" in schema["properties"]
        assert "monitoring" in schema["properties"]
        assert "calculation" in schema["properties"]

    def test_validate_missing_rid(self):
        skill = ShortCircuitAnalysis()
        valid, errors = skill.validate(
            {"fault": {"location": "Bus7"}, "auth": {"token": "t"}}
        )
        assert not valid
        assert any("model.rid" in e for e in errors)

    def test_validate_missing_fault_location(self):
        skill = ShortCircuitAnalysis()
        valid, errors = skill.validate(
            {"model": {"rid": "test"}, "auth": {"token": "t"}}
        )
        assert not valid
        assert any("fault.location" in e for e in errors)

    def test_validate_valid_config(self):
        skill = ShortCircuitAnalysis()
        valid, errors = skill.validate(
            {
                "model": {"rid": "test"},
                "fault": {"location": "Bus7"},
                "auth": {"token": "t"},
            }
        )
        assert valid
        assert errors == []

    def test_run_validation_failure(self):
        skill = ShortCircuitAnalysis()
        result = skill.run({})
        assert result.status == SkillStatus.FAILED
        assert "model.rid" in result.error

    def test_run_success_with_adapter_data(self):
        skill = ShortCircuitAnalysis()
        mock_api, mock_result = _make_mock_api(
            {
                "fault_currents": [
                    {"channel": "I_fault_A", "current_ka": 15.2},
                    {"channel": "I_fault_B", "current_ka": 12.8},
                ],
                "bus_voltages": [
                    {"channel": "V_bus7", "voltage_pu": 0.35},
                ],
            }
        )

        with patch(
            "cloudpss_skills_v2.poweranalysis.short_circuit.Engine"
        ) as mock_factory:
            mock_factory.create_short_circuit_api.return_value = mock_api
            result = skill.run(
                {
                    "model": {"rid": "test", "source": "cloud"},
                    "fault": {"location": "Bus7", "type": "three_phase"},
                    "auth": {"token": "test"},
                    "output": {"path": tempfile.mkdtemp(), "generate_report": False},
                }
            )

        assert result.status == SkillStatus.SUCCESS
        assert "analysis" in result.data
        assert "short_circuit_mva" in result.data

    def test_calculate_short_circuit_capacity(self):
        skill = ShortCircuitAnalysis()
        analysis = {
            "I_A": {"steady_current": 10.0},
            "I_B": {"steady_current": 5.0},
        }
        scc = skill._calculate_short_circuit_capacity(analysis, 500, 100)
        assert "I_A" in scc
        assert scc["I_A"]["short_circuit_mva"] > 0

    def test_build_analysis_from_adapter_data(self):
        skill = ShortCircuitAnalysis()
        data = {
            "fault_currents": [
                {"channel": "ch1", "current_ka": 20.0},
            ],
            "bus_voltages": [
                {"channel": "ch2", "voltage_pu": 0.5},
            ],
        }
        analysis = skill._build_analysis_from_adapter_data(data)
        assert "ch1" in analysis
        assert "peak_current" in analysis["ch1"]
        assert "ch2" in analysis
        assert "min_voltage" in analysis["ch2"]


class TestContingencyAnalysis:
    def test_name_and_description(self):
        skill = ContingencyAnalysis()
        assert skill.name == "contingency_analysis"
        assert "预想事故" in skill.description

    def test_default_config(self):
        skill = ContingencyAnalysis()
        config = skill.get_default_config()
        assert config["skill"] == "contingency_analysis"
        assert config["contingency"]["level"] == "N-1"

    def test_config_schema(self):
        skill = ContingencyAnalysis()
        schema = skill.config_schema
        assert schema["required"] == ["skill", "model"]
        assert "contingency" in schema["properties"]
        assert "ranking" in schema["properties"]

    def test_validate_missing_rid(self):
        skill = ContingencyAnalysis()
        valid, errors = skill.validate({"auth": {"token": "t"}})
        assert not valid

    def test_validate_valid_config(self):
        skill = ContingencyAnalysis()
        valid, errors = skill.validate(
            {"model": {"rid": "test"}, "auth": {"token": "t"}}
        )
        assert valid

    def test_calculate_severity_fail(self):
        skill = ContingencyAnalysis()
        result = {"status": "FAIL"}
        severity = skill._calculate_severity(result, {"min": 0.95, "max": 1.05}, 1.0)
        assert severity == 1.0

    def test_calculate_severity_violation(self):
        skill = ContingencyAnalysis()
        result = {
            "status": "VIOLATION",
            "min_voltage": 0.85,
            "max_voltage": 1.05,
        }
        severity = skill._calculate_severity(result, {"min": 0.95, "max": 1.05}, 1.0)
        assert severity > 0
        assert severity <= 1.0

    def test_calculate_severity_pass(self):
        skill = ContingencyAnalysis()
        result = {
            "status": "PASS",
            "min_voltage": 0.98,
            "max_voltage": 1.02,
        }
        severity = skill._calculate_severity(result, {"min": 0.95, "max": 1.05}, 1.0)
        assert severity == 0.0

    def test_identify_weak_points(self):
        skill = ContingencyAnalysis()
        results = [
            {"name": "Case1", "components": ["Line1", "Line2"], "severity": 0.9},
            {"name": "Case2", "components": ["Line1", "Line3"], "severity": 0.7},
            {"name": "Case3", "components": ["Line2"], "severity": 0.5},
        ]
        weak = skill._identify_weak_points(results, 3)
        assert len(weak) > 0
        line1_count = next(
            w["critical_cases"] for w in weak if w["component"] == "Line1"
        )
        assert line1_count == 2

    def test_discover_components_type_mapping(self):
        """Verify _discover_components maps type strings to ComponentType correctly."""
        from cloudpss_skills_v2.powerskill import ComponentInfo, ComponentType

        skill = ContingencyAnalysis()
        mock_handle = MagicMock()
        branch_comp = ComponentInfo(
            key="line_1",
            name="Line1",
            definition="model/CloudPSS/line",
            component_type=ComponentType.BRANCH,
            args={},
        )
        mock_handle.get_components_by_type.side_effect = lambda ct: (
            [branch_comp] if ct == ComponentType.BRANCH else []
        )

        available = skill._discover_components(mock_handle, ["branch"], [])
        assert len(available) == 1
        assert available[0]["type"] == "branch"
        assert available[0]["key"] == "line_1"

        mock_handle.get_components_by_type.side_effect = lambda ct: []
        available_empty = skill._discover_components(
            mock_handle, ["nonexistent_type"], []
        )
        assert available_empty == []

    def test_run_validation_failure(self):
        skill = ContingencyAnalysis()
        result = skill.run({})
        assert result.status == SkillStatus.FAILED


class TestLossAnalysis:
    def test_name_and_description(self):
        skill = LossAnalysis()
        assert skill.name == "loss_analysis"
        assert "网损" in skill.description

    def test_default_config(self):
        skill = LossAnalysis()
        config = skill.get_default_config()
        assert config["skill"] == "loss_analysis"
        assert "analysis" in config

    def test_config_schema(self):
        skill = LossAnalysis()
        schema = skill.config_schema
        assert schema["required"] == ["skill", "model"]
        assert "analysis" in schema["properties"]

    def test_validate_missing_rid(self):
        skill = LossAnalysis()
        valid, errors = skill.validate({"auth": {"token": "t"}})
        assert not valid

    def test_validate_valid_config(self):
        skill = LossAnalysis()
        valid, errors = skill.validate(
            {"model": {"rid": "test"}, "auth": {"token": "t"}}
        )
        assert valid

    def test_calculate_line_losses(self):
        skill = LossAnalysis()
        branches = [
            {
                "name": "Line1",
                "from_bus": "Bus1",
                "to_bus": "Bus2",
                "power_loss_mw": 2.5,
                "reactive_loss_mvar": 1.2,
                "current_ka": 0.8,
            },
            {
                "name": "Line2",
                "from_bus": "Bus3",
                "to_bus": "Bus4",
                "power_loss_mw": 0.0001,
                "reactive_loss_mvar": 0.0001,
            },
        ]
        skill._calculate_line_losses(branches)
        assert len(skill.branch_losses) == 1
        assert skill.branch_losses[0].branch_id == "Line1"
        assert skill.branch_losses[0].p_loss_mw == 2.5

    def test_generate_summary(self):
        skill = LossAnalysis()
        skill.branch_losses = [
            BranchLoss("L1", "B1", "B2", 3.0, 1.5, 0.5, 60),
            BranchLoss("L2", "B3", "B4", 1.0, 0.5, 0.3, 40),
        ]
        skill.transformer_losses = [
            TransformerLoss("T1", "B1", "B2", None, None, 0.8, 0.3),
        ]
        summary = skill._generate_summary()
        assert summary["total_loss_mw"] == 4.8
        assert summary["branch_loss_mw"] == 4.0
        assert summary["transformer_loss_mw"] == 0.8
        assert summary["branch_count"] == 2
        assert summary["transformer_count"] == 1

    def test_generate_optimization_suggestions(self):
        skill = LossAnalysis()
        skill.branch_losses = [
            BranchLoss("L1", "B1", "B2", 20.0, 5.0, 1.0, 80),
        ]
        skill.transformer_losses = []
        opt = skill._generate_optimization_suggestions()
        assert opt["current_total_loss_mw"] == 20.0
        assert opt["optimization_potential"] > 0
        assert len(opt["suggestions"]) >= 2

    def test_as_float(self):
        assert loss_as_float(None) == 0.0
        assert loss_as_float("") == 0.0
        assert loss_as_float("3.14") == 3.14
        assert loss_as_float(42) == 42.0
        assert loss_as_float("abc", 99) == 99

    def test_branch_to_dict(self):
        skill = LossAnalysis()
        bl = BranchLoss("L1", "B1", "B2", 3.0, 1.5, 0.5, 60)
        d = skill._branch_to_dict(bl)
        assert d["branch_id"] == "L1"
        assert d["p_loss_mw"] == 3.0

    def test_transformer_to_dict(self):
        skill = LossAnalysis()
        tl = TransformerLoss("T1", "B1", "B2", None, None, 0.8, 0.3)
        d = skill._transformer_to_dict(tl)
        assert d["transformer_id"] == "T1"
        assert d["core_loss_mw"] is None
        assert d["total_loss_mw"] == 0.8

    def test_run_validation_failure(self):
        skill = LossAnalysis()
        result = skill.run({})
        assert result.status == SkillStatus.FAILED


class TestVoltageStabilityAnalysis:
    def test_name_and_description(self):
        skill = VoltageStabilityAnalysis()
        assert skill.name == "voltage_stability"
        assert "电压" in skill.description

    def test_default_config(self):
        skill = VoltageStabilityAnalysis()
        config = skill.get_default_config()
        assert config["skill"] == "voltage_stability"
        assert "scan" in config
        assert len(config["scan"]["load_scaling"]) > 0

    def test_config_schema(self):
        skill = VoltageStabilityAnalysis()
        schema = skill.config_schema
        assert schema["required"] == ["skill", "model"]
        assert "scan" in schema["properties"]
        assert "monitoring" in schema["properties"]

    def test_validate_missing_rid(self):
        skill = VoltageStabilityAnalysis()
        valid, errors = skill.validate({"auth": {"token": "t"}})
        assert not valid

    def test_validate_valid_config(self):
        skill = VoltageStabilityAnalysis()
        valid, errors = skill.validate(
            {"model": {"rid": "test"}, "auth": {"token": "t"}}
        )
        assert valid

    def test_matches_bus_identifier(self):
        assert VoltageStabilityAnalysis._matches_bus_identifier("Bus7", "Bus7")
        assert VoltageStabilityAnalysis._matches_bus_identifier("bus7", "Bus7")
        assert not VoltageStabilityAnalysis._matches_bus_identifier("Bus7", "Bus8")
        assert VoltageStabilityAnalysis._matches_bus_identifier("Bus", "Bus_7")

    def test_generate_pv_curve(self):
        skill = VoltageStabilityAnalysis()
        converged = [
            {"scale": 1.0, "voltages": {"Bus30": 1.02, "Bus38": 0.98}},
            {"scale": 1.5, "voltages": {"Bus30": 0.95, "Bus38": 0.88}},
        ]
        pv = skill._generate_pv_curve(converged, ["Bus30", "Bus38"])
        assert len(pv) == 4
        assert pv[0]["bus"] == "Bus30"
        assert pv[0]["scale"] == 1.0
        assert pv[0]["voltage"] == 1.02

    def test_run_validation_failure(self):
        skill = VoltageStabilityAnalysis()
        result = skill.run({})
        assert result.status == SkillStatus.FAILED

    def test_run_with_pf_failure(self):
        skill = VoltageStabilityAnalysis()
        mock_api, mock_result = _make_mock_api()
        mock_result.is_success = False
        mock_result.errors = ["PF failed"]

        mock_handle = MagicMock()
        mock_handle.get_components_by_type.return_value = []
        mock_handle.clone.return_value = mock_handle
        mock_api.get_model_handle.return_value = mock_handle

        with patch(
            "cloudpss_skills_v2.poweranalysis.voltage_stability.Engine"
        ) as mock_factory:
            mock_factory.create_powerflow_api.return_value = mock_api
            result = skill.run(
                {
                    "model": {"rid": "test", "source": "cloud"},
                    "auth": {"token": "test"},
                    "scan": {"load_scaling": [1.0, 1.2]},
                }
            )

        assert result.status == SkillStatus.FAILED
