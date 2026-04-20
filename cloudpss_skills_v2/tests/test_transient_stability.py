"""Tests for cloudpss_skills_v2.skills.transient_stability."""
import pytest
from cloudpss_skills_v2.skills.transient_stability import TransientStabilitySkill


class TestTransientStabilitySkill:

    def test_import(self):
        """Smoke test: module and class can be imported."""
        assert TransientStabilitySkill is not None

    def test_instantiation(self):
        """Smoke test: class can be instantiated."""
        try:
            instance = TransientStabilitySkill()
        except TypeError:
            pytest.skip("Class requires constructor arguments")

    def test_has_name_attribute(self):
        """Smoke test: instance has expected attributes."""
        try:
            instance = TransientStabilitySkill()
            assert hasattr(instance, 'name') or hasattr(instance, 'run')
        except TypeError:
            pytest.skip("Class requires constructor arguments")
