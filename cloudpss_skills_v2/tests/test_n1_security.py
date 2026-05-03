"""Tests for cloudpss_skills_v2.poweranalysis.n1_security."""

from types import SimpleNamespace

from cloudpss_skills_v2.core.skill_result import SkillStatus
from cloudpss_skills_v2.core.system_model import Bus, Branch, PowerSystemModel
from cloudpss_skills_v2.libs.data_lib import SeverityLevel
from cloudpss_skills_v2.poweranalysis.n1_security import N1SecurityAnalysis


class _FakeHandle:
    def __init__(self):
        self.removed = []

    def get_components_by_type(self, component_type):
        if component_type == "branch":
            return [SimpleNamespace(key="line_1", name="Line 1")]
        return []

    def clone(self):
        clone = _FakeHandle()
        clone.removed = self.removed
        return clone

    def remove_component(self, component_key):
        self.removed.append(component_key)
        return True


class TestN1SecurityAnalysis:
    def test_collects_voltage_and_thermal_violations_without_overwriting(self, monkeypatch):
        skill = N1SecurityAnalysis()

        # Create unified model for testing
        test_model = PowerSystemModel(
            buses=[
                Bus(bus_id=0, name="Bus 1", base_kv=230.0, bus_type="PQ",
                    v_magnitude_pu=0.92, vm_min_pu=0.95, vm_max_pu=1.05),
                Bus(bus_id=1, name="Bus 2", base_kv=230.0, bus_type="SLACK",
                    v_magnitude_pu=1.0, vm_min_pu=0.95, vm_max_pu=1.05),
            ],
            branches=[
                Branch(from_bus=0, to_bus=1, name="Line 1",
                       rate_a_mva=100.0, loading_percent=135.0, in_service=True),
            ],
            base_mva=100.0,
            name="Test Model"
        )

        handle = _FakeHandle()
        fake_api = SimpleNamespace(
            adapter=SimpleNamespace(engine_name="fake_pf"),
            get_model_handle=lambda model_rid: handle,
            get_system_model=lambda job_id: test_model,
            run_power_flow=lambda **kwargs: SimpleNamespace(
                is_success=True,
                job_id="test_job_1",
                data={
                    "buses": [{"name": "Bus 1", "voltage_pu": 0.92}],
                    "branches": [{"name": "Line 1", "loading_pct": 135.0}],
                },
            ),
        )

        monkeypatch.setattr(
            "cloudpss_skills_v2.poweranalysis.n1_security.Engine.create_powerflow_for_skill",
            lambda engine="cloudpss", **kwargs: fake_api,
        )
        monkeypatch.setattr(
            skill,
            "_save_output",
            lambda result_data, output_config: None,
        )

        result = skill.run(
            {
                "model": {"rid": "model/test", "source": "cloud"},
                "auth": {"token": "token"},
                "analysis": {"check_voltage": True, "check_thermal": True},
                "output": {"timestamp": False},
            }
        )

        assert result.status == SkillStatus.FAILED
        contingencies = result.data["_typed"]["contingencies"]
        assert len(contingencies) == 1
        violation_types = [v["violation_type"] for v in contingencies[0]["violations"]]
        assert violation_types == ["voltage", "thermal"]
        assert len(result.data["_typed"]["violations"]) == 2

    def test_validate_requires_model_rid_and_auth(self):
        skill = N1SecurityAnalysis()
        valid, errors = skill.validate({})
        assert not valid
        assert "必须提供 model.rid" in errors
        assert "必须提供 auth.token 或 auth.token_file" in errors

    def test_validate_local_pandapower_does_not_require_auth(self):
        skill = N1SecurityAnalysis()
        valid, errors = skill.validate(
            {"engine": "pandapower", "model": {"rid": "case14", "source": "local"}}
        )
        assert valid, errors

    def test_summarize_violations_returns_critical_for_convergence(self):
        skill = N1SecurityAnalysis()
        summary = skill._summarize_violations(
            [{"type": "convergence", "message": "did not converge"}]
        )
        assert summary is not None
        assert summary["severity"] == SeverityLevel.CRITICAL.value
