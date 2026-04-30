"""Compare Visualization Skill v2 - compare multiple scenario result sets."""

from __future__ import annotations

from datetime import datetime
from typing import Any

import numpy as np

from cloudpss_skills_v2.core import LogEntry, SkillResult, SkillStatus


class CompareVisualizationTool:
    """Compute chart-ready comparison data across multiple sources."""

    name = "compare_visualization"

    def __init__(self):
        self.logs = []
        self.artifacts = []

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill"],
            "properties": {
                "skill": {"type": "string", "const": "compare_visualization", "default": "compare_visualization"},
                "sources": {"type": "array", "items": {"type": "object"}, "default": []},
                "compare": {
                    "type": "object",
                    "properties": {
                        "channels": {"type": "array", "items": {"type": "string"}, "default": []},
                        "metrics": {"type": "array", "items": {"type": "string"}, "default": ["mean", "delta", "ratio"]},
                        "chart": {"type": "string", "default": "time_series"},
                    },
                },
                "time_range": {
                    "type": "object",
                    "properties": {
                        "start": {"type": ["number", "null"], "default": None},
                        "end": {"type": ["number", "null"], "default": None},
                    },
                    "default": {"start": None, "end": None},
                },
            },
        }

    def get_default_config(self):
        return {
            "skill": self.name,
            "sources": [],
            "compare": {"channels": [], "metrics": ["mean", "delta", "ratio"], "chart": "time_series"},
            "time_range": {"start": None, "end": None},
        }

    def validate(self, config):
        errors = []
        if config is None:
            return False, ["config is required"]
        if not isinstance(config, dict):
            return False, ["config must be a dictionary"]
        sources = config.get("sources", [])
        if not isinstance(sources, list) or len(sources) < 2:
            errors.append("sources must contain at least two scenario entries")
        channels = config.get("compare", {}).get("channels", [])
        if channels is not None and not isinstance(channels, list):
            errors.append("compare.channels must be a list")
        metrics = config.get("compare", {}).get("metrics", [])
        if metrics is not None and not isinstance(metrics, list):
            errors.append("compare.metrics must be a list")
        return len(errors) == 0, errors

    def _compute_metrics(self, values, metrics):
        array = np.asarray(values, dtype=float)
        if array.size == 0:
            return {metric: 0.0 for metric in metrics}
        result = {}
        base = float(array[0])
        current = float(array[-1])
        for metric in metrics:
            if metric == "min":
                result[metric] = float(np.min(array))
            elif metric == "max":
                result[metric] = float(np.max(array))
            elif metric == "mean":
                result[metric] = float(np.mean(array))
            elif metric == "delta":
                result[metric] = current - base
            elif metric == "ratio":
                result[metric] = current / base if base != 0 else 0.0
            elif metric == "std":
                result[metric] = float(np.std(array))
            else:
                result[metric] = 0.0
        return result

    def _filter_time_range(self, time, values, start=None, end=None):
        time_array = np.asarray(time, dtype=float)
        value_array = np.asarray(values, dtype=float)
        if time_array.size != value_array.size:
            length = min(time_array.size, value_array.size)
            time_array = time_array[:length]
            value_array = value_array[:length]
        mask = np.ones(time_array.shape, dtype=bool)
        if start is not None:
            mask &= time_array >= float(start)
        if end is not None:
            mask &= time_array <= float(end)
        return time_array[mask], value_array[mask]

    def _normalize_for_radar(self, values):
        numeric = np.asarray(values, dtype=float)
        if numeric.size == 0:
            return []
        low = float(np.min(numeric))
        high = float(np.max(numeric))
        if high == low:
            return [1.0 for _ in numeric]
        return [float((value - low) / (high - low)) for value in numeric]

    def _extract_channel_data(self, sources, channels, metrics, time_range):
        extracted = {}
        start = time_range.get("start") if isinstance(time_range, dict) else None
        end = time_range.get("end") if isinstance(time_range, dict) else None
        for source in sources:
            source_name = source.get("name", f"source_{len(extracted) + 1}")
            source_data = source.get("data", {})
            source_result = {}
            available_channels = source_data.get("channels", source_data)
            requested_channels = channels or [key for key, value in available_channels.items() if isinstance(value, (list, tuple))]
            for channel in requested_channels:
                series = available_channels.get(channel, [])
                time = source_data.get("time") or list(range(len(series)))
                filtered_time, filtered_values = self._filter_time_range(time, series, start, end)
                source_result[channel] = {
                    "time": filtered_time.tolist(),
                    "values": filtered_values.tolist(),
                    "metrics": self._compute_metrics(filtered_values, metrics),
                }
            extracted[source_name] = source_result
        return extracted

    def run(self, config):
        start_time = datetime.now()
        if config is None:
            config = {}
        self.logs = []
        valid, errors = self.validate(config)
        if not valid:
            return SkillResult.failure(self.name, "; ".join(errors), {"errors": errors}, "validation")
        try:
            compare_config = config.get("compare", {})
            channels = compare_config.get("channels", [])
            metrics = compare_config.get("metrics", ["mean", "delta", "ratio"])
            extracted = self._extract_channel_data(config.get("sources", []), channels, metrics, config.get("time_range", {}))

            radar = {}
            for source_name, channel_map in extracted.items():
                metric_values = [channel_data["metrics"].get("mean", 0.0) for channel_data in channel_map.values()]
                radar[source_name] = self._normalize_for_radar(metric_values)

            self.logs.append(LogEntry(level="info", message="Compare visualization data prepared"))
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                data={
                    "chart": compare_config.get("chart", "time_series"),
                    "comparison": extracted,
                    "radar": radar,
                },
                logs=self.logs,
                metrics={"source_count": len(config.get("sources", [])), "channel_count": len(channels or [])},
                start_time=start_time,
                end_time=datetime.now(),
            )
        except (TypeError, ValueError) as exc:
            return SkillResult.failure(self.name, str(exc), stage="compare_visualization")


__all__ = ["CompareVisualizationTool"]
