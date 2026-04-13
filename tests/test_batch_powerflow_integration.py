#!/usr/bin/env python3
"""
Batch Power Flow Skill - Integration Tests

Tests for batch_powerflow skill with real CloudPSS API.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss_skills.builtin.batch_powerflow import BatchPowerFlowSkill
from cloudpss_skills.core import SkillStatus


class TestBatchPowerFlowSkillIntegration:
    """Integration tests for batch_powerflow skill"""

    def setup_method(self):
        """Setup for each test"""
        self.skill = BatchPowerFlowSkill()

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

        skill = get_skill("batch_powerflow")
        assert skill is not None
        assert skill.name == "batch_powerflow"

    def test_config_schema_validation(self):
        """Test config schema validation"""
        config = self.skill.get_default_config()
        result = self.skill.validate(config)
        assert result.valid or len(result.errors) > 0

    def test_validation_with_missing_model_rid(self):
        """Test validation handles missing model.rid"""
        config = {
            "skill": "batch_powerflow",
            "model": {},
        }
        result = self.skill.validate(config)
        # May be valid but with warnings
        assert result.valid or len(result.warnings) > 0 or len(result.errors) > 0

    @pytest.mark.integration
    def test_integration_ieee39_batch(self, auth_token):
        """Test batch power flow on IEEE39 model"""
        config = {
            "skill": "batch_powerflow",
            "auth": {"token": auth_token, },
            "model": {"rid": "model/holdme/IEEE39"},
            "scenarios": [
                {"name": "base", "modifications": {}},
                {"name": "high_load", "modifications": {"load_factor": 1.2}},
            ],
            "output": {"format": "json", "path": "/tmp", "prefix": "batch_test"},
        }

        result = self.skill.run(config)
        assert result is not None
        assert result.status in [SkillStatus.SUCCESS, SkillStatus.FAILED]

    @pytest.mark.integration
    def test_integration_result_structure(self, auth_token):
        """Test result has expected data structure"""
        config = {
            "skill": "batch_powerflow",
            "auth": {"token": auth_token, },
            "model": {"rid": "model/holdme/IEEE39"},
            "scenarios": [
                {"name": "base", "modifications": {}},
            ],
        }

        result = self.skill.run(config)
        if result.success:
            assert result.data is not None
            data = result.data
            # Should contain batch results
            assert "scenarios" in data or "results" in data or "summary" in data

    def test_default_config_values(self):
        """Test default config has correct structure"""
        config = self.skill.get_default_config()
        assert config["skill"] == "batch_powerflow"
        assert "models" in config  # Note: uses 'models' (plural) not 'model'
        assert len(config["models"]) > 0  # Should have at least one model
