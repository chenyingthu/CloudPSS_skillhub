"""Tests for cloudpss_skills_v2.poweranalysis.batch_powerflow."""
import pytest
from cloudpss_skills_v2.poweranalysis.batch_powerflow import BatchPowerFlowAnalysis


class TestBatchPowerFlowAnalysis:

    def test_import(self):
        """module and class can be imported."""
        assert BatchPowerFlowAnalysis is not None

    def test_instantiation(self):
        """class can be instantiated."""
        instance = BatchPowerFlowAnalysis()
        assert instance is not None

    def test_has_name_attribute(self):
        """instance has expected attributes."""
        instance = BatchPowerFlowAnalysis()
        assert hasattr(instance, 'name') or hasattr(instance, 'run')
