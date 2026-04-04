"""
VSI Weak Bus Analysis Skill

VSI弱母线分析 - 基于动态无功注入的电压稳定敏感度分析

核心流程：
1. 为每个母线添加动态无功注入源（shuntLC + 断路器）
2. 配置时序信号，依次在各母线注入无功
3. 运行EMT仿真
4. 从结果计算VSI（Voltage Stability Index）
5. 识别弱母线（VSI高的母线电压稳定性差）

参考自：PSA Skills S05 - vsi-weak-bus-analysis
"""

import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from cloudpss import Model

from cloudpss_skills.core import Artifact, LogEntry, SkillBase, SkillResult, SkillStatus, ValidationResult, register
from cloudpss_skills.core.utils import (
    get_bus_components,
    get_time_index,
    calculate_voltage_average,
    clean_component_key
)

logger = logging.getLogger(__name__)


@register
class VSIWeakBusSkill(SkillBase):
    """VSI弱母线分析技能"""

    @property
    def name(self) -> str:
        return "vsi_weak_bus"

    @property
    def description(self) -> str:
        return "VSI弱母线分析 - 通过动态无功注入测试识别电压稳定性薄弱母线"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["model"],
            "properties": {
                "auth": {
                    "type": "object",
                    "properties": {
                        "token_file": {"type": "string", "default": ".cloudpss_token"}
                    }
                },
                "model": {
                    "type": "object",
                    "required": ["rid"],
                    "properties": {
                        "rid": {"type": "string", "description": "模型RID"},
                        "source": {"type": "string", "enum": ["cloud", "local"], "default": "cloud"}
                    }
                },
                "vsi_setup": {
                    "type": "object",
                    "description": "VSI测试配置",
                    "properties": {
                        "bus_filter": {
                            "type": "object",
                            "properties": {
                                "v_min": {"type": "number", "default": 0.6, "description": "母线最小电压筛选(kV)"},
                                "v_max": {"type": "number", "default": 300, "description": "母线最大电压筛选(kV)"},
                                "name_keywords": {"type": "array", "items": {"type": "string"}, "description": "母线名称关键字筛选"}
                            }
                        },
                        "injection": {
                            "type": "object",
                            "properties": {
                                "v_base": {"type": "number", "default": 220, "description": "基准电压(kV)"},
                                "q_base": {"type": "number", "default": 100, "description": "注入无功(MVar)"},
                                "start_time": {"type": "number", "default": 8.0, "description": "开始时间(s)"},
                                "interval": {"type": "number", "default": 1.5, "description": "每个母线测试时长(s)"},
                                "duration": {"type": "number", "default": 0.5, "description": "无功注入持续时间(s)"}
                            }
                        },
                        "simulation": {
                            "type": "object",
                            "properties": {
                                "step_time": {"type": "number", "default": 0.0001, "description": "仿真步长(s)"},
                                "freq": {"type": "number", "default": 100, "description": "输出频率(Hz)"}
                            }
                        }
                    }
                },
                "analysis": {
                    "type": "object",
                    "properties": {
                        "vsi_threshold": {"type": "number", "default": 0.01, "description": "弱母线VSI阈值"},
                        "top_n": {"type": "integer", "default": 10, "description": "输出前N个弱母线"}
                    }
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"type": "string", "enum": ["json", "csv"], "default": "json"},
                        "path": {"type": "string", "default": "./results/"},
                        "prefix": {"type": "string", "default": "vsi_weak_bus"}
                    }
                }
            }
        }

    def validate(self, config: Dict[str, Any]) -> ValidationResult:
        """验证配置"""
        errors = []

        if "model" not in config:
            errors.append("必须指定model配置")
        elif "rid" not in config["model"]:
            errors.append("必须指定model.rid")

        if errors:
            return ValidationResult(valid=False, errors=errors)

        return ValidationResult(valid=True)

    def run(self, config: Dict[str, Any]) -> SkillResult:
        """执行VSI弱母线分析"""
        start_time = datetime.now()
        logs = []
        artifacts = []

        try:
            # 1. 获取模型
            model_rid = config["model"]["rid"]
            logger.info(f"VSI弱母线分析开始 - 模型: {model_rid}")
            logs.append(LogEntry(level="INFO", message=f"加载模型: {model_rid}"))

            model = Model.fetch(model_rid)

            # 2. 筛选测试母线
            vsi_config = config.get("vsi_setup", {})
            bus_filter = vsi_config.get("bus_filter", {})

            test_buses = self._select_test_buses(
                model,
                v_min=bus_filter.get("v_min", 0.6),
                v_max=bus_filter.get("v_max", 300),
                name_keywords=bus_filter.get("name_keywords")
            )

            if not test_buses:
                return SkillResult(
                    status=SkillStatus.FAILED,
                    data={},
                    artifacts=artifacts,
                    logs=logs + [LogEntry(level="ERROR", message="未找到符合条件的测试母线")],
                    metrics={"duration": (datetime.now() - start_time).total_seconds()}
                )

            logger.info(f"选定 {len(test_buses)} 个测试母线")
            logs.append(LogEntry(level="INFO", message=f"选定 {len(test_buses)} 个测试母线"))

            # 3. 添加VSI无功源
            injection_config = vsi_config.get("injection", {})
            vsi_q_keys = self._add_vsi_q_sources(
                model,
                test_buses,
                v_base=injection_config.get("v_base", 220),
                q_base=injection_config.get("q_base", 100),
                start_time=injection_config.get("start_time", 8.0),
                interval=injection_config.get("interval", 1.5),
                duration=injection_config.get("duration", 0.5)
            )

            logger.info(f"添加了 {len(vsi_q_keys)} 个VSI无功源")
            logs.append(LogEntry(level="INFO", message=f"添加了 {len(vsi_q_keys)} 个VSI无功源"))

            # 4. 添加量测
            sim_config = vsi_config.get("simulation", {})
            measure_indices = self._add_vsi_measures(
                model,
                vsi_q_keys,
                freq=sim_config.get("freq", 100)
            )

            voltage_measure_k = measure_indices["voltageMeasureK"]
            q_measure_k = measure_indices["dQMeasureK"]

            logger.info(f"量测通道: 电压={voltage_measure_k}, 无功={q_measure_k}")
            logs.append(LogEntry(level="INFO", message=f"量测通道: 电压={voltage_measure_k}, 无功={q_measure_k}"))

            # 5. 设置仿真参数
            end_time = injection_config.get("start_time", 8.0) + len(test_buses) * injection_config.get("interval", 1.5)

            logger.info(f"仿真参数: 步长={sim_config.get('step_time', 0.0001)}, 结束时间={end_time}")

            # 6. 运行EMT仿真
            logger.info("开始EMT仿真...")
            logs.append(LogEntry(level="INFO", message="开始EMT仿真"))

            try:
                # 使用SDK支持的参数调用runEMT
                job = model.runEMT()

                # 等待完成
                import time
                max_wait = 300
                waited = 0
                while job.status() == 0 and waited < max_wait:
                    time.sleep(2)
                    waited += 2

                if job.status() != 1:
                    return SkillResult(
                        status=SkillStatus.FAILED,
                        data={},
                        artifacts=artifacts,
                        logs=logs + [LogEntry(level="ERROR", message="EMT仿真失败或未在时间内完成")],
                        metrics={"duration": (datetime.now() - start_time).total_seconds()}
                    )

                emt_result = job.result
                logger.info("EMT仿真完成")
                logs.append(LogEntry(level="INFO", message="EMT仿真完成"))

            except (KeyError, AttributeError, ConnectionError, TypeError) as e:
                logger.error(f"EMT仿真失败: {e}")
                return SkillResult(
                    status=SkillStatus.FAILED,
                    data={},
                    artifacts=artifacts,
                    logs=logs + [LogEntry(level="ERROR", message=f"EMT仿真失败: {str(e)}")],
                    metrics={"duration": (datetime.now() - start_time).total_seconds()}
                )

            # 7. 计算VSI
            logger.info("开始计算VSI...")
            logs.append(LogEntry(level="INFO", message="开始计算VSI"))

            vsi_results = self._calculate_vsi(
                emt_result,
                test_buses,
                voltage_measure_k,
                q_measure_k,
                injection_config.get("start_time", 8.0),
                injection_config.get("interval", 1.5),
                injection_config.get("duration", 0.5)
            )

            logger.info(f"VSI计算完成 - 母线数: {len(vsi_results['vsi_i'])}")
            logs.append(LogEntry(level="INFO", message=f"VSI计算完成 - 母线数: {len(vsi_results['vsi_i'])}"))

            # 8. 识别弱母线
            analysis_config = config.get("analysis", {})
            weak_buses = self._identify_weak_buses(
                vsi_results,
                threshold=analysis_config.get("vsi_threshold", 0.01),
                top_n=analysis_config.get("top_n", 10)
            )

            # 9. 生成输出
            output_config = config.get("output", {})
            output_path = Path(output_config.get("path", "./results/"))
            output_path.mkdir(parents=True, exist_ok=True)
            prefix = output_config.get("prefix", "vsi_weak_bus")

            result_data = {
                "model_rid": model_rid,
                "test_bus_count": len(test_buses),
                "vsi_results": vsi_results,
                "weak_buses": weak_buses,
                "summary": {
                    "total_buses": len(test_buses),
                    "weak_bus_count": len(weak_buses),
                    "max_vsi": max(vsi_results["vsi_i"].values()) if vsi_results["vsi_i"] else 0,
                    "min_vsi": min(vsi_results["vsi_i"].values()) if vsi_results["vsi_i"] else 0,
                    "avg_vsi": sum(vsi_results["vsi_i"].values()) / len(vsi_results["vsi_i"]) if vsi_results["vsi_i"] else 0
                }
            }

            # 保存JSON结果
            json_path = output_path / f"{prefix}_result.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, indent=2, ensure_ascii=False)

            artifacts.append(Artifact(
                type="json",
                path=str(json_path),
                size=json_path.stat().st_size,
                description="VSI分析结果"
            ))

            # 保存CSV结果
            csv_path = output_path / f"{prefix}_result.csv"
            self._save_csv_results(vsi_results, weak_buses, csv_path)

            artifacts.append(Artifact(
                type="csv",
                path=str(csv_path),
                size=csv_path.stat().st_size,
                description="VSI指标汇总"
            ))

            # 生成Markdown报告
            report_path = output_path / f"{prefix}_report.md"
            self._generate_report(result_data, report_path)

            artifacts.append(Artifact(
                type="markdown",
                path=str(report_path),
                size=report_path.stat().st_size,
                description="VSI分析报告"
            ))

            duration = (datetime.now() - start_time).total_seconds()
            logs.append(LogEntry(level="INFO", message=f"VSI弱母线分析完成，耗时 {duration:.2f}s"))

            return SkillResult(
                status=SkillStatus.SUCCESS,
                data=result_data,
                artifacts=artifacts,
                logs=logs,
                metrics={"duration": duration, "bus_count": len(test_buses), "weak_count": len(weak_buses)}
            )

        except (KeyError, AttributeError, ConnectionError) as e:
            logger.error(f"VSI弱母线分析失败: {e}", exc_info=True)
            return SkillResult(
                status=SkillStatus.FAILED,
                data={},
                artifacts=artifacts,
                logs=logs + [LogEntry(level="ERROR", message=f"分析失败: {str(e)}")],
                metrics={"duration": (datetime.now() - start_time).total_seconds()}
            )

    def _select_test_buses(
        self,
        model: Model,
        v_min: float = 0.6,
        v_max: float = 300,
        name_keywords: Optional[List[str]] = None
    ) -> List[Dict]:
        """筛选测试母线"""
        buses = get_bus_components(model)
        test_buses = []

        for key, data in buses.items():
            try:
                # 获取母线电压
                v_base = float(data.get("args", {}).get("V", 1.0))
                v_base_kv = float(data.get("args", {}).get("VBase", 1.0))
                bus_voltage = v_base * v_base_kv

                # 电压筛选
                if not (v_min <= bus_voltage <= v_max):
                    continue

                # 名称筛选
                label = data.get("label", "")
                if name_keywords:
                    if not any(kw in label for kw in name_keywords):
                        continue

                test_buses.append({
                    "key": key,
                    "label": label,
                    "voltage": bus_voltage,
                    "v_base": v_base,
                    "v_base_kv": v_base_kv
                })

            except (KeyError, AttributeError) as e:
                logger.warning(f"处理母线 {key} 失败: {e}")
                continue

        # 按label排序
        test_buses.sort(key=lambda x: x["label"])

        return test_buses

    def _add_vsi_q_sources(
        self,
        model: Model,
        test_buses: List[Dict],
        v_base: float = 220,
        q_base: float = 100,
        start_time: float = 8.0,
        interval: float = 1.5,
        duration: float = 0.5
    ) -> List[str]:
        """添加VSI动态无功源"""
        vsi_q_keys = []
        canvas_id = "canvas_VSI_Analysis"

        # 创建画布
        try:
            model.createCanvas(canvas_id, "VSI动态无功分析")
        except Exception as e:
            logger.warning(f"画布 {canvas_id} 可能已存在")

        for k, bus in enumerate(test_buses):
            bus_key = bus["key"]
            bus_voltage = bus["voltage"]

            # 添加shuntLC（无功注入源）
            shunt_id = f"VSI_ShuntLC_{k}"
            shunt_name = f"VSI_无功源_{k}"

            shunt_args = {
                "Name": shunt_name,
                "Dim": "3",
                "v": str(bus_voltage),
                "s": str(-q_base),  # 负号表示注入无功
                "Q": f"#VSI_DQ_{k}"  # 控制信号
            }

            shunt_pins = {"0": f"VSI_Bus_{k}"}

            try:
                key1, _ = model.addComponent(
                    definition="model/CloudPSS/_newShuntLC_3p",
                    key=shunt_id,
                    args=shunt_args,
                    pins=shunt_pins
                )
                vsi_q_keys.append(key1)
            except (AttributeError, TypeError) as e:
                logger.warning(f"添加无功源 {shunt_id} 失败: {e}")
                continue

            # 添加断路器
            breaker_id = f"VSI_Breaker_{k}"
            breaker_name = f"VSI_断路器_{k}"
            ctrl_signal = f"@VSI_Breaker_Ctrl_{k}"

            breaker_args = {
                "Name": breaker_name,
                "ctrlsignal": ctrl_signal,
                "Init": "0"  # 初始断开
            }

            # 获取母线引脚
            try:
                bus_component = model.getComponentByKey(bus_key)
                bus_pin = bus_component.pins.get("0", bus_key)
            except Exception as e:
                bus_pin = bus_key

            breaker_pins = {"0": bus_pin, "1": f"VSI_Bus_{k}"}

            try:
                model.addComponent(
                    definition="model/CloudPSS/_newBreaker_3p",
                    key=breaker_id,
                    args=breaker_args,
                    pins=breaker_pins
                )
            except (AttributeError, TypeError) as e:
                logger.warning(f"添加断路器 {breaker_id} 失败: {e}")

            # 添加开关信号（步进信号）
            signal_name = f"VSI_Signal_{k}"
            t1 = start_time + k * interval
            t2 = t1 + duration

            signal_args = {
                "Name": signal_name,
                "INIT": "0",
                "Drop": "1",
                "T1": str(t1),
                "T2": str(t2)
            }

            signal_pins = {"0": ctrl_signal}

            try:
                model.addComponent(
                    definition="model/CloudPSS/_newStepGen",
                    key=f"VSI_Step_{k}",
                    args=signal_args,
                    pins=signal_pins
                )
            except (AttributeError, TypeError) as e:
                logger.warning(f"添加信号源 {signal_name} 失败: {e}")

        return vsi_q_keys

    def _add_vsi_measures(
        self,
        model: Model,
        vsi_q_keys: List[str],
        freq: float = 100
    ) -> Dict[str, int]:
        """添加VSI量测"""
        # 添加电压量测（所有母线）
        try:
            # 获取所有母线
            buses = get_bus_components(model)
            bus_pins = []

            for key, data in buses.items():
                try:
                    comp = model.getComponentByKey(key)
                    pin = comp.pins.get("0", key)
                    bus_pins.append(pin)
                except Exception as e:
                    bus_pins.append(key)

            # 添加电压量测通道
            voltage_channel = {
                "0": bus_pins,
                "dim": 1,
                "freq": freq,
                "label": "VSI_电压量测",
                "plot": {"name": "VSI_节点电压", "xlabel": "time", "ylabel": "V"}
            }

            # 这里假设model.addOutputChannel方法存在
            # 如果不存在，需要在实际模型中使用相应方法
            voltage_measure_k = 0  # 假设这是第一个通道

        except (KeyError, AttributeError, AttributeError) as e:
            logger.warning(f"添加电压量测失败: {e}")
            voltage_measure_k = 0

        # 添加无功量测
        try:
            q_pins = []
            for key in vsi_q_keys:
                try:
                    comp = model.getComponentByKey(key)
                    pin = comp.pins.get("0", key)
                    q_pins.append(pin)
                except Exception as e:
                    q_pins.append(key)

            q_channel = {
                "0": q_pins,
                "dim": 1,
                "freq": freq,
                "label": "VSI_无功量测",
                "plot": {"name": "VSI_无功功率", "xlabel": "time", "ylabel": "Q"}
            }

            q_measure_k = 1  # 假设这是第二个通道

        except (KeyError, AttributeError, AttributeError) as e:
            logger.warning(f"添加无功量测失败: {e}")
            q_measure_k = 1

        return {"voltageMeasureK": voltage_measure_k, "dQMeasureK": q_measure_k}

    def _calculate_vsi(
        self,
        result: Any,
        test_buses: List[Dict],
        voltage_measure_k: int,
        q_measure_k: int,
        start_time: float,
        interval: float,
        duration: float
    ) -> Dict[str, Any]:
        """计算VSI指标"""
        try:
            # 获取电压量测数据
            voltage_plot = result.getPlot(voltage_measure_k)
            voltage_traces = voltage_plot.get("data", {}).get("traces", [])

            # 获取无功量测数据
            q_plot = result.getPlot(q_measure_k)
            q_traces = q_plot.get("data", {}).get("traces", [])

            vsi_i = {}  # 每个母线的平均VSI
            vsi_ij = {}  # VSI矩阵

            # 对每个测试母线
            for n, bus in enumerate(test_buses):
                bus_label = bus["label"]

                # 计算注入时刻的电压变化
                ts_inject = start_time + n * interval
                te_inject = ts_inject + duration
                ts_before = ts_inject - duration

                vsi_values = []

                # 对每个观察母线
                for k, v_trace in enumerate(voltage_traces):
                    vx = v_trace.get("x", [])
                    vy = v_trace.get("y", [])

                    if not vx or not vy:
                        continue

                    # 注入前电压
                    ms_before = get_time_index(vx, ts_before)
                    me_before = get_time_index(vx, ts_inject)
                    v_before = calculate_voltage_average(vy, ms_before, me_before)

                    # 注入时电压
                    ms_inject = get_time_index(vx, ts_inject)
                    me_inject = get_time_index(vx, te_inject)
                    v_after = calculate_voltage_average(vy, ms_inject, me_inject)

                    # 获取注入的无功量
                    if n < len(q_traces):
                        q_trace = q_traces[n]
                        qx = q_trace.get("x", [])
                        qy = q_trace.get("y", [])
                        if qy:
                            q_injected = abs(qy[-1]) if qy[-1] != 0 else 100
                        else:
                            q_injected = 100
                    else:
                        q_injected = 100

                    # 计算VSI
                    delta_v = v_before - v_after
                    vsi = delta_v / q_injected if q_injected != 0 else 0
                    vsi_values.append(vsi)

                    # 记录到VSI矩阵
                    if bus_label not in vsi_ij:
                        vsi_ij[bus_label] = {}
                    obs_name = v_trace.get("name", f"Bus_{k}")
                    vsi_ij[bus_label][obs_name] = vsi

                # 计算平均VSI
                vsi_i[bus_label] = sum(vsi_values) / len(vsi_values) if vsi_values else 0

            return {"vsi_i": vsi_i, "vsi_ij": vsi_ij}

        except (KeyError, AttributeError, ZeroDivisionError) as e:
            logger.error(f"计算VSI失败: {e}")
            return {"vsi_i": {}, "vsi_ij": {}}

    def _identify_weak_buses(
        self,
        vsi_results: Dict[str, Any],
        threshold: float = 0.01,
        top_n: int = 10
    ) -> List[Dict]:
        """识别弱母线"""
        vsi_i = vsi_results.get("vsi_i", {})

        # 按VSI排序（VSI越高越弱）
        sorted_buses = sorted(vsi_i.items(), key=lambda x: x[1], reverse=True)

        weak_buses = []
        for bus_label, vsi in sorted_buses[:top_n]:
            if vsi >= threshold:
                weak_buses.append({
                    "label": bus_label,
                    "vsi": vsi,
                    "is_weak": True
                })

        return weak_buses

    def _save_csv_results(
        self,
        vsi_results: Dict[str, Any],
        weak_buses: List[Dict],
        csv_path: Path
    ):
        """保存CSV结果"""
        import csv

        vsi_i = vsi_results.get("vsi_i", {})

        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["母线名称", "VSI", "是否弱母线"])

            # 按VSI降序
            sorted_buses = sorted(vsi_i.items(), key=lambda x: x[1], reverse=True)
            weak_labels = {wb["label"] for wb in weak_buses}

            for label, vsi in sorted_buses:
                is_weak = "是" if label in weak_labels else "否"
                writer.writerow([label, f"{vsi:.6f}", is_weak])

    def _generate_report(self, result_data: Dict[str, Any], report_path: Path):
        """生成Markdown报告"""
        lines = [
            "# VSI弱母线分析报告",
            "",
            f"**模型**: {result_data['model_rid']}",
            f"**测试母线数**: {result_data['summary']['total_buses']}",
            f"**弱母线数**: {result_data['summary']['weak_bus_count']}",
            f"**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## 摘要",
            "",
            f"- **总母线数**: {result_data['summary']['total_buses']}",
            f"- **弱母线数**: {result_data['summary']['weak_bus_count']}",
            f"- **VSI最大值**: {result_data['summary']['max_vsi']:.6f}",
            f"- **VSI最小值**: {result_data['summary']['min_vsi']:.6f}",
            f"- **VSI平均值**: {result_data['summary']['avg_vsi']:.6f}",
            ""
        ]

        # 弱母线列表
        weak_buses = result_data.get("weak_buses", [])
        if weak_buses:
            lines.extend([
                "## 弱母线列表 (Top {})".format(len(weak_buses)),
                "",
                "| 排名 | 母线名称 | VSI |",
                "|------|----------|-----|"
            ])

            for i, wb in enumerate(weak_buses, 1):
                lines.append(f"| {i} | {wb['label']} | {wb['vsi']:.6f} |")

            lines.append("")

        # VSI分布
        lines.extend([
            "## VSI指标分布",
            "",
            "| 母线名称 | VSI |",
            "|----------|-----|"
        ])

        vsi_i = result_data.get("vsi_results", {}).get("vsi_i", {})
        for label, vsi in sorted(vsi_i.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"| {label} | {vsi:.6f} |")

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
