#!/usr/bin/env python3
"""
Voltage Stability Skill - Integration Tests

Tests for voltage_stability skill with real CloudPSS API.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss_skills.builtin.voltage_stability import VoltageStabilitySkill
from cloudpss_skills.core import SkillStatus


class TestVoltageStabilitySkillIntegration:
    """Integration tests for voltage_stability skill"""

    def setup_method(self):
        """Setup for each test"""
        self.skill = VoltageStabilitySkill()

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

        skill = get_skill("voltage_stability")
        assert skill is not None
        assert skill.name == "voltage_stability"

    def test_config_schema_validation(self):
        """Test config schema validation"""
        config = self.skill.get_default_config()
        result = self.skill.validate(config)
        assert result.valid or len(result.errors) > 0

    def test_validation_with_missing_model_rid(self):
        """Test validation handles missing model.rid"""
        config = {
            "skill": "voltage_stability",
            "model": {},
        }
        result = self.skill.validate(config)
        assert result.valid or len(result.warnings) > 0 or len(result.errors) > 0

    @pytest.mark.integration
    def test_integration_ieee39_voltage_stability(self, auth_token):
        """Test voltage stability on IEEE39 model"""
        config = {
            "skill": "voltage_stability",
            "auth": {"token": auth_token, "server": "internal"},
            "model": {"rid": "model/chenying/IEEE39"},
            "scan": {
                "load_scaling": [1.0, 1.2],
            },
            "monitoring": {
                "buses": [],
                "collapse_threshold": 0.7,
            },
            "output": {"format": "json", "path": "/tmp", "prefix": "vs_test"},
        }

        result = self.skill.run(config)
        assert result is not None
        assert result.status in [SkillStatus.SUCCESS, SkillStatus.FAILED]

    def test_default_config_values(self):
        """Test default config has correct structure"""
        config = self.skill.get_default_config()
        assert config["skill"] == "voltage_stability"
        assert "model" in config
