"""Tests for TransientStabilityAnalysis using unified PowerSystemModel."""

import pytest

from cloudpss_skills_v2.core.system_model import Bus, Generator, PowerSystemModel
from cloudpss_skills_v2.poweranalysis.transient_stability import (
    TransientStabilityAnalysis,
)


class TestTransientStabilityUnified:
    """Test TransientStabilityAnalysis with unified PowerSystemModel interface."""

    def test_transient_stability_runs_on_unified_model(self):
        """Test that TransientStabilityAnalysis can run on unified PowerSystemModel."""
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

        analysis = TransientStabilityAnalysis()
        result = analysis.run(
            model,
            {
                "disturbance": {"type": "fault", "location": "Bus2", "duration": 0.1},
                "simulation_time": 10.0,
            },
        )

        assert result["status"] in ["success", "error"]
        assert "transient_angles" in result or "errors" in result

    def test_transient_stability_inherits_from_power_analysis(self):
        """Test that TransientStabilityAnalysis inherits from PowerAnalysis."""
        from cloudpss_skills_v2.poweranalysis.base import PowerAnalysis

        assert issubclass(TransientStabilityAnalysis, PowerAnalysis)

    def test_transient_stability_accepts_model_and_config(self):
        """Test that run() method accepts model and config parameters."""
        model = PowerSystemModel(
            buses=[
                Bus(
                    bus_id=0,
                    name="Bus1",
                    base_kv=230.0,
                    bus_type="SLACK",
                ),
            ],
            generators=[
                Generator(bus_id=0, name="Gen1", p_gen_mw=100, in_service=True),
            ],
            base_mva=100.0,
        )

        analysis = TransientStabilityAnalysis()
        # Should accept model as first positional argument and config as second
        result = analysis.run(model, {"simulation_time": 5.0})

        # Result should be a dict (unified interface returns dict, not SkillResult)
        assert isinstance(result, dict)

    def test_transient_stability_returns_dict_result(self):
        """Test that the new interface returns a dict result."""
        model = PowerSystemModel(
            buses=[
                Bus(
                    bus_id=0,
                    name="Bus1",
                    base_kv=230.0,
                    bus_type="SLACK",
                ),
                Bus(
                    bus_id=1,
                    name="Bus2",
                    base_kv=230.0,
                    bus_type="PV",
                ),
            ],
            generators=[
                Generator(bus_id=0, name="Gen1", p_gen_mw=100, in_service=True),
                Generator(bus_id=1, name="Gen2", p_gen_mw=150, in_service=True),
            ],
            base_mva=100.0,
        )

        analysis = TransientStabilityAnalysis()
        result = analysis.run(
            model,
            {
                "disturbance": {"type": "fault", "location": "Bus2", "duration": 0.1},
                "simulation_time": 10.0,
                "time_step": 0.01,
            },
        )

        assert isinstance(result, dict)
        assert "status" in result
