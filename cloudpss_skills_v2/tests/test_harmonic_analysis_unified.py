"""Tests for HarmonicAnalysis using unified PowerSystemModel."""

import numpy as np
import pytest


def test_harmonic_analysis_runs_on_unified_model():
    """Test that HarmonicAnalysis works with unified PowerSystemModel."""
    from cloudpss_skills_v2.poweranalysis.harmonic_analysis import HarmonicAnalysis
    from cloudpss_skills_v2.core.system_model import PowerSystemModel, Bus, Branch

    # Create a simple 2-bus test system
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ"),
        ],
        branches=[
            Branch(
                from_bus=0,
                to_bus=1,
                name="Line1",
                branch_type="LINE",
                r_pu=0.01,
                x_pu=0.1,
                b_pu=0.001,
            )
        ],
        base_mva=100.0
    )

    analysis = HarmonicAnalysis()
    result = analysis.run(model, {
        "harmonic_orders": [3, 5, 7],
        "sources": [{"bus": "Bus2", "order": 5, "magnitude": 0.05}]
    })

    assert result["status"] == "success"
    assert "harmonic_voltages" in result
    assert "thd" in result  # Total Harmonic Distortion


def test_harmonic_analysis_returns_correct_structure():
    """Test that harmonic analysis returns properly structured results."""
    from cloudpss_skills_v2.poweranalysis.harmonic_analysis import HarmonicAnalysis
    from cloudpss_skills_v2.core.system_model import PowerSystemModel, Bus, Branch

    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ"),
            Bus(bus_id=2, name="Bus3", base_kv=230.0, bus_type="PQ"),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="Line1", r_pu=0.01, x_pu=0.1),
            Branch(from_bus=1, to_bus=2, name="Line2", r_pu=0.01, x_pu=0.1),
        ],
        base_mva=100.0
    )

    analysis = HarmonicAnalysis()
    result = analysis.run(model, {
        "harmonic_orders": [3, 5, 7, 11],
        "sources": [
            {"bus": "Bus2", "order": 5, "magnitude": 0.05},
            {"bus": "Bus3", "order": 7, "magnitude": 0.03},
        ]
    })

    # Check structure
    assert result["status"] == "success"
    assert "harmonic_voltages" in result
    assert "thd" in result
    assert "harmonic_orders" in result

    # Check harmonic voltages structure
    harmonic_voltages = result["harmonic_voltages"]
    assert isinstance(harmonic_voltages, dict)

    # Check THD structure
    thd = result["thd"]
    assert isinstance(thd, dict)
    assert "Bus1" in thd or len(thd) == 0  # May be empty if no harmonics at slack
    assert "Bus2" in thd
    assert "Bus3" in thd

    # THD should be non-negative
    for bus_name, thd_value in thd.items():
        assert thd_value >= 0.0
        assert thd_value < 100.0  # THD percentage should be reasonable


def test_harmonic_analysis_calculates_impedance_matrix():
    """Test that harmonic impedance matrix is built correctly."""
    from cloudpss_skills_v2.poweranalysis.harmonic_analysis import HarmonicAnalysis
    from cloudpss_skills_v2.core.system_model import PowerSystemModel, Bus, Branch

    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ"),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="Line1", r_pu=0.01, x_pu=0.1),
        ],
        base_mva=100.0
    )

    analysis = HarmonicAnalysis()

    # Build Ybus for a harmonic order
    ybus = analysis._build_harmonic_ybus(model, harmonic_order=5)

    # Ybus should be square matrix with size = number of buses
    assert ybus.shape == (2, 2)

    # At harmonic h=5, reactance becomes h * X (5 * 0.1 = 0.5)
    # Susceptance B = -1/X_h = -1/0.5 = -2.0 (approximately, ignoring resistance)


def test_harmonic_analysis_with_no_sources():
    """Test analysis behavior with no harmonic sources."""
    from cloudpss_skills_v2.poweranalysis.harmonic_analysis import HarmonicAnalysis
    from cloudpss_skills_v2.core.system_model import PowerSystemModel, Bus

    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ"),
        ],
        base_mva=100.0
    )

    analysis = HarmonicAnalysis()
    result = analysis.run(model, {
        "harmonic_orders": [3, 5, 7],
        "sources": []  # No sources
    })

    assert result["status"] == "success"
    assert "harmonic_voltages" in result
    assert "thd" in result

    # With no sources, THD should be zero
    thd = result["thd"]
    for bus_name, thd_value in thd.items():
        assert thd_value == pytest.approx(0.0, abs=1e-10)


def test_harmonic_analysis_validates_model():
    """Test that analysis validates the model before running."""
    from cloudpss_skills_v2.poweranalysis.harmonic_analysis import HarmonicAnalysis
    from cloudpss_skills_v2.core.system_model import PowerSystemModel, Bus

    analysis = HarmonicAnalysis()

    # Test with empty model
    empty_model = PowerSystemModel(buses=[], base_mva=100.0)
    result = analysis.run(empty_model, {
        "harmonic_orders": [3, 5],
        "sources": []
    })

    assert result["status"] == "error"
    assert "error" in result


def test_thd_calculation():
    """Test THD calculation from harmonic voltages."""
    from cloudpss_skills_v2.poweranalysis.harmonic_analysis import HarmonicAnalysis

    analysis = HarmonicAnalysis()

    # Test THD calculation with known values
    # V1 = 1.0 (fundamental), V5 = 0.1, V7 = 0.05
    # THD = sqrt(V5^2 + V7^2) / V1 * 100
    # THD = sqrt(0.01 + 0.0025) / 1.0 * 100 = sqrt(0.0125) * 100 = 11.18%
    voltages = {
        1: 1.0,   # Fundamental
        5: 0.1,   # 5th harmonic
        7: 0.05,  # 7th harmonic
    }

    thd = analysis._calculate_thd(voltages)
    expected_thd = np.sqrt(0.1**2 + 0.05**2) / 1.0 * 100
    assert thd == pytest.approx(expected_thd, abs=0.01)


def test_harmonic_analysis_with_transformer():
    """Test analysis with transformer branches."""
    from cloudpss_skills_v2.poweranalysis.harmonic_analysis import HarmonicAnalysis
    from cloudpss_skills_v2.core.system_model import PowerSystemModel, Bus, Branch

    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="HV_Bus", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="LV_Bus", base_kv=11.0, bus_type="PQ"),
        ],
        branches=[
            Branch(
                from_bus=0,
                to_bus=1,
                name="T1",
                branch_type="TRANSFORMER",
                r_pu=0.005,
                x_pu=0.08,
                tap_ratio=1.0,
            )
        ],
        base_mva=100.0
    )

    analysis = HarmonicAnalysis()
    result = analysis.run(model, {
        "harmonic_orders": [3, 5, 7],
        "sources": [{"bus": "LV_Bus", "order": 5, "magnitude": 0.05}]
    })

    assert result["status"] == "success"
    assert "thd" in result
    assert "LV_Bus" in result["thd"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
