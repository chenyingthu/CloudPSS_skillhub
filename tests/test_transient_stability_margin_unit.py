#!/usr/bin/env python3
"""
暂态稳定裕度技能 - 单元测试
"""

from unittest.mock import patch

from cloudpss_skills.builtin.transient_stability_margin import TransientStabilityMarginSkill
from cloudpss_skills.core.base import SkillStatus


class TestTransientStabilityMarginUnit:
    @patch("cloudpss.setToken")
    @patch("cloudpss.Model")
    def test_run_wraps_generic_model_fetch_exception(self, mock_model_class, mock_set_token):
        skill = TransientStabilityMarginSkill()
        mock_model_class.fetch.side_effect = Exception("invalid resource id")

        result = skill.run(
            {
                "skill": "transient_stability_margin",
                "auth": {"token": "dummy"},
                "model": {"rid": "model/not_exists", "source": "cloud"},
                "fault_scenarios": [{"location": "BUS_1"}],
            }
        )

        assert result.status == SkillStatus.FAILED
        assert "invalid resource id" in (result.error or "")
