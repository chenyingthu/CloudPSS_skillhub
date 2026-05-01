"""Renewable integration analysis for CloudPSS SkillHub v2.

This skill evaluates grid strength (SCR), harmonic distortion, LVRT ride-through
performance, and renewable capacity utilization using standardized result
payloads compatible with the v2 output contract.
"""

from __future__ import annotations

import logging
import math
import uuid
from datetime import datetime
from typing import Any

from cloudpss_skills_v2.core.skill_result import LogEntry, SkillResult, SkillStatus
from cloudpss_skills_v2.powerskill import Engine

logger = logging.getLogger(__name__)


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        number = float(value)
        if math.isnan(number) or math.isinf(number):
            return default
        return number
    except (TypeError, ValueError):
        return default


def classify_grid_strength(scr: float) -> str:
    if scr >= 3.0:
        return "strong"
    if scr >= 2.0:
        return "moderate"
    return "weak"


def compute_scr(short_circuit_mva: float, renewable_mw: float, base_mva: float = 100.0) -> float:
    del base_mva
    if renewable_mw <= 0:
        return 0.0
    return short_circuit_mva / renewable_mw


class RenewableIntegrationAnalysis:
    name = "renewable_integration"
    description = "Renewable integration assessment for SCR, THD, LVRT, and capacity"

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "renewable_integration", "default": "renewable_integration"},
                "engine": {
                    "type": "string",
                    "enum": ["cloudpss", "pandapower"],
                    "default": "pandapower",
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
                "renewable": {
                    "type": "object",
                    "properties": {
                        "type": {
                            "type": "string",
                            "enum": ["pv", "wind", "hybrid"],
                            "default": "pv",
                        },
                        "capacity_mw": {"type": "number", "default": 50.0},
                        "short_circuit_mva": {"type": "number", "default": 1000.0},
                        "point_of_interconnection": {"type": "string", "default": ""},
                        "capacity_series_mw": {"type": "array", "items": {"type": "number"}, "default": []},
                    },
                },
                "harmonics": {
                    "type": "object",
                    "properties": {
                        "fundamental_voltage": {"type": "number", "default": 1.0},
                        "orders": {"type": "object", "default": {}},
                        "limit_thd": {"type": "number", "default": 0.05},
                    },
                },
                "lvrt": {
                    "type": "object",
                    "properties": {
                        "profile": {"type": "array", "items": {"type": "object"}, "default": []},
                        "min_voltage_pu": {"type": "number", "default": 0.15},
                        "max_recovery_time_s": {"type": "number", "default": 1.5},
                    },
                },
                "analysis": {
                    "type": "object",
                    "properties": {
                        "min_scr": {"type": "number", "default": 2.0},
                        "target_capacity_factor": {"type": "number", "default": 0.25},
                    },
                },
            },
        }

    def __init__(self):
        self.logs: list[LogEntry] = []

    def _log(self, level: str, message: str) -> None:
        self.logs.append(LogEntry(timestamp=datetime.now(), level=level, message=message))
        getattr(logger, level.lower(), logger.info)(message)

    def get_default_config(self) -> dict[str, Any]:
        return {
            "skill": self.name,
            "engine": "pandapower",
            "auth": {"token": "local-pandapower-token"},
            "model": {"rid": "case14", "source": "local"},
            "renewable": {
                "type": "pv",
                "capacity_mw": 50.0,
                "short_circuit_mva": 1000.0,
                "point_of_interconnection": "",
                "capacity_series_mw": [],
            },
            "harmonics": {
                "fundamental_voltage": 1.0,
                "orders": {},
                "limit_thd": 0.05,
            },
            "lvrt": {
                "profile": [],
                "min_voltage_pu": 0.15,
                "max_recovery_time_s": 1.5,
            },
            "analysis": {"min_scr": 2.0, "target_capacity_factor": 0.25},
        }

    def validate(self, config: dict[str, Any] | None) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if not isinstance(config, dict):
            return False, ["config must be a dict"]

        if not config.get("model", {}).get("rid"):
            errors.append("model.rid is required")

        renewable = config.get("renewable", {}) or {}
        if _as_float(renewable.get("capacity_mw", 0), 0) <= 0:
            errors.append("renewable.capacity_mw must be positive")
        if _as_float(renewable.get("short_circuit_mva", 0), 0) <= 0:
            errors.append("renewable.short_circuit_mva must be positive")
        capacity_series = renewable.get("capacity_series_mw")
        if not isinstance(capacity_series, list) or not capacity_series:
            errors.append("renewable.capacity_series_mw must be a non-empty list")
        else:
            for idx, value in enumerate(capacity_series):
                if _as_float(value, -1.0) < 0:
                    errors.append(f"renewable.capacity_series_mw[{idx}] must be non-negative")

        harmonics = config.get("harmonics", {}) or {}
        if _as_float(harmonics.get("fundamental_voltage", 1.0), 1.0) <= 0:
            errors.append("harmonics.fundamental_voltage must be positive")
        if _as_float(harmonics.get("limit_thd", 0.05), 0.05) <= 0:
            errors.append("harmonics.limit_thd must be positive")
        orders = harmonics.get("orders")
        if not isinstance(orders, dict) or not orders:
            errors.append("harmonics.orders must be a non-empty object")

        lvrt = config.get("lvrt", {}) or {}
        profile = lvrt.get("profile")
        if not isinstance(profile, list) or not profile:
            errors.append("lvrt.profile must be a non-empty list")
        for idx, point in enumerate(profile if isinstance(profile, list) else []):
            if not isinstance(point, dict):
                errors.append(f"lvrt.profile[{idx}] must be an object")
                continue
            if "time_s" not in point or "voltage_pu" not in point:
                errors.append(f"lvrt.profile[{idx}] requires time_s and voltage_pu")

        return len(errors) == 0, errors

    def run(self, config: dict[str, Any] | None) -> SkillResult:
        start_time = datetime.now()
        self.logs = []
        config = config or {}

        valid, errors = self.validate(config)
        if not valid:
            return self._failure("; ".join(errors), start_time)

        try:
            engine = config.get("engine", "pandapower")
            model_rid = config["model"]["rid"]
            api = Engine.create_powerflow(engine=engine)
            self._log("INFO", f"Using engine: {api.adapter.engine_name}")
            handle = api.get_model_handle(model_rid)
            pf_result = api.run_power_flow(model_handle=handle)

            renewable = config.get("renewable", {}) or {}
            harmonics = config.get("harmonics", {}) or {}
            lvrt = config.get("lvrt", {}) or {}
            analysis = config.get("analysis", {}) or {}

            scr_result = self._analyze_scr(renewable, analysis)
            harmonic_result = self._analyze_harmonics(harmonics)
            lvrt_result = self._analyze_lvrt(lvrt)
            capacity_result = self._analyze_capacity(renewable, analysis)

            checks = [
                scr_result["passed"],
                harmonic_result["passed"],
                lvrt_result["passed"],
                capacity_result["passed"],
            ]
            passed = all(checks)

            data = {
                "skill_name": self.name,
                "execution_id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "success": passed,
                "message": "Renewable integration analysis completed",
                "model_info": {
                    "rid": model_rid,
                    "engine": api.adapter.engine_name,
                    "power_flow_converged": bool(pf_result.is_success),
                    "point_of_interconnection": renewable.get("point_of_interconnection"),
                },
                "analysis_type": "renewable_integration",
                "data_source": {
                    "scr": "renewable.short_circuit_mva",
                    "harmonics": "harmonics.orders",
                    "lvrt": "lvrt.profile",
                    "capacity": "renewable.capacity_series_mw",
                },
                "confidence_level": "formula_derived_from_explicit_input",
                "validation_status": "explicit_inputs_required",
                "standard_basis": (
                    "SCR grid-strength screening, IEEE 519/IEC-style THD "
                    "convention, configured LVRT thresholds, and capacity-factor arithmetic"
                ),
                "assumptions": [
                    "renewable.short_circuit_mva is supplied from a trusted upstream short-circuit study",
                    "harmonics.orders, lvrt.profile, and renewable.capacity_series_mw are explicit measurements or study results",
                ],
                "limitations": [
                    "The skill does not certify regional grid-code compliance or inverter control performance",
                    "LVRT pass/fail checks the configured profile and thresholds only",
                ],
                "results": {
                    "scr": scr_result,
                    "harmonics": harmonic_result,
                    "lvrt": lvrt_result,
                    "capacity": capacity_result,
                },
                "summary": {
                    "overall_passed": passed,
                    "failed_checks": [
                        name
                        for name, result in {
                            "scr": scr_result,
                            "harmonics": harmonic_result,
                            "lvrt": lvrt_result,
                            "capacity": capacity_result,
                        }.items()
                        if not result["passed"]
                    ],
                    "recommendations": self._build_recommendations(
                        scr_result, harmonic_result, lvrt_result, capacity_result
                    ),
                },
            }

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS if passed else SkillStatus.FAILED,
                data=data,
                logs=self.logs,
                metrics={
                    "scr": scr_result["scr"],
                    "thd": harmonic_result["thd"],
                    "capacity_factor": capacity_result["capacity_factor"],
                },
                error=None if passed else "Renewable integration checks failed",
                start_time=start_time,
                end_time=datetime.now(),
            )
        except Exception as exc:
            self._log("ERROR", f"Renewable integration analysis failed: {exc}")
            return self._failure(str(exc), start_time)

    def _failure(self, error: str, start_time: datetime) -> SkillResult:
        return SkillResult(
            skill_name=self.name,
            status=SkillStatus.FAILED,
            data={
                "skill_name": self.name,
                "execution_id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "success": False,
                "message": error,
            },
            error=error,
            logs=self.logs,
            start_time=start_time,
            end_time=datetime.now(),
        )

    def _analyze_scr(self, renewable: dict[str, Any], analysis: dict[str, Any]) -> dict[str, Any]:
        capacity_mw = _as_float(renewable.get("capacity_mw", 0), 0)
        short_circuit_mva = _as_float(renewable.get("short_circuit_mva", 0), 0)
        min_scr = _as_float(analysis.get("min_scr", 2.0), 2.0)
        scr = compute_scr(short_circuit_mva, capacity_mw)
        return {
            "short_circuit_mva": short_circuit_mva,
            "capacity_mw": capacity_mw,
            "scr": round(scr, 4),
            "minimum_scr": min_scr,
            "grid_strength": classify_grid_strength(scr),
            "passed": scr >= min_scr,
        }

    def _analyze_harmonics(self, harmonics: dict[str, Any]) -> dict[str, Any]:
        fundamental = _as_float(harmonics.get("fundamental_voltage", 1.0), 1.0)
        orders = harmonics.get("orders", {}) or {}
        squared_sum = 0.0
        normalized_orders: list[dict[str, float]] = []
        for order, magnitude in orders.items():
            magnitude_value = _as_float(magnitude, 0)
            squared_sum += magnitude_value**2
            normalized_orders.append({"order": int(order), "magnitude": round(magnitude_value, 6)})
        thd = math.sqrt(squared_sum) / fundamental if fundamental > 0 else 0.0
        limit_thd = _as_float(harmonics.get("limit_thd", 0.05), 0.05)
        return {
            "fundamental_voltage": round(fundamental, 6),
            "orders": sorted(normalized_orders, key=lambda item: item["order"]),
            "thd": round(thd, 6),
            "limit_thd": limit_thd,
            "passed": thd <= limit_thd,
        }

    def _analyze_lvrt(self, lvrt: dict[str, Any]) -> dict[str, Any]:
        profile = sorted(
            lvrt.get("profile", []) or [], key=lambda item: _as_float(item.get("time_s", 0), 0)
        )
        min_voltage_allowed = _as_float(lvrt.get("min_voltage_pu", 0.15), 0.15)
        max_recovery_time = _as_float(lvrt.get("max_recovery_time_s", 1.5), 1.5)
        min_voltage = min(_as_float(point.get("voltage_pu", 1.0), 1.0) for point in profile)
        recovery_time = next(
            (
                _as_float(point.get("time_s", 0), 0)
                for point in profile
                if _as_float(point.get("voltage_pu", 0), 0) >= 0.9
            ),
            max_recovery_time + 999.0,
        )
        passed = min_voltage >= min_voltage_allowed and recovery_time <= max_recovery_time
        return {
            "profile": [
                {
                    "time_s": round(_as_float(point.get("time_s", 0), 0), 6),
                    "voltage_pu": round(_as_float(point.get("voltage_pu", 0), 0), 6),
                }
                for point in profile
            ],
            "minimum_voltage_observed": round(min_voltage, 6),
            "minimum_voltage_required": min_voltage_allowed,
            "recovery_time_s": round(recovery_time, 6),
            "maximum_recovery_time_s": max_recovery_time,
            "passed": passed,
        }

    def _analyze_capacity(
        self, renewable: dict[str, Any], analysis: dict[str, Any]
    ) -> dict[str, Any]:
        capacity_mw = _as_float(renewable.get("capacity_mw", 0), 0)
        series = renewable.get("capacity_series_mw", []) or []
        capacity_series = [_as_float(value, 0) for value in series if _as_float(value, 0) >= 0]
        average_output = sum(capacity_series) / len(capacity_series) if capacity_series else 0.0
        capacity_factor = average_output / capacity_mw if capacity_mw > 0 else 0.0
        target = _as_float(analysis.get("target_capacity_factor", 0.25), 0.25)
        return {
            "capacity_mw": capacity_mw,
            "average_output_mw": round(average_output, 6),
            "capacity_factor": round(capacity_factor, 6),
            "target_capacity_factor": target,
            "series_points": len(capacity_series),
            "passed": capacity_factor >= target,
        }

    def _build_recommendations(
        self,
        scr_result: dict[str, Any],
        harmonic_result: dict[str, Any],
        lvrt_result: dict[str, Any],
        capacity_result: dict[str, Any],
    ) -> list[str]:
        recommendations = []
        if not scr_result["passed"]:
            recommendations.append(
                "Increase short-circuit strength or reduce renewable capacity at the PCC"
            )
        if not harmonic_result["passed"]:
            recommendations.append("Add harmonic filtering or update converter switching strategy")
        if not lvrt_result["passed"]:
            recommendations.append(
                "Tune LVRT controls to improve minimum voltage tolerance or recovery speed"
            )
        if not capacity_result["passed"]:
            recommendations.append(
                "Review energy yield assumptions and curtailment strategy for better utilization"
            )
        return recommendations or ["All renewable integration checks passed"]

    def _calculate_scr_at_buses(
        self, buses: list[dict[str, Any]], renewable_mw: float
    ) -> list[dict[str, Any]]:
        results = []
        for bus in buses:
            sc_mva = _as_float(bus.get("sc_mva", 0), 0)
            scr = compute_scr(sc_mva, renewable_mw)
            results.append(
                {
                    "bus": bus.get("name", "unknown"),
                    "short_circuit_mva": sc_mva,
                    "scr": scr,
                    "strength": classify_grid_strength(scr),
                }
            )
        return results


__all__ = ["RenewableIntegrationAnalysis", "classify_grid_strength", "compute_scr"]
