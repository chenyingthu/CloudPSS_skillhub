"""VSI Weak Bus Analysis - Identify voltage stability weak buses.

VSI弱母线分析 - 识别电压稳定薄弱的母线。
"""

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
from cloudpss_skills_v2.libs.algo_lib import BusWeaknessIndex

logger = logging.getLogger(__name__)


class VSIWeakBusAnalysis:
    name = "vsi_weak_bus"
    description = "VSI弱母线分析 - 识别电压稳定薄弱母线"

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "vsi_weak_bus"},
                "engine": {
                    "type": "string",
                    "enum": ["cloudpss", "pandapower"],
                    "default": "pandapower",
                },
                "model": {"type": "object", "required": ["rid"]},
                "analysis": {
                    "type": "object",
                    "properties": {
                        "threshold": {"type": "number", "default": 95.0},
                        "top_n": {"type": "integer", "default": 10},
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

            analysis = config.get("analysis", {})
            threshold = analysis.get("threshold", 95.0)
            top_n = analysis.get("top_n", 10)

            handle = api.get_model_handle(model_rid)
            result = api.run_power_flow(model_handle=handle)

            if not result.is_success:
                self._log("WARNING", "Power flow did not converge, using raw data")

            bus_data = result.data.get("bus_results", []) if result.data else []
            branch_data = result.data.get("branch_results", []) if result.data else []

            weakness_calc = BusWeaknessIndex()
            weak_buses = weakness_calc.identify(
                bus_data,
                branch_data,
                voltage_threshold_pu=threshold / 100.0,
            )

            result_data = {
                "total_buses": len(bus_data),
                "weak_buses_count": len(weak_buses),
                "weak_buses": weak_buses[:top_n],
            }

            self._log("INFO", f"Found {len(weak_buses)} weak buses")

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
            self._log("ERROR", f"VSI weak bus analysis failed: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error=str(e),
                logs=self.logs,
                start_time=start_time,
                end_time=datetime.now(),
            )


__all__ = ["VSIWeakBusAnalysis"]
