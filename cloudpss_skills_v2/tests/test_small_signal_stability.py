import pytest
import numpy as np
from cloudpss_skills_v2.poweranalysis.small_signal_stability import (
    SmallSignalStabilityAnalysis,
)


class TestSmallSignalStabilityAnalysis:
    def test_import(self):
        assert SmallSignalStabilityAnalysis is not None

    def test_instantiation(self):
        instance = SmallSignalStabilityAnalysis()
        assert instance is not None

    def test_has_name_attribute(self):
        instance = SmallSignalStabilityAnalysis()
        assert instance.name == "small_signal_stability"

    def test_has_config_schema(self):
        instance = SmallSignalStabilityAnalysis()
        schema = instance.config_schema
        assert schema is not None

    def test_validate_empty_config(self):
        instance = SmallSignalStabilityAnalysis()
        valid, errors = instance.validate({})
        assert valid is False

    def test_validate_missing_rid(self):
        instance = SmallSignalStabilityAnalysis()
        config = {"model": {}}
        valid, errors = instance.validate(config)
        assert valid is False

    def test_validate_valid_config(self):
        instance = SmallSignalStabilityAnalysis()
        config = {"model": {"rid": "test"}}
        valid, errors = instance.validate(config)
        assert valid is True

    def test_eigenvalue_analysis_stable(self):
        instance = SmallSignalStabilityAnalysis()
        A = np.array([[-0.5, 0.0], [0.0, -0.3]])
        result = instance._eigenvalue_analysis(A)
        assert result["stable"] is True

    def test_eigenvalue_analysis_unstable(self):
        instance = SmallSignalStabilityAnalysis()
        A = np.array([[0.5, 0.0], [0.0, 0.3]])
        result = instance._eigenvalue_analysis(A)
        assert result["stable"] is False

    def test_eigenvalue_analysis_with_critical(self):
        instance = SmallSignalStabilityAnalysis()
        A = np.array([[-0.5, 0.0], [0.0, -0.3]])
        result = instance._eigenvalue_analysis(A, damping_threshold=0.05)
        assert "critical_modes" in result

    def test_eigenvalue_analysis_empty(self):
        instance = SmallSignalStabilityAnalysis()
        A = np.array([])
        result = instance._eigenvalue_analysis(A)
        assert result["stable"] is False

    def test_eigenvalue_returns_modes(self):
        instance = SmallSignalStabilityAnalysis()
        A = np.array([[-0.5, 0.1], [-0.1, -0.3]])
        result = instance._eigenvalue_analysis(A)
        assert "modes" in result
        assert len(result["modes"]) > 0

    def test_run_returns_skill_result(self):
        instance = SmallSignalStabilityAnalysis()
        result = instance.run({"model": {"rid": "test"}})
        assert result is not None
        assert hasattr(result, "skill_name")

    def test_run_with_invalid_config(self):
        instance = SmallSignalStabilityAnalysis()
        result = instance.run({})
        assert result.status.value == "failed" or result.status.name == "failed"

    def test_has_log_method(self):
        instance = SmallSignalStabilityAnalysis()
        assert hasattr(instance, "_log")
        assert callable(instance._log)
