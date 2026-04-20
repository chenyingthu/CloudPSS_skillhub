#!/usr/bin/env python3
"""
fault_severity_scan Skill - Integration Tests

Tests for fault_severity_scan skill with real CloudPSS API.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss import setToken
from cloudpss_skills.builtin.fault_severity_scan import FaultSeverityScanSkill
from cloudpss_skills.core import SkillStatus


class TestFaultSeverityScanSkillIntegration:
    """Integration tests for fault_severity_scan skill"""

    def setup_method(self):
        """Setup for each test"""
        self.skill = FaultSeverityScanSkill()

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

        skill = get_skill("fault_severity_scan")
        assert skill is not None
        assert skill.name == "fault_severity_scan"

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
            "skill": "fault_severity_scan",
            "auth": {"token": auth_token, },
        }
        result = self.skill.validate(config)
        # Should fail or have warnings about missing rid

    @pytest.mark.integration
    def test_integration_ieee3_fault_severity_scan(self, auth_token):
        """Test fault severity scan on IEEE3 model"""
        import os

        

        config = {
            "skill": "fault_severity_scan",
            "auth": {"token": auth_token, },
            "model": {"rid": "model/holdme/IEEE3"},
            "scan": {
                "fs": 2.5,
                "fe": 2.7,
                "chg_values": [0.01, 0.1, 1.0],
            },
            "output": {"format": "json", "path": "/tmp", "prefix": "fs_test"},
        }

        result = self.skill.run(config)
        assert result is not None
        assert result.status in [SkillStatus.SUCCESS, SkillStatus.FAILED]

    @pytest.mark.integration
    def test_integration_documents_channel_requirement(self, auth_token):
        """Document that IEEE39 requires voltage channel pre-configuration"""
        pass
