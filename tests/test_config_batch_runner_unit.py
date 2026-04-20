#!/usr/bin/env python3
"""
多配置批量运行器 - 单元测试
"""

from cloudpss_skills.builtin.config_batch_runner import ConfigBatchRunnerSkill
from cloudpss_skills.core.base import SkillStatus
from unittest.mock import patch


class TestConfigBatchRunnerUnit:
    @patch("cloudpss.setToken")
    @patch("cloudpss.Model")
    def test_fetch_exception_is_wrapped_as_failed_skill_result(self, mock_model_class, mock_set_token):
        skill = ConfigBatchRunnerSkill()
        mock_model_class.fetch.side_effect = Exception("invalid resource id")

        config = {
            "skill": "config_batch_runner",
            "auth": {"token": "dummy"},
            "model": {"rid": "model/not_exists", "source": "cloud"},
            "configs": {"mode": "all"},
            "output": {"path": "/tmp", "prefix": "config_batch_unit"},
        }

        result = skill.run(config)

        assert result.status == SkillStatus.FAILED
        assert "invalid resource id" in (result.error or "")
