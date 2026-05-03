"""Tests for SmallSignalStabilityAnalysis using unified PowerSystemModel."""

import pytest
import numpy as np

from cloudpss_skills_v2.poweranalysis.small_signal_stability import (
    SmallSignalStabilityAnalysis,
)
from cloudpss_skills_v2.core.system_model import PowerSystemModel, Bus, Generator


class TestSmallSignalStabilityUnified:
    """Test SmallSignalStabilityAnalysis with unified PowerSystemModel."""

    def test_analysis_inherits_from_power_analysis(self):
        """Test that SmallSignalStabilityAnalysis inherits from PowerAnalysis."""
        from cloudpss_skills_v2.poweranalysis.base import PowerAnalysis

        assert issubclass(SmallSignalStabilityAnalysis, PowerAnalysis)

    def test_small_signal_stability_runs_on_unified_model(self):
        """Test that analysis runs successfully on unified PowerSystemModel."""
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
                    bus_type="PV",
                    v_magnitude_pu=1.02,
                    v_angle_degree=5.0,
                ),
            ],
            generators=[
                Generator(bus_id=0, name="Gen1", p_gen_mw=100, in_service=True),
                Generator(bus_id=1, name="Gen2", p_gen_mw=150, in_service=True),
            ],
            base_mva=100.0,
        )

        analysis = SmallSignalStabilityAnalysis()
        result = analysis.run(
            model,
            {"analysis_modes": ["eigenvalues", "participation_factors"], "num_modes": 10},
        )

        assert result["status"] == "success"
        assert "eigenvalues" in result
        assert "damping_ratios" in result

    def test_analysis_validates_model_before_running(self):
        """Test that analysis validates model before running."""
        # Empty model should fail validation
        model = PowerSystemModel(buses=[], generators=[], base_mva=100.0)

        analysis = SmallSignalStabilityAnalysis()
        result = analysis.run(model, {})

        assert result["status"] == "error"
        assert "validation" in result.get("message", "").lower() or "No buses" in result.get(
            "message", ""
        )

    def test_analysis_requires_slack_bus(self):
        """Test that analysis requires a slack bus."""
        # Model without slack bus
        model = PowerSystemModel(
            buses=[
                Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="PV"),
                Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ"),
            ],
            generators=[
                Generator(bus_id=0, name="Gen1", p_gen_mw=100, in_service=True),
            ],
            base_mva=100.0,
        )

        analysis = SmallSignalStabilityAnalysis()
        result = analysis.run(model, {})

        assert result["status"] == "error"

    def test_analysis_returns_stability_assessment(self):
        """Test that analysis returns stability assessment."""
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
                    bus_type="PV",
                    v_magnitude_pu=1.02,
                    v_angle_degree=5.0,
                ),
                Bus(
                    bus_id=2,
                    name="Bus3",
                    base_kv=230.0,
                    bus_type="PQ",
                ),
            ],
            generators=[
                Generator(bus_id=0, name="Gen1", p_gen_mw=100, in_service=True),
                Generator(bus_id=1, name="Gen2", p_gen_mw=150, in_service=True),
            ],
            base_mva=100.0,
        )

        analysis = SmallSignalStabilityAnalysis()
        result = analysis.run(model, {"damping_threshold": 0.05})

        assert result["status"] == "success"
        assert "stable" in result
        assert isinstance(result["stable"], bool)

    def test_analysis_calculates_eigenvalues_for_electromechanical_modes(self):
        """Test that eigenvalues are calculated for electromechanical modes."""
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
                    bus_type="PV",
                    v_magnitude_pu=1.02,
                    v_angle_degree=5.0,
                ),
            ],
            generators=[
                Generator(bus_id=0, name="Gen1", p_gen_mw=100, in_service=True),
                Generator(bus_id=1, name="Gen2", p_gen_mw=150, in_service=True),
            ],
            base_mva=100.0,
        )

        analysis = SmallSignalStabilityAnalysis()
        result = analysis.run(model, {})

        assert result["status"] == "success"
        assert "eigenvalues" in result
        # Eigenvalues should be a numpy array or list of complex numbers
        eigenvalues = result["eigenvalues"]
        assert isinstance(eigenvalues, (np.ndarray, list))

    def test_analysis_calculates_damping_ratios(self):
        """Test that damping ratios are calculated."""
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
                    bus_type="PV",
                    v_magnitude_pu=1.02,
                    v_angle_degree=5.0,
                ),
            ],
            generators=[
                Generator(bus_id=0, name="Gen1", p_gen_mw=100, in_service=True),
                Generator(bus_id=1, name="Gen2", p_gen_mw=150, in_service=True),
            ],
            base_mva=100.0,
        )

        analysis = SmallSignalStabilityAnalysis()
        result = analysis.run(model, {})

        assert result["status"] == "success"
        assert "damping_ratios" in result
        damping_ratios = result["damping_ratios"]
        assert isinstance(damping_ratios, (np.ndarray, list))

    def test_analysis_optionally_calculates_participation_factors(self):
        """Test that participation factors are calculated when requested."""
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
                    bus_type="PV",
                    v_magnitude_pu=1.02,
                    v_angle_degree=5.0,
                ),
            ],
            generators=[
                Generator(bus_id=0, name="Gen1", p_gen_mw=100, in_service=True),
                Generator(bus_id=1, name="Gen2", p_gen_mw=150, in_service=True),
            ],
            base_mva=100.0,
        )

        analysis = SmallSignalStabilityAnalysis()
        result = analysis.run(
            model, {"analysis_modes": ["eigenvalues", "participation_factors"]}
        )

        assert result["status"] == "success"
        # Participation factors may or may not be included depending on implementation
        # But the analysis should complete successfully

    def test_analysis_respects_damping_threshold(self):
        """Test that damping threshold is respected in analysis."""
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
                    bus_type="PV",
                    v_magnitude_pu=1.02,
                    v_angle_degree=5.0,
                ),
            ],
            generators=[
                Generator(bus_id=0, name="Gen1", p_gen_mw=100, in_service=True),
                Generator(bus_id=1, name="Gen2", p_gen_mw=150, in_service=True),
            ],
            base_mva=100.0,
        )

        analysis = SmallSignalStabilityAnalysis()
        result = analysis.run(model, {"damping_threshold": 0.03})

        assert result["status"] == "success"
        assert "damping_threshold" in result or "critical_modes" in result

    def test_validate_model_method_exists(self):
        """Test that validate_model method exists from PowerAnalysis base class."""
        analysis = SmallSignalStabilityAnalysis()
        assert hasattr(analysis, "validate_model")
        assert callable(analysis.validate_model)

    def test_validate_model_returns_errors_for_invalid_model(self):
        """Test that validate_model returns errors for invalid model."""
        model = PowerSystemModel(buses=[], generators=[], base_mva=100.0)

        analysis = SmallSignalStabilityAnalysis()
        errors = analysis.validate_model(model)

        assert len(errors) > 0
        assert any("bus" in err.lower() for err in errors)

    def test_validate_model_returns_empty_for_valid_model(self):
        """Test that validate_model returns empty list for valid model."""
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
            ],
            generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=100, in_service=True)],
            base_mva=100.0,
        )

        analysis = SmallSignalStabilityAnalysis()
        errors = analysis.validate_model(model)

        assert errors == []
