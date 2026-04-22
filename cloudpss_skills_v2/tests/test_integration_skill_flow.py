"""Skill integration tests: End-to-end workflows with pandapower."""

import pytest
from cloudpss_skills_v2.powerskill import Engine, PowerFlow, ShortCircuit
from cloudpss_skills_v2.powerapi import SimulationStatus
from cloudpss_skills_v2.core.skill_result import SkillStatus
from cloudpss_skills_v2.tools.topology_check import TopologyCheckTool
from cloudpss_skills_v2.tools.visualize import VisualizeTool
from cloudpss_skills_v2.tools.report_generator import ReportGeneratorTool


@pytest.mark.pandapower
class TestSkillWorkflowPowerFlow:
    def test_create_powerflow_skill(self):
        pf = Engine.create_powerflow(engine="pandapower")
        assert pf is not None

    def test_load_ieee_case(self):
        pf = Engine.create_powerflow(engine="pandapower")
        pf.adapter.connect()
        success = pf.adapter.load_model("case14")
        assert success is True

    def test_run_powerflow_skill(self):
        pf = Engine.create_powerflow(engine="pandapower")
        pf.adapter.connect()
        result = pf.adapter.run_simulation({"model_id": "case14"})
        assert result.status == SimulationStatus.COMPLETED
        assert result.data is not None
        assert len(result.data.get("buses", [])) > 0


@pytest.mark.pandapower
class TestSkillWorkflowShortCircuit:
    def test_create_short_circuit_skill(self):
        sc = Engine.create_short_circuit(engine="pandapower")
        assert sc is not None

    def test_run_short_circuit_skill(self):
        sc = Engine.create_short_circuit(engine="pandapower")
        sc.adapter.connect()
        result = sc.adapter.run_simulation({"model_id": "case14"})
        assert result.status == SimulationStatus.COMPLETED


@pytest.mark.pandapower
class TestSkillWorkflowTopologyCheck:
    def test_topology_tool_success(self):
        tool = TopologyCheckTool()
        result = tool.run({"model": {"rid": "case14"}})
        assert result.status == SkillStatus.SUCCESS
        assert result.data is not None

    def test_topology_tool_returns_valid_data(self):
        tool = TopologyCheckTool()
        result = tool.run({"model": {"rid": "case14"}})
        assert result.status == SkillStatus.SUCCESS
        assert isinstance(result.data, dict)


@pytest.mark.pandapower
class TestSkillWorkflowVisualize:
    def test_visualize_tool_success(self):
        tool = VisualizeTool()
        result = tool.run({"model": {"rid": "case14"}})
        assert result.status == SkillStatus.SUCCESS
        assert result.data is not None


@pytest.mark.pandapower
class TestSkillWorkflowReport:
    def test_report_needs_sections(self):
        tool = ReportGeneratorTool()
        result = tool.run({"model": {"rid": "case14"}})
        assert result.status == SkillStatus.FAILED

    def test_report_with_sections(self):
        tool = ReportGeneratorTool()
        result = tool.run(
            {"model": {"rid": "case14"}, "report": {"sections": ["summary"]}}
        )
        assert result.status == SkillStatus.SUCCESS
        assert result.data is not None


@pytest.mark.pandapower
class TestSkillWorkflowMultiCase:
    @pytest.mark.parametrize("case", ["case14", "case30", "case57"])
    def test_powerflow_multiple_cases(self, case):
        pf = Engine.create_powerflow(engine="pandapower")
        pf.adapter.connect()
        result = pf.adapter.run_simulation({"model_id": case})
        assert result.status == SimulationStatus.COMPLETED


@pytest.mark.pandapower
class TestSkillWorkflowChain:
    def test_pf_then_topology(self):
        pf = Engine.create_powerflow(engine="pandapower")
        pf.adapter.connect()
        pf_result = pf.adapter.run_simulation({"model_id": "case14"})
        assert pf_result.status == SimulationStatus.COMPLETED

        topology = TopologyCheckTool()
        topo_result = topology.run({"model": {"rid": "case14"}})
        assert topo_result.status == SkillStatus.SUCCESS
        assert topo_result.data is not None

    def test_full_chain_pf_viz_report(self):
        pf = Engine.create_powerflow(engine="pandapower")
        pf.adapter.connect()
        pf_result = pf.adapter.run_simulation({"model_id": "case14"})
        assert pf_result.status == SimulationStatus.COMPLETED

        viz = VisualizeTool()
        viz_result = viz.run({"model": {"rid": "case14"}})
        assert viz_result.status == SkillStatus.SUCCESS

        report = ReportGeneratorTool()
        report_result = report.run(
            {"model": {"rid": "case14"}, "report": {"sections": ["summary"]}}
        )
        assert report_result.status == SkillStatus.SUCCESS


@pytest.mark.pandapower
class TestSkillValidation:
    def test_powerflow_validates_config(self):
        pf = Engine.create_powerflow(engine="pandapower")
        valid = pf.adapter.validate_config({"model_id": "case14"})
        assert valid.valid is True

    def test_powerflow_rejects_invalid(self):
        pf = Engine.create_powerflow(engine="pandapower")
        pf.adapter.connect()
        result = pf.adapter.run_simulation({"model_id": "invalid"})
        assert result.status == SimulationStatus.FAILED


@pytest.mark.pandapower
class TestSkillErrorRecovery:
    def test_graceful_failure_invalid_case(self):
        pf = Engine.create_powerflow(engine="pandapower")
        pf.adapter.connect()
        result = pf.adapter.run_simulation({"model_id": "nonexistent_case"})
        assert result.status == SimulationStatus.FAILED
        assert len(result.errors) > 0
