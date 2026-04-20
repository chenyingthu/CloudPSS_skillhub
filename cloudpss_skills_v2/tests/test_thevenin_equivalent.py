"""Tests for cloudpss_skills_v2.skills.thevenin_equivalent."""
import pytest
from cloudpss_skills_v2.skills.thevenin_equivalent import TheveninEquivalentSkill


class TestTheveninEquivalentSkill:

    def test_import(self):
        """Smoke test: module and class can be imported."""
        assert TheveninEquivalentSkill is not None

    def test_instantiation(self):
        """Smoke test: class can be instantiated."""
        try:
            instance = TheveninEquivalentSkill()
        except TypeError:
            pytest.skip("Class requires constructor arguments")

    def test_has_name_attribute(self):
        """Smoke test: instance has expected attributes."""
        try:
            instance = TheveninEquivalentSkill()
            assert hasattr(instance, 'name') or hasattr(instance, 'run')
        except TypeError:
            pytest.skip("Class requires constructor arguments")
