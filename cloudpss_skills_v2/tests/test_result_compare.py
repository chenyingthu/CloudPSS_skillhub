import pytest
from cloudpss_skills_v2.tools.result_compare import ResultCompareTool


class TestResultCompareTool:
    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_import(self):
        assert ResultCompareTool is not None

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_instantiation(self):
        instance = ResultCompareTool()
        assert instance is not None

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_has_name_attribute(self):
        instance = ResultCompareTool()
        assert instance.name == "result_compare"

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_has_description(self):
        instance = ResultCompareTool()
        assert hasattr(instance, "description")

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_has_config_schema(self):
        instance = ResultCompareTool()
        schema = instance.config_schema
        assert schema is not None
        assert schema["type"] == "object"

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_validate_empty_config(self):
        instance = ResultCompareTool()
        valid, errors = instance.validate({})
        assert valid is False

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_validate_single_source(self):
        instance = ResultCompareTool()
        config = {"sources": [{"name": "source1"}]}
        valid, errors = instance.validate(config)
        assert valid is False

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_validate_two_sources(self):
        instance = ResultCompareTool()
        config = {"sources": [{"name": "s1"}, {"name": "s2"}]}
        valid, errors = instance.validate(config)
        assert valid is True

    def test_compute_metric_max(self):
        instance = ResultCompareTool()
        values = [1, 5, 3, 10, 2]
        result = instance._compute_metric(values, "max")
        assert result == 10

    def test_compute_metric_min(self):
        instance = ResultCompareTool()
        values = [1, 5, 3, 10, 2]
        result = instance._compute_metric(values, "min")
        assert result == 1

    def test_compute_metric_mean(self):
        instance = ResultCompareTool()
        values = [1, 2, 3, 4, 5]
        result = instance._compute_metric(values, "mean")
        assert result == 3.0

    def test_compute_metric_empty(self):
        instance = ResultCompareTool()
        result = instance._compute_metric([], "max")
        assert result == 0.0

    def test_compute_metric_unknown(self):
        instance = ResultCompareTool()
        values = [1, 2, 3]
        result = instance._compute_metric(values, "unknown_metric")
        assert result == 0.0

    def test_extract_values_from_values_key(self):
        instance = ResultCompareTool()
        data = {"values": [1, 2, 3]}
        result = instance._extract_values(data)
        assert result == [1, 2, 3]

    def test_extract_values_from_series_key(self):
        instance = ResultCompareTool()
        data = {"series": [10, 20, 30]}
        result = instance._extract_values(data)
        assert result == [10, 20, 30]

    def test_extract_values_from_data_key(self):
        instance = ResultCompareTool()
        data = {"data": [100, 200]}
        result = instance._extract_values(data)
        assert result == [100, 200]

    def test_extract_values_empty(self):
        instance = ResultCompareTool()
        data = {"other": "value"}
        result = instance._extract_values(data)
        assert result == []

    def test_compare_sources_single_metric(self):
        instance = ResultCompareTool()
        sources = [
            {"name": "source1", "data": {"values": [1, 2, 3]}},
            {"name": "source2", "data": {"values": [4, 5, 6]}},
        ]
        comparison = instance._compare_sources(sources, ["max"])
        assert "max" in comparison
        assert comparison["max"]["source1"] == 3
        assert comparison["max"]["source2"] == 6

    def test_compare_sources_multiple_metrics(self):
        instance = ResultCompareTool()
        sources = [
            {"name": "A", "data": {"values": [1, 10]}},
            {"name": "B", "data": {"values": [2, 20]}},
        ]
        comparison = instance._compare_sources(sources, ["max", "min", "mean"])
        assert len(comparison) == 3

    def test_compare_sources_empty_data(self):
        instance = ResultCompareTool()
        sources = [{"name": "A", "data": {}}, {"name": "B", "data": {}}]
        comparison = instance._compare_sources(sources, ["max"])
        assert comparison["max"]["A"] == 0.0

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_has_run_method(self):
        instance = ResultCompareTool()
        assert hasattr(instance, "run")
        assert callable(instance.run)

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_has_log_method(self):
        instance = ResultCompareTool()
        assert hasattr(instance, "_log")
        assert callable(instance._log)
