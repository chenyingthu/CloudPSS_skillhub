"""Unit tests for ContingencyAnalysis with unified PowerSystemModel.

TDD approach: Test the refactored ContingencyAnalysis that inherits from PowerAnalysis.
"""

import pytest

from cloudpss_skills_v2.core.system_model import PowerSystemModel, Bus, Branch, Generator
from cloudpss_skills_v2.poweranalysis.contingency_analysis import ContingencyAnalysis
from cloudpss_skills_v2.poweranalysis.base import PowerAnalysis


class TestContingencyAnalysisUnified:
    """Test ContingencyAnalysis with unified PowerSystemModel."""

    def test_contingency_analysis_inherits_from_power_analysis(self):
        """Test that ContingencyAnalysis inherits from PowerAnalysis base class."""
        analysis = ContingencyAnalysis()
        assert isinstance(analysis, PowerAnalysis)

    def test_contingency_analysis_runs_on_unified_model(self):
        """Test basic contingency analysis on unified PowerSystemModel."""
        model = PowerSystemModel(
            buses=[
                Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
                Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ"),
                Bus(bus_id=2, name="Bus3", base_kv=230.0, bus_type="PQ"),
            ],
            branches=[
                Branch(from_bus=0, to_bus=1, name="Line1", branch_type="LINE", rate_a_mva=100),
                Branch(from_bus=1, to_bus=2, name="Line2", branch_type="LINE", rate_a_mva=80),
            ],
            generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=100)],
            base_mva=100.0
        )

        analysis = ContingencyAnalysis()
        result = analysis.run(model, {
            "contingency_type": "n1",
            "check_violations": ["thermal", "voltage"]
        })

        assert result["status"] == "success"
        assert "contingencies" in result
        assert "summary" in result

    def test_contingency_analysis_n1_type(self):
        """Test N-1 contingency analysis."""
        model = PowerSystemModel(
            buses=[
                Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
                Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ"),
                Bus(bus_id=2, name="Bus3", base_kv=230.0, bus_type="PQ"),
            ],
            branches=[
                Branch(from_bus=0, to_bus=1, name="Line1", branch_type="LINE", rate_a_mva=100),
                Branch(from_bus=1, to_bus=2, name="Line2", branch_type="LINE", rate_a_mva=80),
            ],
            generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=100)],
            base_mva=100.0
        )

        analysis = ContingencyAnalysis()
        result = analysis.run(model, {
            "contingency_type": "n1",
            "check_violations": ["thermal", "voltage"]
        })

        # N-1 should create one contingency per branch
        assert len(result["contingencies"]) == 2
        assert result["summary"]["total_cases"] == 2

    def test_contingency_analysis_n2_type(self):
        """Test N-2 contingency analysis."""
        model = PowerSystemModel(
            buses=[
                Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
                Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ"),
                Bus(bus_id=2, name="Bus3", base_kv=230.0, bus_type="PQ"),
                Bus(bus_id=3, name="Bus4", base_kv=230.0, bus_type="PQ"),
            ],
            branches=[
                Branch(from_bus=0, to_bus=1, name="Line1", branch_type="LINE", rate_a_mva=100),
                Branch(from_bus=1, to_bus=2, name="Line2", branch_type="LINE", rate_a_mva=80),
                Branch(from_bus=2, to_bus=3, name="Line3", branch_type="LINE", rate_a_mva=80),
            ],
            generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=100)],
            base_mva=100.0
        )

        analysis = ContingencyAnalysis()
        result = analysis.run(model, {
            "contingency_type": "n2",
            "check_violations": ["thermal", "voltage"]
        })

        # N-2 should create C(3,2) = 3 contingencies
        assert result["status"] == "success"
        assert result["summary"]["total_cases"] == 3

    def test_contingency_analysis_n1_1_type(self):
        """Test N-1-1 contingency analysis."""
        model = PowerSystemModel(
            buses=[
                Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
                Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ"),
                Bus(bus_id=2, name="Bus3", base_kv=230.0, bus_type="PQ"),
            ],
            branches=[
                Branch(from_bus=0, to_bus=1, name="Line1", branch_type="LINE", rate_a_mva=100),
                Branch(from_bus=1, to_bus=2, name="Line2", branch_type="LINE", rate_a_mva=80),
            ],
            generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=100)],
            base_mva=100.0
        )

        analysis = ContingencyAnalysis()
        result = analysis.run(model, {
            "contingency_type": "n1_1",
            "check_violations": ["thermal", "voltage"]
        })

        # N-1-1 should create contingencies for sequential failures
        assert result["status"] == "success"
        assert "contingencies" in result

    def test_contingency_analysis_returns_severity(self):
        """Test that contingency results include severity assessment."""
        model = PowerSystemModel(
            buses=[
                Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
                Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ"),
                Bus(bus_id=2, name="Bus3", base_kv=230.0, bus_type="PQ"),
            ],
            branches=[
                Branch(from_bus=0, to_bus=1, name="Line1", branch_type="LINE", rate_a_mva=100),
                Branch(from_bus=1, to_bus=2, name="Line2", branch_type="LINE", rate_a_mva=80),
            ],
            generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=100)],
            base_mva=100.0
        )

        analysis = ContingencyAnalysis()
        result = analysis.run(model, {
            "contingency_type": "n1",
            "check_violations": ["thermal", "voltage"]
        })

        # Each contingency should have a severity field
        for contingency in result["contingencies"]:
            assert "severity" in contingency
            assert contingency["severity"] in ["normal", "warning", "critical"]

    def test_contingency_analysis_check_violations(self):
        """Test that violation checking works correctly."""
        model = PowerSystemModel(
            buses=[
                Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
                Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ"),
            ],
            branches=[
                Branch(from_bus=0, to_bus=1, name="Line1", branch_type="LINE", rate_a_mva=100),
            ],
            generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=100)],
            base_mva=100.0
        )

        analysis = ContingencyAnalysis()

        # Test with only thermal check
        result_thermal = analysis.run(model, {
            "contingency_type": "n1",
            "check_violations": ["thermal"]
        })
        assert result_thermal["status"] == "success"

        # Test with only voltage check
        result_voltage = analysis.run(model, {
            "contingency_type": "n1",
            "check_violations": ["voltage"]
        })
        assert result_voltage["status"] == "success"

    def test_contingency_analysis_with_no_slack_bus(self):
        """Test that analysis validates model has slack bus."""
        model = PowerSystemModel(
            buses=[
                Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="PQ"),
                Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ"),
            ],
            branches=[
                Branch(from_bus=0, to_bus=1, name="Line1", branch_type="LINE", rate_a_mva=100),
            ],
            generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=100)],
            base_mva=100.0
        )

        analysis = ContingencyAnalysis()
        result = analysis.run(model, {
            "contingency_type": "n1",
            "check_violations": ["thermal", "voltage"]
        })

        # Should fail validation due to missing slack bus
        assert result["status"] == "error"
        assert "slack" in result["error"].lower()

    def test_contingency_analysis_empty_model(self):
        """Test that analysis validates non-empty model."""
        model = PowerSystemModel(
            buses=[],
            branches=[],
            generators=[],
            base_mva=100.0
        )

        analysis = ContingencyAnalysis()
        result = analysis.run(model, {
            "contingency_type": "n1",
            "check_violations": ["thermal", "voltage"]
        })

        # Should fail validation due to empty model
        assert result["status"] == "error"

    def test_contingency_analysis_modifies_model_correctly(self):
        """Test that contingencies create modified models correctly."""
        model = PowerSystemModel(
            buses=[
                Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
                Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ"),
                Bus(bus_id=2, name="Bus3", base_kv=230.0, bus_type="PQ"),
            ],
            branches=[
                Branch(from_bus=0, to_bus=1, name="Line1", branch_type="LINE", rate_a_mva=100),
                Branch(from_bus=1, to_bus=2, name="Line2", branch_type="LINE", rate_a_mva=80),
            ],
            generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=100)],
            base_mva=100.0
        )

        analysis = ContingencyAnalysis()
        result = analysis.run(model, {
            "contingency_type": "n1",
            "check_violations": ["thermal", "voltage"]
        })

        # Each contingency should reference the removed component
        for contingency in result["contingencies"]:
            assert "components" in contingency
            assert len(contingency["components"]) >= 1
            assert "name" in contingency

    def test_contingency_analysis_returns_weak_points(self):
        """Test that analysis identifies weak points in the system."""
        model = PowerSystemModel(
            buses=[
                Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
                Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ"),
                Bus(bus_id=2, name="Bus3", base_kv=230.0, bus_type="PQ"),
            ],
            branches=[
                Branch(from_bus=0, to_bus=1, name="Line1", branch_type="LINE", rate_a_mva=100),
                Branch(from_bus=1, to_bus=2, name="Line2", branch_type="LINE", rate_a_mva=80),
            ],
            generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=100)],
            base_mva=100.0
        )

        analysis = ContingencyAnalysis()
        result = analysis.run(model, {
            "contingency_type": "n1",
            "check_violations": ["thermal", "voltage"]
        })

        # Should include weak points in summary
        assert "weak_points" in result
        assert isinstance(result["weak_points"], list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
