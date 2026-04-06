#!/usr/bin/env python3
"""
电能质量分析技能 - 单元测试
"""

from types import SimpleNamespace

import pytest

from cloudpss_skills.builtin.power_quality_analysis import PowerQualityAnalysisSkill
from cloudpss_skills.core.base import SkillStatus


class FakeResult:
    def __init__(self, plots, names):
        self._plots = plots
        self._names = names

    def getPlots(self):
        return self._plots

    def getPlotChannelNames(self, index):
        return self._names[index]


class TestPowerQualityAnalysisUnit:
    @pytest.fixture
    def skill(self):
        return PowerQualityAnalysisSkill()

    def test_detect_three_phase_channels_uses_channel_triplets_not_single_letter_title_matches(self, skill):
        result = FakeResult(
            plots=[{"data": {"title": "Device Overview"}}],
            names=[["bus1_va", "bus1_vb", "bus1_vc", "freq"]],
        )

        detected = skill._detect_three_phase_channels(result)

        assert len(detected) == 1
        assert detected[0]["a"] == "bus1_va"
        assert detected[0]["b"] == "bus1_vb"
        assert detected[0]["c"] == "bus1_vc"

    def test_summarize_pq_fails_when_only_error_placeholders_exist(self, skill):
        summary = skill._summarize_pq(
            {
                "harmonic": {"va": {"error": "无数据"}},
                "unbalance": {},
                "voltage_dip": {},
                "flicker": {},
                "dc_offset": {},
            },
            {"thd": 5.0},
        )

        assert summary["overall_status"] == "FAIL"
        assert summary["violation_count"] == 1
        assert summary["violations"][0]["type"] == "no_data"

    def test_valid_indicator_results_filters_error_entries(self, skill):
        filtered = skill._valid_indicator_results(
            {
                "good": {"thd": 1.2},
                "bad": {"error": "missing"},
                "empty": {},
            }
        )

        assert filtered == {"good": {"thd": 1.2}}
