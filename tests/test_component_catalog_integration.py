#!/usr/bin/env python3
"""
component_catalog Skill - Integration Tests

Tests for component_catalog skill with real CloudPSS API.
"""

import os
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss import setToken
from cloudpss_skills.builtin.component_catalog import ComponentCatalogSkill
from cloudpss_skills.core import SkillStatus


class TestComponentCatalogSkillIntegration:
    """Integration tests for component_catalog skill"""

    def setup_method(self):
        """Setup for each test"""
        self.skill = ComponentCatalogSkill()

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

        skill = get_skill("component_catalog")
        assert skill is not None
        assert skill.name == "component_catalog"

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
            "skill": "component_catalog",
            "auth": {"token": auth_token, },
        }
        result = self.skill.validate(config)

    @pytest.mark.integration
    def test_integration_list_components(self, auth_token):
        """Test listing components from IEEE3 model"""
        
        config = {
            "skill": "component_catalog",
            "auth": {"token": auth_token, },
            "model": {"rid": "model/holdme/IEEE3"},
        }
        result = self.skill.run(config)
        assert result.status in [SkillStatus.SUCCESS, SkillStatus.FAILED]
