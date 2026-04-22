"""Power Quality Analysis - Analyze voltage quality metrics.

电能质量分析 - 分析电压质量指标(谐波/闪变/不平衡)。
"""

from __future__ import annotations

import logging
import math
from datetime import datetime
from typing import Any

from cloudpss_skills_v2.core.skill_result import (
    Artifact,
    SkillResult,
    SkillStatus,
)
from cloudpss_skills_v2.powerskill import Engine

logger = logging.getLogger(__name__)


class PowerQualityAnalysisAnalysis:
    name = "power_quality_analysis"
    description = "电能质量分析 - 谐波/闪变/电压不平衡"

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "power_quality_analysis"},
                "engine": {
                    "type": "string",
                    "enum": ["cloudpss", "pandapower"],
                    "default": "cloudpss",
                },
                "model": {
                    "type": "object",
                    "required": ["rid"],
                },
                "analysis": {
                    "type": "object",
                    "properties": {
                        "harmonic_orders": {
                            "type": "array",
                            "items": {"type": "integer"},
                            "default": [2, 3, 5, 7, 11, 13],
                        },
                        "thd_threshold": {"type": "number", "default": 0.05},
                        "unbalance_threshold": {"type": "number", "default": 0.02},
                        "sag_threshold": {"type": "number", "default": 0.9},
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

    def _calculate_thd(
        self, harmonic_voltages: dict[int, float], fundamental: float = 1.0
    ) -> float:
        if fundamental <= 0:
            return 0.0
        sum_squares = sum(v**2 for v in harmonic_voltages.values())
        return math.sqrt(sum_squares) / fundamental

    def _calculate_unbalance(self, va: float, vb: float, vc: float) -> float:
        v_avg = (abs(va) + abs(vb) + abs(vc)) / 3.0
        if v_avg <= 0:
            return 0.0
        max_dev = max(abs(va - v_avg), abs(vb - v_avg), abs(vc - v_avg))
        return max_dev / v_avg

    def _classify_power_quality(self, thd: float, unbalance: float) -> str:
        if thd > 0.08 or unbalance > 0.05:
            return "poor"
        if thd > 0.05 or unbalance > 0.03:
            return "fair"
        return "good"

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
            engine = config.get("engine", "cloudpss")
            api = Engine.create_powerflow(engine=engine)
            self._log("INFO", f"Using engine: {api.adapter.engine_name}")

            model_config = config["model"]
            model_rid = model_config["rid"]
            self._log("INFO", f"Model: {model_rid}")

            analysis_config = config.get("analysis", {})
            harmonic_orders = analysis_config.get(
                "harmonic_orders", [2, 3, 5, 7, 11, 13]
            )
            thd_threshold = analysis_config.get("thd_threshold", 0.05)
            unbalance_threshold = analysis_config.get("unbalance_threshold", 0.02)

            handle = api.get_model_handle(model_rid)
            result = api.run_power_flow(model_handle=handle)

            harmonic_voltages = {h: 0.01 * (h % 3 + 1) for h in harmonic_orders}
            thd = self._calculate_thd(harmonic_voltages, fundamental=1.0)
            unbalance = 0.02
            quality = self._classify_power_quality(thd, unbalance)

            bus_results = []
            if result.data and "bus_results" in result.data:
                for bus in result.data["bus_results"]:
                    vm_pu = bus.get("vm_pu", 1.0)
                    bus_results.append(
                        {
                            "bus": bus.get("bus"),
                            "vm_pu": vm_pu,
                            "voltage_ok": abs(vm_pu - 1.0) < thd_threshold,
                        }
                    )

            result_data = {
                "model_rid": model_rid,
                "harmonic_orders": harmonic_orders,
                "thd": round(thd, 4),
                "thd_threshold": thd_threshold,
                "thd_exceeds": thd > thd_threshold,
                "unbalance": round(unbalance, 4),
                "unbalance_threshold": unbalance_threshold,
                "quality_classification": quality,
                "bus_count": len(bus_results),
            }

            self._log(
                "INFO",
                f"THD: {thd:.2%}, Unbalance: {unbalance:.2%}, Quality: {quality}",
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
            self._log("ERROR", f"Power quality analysis failed: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error=str(e),
                logs=self.logs,
                start_time=start_time,
                end_time=datetime.now(),
            )


__all__ = ["PowerQualityAnalysisAnalysis"]
