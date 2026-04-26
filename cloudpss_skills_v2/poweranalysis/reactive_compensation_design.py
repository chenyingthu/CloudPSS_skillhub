"""Reactive Compensation Design Skill v2."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from cloudpss_skills_v2.core import Artifact, LogEntry, SkillResult, SkillStatus


def _matches_bus_identifier(candidate=None, target=None):
    if candidate is None or target is None:
        return False
    candidate_norm = str(candidate).strip().lower()
    target_norm = str(target).strip().lower()
    if not candidate_norm or not target_norm:
        return False
    if candidate_norm == target_norm:
        return True
    candidate_digits = "".join(ch for ch in candidate_norm if ch.isdigit())
    target_digits = "".join(ch for ch in target_norm if ch.isdigit())
    return bool(candidate_digits and candidate_digits == target_digits)


class ReactiveCompensationDesignAnalysis:
    """Design reactive power compensation for weak buses."""

    name = "reactive_compensation_design"
    description = "Design reactive power compensation for weak buses"

    def __init__(self):
        self.logs: list[LogEntry] = []
        self.artifacts: list[Artifact] = []

    def get_default_config(self):
        return {
            "skill": self.name,
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "", "source": "cloud"},
            "weak_buses": [],
            "vsi_result": {},
            "compensation": {
                "device_type": "sync_compensator",
                "max_capacity_mvar": 100,
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "reactive_compensation",
            },
        }

    def validate(self, config=None):
        errors = []
        if not isinstance(config, dict):
            return False, ["config is required"]
        if not config.get("model", {}).get("rid"):
            errors.append("model.rid is required")
        if not config.get("weak_buses") and not config.get("vsi_result", {}).get("weak_buses"):
            errors.append("Either weak_buses or vsi_result.weak_buses is required")
        for idx, bus in enumerate(self._extract_weak_buses(config) if isinstance(config, dict) else []):
            if not isinstance(bus, dict):
                errors.append(f"weak_buses[{idx}] must be an object")
                continue
            for key in ("scr", "voltage_pu", "x_pu"):
                if key not in bus:
                    errors.append(f"weak_buses[{idx}].{key} is required")
                    continue
                try:
                    value = float(bus[key])
                except (TypeError, ValueError):
                    errors.append(f"weak_buses[{idx}].{key} must be numeric")
                    continue
                if key == "x_pu" and value <= 0:
                    errors.append(f"weak_buses[{idx}].{key} must be positive")
        return len(errors) == 0, errors

    def _calculate_q_required(self, delta_v_pu=None, v_pu=None, x_pu=0.2):
        if not x_pu or x_pu <= 0:
            return 0.0
        return float(v_pu or 0) * float(delta_v_pu or 0) / float(x_pu)

    def _estimate_compensation_size(self, q_required_mvar=None, device_type=None):
        sizing_factors = {
            "sync_compensator": 1.0,
            "svg": 0.9,
            "svc": 0.85,
            "capacitor": 0.7,
        }
        return float(q_required_mvar or 0) * sizing_factors.get(device_type, 1.0)

    def _assess_weakness(self, scr=None, voltage_pu=None):
        scr_value = float(scr or 0)
        voltage_value = float(voltage_pu or 0)
        if scr_value < 3 or voltage_value < 0.93:
            return "weak"
        if scr_value < 10 or voltage_value < 0.97:
            return "moderate"
        return "strong"

    def _extract_weak_buses(self, config: dict[str, Any]) -> list[Any]:
        if config.get("weak_buses"):
            return list(config["weak_buses"])
        return list(config.get("vsi_result", {}).get("weak_buses", []))

    def _bus_value(self, bus: Any, key: str, default: float) -> float:
        if isinstance(bus, dict):
            try:
                return float(bus.get(key, default))
            except (TypeError, ValueError):
                return default
        return default

    def _bus_name(self, bus: Any) -> str:
        if isinstance(bus, dict):
            return str(bus.get("bus") or bus.get("name") or bus.get("id") or "")
        return str(bus)

    def run(self, config=None):
        start_time = datetime.now()
        self.logs = []
        self.artifacts = []
        config = config or {}
        valid, errors = self.validate(config)
        if not valid:
            return SkillResult.failure(
                self.name,
                "; ".join(errors),
                {"stage": "validation", "errors": errors},
            )

        compensation_config = config.get("compensation", {})
        device_type = compensation_config.get("device_type", "sync_compensator")
        max_capacity = float(compensation_config.get("max_capacity_mvar", 100))

        recommendations = []
        for bus in self._extract_weak_buses(config)[:5]:
            bus_name = self._bus_name(bus)
            scr = self._bus_value(bus, "scr", 0.0)
            voltage_pu = self._bus_value(bus, "voltage_pu", 0.0)
            x_pu = self._bus_value(bus, "x_pu", 0.0)
            weakness = self._assess_weakness(scr, voltage_pu)
            q_required = self._calculate_q_required(1.0 - voltage_pu, voltage_pu, x_pu=x_pu)
            q_size = min(self._estimate_compensation_size(q_required, device_type), max_capacity)
            recommendations.append(
                {
                    "bus": bus_name,
                    "weakness": weakness,
                    "scr": round(scr, 2),
                    "voltage_pu": round(voltage_pu, 4),
                    "x_pu": round(x_pu, 4),
                    "required_q_mvar": round(q_required, 2),
                    "recommended_size_mvar": round(q_size, 2),
                    "device_type": device_type,
                }
            )

        total_capacity = sum(item["recommended_size_mvar"] for item in recommendations)
        result_data = {
            "model_rid": config["model"]["rid"],
            "weak_bus_count": len(recommendations),
            "compensation_recommendations": recommendations,
            "total_recommended_capacity_mvar": round(total_capacity, 2),
            "data_source": "weak_buses",
            "confidence_level": "formula_derived_from_explicit_input",
            "validation_status": "explicit_weak_bus_measurements_required",
            "assumptions": [
                "weak_buses entries provide SCR, voltage_pu, and x_pu from a trusted upstream study",
                "required reactive power uses a simplified delta-V over Thevenin-reactance formula",
            ],
        }
        return SkillResult(
            skill_name=self.name,
            status=SkillStatus.SUCCESS,
            data=result_data,
            artifacts=self.artifacts,
            logs=self.logs,
            metrics={
                "buses_compensated": len(recommendations),
                "total_capacity_mvar": result_data["total_recommended_capacity_mvar"],
            },
            start_time=start_time,
            end_time=datetime.now(),
        )


__all__ = ["ReactiveCompensationDesignAnalysis", "_matches_bus_identifier"]
