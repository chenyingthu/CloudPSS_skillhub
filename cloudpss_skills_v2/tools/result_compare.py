"""Result Compare Tool - Compare simulation results.

结果比较工具 - 比较仿真结果。
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from cloudpss_skills_v2.core.skill_result import (
    Artifact,
    SkillResult,
    SkillStatus,
)

logger = logging.getLogger(__name__)


class ResultCompareTool:
    name = "result_compare"
    description = "结果比较工具 - 比较仿真结果"

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill"],
            "properties": {
                "skill": {"type": "string", "const": "result_compare", "default": "result_compare"},
                "sources": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "data": {"type": "object"},
                        },
                    },
                    "minItems": 2,
                    "default": [],
                },
                "compare": {
                    "type": "object",
                    "properties": {
                        "metrics": {
                            "type": "array",
                            "items": {"type": "string"},
                            "default": ["max", "min", "mean"],
                        },
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {
                            "type": "string",
                            "enum": ["json", "markdown"],
                            "default": "json",
                        },
                    },
                },
            },
        }

    def __init__(self):
        self.logs = []
        self.artifacts = []

    def get_default_config(self) -> dict[str, Any]:
        return {
            "skill": self.name,
            "sources": [],
            "compare": {
                "metrics": ["max", "min", "mean"],
            },
            "output": {
                "format": "json",
            },
        }

    def _log(self, level: str, message: str) -> None:
        self.logs.append(
            {
                "timestamp": datetime.now().isoformat(),
                "level": level,
                "message": message,
            }
        )
        getattr(logger, level.lower(), logger.info)(message)

    def validate(self, config: dict | None) -> tuple[bool, list[str]]:
        errors = []
        if not config:
            errors.append("config is required")
            return (False, errors)

        sources = config.get("sources", [])
        if len(sources) < 2:
            errors.append("At least 2 sources are required for comparison")

        return (len(errors) == 0, errors)

    def _compute_metric(self, values: list, metric: str) -> float:
        if not values:
            return 0.0

        if metric == "max":
            return max(values)
        elif metric == "min":
            return min(values)
        elif metric == "mean":
            return sum(values) / len(values)
        elif metric == "rms":
            return (sum(v * v for v in values) / len(values)) ** 0.5
        else:
            return 0.0

    def _extract_values(self, data: dict) -> list:
        if isinstance(data, dict):
            for key in ["values", "series", "data", "results"]:
                if key in data:
                    val = data[key]
                    if isinstance(val, list):
                        return val
        return []

    def _compare_sources(self, sources: list, metrics: list) -> dict:
        if not sources:
            return {}

        comparison = {}
        first_source = sources[0].get("data", {})
        first_values = self._extract_values(first_source)

        for metric in metrics:
            metric_values = {}
            for source in sources:
                name = source.get("name", f"source_{len(metric_values)}")
                data = source.get("data", {})
                values = self._extract_values(data)
                metric_values[name] = self._compute_metric(values, metric)

            comparison[metric] = metric_values

        return comparison

    def run(self, config: dict | None) -> SkillResult:
        start_time = datetime.now()
        if config is None:
            config = {}
        self.logs = []
        self.artifacts = []

        valid, errors = self.validate(config)
        if not valid:
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error="; ".join(errors),
                logs=self.logs,
                start_time=start_time,
                end_time=datetime.now(),
            )

        try:
            sources = config.get("sources", [])
            compare_config = config.get("compare", {})
            metrics = compare_config.get("metrics", ["max", "min", "mean"])

            comparison = self._compare_sources(sources, metrics)

            result_data = {
                "sources": [s.get("name") for s in sources],
                "metrics": metrics,
                "comparison": comparison,
            }

            self._log(
                "INFO",
                f"Comparison complete: {len(sources)} sources, {len(metrics)} metrics",
            )

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                data=result_data,
                logs=self.logs,
                artifacts=self.artifacts,
                start_time=start_time,
                end_time=datetime.now(),
            )

        except Exception as e:
            self._log("ERROR", f"Comparison failed: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error=str(e),
                logs=self.logs,
                start_time=start_time,
                end_time=datetime.now(),
            )


__all__ = ["ResultCompareTool"]
