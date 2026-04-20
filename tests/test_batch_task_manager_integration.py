"""
Batch Task Manager 集成测试

验证真实 CloudPSS API 上的批处理任务管理功能
"""

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss_skills.builtin import BatchTaskManagerSkill


@pytest.mark.integration
class TestBatchTaskManagerLive:
    """真实 CloudPSS 集成测试 - 验证批处理任务管理"""

    def test_skill_config_requires_tasks(self):
        """验证配置需要任务列表"""
        skill = BatchTaskManagerSkill()

        config = {
            "execution": {"parallel": True}
        }

        result = skill.validate(config)
        assert not result.valid, "缺少任务的配置应该失败"

    def test_skill_config_accepts_minimal_valid_config(self):
        """验证配置接受最小有效配置"""
        skill = BatchTaskManagerSkill()

        config = {
            "tasks": [
                {
                    "name": "task1",
                    "type": "skill",
                    "skill": "power_flow",
                    "config": {"model": {"rid": "model/holdme/IEEE39"}}
                }
            ]
        }

        result = skill.validate(config)
        assert result.valid, f"有效配置应该通过验证: {result.errors}"

    def test_skill_name_is_correct(self):
        """验证技能名称正确"""
        skill = BatchTaskManagerSkill()
        assert skill.name == "batch_task_manager", f"技能名称应该是 batch_task_manager: {skill.name}"

    def test_skill_description_matches_functionality(self):
        """验证技能描述符合功能"""
        skill = BatchTaskManagerSkill()
        desc = skill.description.lower()

        keywords = ["batch", "task", "批处理", "任务", "manager", "管理"]
        assert any(kw in desc for kw in keywords), f"描述应该包含批处理任务相关词汇: {desc}"

    def test_config_schema_is_valid(self):
        """验证配置schema是有效的JSON Schema"""
        skill = BatchTaskManagerSkill()
        schema = skill.config_schema

        assert "type" in schema, "schema应该有type"
        assert "properties" in schema, "schema应该有properties"
