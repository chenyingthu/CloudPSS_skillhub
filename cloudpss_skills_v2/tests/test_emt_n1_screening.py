import pytest
from cloudpss_skills_v2.poweranalysis.emt_n1_screening import EmtN1ScreeningAnalysis


class TestEmtN1ScreeningAnalysis:
    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_import(self):
        assert EmtN1ScreeningAnalysis is not None

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_instantiation(self):
        instance = EmtN1ScreeningAnalysis()
        assert instance is not None

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_has_name_attribute(self):
        instance = EmtN1ScreeningAnalysis()
        assert instance.name == "emt_n1_screening"

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_has_description(self):
        instance = EmtN1ScreeningAnalysis()
        assert hasattr(instance, "description")

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_has_config_schema(self):
        instance = EmtN1ScreeningAnalysis()
        schema = instance.config_schema
        assert schema is not None

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_validate_empty_config(self):
        instance = EmtN1ScreeningAnalysis()
        valid, errors = instance.validate({})
        assert valid is False

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_validate_missing_rid(self):
        instance = EmtN1ScreeningAnalysis()
        config = {"model": {}}
        valid, errors = instance.validate(config)
        assert valid is False

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_validate_valid_config(self):
        instance = EmtN1ScreeningAnalysis()
        config = {"model": {"rid": "test_model"}}
        valid, errors = instance.validate(config)
        assert valid is True

    def test_calculate_postfault_gap_equal(self):
        instance = EmtN1ScreeningAnalysis()
        gap = instance._calculate_postfault_gap(1.0, 1.0)
        assert gap == 0.0

    def test_calculate_postfault_gap_positive(self):
        instance = EmtN1ScreeningAnalysis()
        gap = instance._calculate_postfault_gap(1.0, 1.1)
        assert gap == abs(1.0 - 1.1)

    def test_calculate_postfault_gap_negative(self):
        instance = EmtN1ScreeningAnalysis()
        gap = instance._calculate_postfault_gap(1.0, 0.9)
        assert gap == abs(1.0 - 0.9)

    def test_assess_severity_high_gap(self):
        instance = EmtN1ScreeningAnalysis()
        thresholds = {"voltage_deviation": 0.1}
        severity = instance._assess_severity_level(0.25, thresholds)
        assert severity == "severe"

    def test_assess_severity_moderate_gap(self):
        instance = EmtN1ScreeningAnalysis()
        thresholds = {"voltage_deviation": 0.1}
        severity = instance._assess_severity_level(0.15, thresholds)
        assert severity == "moderate"

    def test_assess_severity_normal_gap(self):
        instance = EmtN1ScreeningAnalysis()
        thresholds = {"voltage_deviation": 0.1}
        severity = instance._assess_severity_level(0.05, thresholds)
        assert severity == "normal"

    def test_rank_results(self):
        instance = EmtN1ScreeningAnalysis()
        results = [
            {"branch": "B1", "max_gap": 0.05},
            {"branch": "B2", "max_gap": 0.15},
            {"branch": "B3", "max_gap": 0.25},
        ]
        thresholds = {"voltage_deviation": 0.1}
        ranked = instance._rank_results(results, thresholds)
        assert ranked[0]["severity"] == "severe"
        assert ranked[2]["severity"] == "normal"

    def test_build_digest_all_severe(self):
        instance = EmtN1ScreeningAnalysis()
        results = [
            {"branch": "B1", "severity": "severe"},
            {"branch": "B2", "severity": "severe"},
        ]
        baseline = {}
        digest = instance._build_digest(baseline, results)
        assert digest["severe_count"] == 2
        assert digest["total_contingencies"] == 2

    def test_build_digest_mixed(self):
        instance = EmtN1ScreeningAnalysis()
        results = [
            {"branch": "B1", "severity": "severe"},
            {"branch": "B2", "severity": "moderate"},
            {"branch": "B3", "severity": "normal"},
        ]
        baseline = {}
        digest = instance._build_digest(baseline, results)
        assert digest["severe_count"] == 1
        assert digest["moderate_count"] == 1
        assert digest["normal_count"] == 1

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_has_run_method(self):
        instance = EmtN1ScreeningAnalysis()
        assert hasattr(instance, "run")
        assert callable(instance.run)

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_run_returns_skill_result(self):
        instance = EmtN1ScreeningAnalysis()
        result = instance.run({"model": {"rid": "test"}})
        assert result is not None
        assert hasattr(result, "skill_name")
        assert hasattr(result, "status")

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_run_with_invalid_config(self):
        instance = EmtN1ScreeningAnalysis()
        result = instance.run({})
        assert result.status.value == "failed" or result.status.name == "failed"

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_has_log_method(self):
        instance = EmtN1ScreeningAnalysis()
        assert hasattr(instance, "_log")
        assert callable(instance._log)
