"""Tests for cloudpss_skills_v2.tools.model_parameter_extractor."""
import pytest
from cloudpss_skills_v2.tools.model_parameter_extractor import ModelParameterExtractorTool


class TestModelParameterExtractorTool:

    def test_import(self):
        """module and class can be imported."""
        assert ModelParameterExtractorTool is not None

    def test_instantiation(self):
        """class can be instantiated."""
        instance = ModelParameterExtractorTool()
        assert instance is not None

    def test_has_name_attribute(self):
        """instance has expected attributes."""
        instance = ModelParameterExtractorTool()
        assert hasattr(instance, 'name') or hasattr(instance, 'run')
