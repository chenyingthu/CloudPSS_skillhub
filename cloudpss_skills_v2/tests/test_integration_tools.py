"""Integration tests for Tools layer with pandapower."""

import pytest
from cloudpss_skills_v2.powerskill import Engine, PowerFlow
from cloudpss_skills_v2.tools.topology_check import TopologyCheckTool
from cloudpss_skills_v2.tools.visualize import VisualizeTool
from cloudpss_skills_v2.tools.report_generator import ReportGeneratorTool
from cloudpss_skills_v2.tools.result_compare import ResultCompareTool


@pytest.mark.pandapower
class TestTopologyCheckToolBasics:
    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_tool_instantiation(self):
        tool = TopologyCheckTool()
        assert tool is not None

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_tool_name(self):
        tool = TopologyCheckTool()
        assert tool.name == "topology_check"

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_tool_has_run_method(self):
        tool = TopologyCheckTool()
        assert hasattr(tool, "run")

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_tool_has_validate(self):
        tool = TopologyCheckTool()
        assert hasattr(tool, "validate")

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_tool_config_schema(self):
        tool = TopologyCheckTool()
        schema = tool.config_schema
        assert schema is not None


@pytest.mark.pandapower
class TestVisualizeToolBasics:
    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_tool_instantiation(self):
        tool = VisualizeTool()
        assert tool is not None

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_tool_name(self):
        tool = VisualizeTool()
        assert tool.name == "visualize"

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_tool_has_run_method(self):
        tool = VisualizeTool()
        assert hasattr(tool, "run")


@pytest.mark.pandapower
class TestReportGeneratorToolBasics:
    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_tool_instantiation(self):
        tool = ReportGeneratorTool()
        assert tool is not None

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_tool_has_run_method(self):
        tool = ReportGeneratorTool()
        assert hasattr(tool, "run")


@pytest.mark.pandapower
class TestResultCompareToolBasics:
    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_tool_instantiation(self):
        tool = ResultCompareTool()
        assert tool is not None

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_tool_has_run_method(self):
        tool = ResultCompareTool()
        assert hasattr(tool, "run")


@pytest.mark.pandapower
class TestToolsRunWithCase14:
    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_topology_run(self):
        tool = TopologyCheckTool()
        result = tool.run({"model": {"rid": "case14"}})
        assert result is not None

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_visualize_run(self):
        tool = VisualizeTool()
        result = tool.run({"model": {"rid": "case14"}})
        assert result is not None

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_report_run(self):
        tool = ReportGeneratorTool()
        result = tool.run({"model": {"rid": "case14"}})
        assert result is not None


@pytest.mark.pandapower
class TestTopologyRunMultipleCases:
    @pytest.mark.parametrize("case", ["case14", "case30", "case57"])
    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_topology_run(self, case):
        tool = TopologyCheckTool()
        result = tool.run({"model": {"rid": case}})
        assert result is not None


@pytest.mark.pandapower
class TestVisualizeRunMultipleCases:
    @pytest.mark.parametrize("case", ["case14", "case30", "case57"])
    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_visualize_run(self, case):
        tool = VisualizeTool()
        result = tool.run({"model": {"rid": case}})
        assert result is not None


@pytest.mark.pandapower
class TestReportRunMultipleCases:
    @pytest.mark.parametrize("case", ["case14", "case30", "case57"])
    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_report_run(self, case):
        tool = ReportGeneratorTool()
        result = tool.run({"model": {"rid": case}})
        assert result is not None
