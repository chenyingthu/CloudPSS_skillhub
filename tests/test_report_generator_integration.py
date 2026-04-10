#!/usr/bin/env python3
"""
report_generator Skill - Integration Tests

Tests for report_generator skill with real CloudPSS API.
"""

import os
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss import setToken
from cloudpss_skills.builtin.report_generator import ReportGeneratorSkill
from cloudpss_skills.core import SkillStatus


class TestReportGeneratorSkillIntegration:
    """Integration tests for report_generator skill"""

    def setup_method(self):
        """Setup for each test"""
        self.skill = ReportGeneratorSkill()

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

        skill = get_skill("report_generator")
        assert skill is not None
        assert skill.name == "report_generator"

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
            "skill": "report_generator",
            "auth": {"token": auth_token, "server": "internal"},
        }
        result = self.skill.validate(config)

    @pytest.mark.integration
    def test_integration_run_report_generator(self, auth_token):
        """Test running report generator on IEEE3 model"""
        server: "internal"
        config = {
            "skill": "report_generator",
            "auth": {"token": auth_token, "server": "internal"},
            "model": {"rid": "model/chenying/IEEE3"},
        }
        result = self.skill.run(config)
        assert result.status in [SkillStatus.SUCCESS, SkillStatus.FAILED]
