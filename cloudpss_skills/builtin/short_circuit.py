"""
Short Circuit Analysis Skill

短路电流计算 - 基于EMT仿真计算短路电流
支持三相短路、单相接地短路、两相短路
提取峰值电流、稳态短路电流、直流分量
"""

import csv
import json
import logging
import math
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from cloudpss_skills.core import Artifact, LogEntry, SkillBase, SkillResult, SkillStatus, ValidationResult, register

logger = logging.getLogger(__name__)

FAULT_DEFINITION = "model/CloudPSS/_newFaultResistor_3p"
FAULT_SINGLE_LINE = "model/CloudPSS/_newFaultResistor_1p"


@register
class ShortCircuitSkill(SkillBase):
    """短路电流计算技能"""

    @property
    def name(self) -> str:
        return "short_circuit"

    @property
    def description(self) -> str:
        return "短路电流计算 - 基于EMT仿真计算短路电流和短路容量"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model", "fault"],
            "properties": {
                "skill": {"type": "string", "const": "short_circuit"},
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
                        "rid": {"type": "string"},
                        "source": {"enum": ["cloud", "local"], "default": "cloud"},
                    },
                },
                "fault": {
                    "type": "object",
                    "required": ["location"],
                    "properties": {
                        "location": {"type": "string", "description": "短路位置母线ID"},
                        "type": {
                            "enum": ["three_phase", "line_to_ground", "line_to_line"],
                            "default": "three_phase",
                            "description": "短路类型",
                        },
                        "resistance": {"type": "number", "default": 0.0001, "description": "短路电阻(Ω)"},
                        "fs": {"type": "number", "default": 2.0, "description": "故障开始时间(s)"},
                        "fe": {"type": "number", "default": 2.1, "description": "故障结束时间(s)"},
                    },
                },
                "monitoring": {
                    "type": "object",
                    "properties": {
                        "current_channels": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "监测电流的通道",
                        },
                        "voltage_channels": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "监测电压的通道",
                        },
                    },
                },
                "calculation": {
                    "type": "object",
                    "properties": {
                        "base_voltage": {"type": "number", "default": 500, "description": "基准电压(kV)"},
                        "base_capacity": {"type": "number", "default": 100, "description": "基准容量(MVA)"},
                        "sample_window": {
                            "type": "array",
                            "items": {"type": "number"},
                            "default": [2.0, 2.05],
                            "description": "采样时间窗口[s]",
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

    def get_default_config(self) -> Dict[str, Any]:
        return {
            "skill": self.name,
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
                "current_channels": ["#Gen38.IT:0"],
                "voltage_channels": ["#Gen38.VT:0"],
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

    def run(self, config: Dict[str, Any]) -> SkillResult:
        from cloudpss import Model, setToken
        import time

        start_time = datetime.now()
        logs = []
        artifacts = []

        def log(level: str, message: str):
            logs.append(LogEntry(timestamp=datetime.now(), level=level, message=message))
            getattr(logger, level.lower(), logger.info)(message)

        try:
            log("INFO", "加载认证...")
            auth = config.get("auth", {})
            token = auth.get("token")
            if not token:
                token_file = auth.get("token_file", ".cloudpss_token")
                token_path = Path(token_file)
                if not token_path.exists():
                    raise FileNotFoundError(f"Token文件不存在: {token_file}")
                token = token_path.read_text().strip()
            setToken(token)
            log("INFO", "认证成功")

            model_config = config["model"]
            if model_config.get("source") == "local":
                base_model = Model.load(model_config["rid"])
            else:
                base_model = Model.fetch(model_config["rid"])
            log("INFO", f"模型: {base_model.name}")

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

            base_voltage = calc_config.get("base_voltage", 500)  # kV
            base_capacity = calc_config.get("base_capacity", 100)  # MVA
            sample_window = calc_config.get("sample_window", [2.0, 2.05])

            log("INFO", f"短路电流计算: {fault_location}")
            log("INFO", f"短路类型: {fault_type}")
            log("INFO", f"短路电阻: {fault_resistance} Ω")
            log("INFO", f"故障时间: {fs}s ~ {fe}s")

            # 准备模型
            working_model = Model(deepcopy(base_model.toJSON()))

            # 配置故障
            self._configure_fault(working_model, fault_type, fault_resistance, fs, fe, log)

            # 运行EMT
            log("INFO", "运行EMT仿真...")
            job = working_model.runEMT()
            log("INFO", f"Job ID: {job.id}")

            # 等待完成
            while True:
                status = job.status()
                if status == 1:
                    break
                if status == 2:
                    raise RuntimeError("EMT仿真失败")
                time.sleep(2)

            result = job.result
            log("INFO", "EMT仿真完成")

            # 分析结果
            log("INFO", "分析短路电流...")
            analysis = self._analyze_short_circuit(
                result, current_channels, voltage_channels, sample_window,
                base_voltage, base_capacity, log
            )

            # 计算短路容量
            short_circuit_mva = self._calculate_short_circuit_capacity(
                analysis, base_voltage, base_capacity
            )

            result_data = {
                "model": base_model.name,
                "fault_location": fault_location,
                "fault_type": fault_type,
                "fault_resistance": fault_resistance,
                "base_voltage": base_voltage,
                "base_capacity": base_capacity,
                "analysis": analysis,
                "short_circuit_mva": short_circuit_mva,
            }

            # 导出结果
            output_path = Path(output_config.get("path", "./results/"))
            output_path.mkdir(parents=True, exist_ok=True)
            prefix = output_config.get("prefix", "short_circuit")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            # JSON输出
            json_path = output_path / f"{prefix}_{timestamp}.json"
            with open(json_path, 'w') as f:
                json.dump(result_data, f, indent=2)
            artifacts.append(Artifact(type="json", path=str(json_path), size=json_path.stat().st_size, description="短路电流计算结果"))

            # CSV输出
            csv_path = output_path / f"{prefix}_{timestamp}.csv"
            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["channel", "peak_current_ka", "steady_current_ka", "dc_component_ka", "time_constant_ms"])
                for ch, data in analysis.items():
                    writer.writerow([
                        ch,
                        f"{data.get('peak_current', 0):.4f}",
                        f"{data.get('steady_current', 0):.4f}",
                        f"{data.get('dc_component', 0):.4f}",
                        f"{data.get('time_constant', 0):.2f}",
                    ])
            artifacts.append(Artifact(type="csv", path=str(csv_path), size=csv_path.stat().st_size, description="短路电流数据"))

            # 生成报告
            if output_config.get("generate_report", True):
                report_path = output_path / f"{prefix}_report_{timestamp}.md"
                self._generate_report(result_data, report_path)
                artifacts.append(Artifact(type="markdown", path=str(report_path), size=report_path.stat().st_size, description="短路电流分析报告"))

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                start_time=start_time,
                end_time=datetime.now(),
                data=result_data,
                artifacts=artifacts,
                logs=logs,
            )

        except (KeyError, AttributeError, ZeroDivisionError, RuntimeError) as e:
            log("ERROR", f"执行失败: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                data={},
                artifacts=artifacts,
                logs=logs,
                error=str(e),
            )

    def _configure_fault(self, model, fault_type: str, resistance: float, fs: float, fe: float, log_func):
        """配置故障"""
        components = model.getAllComponents()
        fault = None

        # 根据故障类型选择故障组件
        fault_def = FAULT_DEFINITION if fault_type == "three_phase" else FAULT_SINGLE_LINE

        for comp in components.values():
            if getattr(comp, "definition", None) == fault_def:
                fault = comp
                break

        if fault:
            args = {
                "fs": {"source": str(fs), "ɵexp": ""},
                "fe": {"source": str(fe), "ɵexp": ""},
                "chg": {"source": str(resistance), "ɵexp": ""},
            }

            # 单相接地故障需要设置接地电阻
            if fault_type == "line_to_ground":
                args["gnd"] = {"source": str(resistance), "ɵexp": ""}

            model.updateComponent(fault.id, args=args)
            log_func("INFO", f"故障配置: {fault_type}, R={resistance}Ω, {fs}s~{fe}s")
        else:
            log_func("WARNING", f"未找到故障组件: {fault_def}")

    def _analyze_short_circuit(self, result, current_channels: List, voltage_channels: List,
                               sample_window: List, base_voltage: float, base_capacity: float,
                               log_func) -> Dict:
        """分析短路电流"""
        analysis = {}

        for plot_idx in range(len(result.getPlots())):
            channel_names = result.getPlotChannelNames(plot_idx)

            # 分析电流通道
            for ch in current_channels:
                if ch in channel_names:
                    trace = result.getPlotChannelData(plot_idx, ch)
                    if trace and trace.get("y"):
                        xs = trace.get("x", [])
                        ys = trace.get("y", [])

                        if not xs or not ys:
                            continue

                        # 提取故障期间数据
                        fault_data = [(t, v) for t, v in zip(xs, ys)
                                     if sample_window[0] <= t <= sample_window[1]]

                        if not fault_data:
                            continue

                        times = [d[0] for d in fault_data]
                        currents = [d[1] for d in fault_data]

                        # 计算指标
                        peak_current = max(abs(v) for v in currents) if currents else 0

                        # 稳态电流（取最后10个点的平均值）
                        steady_current = sum(currents[-10:]) / len(currents[-10:]) if len(currents) >= 10 else 0

                        # 直流分量（峰值 - 稳态峰值）
                        dc_component = peak_current - abs(steady_current)

                        # 估算时间常数（简化计算）
                        time_constant = 0
                        if len(currents) > 20 and dc_component > 0:
                            # 找电流下降到初始直流分量37%的时间
                            target = steady_current + dc_component * 0.37
                            for i, (t, v) in enumerate(fault_data):
                                if i > 0 and abs(v) < abs(target):
                                    time_constant = (t - times[0]) * 1000  # ms
                                    break

                        analysis[ch] = {
                            "peak_current": peak_current,
                            "steady_current": steady_current,
                            "dc_component": dc_component,
                            "time_constant": time_constant,
                        }

                        log_func("INFO", f"  {ch}: 峰值={peak_current:.4f}kA, 稳态={steady_current:.4f}kA")

            # 分析电压通道
            for ch in voltage_channels:
                if ch in channel_names:
                    trace = result.getPlotChannelData(plot_idx, ch)
                    if trace and trace.get("y"):
                        xs = trace.get("x", [])
                        ys = trace.get("y", [])

                        fault_data = [(t, v) for t, v in zip(xs, ys)
                                     if sample_window[0] <= t <= sample_window[1]]

                        if fault_data:
                            voltages = [d[1] for d in fault_data]
                            min_voltage = min(voltages) if voltages else 0

                            analysis[ch] = {
                                "min_voltage": min_voltage,
                            }

                            log_func("INFO", f"  {ch}: 最低电压={min_voltage:.4f}pu")

        return analysis

    def _calculate_short_circuit_capacity(self, analysis: Dict, base_voltage: float, base_capacity: float) -> Dict:
        """计算短路容量"""
        sqrt3 = math.sqrt(3)

        results = {}
        for ch, data in analysis.items():
            if "peak_current" in data:  # 是电流通道
                steady_current = data.get("steady_current", 0)  # kA
                # 短路容量 S = sqrt(3) * V * I
                # V是基准电压(kV), I是短路电流(kA)
                if base_voltage > 0 and steady_current > 0:
                    scc_mva = sqrt3 * base_voltage * steady_current
                    results[ch] = {
                        "steady_current_ka": steady_current,
                        "short_circuit_mva": scc_mva,
                    }

        return results

    def _generate_report(self, data: Dict, path: Path):
        """生成Markdown报告"""
        lines = [
            "# 短路电流计算报告",
            "",
            f"**模型**: {data['model']}",
            f"**短路位置**: {data['fault_location']}",
            f"**短路类型**: {data['fault_type']}",
            f"**短路电阻**: {data['fault_resistance']} Ω",
            "",
            "## 基准值",
            "",
            f"- 基准电压: {data['base_voltage']} kV",
            f"- 基准容量: {data['base_capacity']} MVA",
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

        lines.extend([
            "",
            "## 短路容量",
            "",
            "| 通道 | 稳态电流(kA) | 短路容量(MVA) |",
            "|------|--------------|---------------|",
        ])

        for ch, scc in data.get("short_circuit_mva", {}).items():
            lines.append(
                f"| {ch} | {scc.get('steady_current_ka', 0):.4f} | {scc.get('short_circuit_mva', 0):.2f} |"
            )

        lines.extend([
            "",
            "## 结论",
            "",
        ])

        if data.get("short_circuit_mva"):
            max_scc = max(scc.get("short_circuit_mva", 0) for scc in data["short_circuit_mva"].values())
            lines.append(f"最大短路容量约为 **{max_scc:.2f} MVA**")

        path.write_text("\n".join(lines), encoding="utf-8")
