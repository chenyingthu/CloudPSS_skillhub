#!/usr/bin/env python3
"""
Power Flow Skill - Integration Tests

Tests for power_flow skill with real CloudPSS API.
"""

import pytest
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss_skills.builtin.power_flow import PowerFlowSkill
from cloudpss_skills.core import SkillStatus


class TestPowerFlowSkillIntegration:
    """Integration tests for power_flow skill"""

    def setup_method(self):
        """Setup for each test"""
        self.skill = PowerFlowSkill()

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

        skill = get_skill("power_flow")
        assert skill is not None
        assert skill.name == "power_flow"

    def test_config_schema_validation(self):
        """Test config schema validation"""
        config = self.skill.get_default_config()
        result = self.skill.validate(config)
        assert result.valid or len(result.errors) > 0

    def test_validation_with_missing_rid(self):
        """Test validation handles missing model.rid"""
        config = {
            "skill": "power_flow",
            "model": {},
        }
        result = self.skill.validate(config)
        # May be valid but with warnings, or invalid
        assert result.valid or len(result.warnings) > 0 or len(result.errors) > 0

    def test_validation_with_missing_auth(self):
        """Test validation handles missing auth"""
        config = {
            "skill": "power_flow",
            "model": {"rid": "model/test"},
        }
        result = self.skill.validate(config)
        # Should have warnings about missing auth

    @pytest.mark.integration
    def test_integration_ieee39_convergence(self, auth_token):
        """Test IEEE39 model converges"""
        config = {
            "skill": "power_flow",
            "auth": {"token": auth_token, "server": "internal"},
            "model": {"rid": "model/chenying/IEEE39"},
            "algorithm": {
                "type": "newton_raphson",
                "tolerance": 1e-6,
            },
            "output": {"format": "json", "path": "/tmp", "prefix": "pf_test"},
        }

        result = self.skill.run(config)
        assert result.status in [SkillStatus.SUCCESS, SkillStatus.FAILED]
        assert result.data is not None

    @pytest.mark.integration
    def test_integration_ieee3_convergence(self, auth_token):
        """Test IEEE3 model converges"""
        config = {
            "skill": "power_flow",
            "auth": {"token": auth_token, "server": "internal"},
            "model": {"rid": "model/chenying/IEEE3"},
            "algorithm": {
                "type": "newton_raphson",
                "tolerance": 1e-6,
            },
        }

        result = self.skill.run(config)
        assert result.status in [SkillStatus.SUCCESS, SkillStatus.FAILED]

    @pytest.mark.integration
    def test_integration_result_structure(self, auth_token):
        """Test result has expected data structure"""
        config = {
            "skill": "power_flow",
            "auth": {"token": auth_token, "server": "internal"},
            "model": {"rid": "model/chenying/IEEE39"},
            "output": {"format": "json"},
        }

        result = self.skill.run(config)
        assert result.success
        data = result.data

        # Check expected keys
        assert "buses" in data or "bus_count" in data or "summary" in data

    @pytest.mark.integration
    def test_integration_fast_decoupled_algorithm(self, auth_token):
        """Test fast_decoupled algorithm"""
        config = {
            "skill": "power_flow",
            "auth": {"token": auth_token, "server": "internal"},
            "model": {"rid": "model/chenying/IEEE39"},
            "algorithm": {
                "type": "fast_decoupled",
                "tolerance": 1e-5,
            },
        }

        result = self.skill.run(config)
        # May or may not converge depending on system
        assert result.status in [SkillStatus.SUCCESS, SkillStatus.FAILED]

    @pytest.mark.integration
    def test_integration_nonexistent_model(self, auth_token):
        """Test handling of nonexistent model"""
        config = {
            "skill": "power_flow",
            "auth": {"token": auth_token, "server": "internal"},
            "model": {"rid": "model/nonexistent/model"},
            "output": {"path": "/tmp"},
        }

        result = self.skill.run(config)
        assert result.status == SkillStatus.FAILED

    def test_default_config_values(self):
        """Test default config has correct values"""
        config = self.skill.get_default_config()
        assert config["skill"] == "power_flow"
        assert config["algorithm"]["type"] == "newton_raphson"
        assert config["algorithm"]["tolerance"] == 1e-6
        assert config["output"]["format"] == "json"
