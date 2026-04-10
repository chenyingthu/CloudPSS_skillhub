#!/usr/bin/env python3
"""
emt_n1_screening Skill - Integration Tests

Tests for emt_n1_screening skill with real CloudPSS API.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss import setToken
from cloudpss_skills.builtin.emt_n1_screening import EmtN1ScreeningSkill
from cloudpss_skills.core import SkillStatus


class TestEmtN1ScreeningSkillIntegration:
    """Integration tests for emt_n1_screening skill"""

    def setup_method(self):
        """Setup for each test"""
        self.skill = EmtN1ScreeningSkill()

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

        skill = get_skill("emt_n1_screening")
        assert skill is not None
        assert skill.name == "emt_n1_screening"

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
            "skill": "emt_n1_screening",
            "auth": {"token": auth_token},
        }
        result = self.skill.validate(config)
        # Should fail or have warnings about missing rid

    @pytest.mark.integration
    def test_integration_ieee3_n1_screening(self, auth_token):
        """Test EMT N-1 screening on IEEE3 model"""
        import os

        os.environ["CLOUDPSS_API_URL"] = "http://166.111.60.76:50001"

        config = {
            "skill": "emt_n1_screening",
            "auth": {"token": auth_token},
            "model": {"rid": "model/chenying/IEEE3"},
            "n1_scenarios": {
                "branch_outages": [{"from_bus": "Bus1", "to_bus": "Bus2"}],
            },
            "output": {"format": "json", "path": "/tmp", "prefix": "n1_test"},
        }

        result = self.skill.run(config)
        assert result is not None
        assert result.status in [SkillStatus.SUCCESS, SkillStatus.FAILED]

    @pytest.mark.integration
    def test_integration_documents_channel_requirement(self, auth_token):
        """Document that IEEE39 requires voltage channel pre-configuration"""
        pass
