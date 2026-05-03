"""Tests for ParameterSensitivityAnalysis using unified PowerSystemModel."""

from __future__ import annotations

import pytest

from cloudpss_skills_v2.core.system_model import Bus, Branch, Load, PowerSystemModel
from cloudpss_skills_v2.poweranalysis.parameter_sensitivity import ParameterSensitivityAnalysis


def test_parameter_sensitivity_runs_on_unified_model():
    """Test that ParameterSensitivityAnalysis can run on unified PowerSystemModel."""
    model = PowerSystemModel(
        buses=[
            Bus(
                bus_id=0,
                name="Bus1",
                base_kv=230.0,
                bus_type="SLACK",
                v_magnitude_pu=1.0,
                v_angle_degree=0.0,
            ),
            Bus(
                bus_id=1,
                name="Bus2",
                base_kv=230.0,
                bus_type="PQ",
                v_magnitude_pu=0.98,
                v_angle_degree=-2.0,
            ),
        ],
        branches=[
            Branch(
                from_bus=0,
                to_bus=1,
                name="Line1",
                branch_type="LINE",
                r_pu=0.01,
                x_pu=0.1,
                rate_a_mva=100.0,
            ),
        ],
        loads=[Load(bus_id=1, name="Load1", p_mw=50, q_mvar=10)],
        base_mva=100.0,
    )

    analysis = ParameterSensitivityAnalysis()
    result = analysis.run(
        model, {"target_parameter": "load.p_mw", "delta": 0.01}
    )

    assert result["status"] == "success"
    assert "sensitivities" in result
    assert "rankings" in result


def test_parameter_sensitivity_inherits_from_power_analysis():
    """Test that ParameterSensitivityAnalysis inherits from PowerAnalysis."""
    from cloudpss_skills_v2.poweranalysis.base import PowerAnalysis

    analysis = ParameterSensitivityAnalysis()
    assert isinstance(analysis, PowerAnalysis)


def test_parameter_sensitivity_validates_model():
    """Test that analysis validates model before running."""
    # Empty model should fail validation
    empty_model = PowerSystemModel(buses=[], branches=[], loads=[])

    analysis = ParameterSensitivityAnalysis()
    result = analysis.run(empty_model, {"target_parameter": "load.p_mw"})

    assert result["status"] == "error"
    assert "errors" in result


def test_parameter_sensitivity_load_sensitivity():
    """Test load sensitivity calculation."""
    model = PowerSystemModel(
        buses=[
            Bus(
                bus_id=0,
                name="Bus1",
                base_kv=230.0,
                bus_type="SLACK",
                v_magnitude_pu=1.0,
                v_angle_degree=0.0,
            ),
            Bus(
                bus_id=1,
                name="Bus2",
                base_kv=230.0,
                bus_type="PQ",
                v_magnitude_pu=0.98,
                v_angle_degree=-2.0,
            ),
            Bus(
                bus_id=2,
                name="Bus3",
                base_kv=230.0,
                bus_type="PQ",
                v_magnitude_pu=0.97,
                v_angle_degree=-3.0,
            ),
        ],
        branches=[
            Branch(
                from_bus=0,
                to_bus=1,
                name="Line1",
                branch_type="LINE",
                r_pu=0.01,
                x_pu=0.1,
                rate_a_mva=100.0,
            ),
            Branch(
                from_bus=1,
                to_bus=2,
                name="Line2",
                branch_type="LINE",
                r_pu=0.02,
                x_pu=0.15,
                rate_a_mva=80.0,
            ),
        ],
        loads=[
            Load(bus_id=1, name="Load1", p_mw=50, q_mvar=10),
            Load(bus_id=2, name="Load2", p_mw=30, q_mvar=5),
        ],
        base_mva=100.0,
    )

    analysis = ParameterSensitivityAnalysis()
    result = analysis.run(
        model, {"target_parameter": "load.p_mw", "delta": 0.01}
    )

    assert result["status"] == "success"
    assert len(result["sensitivities"]) == 2

    # Check sensitivity structure
    for sens in result["sensitivities"]:
        assert "component" in sens
        assert "bus_id" in sens
        assert "parameter" in sens
        assert "base_value" in sens
        assert "sensitivity" in sens

    # Check rankings are sorted by absolute sensitivity
    rankings = result["rankings"]
    for i in range(len(rankings) - 1):
        assert abs(rankings[i]["sensitivity"]) >= abs(rankings[i + 1]["sensitivity"])


def test_parameter_sensitivity_branch_sensitivity():
    """Test branch sensitivity calculation."""
    model = PowerSystemModel(
        buses=[
            Bus(
                bus_id=0,
                name="Bus1",
                base_kv=230.0,
                bus_type="SLACK",
                v_magnitude_pu=1.0,
                v_angle_degree=0.0,
            ),
            Bus(
                bus_id=1,
                name="Bus2",
                base_kv=230.0,
                bus_type="PQ",
                v_magnitude_pu=0.98,
                v_angle_degree=-2.0,
            ),
        ],
        branches=[
            Branch(
                from_bus=0,
                to_bus=1,
                name="Line1",
                branch_type="LINE",
                r_pu=0.01,
                x_pu=0.1,
                rate_a_mva=100.0,
            ),
        ],
        loads=[Load(bus_id=1, name="Load1", p_mw=50, q_mvar=10)],
        base_mva=100.0,
    )

    analysis = ParameterSensitivityAnalysis()
    result = analysis.run(
        model, {"target_parameter": "branch.r_pu", "delta": 0.01}
    )

    assert result["status"] == "success"
    assert "sensitivities" in result


def test_parameter_sensitivity_includes_transformer_branches():
    """Transformer branches should participate in branch sensitivity rankings."""
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="Bus2", base_kv=115.0, bus_type="PQ"),
        ],
        branches=[
            Branch(
                from_bus=0,
                to_bus=1,
                name="T1",
                branch_type="TRANSFORMER",
                r_pu=0.005,
                x_pu=0.06,
                rate_a_mva=80.0,
                tap_ratio=1.05,
            ),
        ],
        loads=[Load(bus_id=1, name="Load1", p_mw=50, q_mvar=10)],
        base_mva=100.0,
    )

    result = ParameterSensitivityAnalysis().run(
        model, {"target_parameter": "branch.x_pu", "delta": 0.01}
    )

    assert result["status"] == "success"
    assert [item["component"] for item in result["sensitivities"]] == ["T1"]
    assert result["sensitivities"][0]["base_value"] == 0.06


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
