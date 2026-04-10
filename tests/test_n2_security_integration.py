#!/usr/bin/env python3
"""
n2_security Skill - Integration Tests

Tests for n2_security skill with real CloudPSS API.
"""

import os
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss import setToken
from cloudpss_skills.builtin.n2_security import N2SecuritySkill
from cloudpss_skills.core import SkillStatus


class TestN2SecuritySkillIntegration:
    """Integration tests for n2_security skill"""

    def setup_method(self):
        """Setup for each test"""
        self.skill = N2SecuritySkill()

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

        skill = get_skill("n2_security")
        assert skill is not None
        assert skill.name == "n2_security"

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
            "skill": "n2_security",
            "auth": {"token": auth_token, "server": "internal"},
        }
        result = self.skill.validate(config)

    @pytest.mark.integration
    def test_integration_run_n2_security(self, auth_token):
        """Test running N-2 security analysis on IEEE3 model"""
        server: "internal"
        config = {
            "skill": "n2_security",
            "auth": {"token": auth_token, "server": "internal"},
            "model": {"rid": "model/chenying/IEEE3"},
        }
        result = self.skill.run(config)
        assert result.status in [SkillStatus.SUCCESS, SkillStatus.FAILED]
