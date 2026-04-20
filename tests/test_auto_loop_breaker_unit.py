#!/usr/bin/env python3
"""
自动解环技能 - 单元测试
"""

from unittest.mock import patch

from cloudpss_skills.builtin.auto_loop_breaker import AutoLoopBreakerSkill
from cloudpss_skills.core.base import SkillStatus


class TestAutoLoopBreakerUnit:
    @patch("cloudpss.setToken")
    @patch("cloudpss.Model")
    def test_run_wraps_generic_model_fetch_exception(self, mock_model_class, mock_set_token, tmp_path):
        skill = AutoLoopBreakerSkill()
        mock_model_class.fetch.side_effect = Exception("invalid resource id")

        token_file = tmp_path / ".cloudpss_token"
        token_file.write_text("dummy", encoding="utf-8")

        result = skill.run(
            {
                "skill": "auto_loop_breaker",
                "auth": {"token_file": str(token_file)},
                "model": {"rid": "model/not_exists", "source": "cloud"},
                "output": {"dry_run": True, "save_model": False},
            }
        )

        assert result.status == SkillStatus.FAILED
        assert "invalid resource id" in (result.error or "")
