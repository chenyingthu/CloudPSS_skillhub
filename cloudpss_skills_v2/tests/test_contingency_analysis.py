import pytest
from cloudpss_skills_v2.poweranalysis.contingency_analysis import ContingencyAnalysis


class TestContingencyAnalysis:
    @pytest.fixture
    def instance(self):
        return ContingencyAnalysis()

    def test_import(self):
        assert ContingencyAnalysis is not None

    def test_class_attributes(self, instance):
        assert hasattr(instance, "name") or hasattr(instance, "run")

    def test_config_schema(self, instance):
        schema = instance.config_schema
        assert isinstance(schema, dict)
        assert "properties" in schema

    def test_get_default_config(self, instance):
        config = instance.get_default_config()
        assert isinstance(config, dict)
