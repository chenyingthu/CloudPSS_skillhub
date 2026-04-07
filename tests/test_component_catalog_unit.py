#!/usr/bin/env python3
"""
组件目录技能 - 单元测试
"""

from unittest.mock import patch

from cloudpss_skills.builtin.component_catalog import ComponentCatalogSkill
from cloudpss_skills.core.base import SkillStatus


class TestComponentCatalogUnit:
    @patch("cloudpss.setToken")
    @patch("cloudpss.Model")
    def test_run_wraps_generic_fetchmany_exception(self, mock_model_class, mock_set_token, tmp_path):
        skill = ComponentCatalogSkill()
        mock_model_class.fetchMany.side_effect = Exception("catalog fetch failed")

        token_file = tmp_path / ".cloudpss_token"
        token_file.write_text("dummy", encoding="utf-8")

        result = skill.run(
            {
                "auth": {"token_file": str(token_file)},
                "output": {"format": "console"},
            }
        )

        assert result.status == SkillStatus.FAILED
        assert "catalog fetch failed" in (result.error or "")
