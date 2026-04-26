from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from cloudpss_skills_v2.core.skill_result import (
    Artifact,
    SkillResult,
    SkillStatus,
)
from cloudpss_skills_v2.powerskill import Engine

logger = logging.getLogger(__name__)


class FaultClearingScanAnalysis:
    name = "fault_clearing_scan"
    description = "故障清除扫描 - 扫描不同清除时间对系统稳定性的影响"

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "fault_clearing_scan"},
                "engine": {
                    "type": "string",
                    "enum": ["cloudpss", "pandapower"],
                    "default": "cloudpss",
                },
                "model": {
                    "type": "object",
                    "required": ["rid"],
                    "properties": {"rid": {"type": "string"}},
                },
                "fault": {
                    "type": "object",
                    "properties": {
                        "bus": {"type": "string"},
                        "type": {"type": "string", "default": "3ph"},
                    },
                },
                "scan": {
                    "type": "object",
                    "properties": {
                        "clearing_times": {
                            "type": "array",
                            "items": {"type": "number"},
                        },
                    },
                },
                "stability_results": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["clearing_time", "stable"],
                        "properties": {
                            "clearing_time": {"type": "number"},
                            "stable": {"type": "boolean"},
                        },
                    },
                },
            },
        }

    def __init__(self):
        self.logs = []
        self.artifacts = []

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
        if not config.get("model", {}).get("rid"):
            errors.append("model.rid is required")
        stability_results = config.get("stability_results")
        if not isinstance(stability_results, list) or not stability_results:
            errors.append("stability_results must be a non-empty list")
        else:
            for idx, item in enumerate(stability_results):
                if not isinstance(item, dict):
                    errors.append(f"stability_results[{idx}] must be an object")
                    continue
                if "clearing_time" not in item or "stable" not in item:
                    errors.append(
                        f"stability_results[{idx}] requires clearing_time and stable"
                    )
                    continue
                try:
                    float(item["clearing_time"])
                except (TypeError, ValueError):
                    errors.append(f"stability_results[{idx}].clearing_time must be numeric")
                if not isinstance(item["stable"], bool):
                    errors.append(f"stability_results[{idx}].stable must be boolean")
        return (len(errors) == 0, errors)

    def _compute_scan_results(
        self, stability_results: list, fault_bus: str, fault_type: str
    ) -> list:
        results = []
        for item in stability_results:
            ct = float(item["clearing_time"])
            stable = bool(item["stable"])
            results.append(
                {
                    "clearing_time": ct,
                    "bus": fault_bus,
                    "fault_type": fault_type,
                    "stable": stable,
                    "critical": bool(item.get("critical", not stable)),
                    "data_source": item.get("data_source", "stability_results"),
                }
            )
        return results

    def _check_monotonic_degradation(self, results: list) -> bool:
        if len(results) < 2:
            return True
        stable_counts = [r.get("stable", False) for r in results]
        for i in range(len(stable_counts) - 1):
            if stable_counts[i] and not stable_counts[i + 1]:
                return True
        return False

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
            engine = config.get("engine", "cloudpss")
            auth = config.get("auth", {})
            api = Engine.create_powerflow_for_skill(
                engine=engine,
                base_url=auth.get("base_url"),
                auth=auth,
            )
            self._log("INFO", f"Using engine: {api.adapter.engine_name}")

            model_rid = config["model"]["rid"]
            self._log("INFO", f"Model: {model_rid}")

            fault = config.get("fault", {})
            fault_bus = fault.get("bus", "bus1")
            fault_type = fault.get("type", "3ph")

            stability_results = config["stability_results"]
            ct_values = [float(item["clearing_time"]) for item in stability_results]

            self._log("INFO", f"Scanning clearing times: {ct_values}")

            results = self._compute_scan_results(
                stability_results, fault_bus, fault_type
            )

            monotonic = self._check_monotonic_degradation(results)

            stable_count = len([r for r in results if r.get("stable")])
            critical_count = len([r for r in results if r.get("critical")])

            result_data = {
                "fault_bus": fault_bus,
                "fault_type": fault_type,
                "clearing_times": ct_values,
                "results": results,
                "stable_count": stable_count,
                "critical_count": critical_count,
                "monotonic_degradation": monotonic,
                "data_source": "stability_results",
                "confidence_level": "trace_or_simulation_derived",
                "validation_status": "explicit_stability_results_required",
            }

            self._log(
                "INFO",
                f"Fault clearing scan complete: {stable_count} stable, {critical_count} critical",
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
            self._log("ERROR", f"Fault clearing scan failed: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error=str(e),
                logs=self.logs,
                start_time=start_time,
                end_time=datetime.now(),
            )


__all__ = ["FaultClearingScanAnalysis"]
