"""Tests for cloudpss_skills_v2.tools.config_batch_runner."""
import pytest
from cloudpss_skills_v2.tools.config_batch_runner import ConfigBatchRunnerTool


class TestConfigBatchRunnerTool:

    def test_import(self):
        """Smoke test: module and class can be imported."""
        assert ConfigBatchRunnerTool is not None

    def test_instantiation(self):
        """Smoke test: class can be instantiated."""
        instance = ConfigBatchRunnerTool()
        assert instance is not None

    def test_has_name_attribute(self):
        """Smoke test: instance has expected attributes."""
        instance = ConfigBatchRunnerTool()
        assert hasattr(instance, 'name') or hasattr(instance, 'run')
