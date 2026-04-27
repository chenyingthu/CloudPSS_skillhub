"""Protection coordination analysis for CloudPSS SkillHub v2.

The skill calculates relay pickup settings, IEC inverse-time TCC points,
primary/backup coordination margins, and basic distance-protection zone
coverage. It can work from explicit relay definitions in the config and also
touches the configured PowerFlow engine so integration failures are surfaced
instead of silently returning mock data.
"""

from __future__ import annotations

import logging
import math
import uuid
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any

from cloudpss_skills_v2.core.skill_result import LogEntry, SkillResult, SkillStatus
from cloudpss_skills_v2.powerskill import Engine

logger = logging.getLogger(__name__)


class ProtectionType(Enum):
    DISTANCE = "distance"
    OVERCURRENT = "overcurrent"
    DIFFERENTIAL = "differential"
    ZERO_SEQUENCE = "zero_sequence"


@dataclass
class RelaySettings:
    relay_id: str
    relay_type: str = ProtectionType.OVERCURRENT.value
    location: str = ""
    protected_element: str = ""
    pickup_current: float = 0.0
    time_dial: float = 0.1
    time_delay: float = 0.0
    curve_type: str = "iec_standard_inverse"
    fault_current: float = 0.0
    load_current: float = 0.0


@dataclass
class CoordinationResult:
    primary_relay: str
    backup_relay: str
    primary_time: float
    backup_time: float
    coordination_time: float
    required_margin: float
    is_valid: bool


IEC_CURVE_CONSTANTS: dict[str, tuple[float, float]] = {
    "iec_standard_inverse": (0.14, 0.02),
    "iec_very_inverse": (13.5, 1.0),
    "iec_extremely_inverse": (80.0, 2.0),
}


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


def _round(value: float, ndigits: int = 4) -> float:
    return round(float(value), ndigits)


class ProtectionCoordinationAnalysis:
    """Relay setting and coordination analysis."""

    name = "protection_coordination"
    description = "Relay protection setting calculation and coordination validation"

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "protection_coordination"},
                "engine": {
                    "type": "string",
                    "enum": ["cloudpss", "pandapower"],
                    "default": "pandapower",
                },
                "model": {"type": "object", "required": ["rid"]},
                "relays": {"type": "array", "items": {"type": "object"}},
                "coordination_pairs": {"type": "array", "items": {"type": "object"}},
                "analysis": {
                    "type": "object",
                    "properties": {
                        "min_coordination_margin_s": {"type": "number", "default": 0.3},
                        "max_coordination_margin_s": {"type": "number", "default": 0.5},
                        "load_multiplier": {"type": "number", "default": 1.25},
                        "fault_current_safety_factor": {"type": "number", "default": 0.5},
                        "curve_multiples": {
                            "type": "array",
                            "items": {"type": "number"},
                            "default": [1.5, 2, 3, 5, 8, 10, 15, 20],
                        },
                        "zones": {"type": "array", "items": {"type": "object"}},
                    },
                },
            },
        }

    def __init__(self, name: str | None = None):
        if name:
            self.name = name
        self.logs: list[LogEntry] = []

    def _log(self, level: str, message: str) -> None:
        self.logs.append(LogEntry(timestamp=datetime.now(), level=level, message=message))
        getattr(logger, level.lower(), logger.info)(message)

    def get_default_config(self) -> dict[str, Any]:
        return {
            "skill": self.name,
            "engine": "pandapower",
            "model": {"rid": "case14"},
            "analysis": {
                "min_coordination_margin_s": 0.3,
                "max_coordination_margin_s": 0.5,
                "load_multiplier": 1.25,
                "fault_current_safety_factor": 0.5,
                "curve_multiples": [1.5, 2, 3, 5, 8, 10, 15, 20],
            },
        }

    def validate(self, config: dict[str, Any] | None) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if not isinstance(config, dict):
            return False, ["config must be a dict"]

        if not config.get("model", {}).get("rid"):
            errors.append("model.rid is required")

        analysis = config.get("analysis", {}) or {}
        min_margin = _as_float(analysis.get("min_coordination_margin_s", 0.3), 0.3)
        max_margin = _as_float(analysis.get("max_coordination_margin_s", 0.5), 0.5)
        if min_margin <= 0:
            errors.append("analysis.min_coordination_margin_s must be positive")
        if max_margin < min_margin:
            errors.append("analysis.max_coordination_margin_s must be >= min_coordination_margin_s")
        if _as_float(analysis.get("load_multiplier", 1.25), 1.25) <= 0:
            errors.append("analysis.load_multiplier must be positive")
        if _as_float(analysis.get("fault_current_safety_factor", 0.5), 0.5) <= 0:
            errors.append("analysis.fault_current_safety_factor must be positive")

        relays = config.get("relays")
        if not isinstance(relays, list) or not relays:
            errors.append("relays must be a non-empty list")
        for idx, relay in enumerate(relays if isinstance(relays, list) else []):
            if not isinstance(relay, dict):
                errors.append(f"relays[{idx}] must be an object")
                continue
            relay_type = relay.get(
                "type", relay.get("relay_type", ProtectionType.OVERCURRENT.value)
            )
            if relay_type not in {item.value for item in ProtectionType}:
                errors.append(f"relays[{idx}].type is invalid")
            if _as_float(relay.get("load_current", relay.get("load_current_a", 0)), 0) < 0:
                errors.append(f"relays[{idx}].load_current must be non-negative")
            if _as_float(relay.get("fault_current", relay.get("fault_current_a", 0)), 0) < 0:
                errors.append(f"relays[{idx}].fault_current must be non-negative")
            if _as_float(relay.get("load_current", relay.get("load_current_a", 0)), 0) <= 0:
                errors.append(f"relays[{idx}].load_current must be positive")
            if _as_float(relay.get("fault_current", relay.get("fault_current_a", 0)), 0) <= 0:
                errors.append(f"relays[{idx}].fault_current must be positive")

        pairs = config.get("coordination_pairs", []) or []
        if not isinstance(pairs, list):
            errors.append("coordination_pairs must be a list")
        for idx, pair in enumerate(pairs if isinstance(pairs, list) else []):
            if not isinstance(pair, dict) or not pair.get("primary") or not pair.get("backup"):
                errors.append(f"coordination_pairs[{idx}] requires primary and backup")

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

            analysis = config.get("analysis", {}) or {}
            relays = config["relays"]
            settings = [self._calculate_relay_settings(relay, analysis) for relay in relays]
            settings_by_id = {setting.relay_id: setting for setting in settings}
            coordination = self._check_coordination(settings_by_id, config, analysis)
            tcc_curves = self._generate_tcc_curves(settings, analysis)
            zones = self._validate_zones(analysis.get("zones", []), settings_by_id)

            total_pairs = len(coordination)
            valid_pairs = sum(1 for item in coordination if item.is_valid)
            has_failed_zone = any(not zone["is_valid"] for zone in zones)
            passed = (total_pairs == 0 or valid_pairs == total_pairs) and not has_failed_zone

            data = {
                "skill_name": self.name,
                "execution_id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "success": passed,
                "message": "Protection coordination analysis completed",
                "model_info": {
                    "rid": model_rid,
                    "engine": api.adapter.engine_name,
                    "power_flow_converged": bool(pf_result.is_success),
                },
                "analysis_type": "protection_coordination",
                "data_source": "explicit_relay_settings",
                "confidence_level": "formula_derived_from_explicit_input",
                "validation_status": "explicit_relays_required",
                "standard_basis": (
                    "IEC 60255 / IEC 60255-151 inverse-time overcurrent "
                    "curve family for supported IEC curve constants"
                ),
                "assumptions": [
                    "relay load_current, fault_current, time_dial, and curve_type are supplied by the caller",
                    "pickup and operating time are formula-derived from explicit relay settings",
                ],
                "limitations": [
                    "The skill does not model CT saturation, breaker clearing time, reset behavior, or protection-device dynamics",
                    "Distance-zone checks are configured reach checks, not a full protection simulation",
                ],
                "relay_count": len(settings),
                "coordination_pair_count": total_pairs,
                "valid_coordination_pairs": valid_pairs,
                "invalid_coordination_pairs": total_pairs - valid_pairs,
                "settings": [setting.__dict__ for setting in settings],
                "coordination_results": [item.__dict__ for item in coordination],
                "tcc_curves": tcc_curves,
                "zone_validation": zones,
                "summary": {
                    "overall_passed": passed,
                    "min_coordination_margin_s": _as_float(
                        analysis.get("min_coordination_margin_s", 0.3), 0.3
                    ),
                    "recommendations": self._build_recommendations(coordination, zones),
                },
            }

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS if passed else SkillStatus.FAILED,
                data=data,
                logs=self.logs,
                metrics={
                    "relay_count": len(settings),
                    "coordination_pair_count": total_pairs,
                    "pass_rate": valid_pairs / total_pairs if total_pairs else 1.0,
                },
                error=(
                    None if passed else "Protection coordination margins or zones failed validation"
                ),
                start_time=start_time,
                end_time=datetime.now(),
            )
        except Exception as exc:
            self._log("ERROR", f"Protection coordination failed: {exc}")
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

    def _calculate_relay_settings(
        self, relay: dict[str, Any], analysis: dict[str, Any]
    ) -> RelaySettings:
        relay_id = str(
            relay.get("id")
            or relay.get("name")
            or relay.get("relay_id")
            or f"relay_{uuid.uuid4().hex[:8]}"
        )
        relay_type = relay.get("type", relay.get("relay_type", ProtectionType.OVERCURRENT.value))
        load_current = _as_float(relay.get("load_current", relay.get("load_current_a", 0)), 0)
        fault_current = _as_float(relay.get("fault_current", relay.get("fault_current_a", 0)), 0)
        load_multiplier = _as_float(analysis.get("load_multiplier", 1.25), 1.25)
        fault_factor = _as_float(analysis.get("fault_current_safety_factor", 0.5), 0.5)
        configured_pickup = _as_float(
            relay.get("pickup_current", relay.get("pickup_current_a", 0)), 0
        )
        pickup_current = configured_pickup or max(
            load_current * load_multiplier, fault_current * fault_factor * 0.1, 1.0
        )
        curve_type = relay.get("curve_type", "iec_standard_inverse")
        time_dial = _as_float(relay.get("time_dial", relay.get("tds", 0.1)), 0.1)
        operating_time = self._calculate_operating_time(
            fault_current, pickup_current, time_dial, curve_type
        )
        return RelaySettings(
            relay_id=relay_id,
            relay_type=str(relay_type),
            location=str(relay.get("location", "")),
            protected_element=str(relay.get("protected_element", relay.get("element", ""))),
            pickup_current=_round(pickup_current),
            time_dial=_round(time_dial),
            time_delay=_round(operating_time),
            curve_type=str(curve_type),
            fault_current=_round(fault_current),
            load_current=_round(load_current),
        )

    def _calculate_operating_time(
        self, fault_current: float, pickup_current: float, time_dial: float, curve_type: str
    ) -> float:
        if pickup_current <= 0 or fault_current <= pickup_current:
            return float("inf")
        constant_a, constant_b = IEC_CURVE_CONSTANTS.get(
            curve_type, IEC_CURVE_CONSTANTS["iec_standard_inverse"]
        )
        multiple = fault_current / pickup_current
        denominator = multiple**constant_b - 1.0
        if denominator <= 0:
            return float("inf")
        return constant_a * time_dial / denominator

    def _check_coordination(
        self,
        settings_by_id: dict[str, RelaySettings],
        config: dict[str, Any],
        analysis: dict[str, Any],
    ) -> list[CoordinationResult]:
        min_margin = _as_float(analysis.get("min_coordination_margin_s", 0.3), 0.3)
        pairs = config.get("coordination_pairs", []) or []
        if not pairs:
            relay_ids = list(settings_by_id)
            pairs = [
                {"primary": relay_ids[idx], "backup": relay_ids[idx + 1]}
                for idx in range(len(relay_ids) - 1)
            ]

        results: list[CoordinationResult] = []
        for pair in pairs:
            primary = settings_by_id.get(str(pair.get("primary")))
            backup = settings_by_id.get(str(pair.get("backup")))
            if primary is None or backup is None:
                continue
            primary_time = _as_float(
                pair.get("primary_time", primary.time_delay), primary.time_delay
            )
            backup_time = _as_float(pair.get("backup_time", backup.time_delay), backup.time_delay)
            coordination_time = backup_time - primary_time
            results.append(
                CoordinationResult(
                    primary_relay=primary.relay_id,
                    backup_relay=backup.relay_id,
                    primary_time=_round(primary_time),
                    backup_time=_round(backup_time),
                    coordination_time=_round(coordination_time),
                    required_margin=_round(
                        _as_float(pair.get("required_margin", min_margin), min_margin)
                    ),
                    is_valid=coordination_time
                    >= _as_float(pair.get("required_margin", min_margin), min_margin),
                )
            )
        return results

    def _generate_tcc_curves(
        self, settings: list[RelaySettings], analysis: dict[str, Any]
    ) -> list[dict[str, Any]]:
        multiples = analysis.get("curve_multiples", [1.5, 2, 3, 5, 8, 10, 15, 20])
        curves = []
        for setting in settings:
            points = []
            for multiple in multiples:
                multiple_value = _as_float(multiple, 0)
                if multiple_value <= 1:
                    continue
                current = setting.pickup_current * multiple_value
                operating_time = self._calculate_operating_time(
                    current, setting.pickup_current, setting.time_dial, setting.curve_type
                )
                points.append({"current_a": _round(current), "time_s": _round(operating_time)})
            curves.append(
                {
                    "relay": setting.relay_id,
                    "curve_type": setting.curve_type,
                    "pickup_current_a": setting.pickup_current,
                    "points": points,
                }
            )
        return curves

    def _validate_zones(
        self, zones: list[dict[str, Any]], settings_by_id: dict[str, RelaySettings]
    ) -> list[dict[str, Any]]:
        results = []
        for zone in zones or []:
            relay_id = str(zone.get("relay"))
            reach = _as_float(zone.get("reach_percent", 0), 0)
            protected_length = _as_float(zone.get("protected_length", 100), 100)
            expected_reach = _as_float(
                zone.get("expected_reach_percent", zone.get("zone", 1) == 1 and 80 or 120), 80
            )
            tolerance = _as_float(zone.get("tolerance_percent", 10), 10)
            lower = max(0.0, expected_reach - tolerance)
            upper = expected_reach + tolerance
            is_valid = (
                relay_id in settings_by_id and lower <= reach <= upper and protected_length > 0
            )
            results.append(
                {
                    "relay": relay_id,
                    "zone": zone.get("zone", 1),
                    "reach_percent": _round(reach),
                    "expected_reach_percent": _round(expected_reach),
                    "tolerance_percent": _round(tolerance),
                    "is_valid": is_valid,
                }
            )
        return results

    def _build_recommendations(
        self, coordination: list[CoordinationResult], zones: list[dict[str, Any]]
    ) -> list[str]:
        recommendations = []
        for item in coordination:
            if not item.is_valid:
                recommendations.append(
                    f"Increase backup delay for {item.backup_relay} or reduce primary delay for {item.primary_relay}"
                )
        for zone in zones:
            if not zone["is_valid"]:
                recommendations.append(
                    f"Review distance zone {zone['zone']} reach for relay {zone['relay']}"
                )
        return recommendations or ["All configured coordination checks passed"]

    def _calculate_coordination_time(self, backup_time: float, primary_time: float) -> float:
        return backup_time - primary_time

    def _validate_coordination(self, coordination_time: float, min_time: float) -> bool:
        return coordination_time >= min_time

    def _assess_backup_valid(self, backup_ok: bool) -> bool:
        return bool(backup_ok)


__all__ = [
    "ProtectionCoordinationAnalysis",
    "ProtectionType",
    "RelaySettings",
    "CoordinationResult",
]
