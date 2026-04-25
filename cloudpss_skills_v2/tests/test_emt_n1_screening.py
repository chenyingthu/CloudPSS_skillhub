import pytest
from types import SimpleNamespace

from cloudpss_skills_v2.core.skill_result import SkillStatus
from cloudpss_skills_v2.poweranalysis.emt_n1_screening import EmtN1ScreeningAnalysis


class _FakeHandle:
    def __init__(self):
        self.removed = []
        self.model_id = "working-model"

    def clone(self):
        clone = _FakeHandle()
        clone.removed = self.removed
        return clone

    def remove_component(self, component_key):
        self.removed.append(component_key)
        return True


class TestEmtN1ScreeningAnalysis:
    def test_build_fault_config_defaults_actual_trip_to_true(self):
        instance = EmtN1ScreeningAnalysis()
        fault_config = instance._build_fault_config({"branch": "line_1"})
        assert fault_config["branch"] == "line_1"
        assert fault_config["actual_trip"] is True

    def test_build_fault_config_preserves_explicit_actual_trip(self):
        instance = EmtN1ScreeningAnalysis()
        fault_config = instance._build_fault_config(
            {"branch": "line_1", "actual_trip": False, "fault": {"type": "3ph"}}
        )
        assert fault_config == {"type": "3ph", "branch": "line_1", "actual_trip": False}

    def test_run_executes_actual_trip_and_emt_simulation(self, monkeypatch):
        instance = EmtN1ScreeningAnalysis()
        handle = _FakeHandle()
        pf_calls = []
        emt_calls = []

        pf_api = SimpleNamespace(
            adapter=SimpleNamespace(engine_name="fake_pf"),
            get_model_handle=lambda model_rid: handle,
            run_power_flow=lambda **kwargs: (
                pf_calls.append(kwargs)
                or SimpleNamespace(is_success=True, data={"max_voltage": 0.9})
            ),
        )
        emt_api = SimpleNamespace(
            adapter=SimpleNamespace(engine_name="fake_emt"),
            run_emt=lambda **kwargs: (
                emt_calls.append(kwargs)
                or SimpleNamespace(is_success=True, data={"plots": []})
            ),
        )

        monkeypatch.setattr(
            "cloudpss_skills_v2.poweranalysis.emt_n1_screening.Engine.create_powerflow_for_skill",
            lambda engine="cloudpss", **kwargs: pf_api,
        )
        monkeypatch.setattr(
            "cloudpss_skills_v2.poweranalysis.emt_n1_screening.Engine.create_emt_for_skill",
            lambda engine="cloudpss", **kwargs: emt_api,
        )

        result = instance.run(
            {
                "model": {"rid": "model/test", "source": "cloud"},
                "auth": {"token": "token"},
                "contingencies": [{"branch": "line_1"}],
                "simulation": {"duration": 1.5, "sampling_freq": 1000},
            }
        )

        assert result.status == SkillStatus.SUCCESS
        assert handle.removed == ["line_1"]
        assert len(pf_calls) == 2
        assert len(emt_calls) == 1
        assert emt_calls[0]["model_id"] is not None
        assert emt_calls[0]["fault_config"]["actual_trip"] is True
        assert result.data["results"][0]["actual_trip"] is True
        assert result.data["results"][0]["emt_success"] is True

    def test_run_skips_topology_trip_when_actual_trip_disabled(self, monkeypatch):
        instance = EmtN1ScreeningAnalysis()
        handle = _FakeHandle()

        pf_api = SimpleNamespace(
            adapter=SimpleNamespace(engine_name="fake_pf"),
            get_model_handle=lambda model_rid: handle,
            run_power_flow=lambda **kwargs: SimpleNamespace(
                is_success=True, data={"max_voltage": 1.0}
            ),
        )
        emt_api = SimpleNamespace(
            adapter=SimpleNamespace(engine_name="fake_emt"),
            run_emt=lambda **kwargs: SimpleNamespace(is_success=True, data={"plots": []}),
        )

        monkeypatch.setattr(
            "cloudpss_skills_v2.poweranalysis.emt_n1_screening.Engine.create_powerflow_for_skill",
            lambda engine="cloudpss", **kwargs: pf_api,
        )
        monkeypatch.setattr(
            "cloudpss_skills_v2.poweranalysis.emt_n1_screening.Engine.create_emt_for_skill",
            lambda engine="cloudpss", **kwargs: emt_api,
        )

        result = instance.run(
            {
                "model": {"rid": "model/test"},
                "contingencies": [{"branch": "line_1", "actual_trip": False}],
            }
        )

        assert result.status == SkillStatus.SUCCESS
        assert handle.removed == []
        assert result.data["results"][0]["actual_trip"] is False

    def test_validate_empty_config(self):
        instance = EmtN1ScreeningAnalysis()
        valid, errors = instance.validate({})
        assert valid is False
        assert errors == ["config is required"]
