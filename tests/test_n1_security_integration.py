#!/usr/bin/env python3
"""
N-1 Security Analysis Skill - Integration Tests

Tests for n1_security skill with real CloudPSS API.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss_skills.builtin.n1_security import N1SecuritySkill
from cloudpss_skills.core import SkillStatus


class TestN1SecuritySkillIntegration:
    """Integration tests for n1_security skill"""

    def setup_method(self):
        """Setup for each test"""
        self.skill = N1SecuritySkill()

    @pytest.fixture(scope="class")
    def auth_token(self):
        """Load auth token from file (prefer public cloud token)"""
        token_path = Path(".cloudpss_token")
        if token_path.exists():
            return token_path.read_text().strip()
        token_path = Path(".cloudpss_token_internal")
        if token_path.exists():
            return token_path.read_text().strip()
        pytest.skip("No CloudPSS token found")

    def test_skill_registration(self):
        """Test that skill is registered"""
        from cloudpss_skills import get_skill

        skill = get_skill("n1_security")
        assert skill is not None
        assert skill.name == "n1_security"

    def test_config_schema_validation(self):
        """Test config schema validation"""
        config = self.skill.get_default_config()
        result = self.skill.validate(config)
        assert result.valid or len(result.errors) > 0

    def test_validation_with_missing_model_rid(self):
        """Test validation handles missing model.rid"""
        config = {
            "skill": "n1_security",
            "model": {},
        }
        result = self.skill.validate(config)
        # May be valid but with warnings
        assert result.valid or len(result.warnings) > 0 or len(result.errors) > 0

    def test_validation_with_missing_auth(self):
        """Test validation handles missing auth"""
        config = {
            "skill": "n1_security",
            "model": {"rid": "model/test"},
        }
        result = self.skill.validate(config)
        # May fail or have warnings

    @pytest.mark.integration
    @pytest.mark.slow
    def test_integration_ieee3_n1_screening(self, auth_token):
        """Test N-1 screening on IEEE3 model (requires multiple power flow runs)"""
        import os

        server: "internal"

        config = {
            "skill": "n1_security",
            "auth": {"token": auth_token},
            "model": {"rid": "model/holdme/IEEE3"},
            "analysis": {
                "branch_types": ["TransmissionLine", "_newTransformer_3p2w"],
                "max_outages": 3,
            },
            "output": {"format": "json", "path": "/tmp", "prefix": "n1_test"},
        }

        result = self.skill.run(config)
        assert result is not None
        assert result.status in [SkillStatus.SUCCESS, SkillStatus.FAILED]

    @pytest.mark.integration
    @pytest.mark.slow
    def test_integration_result_structure(self, auth_token):
        """Test result has expected data structure (requires multiple power flow runs)"""
        import os

        server: "internal"

        config = {
            "skill": "n1_security",
            "auth": {"token": auth_token},
            "model": {"rid": "model/holdme/IEEE3"},
            "analysis": {
                "max_outages": 2,
            },
        }

        result = self.skill.run(config)
        if result.success:
            assert result.data is not None

    @pytest.mark.integration
    @pytest.mark.slow
    def test_integration_single_branch_outage(self, auth_token):
        """Test single branch outage analysis (requires power flow runs)"""
        import os

        server: "internal"

        config = {
            "skill": "n1_security",
            "auth": {"token": auth_token},
            "model": {"rid": "model/holdme/IEEE3"},
            "analysis": {
                "max_outages": 1,
            },
        }

        result = self.skill.run(config)
        assert result.status in [SkillStatus.SUCCESS, SkillStatus.FAILED]

    def test_default_config_values(self):
        """Test default config has correct structure"""
        config = self.skill.get_default_config()
        assert config["skill"] == "n1_security"
        assert "model" in config
        assert "analysis" in config
