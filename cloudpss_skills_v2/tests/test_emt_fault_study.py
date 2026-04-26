import pytest
from cloudpss_skills_v2.poweranalysis.emt_fault_study import EmtFaultStudyAnalysis


class TestEmtFaultStudyAnalysis:
    @pytest.fixture
    def instance(self):
        return EmtFaultStudyAnalysis()

    def test_import(self):
        assert EmtFaultStudyAnalysis is not None

    def test_class_attributes(self, instance):
        assert hasattr(instance, "name") or hasattr(instance, "run")

    def test_config_schema(self, instance):
        schema = instance.config_schema
        assert isinstance(schema, dict)
        assert "properties" in schema
        assert "model" in schema["properties"]

    def test_get_default_config(self, instance):
        config = instance.get_default_config()
        assert isinstance(config, dict)
        valid, errors = instance.validate(config)
        assert valid, errors
        assert config["model"]["rid"] == "case14"
        assert set(config["scenarios"]) == {
            "baseline",
            "delayed_clear",
            "mild_fault",
        }
