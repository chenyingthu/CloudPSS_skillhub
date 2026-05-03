"""Short Circuit Skill v2 - Engine-agnostic short circuit current calculation.

短路电流计算 - 基于EMT仿真计算短路电流
支持三相短路、单相接地短路、两相短路
提取峰值电流、稳态短路电流、直流分量
"""

from __future__ import annotations

import csv
import json
import logging
import math
from datetime import datetime
from pathlib import Path
from typing import Any

from cloudpss_skills_v2.core.skill_result import (
    Artifact,
    LogEntry,
    SkillResult,
    SkillStatus,
)
from cloudpss_skills_v2.core.system_model import PowerSystemModel
from cloudpss_skills_v2.poweranalysis.base import PowerAnalysis
from cloudpss_skills_v2.powerapi import EngineConfig
from cloudpss_skills_v2.powerskill import Engine, ShortCircuit

logger = logging.getLogger(__name__)


def _as_float(value, default=0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


class ShortCircuitAnalysis(PowerAnalysis):
    """短路电流计算技能 - v2 engine-agnostic implementation.

    Inherits from PowerAnalysis to work with unified PowerSystemModel.
    """

    name = "short_circuit"
    description = "短路电流计算 - 基于EMT仿真计算短路电流和短路容量"

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model", "fault"],
            "properties": {
                "skill": {"type": "string", "const": "short_circuit", "default": "short_circuit"},
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
                        "file": {"type": "string"},
                        "path": {"type": "string"},
                    },
                },
                "fault": {
                    "type": "object",
                    "required": ["location"],
                    "properties": {
                        "location": {
                            "type": "string",
                            "default": "Bus7",
                        },
                        "type": {
                            "enum": [
                                "three_phase",
                                "line_to_ground",
                                "line_to_line",
                            ],
                            "default": "three_phase",
                        },
                        "resistance": {
                            "type": "number",
                            "default": 0.0001,
                        },
                        "fs": {
                            "type": "number",
                            "default": 2.0,
                        },
                        "fe": {
                            "type": "number",
                            "default": 2.1,
                        },
                    },
                },
                "monitoring": {
                    "type": "object",
                    "properties": {
                        "current_channels": {
                            "type": "array",
                            "items": {"type": "string"},
                            "default": [],
                        },
                        "voltage_channels": {
                            "type": "array",
                            "items": {"type": "string"},
                            "default": [],
                        },
                    },
                },
                "calculation": {
                    "type": "object",
                    "properties": {
                        "base_voltage": {
                            "type": "number",
                            "default": 500,
                        },
                        "base_capacity": {
                            "type": "number",
                            "default": 100,
                        },
                        "sample_window": {
                            "type": "array",
                            "items": {"type": "number"},
                            "default": [2.0, 2.05],
                        },
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"enum": ["json", "csv"], "default": "json"},
                        "path": {"type": "string", "default": "./results/"},
                        "prefix": {"type": "string", "default": "short_circuit"},
                        "generate_report": {"type": "boolean", "default": True},
                    },
                },
            },
        }

    def get_default_config(self) -> dict[str, Any]:
        return {
            "skill": self.name,
            "engine": "cloudpss",
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "model/holdme/IEEE39", "source": "cloud"},
            "fault": {
                "location": "Bus7",
                "type": "three_phase",
                "resistance": 0.0001,
                "fs": 2.0,
                "fe": 2.1,
            },
            "monitoring": {
                "current_channels": [],
                "voltage_channels": [],
            },
            "calculation": {
                "base_voltage": 500,
                "base_capacity": 100,
                "sample_window": [2.0, 2.05],
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "short_circuit",
                "generate_report": True,
            },
        }

    def __init__(self):
        self.logs: list[LogEntry] = []
        self.artifacts: list[Artifact] = []

    def run(self, model: PowerSystemModel | None = None, config: dict | None = None) -> dict | SkillResult:
        """Run short circuit analysis on unified PowerSystemModel.

        This method supports two calling conventions:
        1. Unified model interface (new): run(model, config)
        2. Legacy config-only interface (backward compat): run(config)

        Args:
            model: Unified PowerSystemModel containing buses, branches, generators, etc.
                   If None and first arg is dict, treats first arg as legacy config.
            config: Analysis configuration dictionary with keys:
                - fault_location: str - Bus name where fault occurs
                - fault_type: str - "three_phase", "line_to_ground", or "line_to_line"
                - fault_resistance: float - Fault resistance in ohms (default: 0.0)

        Returns:
            For unified model interface: Dictionary with analysis results
            For legacy interface: SkillResult object
        """
        # Handle backward compatibility: if model is actually a dict, treat as legacy config
        if model is not None and isinstance(model, dict) and config is None:
            # Legacy API: run(config_dict)
            return self.run_with_config(model)

        # Unified model interface
        if model is None or config is None:
            raise TypeError("run() requires both 'model' and 'config' arguments")
        self.logs = []
        self.artifacts = []

        # Validate model
        errors = self.validate_model(model)
        if errors:
            return {
                "status": "error",
                "errors": errors,
            }

        # Get fault configuration
        fault_location = config.get("fault_location", "")
        fault_type = config.get("fault_type", "three_phase")
        fault_resistance = config.get("fault_resistance", 0.0)

        # Validate fault location
        target_bus = model.get_bus_by_name(fault_location)
        if target_bus is None:
            # Try to find by ID if name fails
            try:
                bus_id = int(fault_location.replace("Bus", ""))
                target_bus = model.get_bus_by_id(bus_id)
            except (ValueError, AttributeError):
                pass

        if target_bus is None:
            return {
                "status": "error",
                "errors": [f"Fault location '{fault_location}' not found in model"],
            }

        self._log("INFO", f"Running short circuit analysis at {fault_location}")
        self._log("INFO", f"Fault type: {fault_type}")
        self._log("INFO", f"Fault resistance: {fault_resistance} Ω")

        # Calculate short circuit currents using the unified model
        result = self._calculate_short_circuit(model, target_bus, fault_type, fault_resistance)

        return result

    def _calculate_short_circuit(
        self,
        model: PowerSystemModel,
        fault_bus: Any,
        fault_type: str,
        fault_resistance: float,
    ) -> dict:
        """Calculate short circuit currents using the unified model.

        This is a simplified calculation based on the unified model.
        For more accurate results, the full PowerSkill API with EMT simulation
        should be used.
        """
        from cloudpss_skills_v2.core.system_model import Bus

        fault_currents = {}
        short_circuit_mva = {}

        # Get system base values
        base_mva = model.base_mva
        base_voltage = fault_bus.base_kv

        # Calculate equivalent impedance at fault location
        # This is a simplified calculation
        branches_at_fault = model.get_branches_connected_to(fault_bus.bus_id)

        if not branches_at_fault:
            return {
                "status": "error",
                "errors": [f"No branches connected to fault bus {fault_bus.name}"],
            }

        # Calculate parallel impedance of all branches connected to fault bus
        # Z_eq = 1 / sum(1/Z_i) for all branches
        y_total = complex(0, 0)
        for branch in branches_at_fault:
            if branch.in_service and branch.x_pu > 0:
                z_branch = complex(branch.r_pu, branch.x_pu)
                y_branch = 1 / z_branch if z_branch != 0 else complex(0, 0)
                y_total += y_branch

        if y_total == 0:
            return {
                "status": "error",
                "errors": ["Cannot calculate short circuit: no valid branch impedances"],
            }

        z_eq = 1 / y_total

        # Add fault resistance
        z_fault = complex(fault_resistance / (base_voltage ** 2 / base_mva), 0)
        z_total = z_eq + z_fault

        # Calculate fault current in per unit
        v_prefault = 1.0  # Assume 1.0 pu pre-fault voltage
        i_fault_pu = v_prefault / abs(z_total) if abs(z_total) > 0 else 0

        # Convert to kA
        i_base = base_mva / (math.sqrt(3) * base_voltage)
        i_fault_ka = i_fault_pu * i_base

        # Calculate short circuit capacity
        scc_mva = math.sqrt(3) * base_voltage * i_fault_ka

        # Store results for fault bus
        fault_currents[fault_bus.name] = {
            "peak_current": i_fault_ka * math.sqrt(2),  # Peak = RMS * sqrt(2)
            "steady_current": i_fault_ka,
            "dc_component": i_fault_ka * 0.5,  # Simplified assumption
            "time_constant": 0.05,  # Simplified assumption (50 ms)
            "impedance_pu": abs(z_total),
        }

        short_circuit_mva[fault_bus.name] = {
            "steady_current_ka": i_fault_ka,
            "short_circuit_mva": round(scc_mva, 2),
        }

        # Calculate voltages at other buses during fault
        for bus in model.buses:
            if bus.bus_id != fault_bus.bus_id:
                # Simplified voltage calculation during fault
                # V = 1 - I_fault * Z_transfer
                # For simplicity, assume voltage drops proportionally to distance
                branches_to_fault = model.get_branches_connected_to(bus.bus_id)
                if branches_to_fault:
                    min_z = min(
                        (b.x_pu for b in branches_to_fault if b.in_service and b.x_pu > 0),
                        default=0.1
                    )
                    voltage_drop = i_fault_pu * min_z
                    v_during_fault = max(0, 1.0 - voltage_drop)
                else:
                    v_during_fault = 1.0

                fault_currents[bus.name] = {
                    "voltage_during_fault": round(v_during_fault, 4),
                }

        self._log("INFO", f"Calculated fault current: {i_fault_ka:.4f} kA")
        self._log("INFO", f"Short circuit capacity: {scc_mva:.2f} MVA")

        return {
            "status": "success",
            "fault_location": fault_bus.name,
            "fault_type": fault_type,
            "fault_resistance": fault_resistance,
            "fault_current": fault_currents,
            "short_circuit_mva": short_circuit_mva,
            "base_mva": base_mva,
            "base_voltage_kv": base_voltage,
        }

    def _log(self, level: str, message: str) -> None:
        self.logs.append(LogEntry(timestamp=datetime.now(), level=level, message=message))
        getattr(logger, level.lower(), logger.info)(message)

    def _get_api(self, config: dict[str, Any]) -> ShortCircuit:
        engine = config.get("engine", "cloudpss")
        auth = config.get("auth", {})
        engine_config = EngineConfig(
            engine_name=engine,
            base_url=auth.get("base_url", ""),
            extra={"auth": auth},
        )
        return Engine.create_short_circuit(engine=engine, config=engine_config)

    def validate(self, config: dict[str, Any]) -> tuple[bool, list[str]]:
        errors = []
        if not config.get("model", {}).get("rid"):
            errors.append("必须提供 model.rid")
        fault_config = config.get("fault", {})
        if not fault_config.get("location"):
            errors.append("必须提供 fault.location (短路位置)")
        engine = config.get("engine", "cloudpss")
        auth = config.get("auth", {})
        if engine == "cloudpss" and not auth.get("token") and not auth.get("token_file"):
            errors.append("必须提供 auth.token 或 auth.token_file")
        return len(errors) == 0, errors

    def run_with_config(self, config: dict[str, Any]) -> SkillResult:
        start_time = datetime.now()
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
            api = self._get_api(config)
            self._log("INFO", f"使用引擎: {api.adapter.engine_name}")

            model_config = config["model"]
            model_rid = model_config["rid"]
            model_file = model_config.get("file") or model_config.get("path")
            source = model_config.get("source", "cloud")
            auth = config.get("auth", {})

            fault_config = config["fault"]
            monitoring_config = config.get("monitoring", {})
            calc_config = config.get("calculation", {})
            output_config = config.get("output", {})

            fault_location = fault_config["location"]
            fault_type = fault_config.get("type", "three_phase")
            fault_resistance = fault_config.get("resistance", 0.0001)
            fs = fault_config.get("fs", 2.0)
            fe = fault_config.get("fe", 2.1)

            current_channels = monitoring_config.get("current_channels", [])
            voltage_channels = monitoring_config.get("voltage_channels", [])

            base_voltage = calc_config.get("base_voltage", 500)
            base_capacity = calc_config.get("base_capacity", 100)
            sample_window = calc_config.get("sample_window", [2.0, 2.05])

            self._log("INFO", f"短路电流计算: {fault_location}")
            self._log("INFO", f"短路类型: {fault_type}")
            self._log("INFO", f"短路电阻: {fault_resistance} Ω")
            self._log("INFO", f"故障时间: {fs}s ~ {fe}s")

            sim_result = api.run_short_circuit(
                model_id=model_rid,
                fault_type=fault_type,
                fault_impedance={"r": fault_resistance},
                bus_id=fault_location,
                source=source,
                auth=auth,
                model_file=model_file,
            )

            if not sim_result.is_success:
                raise RuntimeError(
                    sim_result.errors[0] if sim_result.errors else "短路计算EMT仿真失败"
                )

            # Get unified PowerSystemModel (new architecture)
            system_model = None
            if hasattr(api, 'get_system_model'):
                system_model = api.get_system_model(sim_result.job_id)

            if system_model is not None:
                self._log("INFO", f"统一模型: {len(system_model.buses)} 母线, {len(system_model.branches)} 支路")

            result_data = sim_result.data

            if current_channels or voltage_channels:
                analysis = self._analyze_from_emt_result(
                    sim_result,
                    current_channels,
                    voltage_channels,
                    sample_window,
                    base_voltage,
                    base_capacity,
                )
            else:
                analysis = self._build_analysis_from_adapter_data(result_data)

            short_circuit_mva = self._calculate_short_circuit_capacity(
                analysis, base_voltage, base_capacity
            )

            result_data = {
                "model_rid": model_rid,
                "fault_location": fault_location,
                "fault_type": fault_type,
                "fault_resistance": fault_resistance,
                "base_voltage": base_voltage,
                "base_capacity": base_capacity,
                "analysis": analysis,
                "short_circuit_mva": short_circuit_mva,
                "timestamp": datetime.now().isoformat(),
                "unified_model": {
                    "has_model": system_model is not None,
                    "bus_count": len(system_model.buses) if system_model else 0,
                    "branch_count": len(system_model.branches) if system_model else 0,
                } if system_model else None,
            }

            self._save_output(result_data, output_config)

            self._log("INFO", f"短路计算完成: {len(analysis)} 个通道分析")

            has_currents = any("peak_current" in v or "current_ka" in v for v in analysis.values())
            status = SkillStatus.SUCCESS if has_currents else SkillStatus.FAILED

            return SkillResult(
                skill_name=self.name,
                status=status,
                data=result_data,
                artifacts=self.artifacts,
                logs=self.logs,
                metrics={
                    "fault_type": fault_type,
                    "fault_location": fault_location,
                    "channels_analyzed": len(analysis),
                },
                start_time=start_time,
                end_time=datetime.now(),
            )

        except Exception as e:
            self._log("ERROR", f"执行失败: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                data={
                    "success": False,
                    "error": str(e),
                    "stage": "short_circuit",
                },
                artifacts=self.artifacts,
                logs=self.logs,
                error=str(e),
                start_time=start_time,
                end_time=datetime.now(),
            )

    def _build_analysis_from_adapter_data(self, result_data: dict) -> dict:
        analysis = {}

        for fc in result_data.get("fault_currents", []):
            channel = fc.get("channel", "unknown")
            analysis[channel] = {
                "peak_current": fc.get("current_ka", 0),
                "steady_current": fc.get("current_ka", 0),
                "dc_component": 0,
                "time_constant": 0,
            }

        for bv in result_data.get("bus_voltages", []):
            channel = bv.get("channel", "unknown")
            analysis[channel] = {
                "min_voltage": bv.get("voltage_pu", 0),
            }

        for bus in result_data.get("bus_results", []):
            channel = str(bus.get("bus") or bus.get("bus_index") or "unknown")
            current_ka = _as_float(bus.get("ikss_ka"), 0)
            peak_current = _as_float(bus.get("ip_ka"), 0)
            if peak_current <= 0 and current_ka > 0:
                peak_current = current_ka
            analysis[channel] = {
                "peak_current": peak_current,
                "steady_current": current_ka,
                "current_ka": current_ka,
                "thermal_current": _as_float(bus.get("ith_ka"), 0),
                "min_voltage": _as_float(bus.get("v_pu"), 0),
            }

        return analysis

    def _analyze_from_emt_result(
        self,
        sim_result: Any,
        current_channels: list[str],
        voltage_channels: list[str],
        sample_window: list[float],
        base_voltage: float,
        base_capacity: float,
    ) -> dict:
        """Analyze short circuit from raw EMT result waveform data.

        When specific monitoring channels are configured, this method attempts
        to extract detailed peak/steady-state/DC component data from the raw
        waveform. Currently requires CloudPSS SDK for waveform access.

        TODO: Extend ModelHandle/ShortCircuit to support waveform data
        extraction so skills don't need direct SDK access.
        """
        analysis: dict[str, Any] = {}

        raw_result = sim_result.data.get("_raw_result")
        if raw_result is None:
            return self._build_analysis_from_adapter_data(sim_result.data)

        try:
            for plot_idx in range(len(raw_result.getPlots())):
                channel_names = raw_result.getPlotChannelNames(plot_idx)

                for ch in current_channels:
                    if ch in channel_names:
                        trace = raw_result.getPlotChannelData(plot_idx, ch)
                        if trace and trace.get("y"):
                            xs = trace.get("x", [])
                            ys = trace.get("y", [])
                            if not xs or not ys:
                                continue

                            fault_data = [
                                (t, v)
                                for t, v in zip(xs, ys)
                                if sample_window[0] <= t <= sample_window[1]
                            ]
                            if not fault_data:
                                continue

                            currents = [d[1] for d in fault_data]
                            times = [d[0] for d in fault_data]

                            peak_current = max(abs(v) for v in currents) if currents else 0
                            steady_current = (
                                sum(currents[-10:]) / len(currents[-10:])
                                if len(currents) >= 10
                                else 0
                            )
                            dc_component = peak_current - abs(steady_current)

                            time_constant = 0
                            if len(currents) > 20 and dc_component > 0:
                                target = steady_current + dc_component * 0.37
                                for i, (t, v) in enumerate(fault_data):
                                    if i > 0 and abs(v) < abs(target):
                                        time_constant = (t - times[0]) * 1000
                                        break

                            analysis[ch] = {
                                "peak_current": peak_current,
                                "steady_current": steady_current,
                                "dc_component": dc_component,
                                "time_constant": time_constant,
                            }

                for ch in voltage_channels:
                    if ch in channel_names:
                        trace = raw_result.getPlotChannelData(plot_idx, ch)
                        if trace and trace.get("y"):
                            xs = trace.get("x", [])
                            ys = trace.get("y", [])
                            fault_data = [
                                (t, v)
                                for t, v in zip(xs, ys)
                                if sample_window[0] <= t <= sample_window[1]
                            ]
                            if fault_data:
                                voltages = [d[1] for d in fault_data]
                                min_voltage = min(voltages) if voltages else 0
                                analysis[ch] = {
                                    "min_voltage": min_voltage,
                                }

        except (AttributeError, TypeError):
            return self._build_analysis_from_adapter_data(sim_result.data)

        return analysis

    def _calculate_short_circuit_capacity(
        self, analysis: dict, base_voltage: float, base_capacity: float
    ) -> dict:
        sqrt3 = math.sqrt(3)
        results = {}

        for ch, data in analysis.items():
            steady_current = data.get("steady_current", data.get("current_ka", 0))
            if base_voltage > 0 and steady_current > 0:
                scc_mva = sqrt3 * base_voltage * steady_current
                results[ch] = {
                    "steady_current_ka": steady_current,
                    "short_circuit_mva": round(scc_mva, 2),
                }

        return results

    def _save_output(self, result_data: dict, output_config: dict) -> None:
        output_format = output_config.get("format", "json")
        output_path = Path(output_config.get("path", "./results/"))
        prefix = output_config.get("prefix", "short_circuit")

        output_path.mkdir(parents=True, exist_ok=True)

        ts_suffix = f"_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        filename = f"{prefix}{ts_suffix}.{output_format}"
        filepath = output_path / filename

        if output_format == "json":
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(result_data, f, indent=2, ensure_ascii=False, default=str)
        else:
            self._save_csv(result_data, filepath)

        self.artifacts.append(
            Artifact(
                name=filename,
                path=str(filepath),
                type=output_format,
                size_bytes=filepath.stat().st_size,
                description="短路电流计算结果",
            )
        )
        self._log("INFO", f"导出: {filepath}")

        if output_config.get("generate_report", True):
            report_filename = f"{prefix}_report{ts_suffix}.md"
            report_path = output_path / report_filename
            self._generate_report(result_data, report_path)
            self.artifacts.append(
                Artifact(
                    name=report_filename,
                    path=str(report_path),
                    type="markdown",
                    size_bytes=report_path.stat().st_size,
                    description="短路电流分析报告",
                )
            )

    def _save_csv(self, result_data: dict, filepath: Path) -> None:
        analysis = result_data.get("analysis", {})
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "channel",
                    "peak_current_ka",
                    "steady_current_ka",
                    "dc_component_ka",
                    "time_constant_ms",
                ]
            )
            for ch, data in analysis.items():
                if "peak_current" in data:
                    writer.writerow(
                        [
                            ch,
                            f"{data.get('peak_current', 0):.4f}",
                            f"{data.get('steady_current', 0):.4f}",
                            f"{data.get('dc_component', 0):.4f}",
                            f"{data.get('time_constant', 0):.2f}",
                        ]
                    )

    def _generate_report(self, data: dict, path: Path) -> None:
        lines = [
            "# 短路电流计算报告",
            "",
            f"**模型**: {data.get('model_rid', 'Unknown')}",
            f"**短路位置**: {data.get('fault_location', 'Unknown')}",
            f"**短路类型**: {data.get('fault_type', 'Unknown')}",
            f"**短路电阻**: {data.get('fault_resistance', 0)} Ω",
            "",
            "## 基准值",
            "",
            f"- 基准电压: {data.get('base_voltage', 0)} kV",
            f"- 基准容量: {data.get('base_capacity', 0)} MVA",
            "",
            "## 短路电流分析",
            "",
            "| 通道 | 峰值电流(kA) | 稳态电流(kA) | 直流分量(kA) | 时间常数(ms) |",
            "|------|--------------|--------------|--------------|--------------|",
        ]

        for ch, analysis in data.get("analysis", {}).items():
            if "peak_current" in analysis:
                lines.append(
                    f"| {ch} | {analysis.get('peak_current', 0):.4f} | "
                    f"{analysis.get('steady_current', 0):.4f} | "
                    f"{analysis.get('dc_component', 0):.4f} | "
                    f"{analysis.get('time_constant', 0):.2f} |"
                )

        lines.extend(
            [
                "",
                "## 短路容量",
                "",
                "| 通道 | 稳态电流(kA) | 短路容量(MVA) |",
                "|------|--------------|---------------|",
            ]
        )

        for ch, scc in data.get("short_circuit_mva", {}).items():
            lines.append(
                f"| {ch} | {scc.get('steady_current_ka', 0):.4f} | "
                f"{scc.get('short_circuit_mva', 0):.2f} |"
            )

        if data.get("short_circuit_mva"):
            max_scc = max(
                scc.get("short_circuit_mva", 0) for scc in data["short_circuit_mva"].values()
            )
            lines.extend(
                [
                    "",
                    "## 结论",
                    "",
                    f"最大短路容量约为 **{max_scc:.2f} MVA**",
                ]
            )

        path.write_text("\n".join(lines), encoding="utf-8")


__all__ = ["ShortCircuitAnalysis"]
