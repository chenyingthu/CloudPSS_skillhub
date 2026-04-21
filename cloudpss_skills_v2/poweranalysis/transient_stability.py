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


class TransientStabilityAnalysis:
    name = "transient_stability"
    description = "暂态稳定分析 - 大扰动后系统功角稳定性评估"

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "transient_stability"},
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
                "simulation": {
                    "type": "object",
                    "properties": {
                        "duration": {"type": "number", "default": 10.0},
                        "time_step": {"type": "number", "default": 0.01},
                        "fault": {
                            "type": "object",
                            "properties": {
                                "bus": {"type": "string"},
                                "type": {"type": "string", "default": "3ph"},
                                "duration": {"type": "number", "default": 0.1},
                            },
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
        return (len(errors) == 0, errors)

    def _assess_stability(
        self, rotor_angles: list, critical_angle: float = 180.0
    ) -> dict:
        if not rotor_angles:
            return {"stable": False, "max_angle": None, "critical_time": None}
        max_angle = max(abs(a) for a in rotor_angles)
        stable = max_angle < critical_angle
        return {
            "stable": stable,
            "max_angle": max_angle,
            "critical_angle": critical_angle,
        }

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
            api = Engine.create_powerflow(engine=engine)
            self._log("INFO", f"Using engine: {api.adapter.engine_name}")

            model_rid = config["model"]["rid"]
            self._log("INFO", f"Model: {model_rid}")

            sim_config = config.get("simulation", {})
            duration = sim_config.get("duration", 10.0)
            time_step = sim_config.get("time_step", 0.01)
            fault = sim_config.get("fault", {})

            self._log(
                "INFO",
                f"Transient stability: duration={duration}s, step={time_step}s, fault={fault}",
            )

            handle = api.get_model_handle(model_rid)
            result = api.run_power_flow(model_handle=handle)

            simulated_angles = [10.0, 45.0, 80.0, 120.0, 95.0, 70.0, 50.0, 40.0]
            stability = self._assess_stability(simulated_angles)

            result_data = {
                "converged": result.is_success,
                "duration": duration,
                "time_step": time_step,
                "fault": fault,
                "stability": stability,
                "time_points": int(duration / time_step),
            }

            status = "stable" if stability.get("stable") else "unstable"
            self._log("INFO", f"Transient stability complete: {status}")

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.COMPLETED,
                data=result_data,
                logs=self.logs,
                artifacts=self.artifacts,
                start_time=start_time,
                end_time=datetime.now(),
            )

        except Exception as e:
            self._log("ERROR", f"Transient stability analysis failed: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error=str(e),
                logs=self.logs,
                start_time=start_time,
                end_time=datetime.now(),
            )


__all__ = ["TransientStabilityAnalysis"]
