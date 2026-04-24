"""Tests for cloudpss_skills_v2.tools.compare_visualization."""

from cloudpss_skills_v2.tools.compare_visualization import CompareVisualizationTool


class TestCompareVisualizationTool:
    def test_validate_requires_two_sources(self):
        tool = CompareVisualizationTool()
        valid, errors = tool.validate({"sources": [{"name": "one"}]})
        assert valid is False
        assert "at least two" in errors[0]

    def test_compute_metrics_delta_ratio_and_stats(self):
        tool = CompareVisualizationTool()
        metrics = tool._compute_metrics([2, 4, 6], ["min", "max", "mean", "delta", "ratio", "std", "unknown"])
        assert metrics["min"] == 2.0
        assert metrics["max"] == 6.0
        assert metrics["mean"] == 4.0
        assert metrics["delta"] == 4.0
        assert metrics["ratio"] == 3.0
        assert metrics["unknown"] == 0.0

    def test_filter_time_range_trims_mismatched_lengths(self):
        tool = CompareVisualizationTool()
        time, values = tool._filter_time_range([0, 1, 2, 3], [10, 20, 30], 1, 2)
        assert time.tolist() == [1.0, 2.0]
        assert values.tolist() == [20.0, 30.0]

    def test_normalize_for_radar(self):
        tool = CompareVisualizationTool()
        assert tool._normalize_for_radar([10, 20, 30]) == [0.0, 0.5, 1.0]
        assert tool._normalize_for_radar([5, 5]) == [1.0, 1.0]

    def test_extract_channel_data_and_run(self):
        tool = CompareVisualizationTool()
        sources = [
            {"name": "base", "data": {"time": [0, 1, 2, 3], "channels": {"v": [1.0, 1.1, 1.2, 1.3], "i": [2, 3, 4, 5]}}},
            {"name": "case", "data": {"time": [0, 1, 2, 3], "channels": {"v": [0.9, 1.0, 1.1, 1.2], "i": [3, 4, 5, 6]}}},
        ]
        config = {
            "sources": sources,
            "compare": {"channels": ["v", "i"], "metrics": ["mean", "delta", "ratio"], "chart": "radar"},
            "time_range": {"start": 1, "end": 3},
        }
        extracted = tool._extract_channel_data(sources, ["v"], ["mean"], {"start": 1, "end": 2})
        result = tool.run(config)

        assert extracted["base"]["v"]["time"] == [1.0, 2.0]
        assert result.status.value == "success"
        assert result.data["chart"] == "radar"
        assert result.data["comparison"]["case"]["v"]["metrics"]["delta"] == 0.19999999999999996
        assert "base" in result.data["radar"]
