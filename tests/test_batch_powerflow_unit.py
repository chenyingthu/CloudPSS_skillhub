#!/usr/bin/env python3
"""
批量潮流技能 - 单元测试
"""

from unittest.mock import Mock, patch

from cloudpss_skills.builtin.batch_powerflow import BatchPowerFlowSkill
from cloudpss_skills.core.base import SkillStatus


class TestBatchPowerFlowUnit:
    @patch("cloudpss.setToken")
    @patch("cloudpss.Model")
    @patch("cloudpss_skills.core.model_utils.Model")
    def test_partial_fetch_failure_returns_failed_skill_result(
        self, mock_model_utils_model, mock_model_class, mock_set_token
    ):
        skill = BatchPowerFlowSkill()

        ok_model = Mock()
        ok_model.name = "IEEE3"
        ok_job = Mock()
        ok_job.id = "job-ok"
        ok_job.status.return_value = 1
        ok_job.result.getBuses.return_value = [
            {"data": {"columns": [{"name": "Vm", "data": [1.0]}]}}
        ]
        ok_job.result.getBranches.return_value = [
            {"data": {"columns": [{"name": "Branch", "data": ["line-1"]}]}}
        ]
        ok_model.runPowerFlow.return_value = ok_job

        def fake_fetch(rid, **kwargs):
            if rid == "model/holdme/IEEE3":
                return ok_model
            raise Exception("invalid resource id")

        mock_model_class.fetch.side_effect = fake_fetch
        mock_model_utils_model.fetch.side_effect = fake_fetch

        config = {
            "skill": "batch_powerflow",
            "auth": {"token": "dummy"},
            "models": [
                {"rid": "model/holdme/IEEE3", "name": "IEEE3", "source": "cloud"},
                {"rid": "model/not_exists", "name": "BadModel", "source": "cloud"},
            ],
            "output": {
                "path": "/tmp",
                "aggregate": False,
                "timestamp": False,
                "prefix": "batch_powerflow_unit",
            },
        }

        result = skill.run(config)

        assert result.status == SkillStatus.FAILED
        assert result.data["summary"]["total"] == 2
        assert result.data["summary"]["converged"] == 1
        assert result.data["summary"]["failed"] == 1
        bad = next(
            item for item in result.data["results"] if item["model_name"] == "BadModel"
        )
        assert bad["status"] == "error"
        assert "invalid resource id" in bad["error"]
