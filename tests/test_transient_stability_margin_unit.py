#!/usr/bin/env python3
"""
暂态稳定裕度技能 - 单元测试
"""

from unittest.mock import patch, Mock

from cloudpss_skills.builtin.transient_stability_margin import TransientStabilityMarginSkill
from cloudpss_skills.core.base import SkillStatus


class TestTransientStabilityMarginUnit:
    @patch("cloudpss_skills.builtin.transient_stability_margin.fetch_model_by_rid")
    @patch.object(TransientStabilityMarginSkill, "_check_stability")
    def test_compute_cct_expands_upper_bound_until_unstable(self, mock_check_stability, mock_fetch_model):
        skill = TransientStabilityMarginSkill()
        mock_fetch_model.return_value = Mock()
        mock_check_stability.side_effect = [
            (True, {"stable": True}),
            (True, {"stable": True}),
            (False, {"stable": False}),
            (True, {"stable": True}),
            (False, {"stable": False}),
            (True, {"stable": True}),
        ]

        cct = skill._compute_cct(
            "model/test",
            {"location": "BUS_1", "type": "three_phase"},
            {
                "analysis": {
                    "cct_initial_upper_bound": 1.0,
                    "cct_search_upper_bound": 5.0,
                    "cct_bound_expansion_factor": 2.0,
                    "cct_tolerance": 0.5,
                    "max_iterations": 6,
                }
            },
        )

        assert cct["bounded"] is True
        assert cct["cct_seconds"] >= 2.0

    @patch("cloudpss_skills.builtin.transient_stability_margin.fetch_model_by_rid")
    @patch.object(TransientStabilityMarginSkill, "_check_stability")
    def test_compute_cct_reports_lower_bound_when_no_unstable_upper_bound(self, mock_check_stability, mock_fetch_model):
        skill = TransientStabilityMarginSkill()
        mock_fetch_model.return_value = Mock()
        mock_check_stability.side_effect = [
            (True, {"stable": True}),
            (True, {"stable": True}),
            (True, {"stable": True}),
        ]

        cct = skill._compute_cct(
            "model/test",
            {"location": "BUS_1", "type": "three_phase"},
            {
                "analysis": {
                    "cct_initial_upper_bound": 1.0,
                    "cct_search_upper_bound": 4.0,
                    "cct_bound_expansion_factor": 2.0,
                    "cct_tolerance": 0.5,
                    "max_iterations": 6,
                }
            },
        )

        assert cct["bounded"] is False
        assert cct["cct_seconds"] == 4.0
        assert cct["cct_relation"] == ">="

    def test_compute_margin_marks_lower_bound_results(self):
        skill = TransientStabilityMarginSkill()

        margin = skill._compute_margin(
            {"cct_seconds": 4.0, "bounded": False, "cct_relation": ">="},
            baseline=0.1,
        )

        assert margin["bounded"] is False
        assert margin["cct_relation"] == ">="
        assert "下界" in margin["assessment"]

    @patch("cloudpss_skills.builtin.transient_stability_margin.trace_rms")
    @patch("cloudpss_skills.builtin.transient_stability_margin.find_trace")
    @patch("cloudpss_skills.builtin.transient_stability_margin.run_emt_and_wait")
    @patch("cloudpss_skills.builtin.transient_stability_margin.apply_fault_parameters")
    @patch("cloudpss_skills.builtin.transient_stability_margin.find_fault_component")
    @patch("cloudpss_skills.builtin.transient_stability_margin.clone_model")
    def test_check_stability_uses_waveform_recovery_ratios(
        self,
        mock_clone_model,
        mock_find_fault,
        mock_apply_fault,
        mock_run_emt,
        mock_find_trace,
        mock_trace_rms,
    ):
        skill = TransientStabilityMarginSkill()
        working_model = Mock()
        mock_clone_model.return_value = working_model
        fault = Mock()
        fault.args = {"fs": {"source": "3.0"}, "chg": {"source": "0.01"}}
        mock_find_fault.return_value = fault
        job = Mock()
        job.result = object()
        mock_run_emt.return_value = job
        mock_find_trace.return_value = (2, {"x": [0.0], "y": [1.0]})
        mock_trace_rms.side_effect = [1.0, 0.92, 0.97]

        stable, evidence = skill._check_stability(
            base_model=Mock(),
            scenario={"location": "BUS_1", "type": "three_phase"},
            clearing_time=0.2,
            config={"analysis": {"stability_trace_name": "vac:0"}},
        )

        assert stable is True
        assert evidence["postfault_ratio"] == 0.92
        assert evidence["late_recovery_ratio"] == 0.97

    @patch("cloudpss.setToken")
    @patch("cloudpss.Model")
    def test_run_wraps_generic_model_fetch_exception(self, mock_model_class, mock_set_token):
        skill = TransientStabilityMarginSkill()
        mock_model_class.fetch.side_effect = Exception("invalid resource id")

        result = skill.run(
            {
                "skill": "transient_stability_margin",
                "auth": {"token": "dummy"},
                "model": {"rid": "model/not_exists", "source": "cloud"},
                "fault_scenarios": [{"location": "BUS_1"}],
            }
        )

        assert result.status == SkillStatus.FAILED
        assert "invalid resource id" in (result.error or "")
