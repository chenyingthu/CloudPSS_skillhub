"""Tests for cloudpss_skills_v2.poweranalysis.transient_stability_margin."""
import pytest
from cloudpss_skills_v2.poweranalysis.transient_stability_margin import TransientStabilityMarginAnalysis


class TestTransientStabilityMarginAnalysis:

    def test_import(self):
        """module and class can be imported."""
        assert TransientStabilityMarginAnalysis is not None

    def test_instantiation(self):
        """class can be instantiated."""
        instance = TransientStabilityMarginAnalysis()
        assert instance is not None

    def test_has_name_attribute(self):
        """instance has expected attributes."""
        instance = TransientStabilityMarginAnalysis()
        assert hasattr(instance, 'name') or hasattr(instance, 'run')

    def test_requires_explicit_cct_for_each_fault_scenario(self):
        instance = TransientStabilityMarginAnalysis()
        valid, errors = instance.validate(
            {
                "model": {"rid": "case14"},
                "fault_scenarios": [{"location": "bus:0", "clearing_time": 0.1}],
            }
        )
        assert valid is False
        assert any(".cct is required" in error for error in errors)

    def test_accepts_explicit_clearing_time_and_cct(self):
        instance = TransientStabilityMarginAnalysis()
        valid, errors = instance.validate(
            {
                "model": {"rid": "case14"},
                "fault_scenarios": [
                    {"location": "bus:0", "clearing_time": 0.1, "cct": 0.2}
                ],
            }
        )
        assert valid is True
        assert errors == []

    def test_run_reports_explicit_cct_data_source(self):
        instance = TransientStabilityMarginAnalysis()
        result = instance.run(
            {
                "model": {"rid": "case14"},
                "fault_scenarios": [
                    {"location": "bus:0", "clearing_time": 0.1, "cct": 0.2}
                ],
            }
        )
        assert result.is_success
        assert result.data["data_source"] == "fault_scenarios.cct"
        assert result.data["results"][0]["margin_percent"] == 50.0
