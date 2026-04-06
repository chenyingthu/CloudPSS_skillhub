#!/usr/bin/env python3
"""
电压稳定性分析技能 - 单元测试
"""

from unittest.mock import Mock, patch

from cloudpss_skills.builtin.voltage_stability import VoltageStabilitySkill
from cloudpss_skills.core.base import SkillStatus


def make_table(rows):
    columns = {}
    for row in rows:
        for key, value in row.items():
            columns.setdefault(key, []).append(value)
    return [{
        "type": "table",
        "data": {
            "columns": [{"name": key, "data": values} for key, values in columns.items()]
        },
    }]


class TestVoltageStabilityUnit:
    def test_extract_bus_voltages_matches_targets_from_real_rows(self):
        skill = VoltageStabilitySkill()
        result = Mock()
        result.getBuses.return_value = make_table(
            [
                {"Bus": "canvas_0_1091", "Vm": 0.9633},
                {"Bus": "canvas_0_1088", "Vm": 0.9878},
            ]
        )

        voltages = skill._extract_bus_voltages(result, ["canvas_0_1091", "canvas_0_1088"])

        assert voltages == {
            "canvas_0_1091": 0.9633,
            "canvas_0_1088": 0.9878,
        }

    @patch("cloudpss.setToken")
    @patch("cloudpss.Model")
    def test_run_fails_when_target_bus_voltages_cannot_be_extracted(self, mock_model_class, mock_set_token, tmp_path):
        skill = VoltageStabilitySkill()

        model = Mock()
        model.name = "TestModel"
        model.toJSON.return_value = {"dummy": True}
        model.getAllComponents.return_value = {}
        model.runPowerFlow.return_value = Mock()
        job = model.runPowerFlow.return_value
        job.id = "job-1"
        job.status.return_value = 1
        job.result.getBuses.return_value = make_table([{"Bus": "canvas_0_1", "Vm": 1.0}])
        mock_model_class.fetch.return_value = model
        mock_model_class.return_value = model

        token_file = tmp_path / ".cloudpss_token"
        token_file.write_text("dummy", encoding="utf-8")

        result = skill.run(
            {
                "skill": "voltage_stability",
                "auth": {"token_file": str(token_file)},
                "model": {"rid": "model/test", "source": "cloud"},
                "scan": {"load_scaling": [1.0], "scale_generation": False},
                "monitoring": {"buses": ["missing_bus"], "collapse_threshold": 0.7},
                "output": {"path": str(tmp_path), "prefix": "vs_unit", "generate_report": False, "export_pv_curve": False},
            }
        )

        assert result.status == SkillStatus.FAILED
        assert result.data["converged_cases"] == 0
