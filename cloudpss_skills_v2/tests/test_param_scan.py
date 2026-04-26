"""Tests for cloudpss_skills_v2.poweranalysis.param_scan."""
import pytest
from cloudpss_skills_v2.poweranalysis.param_scan import ParamScanAnalysis


class TestParamScanAnalysis:

    def test_import(self):
        """module and class can be imported."""
        assert ParamScanAnalysis is not None

    def test_instantiation(self):
        """class can be instantiated."""
        instance = ParamScanAnalysis()
        assert instance is not None

    def test_has_name_attribute(self):
        """instance has expected attributes."""
        instance = ParamScanAnalysis()
        assert hasattr(instance, 'name') or hasattr(instance, 'run')
