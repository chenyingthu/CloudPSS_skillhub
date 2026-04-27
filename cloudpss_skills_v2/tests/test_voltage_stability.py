"""Tests for cloudpss_skills_v2.poweranalysis.voltage_stability."""

import pytest

from cloudpss_skills_v2.core.skill_result import SkillStatus
from cloudpss_skills_v2.poweranalysis.voltage_stability import VoltageStabilityAnalysis


class TestVoltageStabilityAnalysis:

    def test_import(self):
        """Module and class can be imported."""
        assert VoltageStabilityAnalysis is not None

    def test_instantiation(self):
        """Class can be instantiated."""
        instance = VoltageStabilityAnalysis()
        assert instance is not None

    def test_has_name_attribute(self):
        """Instance has expected attributes."""
        instance = VoltageStabilityAnalysis()
        assert hasattr(instance, "name") or hasattr(instance, "run")

    def test_pandapower_scan_returns_ordered_convergence_and_pv_curve(self, tmp_path):
        instance = VoltageStabilityAnalysis()
        result = instance.run(
            {
                "engine": "pandapower",
                "model": {"rid": "case14", "source": "local"},
                "scan": {"load_scaling": [1.0, 1.01], "scale_generation": False},
                "monitoring": {"buses": ["0", "1"], "collapse_threshold": 0.7},
                "output": {
                    "format": "json",
                    "path": str(tmp_path),
                    "generate_report": False,
                    "export_pv_curve": False,
                },
            }
        )

        assert result.status == SkillStatus.SUCCESS
        assert result.error is None
        assert result.data["total_cases"] == 2
        assert result.data["converged_cases"] == 2
        assert result.data["collapse_point"] is None
        assert result.data["max_loadability"] == 1.01
        assert result.metrics["converged"] == 2

        scales = [case["scale"] for case in result.data["results"]]
        assert scales == [1.0, 1.01]
        assert all(case["converged"] for case in result.data["results"])
        assert all(set(case["voltages"]) == {"0", "1"} for case in result.data["results"])
        assert all(
            case["min_voltage"] > result.data["collapse_threshold"]
            for case in result.data["results"]
        )

        pv_points = result.data["pv_curve"]
        assert len(pv_points) == 4
        assert {(p["bus"], p["scale"]) for p in pv_points} == {
            ("0", 1.0),
            ("1", 1.0),
            ("0", 1.01),
            ("1", 1.01),
        }

    def test_all_failed_scan_returns_failed_status(self, monkeypatch, tmp_path):
        instance = VoltageStabilityAnalysis()

        class FailingApi:
            adapter = type("Adapter", (), {"engine_name": "fake_pf"})()

            def get_model_handle(self, model_rid):
                return type(
                    "Handle",
                    (),
                    {
                        "get_components_by_type": lambda self, component_type: [],
                        "clone": lambda self: self,
                    },
                )()

            def run_power_flow(self, **kwargs):
                return type(
                    "Result",
                    (),
                    {"is_success": False, "data": {}, "errors": ["no convergence"]},
                )()

        monkeypatch.setattr(
            "cloudpss_skills_v2.poweranalysis.voltage_stability.Engine.create_powerflow",
            lambda engine="cloudpss", config=None: FailingApi(),
        )

        result = instance.run(
            {
                "engine": "cloudpss",
                "auth": {"token": "token"},
                "model": {"rid": "model/test", "source": "cloud"},
                "scan": {"load_scaling": [1.0, 1.2]},
                "monitoring": {"buses": ["Bus 1"], "collapse_threshold": 0.7},
                "output": {
                    "format": "json",
                    "path": str(tmp_path),
                    "generate_report": False,
                    "export_pv_curve": False,
                },
            }
        )

        assert result.status == SkillStatus.FAILED
        assert result.error == "No voltage stability scan cases converged"
        assert result.data["converged_cases"] == 0
        assert all(not case["converged"] for case in result.data["results"])
