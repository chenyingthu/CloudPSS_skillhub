"""Fault severity scan analysis.

This module provides a deterministic severity scan over fault clearing or
voltage-drop values. It is intentionally local and bounded so it can be covered
by integration tests without requiring an EMT service.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

import numpy as np

from cloudpss_skills_v2.core import SkillResult, SkillStatus


class FaultSeverityScanAnalysis:
    name = "fault_severity_scan"
    description = "故障严重度扫描 - 评估不同故障参数下的电压跌落严重度"

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["model", "scan"],
            "properties": {
                "model": {"type": "object", "required": ["rid"]},
                "fault": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string"},
                        "reference_voltage": {"type": "number", "default": 1.0},
                    },
                },
                "scan": {
                    "type": "object",
                    "properties": {
                        "chg_values": {"type": "array", "items": {"type": "number"}},
                        "voltage_drops": {
                            "type": "array",
                            "items": {"type": "number"},
                        },
                    },
                },
            },
        }

    def get_default_config(self) -> dict[str, Any]:
        return {
            "skill": self.name,
            "model": {"rid": ""},
            "fault": {"location": "", "reference_voltage": 1.0},
            "scan": {"chg_values": [], "voltage_drops": []},
        }

    def validate(self, config: dict[str, Any] | None = None) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if not isinstance(config, dict):
            return False, ["config must be a dictionary"]

        model = config.get("model")
        if not isinstance(model, dict) or not model.get("rid"):
            errors.append("model.rid is required")

        scan = config.get("scan")
        if not isinstance(scan, dict):
            errors.append("scan is required")
        else:
            values = scan.get("chg_values") or scan.get("voltage_drops")
            if not isinstance(values, list) or not values:
                errors.append("scan.chg_values or scan.voltage_drops is required")

        return len(errors) == 0, errors

    def _calculate_severity(
        self, voltage_drop: float | None = None, reference_voltage: float | None = None
    ) -> float:
        reference = float(reference_voltage or 0.0)
        if reference == 0:
            return 0.0
        return abs(float(voltage_drop or 0.0)) / reference

    def _assess_severity_level(self, severity_fraction: float | None = None) -> str:
        severity = float(severity_fraction or 0.0)
        if severity < 0.2:
            return "low"
        if severity < 0.6:
            return "moderate"
        return "critical"

    def _calculate_recovery_time(
        self, voltage: Any = None, time: Any = None, threshold: float = 0.9
    ) -> float | None:
        v = np.asarray(voltage if voltage is not None else [], dtype=float)
        t = np.asarray(time if time is not None else [], dtype=float)
        if v.size == 0 or t.size == 0:
            return None

        below = np.where(v < threshold)[0]
        if below.size == 0:
            return float(t[0])

        last_below = int(below[-1])
        if last_below + 1 < t.size:
            return float(t[last_below + 1])
        return float(t[last_below])

    def run(self, config: dict[str, Any] | None = None) -> SkillResult:
        start_time = datetime.now()
        config = config or {}
        valid, errors = self.validate(config)
        if not valid:
            return SkillResult.failure(
                skill_name=self.name,
                error="; ".join(errors),
                data={"stage": "validation", "errors": errors},
            )

        fault = config.get("fault", {})
        scan = config.get("scan", {})
        reference_voltage = float(fault.get("reference_voltage", 1.0))
        values = scan.get("voltage_drops") or scan.get("chg_values") or []

        results = []
        for index, value in enumerate(values):
            severity = self._calculate_severity(value, reference_voltage)
            results.append(
                {
                    "index": index,
                    "fault_parameter": float(value),
                    "severity": severity,
                    "severity_level": self._assess_severity_level(severity),
                }
            )

        worst = max(results, key=lambda item: item["severity"]) if results else None
        return SkillResult(
            skill_name=self.name,
            status=SkillStatus.SUCCESS,
            data={
                "model_rid": config["model"]["rid"],
                "fault_location": fault.get("location", "unknown"),
                "reference_voltage": reference_voltage,
                "results": results,
                "worst_case": worst,
                "critical_count": len(
                    [item for item in results if item["severity_level"] == "critical"]
                ),
            },
            metrics={"scan_count": len(results)},
            start_time=start_time,
            end_time=datetime.now(),
        )


__all__ = ["FaultSeverityScanAnalysis"]
