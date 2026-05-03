"""Tests for SkillBase unified model caching support.

TDD test to verify SkillBase caches and retrieves unified PowerSystemModel.
"""

import pytest
from cloudpss_skills_v2.powerskill.base import SkillBase
from cloudpss_skills_v2.core.system_model import PowerSystemModel, Bus


class MockSkill(SkillBase):
    """Concrete mock skill for testing SkillBase functionality."""

    @property
    def name(self) -> str:
        return "mock_skill"

    @property
    def description(self) -> str:
        return "Mock skill for unit testing"

    def run(self, config):
        pass

    def validate(self, config):
        pass


class TestSkillBaseUnifiedModel:
    """Test cases for SkillBase unified model caching."""

    def test_skill_base_caches_unified_model(self):
        """Test that SkillBase can cache and retrieve unified model."""
        skill = MockSkill()
        bus = Bus(bus_id=1, name="Bus 1", base_kv=110.0, bus_type="PQ")
        model = PowerSystemModel(buses=[bus], base_mva=100.0)

        # Set unified model
        skill.set_unified_model(model)

        # Verify get_unified_model returns it
        assert skill.get_unified_model() is model

    def test_skill_base_has_unified_model_returns_true_when_set(self):
        """Test has_unified_model returns True when model is set."""
        skill = MockSkill()
        bus = Bus(bus_id=1, name="Bus 1", base_kv=110.0, bus_type="PQ")
        model = PowerSystemModel(buses=[bus], base_mva=100.0)

        # Initially should be False
        assert skill.has_unified_model() is False

        # After setting should be True
        skill.set_unified_model(model)
        assert skill.has_unified_model() is True

    def test_skill_base_get_unified_model_returns_none_when_not_set(self):
        """Test get_unified_model returns None when no model set."""
        skill = MockSkill()

        assert skill.get_unified_model() is None

    def test_skill_base_unified_model_can_be_updated(self):
        """Test that unified model can be replaced."""
        skill = MockSkill()
        bus1 = Bus(bus_id=1, name="Bus 1", base_kv=110.0, bus_type="PQ")
        model1 = PowerSystemModel(buses=[bus1], base_mva=100.0)

        bus2 = Bus(bus_id=1, name="Bus 1 Updated", base_kv=220.0, bus_type="PV")
        model2 = PowerSystemModel(buses=[bus2], base_mva=1000.0)

        skill.set_unified_model(model1)
        assert skill.get_unified_model() is model1

        skill.set_unified_model(model2)
        assert skill.get_unified_model() is model2
        assert skill.get_unified_model() is not model1

    def test_skill_base_clear_unified_model(self):
        """Test that unified model can be cleared by setting None."""
        skill = MockSkill()
        bus = Bus(bus_id=1, name="Bus 1", base_kv=110.0, bus_type="PQ")
        model = PowerSystemModel(buses=[bus], base_mva=100.0)

        skill.set_unified_model(model)
        assert skill.has_unified_model() is True

        # Clear by setting None
        skill.set_unified_model(None)
        assert skill.has_unified_model() is False
        assert skill.get_unified_model() is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
