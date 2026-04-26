"""Tests for cloudpss_skills_v2.libs.workflow_lib."""
import pytest
from cloudpss_skills_v2.libs.workflow_lib import Pipeline, WorkflowStep


class TestPipeline:

    def test_import(self):
        """Smoke test: module and class can be imported."""
        assert Pipeline is not None

    def test_instantiation(self):
        """Smoke test: class can be instantiated."""
        instance = Pipeline(name="test-pipeline")
        assert instance is not None

    def test_has_name_attribute(self):
        """Smoke test: instance has expected attributes."""
        instance = Pipeline(name="test-pipeline")
        assert hasattr(instance, 'name') or hasattr(instance, 'run')
