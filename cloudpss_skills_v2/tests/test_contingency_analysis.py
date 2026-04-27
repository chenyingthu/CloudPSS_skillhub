import pytest

from cloudpss_skills_v2.core.skill_result import SkillStatus
from cloudpss_skills_v2.poweranalysis.contingency_analysis import ContingencyAnalysis


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
        assert summary == {
            "total_cases": 2,
            "passed": 2,
            "failed": 0,
            "errors": 0,
            "pass_rate": 100.0,
            "severe_cases": 0,
        }
        assert result.data["base_case"] == {"bus_count": 14, "branch_count": 20}
        assert len(result.data["all_results"]) == summary["total_cases"]
        assert len(result.data["top_severe_cases"]) == 2
        assert [case["components"] for case in result.data["top_severe_cases"]] == [
            ["line:0"],
            ["line:1"],
        ]
        assert result.metrics["total_cases"] == summary["total_cases"]
        assert result.metrics["passed"] == summary["passed"]
        assert all(case["status"] == "PASS" for case in result.data["all_results"])
        assert all(0 <= case["severity"] <= 1 for case in result.data["all_results"])
        assert {p["component"] for p in result.data["weak_points"]} == {
            "line:0",
            "line:1",
        }
