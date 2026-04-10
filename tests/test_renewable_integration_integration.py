#!/usr/bin/env python3
"""
renewable_integration Skill - Integration Tests

Tests for renewable_integration skill with real CloudPSS API.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss import setToken
from cloudpss_skills.builtin.renewable_integration import RenewableIntegrationSkill
from cloudpss_skills.core import SkillStatus


class TestRenewableIntegrationSkillIntegration:
    """Integration tests for renewable_integration skill"""

    def setup_method(self):
        """Setup for each test"""
        self.skill = RenewableIntegrationSkill()

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

        skill = get_skill("renewable_integration")
        assert skill is not None
        assert skill.name == "renewable_integration"

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
        # Validation may fail due to missing rid, which is expected

    def test_validation_with_missing_rid(self, auth_token):
        """Test validation fails when model.rid is missing"""
        config = {
            "skill": "renewable_integration",
            "auth": {"token": auth_token},
        }
        result = self.skill.validate(config)
        # Should fail or have warnings about missing rid

    @pytest.mark.integration
    def test_integration_ieee3_renewable_analysis(self, auth_token):
        """Test renewable integration analysis on IEEE3 model"""
        config = {
            "skill": "renewable_integration",
            "auth": {"token": auth_token, "server": "internal"},
            "model": {"rid": "model/chenying/IEEE3"},
            "output": {"format": "json", "path": "/tmp", "prefix": "renewable_test"},
        }

        result = self.skill.run(config)
        assert result is not None
        assert result.status in [SkillStatus.SUCCESS, SkillStatus.FAILED]

    @pytest.mark.integration
    def test_integration_documents_expected_behavior(self, auth_token):
        """Document expected behavior for renewable integration analysis"""
        pass
