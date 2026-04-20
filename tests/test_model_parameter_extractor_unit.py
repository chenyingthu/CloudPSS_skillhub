#!/usr/bin/env python3
"""
模型参数提取器 - 单元测试
"""

from unittest.mock import patch

from cloudpss_skills.builtin.model_parameter_extractor import ModelParameterExtractorSkill
from cloudpss_skills.core.base import SkillStatus


class TestModelParameterExtractorUnit:
    @patch("cloudpss.setToken")
    @patch("cloudpss.Model")
    def test_run_wraps_generic_fetch_exception(self, mock_model_class, mock_set_token, tmp_path):
        skill = ModelParameterExtractorSkill()
        mock_model_class.fetch.side_effect = Exception("invalid resource id")

        token_file = tmp_path / ".cloudpss_token"
        token_file.write_text("dummy", encoding="utf-8")

        result = skill.run(
            {
                "skill": "model_parameter_extractor",
                "auth": {"token_file": str(token_file)},
                "model": {"rid": "model/not_exists", "source": "cloud"},
                "extraction": {"component_types": ["bus_3p"]},
                "output": {"path": str(tmp_path), "format": "json"},
            }
        )

        assert result.status == SkillStatus.FAILED
        assert "invalid resource id" in (result.error or "")
