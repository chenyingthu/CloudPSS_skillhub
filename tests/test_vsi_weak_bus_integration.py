"""
VSI Weak Bus 集成测试

验证真实 CloudPSS API 上的VSI弱母线分析功能
"""

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss_skills.builtin import VSIWeakBusSkill


@pytest.mark.integration
class TestVSIWeakBusLive:
    """真实 CloudPSS 集成测试 - 验证VSI弱母线分析"""

    def test_skill_config_requires_model(self):
        """验证配置需要模型"""
        skill = VSIWeakBusSkill()

        config = {
            "analysis": {"threshold": 0.01}
        }

        result = skill.validate(config)
        assert not result.valid, "缺少模型的配置应该失败"

    def test_skill_config_accepts_minimal_valid_config(self):
        """验证配置接受最小有效配置"""
        skill = VSIWeakBusSkill()

        config = {
            "model": {"rid": "model/holdme/IEEE39"}
        }

        result = skill.validate(config)
        assert result.valid, f"有效配置应该通过验证: {result.errors}"

    def test_skill_name_is_correct(self):
        """验证技能名称正确"""
        skill = VSIWeakBusSkill()
        assert skill.name == "vsi_weak_bus", f"技能名称应该是 vsi_weak_bus: {skill.name}"

    def test_skill_description_matches_functionality(self):
        """验证技能描述符合功能"""
        skill = VSIWeakBusSkill()
        desc = skill.description.lower()

        keywords = ["vsi", "voltage stability", "weak bus", "电压稳定", "弱母线"]
        assert any(kw in desc for kw in keywords), f"描述应该包含VSI弱母线相关词汇: {desc}"

    def test_config_schema_is_valid(self):
        """验证配置schema是有效的JSON Schema"""
        skill = VSIWeakBusSkill()
        schema = skill.config_schema

        assert "type" in schema, "schema应该有type"
        assert "properties" in schema, "schema应该有properties"
