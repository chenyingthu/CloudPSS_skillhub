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

    def test_validate_rejects_scenario_without_measurements(self, instance):
        valid, errors = instance.validate(
            {
                "model": {"rid": "case14"},
                "scenarios": {"baseline": {"enabled": True}},
            }
        )

        assert not valid
        assert errors == [
            "scenarios.baseline requires voltage_deviation or prefault/minimum voltage measurements"
        ]

    def test_run_uses_voltage_measurements_for_deviation(self, instance):
        result = instance.run(
            {
                "model": {"rid": "case14"},
                "scenarios": {
                    "baseline": {
                        "prefault_voltage_pu": 1.0,
                        "minimum_voltage_pu": 0.7,
                        "clearing_time": 0.1,
                    },
                    "delayed_clear": {
                        "prefault_voltage_pu": 1.0,
                        "minimum_voltage_pu": 0.5,
                        "clearing_time": 0.2,
                    },
                    "mild_fault": {
                        "prefault_voltage_pu": 1.0,
                        "minimum_voltage_pu": 0.85,
                        "clearing_time": 0.08,
                    },
                },
            }
        )

        assert result.is_success
        assert result.data["scenarios"]["baseline"]["voltage_deviation"] == pytest.approx(0.3)
        assert result.data["scenarios"]["baseline"]["data_source"] == "voltage_measurements"
        assert result.data["comparison"]["worst_scenario"] == "delayed_clear"
