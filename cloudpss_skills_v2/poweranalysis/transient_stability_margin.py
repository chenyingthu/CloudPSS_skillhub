"""Transient stability margin analysis."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from cloudpss_skills_v2.core import SkillResult, SkillStatus


@dataclass
class StabilityMargin:
    fault_location: str = ""
    cct: float = 0.0
    actual_time: float = 0.0
    margin_percent: float = 0.0
    stability_status: str = "unknown"

    def to_dict(self) -> dict[str, Any]:
        return {
            "fault_location": self.fault_location,
            "cct": self.cct,
            "actual_time": self.actual_time,
            "margin_percent": self.margin_percent,
            "stability_status": self.stability_status,
        }


class TransientStabilityMarginAnalysis:
    name = "transient_stability_margin"
    description = "暂态稳定裕度 - 根据故障清除时间估算稳定裕度"

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["model", "fault_scenarios"],
            "properties": {
                "model": {"type": "object", "required": ["rid"]},
                "fault_scenarios": {"type": "array"},
                "target_margin": {"type": "number", "default": 10.0},
            },
        }

    def validate(self, config: dict[str, Any] | None = None) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if not isinstance(config, dict):
            return False, ["config is required"]
        model = config.get("model")
        if not isinstance(model, dict) or not model.get("rid"):
            errors.append("model.rid is required")
        scenarios = config.get("fault_scenarios")
        if not isinstance(scenarios, list) or not scenarios:
            errors.append("fault_scenarios must be a non-empty list")
        return len(errors) == 0, errors

    def _calculate_margin_percent(self, cct: float | None, actual_time: float | None) -> float:
        cct_value = float(cct or 0.0)
        if cct_value <= 0:
            return 0.0
        return ((cct_value - float(actual_time or 0.0)) / cct_value) * 100.0

    def _assess_stability(self, margin_percent: float | None) -> str:
        margin = float(margin_percent or 0.0)
        if margin > 10.0:
            return "stable"
        if margin < 0.0:
            return "unstable"
        return "marginal"

    def _estimate_cct(self, actual_time: float, target_margin: float) -> float:
        ratio = 1.0 - target_margin / 100.0
        if ratio <= 0:
            return max(actual_time, 0.5)
        return max(actual_time / ratio, actual_time)

    def run(self, config: dict[str, Any] | None = None) -> SkillResult:
        start_time = datetime.now()
        config = config or {}
        valid, errors = self.validate(config)
        if not valid:
            return SkillResult.failure(
                skill_name=self.name,
                error="; ".join(errors),
                data={"stage": "validation", "errors": errors},
            )

        target_margin = float(config.get("target_margin", 10.0))
        results = []
        for scenario in config["fault_scenarios"]:
            location = str(scenario.get("location") or scenario.get("bus") or "unknown")
            actual_time = float(scenario.get("clearing_time", 0.3))
            cct = float(scenario.get("cct", self._estimate_cct(actual_time, target_margin)))
            margin = self._calculate_margin_percent(cct, actual_time)
            results.append(
                StabilityMargin(
                    fault_location=location,
                    cct=cct,
                    actual_time=actual_time,
                    margin_percent=margin,
                    stability_status=self._assess_stability(margin),
                ).to_dict()
            )

        secure_count = len(
            [item for item in results if item["stability_status"] == "stable"]
        )
        return SkillResult(
            skill_name=self.name,
            status=SkillStatus.SUCCESS,
            data={
                "model_rid": config["model"]["rid"],
                "target_margin": target_margin,
                "results": results,
                "secure_count": secure_count,
                "total_scenarios": len(results),
            },
            metrics={"secure_count": secure_count, "scenario_count": len(results)},
            start_time=start_time,
            end_time=datetime.now(),
        )


__all__ = ["TransientStabilityMarginAnalysis", "StabilityMargin"]
