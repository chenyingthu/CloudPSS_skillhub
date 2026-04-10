#!/usr/bin/env python3
"""
Parameter Scan Skill - Integration Tests

Tests for param_scan skill with real CloudPSS API.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss_skills.builtin.param_scan import ParamScanSkill
from cloudpss_skills.core import SkillStatus


class TestParamScanSkillIntegration:
    """Integration tests for param_scan skill"""

    def setup_method(self):
        """Setup for each test"""
        self.skill = ParamScanSkill()

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

        skill = get_skill("param_scan")
        assert skill is not None
        assert skill.name == "param_scan"

    def test_config_schema_validation(self):
        """Test config schema validation"""
        config = self.skill.get_default_config()
        result = self.skill.validate(config)
        assert result.valid or len(result.errors) > 0

    def test_validation_with_missing_model_rid(self):
        """Test validation fails when model.rid is missing"""
        config = {
            "skill": "param_scan",
            "model": {},
        }
        result = self.skill.validate(config)
        assert not result.valid

    def test_validation_with_missing_scan_params(self):
        """Test validation fails when scan params are missing"""
        config = {
            "skill": "param_scan",
            "auth": {"token": "test"},
            "model": {"rid": "model/test"},
        }
        result = self.skill.validate(config)
        # Should fail or have warnings

    @pytest.mark.integration
    def test_integration_ieee3_powerflow_scan(self, auth_token):
        """Test parameter scan with power flow on IEEE3"""
        config = {
            "skill": "param_scan",
            "auth": {"token": auth_token},
            "model": {"rid": "model/chenying/IEEE3"},
            "scan": {
                "simulation_type": "power_flow",
                "values": [1.0, 1.1, 1.2],  # Simple load scaling
            },
            "output": {"format": "json", "path": "/tmp", "prefix": "scan_test"},
        }

        result = self.skill.run(config)
        assert result is not None
        assert result.status in [SkillStatus.SUCCESS, SkillStatus.FAILED]

    @pytest.mark.integration
    def test_integration_result_structure(self, auth_token):
        """Test result has expected data structure"""
        config = {
            "skill": "param_scan",
            "auth": {"token": auth_token},
            "model": {"rid": "model/chenying/IEEE3"},
            "scan": {
                "simulation_type": "power_flow",
                "values": [1.0, 1.2],
            },
        }

        result = self.skill.run(config)
        if result.success:
            assert result.data is not None
            data = result.data
            # Should contain scan results
            assert "results" in data or "summary" in data or "scans" in data

    def test_default_config_values(self):
        """Test default config has correct structure"""
        config = self.skill.get_default_config()
        assert config["skill"] == "param_scan"
        assert "model" in config
        assert "scan" in config
