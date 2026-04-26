"""Tests for cloudpss_skills_v2.poweranalysis.reactive_compensation_design."""
import pytest
from cloudpss_skills_v2.poweranalysis.reactive_compensation_design import ReactiveCompensationDesignAnalysis


class TestReactiveCompensationDesignAnalysis:

    def test_import(self):
        """module and class can be imported."""
        assert ReactiveCompensationDesignAnalysis is not None

    def test_instantiation(self):
        """class can be instantiated."""
        instance = ReactiveCompensationDesignAnalysis()
        assert instance is not None

    def test_has_name_attribute(self):
        """instance has expected attributes."""
        instance = ReactiveCompensationDesignAnalysis()
        assert hasattr(instance, 'name') or hasattr(instance, 'run')
