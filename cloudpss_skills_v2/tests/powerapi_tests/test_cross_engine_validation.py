"""Tests for cross-engine validation in powerapi."""
import pytest
from cloudpss_skills_v2.powerapi import EngineAdapter, EngineConfig, SimulationResult


class TestCrossEngineValidation:

    def test_engine_config_creation(self):
        config = EngineConfig(engine_name="test")
        assert config.engine_name == "test"

    def test_simulation_result_creation(self):
        result = SimulationResult(job_id="test-1")
        assert result.job_id == "test-1"
