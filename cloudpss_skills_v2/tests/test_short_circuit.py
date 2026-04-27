import pytest

from cloudpss_skills_v2.core.skill_result import SkillStatus
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

    def test_adapter_bus_results_preserve_nonzero_peak_when_ip_missing(self, instance):
        analysis = instance._build_analysis_from_adapter_data(
            {
                "bus_results": [
                    {
                        "bus": "Bus 1",
                        "ikss_ka": 10.0,
                        "ip_ka": 0.0,
                        "ith_ka": 8.0,
                        "v_pu": 0.0,
                    }
                ]
            }
        )

        assert analysis["Bus 1"]["current_ka"] == 10.0
        assert analysis["Bus 1"]["steady_current"] == 10.0
        assert analysis["Bus 1"]["peak_current"] == 10.0
        assert analysis["Bus 1"]["thermal_current"] == 8.0

    def test_pandapower_validation_does_not_require_auth(self, instance):
        valid, errors = instance.validate(
            {
                "engine": "pandapower",
                "model": {"rid": "case14", "source": "local"},
                "fault": {"location": "0", "type": "3ph"},
            }
        )

        assert valid
        assert errors == []

    def test_pandapower_short_circuit_has_positive_currents_and_capacity(self, instance, tmp_path):
        result = instance.run(
            {
                "engine": "pandapower",
                "model": {"rid": "case14", "source": "local"},
                "fault": {"location": "0", "type": "3ph"},
                "calculation": {"base_voltage": 135.0, "base_capacity": 100},
                "output": {
                    "format": "json",
                    "path": str(tmp_path),
                    "generate_report": False,
                },
            }
        )

        assert result.status == SkillStatus.SUCCESS
        assert result.metrics["channels_analyzed"] == 14
        analysis = result.data["analysis"]
        assert len(analysis) == 14
        assert result.data["short_circuit_mva"].keys() == analysis.keys()

        for channel, values in analysis.items():
            assert values["current_ka"] > 0
            assert values["steady_current"] == values["current_ka"]
            assert values["peak_current"] >= values["steady_current"]
            capacity = result.data["short_circuit_mva"][channel]
            assert capacity["steady_current_ka"] == values["steady_current"]
            assert capacity["short_circuit_mva"] > 0
