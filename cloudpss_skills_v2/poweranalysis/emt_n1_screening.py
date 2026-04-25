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


class EmtN1ScreeningAnalysis:
    name = "emt_n1_screening"
    description = "EMT N-1安全筛选 - 评估预想事故后系统电磁暂态行为"

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "emt_n1_screening"},
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
                "contingencies": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {"branch": {"type": "string"}},
                    },
                },
                "thresholds": {
                    "type": "object",
                    "properties": {
                        "voltage_deviation": {"type": "number", "default": 0.1},
                        "frequency_deviation": {"type": "number", "default": 0.5},
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

    def validate(
        self, config: dict[str, Any] | None
    ) -> tuple[bool, list[str]]:
        errors = []
        if not config:
            errors.append("config is required")
            return (False, errors)
        if not config.get("model", {}).get("rid"):
            errors.append("model.rid is required")
        return (len(errors) == 0, errors)

    def _calculate_postfault_gap(self, prefault: float, postfault: float) -> float:
        return abs(prefault - postfault)

    def _build_fault_config(self, contingency: dict[str, Any]) -> dict[str, Any]:
        fault_config = dict(contingency.get("fault") or {})
        if contingency.get("branch") is not None:
            fault_config.setdefault("branch", contingency.get("branch"))
        actual_trip = contingency.get("actual_trip")
        if actual_trip is None:
            actual_trip = contingency.get("trip")
        if actual_trip is None:
            actual_trip = True
        fault_config["actual_trip"] = actual_trip
        return fault_config

    def _assess_severity_level(
        self, gap: float, thresholds: dict[str, Any]
    ) -> str:
        v_thresh = thresholds.get("voltage_deviation", 0.1)
        if gap > v_thresh * 2:
            return "severe"
        elif gap > v_thresh:
            return "moderate"
        else:
            return "normal"

    def _rank_results(
        self, results: list[dict[str, Any]], thresholds: dict[str, Any]
    ) -> list[dict[str, Any]]:
        ranked = []
        for r in results:
            gap = r.get("max_gap", 0)
            severity = self._assess_severity_level(gap, thresholds)
            ranked.append({**r, "severity": severity})
        return sorted(ranked, key=lambda x: x.get("max_gap", 0), reverse=True)

    def _build_digest(
        self, baseline: dict[str, Any], results: list[dict[str, Any]]
    ) -> dict[str, Any]:
        severe = [r for r in results if r.get("severity") == "severe"]
        moderate = [r for r in results if r.get("severity") == "moderate"]
        normal = [r for r in results if r.get("severity") == "normal"]
        return {
            "total_contingencies": len(results),
            "severe_count": len(severe),
            "moderate_count": len(moderate),
            "normal_count": len(normal),
            "severe_contingencies": [r.get("branch") for r in severe],
        }

    def run(self, config: dict[str, Any] | None) -> SkillResult:
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
            pf_api = Engine.create_powerflow_for_skill(
                engine=engine,
                base_url=auth.get("base_url"),
                auth=auth,
            )
            emt_api = Engine.create_emt_for_skill(
                engine=engine,
                base_url=auth.get("base_url"),
                auth=auth,
            )
            self._log(
                "INFO",
                f"Using engines: PF={pf_api.adapter.engine_name}, EMT={emt_api.adapter.engine_name}",
            )

            model_rid = config["model"]["rid"]
            self._log("INFO", f"Model: {model_rid}")

            contingencies = config.get("contingencies", [])
            thresholds = config.get("thresholds", {})

            if not contingencies:
                self._log(
                    "INFO", "No contingencies specified, using default branch list"
                )
                contingencies = [{"branch": f"branch_{i}"} for i in range(1, 6)]

            handle = pf_api.get_model_handle(model_rid)
            baseline = pf_api.run_power_flow(model_handle=handle)

            emt_config = config.get("simulation", {})

            results = []
            for cont in contingencies:
                branch = cont.get("branch", "unknown")
                self._log("INFO", f"Analyzing contingency: {branch}")

                working = handle.clone()
                trip_applied = False
                actual_trip = cont.get("actual_trip")
                if actual_trip is None:
                    actual_trip = cont.get("trip")
                if actual_trip is None:
                    actual_trip = True

                if actual_trip:
                    trip_applied = working.remove_component(branch)
                    if not trip_applied:
                        self._log("WARNING", f"Failed to trip contingency branch: {branch}")

                pf_result = pf_api.run_power_flow(model_handle=working)
                emt_result = emt_api.run_emt(
                    model_id=working.model_id,
                    duration=emt_config.get("duration"),
                    step_size=emt_config.get("step_size"),
                    timeout=emt_config.get("timeout", 300),
                    sampling_freq=emt_config.get("sampling_freq", 2000),
                    fault_config=self._build_fault_config(cont),
                    source=config["model"].get("source", "cloud"),
                    auth=config.get("auth", {}),
                )

                gap = 0.0
                if pf_result.is_success and baseline.is_success:
                    gap = self._calculate_postfault_gap(
                        baseline.data.get("max_voltage", 1.0),
                        pf_result.data.get("max_voltage", 1.0),
                    )

                results.append(
                    {
                        "branch": branch,
                        "converged": pf_result.is_success and emt_result.is_success,
                        "max_gap": gap,
                        "actual_trip": trip_applied,
                        "powerflow_converged": pf_result.is_success,
                        "emt_success": emt_result.is_success,
                    }
                )

            ranked_results = self._rank_results(results, thresholds)
            digest = self._build_digest(
                baseline.data if baseline.data else {}, ranked_results
            )

            result_data = {
                "baseline_converged": baseline.is_success,
                "total_contingencies": len(contingencies),
                "results": ranked_results,
                "digest": digest,
            }

            self._log(
                "INFO",
                f"EMT N-1 screening complete: {digest['severe_count']} severe, {digest['moderate_count']} moderate",
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
            self._log("ERROR", f"EMT N-1 screening failed: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error=str(e),
                logs=self.logs,
                start_time=start_time,
                end_time=datetime.now(),
            )


__all__ = ["EmtN1ScreeningAnalysis"]
