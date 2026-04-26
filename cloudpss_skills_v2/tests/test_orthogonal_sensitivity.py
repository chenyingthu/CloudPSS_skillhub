import pytest
from cloudpss_skills_v2.poweranalysis.orthogonal_sensitivity import OrthogonalSensitivityAnalysis


class TestOrthogonalSensitivityAnalysis:
    @pytest.fixture
    def instance(self):
        return OrthogonalSensitivityAnalysis()

    def test_import(self):
        assert OrthogonalSensitivityAnalysis is not None

    def test_class_attributes(self, instance):
        assert hasattr(instance, "name") or hasattr(instance, "run")

    def test_config_schema(self, instance):
        schema = instance.config_schema
        assert isinstance(schema, dict)
        assert "properties" in schema
        assert {"model", "parameters", "target"} <= set(schema["properties"])

    def test_get_default_config(self, instance):
        config = instance.get_default_config()
        assert isinstance(config, dict)
        valid, errors = instance.validate(config)
        assert valid, errors
        assert config["model"]["rid"] == "case14"
        assert len(config["parameters"]) == 2
        assert config["target"]["metric"] == "voltage"
