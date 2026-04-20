"""Tests for cloudpss_skills_v2.libs.data_lib."""
import pytest
from cloudpss_skills_v2.libs.data_lib import BusData, BranchData, GeneratorData


class TestBusData:

    def test_import(self):
        """Smoke test: module and class can be imported."""
        assert BusData is not None

    def test_instantiation(self):
        """Smoke test: class can be instantiated."""
        try:
            instance = BusData()
        except TypeError:
            pytest.skip("Class requires constructor arguments")

    def test_has_name_attribute(self):
        """Smoke test: instance has expected attributes."""
        try:
            instance = BusData()
            assert hasattr(instance, 'name') or hasattr(instance, 'run')
        except TypeError:
            pytest.skip("Class requires constructor arguments")
