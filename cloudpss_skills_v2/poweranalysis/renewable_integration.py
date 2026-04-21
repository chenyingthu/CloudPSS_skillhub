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


def classify_grid_strength(scr: float) -> str:
    if scr >= 3.0:
        return "strong"
    elif scr >= 2.0:
        return "moderate"
    else:
        return "weak"


def compute_scr(
    short_circuit_mva: float, bus_voltage_kv: float, base_mva: float = 100.0
) -> float:
    if bus_voltage_kv <= 0 or base_mva <= 0:
        return 0.0
    return short_circuit_mva / base_mva


class RenewableIntegrationAnalysis:
    name = "renewable_integration"
    description = "新能源并网分析 - 评估新能源接入对电网强度的影响"

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "renewable_integration"},
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
                "renewables": {
                    "type": "object",
                    "properties": {
                        "solar_mw": {"type": "number", "default": 0},
                        "wind_mw": {"type": "number", "default": 0},
                        "buses": {"type": "array", "items": {"type": "string"}},
                    },
                },
                "thresholds": {
                    "type": "object",
                    "properties": {
                        "min_scr": {"type": "number", "default": 2.0},
                        "max_thd": {"type": "number", "default": 0.05},
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

    def _calculate_scr_at_buses(self, buses: list, base_mva: float) -> list:
        results = []
        for bus in buses:
            bus_name = bus.get("name", f"bus_{len(results)}")
            sc_mva = bus.get("sc_mva", 1000.0)
            scr = compute_scr(sc_mva, 1.0, base_mva)
            results.append(
                {
                    "bus": bus_name,
                    "short_circuit_mva": sc_mva,
                    "scr": scr,
                    "strength": classify_grid_strength(scr),
                }
            )
        return results

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

            renewables = config.get("renewables", {})
            solar_mw = renewables.get("solar_mw", 0)
            wind_mw = renewables.get("wind_mw", 0)
            buses = renewables.get("buses", [])

            thresholds = config.get("thresholds", {})
            min_scr = thresholds.get("min_scr", 2.0)

            handle = api.get_model_handle(model_rid)
            result = api.run_power_flow(model_handle=handle)

            if not buses:
                buses = [{"name": "bus1", "sc_mva": 1000.0}]
            scr_results = self._calculate_scr_at_buses(buses, 100.0)

            weak_buses = [r for r in scr_results if r["scr"] < min_scr]
            strong_buses = [
                r for r in scr_results if r["strength"] in ["strong", "moderate"]
            ]

            result_data = {
                "converged": result.is_success,
                "solar_mw": solar_mw,
                "wind_mw": wind_mw,
                "total_renewable_mw": solar_mw + wind_mw,
                "scr_results": scr_results,
                "weak_bus_count": len(weak_buses),
                "strong_bus_count": len(strong_buses),
                "min_scr_threshold": min_scr,
            }

            self._log(
                "INFO",
                f"Renewable integration complete: {len(weak_buses)} weak, {len(strong_buses)} strong",
            )

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
            self._log("ERROR", f"Renewable integration analysis failed: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error=str(e),
                logs=self.logs,
                start_time=start_time,
                end_time=datetime.now(),
            )


__all__ = ["RenewableIntegrationAnalysis", "classify_grid_strength", "compute_scr"]
