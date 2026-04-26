"""Tests for cloudpss_skills_v2.tools.config_batch_runner."""
import pytest
from cloudpss_skills_v2.tools.config_batch_runner import ConfigBatchRunnerTool


class TestConfigBatchRunnerTool:

    def test_import(self):
        """module and class can be imported."""
        assert ConfigBatchRunnerTool is not None

    def test_instantiation(self):
        """class can be instantiated."""
        instance = ConfigBatchRunnerTool()
        assert instance is not None

    def test_has_name_attribute(self):
        """instance has expected attributes."""
        instance = ConfigBatchRunnerTool()
        assert hasattr(instance, 'name') or hasattr(instance, 'run')
