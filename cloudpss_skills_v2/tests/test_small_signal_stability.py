"""Tests for cloudpss_skills_v2.skills.small_signal_stability."""
import pytest
from cloudpss_skills_v2.skills.small_signal_stability import SmallSignalStabilitySkill


class TestSmallSignalStabilitySkill:

    def test_import(self):
        """Smoke test: module and class can be imported."""
        assert SmallSignalStabilitySkill is not None

    def test_instantiation(self):
        """Smoke test: class can be instantiated."""
        try:
            instance = SmallSignalStabilitySkill()
        except TypeError:
            pytest.skip("Class requires constructor arguments")

    def test_has_name_attribute(self):
        """Smoke test: instance has expected attributes."""
        try:
            instance = SmallSignalStabilitySkill()
            assert hasattr(instance, 'name') or hasattr(instance, 'run')
        except TypeError:
            pytest.skip("Class requires constructor arguments")
