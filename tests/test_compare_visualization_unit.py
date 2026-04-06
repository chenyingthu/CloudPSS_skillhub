#!/usr/bin/env python3
"""
对比可视化技能 - 单元测试
"""

from pathlib import Path
from unittest.mock import patch

from cloudpss_skills.builtin.compare_visualization import CompareVisualizationSkill
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


class TestCompareVisualizationUnit:
    @patch("cloudpss.setToken")
    @patch("cloudpss_skills.builtin.compare_visualization.fetch_job_with_result")
    def test_run_fails_when_all_sources_have_no_usable_channels(self, mock_fetch, mock_set_token, tmp_path):
        skill = CompareVisualizationSkill()

        empty_result = FakeResult({"vac:0": {"x": [], "y": []}})
        mock_fetch.side_effect = [
            (object(), empty_result),
            (object(), empty_result),
        ]

        token_file = tmp_path / ".cloudpss_token"
        token_file.write_text("dummy-token", encoding="utf-8")

        config = {
            "skill": "compare_visualization",
            "auth": {"token_file": str(token_file)},
            "sources": [
                {"job_id": "job-1", "label": "case-1"},
                {"job_id": "job-2", "label": "case-2"},
            ],
            "output": {"path": str(tmp_path)},
        }

        result = skill.run(config)

        assert result.status == SkillStatus.FAILED
        assert "未提取到有效通道" in (result.error or "")
