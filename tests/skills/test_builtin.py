"""
Tests for built-in skills

测试内置技能
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from cloudpss_skills.builtin import (
    EmtSimulationSkill,
    IEEE3PrepSkill,
    PowerFlowSkill,
    WaveformExportSkill,
    N1SecuritySkill,
    ParamScanSkill,
    ResultCompareSkill,
    VisualizeSkill,
    TopologyCheckSkill,
    BatchPowerFlowSkill,
)
from cloudpss_skills.core import SkillStatus


class TestEmtSimulationSkill(unittest.TestCase):
    """测试EMT仿真技能"""

    def setUp(self):
        self.skill = EmtSimulationSkill()

    def test_name(self):
        self.assertEqual(self.skill.name, "emt_simulation")

    def test_description(self):
        self.assertIn("EMT", self.skill.description)

    def test_default_config(self):
        defaults = self.skill.get_default_config()
        self.assertEqual(defaults["skill"], "emt_simulation")
        self.assertEqual(defaults["model"]["rid"], "model/holdme/IEEE3")
        self.assertEqual(defaults["output"]["format"], "csv")

    def test_validate_valid_config(self):
        config = {
            "skill": "emt_simulation",
            "model": {"rid": "model/test"},
            "auth": {"token_file": ".token"},
        }
        result = self.skill.validate(config)
        self.assertTrue(result.valid)

    def test_validate_missing_model_rid(self):
        config = {
            "skill": "emt_simulation",
            "model": {},
        }
        result = self.skill.validate(config)
        self.assertFalse(result.valid)
        self.assertTrue(any("rid" in e for e in result.errors))


class TestPowerFlowSkill(unittest.TestCase):
    """测试潮流计算技能"""

    def setUp(self):
        self.skill = PowerFlowSkill()

    def test_name(self):
        self.assertEqual(self.skill.name, "power_flow")

    def test_default_config(self):
        defaults = self.skill.get_default_config()
        self.assertEqual(defaults["skill"], "power_flow")
        self.assertEqual(defaults["algorithm"]["type"], "newton_raphson")


class TestIEEE3PrepSkill(unittest.TestCase):
    """测试IEEE3准备技能"""

    def setUp(self):
        self.skill = IEEE3PrepSkill()

    def test_name(self):
        self.assertEqual(self.skill.name, "ieee3_prep")

    def test_fault_config(self):
        defaults = self.skill.get_default_config()
        self.assertEqual(defaults["fault"]["start_time"], 2.5)
        self.assertEqual(defaults["fault"]["end_time"], 2.7)


class TestWaveformExportSkill(unittest.TestCase):
    """测试波形导出技能"""

    def setUp(self):
        self.skill = WaveformExportSkill()

    def test_name(self):
        self.assertEqual(self.skill.name, "waveform_export")

    def test_validate_requires_job_id(self):
        config = {"skill": "waveform_export", "source": {}}
        result = self.skill.validate(config)
        self.assertFalse(result.valid)
        self.assertTrue(any("job_id" in e for e in result.errors))


class TestSkillRegistry(unittest.TestCase):
    """测试技能已正确注册"""

    def test_all_skills_registered(self):
        from cloudpss_skills.core import list_skills, auto_discover

        auto_discover()
        skill_names = [s.name for s in list_skills()]
        expected = [
            "emt_simulation", "power_flow", "ieee3_prep", "waveform_export",
            "n1_security", "param_scan", "result_compare", "visualize",
            "topology_check", "batch_powerflow",
        ]

        for name in expected:
            self.assertIn(name, skill_names)


if __name__ == "__main__":
    unittest.main()
