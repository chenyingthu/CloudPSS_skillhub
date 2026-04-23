import pytest
import numpy as np
from cloudpss_skills_v2.poweranalysis.disturbance_severity import (
    DisturbanceSeverityAnalysis,
)


class TestDisturbanceSeverityAnalysis:
    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_import(self):
        assert DisturbanceSeverityAnalysis is not None

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_instantiation(self):
        instance = DisturbanceSeverityAnalysis()
        assert instance is not None

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_has_name_attribute(self):
        instance = DisturbanceSeverityAnalysis()
        assert instance.name == "disturbance_severity"

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_has_config_schema(self):
        instance = DisturbanceSeverityAnalysis()
        schema = instance.config_schema
        assert schema is not None

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_validate_empty_config(self):
        instance = DisturbanceSeverityAnalysis()
        valid, errors = instance.validate({})
        assert valid is False

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_validate_missing_rid(self):
        instance = DisturbanceSeverityAnalysis()
        config = {"model": {}}
        valid, errors = instance.validate(config)
        assert valid is False

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_validate_valid_config(self):
        instance = DisturbanceSeverityAnalysis()
        config = {"model": {"rid": "test"}}
        valid, errors = instance.validate(config)
        assert valid is True

    def test_calculate_dv_with_voltage_dip(self):
        instance = DisturbanceSeverityAnalysis()
        voltage = np.array([1.0, 1.0, 1.0, 0.8, 0.9, 1.0, 1.0])
        time = np.array([0, 1, 2, 3, 4, 5, 6])
        result = instance._calculate_dv(voltage, time, 3.0, 1.0)
        assert result["dv_down"] > 0.0

    def test_calculate_dv_with_voltage_rise(self):
        instance = DisturbanceSeverityAnalysis()
        voltage = np.array([1.0, 1.0, 1.0, 1.2, 1.1, 1.0, 1.0])
        time = np.array([0, 1, 2, 3, 4, 5, 6])
        result = instance._calculate_dv(voltage, time, 3.0, 1.0)
        assert result["dv_up"] > 0.0

    def test_calculate_dv_steady(self):
        instance = DisturbanceSeverityAnalysis()
        voltage = np.array([1.0, 1.0, 1.0, 1.0, 1.0])
        time = np.array([0, 1, 2, 3, 4])
        result = instance._calculate_dv(voltage, time, 10.0, 1.0)
        assert result["dv_up"] == 0.0
        assert result["dv_down"] == 0.0

    def test_calculate_si(self):
        instance = DisturbanceSeverityAnalysis()
        voltage = np.array([1.0, 1.0, 0.5, 0.6, 1.0])
        time = np.array([0, 1, 2, 3, 4])
        si = instance._calculate_si(voltage, time, 2.0, 0.0, 1.0)
        assert si >= 0.0

    def test_calculate_si_no_deviation(self):
        instance = DisturbanceSeverityAnalysis()
        voltage = np.array([1.0, 1.0, 1.0, 1.0, 1.0])
        time = np.array([0, 1, 2, 3, 4])
        si = instance._calculate_si(voltage, time, 2.0, 0.0, 1.0)
        assert si == 0.0

    def test_assess_severity_severe(self):
        instance = DisturbanceSeverityAnalysis()
        severity = instance._assess_severity(0.3, 0.2, 15.0)
        assert severity == "severe"

    def test_assess_severity_moderate(self):
        instance = DisturbanceSeverityAnalysis()
        severity = instance._assess_severity(0.15, 0.1, 6.0)
        assert severity == "moderate"

    def test_assess_severity_normal(self):
        instance = DisturbanceSeverityAnalysis()
        severity = instance._assess_severity(0.05, 0.02, 2.0)
        assert severity == "normal"

    def test_identify_weak_points(self):
        instance = DisturbanceSeverityAnalysis()
        results = [
            {"bus": "B1", "severity": "severe"},
            {"bus": "B2", "severity": "moderate"},
            {"bus": "B3", "severity": "normal"},
        ]
        weak = instance._identify_weak_points(results)
        assert len(weak) == 2

    def test_identify_weak_points_none(self):
        instance = DisturbanceSeverityAnalysis()
        results = [
            {"bus": "B1", "severity": "normal"},
            {"bus": "B2", "severity": "normal"},
        ]
        weak = instance._identify_weak_points(results)
        assert len(weak) == 0

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_run_returns_skill_result(self):
        instance = DisturbanceSeverityAnalysis()
        result = instance.run({"model": {"rid": "test"}})
        assert result is not None
        assert hasattr(result, "skill_name")

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_run_with_invalid_config(self):
        instance = DisturbanceSeverityAnalysis()
        result = instance.run({})
        assert result.status.value == "failed" or result.status.name == "failed"

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_has_log_method(self):
        instance = DisturbanceSeverityAnalysis()
        assert hasattr(instance, "_log")
        assert callable(instance._log)
