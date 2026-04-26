"""Tests for cloudpss_skills_v2.poweranalysis.harmonic_analysis."""
import pytest
from cloudpss_skills_v2.poweranalysis.harmonic_analysis import HarmonicAnalysisAnalysis


class TestHarmonicAnalysisAnalysis:

    def test_import(self):
        """module and class can be imported."""
        assert HarmonicAnalysisAnalysis is not None

    def test_instantiation(self):
        """class can be instantiated."""
        instance = HarmonicAnalysisAnalysis()
        assert instance is not None

    def test_has_name_attribute(self):
        """instance has expected attributes."""
        instance = HarmonicAnalysisAnalysis()
        assert hasattr(instance, 'name') or hasattr(instance, 'run')
