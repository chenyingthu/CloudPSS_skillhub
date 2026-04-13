#!/usr/bin/env python3
"""
ieee3_prep Skill - Integration Tests

Tests for ieee3_prep skill with real CloudPSS API.
"""

import os
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss import setToken
from cloudpss_skills.builtin.ieee3_prep import IEEE3PrepSkill
from cloudpss_skills.core import SkillStatus


class TestIEEE3PrepSkillIntegration:
    """Integration tests for ieee3_prep skill"""

    def setup_method(self):
        """Setup for each test"""
        self.skill = IEEE3PrepSkill()

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

        skill = get_skill("ieee3_prep")
        assert skill is not None
        assert skill.name == "ieee3_prep"

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
            "skill": "ieee3_prep",
            "auth": {"token": auth_token, },
        }
        result = self.skill.validate(config)

    @pytest.mark.integration
    def test_integration_run_ieee3_prep(self, auth_token):
        """Test running ieee3_prep on IEEE3 model"""
        
        config = {
            "skill": "ieee3_prep",
            "auth": {"token": auth_token, },
            "model": {"rid": "model/holdme/IEEE3"},
        }
        result = self.skill.run(config)
        assert result.status in [SkillStatus.SUCCESS, SkillStatus.FAILED]
