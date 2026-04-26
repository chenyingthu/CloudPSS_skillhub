"""Tests for cloudpss_skills_v2.poweranalysis.batch_powerflow."""
import pytest
from cloudpss_skills_v2.poweranalysis.batch_powerflow import BatchPowerFlowAnalysis


class TestBatchPowerFlowAnalysis:

    def test_import(self):
        """Smoke test: module and class can be imported."""
        assert BatchPowerFlowAnalysis is not None

    def test_instantiation(self):
        """Smoke test: class can be instantiated."""
        instance = BatchPowerFlowAnalysis()
        assert instance is not None

    def test_has_name_attribute(self):
        """Smoke test: instance has expected attributes."""
        instance = BatchPowerFlowAnalysis()
        assert hasattr(instance, 'name') or hasattr(instance, 'run')
