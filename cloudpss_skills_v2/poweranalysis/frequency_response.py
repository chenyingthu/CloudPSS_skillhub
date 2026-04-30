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


class FrequencyResponseAnalysis:
    name = "frequency_response"
    description = "频率响应分析 - 评估系统频率响应特性"

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "frequency_response", "default": "frequency_response"},
                "engine": {
                    "type": "string",
                    "enum": ["cloudpss", "pandapower"],
                    "default": "cloudpss",
                },
                "model": {
                    "type": "object",
                    "required": ["rid"],
                    "properties": {"rid": {"type": "string", "default": "model/holdme/IEEE39"}},
                },
                "disturbance": {
                    "type": "object",
                    "properties": {
                        "type": {
                            "type": "string",
                            "enum": [
                                "load_shedding",
                                "generator_trip",
                                "step_load_change",
                            ],
                        },
                        "magnitude": {"type": "number"},
                    },
                },
                "frequency_trace": {
                    "type": "object",
                    "required": ["time", "frequency_hz"],
                    "properties": {
                        "time": {"type": "array", "items": {"type": "number"}},
                        "frequency_hz": {"type": "array", "items": {"type": "number"}},
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
            "disturbance": {"type": "step_load_change", "magnitude": 0.05},
            "frequency_trace": {
                "time": [0.0, 1.0, 2.0, 3.0, 4.0, 5.0],
                "frequency_hz": [50.0, 49.95, 49.88, 49.92, 49.98, 50.0],
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
        disturbance = config.get("disturbance", {})
        if not disturbance.get("type"):
            errors.append("disturbance.type is required")
        trace = config.get("frequency_trace", {})
        times = trace.get("time", [])
        freqs = trace.get("frequency_hz", [])
        if not times or not freqs:
            errors.append("frequency_trace.time and frequency_trace.frequency_hz are required")
        elif len(times) != len(freqs):
            errors.append("frequency_trace.time and frequency_trace.frequency_hz must have the same length")
        elif len(times) < 2:
            errors.append("frequency_trace must contain at least two samples")
        return (len(errors) == 0, errors)

    def _calculate_nadir(self, freq: np.ndarray) -> float:
        if freq.size == 0:
            return 50.0
        return float(np.min(freq))

    def _calculate_rocof(self, freq: np.ndarray, time: np.ndarray) -> float:
        if freq.size < 2 or time.size < 2:
            return 0.0
        df = np.diff(freq)
        dt = np.diff(time)
        dt = np.where(dt == 0, 1e-6, dt)
        rocof = np.max(np.abs(df / dt))
        return float(rocof)

    def _calculate_recovery_time(
        self, freq: np.ndarray, time: np.ndarray, threshold: float = 50.0
    ) -> float:
        if freq.size == 0:
            return 0.0
        idx = np.where(np.abs(freq - threshold) < 0.05)[0]
        if len(idx) > 0:
            return float(time[idx[0]])
        return float(time[-1])

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

            disturbance = config.get("disturbance", {})
            dist_type = disturbance.get("type", "step_load_change")
            magnitude = disturbance.get("magnitude", 0.1)

            self._log("INFO", f"Disturbance: {dist_type}, magnitude: {magnitude}")

            handle = api.get_model_handle(model_rid)
            result = api.run_power_flow(model_handle=handle)

            trace = config["frequency_trace"]
            time = np.asarray(trace["time"], dtype=float)
            freq = np.asarray(trace["frequency_hz"], dtype=float)

            nadir = self._calculate_nadir(freq)
            rocof = self._calculate_rocof(freq, time)
            recovery_time = self._calculate_recovery_time(freq, time, 50.0)

            result_data = {
                "converged": result.is_success,
                "disturbance_type": dist_type,
                "magnitude": magnitude,
                "nadir": nadir,
                "rocof": rocof,
                "recovery_time": recovery_time,
                "frequency_unit": "Hz",
                "time_span": float(time[-1] - time[0]),
                "data_source": "frequency_trace",
            }

            self._log(
                "INFO",
                f"Frequency response: nadir={nadir:.3f}Hz, rocof={rocof:.3f}Hz/s, recovery={recovery_time}s",
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
            self._log("ERROR", f"Frequency response analysis failed: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error=str(e),
                logs=self.logs,
                start_time=start_time,
                end_time=datetime.now(),
            )


__all__ = ["FrequencyResponseAnalysis"]
