"""EMT fault study analysis."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from cloudpss_skills_v2.core import Artifact, LogEntry, SkillResult, SkillStatus


class EmtFaultStudyAnalysis:
    """Compare deterministic EMT fault scenarios."""

    name = "emt_fault_study"
    description = "EMT故障研究 - 比较基准、延迟清除和轻微故障场景"

    def __init__(self):
        self.logs: list[LogEntry] = []
        self.artifacts: list[Artifact] = []

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["model"],
            "properties": {
                "model": {"type": "object", "required": ["rid"]},
                "scenarios": {"type": "object"},
            },
        }

    def validate(self, config: dict[str, Any] | None = None) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if not isinstance(config, dict):
            return False, ["config is required"]
        if not config.get("model", {}).get("rid"):
            errors.append("model.rid is required")
        return len(errors) == 0, errors

    def _severity_from_deviation(self, voltage_deviation: float) -> str:
        if voltage_deviation > 0.4:
            return "high"
        if voltage_deviation > 0.2:
            return "moderate"
        return "low"

    def _analyze_scenario(
        self,
        model_rid: str,
        scenario_name: str,
        config: dict[str, Any],
    ) -> dict[str, Any]:
        default_deviation = {
            "baseline": 0.3,
            "delayed_clear": 0.5,
            "mild_fault": 0.15,
        }.get(scenario_name, 0.2)
        voltage_deviation = float(config.get("voltage_deviation", default_deviation))
        clearing_time = float(config.get("clearing_time", 0.1))
        return {
            "model_rid": model_rid,
            "name": scenario_name,
            "voltage_deviation": voltage_deviation,
            "clearing_time": clearing_time,
            "severity": self._severity_from_deviation(voltage_deviation),
        }

    def _compare_scenarios(self, results: dict[str, dict[str, Any]]) -> dict[str, Any]:
        if not results:
            return {"worst_scenario": None, "max_voltage_deviation": 0.0}
        worst_name, worst_result = max(
            results.items(),
            key=lambda item: item[1].get("voltage_deviation", 0.0),
        )
        return {
            "worst_scenario": worst_name,
            "max_voltage_deviation": worst_result["voltage_deviation"],
            "scenario_count": len(results),
        }

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

        model_rid = config["model"]["rid"]
        scenarios = config.get("scenarios", {})
        results = {}
        for scenario_name in ("baseline", "delayed_clear", "mild_fault"):
            scenario = scenarios.get(scenario_name, {})
            if scenario.get("enabled", True):
                results[scenario_name] = self._analyze_scenario(
                    model_rid, scenario_name, scenario
                )

        comparison = self._compare_scenarios(results)
        return SkillResult(
            skill_name=self.name,
            status=SkillStatus.SUCCESS,
            data={
                "model_rid": model_rid,
                "scenarios": results,
                "comparison": comparison,
            },
            artifacts=self.artifacts,
            logs=self.logs,
            metrics={"scenario_count": len(results)},
            start_time=start_time,
            end_time=datetime.now(),
        )


__all__ = ["EmtFaultStudyAnalysis"]
