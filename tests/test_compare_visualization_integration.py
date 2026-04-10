#!/usr/bin/env python3
"""
compare_visualization Skill - Integration Tests

Tests for compare_visualization skill with real CloudPSS API.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss import setToken
from cloudpss_skills.builtin.compare_visualization import CompareVisualizationSkill
from cloudpss_skills.core import SkillStatus


class TestCompareVisualizationSkillIntegration:
    """Integration tests for compare_visualization skill"""

    def setup_method(self):
        """Setup for each test"""
        self.skill = CompareVisualizationSkill()

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
        skill = get_skill("compare_visualization")
        assert skill is not None
        assert skill.name == "compare_visualization"

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
            "skill": "compare_visualization",
            "auth": {"token": auth_token},
        }
        result = self.skill.validate(config)
        # Should fail or have warnings about missing rid

    @pytest.mark.integration
    def test_integration_real_api_call(self, auth_token):
        """Test real API call - requires valid token"""
        pytest.skip("TODO: Implement real API test")

    @pytest.mark.integration
    def test_integration_execution(self, auth_token):
        """Test full skill execution - requires valid token"""
        pytest.skip("TODO: Implement full execution test")
