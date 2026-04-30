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
                "skill": {"type": "string", "const": "transient_stability", "default": "transient_stability"},
                "engine": {
                    "type": "string",
                    "enum": ["cloudpss", "pandapower"],
                    "default": "cloudpss",
                },
                "auth": {
                    "type": "object",
                    "properties": {
                        "token": {"type": "string"},
                        "token_file": {"type": "string", "default": ".cloudpss_token"},
                    },
                },
                "model": {
                    "type": "object",
                    "required": ["rid"],
                    "properties": {"rid": {"type": "string", "default": "model/holdme/IEEE39"}},
                },
                "simulation": {
                    "type": "object",
                    "properties": {
                        "duration": {"type": "number", "default": 10.0},
                        "time_step": {"type": "number", "default": 0.01},
                        "fault": {
                            "type": "object",
                            "properties": {
                                "bus": {"type": "string", "default": ""},
                                "type": {"type": "string", "default": "3ph"},
                                "duration": {"type": "number", "default": 0.1},
                            },
                        },
                    },
                },
                "rotor_angle_trace": {
                    "type": "object",
                    "required": ["angles_deg"],
                    "properties": {
                        "time": {"type": "array", "items": {"type": "number"}, "default": []},
                        "angles_deg": {"type": "array", "items": {"type": "number"}, "default": []},
                    },
                },
            },
        }

    def get_default_config(self) -> dict[str, Any]:
        return {
            "skill": self.name,
            "engine": "cloudpss",
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "model/holdme/IEEE39"},
            "simulation": {
                "duration": 10.0,
                "time_step": 0.01,
                "fault": {
                    "bus": "",
                    "type": "3ph",
                    "duration": 0.1,
                },
            },
            "rotor_angle_trace": {
                "time": [],
                "angles_deg": [],
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
        trace = config.get("rotor_angle_trace", {})
        angles = trace.get("angles_deg", [])
        if not angles:
            errors.append("rotor_angle_trace.angles_deg is required")
        elif len(angles) < 2:
            errors.append("rotor_angle_trace.angles_deg must contain at least two samples")
        times = trace.get("time", [])
        if times and len(times) != len(angles):
            errors.append("rotor_angle_trace.time and rotor_angle_trace.angles_deg must have the same length")
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
            auth = config.get("auth", {})
            api = Engine.create_powerflow_for_skill(
                engine=engine,
                base_url=auth.get("base_url"),
                auth=auth,
            )
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

            trace = config["rotor_angle_trace"]
            rotor_angles = [float(value) for value in trace["angles_deg"]]
            critical_angle = sim_config.get("critical_angle", 180.0)
            stability = self._assess_stability(rotor_angles, critical_angle)

            result_data = {
                "converged": result.is_success,
                "duration": duration,
                "time_step": time_step,
                "fault": fault,
                "stability": stability,
                "time_points": int(duration / time_step),
                "data_source": "rotor_angle_trace",
            }

            status = "stable" if stability.get("stable") else "unstable"
            self._log("INFO", f"Transient stability complete: {status}")

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
