import pytest
from cloudpss_skills_v2.poweranalysis.fault_clearing_scan import (
    FaultClearingScanAnalysis,
)


class TestFaultClearingScanAnalysis:
    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_import(self):
        assert FaultClearingScanAnalysis is not None

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_instantiation(self):
        instance = FaultClearingScanAnalysis()
        assert instance is not None

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_has_name_attribute(self):
        instance = FaultClearingScanAnalysis()
        assert instance.name == "fault_clearing_scan"

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_has_config_schema(self):
        instance = FaultClearingScanAnalysis()
        schema = instance.config_schema
        assert schema is not None

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_validate_empty_config(self):
        instance = FaultClearingScanAnalysis()
        valid, errors = instance.validate({})
        assert valid is False

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_validate_missing_rid(self):
        instance = FaultClearingScanAnalysis()
        config = {"model": {}}
        valid, errors = instance.validate(config)
        assert valid is False

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_validate_valid_config(self):
        instance = FaultClearingScanAnalysis()
        config = {"model": {"rid": "test"}}
        valid, errors = instance.validate(config)
        assert valid is True

    def test_compute_scan_results(self):
        instance = FaultClearingScanAnalysis()
        ct_values = [0.05, 0.1, 0.15]
        results = instance._compute_scan_results(ct_values, "bus1", "3ph")
        assert len(results) == 3
        assert results[0]["clearing_time"] == 0.05

    def test_compute_scan_results_stability_check(self):
        instance = FaultClearingScanAnalysis()
        ct_values = [0.05, 0.1, 0.15]
        results = instance._compute_scan_results(ct_values, "bus1", "3ph")
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

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_run_returns_skill_result(self):
        instance = FaultClearingScanAnalysis()
        result = instance.run({"model": {"rid": "test"}})
        assert result is not None
        assert hasattr(result, "skill_name")

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_run_with_invalid_config(self):
        instance = FaultClearingScanAnalysis()
        result = instance.run({})
        assert result.status.value == "failed" or result.status.name == "failed"

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_has_log_method(self):
        instance = FaultClearingScanAnalysis()
        assert hasattr(instance, "_log")
        assert callable(instance._log)
