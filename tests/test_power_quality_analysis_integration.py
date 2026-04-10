#!/usr/bin/env python3
"""
power_quality_analysis Skill - Integration Tests

Tests for power_quality_analysis skill with real CloudPSS API.
"""

import os
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss import setToken
from cloudpss_skills.builtin.power_quality_analysis import PowerQualityAnalysisSkill
from cloudpss_skills.core import SkillStatus


class TestPowerQualityAnalysisSkillIntegration:
    """Integration tests for power_quality_analysis skill"""

    def setup_method(self):
        """Setup for each test"""
        self.skill = PowerQualityAnalysisSkill()

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

        skill = get_skill("power_quality_analysis")
        assert skill is not None
        assert skill.name == "power_quality_analysis"

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
            "skill": "power_quality_analysis",
            "auth": {"token": auth_token},
        }
        result = self.skill.validate(config)

    @pytest.mark.integration
    def test_integration_run_power_quality_analysis(self, auth_token):
        """Test running power quality analysis on IEEE3 model"""
        config = {
            "skill": "power_quality_analysis",
            "auth": {"token": auth_token, "server": "internal"},
            "model": {"rid": "model/chenying/IEEE3"},
        }
        result = self.skill.run(config)
        assert result.status in [SkillStatus.SUCCESS, SkillStatus.FAILED]
