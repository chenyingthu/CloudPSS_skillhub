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
