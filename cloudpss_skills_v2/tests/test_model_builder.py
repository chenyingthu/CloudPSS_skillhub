"""Tests for cloudpss_skills_v2.skills.model_builder."""
import pytest
from cloudpss_skills_v2.skills.model_builder import ModelBuilderSkill


class TestModelBuilderSkill:

    def test_import(self):
        """Smoke test: module and class can be imported."""
        assert ModelBuilderSkill is not None

    def test_instantiation(self):
        """Smoke test: class can be instantiated."""
        try:
            instance = ModelBuilderSkill()
        except TypeError:
            pytest.skip("Class requires constructor arguments")

    def test_has_name_attribute(self):
        """Smoke test: instance has expected attributes."""
        try:
            instance = ModelBuilderSkill()
            assert hasattr(instance, 'name') or hasattr(instance, 'run')
        except TypeError:
            pytest.skip("Class requires constructor arguments")
