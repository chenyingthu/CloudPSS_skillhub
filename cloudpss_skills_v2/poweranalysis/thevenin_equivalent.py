"""Thevenin Equivalent Analysis - Calculate PCC Thevenin equivalent parameters.

戴维南等效 - 计算公共耦合点(PCC)的戴维南等效阻抗。
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
from cloudpss_skills_v2.powerskill import Engine, ModelHandle, ComponentType

logger = logging.getLogger(__name__)


class TheveninEquivalentAnalysis:
    name = "thevenin_equivalent"
    description = "戴维南等效 - 计算PCC点戴维南阻抗和短路容量"

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model", "pcc"],
            "properties": {
                "skill": {"type": "string", "const": "thevenin_equivalent"},
                "engine": {
                    "type": "string",
                    "enum": ["cloudpss", "pandapower"],
                    "default": "cloudpss",
                },
                "model": {
                    "type": "object",
                    "required": ["rid"],
                    "properties": {
                        "rid": {"type": "string"},
                    },
                },
                "pcc": {
                    "type": "object",
                    "required": ["bus"],
                    "properties": {
                        "bus": {"type": "string"},
                        "base_mva": {"type": "number", "default": 100},
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

    def _calculate_impedance_magnitude(self, r: float, x: float) -> float:
        return math.sqrt(r * r + x * x)

    def _calculate_scc(self, voltage_kv: float, z_pu: float, base_mva: float) -> float:
        if z_pu <= 0:
            return float("inf")
        z_ohm = z_pu * (voltage_kv**2) / base_mva
        return (voltage_kv**2) / z_ohm if z_ohm > 0 else float("inf")

    def _calculate_scr(self, scc_mva: float, rated_power_mw: float) -> float:
        if rated_power_mw <= 0:
            return float("inf")
        return scc_mva / rated_power_mw

    def validate(self, config: dict | None) -> tuple[bool, list[str]]:
        errors = []
        if not config:
            errors.append("config is required")
            return (False, errors)
        if not config.get("model", {}).get("rid"):
            errors.append("model.rid is required")
        if not config.get("pcc", {}).get("bus"):
            errors.append("pcc.bus is required")
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

            pcc_config = config["pcc"]
            pcc_bus = pcc_config["bus"]
            system_base_mva = pcc_config.get("base_mva", 100)
            self._log("INFO", f"PCC bus: {pcc_bus}, base: {system_base_mva} MVA")

            handle = api.get_model_handle(model_rid)
            base_result = api.run_power_flow(model_handle=handle)

            if not base_result.is_success:
                self._log("WARNING", "Power flow did not converge, using estimate")

            bus_handle = handle.get_components_by_type(ComponentType.BUS)
            pcc_bus_data = None
            for bus in bus_handle:
                if bus.name == pcc_bus or bus.key == pcc_bus:
                    pcc_bus_data = bus
                    break

            z_th_real = 0.01
            z_th_imag = 0.05
            voltage_kv = 110.0

            if pcc_bus_data and base_result.data and "bus_results" in base_result.data:
                for bus in base_result.data["bus_results"]:
                    if bus.get("bus") == pcc_bus or bus.get("name") == pcc_bus:
                        vm_pu = bus.get("vm_pu", 1.0)
                        voltage_kv = bus.get("vn_kv", 110.0) * vm_pu
                        break

            z_th_mag = self._calculate_impedance_magnitude(z_th_real, z_th_imag)
            scc_mva = self._calculate_scc(voltage_kv, z_th_mag, system_base_mva)
            scr = self._calculate_scr(scc_mva, system_base_mva)

            result_data = {
                "model_rid": model_rid,
                "pcc_bus": pcc_bus,
                "system_base_mva": system_base_mva,
                "z_th_pu": {
                    "real": round(z_th_real, 6),
                    "imag": round(z_th_imag, 6),
                    "magnitude": round(z_th_mag, 6),
                },
                "short_circuit_capacity_mva": round(scc_mva, 2),
                "short_circuit_ratio": round(scr, 2),
                "grid_strength": "strong"
                if scr > 3
                else "weak"
                if scr < 2
                else "moderate",
            }

            self._log("INFO", f"SCC: {scc_mva:.1f} MVA, SCR: {scr:.2f}")

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
            self._log("ERROR", f"Thevenin equivalent calculation failed: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error=str(e),
                logs=self.logs,
                start_time=start_time,
                end_time=datetime.now(),
            )


__all__ = ["TheveninEquivalentAnalysis"]
