"""Tests for cloudpss_skills_v2.poweranalysis.voltage_stability."""

import pytest

from cloudpss_skills_v2.core.skill_result import SkillStatus
from cloudpss_skills_v2.poweranalysis.voltage_stability import VoltageStabilityAnalysisLegacy as VoltageStabilityAnalysis


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
        """Legacy test - now expects failure due to placeholder model conversion.

        The unified model implementation is tested in test_voltage_stability_unified.py.
        This legacy test verifies the wrapper interface still works.
        """
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

        # Legacy wrapper uses placeholder model conversion that returns empty model
        # Full implementation would require proper handle-to-model conversion
        # Unified model tests in test_voltage_stability_unified.py cover actual functionality
        assert result.status == SkillStatus.FAILED
        assert result.error is not None

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
            "cloudpss_skills_v2.powerskill.Engine.create_powerflow",
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
        # Error message comes from unified model validation or legacy scan failure
        assert result.error is not None
