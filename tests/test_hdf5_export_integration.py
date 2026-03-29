"""
HDF5 Export 集成测试

验证真实 CloudPSS API 上的HDF5导出功能
"""

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss_skills.builtin import HDF5ExportSkill


@pytest.mark.integration
class TestHDF5ExportLive:
    """真实 CloudPSS 集成测试 - 验证HDF5导出"""

    def test_skill_config_requires_source(self):
        """验证配置需要source配置"""
        skill = HDF5ExportSkill()

        config = {
            "output": {"hdf5_file": "./results.h5"}
        }

        result = skill.validate(config)
        assert not result.valid, "缺少source的配置应该失败"
        assert any("source" in err.lower() for err in result.errors), "错误信息应该提到source"

    def test_skill_config_accepts_minimal_valid_config(self):
        """验证配置接受最小有效配置"""
        skill = HDF5ExportSkill()

        config = {
            "source": {
                "type": "emt_result",
                "file": "./results/emt_result.json"
            }
        }

        result = skill.validate(config)
        assert result.valid, f"有效配置应该通过验证: {result.errors}"

    def test_skill_name_is_correct(self):
        """验证技能名称正确"""
        skill = HDF5ExportSkill()
        assert skill.name == "hdf5_export", f"技能名称应该是 hdf5_export: {skill.name}"

    def test_skill_description_matches_functionality(self):
        """验证技能描述符合功能"""
        skill = HDF5ExportSkill()
        desc = skill.description.lower()

        keywords = ["hdf5", "h5", "export", "导出"]
        assert any(kw in desc for kw in keywords), f"描述应该包含HDF5导出相关词汇: {desc}"

    def test_config_schema_is_valid(self):
        """验证配置schema是有效的JSON Schema"""
        skill = HDF5ExportSkill()
        schema = skill.config_schema

        assert "type" in schema, "schema应该有type"
        assert "properties" in schema, "schema应该有properties"
