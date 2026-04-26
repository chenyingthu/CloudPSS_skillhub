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
