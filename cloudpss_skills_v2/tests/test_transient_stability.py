import pytest
from cloudpss_skills_v2.poweranalysis.transient_stability import (
    TransientStabilityAnalysis,
)


class TestTransientStabilityAnalysis:
    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_import(self):
        assert TransientStabilityAnalysis is not None

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_instantiation(self):
        instance = TransientStabilityAnalysis()
        assert instance is not None

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_has_name_attribute(self):
        instance = TransientStabilityAnalysis()
        assert instance.name == "transient_stability"

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_has_config_schema(self):
        instance = TransientStabilityAnalysis()
        schema = instance.config_schema
        assert schema is not None

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_validate_empty_config(self):
        instance = TransientStabilityAnalysis()
        valid, errors = instance.validate({})
        assert valid is False

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_validate_missing_rid(self):
        instance = TransientStabilityAnalysis()
        config = {"model": {}}
        valid, errors = instance.validate(config)
        assert valid is False

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_validate_valid_config(self):
        instance = TransientStabilityAnalysis()
        config = {"model": {"rid": "test"}}
        valid, errors = instance.validate(config)
        assert valid is True

    def test_assess_stability_stable(self):
        instance = TransientStabilityAnalysis()
        rotor_angles = [10.0, 45.0, 80.0, 95.0, 70.0, 50.0, 40.0, 30.0]
        result = instance._assess_stability(rotor_angles)
        assert result["stable"] is True
        assert result["max_angle"] == 95.0

    def test_assess_stability_unstable(self):
        instance = TransientStabilityAnalysis()
        rotor_angles = [10.0, 45.0, 120.0, 150.0, 180.0]
        result = instance._assess_stability(rotor_angles, critical_angle=150.0)
        assert result["stable"] is False
        assert result["max_angle"] == 180.0

    def test_assess_stability_empty(self):
        instance = TransientStabilityAnalysis()
        result = instance._assess_stability([])
        assert result["stable"] is False

    def test_assess_stability_with_custom_critical(self):
        instance = TransientStabilityAnalysis()
        rotor_angles = [10.0, 45.0, 80.0, 95.0]
        result = instance._assess_stability(rotor_angles, critical_angle=90.0)
        assert result["stable"] is False

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_run_returns_skill_result(self):
        instance = TransientStabilityAnalysis()
        result = instance.run({"model": {"rid": "test"}})
        assert result is not None
        assert hasattr(result, "skill_name")

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_run_with_invalid_config(self):
        instance = TransientStabilityAnalysis()
        result = instance.run({})
        assert result.status.value == "failed" or result.status.name == "failed"

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_has_log_method(self):
        instance = TransientStabilityAnalysis()
        assert hasattr(instance, "_log")
        assert callable(instance._log)
