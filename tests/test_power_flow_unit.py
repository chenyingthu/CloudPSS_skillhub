#!/usr/bin/env python3
"""
潮流技能 - 单元测试
"""

from unittest.mock import Mock, patch

from cloudpss_skills.builtin.power_flow import PowerFlowSkill
from cloudpss_skills.core.base import SkillStatus


class TestPowerFlowUnit:
    @patch("cloudpss.setToken")
    @patch("cloudpss.Model")
    def test_run_fails_when_result_tables_have_no_rows(self, mock_model_class, mock_set_token, tmp_path):
        skill = PowerFlowSkill()

        model = Mock()
        model.name = "TestModel"
        model.rid = "model/test"

        job = Mock()
        job.id = "job-1"
        job.status.return_value = 1
        job.result.getBuses.return_value = [{"type": "table", "data": {"columns": [{"name": "Vm", "data": []}]}}]
        job.result.getBranches.return_value = [{"type": "table", "data": {"columns": [{"name": "Branch", "data": []}]}}]
        model.runPowerFlow.return_value = job
        mock_model_class.fetch.return_value = model

        token_file = tmp_path / ".cloudpss_token"
        token_file.write_text("dummy", encoding="utf-8")

        result = skill.run(
            {
                "skill": "power_flow",
                "auth": {"token_file": str(token_file)},
                "model": {"rid": "model/test", "source": "cloud"},
                "output": {"path": str(tmp_path), "timestamp": False, "prefix": "pf_unit"},
            }
        )

        assert result.status == SkillStatus.FAILED
        assert "结果表为空" in (result.error or "")
