import pytest
from cloudpss_skills_v2.poweranalysis.short_circuit import ShortCircuitAnalysis


class TestShortCircuitAnalysis:
    @pytest.fixture
    def instance(self):
        return ShortCircuitAnalysis()

    def test_import(self):
        assert ShortCircuitAnalysis is not None

    def test_class_attributes(self, instance):
        assert hasattr(instance, "name") or hasattr(instance, "run")

    def test_config_schema(self, instance):
        schema = instance.config_schema
        assert isinstance(schema, dict)
        assert "properties" in schema

    def test_get_default_config(self, instance):
        config = instance.get_default_config()
        assert isinstance(config, dict)
