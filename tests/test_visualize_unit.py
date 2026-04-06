#!/usr/bin/env python3
"""
可视化技能 - 单元测试
"""

from pathlib import Path
from unittest.mock import patch

from cloudpss_skills.builtin.visualize import VisualizeSkill
from cloudpss_skills.core.base import SkillStatus


class FakeResult:
    def getPlots(self):
        return [{}]

    def getPlotChannelNames(self, plot_index):
        return ["vac:0"]

    def getPlotChannelData(self, plot_index, channel):
        return {"x": [0.0, 1.0], "y": [1.0, 2.0]}


class TestVisualizeUnit:
    @patch("cloudpss.setToken")
    @patch("cloudpss_skills.builtin.visualize.fetch_job_with_result")
    def test_run_fails_when_requested_channels_are_missing(self, mock_fetch, mock_set_token, tmp_path):
        skill = VisualizeSkill()
        mock_fetch.return_value = (object(), FakeResult())

        token_file = tmp_path / ".cloudpss_token"
        token_file.write_text("dummy-token", encoding="utf-8")

        result = skill.run(
            {
                "skill": "visualize",
                "auth": {"token_file": str(token_file)},
                "source": {"job_id": "job-1"},
                "plot": {"channels": ["missing_channel"]},
                "output": {"path": str(tmp_path), "filename": "viz_test", "format": "png"},
            }
        )

        assert result.status == SkillStatus.FAILED
        assert "未找到任何可绘制的目标通道" in (result.error or "")
