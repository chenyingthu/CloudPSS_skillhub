"""
Test suite for CloudPSS Skill System

单元测试 - 测试核心功能
"""

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# 确保可以导入技能模块
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from cloudpss_skills.core import (
    Artifact,
    ConfigGenerator,
    ConfigLoader,
    ConfigValidator,
    LogEntry,
    SkillBase,
    SkillResult,
    SkillStatus,
    ValidationResult,
    get_skill,
    has_skill,
    list_skills,
    register,
)
from cloudpss_skills.core.registry import clear_registry, unregister


class TestValidationResult(unittest.TestCase):
    """测试ValidationResult"""

    def test_valid_result(self):
        result = ValidationResult(valid=True)
        self.assertTrue(result.valid)
        self.assertEqual(len(result.errors), 0)

    def test_add_error(self):
        result = ValidationResult(valid=True)
        result.add_error("test error")
        self.assertFalse(result.valid)
        self.assertEqual(result.errors, ["test error"])

    def test_add_warning(self):
        result = ValidationResult(valid=True)
        result.add_warning("test warning")
        self.assertTrue(result.valid)  # 警告不改变valid状态
        self.assertEqual(result.warnings, ["test warning"])


class TestSkillResult(unittest.TestCase):
    """测试SkillResult"""

    def test_success_property(self):
        from datetime import datetime

        result = SkillResult(
            skill_name="test",
            status=SkillStatus.SUCCESS,
            start_time=datetime.now(),
        )
        self.assertTrue(result.success)

        result.status = SkillStatus.FAILED
        self.assertFalse(result.success)

    def test_duration(self):
        from datetime import datetime, timedelta

        start = datetime.now()
        end = start + timedelta(seconds=10)

        result = SkillResult(
            skill_name="test",
            status=SkillStatus.SUCCESS,
            start_time=start,
            end_time=end,
        )
        self.assertEqual(result.duration, 10.0)

    def test_to_dict(self):
        from datetime import datetime

        result = SkillResult(
            skill_name="test",
            status=SkillStatus.SUCCESS,
            start_time=datetime(2024, 1, 1, 12, 0, 0),
            end_time=datetime(2024, 1, 1, 12, 0, 10),
            data={"key": "value"},
            artifacts=[Artifact(type="csv", path="/tmp/test.csv", size=100)],
            metrics={"count": 1},
        )

        d = result.to_dict()
        self.assertEqual(d["skill_name"], "test")
        self.assertEqual(d["status"], "success")
        self.assertEqual(d["duration"], 10.0)
        self.assertEqual(d["data"]["key"], "value")


class TestConfigLoader(unittest.TestCase):
    """测试ConfigLoader"""

    def setUp(self):
        self.test_dir = Path(__file__).parent / "fixtures"
        self.test_dir.mkdir(exist_ok=True)

    def tearDown(self):
        # 清理测试文件
        for f in self.test_dir.glob("*.yaml"):
            f.unlink()

    def test_expand_env_vars(self):
        os.environ["TEST_VAR"] = "test_value"

        # 测试字符串替换
        result = ConfigLoader._expand_env_vars("${TEST_VAR}")
        self.assertEqual(result, "test_value")

        # 测试默认值
        result = ConfigLoader._expand_env_vars("${MISSING:-default}")
        self.assertEqual(result, "default")

        # 测试字典
        result = ConfigLoader._expand_env_vars({"key": "${TEST_VAR}"})
        self.assertEqual(result["key"], "test_value")

        # 测试列表
        result = ConfigLoader._expand_env_vars(["${TEST_VAR}"])
        self.assertEqual(result[0], "test_value")

    def test_load_file(self):
        test_file = self.test_dir / "test_config.yaml"
        test_file.write_text("""
skill: test_skill
model:
  rid: model/test
  source: cloud
""")

        config = ConfigLoader._load_file(test_file)
        self.assertEqual(config["skill"], "test_skill")
        self.assertEqual(config["model"]["rid"], "model/test")


class TestConfigValidator(unittest.TestCase):
    """测试ConfigValidator"""

    def test_simple_validation(self):
        schema = {
            "type": "object",
            "required": ["name"],
            "properties": {
                "name": {"type": "string"},
            },
        }

        # 有效配置
        result = ConfigValidator.validate({"name": "test"}, schema)
        self.assertTrue(result.valid)

        # 缺少必填字段
        result = ConfigValidator.validate({}, schema)
        self.assertFalse(result.valid)

    def test_deep_merge(self):
        base = {"a": 1, "b": {"c": 2, "d": 3}}
        override = {"b": {"d": 4}}

        result = ConfigValidator._deep_merge(base, override)
        self.assertEqual(result["a"], 1)
        self.assertEqual(result["b"]["c"], 2)
        self.assertEqual(result["b"]["d"], 4)


class TestSkillBase(unittest.TestCase):
    """测试SkillBase"""

    def test_abstract_methods(self):
        """测试抽象方法必须实现"""

        class TestSkill(SkillBase):
            @property
            def name(self):
                return "test"

            @property
            def description(self):
                return "test skill"

            def run(self, config):
                return None

        skill = TestSkill()
        self.assertEqual(skill.name, "test")
        self.assertEqual(skill.description, "test skill")
        self.assertEqual(skill.version, "1.0.0")  # 默认值

    def test_validate(self):
        """测试基础验证逻辑"""

        class TestSkill(SkillBase):
            @property
            def name(self):
                return "test"

            @property
            def description(self):
                return "test skill"

            def run(self, config):
                return None

        skill = TestSkill()

        # 缺少skill字段
        result = skill.validate({})
        self.assertFalse(result.valid)

        # skill不匹配
        result = skill.validate({"skill": "other"})
        self.assertFalse(result.valid)

        # 正确
        result = skill.validate({"skill": "test", "model": {"rid": "model/test"}})
        self.assertTrue(result.valid)

    def test_describe(self):
        """测试describe方法"""

        class TestSkill(SkillBase):
            @property
            def name(self):
                return "test"

            @property
            def description(self):
                return "test skill"

            def run(self, config):
                return None

        skill = TestSkill()
        desc = skill.describe()

        self.assertEqual(desc["name"], "test")
        self.assertEqual(desc["description"], "test skill")
        self.assertIn("schema", desc)
        self.assertIn("defaults", desc)


class TestSkillRegistry(unittest.TestCase):
    """测试技能注册表"""

    def setUp(self):
        """每个测试前清理"""
        clear_registry()

    def tearDown(self):
        """清理注册表"""
        clear_registry()

    def test_register_and_get(self):
        """测试注册和获取技能"""

        @register
        class TestSkill(SkillBase):
            @property
            def name(self):
                return "test_skill"

            @property
            def description(self):
                return "test"

            def run(self, config):
                return None

        self.assertTrue(has_skill("test_skill"))

        skill = get_skill("test_skill")
        self.assertIsNotNone(skill)
        self.assertEqual(skill.name, "test_skill")

    def test_list_skills(self):
        """测试列出技能"""

        @register
        class Skill1(SkillBase):
            @property
            def name(self):
                return "skill1"

            @property
            def description(self):
                return "skill 1"

            def run(self, config):
                return None

        @register
        class Skill2(SkillBase):
            @property
            def name(self):
                return "skill2"

            @property
            def description(self):
                return "skill 2"

            def run(self, config):
                return None

        skills = list_skills()
        skill_names = [s.name for s in skills]
        self.assertIn("skill1", skill_names)
        self.assertIn("skill2", skill_names)

    def test_unregister(self):
        """测试注销技能"""

        @register
        class TempSkill(SkillBase):
            @property
            def name(self):
                return "temp"

            @property
            def description(self):
                return "temp"

            def run(self, config):
                return None

        self.assertTrue(has_skill("temp"))
        unregister("temp")
        self.assertFalse(has_skill("temp"))


if __name__ == "__main__":
    unittest.main()
