#!/usr/bin/env python3
"""
自动量测配置技能 - 单元测试
"""

from unittest.mock import Mock, patch

from cloudpss_skills.builtin.auto_channel_setup import AutoChannelSetupSkill
from cloudpss_skills.core.base import SkillStatus


class TestAutoChannelSetupUnit:
    @patch("cloudpss.setToken")
    @patch("cloudpss.Model")
    def test_frequency_measurement_failure_is_wrapped_as_failed_skill_result(self, mock_model_class, mock_set_token, tmp_path):
        skill = AutoChannelSetupSkill()

        model = Mock()
        model.name = "TestModel"
        model.getComponentsByRid.side_effect = RuntimeError("frequency setup failed")
        mock_model_class.fetch.return_value = model

        token_file = tmp_path / ".cloudpss_token"
        token_file.write_text("dummy", encoding="utf-8")

        result = skill.run(
            {
                "skill": "auto_channel_setup",
                "auth": {"token_file": str(token_file)},
                "model": {"rid": "model/test", "source": "cloud"},
                "measurements": {
                    "voltage": {"enabled": False},
                    "current": {"enabled": False},
                    "power": {"enabled": False},
                    "frequency": {"enabled": True},
                },
                "output": {"dry_run": False},
            }
        )

        assert result.status == SkillStatus.FAILED
        assert "frequency setup failed" in (result.error or "")
