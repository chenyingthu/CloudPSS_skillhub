"""Tests for cloudpss_skills_v2.poweranalysis.power_quality_analysis."""
import pytest
from cloudpss_skills_v2.poweranalysis.power_quality_analysis import PowerQualityAnalysisAnalysis


class TestPowerQualityAnalysisAnalysis:

    def test_import(self):
        """module and class can be imported."""
        assert PowerQualityAnalysisAnalysis is not None

    def test_instantiation(self):
        """class can be instantiated."""
        instance = PowerQualityAnalysisAnalysis()
        assert instance is not None

    def test_has_name_attribute(self):
        """instance has expected attributes."""
        instance = PowerQualityAnalysisAnalysis()
        assert hasattr(instance, 'name') or hasattr(instance, 'run')

    def test_requires_explicit_measurements(self):
        instance = PowerQualityAnalysisAnalysis()
        valid, errors = instance.validate({"model": {"rid": "case14"}})
        assert valid is False
        assert any("measurements" in error for error in errors)

    def test_accepts_explicit_harmonic_and_phase_measurements(self):
        instance = PowerQualityAnalysisAnalysis()
        valid, errors = instance.validate(
            {
                "model": {"rid": "case14"},
                "measurements": {
                    "harmonic_voltages": {"5": 0.03, "7": 0.02},
                    "phase_voltages_pu": [1.0, 0.98, 1.01],
                },
            }
        )
        assert valid is True
        assert errors == []
