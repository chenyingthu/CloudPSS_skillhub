#!/usr/bin/env python3
"""
波形导出技能 - 单元测试
"""

from pathlib import Path
from unittest.mock import Mock, patch

from cloudpss_skills.builtin.waveform_export import WaveformExportSkill
from cloudpss_skills.core.base import SkillStatus


class FakeResult:
    def getPlots(self):
        return [{"key": "plot-0"}]

    def getPlotChannelNames(self, plot_index):
        return ["vac:0"]

    def getPlotChannelData(self, plot_index, channel):
        return {"x": [0.0, 1.0], "y": [1.0, 2.0]}


class TestWaveformExportUnit:
    @patch("cloudpss.setToken")
    @patch("cloudpss_skills.builtin.waveform_export.fetch_job_with_result")
    def test_run_fails_when_requested_channels_are_missing(self, mock_fetch, mock_set_token, tmp_path):
        skill = WaveformExportSkill()

        job = Mock()
        job.status.return_value = 1
        mock_fetch.return_value = (job, FakeResult())

        token_file = tmp_path / ".cloudpss_token"
        token_file.write_text("dummy-token", encoding="utf-8")

        result = skill.run(
            {
                "skill": "waveform_export",
                "source": {
                    "job_id": "job-1",
                    "auth": {"token_file": str(token_file)},
                },
                "export": {"channels": ["missing_channel"]},
                "output": {"path": str(tmp_path), "filename": "wf.csv", "format": "csv"},
            }
        )

        assert result.status == SkillStatus.FAILED
        assert "未找到任何可导出的目标波形通道" in (result.error or "")
