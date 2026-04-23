import pytest
from cloudpss_skills_v2.poweranalysis.renewable_integration import (
    RenewableIntegrationAnalysis,
    classify_grid_strength,
    compute_scr,
)


class TestRenewableIntegrationAnalysis:
    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_import(self):
        assert RenewableIntegrationAnalysis is not None

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_instantiation(self):
        instance = RenewableIntegrationAnalysis()
        assert instance is not None

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_has_name_attribute(self):
        instance = RenewableIntegrationAnalysis()
        assert instance.name == "renewable_integration"

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_has_config_schema(self):
        instance = RenewableIntegrationAnalysis()
        schema = instance.config_schema
        assert schema is not None

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_validate_empty_config(self):
        instance = RenewableIntegrationAnalysis()
        valid, errors = instance.validate({})
        assert valid is False

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_validate_missing_rid(self):
        instance = RenewableIntegrationAnalysis()
        config = {"model": {}}
        valid, errors = instance.validate(config)
        assert valid is False

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_validate_valid_config(self):
        instance = RenewableIntegrationAnalysis()
        config = {"model": {"rid": "test"}}
        valid, errors = instance.validate(config)
        assert valid is True

    def test_calculate_scr_at_buses(self):
        instance = RenewableIntegrationAnalysis()
        buses = [{"name": "B1", "sc_mva": 100.0}]
        results = instance._calculate_scr_at_buses(buses, 100.0)
        assert len(results) == 1
        assert results[0]["scr"] == 1.0

    def test_calculate_scr_strong_grid(self):
        instance = RenewableIntegrationAnalysis()
        buses = [{"name": "B1", "sc_mva": 500.0}]
        results = instance._calculate_scr_at_buses(buses, 100.0)
        assert results[0]["strength"] == "strong"

    def test_calculate_scr_moderate_grid(self):
        instance = RenewableIntegrationAnalysis()
        buses = [{"name": "B1", "sc_mva": 250.0}]
        results = instance._calculate_scr_at_buses(buses, 100.0)
        assert results[0]["strength"] == "moderate"

    def test_calculate_scr_weak_grid(self):
        instance = RenewableIntegrationAnalysis()
        buses = [{"name": "B1", "sc_mva": 100.0}]
        results = instance._calculate_scr_at_buses(buses, 100.0)
        assert results[0]["strength"] == "weak"

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_run_returns_skill_result(self):
        instance = RenewableIntegrationAnalysis()
        result = instance.run({"model": {"rid": "test"}})
        assert result is not None
        assert hasattr(result, "skill_name")

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_run_with_invalid_config(self):
        instance = RenewableIntegrationAnalysis()
        result = instance.run({})
        assert result.status.value == "failed" or result.status.name == "failed"

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_has_log_method(self):
        instance = RenewableIntegrationAnalysis()
        assert hasattr(instance, "_log")
        assert callable(instance._log)


class TestGridStrengthClassification:
    def test_classify_grid_strength_strong(self):
        assert classify_grid_strength(3.5) == "strong"
        assert classify_grid_strength(3.0) == "strong"

    def test_classify_grid_strength_moderate(self):
        assert classify_grid_strength(2.5) == "moderate"
        assert classify_grid_strength(2.0) == "moderate"

    def test_classify_grid_strength_weak(self):
        assert classify_grid_strength(1.5) == "weak"
        assert classify_grid_strength(1.0) == "weak"


class TestSCRCalculation:
    def test_compute_scr_basic(self):
        scr = compute_scr(100.0, 1.0, 100.0)
        assert scr == 1.0

    def test_compute_scr_high_sc(self):
        scr = compute_scr(500.0, 1.0, 100.0)
        assert scr == 5.0

    def test_compute_scr_zero_voltage(self):
        scr = compute_scr(100.0, 0.0, 100.0)
        assert scr == 0.0

    def test_compute_scr_zero_base(self):
        scr = compute_scr(100.0, 1.0, 0.0)
        assert scr == 0.0
