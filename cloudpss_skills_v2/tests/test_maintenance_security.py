import pytest
from cloudpss_skills_v2.poweranalysis.maintenance_security import MaintenanceSecurityAnalysis


class TestMaintenanceSecurityAnalysis:
    @pytest.fixture
    def instance(self):
        return MaintenanceSecurityAnalysis()

    def test_import(self):
        assert MaintenanceSecurityAnalysis is not None

    def test_class_attributes(self, instance):
        assert hasattr(instance, "name") or hasattr(instance, "run")

    def test_config_schema(self, instance):
        schema = instance.config_schema
        assert isinstance(schema, dict)
        assert "properties" in schema
        assert "maintenance" in schema["properties"]

    def test_get_default_config(self, instance):
        config = instance.get_default_config()
        assert isinstance(config, dict)
        valid, errors = instance.validate(config)
        assert valid, errors
        assert config["skill"] == instance.name
        assert config["engine"] == "pandapower"
        assert config["model"]["rid"] == "case14"
        assert config["maintenance"]["branch_id"] == "line:0"
