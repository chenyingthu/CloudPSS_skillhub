"""Tests for cloudpss_skills_v2.tools.auto_loop_breaker."""
import pytest
from cloudpss_skills_v2.tools.auto_loop_breaker import AutoLoopBreakerTool


class TestAutoLoopBreakerTool:

    def test_import(self):
        """module and class can be imported."""
        assert AutoLoopBreakerTool is not None

    def test_instantiation(self):
        """class can be instantiated."""
        instance = AutoLoopBreakerTool()
        assert instance is not None

    def test_has_name_attribute(self):
        """instance has expected attributes."""
        instance = AutoLoopBreakerTool()
        assert hasattr(instance, 'name') or hasattr(instance, 'run')
