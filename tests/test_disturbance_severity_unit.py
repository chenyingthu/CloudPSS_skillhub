#!/usr/bin/env python3
"""
扰动严重度分析技能 - 单元测试
"""

from unittest.mock import Mock, patch

from cloudpss_skills.builtin.disturbance_severity import DisturbanceSeveritySkill
from cloudpss_skills.core.base import SkillStatus


class FakeResult:
    def getPlots(self):
        return [{"data": {"traces": [{"name": "V1", "x": [0.0, 1.0], "y": [1.0, 0.8]}]}}]


class TestDisturbanceSeverityUnit:
    @patch("cloudpss.setToken")
    @patch("cloudpss_skills.builtin.disturbance_severity.Model")
    @patch("cloudpss_skills.builtin.disturbance_severity.fetch_job_with_result")
    def test_run_uses_existing_emt_result_job(self, mock_fetch_job, mock_model_class, mock_set_token, tmp_path):
        skill = DisturbanceSeveritySkill()

        model = Mock()
        mock_model_class.fetch.return_value = model

        job = Mock()
        job.status.return_value = 1
        mock_fetch_job.return_value = (job, FakeResult())

        token_file = tmp_path / ".cloudpss_token"
        token_file.write_text("dummy", encoding="utf-8")

        result = skill.run(
            {
                "auth": {"token_file": str(token_file)},
                "model": {"rid": "model/test"},
                "simulation": {"emt_result": "job-1", "fault_time": 0.1},
                "analysis": {"voltage_measure_plot": 0},
                "output": {"path": str(tmp_path), "prefix": "disturbance_unit"},
            }
        )

        assert result.status == SkillStatus.SUCCESS
        assert result.data["channel_count"] == 1

    @patch("cloudpss.setToken")
    @patch("cloudpss_skills.builtin.disturbance_severity.Model")
    def test_run_fails_without_existing_emt_result_job(self, mock_model_class, mock_set_token, tmp_path):
        skill = DisturbanceSeveritySkill()

        model = Mock()
        mock_model_class.fetch.return_value = model

        token_file = tmp_path / ".cloudpss_token"
        token_file.write_text("dummy", encoding="utf-8")

        result = skill.run(
            {
                "auth": {"token_file": str(token_file)},
                "model": {"rid": "model/test"},
                "simulation": {},
                "output": {"path": str(tmp_path), "prefix": "disturbance_unit"},
            }
        )

        assert result.status == SkillStatus.FAILED
        assert any("仅支持基于已有 EMT 任务结果" in entry.message for entry in result.logs)
