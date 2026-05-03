"""Tests for TheveninEquivalentAnalysis with unified PowerSystemModel."""

import pytest
import numpy as np

from cloudpss_skills_v2.poweranalysis.thevenin_equivalent import TheveninEquivalentAnalysis
from cloudpss_skills_v2.core.system_model import PowerSystemModel, Bus, Branch


class TestTheveninEquivalentUnified:
    """Test Thevenin Equivalent Analysis with unified PowerSystemModel."""

    def test_thevenin_equivalent_runs_on_unified_model(self):
        """Test basic Thevenin equivalent calculation on a simple 2-bus system."""
        model = PowerSystemModel(
            buses=[
                Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK", v_magnitude_pu=1.0),
                Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ", v_magnitude_pu=0.98),
            ],
            branches=[
                Branch(from_bus=0, to_bus=1, name="Line1", branch_type="LINE", r_pu=0.01, x_pu=0.1),
            ],
            base_mva=100.0
        )

        analysis = TheveninEquivalentAnalysis()
        result = analysis.run(model, {"target_bus": "Bus2"})

        assert result["status"] == "success"
        assert "thevenin_voltage_pu" in result
        assert "thevenin_impedance_pu" in result

    def test_thevenin_equivalent_3_bus_system(self):
        """Test Thevenin equivalent on a 3-bus system."""
        # Simple 3-bus system: Bus0 (slack) -- Bus1 -- Bus2
        model = PowerSystemModel(
            buses=[
                Bus(bus_id=0, name="Slack", base_kv=230.0, bus_type="SLACK", v_magnitude_pu=1.0, v_angle_degree=0.0),
                Bus(bus_id=1, name="Bus1", base_kv=230.0, bus_type="PQ", v_magnitude_pu=0.98, v_angle_degree=-2.0),
                Bus(bus_id=2, name="Bus2", base_kv=230.0, bus_type="PQ", v_magnitude_pu=0.96, v_angle_degree=-4.0),
            ],
            branches=[
                Branch(from_bus=0, to_bus=1, name="Line1", branch_type="LINE", r_pu=0.01, x_pu=0.1),
                Branch(from_bus=1, to_bus=2, name="Line2", branch_type="LINE", r_pu=0.02, x_pu=0.15),
            ],
            base_mva=100.0
        )

        analysis = TheveninEquivalentAnalysis()
        result = analysis.run(model, {"target_bus": "Bus2"})

        assert result["status"] == "success"
        assert "thevenin_voltage_pu" in result
        assert "thevenin_impedance_pu" in result

        # Verify Thevenin impedance is positive
        z_th = result["thevenin_impedance_pu"]
        assert z_th > 0, f"Thevenin impedance should be positive, got {z_th}"

        # Verify Thevenin voltage is reasonable (close to operating voltage)
        v_th = result["thevenin_voltage_pu"]
        assert 0.5 <= v_th <= 1.5, f"Thevenin voltage {v_th} p.u. out of reasonable range"

    def test_thevenin_equivalent_by_bus_id(self):
        """Test Thevenin equivalent using bus ID instead of name."""
        model = PowerSystemModel(
            buses=[
                Bus(bus_id=0, name="Slack", base_kv=230.0, bus_type="SLACK", v_magnitude_pu=1.0),
                Bus(bus_id=1, name="LoadBus", base_kv=230.0, bus_type="PQ", v_magnitude_pu=0.97),
            ],
            branches=[
                Branch(from_bus=0, to_bus=1, name="Line1", branch_type="LINE", r_pu=0.02, x_pu=0.08),
            ],
            base_mva=100.0
        )

        analysis = TheveninEquivalentAnalysis()
        result = analysis.run(model, {"target_bus": 1})  # Using bus_id

        assert result["status"] == "success"
        assert "thevenin_voltage_pu" in result
        assert "thevenin_impedance_pu" in result

    def test_thevenin_equivalent_invalid_bus(self):
        """Test error handling for non-existent bus."""
        model = PowerSystemModel(
            buses=[
                Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK", v_magnitude_pu=1.0),
            ],
            branches=[],
            base_mva=100.0
        )

        analysis = TheveninEquivalentAnalysis()
        result = analysis.run(model, {"target_bus": "NonExistentBus"})

        assert result["status"] == "error"
        assert "error" in result

    def test_thevenin_equivalent_inherits_power_analysis(self):
        """Test that TheveninEquivalentAnalysis inherits from PowerAnalysis."""
        from cloudpss_skills_v2.poweranalysis.base import PowerAnalysis

        analysis = TheveninEquivalentAnalysis()
        assert isinstance(analysis, PowerAnalysis), \
            "TheveninEquivalentAnalysis should inherit from PowerAnalysis"
