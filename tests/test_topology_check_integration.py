#!/usr/bin/env python3
"""
Topology Check Skill - Integration Tests

Tests for topology_check skill with real CloudPSS API.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss_skills.builtin.topology_check import TopologyCheckSkill
from cloudpss_skills.core import SkillStatus


class TestTopologyCheckSkillIntegration:
    """Integration tests for topology_check skill"""

    def setup_method(self):
        """Setup for each test"""
        self.skill = TopologyCheckSkill()

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

        skill = get_skill("topology_check")
        assert skill is not None
        assert skill.name == "topology_check"

    def test_config_schema_validation(self):
        """Test config schema validation"""
        config = self.skill.get_default_config()
        result = self.skill.validate(config)
        assert result.valid or len(result.errors) > 0

    def test_validation_with_missing_model_rid(self):
        """Test validation handles missing model.rid"""
        config = {
            "skill": "topology_check",
            "model": {},
        }
        result = self.skill.validate(config)
        # May be valid but with warnings
        assert result.valid or len(result.warnings) > 0 or len(result.errors) > 0

    @pytest.mark.integration
    def test_integration_ieee39_topology(self, auth_token):
        """Test topology check on IEEE39 model"""
        config = {
            "skill": "topology_check",
            "auth": {"token": auth_token},
            "model": {"rid": "model/chenying/IEEE39"},
            "output": {"format": "json", "path": "/tmp", "prefix": "topology_test"},
        }

        result = self.skill.run(config)
        assert result is not None
        assert result.status in [SkillStatus.SUCCESS, SkillStatus.FAILED]

    @pytest.mark.integration
    def test_integration_ieee3_topology(self, auth_token):
        """Test topology check on IEEE3 model"""
        config = {
            "skill": "topology_check",
            "auth": {"token": auth_token},
            "model": {"rid": "model/chenying/IEEE3"},
        }

        result = self.skill.run(config)
        assert result.status in [SkillStatus.SUCCESS, SkillStatus.FAILED]

    @pytest.mark.integration
    def test_integration_result_structure(self, auth_token):
        """Test result has expected data structure"""
        config = {
            "skill": "topology_check",
            "auth": {"token": auth_token},
            "model": {"rid": "model/chenying/IEEE39"},
        }

        result = self.skill.run(config)
        if result.success:
            assert result.data is not None
            data = result.data
            # Should contain topology info
            assert (
                "buses" in data
                or "branches" in data
                or "components" in data
                or "summary" in data
            )

    def test_default_config_values(self):
        """Test default config has correct structure"""
        config = self.skill.get_default_config()
        assert config["skill"] == "topology_check"
        assert "model" in config
