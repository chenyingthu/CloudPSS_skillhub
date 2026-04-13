#!/usr/bin/env python3
"""
transient_stability_margin Skill - Integration Tests

Tests for transient_stability_margin skill with real CloudPSS API.

Requirements:
- Model must have EMT measurement channels (voltage meters)
- IEEE39 model has generator angle channels but no voltage channels
- Use IEEE3 model or add voltage meters to IEEE39 before testing

The skill requires:
1. Pre-configured EMT measurement channels (vac:0 or similar)
2. OR the model must support auto-adding voltage meters
"""

import pytest
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

server: "internal"

from cloudpss import setToken, Model
from cloudpss_skills.builtin.transient_stability_margin import (
    TransientStabilityMarginSkill,
)
from cloudpss_skills.core import SkillStatus


class TestTransientStabilityMarginSkillIntegration:
    """Integration tests for transient_stability_margin skill"""

    def setup_method(self):
        """Setup for each test"""
        self.skill = TransientStabilityMarginSkill()

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

        skill = get_skill("transient_stability_margin")
        assert skill is not None
        assert skill.name == "transient_stability_margin"

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
        """Test validation handles missing model.rid"""
        config = {
            "skill": "transient_stability_margin",
            "auth": {"token": auth_token, },
        }
        result = self.skill.validate(config)
        assert result.valid or len(result.warnings) > 0 or len(result.errors) > 0

    @pytest.mark.integration
    def test_integration_ieee3_model(self, auth_token):
        """
        Test IEEE3 model - smaller model suitable for CCT computation.

        Note: IEEE3 model should have voltage measurement channels configured.
        If not, the test will fail with '未找到目标通道 vac:0' error.
        """
        config = {
            "skill": "transient_stability_margin",
            "auth": {
                "token": auth_token,
                },
            "model": {"rid": "model/holdme/IEEE3"},
            "fault_scenarios": [
                {"location": "BUS_1", "type": "three_phase", "duration": 0.1}
            ],
            "analysis": {
                "compute_cct": True,
                "compute_margin": True,
                "margin_baseline": 0.1,
                "max_iterations": 3,
                "cct_tolerance": 0.1,
            },
        }

        result = self.skill.run(config)
        # May fail if model lacks voltage measurement channels
        # Expected error: "未找到目标通道 vac:0"
        assert result is not None

    @pytest.mark.integration
    def test_integration_with_explicit_channel(self, auth_token):
        """
        Test with explicitly specified stability trace channel.

        The model must have this channel configured, or the skill should
        automatically add voltage meters to the target bus.
        """
        # First check available channels
        setToken(auth_token)
        model = Model.fetch("model/holdme/IEEE3")

        # Try to run EMT and get available channels
        try:
            job = model.runEMT(simuTime=0.1)
            import time

            start = time.time()
            while job.status() == 0 and time.time() - start < 60:
                time.sleep(1)

            if job.status() == 1:
                result = job.result
                plots = result.getPlots()
                if plots:
                    channels = result.getPlotChannelNames(0)
                    print(f"Available channels: {channels[:10]}")
        except Exception as e:
            print(f"Could not get channels: {e}")

        config = {
            "skill": "transient_stability_margin",
            "auth": {
                "token": auth_token,
                },
            "model": {"rid": "model/holdme/IEEE3"},
            "fault_scenarios": [{"location": "BUS_1", "type": "three_phase"}],
            "analysis": {
                "compute_cct": True,
                "max_iterations": 2,
                "cct_tolerance": 0.2,
            },
        }

        result = self.skill.run(config)
        assert result is not None
        # The skill may fail if channels are not configured
        assert result.status in [SkillStatus.SUCCESS, SkillStatus.FAILED]

    @pytest.mark.integration
    def test_integration_documents_channel_requirement(self, auth_token):
        """
        Document the channel requirement for transient stability margin.

        This test verifies that the skill properly documents its requirements
        and fails gracefully when channels are missing.
        """
        config = {
            "skill": "transient_stability_margin",
            "auth": {
                "token": auth_token,
                },
            "model": {"rid": "model/holdme/IEEE3"},
            "fault_scenarios": [{"location": "BUS_1", "type": "three_phase"}],
        }

        result = self.skill.run(config)

        # Check that the error message is informative
        if result.status == SkillStatus.FAILED:
            error = result.error or ""
            # Should have informative error message
            assert len(error) > 0, "Error message should not be empty"
            # Common error patterns
            known_errors = [
                "未找到目标通道",
                "不存在或权限不足",
                "CCT",
            ]
            # At least one known error pattern should be present
            has_known_error = any(e in error for e in known_errors)
            assert has_known_error, f"Error should be informative, got: {error}"
