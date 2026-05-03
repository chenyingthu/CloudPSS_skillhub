"""Thevenin Equivalent Analysis - Calculate PCC Thevenin equivalent parameters.

戴维南等效 - 计算公共耦合点(PCC)的戴维南等效阻抗和电压。
"""

from __future__ import annotations

import logging
import math
from datetime import datetime
from typing import Any

import numpy as np

from cloudpss_skills_v2.poweranalysis.base import PowerAnalysis
from cloudpss_skills_v2.core.system_model import PowerSystemModel, Bus

logger = logging.getLogger(__name__)


class TheveninEquivalentAnalysis(PowerAnalysis):
    """Calculate Thevenin equivalent parameters for a target bus.

    The Thevenin equivalent represents the power system as seen from a specific bus:
    - V_th: Open circuit voltage at the target bus (Thevenin voltage)
    - Z_th: Equivalent impedance looking into the network from the target bus

    The calculation uses the network admittance matrix approach:
    1. Build the bus admittance matrix Ybus from branch data
    2. Compute the equivalent impedance as Z_th = 1 / Y_eq
       where Y_eq is the diagonal element of the inverted Ybus (or reduced matrix)
    3. Use the operating voltage as the open-circuit voltage

    Attributes:
        name: Skill identifier
        description: Human-readable description
    """

    name = "thevenin_equivalent"
    description = "戴维南等效 - 计算PCC点戴维南阻抗和开路电压"

    @property
    def config_schema(self) -> dict[str, Any]:
        """JSON Schema for configuration validation."""
        return {
            "type": "object",
            "required": ["target_bus"],
            "properties": {
                "target_bus": {
                    "type": ["string", "integer"],
                    "description": "Target bus name or ID for Thevenin equivalent calculation"
                },
                "include_results": {
                    "type": "boolean",
                    "default": True,
                    "description": "Include detailed intermediate results"
                }
            },
        }

    def get_default_config(self) -> dict[str, Any]:
        """Return default configuration."""
        return {
            "target_bus": "",
            "include_results": True,
        }

    def _validate_config(self, config: dict) -> tuple[bool, str]:
        """Validate the analysis configuration.

        Args:
            config: Configuration dictionary

        Returns:
            Tuple of (is_valid, error_message)
        """
        target_bus = config.get("target_bus")
        if target_bus is None or target_bus == "":
            return False, "target_bus is required (bus name or ID)"
        return True, ""

    def _get_target_bus(self, model: PowerSystemModel, target_bus: str | int) -> Bus | None:
        """Find the target bus by name or ID.

        Args:
            model: PowerSystemModel to search
            target_bus: Bus name (str) or ID (int)

        Returns:
            Bus object if found, None otherwise
        """
        if isinstance(target_bus, int):
            return model.get_bus_by_id(target_bus)
        else:
            return model.get_bus_by_name(target_bus)

    def _build_ybus_matrix(self, model: PowerSystemModel) -> tuple[np.ndarray, dict[int, int]]:
        """Build the bus admittance matrix (Ybus).

        Args:
            model: PowerSystemModel with buses and branches

        Returns:
            Tuple of (Ybus matrix, bus_id to index mapping)
        """
        n_buses = len(model.buses)
        if n_buses == 0:
            return np.array([]), {}

        # Create bus index mapping
        bus_id_to_idx = {bus.bus_id: idx for idx, bus in enumerate(model.buses)}

        # Initialize Ybus matrix (complex)
        Ybus = np.zeros((n_buses, n_buses), dtype=complex)

        # Add branch contributions
        for branch in model.branches:
            if not branch.in_service:
                continue

            from_idx = bus_id_to_idx.get(branch.from_bus)
            to_idx = bus_id_to_idx.get(branch.to_bus)

            if from_idx is None or to_idx is None:
                continue  # Skip branches with invalid bus references

            # Series impedance
            r = branch.r_pu
            x = branch.x_pu

            if r == 0 and x == 0:
                continue  # Skip zero-impedance branches

            z_series = complex(r, x)
            y_series = 1.0 / z_series

            # Shunt admittance (if any)
            y_shunt = complex(branch.g_pu, branch.b_pu) if (branch.g_pu or branch.b_pu) else 0

            # Add to Ybus
            # Diagonal elements
            Ybus[from_idx, from_idx] += y_series + y_shunt / 2
            Ybus[to_idx, to_idx] += y_series + y_shunt / 2

            # Off-diagonal elements
            Ybus[from_idx, to_idx] -= y_series
            Ybus[to_idx, from_idx] -= y_series

        return Ybus, bus_id_to_idx

    def _calculate_thevenin_parameters(
        self,
        model: PowerSystemModel,
        target_bus: Bus
    ) -> dict[str, Any]:
        """Calculate Thevenin equivalent parameters.

        Uses the admittance matrix approach:
        1. Build Ybus from the network topology
        2. Remove the target bus row/column to get reduced Ybus
        3. The equivalent admittance is related to the diagonal element
        4. Calculate Z_th = 1 / Y_eq

        For a simplified calculation:
        - Z_th is approximated from the equivalent impedance seen from the target bus
        - V_th is the open-circuit voltage (approximated by operating voltage)

        Args:
            model: PowerSystemModel
            target_bus: Target bus for Thevenin equivalent

        Returns:
            Dictionary with thevenin_voltage_pu, thevenin_impedance_pu, etc.
        """
        # Build Ybus matrix
        Ybus, bus_id_to_idx = self._build_ybus_matrix(model)

        if Ybus.size == 0:
            raise ValueError("Empty admittance matrix - cannot calculate Thevenin equivalent")

        target_idx = bus_id_to_idx.get(target_bus.bus_id)
        if target_idx is None:
            raise ValueError(f"Target bus {target_bus.name} not found in admittance matrix")

        n_buses = len(model.buses)

        # Method: Use the diagonal element of Zbus (impedance matrix)
        # Zbus = inv(Ybus), and Z_th = Zbus[target_idx, target_idx]
        try:
            # Compute Zbus = Ybus^-1
            Zbus = np.linalg.inv(Ybus)

            # Thevenin impedance is the diagonal element corresponding to target bus
            z_th_complex = Zbus[target_idx, target_idx]

            # Thevenin voltage: use the operating voltage (open circuit approximation)
            v_th_pu = target_bus.v_magnitude_pu if target_bus.v_magnitude_pu is not None else 1.0

            # Extract real and imaginary parts
            z_th_real = float(np.real(z_th_complex))
            z_th_imag = float(np.imag(z_th_complex))
            z_th_mag = float(np.abs(z_th_complex))

        except np.linalg.LinAlgError:
            # Singular matrix - use alternative approach
            # For a simple system, calculate equivalent from connected branches
            connected_branches = model.get_branches_connected_to(target_bus.bus_id)

            if not connected_branches:
                raise ValueError(f"No branches connected to target bus {target_bus.name}")

            # Calculate parallel combination of connected branch impedances
            total_admittance = complex(0, 0)
            for branch in connected_branches:
                if not branch.in_service:
                    continue
                if branch.r_pu == 0 and branch.x_pu == 0:
                    continue
                z_branch = complex(branch.r_pu, branch.x_pu)
                total_admittance += 1.0 / z_branch

            if abs(total_admittance) < 1e-10:
                raise ValueError("Zero total admittance - cannot calculate Thevenin equivalent")

            z_th_complex = 1.0 / total_admittance
            z_th_real = float(np.real(z_th_complex))
            z_th_imag = float(np.imag(z_th_complex))
            z_th_mag = float(np.abs(z_th_complex))

            v_th_pu = target_bus.v_magnitude_pu if target_bus.v_magnitude_pu is not None else 1.0

        # Calculate short circuit capacity
        base_mva = model.base_mva
        if z_th_mag > 0:
            scc_mva = base_mva / z_th_mag
        else:
            scc_mva = float('inf')

        # Determine grid strength based on SCR (assuming some rated power)
        # Using base MVA as reference for SCR calculation
        scr = scc_mva / base_mva if base_mva > 0 else float('inf')

        return {
            "thevenin_voltage_pu": round(v_th_pu, 6),
            "thevenin_impedance_pu": round(z_th_mag, 6),
            "thevenin_impedance_real": round(z_th_real, 6),
            "thevenin_impedance_imag": round(z_th_imag, 6),
            "short_circuit_capacity_mva": round(scc_mva, 2),
            "short_circuit_ratio": round(scr, 2),
            "grid_strength": "strong" if scr > 3 else "weak" if scr < 2 else "moderate",
            "target_bus": target_bus.name,
            "target_bus_id": target_bus.bus_id,
            "base_mva": base_mva,
        }

    def run(self, model: PowerSystemModel, config: dict) -> dict:
        """Run Thevenin equivalent analysis on the unified model.

        Args:
            model: PowerSystemModel containing buses, branches, etc.
            config: Configuration dictionary with:
                - target_bus: str (bus name) or int (bus ID)
                - include_results: bool (optional, default True)

        Returns:
            Analysis results dictionary with:
                - status: "success" or "error"
                - thevenin_voltage_pu: Thevenin voltage in per unit
                - thevenin_impedance_pu: Thevenin impedance magnitude in per unit
                - thevenin_impedance_real: Real part of Thevenin impedance
                - thevenin_impedance_imag: Imaginary part of Thevenin impedance
                - short_circuit_capacity_mva: Short circuit capacity in MVA
                - short_circuit_ratio: Short circuit ratio
                - grid_strength: "strong", "moderate", or "weak"
                - target_bus: Name of the target bus
                - target_bus_id: ID of the target bus
                - base_mva: System base MVA
                - error: Error message (if status is "error")
        """
        # Validate configuration
        is_valid, error_msg = self._validate_config(config)
        if not is_valid:
            return {
                "status": "error",
                "error": error_msg
            }

        # Validate model
        model_errors = self.validate_model(model)
        if model_errors:
            return {
                "status": "error",
                "error": f"Model validation failed: {'; '.join(model_errors)}"
            }

        # Find target bus
        target_bus = self._get_target_bus(model, config["target_bus"])
        if target_bus is None:
            return {
                "status": "error",
                "error": f"Target bus '{config['target_bus']}' not found in model"
            }

        try:
            # Calculate Thevenin equivalent parameters
            result = self._calculate_thevenin_parameters(model, target_bus)
            result["status"] = "success"

            logger.info(
                f"Thevenin equivalent for {target_bus.name}: "
                f"V_th={result['thevenin_voltage_pu']:.4f} pu, "
                f"Z_th={result['thevenin_impedance_pu']:.4f} pu, "
                f"SCC={result['short_circuit_capacity_mva']:.2f} MVA"
            )

            return result

        except Exception as e:
            logger.error(f"Thevenin equivalent calculation failed: {e}")
            return {
                "status": "error",
                "error": f"Calculation failed: {str(e)}"
            }


# Backward compatibility: keep the old class for existing code
class TheveninEquivalentAnalysisLegacy:
    """Legacy Thevenin Equivalent Analysis - for backward compatibility.

    This class maintains the old interface for existing code.
    New code should use TheveninEquivalentAnalysis with PowerSystemModel.
    """

    name = "thevenin_equivalent_legacy"
    description = "戴维南等效 - 计算PCC点戴维南阻抗和短路容量 (Legacy)"

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model", "pcc"],
            "properties": {
                "skill": {"type": "string", "const": "thevenin_equivalent", "default": "thevenin_equivalent"},
                "engine": {
                    "type": "string",
                    "enum": ["cloudpss", "pandapower"],
                    "default": "cloudpss",
                },
                "model": {
                    "type": "object",
                    "required": ["rid"],
                    "properties": {
                        "rid": {"type": "string", "default": "model/holdme/IEEE39"},
                    },
                },
                "pcc": {
                    "type": "object",
                    "required": ["bus"],
                    "properties": {
                        "bus": {"type": "string", "default": ""},
                        "base_mva": {"type": "number", "default": 100},
                    },
                },
                "equivalent": {
                    "type": "object",
                    "properties": {
                        "z_th_pu": {
                            "type": "object",
                            "required": ["real", "imag"],
                            "properties": {
                                "real": {"type": "number"},
                                "imag": {"type": "number"},
                            },
                        },
                        "voltage_kv": {"type": "number"},
                        "source": {"type": "string"},
                    },
                },
            },
        }

    def get_default_config(self) -> dict[str, Any]:
        return {
            "skill": self.name,
            "engine": "cloudpss",
            "model": {"rid": "model/holdme/IEEE39"},
            "pcc": {"bus": "", "base_mva": 100},
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
        z_th = config.get("equivalent", {}).get("z_th_pu")
        if not isinstance(z_th, dict):
            errors.append("equivalent.z_th_pu with real and imag is required")
        else:
            for key in ("real", "imag"):
                if key not in z_th:
                    errors.append(f"equivalent.z_th_pu.{key} is required")
                else:
                    try:
                        float(z_th[key])
                    except (TypeError, ValueError):
                        errors.append(f"equivalent.z_th_pu.{key} must be numeric")
        return (len(errors) == 0, errors)

    def run(self, config: dict | None) -> Any:
        """Legacy run method - requires CloudPSS API."""
        from cloudpss_skills_v2.core.skill_result import (
            SkillResult,
            SkillStatus,
        )
        from cloudpss_skills_v2.powerskill import Engine, ComponentType

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

            equivalent_config = config["equivalent"]
            z_th_input = equivalent_config["z_th_pu"]
            z_th_real = float(z_th_input["real"])
            z_th_imag = float(z_th_input["imag"])
            voltage_kv = float(equivalent_config.get("voltage_kv", 110.0))

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
                "grid_strength": "strong" if scr > 3 else "weak" if scr < 2 else "moderate",
                "data_source": equivalent_config.get("source", "explicit_thevenin_impedance"),
                "confidence_level": "formula_derived_from_explicit_input",
                "validation_status": "explicit_input_required",
                "standard_basis": (
                    "IEC 60909 short-circuit capacity convention; per-unit "
                    "Thevenin impedance arithmetic"
                ),
                "assumptions": [
                    "z_th_pu is supplied by the caller from a trusted short-circuit or Thevenin study",
                    "short-circuit capacity is calculated as base_mva / |z_th_pu|",
                ],
                "limitations": [
                    "The skill does not derive z_th_pu from the network model",
                    "Voltage correction factors, X/R effects, and current-source contributions are outside this calculation",
                ],
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


__all__ = ["TheveninEquivalentAnalysis", "TheveninEquivalentAnalysisLegacy"]
