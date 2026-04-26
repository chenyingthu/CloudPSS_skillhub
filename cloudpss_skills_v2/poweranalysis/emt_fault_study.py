"""EMT fault study analysis."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from cloudpss_skills_v2.core import Artifact, LogEntry, SkillResult, SkillStatus


class EmtFaultStudyAnalysis:
    """Compare explicit EMT fault scenario measurements."""

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

    def get_default_config(self) -> dict[str, Any]:
        return {
            "model": {"rid": "case14", "source": "local"},
            "scenarios": {
                "baseline": {
                    "enabled": True,
                    "prefault_voltage_pu": 1.0,
                    "minimum_voltage_pu": 0.7,
                    "clearing_time": 0.1,
                },
                "delayed_clear": {
                    "enabled": True,
                    "prefault_voltage_pu": 1.0,
                    "minimum_voltage_pu": 0.5,
                    "clearing_time": 0.2,
                },
                "mild_fault": {
                    "enabled": True,
                    "prefault_voltage_pu": 1.0,
                    "minimum_voltage_pu": 0.85,
                    "clearing_time": 0.08,
                },
            },
        }

    def validate(self, config: dict[str, Any] | None = None) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if not isinstance(config, dict):
            return False, ["config is required"]
        if not config.get("model", {}).get("rid"):
            errors.append("model.rid is required")
        scenarios = config.get("scenarios", {})
        if not isinstance(scenarios, dict) or not scenarios:
            errors.append("scenarios are required")
        for scenario_name, scenario in scenarios.items():
            if not isinstance(scenario, dict):
                errors.append(f"scenarios.{scenario_name} must be an object")
                continue
            if scenario.get("enabled", True) and "voltage_deviation" not in scenario:
                missing_voltage = (
                    "prefault_voltage_pu" not in scenario
                    or "minimum_voltage_pu" not in scenario
                )
                if missing_voltage:
                    errors.append(
                        f"scenarios.{scenario_name} requires voltage_deviation or prefault/minimum voltage measurements"
                    )
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
        if "voltage_deviation" in config:
            voltage_deviation = float(config["voltage_deviation"])
            data_source = "voltage_deviation"
        else:
            prefault = float(config["prefault_voltage_pu"])
            minimum = float(config["minimum_voltage_pu"])
            voltage_deviation = abs(prefault - minimum)
            data_source = "voltage_measurements"
        clearing_time = float(config.get("clearing_time", 0.1))
        return {
            "model_rid": model_rid,
            "name": scenario_name,
            "voltage_deviation": voltage_deviation,
            "clearing_time": clearing_time,
            "severity": self._severity_from_deviation(voltage_deviation),
            "data_source": data_source,
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
        for scenario_name, scenario in scenarios.items():
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
