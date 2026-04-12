#!/usr/bin/env python3
"""
Study Pipeline Skill - Unit Tests
"""

from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from cloudpss_skills.builtin.study_pipeline import StudyPipelineSkill
from cloudpss_skills.core.base import SkillStatus


class TestStudyPipelineUnit:
    """Study Pipeline 单元测试"""

    def test_config_schema_validates_required_fields(self):
        """测试配置验证：必填字段"""
        skill = StudyPipelineSkill()

        result = skill.validate({"skill": "study_pipeline"})
        assert not result.valid
        assert any("pipeline不能为空" in e for e in result.errors)

    def test_config_schema_validates_empty_pipeline(self):
        """测试配置验证：空pipeline"""
        skill = StudyPipelineSkill()

        result = skill.validate(
            {
                "skill": "study_pipeline",
                "pipeline": [],
            }
        )
        assert not result.valid

    def test_config_schema_requires_skill_in_steps(self):
        """测试配置验证：步骤需要skill字段"""
        skill = StudyPipelineSkill()

        result = skill.validate(
            {
                "skill": "study_pipeline",
                "pipeline": [{"name": "step1"}],
            }
        )
        assert not result.valid

    def test_resolve_config_replaces_placeholders(self):
        """测试配置解析：替换占位符"""
        skill = StudyPipelineSkill()

        context = {
            "steps": {
                "step1": {
                    "result": Mock(),
                    "status": SkillStatus.SUCCESS,
                    "data": {"critical_buses": ["Bus1", "Bus2"]},
                    "artifacts": [],
                }
            }
        }

        config = {"monitoring": {"buses": "${steps.step1.data.critical_buses}"}}

        resolved = skill._resolve_config(config, context)

        assert resolved["monitoring"]["buses"] == ["Bus1", "Bus2"]

    def test_resolve_config_handles_nested_placeholders(self):
        """测试配置解析：嵌套占位符"""
        skill = StudyPipelineSkill()

        context = {
            "steps": {
                "pf": {
                    "result": Mock(),
                    "status": SkillStatus.SUCCESS,
                    "data": {"job_id": "job-123"},
                    "artifacts": [],
                }
            }
        }

        config = {
            "model": {
                "rid": "model/test",
                "metadata": {"pf_job": "${steps.pf.data.job_id}"},
            }
        }

        resolved = skill._resolve_config(config, context)

        assert resolved["model"]["rid"] == "model/test"
        assert "${" not in str(resolved["model"]["metadata"]["pf_job"])

    def test_resolve_config_preserves_non_string_values(self):
        """测试配置解析：保留非字符串值"""
        skill = StudyPipelineSkill()
        context = {"steps": {}}

        config = {
            "number": 42,
            "boolean": True,
            "list": [1, 2, 3],
        }

        resolved = skill._resolve_config(config, context)

        assert resolved["number"] == 42
        assert resolved["boolean"] is True
        assert resolved["list"] == [1, 2, 3]

    @patch("cloudpss_skills.builtin.study_pipeline.get_skill")
    def test_run_executes_all_steps(self, mock_get_skill):
        """测试运行：执行所有步骤"""
        skill = StudyPipelineSkill()

        mock_step1 = Mock()
        mock_step1.run.return_value = Mock(
            status=SkillStatus.SUCCESS,
            data={"result": "ok"},
            artifacts=[],
            error=None,
            start_time=datetime.now(),
            end_time=datetime.now(),
        )

        mock_step2 = Mock()
        mock_step2.run.return_value = Mock(
            status=SkillStatus.SUCCESS,
            data={"result": "ok"},
            artifacts=[],
            error=None,
            start_time=datetime.now(),
            end_time=datetime.now(),
        )

        def get_skill_side_effect(name):
            if name == "skill1":
                return mock_step1
            elif name == "skill2":
                return mock_step2
            return None

        mock_get_skill.side_effect = get_skill_side_effect

        config = {
            "skill": "study_pipeline",
            "auth": {"token": "dummy"},
            "pipeline": [
                {"name": "step1", "skill": "skill1", "config": {}},
                {"name": "step2", "skill": "skill2", "config": {}},
            ],
        }

        result = skill.run(config)

        assert result.data["total_steps"] == 2

    @patch("cloudpss_skills.builtin.study_pipeline.get_skill")
    def test_run_handles_step_failure(self, mock_get_skill):
        """测试运行：处理步骤失败"""
        skill = StudyPipelineSkill()

        mock_step1 = Mock()
        mock_step1.run.return_value = Mock(
            status=SkillStatus.FAILED,
            data={},
            artifacts=[],
            error="Power flow failed",
            start_time=datetime.now(),
            end_time=datetime.now(),
        )

        mock_get_skill.return_value = mock_step1

        config = {
            "skill": "study_pipeline",
            "auth": {"token": "dummy"},
            "pipeline": [
                {"name": "step1", "skill": "skill1", "config": {}},
                {"name": "step2", "skill": "skill2", "config": {}},
            ],
            "continue_on_failure": False,
        }

        result = skill.run(config)

        assert result.status == SkillStatus.FAILED
        assert result.data["failed_count"] >= 1

    def test_run_validates_config(self):
        """测试运行：验证配置"""
        skill = StudyPipelineSkill()

        result = skill.validate(
            {
                "skill": "study_pipeline",
                "pipeline": [],
            }
        )

        assert not result.valid
        assert any("pipeline不能为空" in e for e in result.errors)

    def test_run_validates_skill_required(self):
        """测试运行：步骤需要skill字段"""
        skill = StudyPipelineSkill()

        result = skill.validate(
            {
                "skill": "study_pipeline",
                "pipeline": [{"name": "step1"}],
            }
        )

        assert not result.valid

    @patch("cloudpss_skills.builtin.study_pipeline.get_skill")
    @patch("cloudpss_skills.builtin.study_pipeline.save_json")
    @patch("cloudpss_skills.builtin.study_pipeline.generate_report")
    def test_run_generates_artifacts(
        self, mock_report, mock_save, mock_get_skill, tmp_path
    ):
        """测试运行：生成产物"""
        skill = StudyPipelineSkill()

        mock_step = Mock()
        mock_step.run.return_value = Mock(
            status=SkillStatus.SUCCESS,
            data={"result": "ok"},
            artifacts=[
                Mock(
                    type="json", path="/tmp/result.json", size=100, description="Test"
                ),
            ],
            error=None,
            start_time=datetime.now(),
            end_time=datetime.now(),
        )

        mock_get_skill.return_value = mock_step

        mock_save.return_value = Mock(
            success=True,
            artifact=Mock(
                type="json", path="/tmp/pipeline.json", size=50, description="Pipeline"
            ),
        )
        mock_report.return_value = Mock(
            success=True,
            artifact=Mock(
                type="markdown", path="/tmp/report.md", size=200, description="Report"
            ),
        )

        config = {
            "skill": "study_pipeline",
            "auth": {"token": "dummy"},
            "pipeline": [
                {"name": "step1", "skill": "skill1", "config": {}},
            ],
            "output": {
                "path": str(tmp_path),
                "generate_report": True,
            },
        }

        result = skill.run(config)

        assert result.data["total_steps"] == 1

    def test_generate_report_format(self):
        """测试报告生成：格式"""
        skill = StudyPipelineSkill()

        pipeline_result = {
            "timestamp": "2026-04-12T14:00:00",
            "total_steps": 2,
            "success_count": 2,
            "failed_count": 0,
            "steps": [
                {
                    "name": "step1",
                    "skill": "power_flow",
                    "status": "success",
                    "duration": 10.0,
                },
                {
                    "name": "step2",
                    "skill": "n1_security",
                    "status": "success",
                    "duration": 30.0,
                },
            ],
            "context": {
                "step1": {"status": "SUCCESS", "has_data": True, "artifacts_count": 1},
            },
        }

        report = skill._generate_report(pipeline_result)

        assert "# 研究流水线执行报告" in report
        assert "总步骤数" in report
        assert "所有步骤执行成功" in report
