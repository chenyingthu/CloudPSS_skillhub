#!/usr/bin/env python3
"""
谐波分析技能 - 单元测试
"""

from unittest.mock import Mock, patch

from cloudpss_skills.builtin.harmonic_analysis import HarmonicAnalysisSkill
from cloudpss_skills.core.base import SkillStatus


class FakeResult:
    def getPlots(self):
        return [{}]

    def getPlotChannelData(self, plot_idx, channel):
        return None


class TestHarmonicAnalysisUnit:
    @patch("cloudpss.setToken")
    @patch("cloudpss.Model")
    def test_run_fails_when_no_channels_produce_harmonic_data(self, mock_model_class, mock_set_token, tmp_path):
        skill = HarmonicAnalysisSkill()

        model = Mock()
        model.name = "TestModel"
        model.toJSON.return_value = {"dummy": True}
        job = Mock()
        job.id = "job-1"
        job.status.return_value = 1
        job.result = FakeResult()
        model.runEMT.return_value = job
        mock_model_class.fetch.return_value = model
        mock_model_class.return_value = model

        token_file = tmp_path / ".cloudpss_token"
        token_file.write_text("dummy", encoding="utf-8")

        result = skill.run(
            {
                "skill": "harmonic_analysis",
                "auth": {"token_file": str(token_file)},
                "model": {"rid": "model/test", "source": "cloud"},
                "channels": {"voltage": ["missing_v"], "current": []},
                "output": {"path": str(tmp_path), "generate_report": False, "export_spectrum": False},
            }
        )

        assert result.status == SkillStatus.FAILED
        assert "未从EMT结果中提取到任何有效的谐波分析通道" in (result.error or "")
