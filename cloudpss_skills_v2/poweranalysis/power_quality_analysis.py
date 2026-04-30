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
                "skill": {"type": "string", "const": "power_quality_analysis", "default": "power_quality_analysis"},
                "engine": {
                    "type": "string",
                    "enum": ["cloudpss", "pandapower"],
                    "default": "cloudpss",
                },
                "auth": {
                    "type": "object",
                    "properties": {
                        "token": {"type": "string", "default": "local-pandapower-token"},
                    },
                },
                "model": {
                    "type": "object",
                    "required": ["rid"],
                    "properties": {
                        "rid": {"type": "string", "default": "case14"},
                        "source": {"type": "string", "enum": ["cloud", "local"], "default": "local"},
                    },
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
                "measurements": {
                    "type": "object",
                    "properties": {
                        "harmonic_voltages": {"type": "object", "default": {}},
                        "fundamental_voltage": {"type": "number", "default": 1.0},
                        "phase_voltages_pu": {
                            "type": "array",
                            "items": {"type": "number"},
                            "minItems": 3,
                            "maxItems": 3,
                            "default": [1.0, 1.0, 1.0],
                        },
                    },
                },
            },
        }

    def __init__(self):
        self.logs = []
        self.artifacts = []

    def get_default_config(self) -> dict[str, Any]:
        return {
            "skill": self.name,
            "engine": "cloudpss",
            "auth": {"token": "local-pandapower-token"},
            "model": {"rid": "case14", "source": "local"},
            "analysis": {
                "harmonic_orders": [2, 3, 5, 7, 11, 13],
                "thd_threshold": 0.05,
                "unbalance_threshold": 0.02,
                "sag_threshold": 0.9,
            },
            "measurements": {
                "harmonic_voltages": {},
                "fundamental_voltage": 1.0,
                "phase_voltages_pu": [1.0, 1.0, 1.0],
            },
        }

    def validate(self, config: dict | None) -> tuple[bool, list[str]]:

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
        measurements = config.get("measurements")
        if not isinstance(measurements, dict):
            errors.append("measurements with harmonic_voltages and phase_voltages_pu is required")
        else:
            harmonics = measurements.get("harmonic_voltages")
            if not isinstance(harmonics, dict) or not harmonics:
                errors.append("measurements.harmonic_voltages must be a non-empty object")
            else:
                for order, magnitude in harmonics.items():
                    try:
                        int(order)
                        float(magnitude)
                    except (TypeError, ValueError):
                        errors.append("measurements.harmonic_voltages entries must be numeric")
                        break
            phase_voltages = measurements.get("phase_voltages_pu")
            if not isinstance(phase_voltages, list) or len(phase_voltages) != 3:
                errors.append("measurements.phase_voltages_pu must contain 3 values")
            else:
                for value in phase_voltages:
                    try:
                        float(value)
                    except (TypeError, ValueError):
                        errors.append("measurements.phase_voltages_pu values must be numeric")
                        break
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
            auth = config.get("auth", {})
            api = Engine.create_powerflow_for_skill(
                engine=engine,
                base_url=auth.get("base_url"),
                auth=auth,
            )
            self._log("INFO", f"Using engine: {api.adapter.engine_name}")

            model_config = config["model"]
            model_rid = model_config["rid"]
            self._log("INFO", f"Model: {model_rid}")

            analysis_config = config.get("analysis", {})
            harmonic_orders = analysis_config.get("harmonic_orders", [2, 3, 5, 7, 11, 13])
            thd_threshold = analysis_config.get("thd_threshold", 0.05)
            unbalance_threshold = analysis_config.get("unbalance_threshold", 0.02)
            measurements = config["measurements"]

            handle = api.get_model_handle(model_rid)
            result = api.run_power_flow(model_handle=handle)

            harmonic_voltages = {
                int(order): float(value)
                for order, value in measurements["harmonic_voltages"].items()
            }
            fundamental = float(measurements.get("fundamental_voltage", 1.0))
            phase_voltages = [float(value) for value in measurements["phase_voltages_pu"]]
            thd = self._calculate_thd(harmonic_voltages, fundamental=fundamental)
            unbalance = self._calculate_unbalance(*phase_voltages)
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
                "harmonic_voltages": harmonic_voltages,
                "fundamental_voltage": fundamental,
                "thd": round(thd, 4),
                "thd_threshold": thd_threshold,
                "thd_exceeds": thd > thd_threshold,
                "unbalance": round(unbalance, 4),
                "unbalance_threshold": unbalance_threshold,
                "quality_classification": quality,
                "bus_count": len(bus_results),
                "data_source": "measurements",
                "confidence_level": "measurement_derived",
                "validation_status": "explicit_measurements_required",
                "standard_basis": (
                    "IEEE 519/IEC-style THD convention and NEMA "
                    "maximum-deviation voltage unbalance convention"
                ),
                "assumptions": [
                    "harmonic_voltages are per-unit magnitudes relative to fundamental_voltage",
                    "phase_voltages_pu are simultaneous phase RMS voltage measurements",
                ],
                "limitations": [
                    "The skill calculates THD and magnitude unbalance from supplied measurements only",
                    "It does not run a harmonic power-flow simulation or compute sequence-component voltage unbalance",
                ],
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
