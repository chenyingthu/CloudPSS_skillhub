"""Tests for cloudpss_skills_v2.poweranalysis.parameter_sensitivity."""
import pytest
from cloudpss_skills_v2.poweranalysis.parameter_sensitivity import ParameterSensitivityAnalysis


class TestParameterSensitivityAnalysis:

    def test_import(self):
        """Smoke test: module and class can be imported."""
        assert ParameterSensitivityAnalysis is not None

    def test_instantiation(self):
        """Smoke test: class can be instantiated."""
        instance = ParameterSensitivityAnalysis()
        assert instance is not None

    def test_has_name_attribute(self):
        """Smoke test: instance has expected attributes."""
        instance = ParameterSensitivityAnalysis()
        assert hasattr(instance, 'name') or hasattr(instance, 'run')
