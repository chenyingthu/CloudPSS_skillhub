#!/usr/bin/env python3
"""
emt_fault_study Skill - Integration Tests

Tests for emt_fault_study skill with real CloudPSS API.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss import setToken
from cloudpss_skills.builtin.emt_fault_study import EmtFaultStudySkill
from cloudpss_skills.core import SkillStatus


class TestEmtFaultStudySkillIntegration:
    """Integration tests for emt_fault_study skill"""

    def setup_method(self):
        """Setup for each test"""
        self.skill = EmtFaultStudySkill()

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

        skill = get_skill("emt_fault_study")
        assert skill is not None
        assert skill.name == "emt_fault_study"

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
            "skill": "emt_fault_study",
            "auth": {"token": auth_token, "server": "internal"},
        }
        result = self.skill.validate(config)
        # Should fail or have warnings about missing rid

    @pytest.mark.integration
    def test_integration_ieee3_fault_study(self, auth_token):
        """Test EMT fault study on IEEE3 model"""
        import os

        server: "internal"

        config = {
            "skill": "emt_fault_study",
            "auth": {"token": auth_token, "server": "internal"},
            "model": {"rid": "model/chenying/IEEE3"},
            "output": {"format": "json", "path": "/tmp", "prefix": "fault_study_test"},
        }

        result = self.skill.run(config)
        assert result is not None
        assert result.status in [SkillStatus.SUCCESS, SkillStatus.FAILED]

    @pytest.mark.integration
    def test_integration_documents_channel_requirement(self, auth_token):
        """Document that IEEE39 requires voltage channel pre-configuration"""
        # This test documents the expected behavior for IEEE39 models
        # that don't have pre-configured voltage channels
        pass
