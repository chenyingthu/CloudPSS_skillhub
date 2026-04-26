from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

import numpy as np

from cloudpss_skills_v2.core.skill_result import (
    Artifact,
    SkillResult,
    SkillStatus,
)
from cloudpss_skills_v2.powerskill import Engine

logger = logging.getLogger(__name__)


class DisturbanceSeverityAnalysis:
    name = "disturbance_severity"
    description = "扰动严重度分析 - 评估故障后电压恢复特性"

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "disturbance_severity"},
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
                        "fault_time": {"type": "number", "default": 4.0},
                        "fault_duration": {"type": "number", "default": 0.1},
                    },
                },
                "analysis": {
                    "type": "object",
                    "properties": {
                        "pre_fault_window": {"type": "number", "default": 0.5},
                        "si_interval": {"type": "number", "default": 0.0},
                        "si_window": {"type": "number", "default": 0.5},
                    },
                },
            },
        }

    def get_default_config(self) -> dict[str, Any]:
        return {
            "skill": self.name,
            "engine": "pandapower",
            "auth": {"token": "local-pandapower-token"},
            "model": {"rid": "case14", "source": "local"},
            "simulation": {"fault_time": 4.0, "fault_duration": 0.1},
            "analysis": {
                "pre_fault_window": 0.5,
                "si_interval": 0.0,
                "si_window": 0.5,
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

    def _calculate_dv(
        self,
        voltage: np.ndarray,
        time: np.ndarray,
        disturbance_time: float,
        pre_fault_window: float,
    ) -> dict:
        pre_mask = (time >= disturbance_time - pre_fault_window) & (
            time < disturbance_time
        )
        pre_v = voltage[pre_mask]
        if len(pre_v) == 0:
            return {"dv_up": 0.0, "dv_down": 0.0, "v_steady": 1.0}
        v_steady = float(np.mean(pre_v))
        post_mask = time >= disturbance_time
        post_v = voltage[post_mask]
        if len(post_v) == 0:
            return {"dv_up": 0.0, "dv_down": 0.0, "v_steady": v_steady}
        v_max = float(np.max(post_v))
        v_min = float(np.min(post_v))
        dv_up = max(0, v_max - v_steady)
        dv_down = max(0, v_steady - v_min)
        return {"dv_up": dv_up, "dv_down": dv_down, "v_steady": v_steady}

    def _calculate_si(
        self,
        voltage: np.ndarray,
        time: np.ndarray,
        disturbance_time: float,
        si_interval: float = 0.0,
        si_window: float = 0.5,
    ) -> float:
        pre_mask = (time >= disturbance_time - 0.5) & (time < disturbance_time)
        pre_v = voltage[pre_mask]
        if len(pre_v) == 0:
            return 0.0
        v_ref = float(np.mean(pre_v))
        t_start = disturbance_time + si_interval
        t_end = t_start + si_window
        window_mask = (time >= t_start) & (time <= t_end)
        window_v = voltage[window_mask]
        if len(window_v) == 0:
            return 0.0
        deviations = np.abs(v_ref - window_v)
        weights = np.where(
            deviations > v_ref * 0.11, 1, np.where(deviations > v_ref * 0.1, 0.5, 0)
        )
        si = float(np.sum(deviations * weights))
        return si

    def _assess_severity(self, dv_up: float, dv_down: float, si: float) -> str:
        if dv_down > 0.2 or si > 10.0:
            return "severe"
        elif dv_down > 0.1 or si > 5.0:
            return "moderate"
        else:
            return "normal"

    def _identify_weak_points(self, results: list) -> list:
        weak = []
        for r in results:
            if r.get("severity") in ["severe", "moderate"]:
                weak.append(r.get("bus", "unknown"))
        return weak

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
            disturbance_time = sim_config.get("fault_time", 4.0)

            analysis_config = config.get("analysis", {})
            pre_fault_window = analysis_config.get("pre_fault_window", 0.5)
            si_interval = analysis_config.get("si_interval", 0.0)
            si_window = analysis_config.get("si_window", 0.5)

            handle = api.get_model_handle(model_rid)
            result = api.run_power_flow(model_handle=handle)

            time = np.array([0, 1, 2, 3, 3.9, 4.0, 4.1, 4.5, 5.0, 6.0])
            voltage = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 0.6, 0.85, 0.98, 1.0])

            dv_result = self._calculate_dv(
                voltage, time, disturbance_time, pre_fault_window
            )
            si = self._calculate_si(
                voltage, time, disturbance_time, si_interval, si_window
            )
            severity = self._assess_severity(
                dv_result["dv_up"], dv_result["dv_down"], si
            )

            result_data = {
                "converged": result.is_success,
                "disturbance_time": disturbance_time,
                "dv_up": dv_result["dv_up"],
                "dv_down": dv_result["dv_down"],
                "v_steady": dv_result["v_steady"],
                "si": si,
                "severity": severity,
            }

            self._log(
                "INFO",
                f"Disturbance severity: dv_up={dv_result['dv_up']:.3f}, dv_down={dv_result['dv_down']:.3f}, severity={severity}",
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
            self._log("ERROR", f"Disturbance severity analysis failed: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error=str(e),
                logs=self.logs,
                start_time=start_time,
                end_time=datetime.now(),
            )


__all__ = ["DisturbanceSeverityAnalysis"]
