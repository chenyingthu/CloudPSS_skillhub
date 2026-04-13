"""
Integration tests for CloudPSS Skill System

集成测试 - 测试完整工作流
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from cloudpss_skills.core import ConfigLoader, auto_discover, get_skill, has_skill
from cloudpss_skills.core.registry import clear_registry


class TestConfigLoading(unittest.TestCase):
    """测试配置加载"""

    def setUp(self):
        self.test_dir = Path(__file__).parent / "fixtures"
        self.test_dir.mkdir(exist_ok=True)

    def tearDown(self):
        # 清理测试文件
        for f in self.test_dir.glob("*.yaml"):
            f.unlink()

    def test_load_emt_simulation_template(self):
        """测试加载EMT仿真模板"""
        template_path = Path("skills/templates/emt_simulation.yaml")
        if template_path.exists():
            config = ConfigLoader._load_file(template_path)
            self.assertEqual(config["skill"], "emt_simulation")
            self.assertIn("model", config)
            self.assertIn("output", config)

    def test_env_var_substitution(self):
        """测试环境变量替换"""
        import os

        os.environ["TEST_MODEL"] = "model/test"

        test_file = self.test_dir / "env_test.yaml"
        test_file.write_text("model:\n  rid: ${TEST_MODEL}\n")

        config = ConfigLoader._load_file(test_file)
        self.assertEqual(config["model"]["rid"], "model/test")

        del os.environ["TEST_MODEL"]


class TestSkillExecution(unittest.TestCase):
    """测试技能执行"""

    def setUp(self):
        auto_discover()

    def test_emt_simulation_skill_exists(self):
        """测试EMT仿真技能存在"""
        self.assertTrue(has_skill("emt_simulation"))

    def test_power_flow_skill_exists(self):
        """测试潮流计算技能存在"""
        self.assertTrue(has_skill("power_flow"))

    def test_waveform_export_skill_exists(self):
        """测试波形导出技能存在"""
        self.assertTrue(has_skill("waveform_export"))


class TestSkillDescribe(unittest.TestCase):
    """测试技能描述"""

    def setUp(self):
        auto_discover()

    def test_emt_simulation_describe(self):
        """测试EMT技能描述"""
        skill = get_skill("emt_simulation")
        desc = skill.describe()

        self.assertEqual(desc["name"], "emt_simulation")
        self.assertIn("schema", desc)
        self.assertIn("defaults", desc)
        self.assertIn("EMT", desc["description"])


class TestConfigurationWorkflow(unittest.TestCase):
    """测试配置工作流"""

    def test_validate_emt_config(self):
        """测试验证EMT配置"""
        from skills.core import ConfigValidator

        auto_discover()
        skill = get_skill("emt_simulation")

        # 有效配置
        valid_config = {
            "skill": "emt_simulation",
            "model": {"rid": "model/test"},
            "auth": {"token_file": ".token"},
        }
        result = skill.validate(valid_config)
        self.assertTrue(result.valid)

        # 无效配置
        invalid_config = {
            "skill": "emt_simulation",
            "model": {},  # 缺少rid
        }
        result = skill.validate(invalid_config)
        self.assertFalse(result.valid)


if __name__ == "__main__":
    unittest.main()
