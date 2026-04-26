"""Tests for cloudpss_skills_v2.poweranalysis.vsi_weak_bus."""

import pytest
from cloudpss_skills_v2.poweranalysis.vsi_weak_bus import VSIWeakBusAnalysis


class TestVSIWeakBusAnalysis:
    @pytest.fixture
    def instance(self):
        return VSIWeakBusAnalysis()

    def test_import(self):
        assert VSIWeakBusAnalysis is not None

    def test_class_attributes(self, instance):
        assert hasattr(instance, "name") or hasattr(instance, "run")

    def test_config_schema(self, instance):
        schema = instance.config_schema
        assert isinstance(schema, dict)
        assert "properties" in schema

    def test_get_default_config(self, instance):
        if hasattr(instance, "get_default_config"):
            config = instance.get_default_config()
            assert isinstance(config, dict)
