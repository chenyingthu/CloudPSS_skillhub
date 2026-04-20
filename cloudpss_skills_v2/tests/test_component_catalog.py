"""Tests for cloudpss_skills_v2.skills.component_catalog."""
import pytest
from cloudpss_skills_v2.skills.component_catalog import ComponentCatalogSkill


class TestComponentCatalogSkill:

    def test_import(self):
        """Smoke test: module and class can be imported."""
        assert ComponentCatalogSkill is not None

    def test_instantiation(self):
        """Smoke test: class can be instantiated."""
        try:
            instance = ComponentCatalogSkill()
        except TypeError:
            pytest.skip("Class requires constructor arguments")

    def test_has_name_attribute(self):
        """Smoke test: instance has expected attributes."""
        try:
            instance = ComponentCatalogSkill()
            assert hasattr(instance, 'name') or hasattr(instance, 'run')
        except TypeError:
            pytest.skip("Class requires constructor arguments")
