"""Tests for cloudpss_skills_v2.poweranalysis.fault_severity_scan."""
import pytest
from cloudpss_skills_v2.poweranalysis.fault_severity_scan import FaultSeverityScanAnalysis


class TestFaultSeverityScanAnalysis:

    def test_import(self):
        """module and class can be imported."""
        assert FaultSeverityScanAnalysis is not None

    def test_instantiation(self):
        """class can be instantiated."""
        instance = FaultSeverityScanAnalysis()
        assert instance is not None

    def test_has_name_attribute(self):
        """instance has expected attributes."""
        instance = FaultSeverityScanAnalysis()
        assert hasattr(instance, 'name') or hasattr(instance, 'run')
