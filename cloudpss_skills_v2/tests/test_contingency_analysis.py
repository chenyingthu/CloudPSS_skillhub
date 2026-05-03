import pytest

from cloudpss_skills_v2.core.skill_result import SkillStatus
from cloudpss_skills_v2.poweranalysis.contingency_analysis import ContingencyAnalysis
from cloudpss_skills_v2.powerskill import ComponentType


class FakeComponent:
    def __init__(self, key, name=None, args=None, properties=None):
        self.key = key
        self.name = name or key
        self.args = args
        self.properties = properties or {}


class FakeHandle:
    def __init__(self, by_type):
        self.by_type = by_type

    def get_components_by_type(self, component_type):
        return self.by_type.get(component_type, [])


class TestContingencyAnalysis:
    @pytest.fixture
    def instance(self):
        return ContingencyAnalysis()

    def test_import(self):
        assert ContingencyAnalysis is not None

    def test_class_attributes(self, instance):
        assert hasattr(instance, "name") or hasattr(instance, "run")

    def test_config_schema(self, instance):
        schema = instance.config_schema
        assert isinstance(schema, dict)
        assert "properties" in schema

    def test_get_default_config(self, instance):
        config = instance.get_default_config()
        assert isinstance(config, dict)

    def test_pandapower_n1_branch_matrix_reports_consistent_summary(self, instance, tmp_path):
        result = instance.run(
            {
                "engine": "pandapower",
                "model": {"rid": "case14", "source": "local"},
                "contingency": {
                    "level": "N-1",
                    "components": ["line:0", "line:1"],
                    "component_types": ["branch"],
                    "max_combinations": 2,
                },
                "analysis": {
                    "check_voltage": True,
                    "check_thermal": True,
                    "voltage_limit": {"min": 0.8, "max": 1.2},
                    "thermal_limit": 200.0,
                    "severity_threshold": 0.8,
                },
                "ranking": {"top_n": 2},
                "output": {
                    "format": "json",
                    "path": str(tmp_path),
                    "generate_report": False,
                },
            }
        )

        assert result.status == SkillStatus.SUCCESS
        summary = result.data["summary"]
        assert summary["total_cases"] == 2
        assert summary["passed"] == 2
        assert summary["failed"] == 0
        assert summary["pass_rate"] == 100.0
        assert len(result.data["all_results"]) == summary["total_cases"]
        # Status can be "normal" or "PASS" depending on implementation
        assert all(case["status"] in ("normal", "PASS") for case in result.data["all_results"])
        assert [case["components"] for case in result.data["all_results"]] == [
            ["line:0"],
            ["line:1"],
        ]

    def test_handle_converter_skips_transformer_without_valid_endpoints(self, instance):
        handle = FakeHandle(
            {
                ComponentType.BUS: [
                    FakeComponent("bus:0", "Bus 0"),
                    FakeComponent("bus:1", "Bus 1"),
                ],
                ComponentType.SOURCE: [FakeComponent("source:0", args={"bus": "bus:0"})],
                ComponentType.BRANCH: [],
                ComponentType.TRANSFORMER: [
                    FakeComponent("trafo:bad", args={"from_bus": "", "to_bus": ""})
                ],
            }
        )

        model = instance._convert_handle_to_model(handle)

        assert len(model.buses) == 2
        assert model.branches == []

    def test_handle_converter_uses_transformer_args(self, instance):
        handle = FakeHandle(
            {
                ComponentType.BUS: [
                    FakeComponent("bus:0", "Bus 0"),
                    FakeComponent("bus:1", "Bus 1"),
                ],
                ComponentType.SOURCE: [FakeComponent("source:0", args={"bus": "bus:0"})],
                ComponentType.BRANCH: [],
                ComponentType.TRANSFORMER: [
                    FakeComponent(
                        "trafo:0",
                        args={"from_bus": "bus:0", "to_bus": "bus:1", "x_pu": 0.08},
                    )
                ],
            }
        )

        model = instance._convert_handle_to_model(handle)

        assert len(model.branches) == 1
        assert model.branches[0].branch_type == "TRANSFORMER"
        assert model.branches[0].x_pu == 0.08
