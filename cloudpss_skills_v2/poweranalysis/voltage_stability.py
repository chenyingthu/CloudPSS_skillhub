"""Voltage Stability Skill v2 - Unified model screening implementation.

电压稳定性筛查 - 通过负荷缩放和近似电压降生成PV筛查曲线
支持负荷增长扫描和关键母线电压监测；不等同于连续潮流(CPF)认证计算。
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
from cloudpss_skills_v2.core.skill_result import Artifact, SkillResult, SkillStatus
from cloudpss_skills_v2.powerapi.adapters.handle_converter import (
    convert_handle_to_power_system_model,
)
from cloudpss_skills_v2.powerskill import Engine

logger = logging.getLogger(__name__)


class VoltageStabilityAnalysis(PowerAnalysis):
    """电压稳定性筛查技能 - unified PowerSystemModel implementation.

    Performs screening PV curve analysis by scaling loads and applying an
    approximate voltage-drop calculation for each load level. It does not
    run a full AC continuation power-flow solver.
    """

    name = "voltage_stability"
    description = "电压稳定性筛查 - 通过负荷缩放和近似电压降生成PV筛查曲线"

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
        method = config.get("method", config.get("analysis_method", "screening_proxy"))

        # If no specific buses to monitor, use all PQ buses
        if not monitor_buses:
            monitor_buses = [bus.name for bus in model.buses if bus.bus_type == "PQ"]

        if method in {"pandapower_ac", "ac_power_flow"}:
            return self._run_pandapower_ac_scan(
                model=model,
                load_scaling=load_scaling,
                monitor_buses=monitor_buses,
                collapse_threshold=collapse_threshold,
            )
        if method in {"matpower_cpf", "cpf"}:
            return self._run_matpower_cpf(
                model=model,
                target_scale=config.get("target_scale", max(load_scaling) if load_scaling else 2.0),
                monitor_buses=monitor_buses,
                collapse_threshold=collapse_threshold,
            )

        # Initialize results
        pv_curve = []
        critical_point = None
        max_loadability = None
        converged_cases = []
        used_singular_ybus_approximation = False

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
            voltages, used_approximation = self._calculate_voltages(scaled_model)
            used_singular_ybus_approximation = (
                used_singular_ybus_approximation or used_approximation
            )

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
            "analysis_mode": "screening_proxy",
            "data_source": {
                "model": "PowerSystemModel converted from selected engine result",
                "load_scaling": "scan.load_scaling",
                "voltage_estimate": "approximate impedance/load voltage-drop screening",
            },
            "confidence_level": "screening_proxy_not_cpf",
            "standard_basis": (
                "Load-scaling voltage stability screening using simplified voltage-drop "
                "estimates; not a continuation power-flow standard calculation"
            ),
            "assumptions": [
                "Branch impedance and load data in the unified model are suitable for screening",
                "Voltage drops can be approximated from local connected-branch impedance",
            ],
            "limitations": [
                "Does not run full AC continuation power flow",
                "Does not certify a true voltage-collapse nose point",
                "Use a dedicated power-flow or CPF engine before operational decisions",
            ],
            "used_singular_ybus_approximation": used_singular_ybus_approximation,
            "timestamp": datetime.now().isoformat(),
        }

    def _run_pandapower_ac_scan(
        self,
        model: PowerSystemModel,
        load_scaling: list[float],
        monitor_buses: list[str],
        collapse_threshold: float,
    ) -> dict:
        """Run an AC power-flow load scan using pandapower when available."""
        try:
            import pandapower as pp

            from cloudpss_skills_v2.powerapi.adapters.pandapower.powerflow import (
                PandapowerPowerFlowAdapter,
            )
        except Exception as exc:
            return {
                "status": "error",
                "error": f"pandapower AC scan unavailable: {exc}",
                "pv_curve": [],
                "critical_point": None,
                "max_loadability": None,
                "analysis_mode": "pandapower_ac_unavailable",
                "confidence_level": "not_evaluated",
            }

        adapter = PandapowerPowerFlowAdapter()
        try:
            base_net = adapter.from_unified_model(model)
        except Exception as exc:
            return {
                "status": "error",
                "error": f"failed to convert unified model to pandapower network: {exc}",
                "pv_curve": [],
                "critical_point": None,
                "max_loadability": None,
                "analysis_mode": "pandapower_ac_conversion_failed",
                "confidence_level": "not_evaluated",
            }

        pv_curve = []
        converged_cases = []
        failed_cases = []
        critical_point = None
        max_loadability = None

        for scale in load_scaling:
            net = adapter.from_unified_model(model)
            if hasattr(net, "load") and not net.load.empty:
                net.load["p_mw"] = base_net.load["p_mw"] * scale
                net.load["q_mvar"] = base_net.load["q_mvar"] * scale

            try:
                pp.runpp(net)
            except Exception as exc:
                failed_cases.append({"scale": scale, "error": str(exc)})
                break

            if not getattr(net, "converged", False):
                failed_cases.append({"scale": scale, "error": "pandapower power flow did not converge"})
                break

            voltages = {}
            for bus in model.buses:
                if bus.name not in monitor_buses:
                    continue
                pp_idx = self._find_pandapower_bus_index(net, bus.name)
                if pp_idx is None or pp_idx not in net.res_bus.index:
                    continue
                voltage = float(net.res_bus.at[pp_idx, "vm_pu"])
                voltages[bus.name] = voltage
                pv_curve.append({
                    "bus": bus.name,
                    "scale": scale,
                    "voltage": voltage,
                    "source": "pandapower_ac",
                })
                if voltage < collapse_threshold and critical_point is None:
                    critical_point = scale

            converged_cases.append({"scale": scale, "voltages": voltages})
            max_loadability = scale

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
            "failed_cases": failed_cases,
            "analysis_mode": "pandapower_ac_power_flow_scan",
            "data_source": {
                "model": "PowerSystemModel converted to pandapower network",
                "load_scaling": "scan.load_scaling",
                "voltage_estimate": "pandapower AC runpp bus voltage results",
            },
            "confidence_level": "ac_power_flow_scan_not_cpf",
            "standard_basis": (
                "Repeated AC power-flow load-scaling scan using pandapower runpp; "
                "not a continuation power-flow standard calculation"
            ),
            "assumptions": [
                "Unified model can be converted to an equivalent pandapower network",
                "Discrete load-scaling points are sufficient for a validation scan",
            ],
            "limitations": [
                "Does not run full AC continuation power flow",
                "Discrete scan may miss the exact voltage-collapse nose point",
                "Use a dedicated CPF engine before operational decisions",
            ],
            "used_singular_ybus_approximation": False,
            "timestamp": datetime.now().isoformat(),
        }

    @staticmethod
    def _find_pandapower_bus_index(net, bus_name: str) -> int | None:
        if not hasattr(net, "bus") or net.bus.empty:
            return None
        matches = net.bus[net.bus["name"] == bus_name]
        if not matches.empty:
            return int(matches.index[0])
        return None

    def _run_matpower_cpf(
        self,
        model: PowerSystemModel,
        target_scale: float,
        monitor_buses: list[str],
        collapse_threshold: float,
    ) -> dict:
        """Run MATPOWER CPF through the optional adapter."""
        try:
            from cloudpss_skills_v2.powerapi.adapters.matpower_cpf import (
                MatpowerCPFAdapter,
                MatpowerCPFUnavailable,
            )
        except Exception as exc:
            return self._matpower_cpf_error(f"MATPOWER CPF adapter unavailable: {exc}")

        adapter = MatpowerCPFAdapter()
        try:
            cpf_result = adapter.run_cpf(model, target_scale=target_scale)
        except MatpowerCPFUnavailable as exc:
            return self._matpower_cpf_error(str(exc), runtime_status=adapter.runtime_status())
        except Exception as exc:
            return self._matpower_cpf_error(
                f"MATPOWER runcpf failed: {exc}",
                runtime_status=adapter.runtime_status(),
                analysis_mode="matpower_cpf_failed",
            )

        max_lambda = cpf_result.get("max_lambda")
        pv_curve = self._extract_matpower_pv_curve(
            model=model,
            cpf=cpf_result.get("cpf", {}),
            monitor_buses=monitor_buses,
        )
        solver_success = bool(cpf_result.get("success", True))
        status = "success" if solver_success else "warning" if pv_curve else "error"
        critical_point = max_lambda
        result = {
            "status": status,
            "solver_success": solver_success,
            "pv_curve": pv_curve,
            "critical_point": critical_point,
            "max_loadability": max_lambda,
            "monitored_buses": monitor_buses,
            "load_scaling": [1.0, target_scale],
            "collapse_threshold": collapse_threshold,
            "converged_cases": len(pv_curve),
            "analysis_mode": "matpower_continuation_power_flow",
            "data_source": {
                "model": "PowerSystemModel converted to MATPOWER case",
                "target": f"all loads scaled to {target_scale}x",
                "voltage_estimate": "MATPOWER runcpf continuation power-flow results",
            },
            "confidence_level": "cpf_solver",
            "standard_basis": "MATPOWER runcpf full AC continuation power flow",
            "assumptions": [
                "Unified model can be converted to a valid MATPOWER case",
                "Target case scales active and reactive loads by target_scale",
            ],
            "limitations": [
                "Requires external Octave/MATLAB plus the Python MATPOWER bridge",
                "Current MVP uses all-load proportional scaling only",
                "MATPOWER solver_success may be false even when a partial CPF trace is available",
            ],
            "matpower_runtime": adapter.runtime_status(),
            "used_singular_ybus_approximation": False,
            "timestamp": datetime.now().isoformat(),
        }
        if not solver_success:
            result["warning"] = (
                "MATPOWER runcpf did not report full convergence, but returned "
                "a CPF trace and max loadability estimate"
            )
        return result

    @staticmethod
    def _matpower_cpf_error(
        error: str,
        runtime_status: dict | None = None,
        analysis_mode: str = "matpower_cpf_unavailable",
    ) -> dict:
        return {
            "status": "error",
            "error": error,
            "pv_curve": [],
            "critical_point": None,
            "max_loadability": None,
            "analysis_mode": analysis_mode,
            "confidence_level": "not_evaluated",
            "standard_basis": "MATPOWER runcpf full AC continuation power flow",
            "limitations": [
                "Requires external Octave/MATLAB plus the Python MATPOWER bridge",
            ],
            "matpower_runtime": runtime_status or {},
            "used_singular_ybus_approximation": False,
            "timestamp": datetime.now().isoformat(),
        }

    @staticmethod
    def _extract_matpower_pv_curve(
        model: PowerSystemModel,
        cpf: dict,
        monitor_buses: list[str],
    ) -> list[dict]:
        if not cpf:
            return []
        bus_by_id = {bus.bus_id: bus for bus in model.buses}
        monitored = set(monitor_buses)
        voltage_trace = cpf.get("V_c")
        if voltage_trace is None:
            voltage_trace = cpf.get("V")
        lambda_trace = cpf.get("lam_c")
        if lambda_trace is None:
            lambda_trace = cpf.get("lambda")
        if lambda_trace is None:
            lambda_trace = cpf.get("lam")
        if voltage_trace is None or lambda_trace is None:
            return []

        voltages = np.asarray(voltage_trace)
        lambdas = np.asarray(lambda_trace).reshape(-1)
        if voltages.ndim == 1:
            voltages = voltages.reshape((-1, 1))

        points = []
        for bus_index, bus in enumerate(model.buses):
            if bus.name not in monitored:
                continue
            if bus_index >= voltages.shape[0]:
                continue
            for step, lam in enumerate(lambdas):
                if step >= voltages.shape[1]:
                    break
                value = voltages[bus_index, step]
                points.append({
                    "bus": bus_by_id.get(bus.bus_id, bus).name,
                    "scale": float(lam),
                    "voltage": float(abs(value)),
                    "source": "matpower_runcpf",
                })
        return points

    def _calculate_voltages(self, model: PowerSystemModel) -> tuple[dict[str, float] | None, bool]:
        """Calculate bus voltages using simplified power flow.

        This is a simplified DC power flow approximation. For production use,
        this should call an external power flow solver like pandapower or CloudPSS.

        Args:
            model: PowerSystemModel to analyze

        Returns:
            Tuple of voltage mapping and whether the singular-Ybus approximation was used.
        """
        if not model.buses or not model.branches:
            return None, False

        # Get slack bus as reference
        slack_bus = model.get_slack_bus()
        if slack_bus is None:
            return None, False

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

        # The legacy converter can produce incomplete topology for CloudPSS canvas
        # handles. Keep the screening approximation available instead of treating
        # that conversion gap as a hard PV-scan failure.
        if np.linalg.matrix_rank(Y) < n_buses - 1:
            logger.warning("Voltage screening using approximate drop model with singular Ybus")
            used_singular_ybus_approximation = True
        else:
            used_singular_ybus_approximation = False

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

        return voltages, used_singular_ybus_approximation

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

            source = config.get("model", {}).get("source", "cloud")
            sim_result = api.run_power_flow(model_id=model_rid, source=source, auth=auth)
            if not sim_result.is_success:
                raise RuntimeError(
                    f"基态潮流计算失败: {sim_result.errors[0] if sim_result.errors else 'unknown'}"
                )
            model = api.get_system_model(sim_result.job_id) if hasattr(api, "get_system_model") else None
            if model is None:
                model = getattr(sim_result, "system_model", None)
            if model is None:
                handle = api.get_model_handle(model_rid)
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
            result["results"] = [
                {
                    "scale": scale,
                    "points": [
                        point for point in result.get("pv_curve", [])
                        if point.get("scale") == scale
                    ],
                }
                for scale in result.get("load_scaling", [])
            ]
            artifacts = [
                Artifact(
                    name="voltage_stability_summary",
                    type="json",
                    data={
                        "model_rid": model_rid,
                        "converged_cases": result.get("converged_cases", 0),
                        "critical_point": result.get("critical_point"),
                    },
                )
            ]

            # Convert result to SkillResult format
            if result["status"] == "error":
                return SkillResult(
                    skill_name=self.name,
                    status=SkillStatus.FAILED,
                    error=result.get("error", "Unknown error"),
                    data=result,
                    artifacts=artifacts,
                    start_time=start_time,
                    end_time=datetime.now(),
                )

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                data=result,
                artifacts=artifacts,
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
        """Convert model handle to unified PowerSystemModel."""
        return convert_handle_to_power_system_model(handle)


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
            result["results"] = [
                {
                    "scale": scale,
                    "points": [
                        point for point in result.get("pv_curve", [])
                        if point.get("scale") == scale
                    ],
                }
                for scale in result.get("load_scaling", [])
            ]
            artifacts = [
                Artifact(
                    name="voltage_stability_summary",
                    type="json",
                    data={
                        "model_rid": model_rid,
                        "converged_cases": result.get("converged_cases", 0),
                        "critical_point": result.get("critical_point"),
                    },
                )
            ]

            # Convert result to SkillResult format
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS if result["status"] == "success" else SkillStatus.FAILED,
                data=result,
                artifacts=artifacts,
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
        return convert_handle_to_power_system_model(handle)


__all__ = ["VoltageStabilityAnalysis", "VoltageStabilityAnalysisLegacy"]
