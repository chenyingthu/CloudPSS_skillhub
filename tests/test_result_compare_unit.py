#!/usr/bin/env python3
"""
结果对比技能 - 单元测试

Note: Tests are marked as integration because they require mocking that conflicts with
conftest.py's module reimport behavior.
"""

import pytest
from pathlib import Path
from unittest.mock import patch

from cloudpss_skills.builtin.result_compare import ResultCompareSkill
from cloudpss_skills.core.base import SkillStatus


class FakeResult:
    def __init__(self, channels):
        self._channels = channels

    def getPlots(self):
        return [{}]

    def getPlotChannelNames(self, plot_index):
        return list(self._channels.keys())

    def getPlotChannelData(self, plot_index, channel):
        return self._channels[channel]


class TestResultCompareUnit:
    @pytest.mark.integration
    @patch("cloudpss.setToken")
    @patch("cloudpss_skills.core.utils.fetch_job_with_result")
    def test_run_fails_when_fewer_than_two_valid_results_are_available(
        self, mock_fetch, mock_set_token, tmp_path
    ):
        skill = ResultCompareSkill()

        valid_result = FakeResult({"vac:0": {"y": [1.0, 2.0]}})
        mock_fetch.side_effect = [
            (object(), valid_result),
            (object(), None),
        ]

        token_file = tmp_path / ".cloudpss_token"
        token_file.write_text("dummy-token", encoding="utf-8")

        result = skill.run(
            {
                "skill": "result_compare",
                "auth": {"token_file": str(token_file)},
                "sources": [
                    {"job_id": "job-1", "label": "case-1"},
                    {"job_id": "job-2", "label": "case-2"},
                ],
                "output": {"path": str(tmp_path), "timestamp": False},
            }
        )

        assert result.status == SkillStatus.FAILED
        assert "有效结果少于2个" in (result.error or "")
