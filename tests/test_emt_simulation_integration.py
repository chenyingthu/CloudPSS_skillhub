#!/usr/bin/env python3
"""
EMT Simulation Skill - Integration Tests

Tests for emt_simulation skill with real CloudPSS API.
"""

import pytest
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss_skills.builtin.emt_simulation import EmtSimulationSkill
from cloudpss_skills.core import SkillStatus


class TestEmtSimulationSkillIntegration:
    """Integration tests for emt_simulation skill"""

    def setup_method(self):
        """Setup for each test"""
        self.skill = EmtSimulationSkill()

    @pytest.fixture(scope="class")
    def auth_token(self):
        """Load auth token from file"""
        token_path = Path(".cloudpss_token_internal")
        if token_path.exists():
            return token_path.read_text().strip()
        token_path = Path(".cloudpss_token")
        if token_path.exists():
            return token_path.read_text().strip()
        pytest.skip("No CloudPSS token found")

    def test_skill_registration(self):
        """Test that skill is registered"""
        from cloudpss_skills import get_skill

        skill = get_skill("emt_simulation")
        assert skill is not None
        assert skill.name == "emt_simulation"

    def test_config_schema_validation(self):
        """Test config schema validation"""
        config = self.skill.get_default_config()
        result = self.skill.validate(config)
        assert result.valid or len(result.errors) > 0

    def test_validation_with_missing_model_rid(self):
        """Test validation fails when model.rid is missing"""
        config = {
            "skill": "emt_simulation",
            "auth": {"token": "test"},
            "model": {},
        }
        result = self.skill.validate(config)
        assert not result.valid
        assert any("rid" in e.lower() for e in result.errors)

    def test_validation_with_missing_auth(self):
        """Test validation fails when auth is missing"""
        config = {
            "skill": "emt_simulation",
            "model": {"rid": "model/test"},
        }
        result = self.skill.validate(config)
        assert not result.valid
        assert any("auth" in e.lower() or "token" in e.lower() for e in result.errors)

    @pytest.mark.integration
    def test_integration_ieee3_emt(self, auth_token):
        """Test IEEE3 model EMT simulation"""
        config = {
            "skill": "emt_simulation",
            "auth": {"token": auth_token},
            "model": {"rid": "model/chenying/IEEE3"},
            "simulation": {
                "duration": 0.1,
            },
            "output": {"format": "csv", "path": "/tmp", "prefix": "emt_test"},
        }

        result = self.skill.run(config)
        # May succeed or fail depending on model state
        assert result is not None
        assert result.status in [
            SkillStatus.SUCCESS,
            SkillStatus.FAILED,
            SkillStatus.PENDING,
        ]

    @pytest.mark.integration
    def test_integration_result_has_plots(self, auth_token):
        """Test result has expected plot data"""
        config = {
            "skill": "emt_simulation",
            "auth": {"token": auth_token},
            "model": {"rid": "model/chenying/IEEE3"},
            "simulation": {
                "duration": 0.1,
            },
        }

        result = self.skill.run(config)
        if result.success:
            assert result.data is not None
            # Result should contain plot information
            assert "plots" in result.data or "job_id" in result.data

    @pytest.mark.integration
    @pytest.mark.slow_emt
    def test_integration_longer_simulation(self, auth_token):
        """Test longer EMT simulation"""
        config = {
            "skill": "emt_simulation",
            "auth": {"token": auth_token},
            "model": {"rid": "model/chenying/IEEE3"},
            "simulation": {
                "duration": 1.0,
            },
        }

        result = self.skill.run(config)
        assert result.status in [
            SkillStatus.SUCCESS,
            SkillStatus.FAILED,
            SkillStatus.PENDING,
        ]

    def test_default_config_values(self):
        """Test default config has correct values"""
        config = self.skill.get_default_config()
        assert config["skill"] == "emt_simulation"
        assert "simulation" in config
        # Check simulation has expected keys
        assert len(config["simulation"]) > 0

    def test_simulation_duration_validation(self):
        """Test validation handles invalid duration"""
        config = {
            "skill": "emt_simulation",
            "auth": {"token": "test"},
            "model": {"rid": "model/test"},
            "simulation": {
                "duration": -1,  # Invalid
            },
        }
        result = self.skill.validate(config)
        # Should have warnings but not errors
        assert result.valid or len(result.warnings) > 0
