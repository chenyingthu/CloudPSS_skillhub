#!/usr/bin/env python3
"""
参数灵敏度技能 - 单元测试
"""

from unittest.mock import Mock, patch

from cloudpss_skills.builtin.parameter_sensitivity import ParameterSensitivitySkill
from cloudpss_skills.core.base import SkillStatus


class TestParameterSensitivityUnit:
    def test_component_match_does_not_confuse_gen1_with_gen10(self):
        skill = ParameterSensitivitySkill()
        comp1 = Mock()
        comp1.label = "Gen1"
        comp1.name = ""
        comp1.args = {"Name": "Gen1"}
        comp10 = Mock()
        comp10.label = "Gen10"
        comp10.name = ""
        comp10.args = {"Name": "Gen10"}

        assert skill._component_matches(comp1, "canvas_gen1", "Gen1") is True
        assert skill._component_matches(comp10, "canvas_gen10", "Gen1") is False

    @patch("cloudpss.setToken")
    @patch("cloudpss.Model")
    def test_run_fails_when_all_scan_points_fail_to_apply(self, mock_model_class, mock_set_token, tmp_path):
        skill = ParameterSensitivitySkill()

        model = Mock()
        model.name = "TestModel"
        model.toJSON.return_value = {"dummy": True}
        model.getAllComponents.return_value = {}
        model.runPowerFlow.return_value = Mock()
        job = model.runPowerFlow.return_value
        job.status.return_value = 1
        job.result.getBuses.return_value = [{"type": "table", "data": {"columns": []}}]
        job.result.getBranches.return_value = [{"type": "table", "data": {"columns": []}}]
        mock_model_class.fetch.return_value = model
        mock_model_class.return_value = model

        token_file = tmp_path / ".cloudpss_token"
        token_file.write_text("dummy", encoding="utf-8")

        result = skill.run(
            {
                "skill": "parameter_sensitivity",
                "auth": {"token_file": str(token_file)},
                "model": {"rid": "model/test", "source": "cloud"},
                "scan": {"target": "NoSuchGen.pf_P", "values": [1.0, 2.0], "simulation_type": "power_flow"},
                "metrics": {"voltage_buses": ["Bus7"]},
                "output": {"path": str(tmp_path), "generate_report": False},
            }
        )

        assert result.status == SkillStatus.FAILED
        assert "所有扫描点都失败" in (result.error or "")
