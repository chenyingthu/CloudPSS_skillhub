import pytest
from cloudpss_skills_v2.poweranalysis.fault_clearing_scan import (
    FaultClearingScanAnalysis,
)


class TestFaultClearingScanAnalysis:
    def test_import(self):
        assert FaultClearingScanAnalysis is not None

    def test_instantiation(self):
        instance = FaultClearingScanAnalysis()
        assert instance is not None

    def test_has_name_attribute(self):
        instance = FaultClearingScanAnalysis()
        assert instance.name == "fault_clearing_scan"

    def test_has_config_schema(self):
        instance = FaultClearingScanAnalysis()
        schema = instance.config_schema
        assert schema is not None

    def test_validate_empty_config(self):
        instance = FaultClearingScanAnalysis()
        valid, errors = instance.validate({})
        assert valid is False

    def test_validate_missing_rid(self):
        instance = FaultClearingScanAnalysis()
        config = {"model": {}}
        valid, errors = instance.validate(config)
        assert valid is False

    def test_validate_valid_config(self):
        instance = FaultClearingScanAnalysis()
        config = {
            "model": {"rid": "test"},
            "stability_results": [{"clearing_time": 0.1, "stable": True}],
        }
        valid, errors = instance.validate(config)
        assert valid is True

    def test_requires_explicit_stability_results(self):
        instance = FaultClearingScanAnalysis()
        valid, errors = instance.validate({"model": {"rid": "test"}})
        assert valid is False
        assert any("stability_results" in error for error in errors)

    def test_compute_scan_results(self):
        instance = FaultClearingScanAnalysis()
        stability_results = [
            {"clearing_time": 0.05, "stable": True},
            {"clearing_time": 0.1, "stable": True},
            {"clearing_time": 0.15, "stable": False},
        ]
        results = instance._compute_scan_results(stability_results, "bus1", "3ph")
        assert len(results) == 3
        assert results[0]["clearing_time"] == 0.05

    def test_compute_scan_results_stability_check(self):
        instance = FaultClearingScanAnalysis()
        stability_results = [
            {"clearing_time": 0.05, "stable": True, "critical": False},
            {"clearing_time": 0.1, "stable": True, "critical": True},
            {"clearing_time": 0.15, "stable": False},
        ]
        results = instance._compute_scan_results(stability_results, "bus1", "3ph")
        assert results[0]["stable"] is True
        assert results[1]["critical"] is True
        assert results[2]["stable"] is False

    def test_check_monotonic_degradation(self):
        instance = FaultClearingScanAnalysis()
        results = [
            {"clearing_time": 0.05, "stable": True},
            {"clearing_time": 0.1, "stable": True},
            {"clearing_time": 0.15, "stable": False},
        ]
        monotonic = instance._check_monotonic_degradation(results)
        assert monotonic is True

    def test_check_monotonic_no_degradation(self):
        instance = FaultClearingScanAnalysis()
        results = [
            {"clearing_time": 0.05, "stable": True},
            {"clearing_time": 0.1, "stable": True},
            {"clearing_time": 0.15, "stable": True},
        ]
        monotonic = instance._check_monotonic_degradation(results)
        assert monotonic is False

    def test_run_returns_skill_result(self):
        instance = FaultClearingScanAnalysis()
        result = instance.run(
            {
                "model": {"rid": "test"},
                "stability_results": [{"clearing_time": 0.1, "stable": True}],
            }
        )
        assert result is not None
        assert hasattr(result, "skill_name")

    def test_run_with_invalid_config(self):
        instance = FaultClearingScanAnalysis()
        result = instance.run({})
        assert result.status.value == "failed" or result.status.name == "failed"

    def test_has_log_method(self):
        instance = FaultClearingScanAnalysis()
        assert hasattr(instance, "_log")
        assert callable(instance._log)
