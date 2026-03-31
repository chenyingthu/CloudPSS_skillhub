#!/usr/bin/env python3
"""
智能报告生成器技能 - 集成测试

运行: pytest tests/test_report_generator_integration.py -v
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cloudpss_skills.builtin.report_generator import ReportGeneratorSkill, ReportSection
from cloudpss_skills.core.base import SkillStatus


class TestReportGeneratorSkill:
    """报告生成器技能集成测试"""

    @pytest.fixture
    def skill(self):
        return ReportGeneratorSkill()

    @pytest.fixture
    def valid_config(self):
        return {
            "report": {
                "title": "电力系统综合分析报告",
                "skills": ["power_flow", "n1_security"],
                "skill_results": {
                    "power_flow": {
                        "status": "success",
                        "summary": "潮流计算收敛",
                        "data": {"total_loss": 10.5}
                    },
                    "n1_security": {
                        "status": "success",
                        "summary": "N-1安全",
                        "data": {"pass_rate": 0.95}
                    }
                },
                "template": {
                    "type": "comprehensive",
                    "sections": ["executive_summary", "system_overview"]
                }
            },
            "output": {
                "format": "markdown",
                "path": "/tmp/test_reports/",
                "filename": "test_report.md"
            }
        }

    def test_skill_registration(self, skill):
        """测试1: 技能注册"""
        assert skill.name == "report_generator"
        assert "报告生成" in skill.description
        print(f"✅ 技能注册: {skill.name}")

    def test_config_schema(self, skill):
        """测试2: 配置Schema"""
        assert skill.config_schema is not None
        print("✅ 配置Schema验证通过")

    def test_validation_valid_config(self, skill, valid_config):
        """测试3: 有效配置验证"""
        result = skill.validate(valid_config)
        assert result.valid is True
        print("✅ 有效配置验证通过")

    def test_validation_missing_skills(self, skill):
        """测试4: 缺少skills的验证"""
        invalid_config = {"report": {}}
        result = skill.validate(invalid_config)
        assert result.valid is False
        print("✅ 缺失检测正确")

    def test_integration_report_generation(self, skill, valid_config):
        """测试5: 报告生成集成测试"""
        print("\n🔄 开始报告生成测试...")

        result = skill.run(valid_config)

        print(f"   状态: {result.status.value}")
        assert result.status == SkillStatus.SUCCESS, f"失败: {result.error}"

        # 验证结果数据
        assert result.data is not None
        assert "report_title" in result.data
        assert "sections_count" in result.data
        assert "output_file" in result.data

        print(f"   报告标题: {result.data['report_title']}")
        print(f"   章节数: {result.data['sections_count']}")
        print(f"   输出文件: {result.data['output_file']}")

        # 验证文件生成
        output_file = result.data['output_file']
        if output_file and os.path.exists(output_file):
            print(f"   文件大小: {os.path.getsize(output_file)} bytes")
            assert result.artifacts
            assert len(result.artifacts) > 0

        print("✅ 报告生成测试通过!")

    def test_integration_report_content(self, skill, valid_config):
        """测试6: 报告内容验证"""
        result = skill.run(valid_config)
        assert result.status == SkillStatus.SUCCESS

        # 验证章节
        sections = result.data.get("sections", [])
        assert len(sections) > 0

        for section in sections:
            assert "title" in section
            assert "level" in section

        print(f"✅ 报告内容验证通过 ({len(sections)}个章节)")

    def test_report_section_dataclass(self):
        """测试7: ReportSection数据类"""
        section = ReportSection(
            title="测试章节",
            content="测试内容",
            level=1
        )
        assert section.title == "测试章节"
        assert section.level == 1
        print("✅ ReportSection数据类测试通过")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
