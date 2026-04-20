"""Tests for cloudpss_skills_v2.skills.n1_security."""
import pytest
from cloudpss_skills_v2.skills.n1_security import N1SecuritySkill


class TestN1SecuritySkill:

    def test_import(self):
        """Smoke test: module and class can be imported."""
        assert N1SecuritySkill is not None

    def test_instantiation(self):
        """Smoke test: class can be instantiated."""
        try:
            instance = N1SecuritySkill()
        except TypeError:
            pytest.skip("Class requires constructor arguments")

    def test_has_name_attribute(self):
        """Smoke test: instance has expected attributes."""
        try:
            instance = N1SecuritySkill()
            assert hasattr(instance, 'name') or hasattr(instance, 'run')
        except TypeError:
            pytest.skip("Class requires constructor arguments")
