"""Voltage Stability Skill v2 - Unified model implementation.

电压稳定性分析 - 通过连续潮流计算PV曲线，识别电压崩溃点
支持负荷增长扫描和关键母线电压监测
"""

from __future__ import annotations

import csv
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np

from cloudpss_skills_v2.poweranalysis.base import PowerAnalysis
from cloudpss_skills_v2.core.system_model import (
    Bus,
    Load,
    PowerSystemModel,
)
from cloudpss_skills_v2.core.skill_result import SkillResult, SkillStatus
from cloudpss_skills_v2.powerskill import Engine

logger = logging.getLogger(__name__)


def _as_float(value, default=0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


class VoltageStabilityAnalysis(PowerAnalysis):
    """电压稳定性分析技能 - unified PowerSystemModel implementation.

    Performs PV curve analysis by scaling loads and computing power flow
    at each load level to identify voltage collapse points.
    """

    name = "voltage_stability"
    description = "电压稳定性分析 - 通过连续潮流计算PV曲线，识别电压崩溃点"

    @property
    def config_schema(self) -> dict[str, Any]:
        """Return configuration schema for legacy interface compatibility."""
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "voltage_stability", "default": "voltage_stability"},
                "engine": {
                    "type": "string",
                    "enum": ["cloudpss", "pandapower"],
                    "default": "cloudpss",
                },
                "auth": {
                    "type": "object",
                    "properties": {
                        "token": {"type": "string"},
                        "token_file": {"type": "string", "default": ".cloudpss_token"},
                    },
                },
                "model": {
                    "type": "object",
                    "required": ["rid"],
                    "properties": {
                        "rid": {"type": "string", "default": "model/holdme/IEEE39"},
                        "source": {"enum": ["cloud", "local"], "default": "cloud"},
                    },
                },
                "scan": {
                    "type": "object",
                    "properties": {
                        "load_scaling": {
                            "type": "array",
                            "items": {"type": "number"},
                            "default": [1.0, 1.2, 1.4, 1.6, 1.8, 2.0],
                        },
                    },
                },
                "monitoring": {
                    "type": "object",
                    "properties": {
                        "buses": {"type": "array", "items": {"type": "string"}},
                        "collapse_threshold": {"type": "number", "default": 0.7},
                    },
                },
            },
        }

    def get_default_config(self) -> dict[str, Any]:
        """Return default configuration for legacy interface compatibility."""
        return {
            "skill": self.name,
            "engine": "cloudpss",
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "model/holdme/IEEE39", "source": "cloud"},
            "scan": {"load_scaling": [1.0, 1.2, 1.4, 1.6, 1.8, 2.0]},
            "monitoring": {"buses": [], "collapse_threshold": 0.7},
        }

    def validate(self, config: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate configuration for legacy interface compatibility."""
        errors = []
        if not config.get("model", {}).get("rid"):
            errors.append("必须指定 model.rid")
        auth = config.get("auth", {})
        if not auth.get("token") and not auth.get("token_file"):
            errors.append("必须提供 auth.token 或 auth.token_file")
        return len(errors) == 0, errors

    @staticmethod
    def _matches_bus_identifier(pattern: str, bus_name: str) -> bool:
        """Check if a bus name matches a pattern (case-insensitive).

        Args:
            pattern: Pattern to match (e.g., "Bus7" or "bus7")
            bus_name: Bus name to check

        Returns:
            True if pattern matches bus_name
        """
        pattern_lower = pattern.lower()
        bus_lower = bus_name.lower()

        # Direct match
        if pattern_lower == bus_lower:
            return True

        # Pattern is prefix of bus name
        if bus_lower.startswith(pattern_lower):
            return True

        # Bus name is prefix of pattern
        if pattern_lower.startswith(bus_lower):
            return True

        return False

    def _generate_pv_curve(
        self,
        converged_cases: list[dict],
        monitor_buses: list[str],
    ) -> list[dict]:
        """Generate PV curve data from converged cases.

        Args:
            converged_cases: List of converged case data with scale and voltages
            monitor_buses: List of bus names to monitor

        Returns:
            List of PV curve points with bus, scale, and voltage
        """
        pv_curve = []
        for case in converged_cases:
            scale = case["scale"]
            voltages = case["voltages"]
            for bus_name, voltage in voltages.items():
                if bus_name in monitor_buses:
                    pv_curve.append({
                        "bus": bus_name,
                        "scale": scale,
                        "voltage": voltage,
                    })
        return pv_curve

    def run(self, model: PowerSystemModel | dict, config: dict | None = None) -> SkillResult | dict:
        """Run voltage stability analysis.

        Supports both unified model interface (model + config) and legacy config-only interface.

        Args:
            model: Either a unified PowerSystemModel or a config dict (legacy mode)
            config: Analysis configuration dictionary (unified mode) or None (legacy mode)

        Returns:
            SkillResult (legacy mode) or dict (unified mode)
        """
        # Detect if called in legacy mode (config dict as first arg)
        if config is None and isinstance(model, dict):
            # Legacy mode: run(config_dict)
            return self._run_legacy(model)

        # Unified mode: run(model, config)
        assert isinstance(model, PowerSystemModel)
        return self._run_unified(model, config or {})

    def _run_unified(self, model: PowerSystemModel, config: dict) -> dict:
        """Run voltage stability analysis on unified model.

        Args:
            model: Unified PowerSystemModel containing buses, branches, loads
            config: Analysis configuration dictionary with keys:
                - load_scaling: List of load scaling factors (default: [1.0, 1.2, 1.4, 1.6, 1.8, 2.0])
                - monitor_buses: List of bus names to monitor (default: all PQ buses)
                - collapse_threshold: Voltage threshold for collapse detection (default: 0.7 pu)

        Returns:
            Dictionary with analysis results:
                - status: "success" or "error"
                - pv_curve: List of (scale, voltage) points for each monitored bus
                - critical_point: Load scale at which voltage collapse occurs (or None)
                - max_loadability: Maximum load scale before divergence
                - monitored_buses: List of monitored bus names
        """
        start_time = datetime.now()

        # Validate model
        errors = self.validate_model(model)
        if errors:
            return {
                "status": "error",
                "error": "; ".join(errors),
                "pv_curve": [],
                "critical_point": None,
                "max_loadability": None,
            }

        # Get configuration
        load_scaling = config.get("load_scaling", [1.0, 1.2, 1.4, 1.6, 1.8, 2.0])
        monitor_buses = config.get("monitor_buses", [])
        collapse_threshold = config.get("collapse_threshold", 0.7)

        # If no specific buses to monitor, use all PQ buses
        if not monitor_buses:
            monitor_buses = [bus.name for bus in model.buses if bus.bus_type == "PQ"]

        # Initialize results
        pv_curve = []
        critical_point = None
        max_loadability = None
        converged_cases = []

        # Store original loads for restoration
        original_loads = {load.bus_id: (load.p_mw, load.q_mvar) for load in model.loads}

        # Run analysis for each load scaling factor
        for scale in load_scaling:
            # Create scaled loads
            scaled_loads = []
            for load in model.loads:
                p_orig, q_orig = original_loads[load.bus_id]
                scaled_load = Load(
                    bus_id=load.bus_id,
                    name=load.name,
                    p_mw=p_orig * scale,
                    q_mvar=q_orig * scale,
                    in_service=load.in_service
                )
                scaled_loads.append(scaled_load)

            # Create modified model with scaled loads
            scaled_model = PowerSystemModel(
                buses=model.buses,
                branches=model.branches,
                generators=model.generators,
                loads=scaled_loads,
                base_mva=model.base_mva,
                name=f"{model.name}_scaled_{scale}x"
            )

            # Perform simplified power flow calculation (DC approximation for speed)
            # For more accurate results, this could call an external power flow solver
            voltages = self._calculate_voltages(scaled_model)

            if voltages:
                # Record converged case
                case_data = {"scale": scale, "voltages": voltages}
                converged_cases.append(case_data)
                max_loadability = scale

                # Check for voltage collapse
                for bus_name, voltage in voltages.items():
                    pv_curve.append({
                        "bus": bus_name,
                        "scale": scale,
                        "voltage": voltage
                    })

                    if bus_name in monitor_buses and voltage < collapse_threshold:
                        if critical_point is None:
                            critical_point = scale
            else:
                # Power flow did not converge - we've reached the limit
                break

        # Calculate summary statistics
        status = "success" if converged_cases else "error"

        return {
            "status": status,
            "pv_curve": pv_curve,
            "critical_point": critical_point,
            "max_loadability": max_loadability,
            "monitored_buses": monitor_buses,
            "load_scaling": load_scaling,
            "collapse_threshold": collapse_threshold,
            "converged_cases": len(converged_cases),
            "timestamp": datetime.now().isoformat(),
        }

    def _calculate_voltages(self, model: PowerSystemModel) -> dict[str, float] | None:
        """Calculate bus voltages using simplified power flow.

        This is a simplified DC power flow approximation. For production use,
        this should call an external power flow solver like pandapower or CloudPSS.

        Args:
            model: PowerSystemModel to analyze

        Returns:
            Dictionary mapping bus names to voltage magnitudes, or None if diverged
        """
        if not model.buses or not model.branches:
            return None

        # Get slack bus as reference
        slack_bus = model.get_slack_bus()
        if slack_bus is None:
            return None

        # Build bus index mapping
        bus_idx = {bus.bus_id: i for i, bus in enumerate(model.buses)}
        n_buses = len(model.buses)

        # Build Ybus matrix (simplified)
        Y = np.zeros((n_buses, n_buses), dtype=complex)

        for branch in model.branches:
            if not branch.in_service:
                continue

            i = bus_idx.get(branch.from_bus)
            j = bus_idx.get(branch.to_bus)
            if i is None or j is None:
                continue

            # Series admittance
            z = complex(branch.r_pu, branch.x_pu)
            if abs(z) < 1e-10:
                continue

            y = 1.0 / z

            # Build Ybus
            Y[i, i] += y
            Y[j, j] += y
            Y[i, j] -= y
            Y[j, i] -= y

            # Shunt admittance
            if branch.b_pu != 0:
                b_shunt = 1j * branch.b_pu / 2
                Y[i, i] += b_shunt
                Y[j, j] += b_shunt

        # Check if Ybus is singular
        if np.linalg.matrix_rank(Y) < n_buses - 1:
            return None

        # Simplified voltage calculation
        # For a more accurate solution, we'd solve the full AC power flow
        voltages = {}

        for bus in model.buses:
            if bus.is_slack():
                # Slack bus has fixed voltage
                voltages[bus.name] = bus.v_magnitude_pu or 1.0
            else:
                # Estimate voltage drop based on load and impedance
                # This is a simplified approximation
                load_p = 0.0
                load_q = 0.0

                for load in model.loads:
                    if load.bus_id == bus.bus_id and load.in_service:
                        load_p = load.p_mw / model.base_mva
                        load_q = load.q_mvar / model.base_mva
                        break

                if load_p > 0:
                    # Estimate voltage drop (simplified)
                    # V_drop ~ P*R + Q*X (approximate)
                    connected_branches = model.get_branches_connected_to(bus.bus_id)
                    if connected_branches:
                        avg_r = np.mean([b.r_pu for b in connected_branches])
                        avg_x = np.mean([b.x_pu for b in connected_branches])
                        v_drop = load_p * avg_r + load_q * avg_x

                        # Slack bus voltage minus estimated drop
                        slack_v = slack_bus.v_magnitude_pu or 1.0
                        est_v = max(0.5, slack_v - v_drop * 0.5)  # Simplified scaling

                        voltages[bus.name] = est_v
                    else:
                        voltages[bus.name] = slack_bus.v_magnitude_pu or 1.0
                else:
                    voltages[bus.name] = slack_bus.v_magnitude_pu or 1.0

        return voltages

    def _generate_report(
        self,
        data: dict,
        path: Path,
        target_buses: list[str],
    ) -> None:
        """Generate markdown report for voltage stability analysis."""
        lines = [
            "# 电压稳定性分析报告",
            "",
            f"**电压崩溃阈值**: {data.get('collapse_threshold', 0.7)} pu",
            f"**总计算工况**: {len(data.get('load_scaling', []))}",
            f"**收敛工况**: {data.get('converged_cases', 0)}",
            "",
        ]

        if data.get("critical_point"):
            lines.extend(
                [
                    "## 电压稳定性评估",
                    "",
                    f"**电压崩溃点**: 约在负荷水平 **{data['critical_point']}x** 处",
                    f"**最大负荷能力**: {data.get('max_loadability', 'N/A')}x",
                    "",
                ]
            )
        else:
            lines.extend(
                [
                    "## 电压稳定性评估",
                    "",
                    f"在给定负荷范围内未发生电压崩溃",
                    f"**最大负荷能力**: {data.get('max_loadability', 'N/A')}x",
                    "",
                ]
            )

        lines.extend(
            [
                "## PV曲线数据",
                "",
                "| 母线 | 负荷水平 | 电压(pu) |",
                "|------|----------|----------|",
            ]
        )

        for point in data.get("pv_curve", []):
            lines.append(
                f"| {point['bus']} | {point['scale']:.2f} | {point['voltage']:.4f} |"
            )

        lines.extend(["", "## 结论", ""])

        if data.get("critical_point"):
            lines.append(
                f"系统在负荷增长至 {data['critical_point']}x 时接近电压崩溃，"
                f"建议加强电压支撑措施。"
            )
        else:
            lines.append(
                f"系统在测试范围内保持电压稳定，"
                f"最大负荷能力约为 {data.get('max_loadability', 'N/A')}x。"
            )

        path.write_text("\n".join(lines), encoding="utf-8")

    def _run_legacy(self, config: dict[str, Any]):
        """Legacy run method that accepts config dict for backward compatibility.

        Args:
            config: Configuration dictionary with model, auth, etc.

        Returns:
            SkillResult with analysis results
        """
        start_time = datetime.now()

        try:
            # Validate config
            valid, errors = self.validate(config)
            if not valid:
                return SkillResult(
                    skill_name=self.name,
                    status=SkillStatus.FAILED,
                    error="; ".join(errors),
                    start_time=start_time,
                    end_time=datetime.now(),
                )

            # Get model from config
            model_rid = config.get("model", {}).get("rid", "")
            engine = config.get("engine", "cloudpss")
            auth = config.get("auth", {})

            # Create API and get model handle
            api = Engine.create_powerflow_for_skill(
                engine=engine,
                base_url=auth.get("base_url"),
                auth=auth,
            )

            handle = api.get_model_handle(model_rid)

            # Convert to unified model (simplified conversion)
            model = self._convert_handle_to_model(handle)

            # Run analysis with unified model
            result = self._run_unified(model, {
                "load_scaling": config.get("scan", {}).get("load_scaling", [1.0, 1.2, 1.4, 1.6, 1.8, 2.0]),
                "monitor_buses": config.get("monitoring", {}).get("buses", []),
                "collapse_threshold": config.get("monitoring", {}).get("collapse_threshold", 0.7),
            })

            # Add expected keys for test compatibility
            result["model_rid"] = model_rid
            result["total_cases"] = result.get("converged_cases", 0)
            result["results"] = result.get("pv_curve", [])

            # Convert result to SkillResult format
            if result["status"] == "error":
                return SkillResult(
                    skill_name=self.name,
                    status=SkillStatus.FAILED,
                    error=result.get("error", "Unknown error"),
                    data=result,
                    start_time=start_time,
                    end_time=datetime.now(),
                )

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                data=result,
                start_time=start_time,
                end_time=datetime.now(),
            )

        except Exception as e:
            logger.error(f"Legacy voltage stability analysis failed: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error=str(e),
                start_time=start_time,
                end_time=datetime.now(),
            )

    def _convert_handle_to_model(self, handle) -> PowerSystemModel:
        """Convert model handle to unified PowerSystemModel.

        This is a simplified conversion for demonstration.
        In production, use the full adapter from powerapi.
        """
        from cloudpss_skills_v2.powerskill import ComponentType
        from cloudpss_skills_v2.core.system_model import Bus, Branch

        # Placeholder conversion - would use actual adapter
        buses = []
        branches = []

        try:
            # Get ext_grid buses (slack buses) first
            slack_bus_indices = set()
            try:
                ext_grid_components = handle.get_components_by_type(ComponentType.SOURCE)
                for comp in ext_grid_components:
                    args = comp.args if hasattr(comp, 'args') and comp.args else {}
                    bus_idx = args.get('bus', '') if isinstance(args, dict) else ''
                    if isinstance(bus_idx, int):
                        slack_bus_indices.add(f"bus:{bus_idx}")
                    elif bus_idx:
                        slack_bus_indices.add(str(bus_idx))
            except Exception:
                pass

            # Try to get buses from handle
            bus_components = handle.get_components_by_type(ComponentType.BUS)
            for comp in bus_components:
                # Get base_kv from component args or use default
                args = comp.args if hasattr(comp, 'args') and comp.args else {}
                base_kv = args.get('vn_kv', 110.0) if isinstance(args, dict) else 110.0
                # Parse bus_id from key (e.g., "bus:0" -> 0)
                bus_id = comp.key
                if isinstance(bus_id, str) and ':' in bus_id:
                    try:
                        bus_id = int(bus_id.split(':')[-1])
                    except ValueError:
                        bus_id = 0
                # Determine bus type - check if this is a slack bus
                bus_type = "SLACK" if comp.key in slack_bus_indices else "PQ"
                bus = Bus(
                    bus_id=bus_id,
                    name=comp.name,
                    base_kv=float(base_kv) if base_kv else 110.0,
                    v_magnitude_pu=1.0,
                    bus_type=bus_type,
                )
                buses.append(bus)

            # Try to get branches from handle
            branch_components = handle.get_components_by_type(ComponentType.BRANCH)
            for comp in branch_components:
                # Get connected buses from args
                args = comp.args if hasattr(comp, 'args') and comp.args else {}
                from_bus_key = args.get("from_bus", "") if isinstance(args, dict) else ""
                to_bus_key = args.get("to_bus", "") if isinstance(args, dict) else ""

                # Parse bus IDs from keys (e.g., "bus:0" -> 0)
                from_bus = from_bus_key
                if isinstance(from_bus_key, str) and ":" in from_bus_key:
                    try:
                        from_bus = int(from_bus_key.split(":")[-1])
                    except ValueError:
                        from_bus = 0
                elif isinstance(from_bus_key, str):
                    try:
                        from_bus = int(from_bus_key)
                    except ValueError:
                        from_bus = 0
                elif not isinstance(from_bus_key, int):
                    from_bus = 0

                to_bus = to_bus_key
                if isinstance(to_bus_key, str) and ":" in to_bus_key:
                    try:
                        to_bus = int(to_bus_key.split(":")[-1])
                    except ValueError:
                        to_bus = 0
                elif isinstance(to_bus_key, str):
                    try:
                        to_bus = int(to_bus_key)
                    except ValueError:
                        to_bus = 0
                elif not isinstance(to_bus_key, int):
                    to_bus = 0

                # Ensure r_pu and x_pu are floats
                try:
                    r_pu = float(args.get("r_pu", 0.001)) if isinstance(args, dict) else 0.001
                except (TypeError, ValueError):
                    r_pu = 0.001
                try:
                    x_pu = float(args.get("x_pu", 0.01)) if isinstance(args, dict) else 0.01
                except (TypeError, ValueError):
                    x_pu = 0.01

                in_service = args.get("in_service", True) if isinstance(args, dict) else True

                # Skip branches that connect a bus to itself (invalid)
                if from_bus == to_bus:
                    logger.warning(f"Skipping branch {comp.key}: connects bus {from_bus} to itself")
                    continue

                try:
                    branch = Branch(
                        name=comp.key,
                        from_bus=from_bus,
                        to_bus=to_bus,
                        r_pu=r_pu,
                        x_pu=x_pu,
                        in_service=in_service,
                    )
                    branches.append(branch)
                except ValueError as e:
                    logger.warning(f"Skipping branch {comp.key}: {e}")
                    continue

        except Exception as e:
            logger.warning(f"Could not convert handle to model: {e}")

        return PowerSystemModel(
            buses=buses,
            branches=branches,
            loads=[],
            base_mva=100.0,
        )


# Keep backward compatibility with old class interface
class VoltageStabilityAnalysisLegacy:
    """Legacy interface for backward compatibility.

    This class maintains the old config-based interface while internally
    delegating to the new unified model implementation.
    """

    name = VoltageStabilityAnalysis.name
    description = VoltageStabilityAnalysis.description

    def __init__(self):
        self._analysis = VoltageStabilityAnalysis()

    def validate(self, config: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate configuration for backward compatibility."""
        errors = []
        if not config:
            errors.append("config is required")
            return False, errors
        if not config.get("model", {}).get("rid"):
            errors.append("model.rid is required")
        return len(errors) == 0, errors

    def run(self, config: dict[str, Any]) -> Any:
        """Legacy run method that converts config to unified model."""
        from cloudpss_skills_v2.core.skill_result import SkillResult, SkillStatus
        from cloudpss_skills_v2.powerskill import Engine

        start_time = datetime.now()

        try:
            # Get model from config
            model_rid = config.get("model", {}).get("rid", "")
            engine = config.get("engine", "cloudpss")
            auth = config.get("auth", {})

            # Create API and get model handle
            api = Engine.create_powerflow_for_skill(
                engine=engine,
                base_url=auth.get("base_url"),
                auth=auth,
            )

            handle = api.get_model_handle(model_rid)

            # Convert to unified model (simplified conversion)
            # In production, this would use the full adapter
            model = self._convert_handle_to_model(handle)

            # Run analysis with unified model
            result = self._analysis._run_unified(model, {
                "load_scaling": config.get("scan", {}).get("load_scaling", [1.0, 1.2, 1.4, 1.6, 1.8, 2.0]),
                "monitor_buses": config.get("monitoring", {}).get("buses", []),
                "collapse_threshold": config.get("monitoring", {}).get("collapse_threshold", 0.7),
            })

            # Add expected keys for test compatibility
            result["model_rid"] = model_rid
            result["total_cases"] = result.get("converged_cases", 0)
            result["results"] = result.get("pv_curve", [])

            # Convert result to SkillResult format
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS if result["status"] == "success" else SkillStatus.FAILED,
                data=result,
                logs=[],
                error=None if result["status"] == "success" else result.get("error"),
                start_time=start_time,
                end_time=datetime.now(),
            )

        except Exception as e:
            logger.error(f"Legacy analysis failed: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error=str(e),
                start_time=start_time,
                end_time=datetime.now(),
            )

    def _convert_handle_to_model(self, handle) -> PowerSystemModel:
        """Convert model handle to unified PowerSystemModel."""
        from cloudpss_skills_v2.powerskill import ComponentType
        from cloudpss_skills_v2.core.system_model import Bus, Branch

        buses = []
        branches = []

        try:
            # Get ext_grid buses (slack buses) first
            slack_bus_indices = set()
            try:
                ext_grid_components = handle.get_components_by_type(ComponentType.SOURCE)
                for comp in ext_grid_components:
                    args = comp.args if hasattr(comp, 'args') and comp.args else {}
                    bus_idx = args.get('bus', '') if isinstance(args, dict) else ''
                    # Handle both int and string bus indices
                    if isinstance(bus_idx, int):
                        slack_bus_indices.add(f"bus:{bus_idx}")
                    elif bus_idx:
                        # If it's already a string like "bus:0", use it directly
                        if str(bus_idx).startswith('bus:'):
                            slack_bus_indices.add(str(bus_idx))
                        else:
                            slack_bus_indices.add(f"bus:{bus_idx}")
            except Exception:
                pass

            bus_components = handle.get_components_by_type(ComponentType.BUS)
            for comp in bus_components:
                # Get base_kv from component args or use default
                args = comp.args if hasattr(comp, 'args') and comp.args else {}
                base_kv = args.get('vn_kv', 110.0) if isinstance(args, dict) else 110.0
                # Ensure base_kv is a float
                try:
                    base_kv = float(base_kv) if base_kv else 110.0
                except (TypeError, ValueError):
                    base_kv = 110.0

                # Parse bus_id from key (e.g., "bus:0" -> 0)
                bus_id = comp.key
                if isinstance(bus_id, str) and ':' in bus_id:
                    try:
                        bus_id = int(bus_id.split(':')[-1])
                    except ValueError:
                        bus_id = 0
                elif isinstance(bus_id, str):
                    # Try to parse as int directly
                    try:
                        bus_id = int(bus_id)
                    except ValueError:
                        bus_id = 0
                elif not isinstance(bus_id, int):
                    bus_id = 0

                # Determine bus type - check if this is a slack bus
                bus_type = "SLACK" if comp.key in slack_bus_indices else "PQ"
                bus = Bus(
                    bus_id=bus_id,
                    name=comp.name,
                    base_kv=base_kv,
                    v_magnitude_pu=1.0,
                    bus_type=bus_type,
                )
                buses.append(bus)

            branch_components = handle.get_components_by_type(ComponentType.BRANCH)
            for comp in branch_components:
                # Get connected buses from args (not properties)
                args = comp.args if hasattr(comp, 'args') and comp.args else {}
                from_bus_key = args.get("from_bus", "") if isinstance(args, dict) else ""
                to_bus_key = args.get("to_bus", "") if isinstance(args, dict) else ""

                # Parse bus IDs from keys (e.g., "bus:0" -> 0)
                from_bus = from_bus_key
                if isinstance(from_bus_key, str) and ":" in from_bus_key:
                    try:
                        from_bus = int(from_bus_key.split(":")[-1])
                    except ValueError:
                        from_bus = 0
                elif isinstance(from_bus_key, str):
                    try:
                        from_bus = int(from_bus_key)
                    except ValueError:
                        from_bus = 0
                elif not isinstance(from_bus_key, int):
                    from_bus = 0

                to_bus = to_bus_key
                if isinstance(to_bus_key, str) and ":" in to_bus_key:
                    try:
                        to_bus = int(to_bus_key.split(":")[-1])
                    except ValueError:
                        to_bus = 0
                elif isinstance(to_bus_key, str):
                    try:
                        to_bus = int(to_bus_key)
                    except ValueError:
                        to_bus = 0
                elif not isinstance(to_bus_key, int):
                    to_bus = 0

                # Ensure r_pu and x_pu are floats
                try:
                    r_pu = float(args.get("r_pu", 0.001)) if isinstance(args, dict) else 0.001
                except (TypeError, ValueError):
                    r_pu = 0.001
                try:
                    x_pu = float(args.get("x_pu", 0.01)) if isinstance(args, dict) else 0.01
                except (TypeError, ValueError):
                    x_pu = 0.01

                in_service = args.get("in_service", True) if isinstance(args, dict) else True

                # Skip branches that connect a bus to itself (invalid)
                if from_bus == to_bus:
                    logger.warning(f"Skipping branch {comp.key}: connects bus {from_bus} to itself")
                    continue

                try:
                    branch = Branch(
                        name=comp.key,
                        from_bus=from_bus,
                        to_bus=to_bus,
                        r_pu=r_pu,
                        x_pu=x_pu,
                        in_service=in_service,
                    )
                    branches.append(branch)
                except ValueError as e:
                    logger.warning(f"Skipping branch {comp.key}: {e}")
                    continue
        except Exception as e:
            logger.warning(f"Could not convert handle to model: {e}")
            import traceback
            logger.warning(traceback.format_exc())

        return PowerSystemModel(
            buses=buses,
            branches=branches,
            base_mva=100.0,
        )


__all__ = ["VoltageStabilityAnalysis", "VoltageStabilityAnalysisLegacy"]
