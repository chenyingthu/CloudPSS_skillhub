import pytest
from cloudpss_skills_v2.poweranalysis.n2_security import N2SecurityAnalysis


class TestN2SecurityAnalysis:
    @pytest.fixture
    def instance(self):
        return N2SecurityAnalysis()

    def test_import(self):
        assert N2SecurityAnalysis is not None

    def test_class_attributes(self, instance):
        assert hasattr(instance, "name") or hasattr(instance, "run")

    def test_config_schema(self, instance):
        if hasattr(instance, "config_schema"):
            schema = instance.config_schema
            assert isinstance(schema, dict)
            assert "properties" in schema
        else:
            pytest.skip("config_schema not available on this skill instance")

    def test_get_default_config(self, instance):
        if hasattr(instance, "get_default_config"):
            config = instance.get_default_config()
            assert isinstance(config, dict)
        else:
            pytest.skip("get_default_config not available on this skill instance")
