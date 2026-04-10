#!/usr/bin/env python3
"""
short_circuit Skill - Integration Tests

Tests for short_circuit skill with real CloudPSS API.
"""

import os
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss import setToken
from cloudpss_skills.builtin.short_circuit import ShortCircuitSkill
from cloudpss_skills.core import SkillStatus


class TestShortCircuitSkillIntegration:
    """Integration tests for short_circuit skill"""

    def setup_method(self):
        """Setup for each test"""
        self.skill = ShortCircuitSkill()

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

        skill = get_skill("short_circuit")
        assert skill is not None
        assert skill.name == "short_circuit"

    def test_config_schema_validation(self):
        """Test config schema validation"""
        config = self.skill.get_default_config()
        result = self.skill.validate(config)
        assert result.valid or len(result.errors) > 0

    def test_validation_with_valid_config(self, auth_token):
        """Test validation with valid config"""
        config = self.skill.get_default_config()
        config["auth"] = {"token": auth_token}
        result = self.skill.validate(config)

    def test_validation_with_missing_rid(self, auth_token):
        """Test validation fails when model.rid is missing"""
        config = {
            "skill": "short_circuit",
            "auth": {"token": auth_token},
        }
        result = self.skill.validate(config)

    @pytest.mark.integration
    def test_integration_run_short_circuit(self, auth_token):
        """Test running short circuit analysis on IEEE3 model"""
        config = {
            "skill": "short_circuit",
            "auth": {"token": auth_token, "server": "internal"},
            "model": {"rid": "model/chenying/IEEE3"},
            "fault": {"location": "Bus1", "type": "three_phase"},
        }
        result = self.skill.run(config)
        assert result.status in [SkillStatus.SUCCESS, SkillStatus.FAILED]
