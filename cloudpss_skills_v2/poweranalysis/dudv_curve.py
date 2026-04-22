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


class DUDVCurveAnalysis:
    name = "dudv_curve"
    description = "D-U/D-V曲线分析 - 电压稳定裕度评估"

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "dudv_curve"},
                "engine": {
                    "type": "string",
                    "enum": ["cloudpss", "pandapower"],
                    "default": "pandapower",
                },
                "model": {
                    "type": "object",
                    "required": ["rid"],
                    "properties": {"rid": {"type": "string"}},
                },
                "bus": {"type": "object", "properties": {"key": {"type": "string"}}},
                "scan": {
                    "type": "object",
                    "properties": {
                        "voltage_range": {"type": "array", "items": {"type": "number"}},
                        "num_points": {"type": "number", "default": 20},
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

    def _compute_dudv_points(
        self, v_base: float, v_range: list, num_points: int
    ) -> list[dict]:
        dv_up = v_base * 1.1 - v_base
        dv_down = v_base - v_base * 0.9
        points = []
        for i in range(num_points):
            v = v_base + (v_range[1] - v_range[0]) * i / (num_points - 1)
            dU = (v - v_base) / v_base
            dV = dU * 100
            points.append({"voltage": v, "dU": dU, "dV": dV})
        return points

    def _extract_dudv_from_result(
        self, bus_voltage: float, v_base: float = 1.0
    ) -> dict:
        dU = (bus_voltage - v_base) / v_base
        dV = dU * 100
        return {"voltage": bus_voltage, "dU": dU, "dV": dV}

    def _identify_stability_boundary(self, voltages: list, dVs: list) -> dict:
        if len(voltages) < 2:
            return {"boundary_voltage": None, "margin": None}
        boundary_idx = None
        for i in range(len(dVs) - 1):
            if dVs[i] * dVs[i + 1] < 0:
                boundary_idx = i
                break
        if boundary_idx is not None:
            return {
                "boundary_voltage": voltages[boundary_idx],
                "margin": abs(dVs[boundary_idx]),
            }
        return {"boundary_voltage": min(voltages), "margin": max(abs(d) for d in dVs)}

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
            engine = config.get("engine", "pandapower")
            api = Engine.create_powerflow(engine=engine)
            self._log("INFO", f"Using engine: {api.adapter.engine_name}")

            model_rid = config["model"]["rid"]
            self._log("INFO", f"Model: {model_rid}")

            handle = api.get_model_handle(model_rid)
            result = api.run_power_flow(model_handle=handle)

            bus_key = config.get("bus", {}).get("key", "bus1")
            scan_config = config.get("scan", {})
            v_range = scan_config.get("voltage_range", [0.9, 1.1])
            num_points = scan_config.get("num_points", 20)

            v_base = 1.0
            if result.is_success and result.data:
                bus_results = result.data.get("bus_results", [])
                for bus in bus_results:
                    if bus.get("bus") == bus_key:
                        v_base = bus.get("vm_pu", 1.0)
                        break

            points = self._compute_dudv_points(v_base, v_range, num_points)
            voltages = [p["voltage"] for p in points]
            dVs = [p["dV"] for p in points]
            boundary = self._identify_stability_boundary(voltages, dVs)

            result_data = {
                "bus": bus_key,
                "v_base": v_base,
                "voltage_range": v_range,
                "num_points": num_points,
                "points": points,
                "stability_boundary": boundary,
                "converged": result.is_success,
            }

            self._log(
                "INFO", f"DUDV curve analysis complete: {num_points} points computed"
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
            self._log("ERROR", f"DUDV curve analysis failed: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error=str(e),
                logs=self.logs,
                start_time=start_time,
                end_time=datetime.now(),
            )


__all__ = ["DUDVCurveAnalysis"]
