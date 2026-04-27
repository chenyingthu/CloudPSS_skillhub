"""Tests for cloudpss_skills_v2.poweranalysis.power_quality_analysis."""

import pytest
from cloudpss_skills_v2.poweranalysis.power_quality_analysis import PowerQualityAnalysisAnalysis


class TestPowerQualityAnalysisAnalysis:

    def test_import(self):
        """module and class can be imported."""
        assert PowerQualityAnalysisAnalysis is not None

    def test_instantiation(self):
        """class can be instantiated."""
        instance = PowerQualityAnalysisAnalysis()
        assert instance is not None

    def test_has_name_attribute(self):
        """instance has expected attributes."""
        instance = PowerQualityAnalysisAnalysis()
        assert hasattr(instance, "name") or hasattr(instance, "run")

    def test_requires_explicit_measurements(self):
        instance = PowerQualityAnalysisAnalysis()
        valid, errors = instance.validate({"model": {"rid": "case14"}})
        assert valid is False
        assert any("measurements" in error for error in errors)

    def test_accepts_explicit_harmonic_and_phase_measurements(self):
        instance = PowerQualityAnalysisAnalysis()
        valid, errors = instance.validate(
            {
                "model": {"rid": "case14"},
                "measurements": {
                    "harmonic_voltages": {"5": 0.03, "7": 0.02},
                    "phase_voltages_pu": [1.0, 0.98, 1.01],
                },
            }
        )
        assert valid is True
        assert errors == []

    def test_success_output_declares_measurement_limits(self, monkeypatch):
        class FakeAdapter:
            engine_name = "fake"

        class FakePowerFlow:
            adapter = FakeAdapter()

            def get_model_handle(self, model_rid):
                return object()

            def run_power_flow(self, model_handle):
                from cloudpss_skills_v2.powerapi.base import (
                    SimulationResult,
                    SimulationStatus,
                )

                return SimulationResult(
                    status=SimulationStatus.COMPLETED,
                    data={"bus_results": []},
                )

        monkeypatch.setattr(
            "cloudpss_skills_v2.poweranalysis.power_quality_analysis.Engine.create_powerflow_for_skill",
            lambda **kwargs: FakePowerFlow(),
        )

        result = PowerQualityAnalysisAnalysis().run(
            {
                "model": {"rid": "case14"},
                "measurements": {
                    "harmonic_voltages": {"5": 0.03, "7": 0.04},
                    "phase_voltages_pu": [1.0, 0.99, 1.01],
                },
            }
        )

        assert result.is_success
        assert result.data["data_source"] == "measurements"
        assert result.data["confidence_level"] == "measurement_derived"
        assert result.data["limitations"]
