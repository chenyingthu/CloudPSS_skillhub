"""Tests for N2SecurityAnalysis using unified PowerSystemModel."""

from __future__ import annotations

import pytest

from cloudpss_skills_v2.core.system_model import PowerSystemModel, Bus, Branch


def test_n2_security_runs_on_unified_model():
    """Test that N2SecurityAnalysis works with unified PowerSystemModel."""
    from cloudpss_skills_v2.poweranalysis.n2_security import N2SecurityAnalysis

    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ"),
            Bus(bus_id=2, name="Bus3", base_kv=230.0, bus_type="PQ"),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="Line1", branch_type="LINE", r_pu=0.01, x_pu=0.1, rate_a_mva=100),
            Branch(from_bus=1, to_bus=2, name="Line2", branch_type="LINE", r_pu=0.01, x_pu=0.1, rate_a_mva=100),
            Branch(from_bus=0, to_bus=2, name="Line3", branch_type="LINE", r_pu=0.02, x_pu=0.2, rate_a_mva=100),
        ],
        base_mva=100.0
    )

    analysis = N2SecurityAnalysis()
    result = analysis.run(model, {"check_pairs": []})

    assert result["status"] == "success"
    assert "n2_results" in result
    assert "total_pairs" in result


def test_n2_security_generates_all_pairs():
    """Test that N2SecurityAnalysis generates all branch pairs."""
    from cloudpss_skills_v2.poweranalysis.n2_security import N2SecurityAnalysis

    # 4 branches should generate C(4,2) = 6 pairs
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ"),
            Bus(bus_id=2, name="Bus3", base_kv=230.0, bus_type="PQ"),
            Bus(bus_id=3, name="Bus4", base_kv=230.0, bus_type="PQ"),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="Line1", branch_type="LINE", r_pu=0.01, x_pu=0.1, rate_a_mva=100),
            Branch(from_bus=1, to_bus=2, name="Line2", branch_type="LINE", r_pu=0.01, x_pu=0.1, rate_a_mva=100),
            Branch(from_bus=2, to_bus=3, name="Line3", branch_type="LINE", r_pu=0.01, x_pu=0.1, rate_a_mva=100),
            Branch(from_bus=0, to_bus=3, name="Line4", branch_type="LINE", r_pu=0.02, x_pu=0.2, rate_a_mva=100),
        ],
        base_mva=100.0
    )

    analysis = N2SecurityAnalysis()
    result = analysis.run(model, {"check_pairs": []})

    # With 4 branches, we should have 6 unique pairs (4 choose 2)
    assert result["total_pairs"] == 6


def test_n2_security_inherits_from_power_analysis():
    """Test that N2SecurityAnalysis inherits from PowerAnalysis base class."""
    from cloudpss_skills_v2.poweranalysis.n2_security import N2SecurityAnalysis
    from cloudpss_skills_v2.poweranalysis.base import PowerAnalysis

    analysis = N2SecurityAnalysis()
    assert isinstance(analysis, PowerAnalysis)


def test_n2_security_validates_model():
    """Test that N2SecurityAnalysis validates model before analysis."""
    from cloudpss_skills_v2.poweranalysis.n2_security import N2SecurityAnalysis

    # Empty model should fail validation
    model = PowerSystemModel(buses=[], branches=[], base_mva=100.0)

    analysis = N2SecurityAnalysis()
    result = analysis.run(model, {})

    assert result["status"] == "error"


def test_n2_security_checks_specific_pairs():
    """Test that N2SecurityAnalysis can check specific branch pairs."""
    from cloudpss_skills_v2.poweranalysis.n2_security import N2SecurityAnalysis

    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ"),
            Bus(bus_id=2, name="Bus3", base_kv=230.0, bus_type="PQ"),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="Line1", branch_type="LINE", r_pu=0.01, x_pu=0.1, rate_a_mva=100),
            Branch(from_bus=1, to_bus=2, name="Line2", branch_type="LINE", r_pu=0.01, x_pu=0.1, rate_a_mva=100),
            Branch(from_bus=0, to_bus=2, name="Line3", branch_type="LINE", r_pu=0.02, x_pu=0.2, rate_a_mva=100),
        ],
        base_mva=100.0
    )

    analysis = N2SecurityAnalysis()
    # Check only one specific pair
    result = analysis.run(model, {"check_pairs": [("Line1", "Line2")]})

    assert result["status"] == "success"
    assert result["total_pairs"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
