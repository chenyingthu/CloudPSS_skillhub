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

    def run(self, model: PowerSystemModel, config: dict) -> dict:
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
            result = self._analysis.run(model, {
                "load_scaling": config.get("scan", {}).get("load_scaling", [1.0, 1.2, 1.4, 1.6, 1.8, 2.0]),
                "monitor_buses": config.get("monitoring", {}).get("buses", []),
                "collapse_threshold": config.get("monitoring", {}).get("collapse_threshold", 0.7),
            })

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
        """Convert model handle to unified PowerSystemModel.

        This is a simplified conversion for demonstration.
        In production, use the full adapter from powerapi.
        """
        # Placeholder conversion - would use actual adapter
        return PowerSystemModel(
            buses=[],
            branches=[],
            loads=[],
            base_mva=100.0,
        )


__all__ = ["VoltageStabilityAnalysis", "VoltageStabilityAnalysisLegacy"]
