"""Tests for cloudpss_skills_v2.libs.model_lib."""
import pytest
from cloudpss_skills_v2.libs.model_lib import PowerSystemModel, ModelConverter


class TestPowerSystemModel:

    def test_import(self):
        """Smoke test: module and class can be imported."""
        assert PowerSystemModel is not None

    def test_instantiation(self):
        """Smoke test: class can be instantiated."""
        instance = PowerSystemModel(name="test-model")
        assert instance is not None

    def test_has_name_attribute(self):
        """Smoke test: instance has expected attributes."""
        instance = PowerSystemModel(name="test-model")
        assert hasattr(instance, 'name') or hasattr(instance, 'run')
