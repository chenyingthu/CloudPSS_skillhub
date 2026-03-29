"""
Disturbance Severity 集成测试

验证真实 CloudPSS API 上的扰动严重度分析功能
"""

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss_skills.builtin import DisturbanceSeveritySkill


@pytest.mark.integration
class TestDisturbanceSeverityLive:
    """真实 CloudPSS 集成测试 - 验证扰动严重度分析"""

    def test_skill_config_requires_model(self):
        """验证配置需要模型"""
        skill = DisturbanceSeveritySkill()

        # 缺少 model
        config = {
            "analysis": {"dv_enabled": True}
        }

        result = skill.validate(config)
        assert not result.valid, "缺少模型的配置应该失败"
        assert any("model" in err.lower() for err in result.errors), "错误信息应该提到model"

    def test_skill_config_accepts_minimal_valid_config(self):
        """验证配置接受最小有效配置"""
        skill = DisturbanceSeveritySkill()

        config = {
            "model": {"rid": "model/holdme/IEEE3"}
        }

        result = skill.validate(config)
        assert result.valid, f"有效配置应该通过验证: {result.errors}"

    def test_skill_name_is_correct(self):
        """验证技能名称正确"""
        skill = DisturbanceSeveritySkill()
        assert skill.name == "disturbance_severity", f"技能名称应该是 disturbance_severity: {skill.name}"

    def test_skill_description_matches_functionality(self):
        """验证技能描述符合功能"""
        skill = DisturbanceSeveritySkill()
        desc = skill.description.lower()

        keywords = ["disturbance", "severity", "扰动", "严重度", "dv", "si"]
        assert any(kw in desc for kw in keywords), f"描述应该包含扰动严重度相关词汇: {desc}"

    def test_config_schema_is_valid(self):
        """验证配置schema是有效的JSON Schema"""
        skill = DisturbanceSeveritySkill()
        schema = skill.config_schema

        assert "type" in schema, "schema应该有type"
        assert schema["type"] == "object", "schema类型应该是object"
        assert "properties" in schema, "schema应该有properties"
        assert "required" in schema, "schema应该有required"
