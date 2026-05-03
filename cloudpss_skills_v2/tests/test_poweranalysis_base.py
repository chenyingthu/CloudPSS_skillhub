"""Tests for PowerAnalysis base class with unified model support."""

import pytest
from cloudpss_skills_v2.poweranalysis.base import PowerAnalysis
from cloudpss_skills_v2.core.system_model import PowerSystemModel, Bus


class TestAnalysis(PowerAnalysis):
    """Test implementation of PowerAnalysis."""

    def run(self, model, config):
        return {"bus_count": len(model.buses)}


def test_poweranalysis_runs_with_unified_model():
    """Test that PowerAnalysis can run with a unified model."""
    analysis = TestAnalysis()
    model = PowerSystemModel(
        buses=[
            Bus(
                bus_id=0,
                name="Bus1",
                base_kv=230.0,
                bus_type="SLACK",
                v_magnitude_pu=1.0,
                v_angle_degree=0.0,
            )
        ],
        base_mva=100.0,
    )

    result = analysis.run(model, {})
    assert result["bus_count"] == 1


def test_poweranalysis_validate_model_with_valid_model():
    """Test validate_model with a valid model."""
    analysis = TestAnalysis()
    model = PowerSystemModel(
        buses=[
            Bus(
                bus_id=0,
                name="Bus1",
                base_kv=230.0,
                bus_type="SLACK",
                v_magnitude_pu=1.0,
                v_angle_degree=0.0,
            )
        ],
        base_mva=100.0,
    )

    errors = analysis.validate_model(model)
    assert errors == []


def test_poweranalysis_validate_model_no_buses():
    """Test validate_model with no buses."""
    analysis = TestAnalysis()
    model = PowerSystemModel(buses=[], base_mva=100.0)

    errors = analysis.validate_model(model)
    assert "No buses in model" in errors


def test_poweranalysis_validate_model_no_slack_bus():
    """Test validate_model with no slack bus."""
    analysis = TestAnalysis()
    model = PowerSystemModel(
        buses=[
            Bus(
                bus_id=0,
                name="Bus1",
                base_kv=230.0,
                bus_type="PQ",  # Not SLACK
            )
        ],
        base_mva=100.0,
    )

    errors = analysis.validate_model(model)
    assert "No slack bus found" in errors


def test_poweranalysis_validate_model_multiple_errors():
    """Test validate_model with multiple validation errors."""
    analysis = TestAnalysis()
    model = PowerSystemModel(
        buses=[
            Bus(
                bus_id=0,
                name="Bus1",
                base_kv=230.0,
                bus_type="PQ",  # Not SLACK
            ),
            Bus(
                bus_id=1,
                name="Bus2",
                base_kv=230.0,
                bus_type="PV",  # Also not SLACK
            ),
        ],
        base_mva=100.0,
    )

    errors = analysis.validate_model(model)
    assert "No slack bus found" in errors
    assert "No buses in model" not in errors  # Buses exist
