#!/usr/bin/env python3
"""
Study Pipeline Skill - Integration Tests
"""

import pytest
import tempfile
from pathlib import Path

from cloudpss_skills.builtin.study_pipeline import StudyPipelineSkill
from cloudpss_skills.core.base import SkillStatus


@pytest.mark.integration
class TestStudyPipelineIntegration:
    """Study Pipeline 集成测试"""

    def test_pipeline_with_powerflow_only(self, tmp_path):
        """测试：仅包含 power_flow 的流水线"""
        skill = StudyPipelineSkill()

        config = {
            "skill": "study_pipeline",
            "auth": {"token_file": ".cloudpss_token_internal"},
            "pipeline": [
                {
                    "name": "baseline",
                    "skill": "power_flow",
                    "config": {
                        "model": {"rid": "model/holdme/IEEE3", "source": "cloud"},
                        "output": {
                            "path": str(tmp_path),
                            "prefix": "test_pf",
                            "timestamp": False,
                        },
                    },
                }
            ],
            "output": {
                "path": str(tmp_path),
                "prefix": "pipeline_test",
                "generate_report": True,
            },
        }

        result = skill.run(config)

        assert result.status == SkillStatus.SUCCESS
        assert result.data["success_count"] == 1
        assert len(result.artifacts) >= 1

    def test_pipeline_continues_on_failure(self, tmp_path):
        """测试：失败时继续执行"""
        skill = StudyPipelineSkill()

        config = {
            "skill": "study_pipeline",
            "auth": {"token_file": ".cloudpss_token_internal"},
            "pipeline": [
                {
                    "name": "step1",
                    "skill": "power_flow",
                    "config": {
                        "model": {"rid": "model/holdme/IEEE3", "source": "cloud"},
                    },
                },
                {
                    "name": "step2",
                    "skill": "power_flow",
                    "config": {
                        "model": {"rid": "nonexistent/model"},  # 会失败
                    },
                },
                {
                    "name": "step3",
                    "skill": "power_flow",
                    "config": {
                        "model": {"rid": "model/holdme/IEEE3", "source": "cloud"},
                    },
                },
            ],
            "continue_on_failure": True,
            "output": {
                "path": str(tmp_path),
                "prefix": "pipeline_continue",
            },
        }

        result = skill.run(config)

        assert result.data["total_steps"] == 3
        assert result.data["success_count"] == 2

    def test_pipeline_with_n1_security(self, tmp_path):
        """测试：power_flow + n1_security 流水线"""
        skill = StudyPipelineSkill()

        config = {
            "skill": "study_pipeline",
            "auth": {"token_file": ".cloudpss_token_internal"},
            "pipeline": [
                {
                    "name": "baseline",
                    "skill": "power_flow",
                    "config": {
                        "model": {"rid": "model/holdme/IEEE3", "source": "cloud"},
                    },
                },
                {
                    "name": "n1",
                    "skill": "n1_security",
                    "config": {
                        "model": {"rid": "model/holdme/IEEE3", "source": "cloud"},
                        "output": {"path": str(tmp_path)},
                    },
                },
            ],
            "output": {
                "path": str(tmp_path),
                "prefix": "pipeline_n1",
            },
        }

        result = skill.run(config)

        assert result.status in [SkillStatus.SUCCESS, SkillStatus.FAILED]
        assert result.data["total_steps"] == 2
