"""
Reactive Compensation Design Skill

无功补偿设计 - 基于VSI结果自动设计调相机补偿方案

核心流程：
1. 读取VSI结果，识别弱母线
2. 批量添加同步调相机到弱母线
3. 配置故障场景，运行EMT仿真
4. 计算DV电压裕度
5. 迭代优化调相机容量
6. 输出最终补偿方案

参考自：PSA Skills S06 - reactive-compensation-design
"""

import json
import logging
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
class ReactiveCompensationDesignSkill(SkillBase):
    """无功补偿设计技能"""

    @property
    def name(self) -> str:
        return "reactive_compensation_design"

    @property
    def description(self) -> str:
        return "无功补偿设计 - 基于VSI结果自动设计调相机补偿方案，迭代优化容量"

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
                "vsi_input": {
                    "type": "object",
                    "description": "VSI分析结果输入",
                    "properties": {
                        "vsi_result_file": {"type": "string", "description": "VSI结果JSON文件路径"},
                        "vsi_threshold": {"type": "number", "default": 0.01, "description": "弱母线VSI阈值"},
                        "max_buses": {"type": "integer", "default": 5, "description": "最大补偿母线数"},
                        "target_buses": {"type": "array", "items": {"type": "string"}, "description": "指定补偿母线列表"}
                    }
                },
                "compensation": {
                    "type": "object",
                    "description": "补偿设备配置",
                    "properties": {
                        "device_type": {"type": "string", "enum": ["sync_compensator"], "default": "sync_compensator", "description": "补偿设备类型"},
                        "initial_capacity": {"type": "number", "default": 100, "description": "初始容量(MVar)"},
                        "max_capacity": {"type": "number", "default": 800, "description": "最大容量(MVar)"},
                        "min_capacity": {"type": "number", "default": 10, "description": "最小容量(MVar)"},
                        "avr_k": {"type": "number", "default": 30, "description": "AVR增益"},
                        "avr_ka": {"type": "number", "default": 14.2, "description": "AVR放大倍数"}
                    }
                },
                "simulation": {
                    "type": "object",
                    "description": "仿真配置",
                    "properties": {
                        "fault_bus": {"type": "string", "description": "故障母线"},
                        "fault_type": {"type": "string", "enum": ["three_phase", "single_phase"], "default": "three_phase"},
                        "fault_time": {"type": "number", "default": 4.0, "description": "故障时间(s)"},
                        "fault_duration": {"type": "number", "default": 0.1, "description": "故障持续时间(s)"},
                        "simulation_time": {"type": "number", "default": 10.0, "description": "仿真时间(s)"},
                        "step_time": {"type": "number", "default": 0.0001, "description": "仿真步长(s)"}
                    }
                },
                "iteration": {
                    "type": "object",
                    "description": "迭代优化配置",
                    "properties": {
                        "max_iterations": {"type": "integer", "default": 20, "description": "最大迭代次数"},
                        "convergence_threshold": {"type": "number", "default": 0.5, "description": "收敛阈值(MVar)"},
                        "speed_ratio": {"type": "number", "default": 0.2, "description": "迭代加速比"},
                        "dv_judge_criteria": {
                            "type": "array",
                            "description": "DV判断条件",
                            "default": [[0.1, 3.0, 0.75, 1.25], [3.0, 999.0, 0.95, 1.05]]
                        }
                    }
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"type": "string", "enum": ["json", "csv"], "default": "json"},
                        "path": {"type": "string", "default": "./results/"},
                        "prefix": {"type": "string", "default": "reactive_compensation"}
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

        vsi_input = config.get("vsi_input", {})
        if not vsi_input.get("vsi_result_file") and not vsi_input.get("target_buses"):
            errors.append("必须指定vsi_result_file或target_buses")

        if errors:
            return ValidationResult(valid=False, errors=errors)

        return ValidationResult(valid=True)

    def run(self, config: Dict[str, Any]) -> SkillResult:
        """执行无功补偿设计"""
        start_time = datetime.now()
        logs = []
        artifacts = []

        try:
            # 1. 获取模型
            model_rid = config["model"]["rid"]
            logger.info(f"无功补偿设计开始 - 模型: {model_rid}")
            logs.append(LogEntry(level="INFO", message=f"加载模型: {model_rid}"))

            model = Model.fetch(model_rid)

            # 2. 确定补偿目标母线
            target_buses = self._get_target_buses(model, config)

            if not target_buses:
                return SkillResult(
                    status=SkillStatus.FAILED,
                    data={},
                    artifacts=artifacts,
                    logs=logs + [LogEntry(level="ERROR", message="未找到补偿目标母线")],
                    metrics={"duration": (datetime.now() - start_time).total_seconds()}
                )

            logger.info(f"补偿目标母线: {[b['label'] for b in target_buses]}")
            logs.append(LogEntry(level="INFO", message=f"补偿目标母线: {len(target_buses)}个"))

            # 3. 批量添加调相机
            comp_config = config.get("compensation", {})
            sync_ids, tran_ids = self._add_sync_compensators(
                model,
                target_buses,
                initial_capacity=comp_config.get("initial_capacity", 100),
                avr_k=comp_config.get("avr_k", 30),
                avr_ka=comp_config.get("avr_ka", 14.2)
            )

            logger.info(f"添加了 {len(sync_ids)} 个调相机")
            logs.append(LogEntry(level="INFO", message=f"添加了 {len(sync_ids)} 个调相机"))

            # 4. 迭代优化
            iteration_config = config.get("iteration", {})
            iteration_result = self._iterative_optimize(
                model,
                target_buses,
                sync_ids,
                tran_ids,
                config,
                max_iterations=iteration_config.get("max_iterations", 20),
                convergence_threshold=iteration_config.get("convergence_threshold", 0.5),
                speed_ratio=iteration_config.get("speed_ratio", 0.2)
            )

            logger.info(f"迭代优化完成 - 迭代次数: {iteration_result['iterations']}")
            logs.append(LogEntry(level="INFO", message=f"迭代优化完成，共{iteration_result['iterations']}次迭代"))

            # 5. 生成输出
            output_config = config.get("output", {})
            output_path = Path(output_config.get("path", "./results/"))
            output_path.mkdir(parents=True, exist_ok=True)
            prefix = output_config.get("prefix", "reactive_compensation")

            result_data = {
                "model_rid": model_rid,
                "target_buses": [b['label'] for b in target_buses],
                "target_bus_keys": [b['key'] for b in target_buses],
                "final_capacities": iteration_result["capacities"],
                "iterations": iteration_result["iterations"],
                "converged": iteration_result["converged"],
                "compensation_scheme": self._generate_scheme(target_buses, iteration_result["capacities"]),
                "iteration_history": iteration_result.get("history", []),
                "dv_results": iteration_result.get("dv_results", {})
            }

            # 保存JSON结果
            json_path = output_path / f"{prefix}_result.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, indent=2, ensure_ascii=False)

            artifacts.append(Artifact(
                type="json",
                path=str(json_path),
                size=json_path.stat().st_size,
                description="无功补偿设计结果"
            ))

            # 保存CSV结果
            csv_path = output_path / f"{prefix}_scheme.csv"
            self._save_scheme_csv(target_buses, iteration_result["capacities"], csv_path)

            artifacts.append(Artifact(
                type="csv",
                path=str(csv_path),
                size=csv_path.stat().st_size,
                description="补偿方案"
            ))

            # 生成Markdown报告
            report_path = output_path / f"{prefix}_report.md"
            self._generate_report(result_data, report_path)

            artifacts.append(Artifact(
                type="markdown",
                path=str(report_path),
                size=report_path.stat().st_size,
                description="无功补偿设计报告"
            ))

            duration = (datetime.now() - start_time).total_seconds()
            logs.append(LogEntry(level="INFO", message=f"无功补偿设计完成，耗时 {duration:.2f}s"))

            return SkillResult(
                status=SkillStatus.SUCCESS,
                data=result_data,
                artifacts=artifacts,
                logs=logs,
                metrics={
                    "duration": duration,
                    "bus_count": len(target_buses),
                    "iterations": iteration_result["iterations"],
                    "converged": iteration_result["converged"]
                }
            )

        except Exception as e:
            logger.error(f"无功补偿设计失败: {e}", exc_info=True)
            return SkillResult(
                status=SkillStatus.FAILED,
                data={},
                artifacts=artifacts,
                logs=logs + [LogEntry(level="ERROR", message=f"设计失败: {str(e)}")],
                metrics={"duration": (datetime.now() - start_time).total_seconds()}
            )

    def _get_target_buses(self, model: Model, config: Dict[str, Any]) -> List[Dict]:
        """获取补偿目标母线"""
        vsi_input = config.get("vsi_input", {})

        # 如果指定了目标母线，直接使用
        if "target_buses" in vsi_input and vsi_input["target_buses"]:
            target_labels = vsi_input["target_buses"]
            buses = get_bus_components(model)
            target_buses = []
            for key, data in buses.items():
                if data.get("label") in target_labels:
                    target_buses.append({
                        "key": key,
                        "label": data.get("label"),
                        "voltage": float(data.get("args", {}).get("V", 1)) * float(data.get("args", {}).get("VBase", 1))
                    })
            return target_buses

        # 从VSI结果文件读取
        vsi_file = vsi_input.get("vsi_result_file")
        if vsi_file and Path(vsi_file).exists():
            with open(vsi_file, 'r', encoding='utf-8') as f:
                vsi_data = json.load(f)

            weak_buses = vsi_data.get("weak_buses", [])
            threshold = vsi_input.get("vsi_threshold", 0.01)
            max_buses = vsi_input.get("max_buses", 5)

            # 筛选VSI超过阈值的母线
            selected_buses = [b for b in weak_buses if b.get("vsi", 0) >= threshold][:max_buses]

            # 获取母线详细信息
            buses = get_bus_components(model)
            target_buses = []
            for bus_info in selected_buses:
                label = bus_info["label"]
                for key, data in buses.items():
                    if data.get("label") == label:
                        target_buses.append({
                            "key": key,
                            "label": label,
                            "voltage": float(data.get("args", {}).get("V", 1)) * float(data.get("args", {}).get("VBase", 1)),
                            "vsi": bus_info.get("vsi", 0)
                        })
                        break

            return target_buses

        # 如果没有VSI结果，返回电压最低的母线
        buses = get_bus_components(model)
        bus_list = []
        for key, data in buses.items():
            try:
                v = float(data.get("args", {}).get("V", 1)) * float(data.get("args", {}).get("VBase", 1))
                bus_list.append({"key": key, "label": data.get("label"), "voltage": v})
            except:
                continue

        # 按电压排序，选择电压最低的
        bus_list.sort(key=lambda x: x["voltage"])
        max_buses = vsi_input.get("max_buses", 5)
        return bus_list[:max_buses]

    def _add_sync_compensators(
        self,
        model: Model,
        target_buses: List[Dict],
        initial_capacity: float = 100,
        avr_k: float = 30,
        avr_ka: float = 14.2
    ) -> Tuple[List[str], List[str]]:
        """批量添加同步调相机"""
        sync_ids = []
        tran_ids = []
        canvas_id = "canvas_Reactive_Comp"

        # 创建画布
        try:
            model.createCanvas(canvas_id, "无功补偿设计")
        except:
            logger.warning(f"画布 {canvas_id} 可能已存在")

        for i, bus in enumerate(target_buses):
            bus_key = bus["key"]
            bus_voltage = bus["voltage"]

            try:
                # 添加调相机
                sync_id = f"SyncComp_{i}"
                sync_name = f"调相机_{bus['label']}"

                sync_args = {
                    "Name": sync_name,
                    "Smva": str(initial_capacity),
                    "Vn": str(bus_voltage),
                    "fn": "50",
                    "H": "6",
                    "xq": "1.5",
                    "xd": "1.8",
                    "xq_": "0.5",
                    "xd_": "0.4",
                    "xq__": "0.3",
                    "xd__": "0.2",
                    "TD": "0.05",
                    "TD_": "0.3",
                    "TD__": "1.0",
                    "ra": "0.005"
                }

                sync_pins = {"0": f"CompBus_{i}"}

                key1, _ = model.addComponent(
                    definition="model/CloudPSS/SyncGeneratorRouter",
                    key=sync_id,
                    args=sync_args,
                    pins=sync_pins
                )
                sync_ids.append(key1)

                # 添加变压器
                tran_id = f"Tran_{i}"
                tran_name = f"变压器_{bus['label']}"

                tran_args = {
                    "Name": tran_name,
                    "Tmva": str(initial_capacity),
                    "f": "50",
                    "v": str(bus_voltage),
                    "R": "0.01",
                    "X": "0.1"
                }

                # 获取母线引脚
                try:
                    bus_component = model.getComponentByKey(bus_key)
                    bus_pin = bus_component.pins.get("0", bus_key)
                except:
                    bus_pin = bus_key

                tran_pins = {"0": bus_pin, "1": f"CompBus_{i}"}

                key2, _ = model.addComponent(
                    definition="model/CloudPSS/_newTransformer_3p2w",
                    key=tran_id,
                    args=tran_args,
                    pins=tran_pins
                )
                tran_ids.append(key2)

                # 添加AVR调压器
                avr_id = f"AVR_{i}"
                avr_name = f"AVR_{bus['label']}"

                avr_args = {
                    "Name": avr_name,
                    "K": str(avr_k),
                    "KA": str(avr_ka),
                    "TA": "0.01"
                }

                avr_pins = {"0": f"CompBus_{i}"}

                model.addComponent(
                    definition="model/CloudPSS/_PSASP_AVR_11to12",
                    key=avr_id,
                    args=avr_args,
                    pins=avr_pins
                )

            except Exception as e:
                logger.warning(f"为母线 {bus['label']} 添加调相机失败: {e}")
                continue

        return sync_ids, tran_ids

    def _iterative_optimize(
        self,
        model: Model,
        target_buses: List[Dict],
        sync_ids: List[str],
        tran_ids: List[str],
        config: Dict[str, Any],
        max_iterations: int = 20,
        convergence_threshold: float = 0.5,
        speed_ratio: float = 0.2
    ) -> Dict[str, Any]:
        """迭代优化调相机容量"""

        # 初始容量
        comp_config = config.get("compensation", {})
        capacities = [comp_config.get("initial_capacity", 100)] * len(target_buses)

        iteration_history = []
        dv_results_history = []

        for iteration in range(max_iterations):
            logger.info(f"========== 迭代 {iteration + 1}/{max_iterations} ==========")

            # 更新容量
            for i, sync_id in enumerate(sync_ids):
                try:
                    comp = model.getComponentByKey(sync_id)
                    comp.args['Smva'] = str(capacities[i])
                except:
                    pass

                try:
                    tran = model.getComponentByKey(tran_ids[i])
                    tran.args['Tmva'] = str(capacities[i])
                except:
                    pass

            # 运行EMT仿真
            sim_config = config.get("simulation", {})
            try:
                job = model.runEMT(
                    endTime=sim_config.get("simulation_time", 10.0),
                    step=sim_config.get("step_time", 0.0001)
                )

                # 等待完成
                import time
                max_wait = 300
                waited = 0
                while job.status() == 0 and waited < max_wait:
                    time.sleep(2)
                    waited += 2

                if job.status() != 1:
                    logger.error("EMT仿真失败")
                    break

                emt_result = job.result

            except Exception as e:
                logger.error(f"EMT仿真失败: {e}")
                break

            # 计算DV
            try:
                dv_result = self._calculate_dv_from_result(
                    emt_result,
                    sim_config.get("fault_time", 4.0)
                )

                dv_up_list = dv_result.get("dv_up", [])
                dv_down_list = dv_result.get("dv_down", [])

                # 检查收敛
                upper_violations = sum(1 for v in dv_up_list if v < 0)
                lower_violations = sum(1 for v in dv_down_list if v < 0)

                logger.info(f"电压裕度 - 上限违规: {upper_violations}, 下限违规: {lower_violations}")

                # 记录历史
                iteration_history.append({
                    "iteration": iteration + 1,
                    "capacities": capacities.copy(),
                    "upper_violations": upper_violations,
                    "lower_violations": lower_violations
                })

                dv_results_history.append(dv_result)

                # 如果无违规，已收敛
                if upper_violations == 0 and lower_violations == 0:
                    logger.info(f"电压裕度满足要求，迭代收敛")
                    return {
                        "capacities": capacities,
                        "iterations": iteration + 1,
                        "converged": True,
                        "history": iteration_history,
                        "dv_results": dv_results_history
                    }

                # 根据DV调整容量
                adjustments = self._calculate_adjustments(
                    capacities,
                    dv_up_list,
                    dv_down_list,
                    target_buses,
                    speed_ratio,
                    comp_config.get("max_capacity", 800),
                    comp_config.get("min_capacity", 10)
                )

                # 检查调整量
                max_adjustment = max(abs(a) for a in adjustments)
                logger.info(f"容量调整: {[f'{a:+.2f}' for a in adjustments]}, 最大调整: {max_adjustment:.2f}")

                if max_adjustment < convergence_threshold:
                    logger.info(f"调整量小于收敛阈值({convergence_threshold})，迭代收敛")
                    return {
                        "capacities": capacities,
                        "iterations": iteration + 1,
                        "converged": True,
                        "history": iteration_history,
                        "dv_results": dv_results_history
                    }

                # 更新容量
                for i in range(len(capacities)):
                    capacities[i] += adjustments[i]
                    capacities[i] = max(comp_config.get("min_capacity", 10),
                                      min(comp_config.get("max_capacity", 800), capacities[i]))

            except Exception as e:
                logger.error(f"计算DV失败: {e}")
                break

        logger.warning(f"达到最大迭代次数({max_iterations})但未收敛")
        return {
            "capacities": capacities,
            "iterations": max_iterations,
            "converged": False,
            "history": iteration_history,
            "dv_results": dv_results_history
        }

    def _calculate_dv_from_result(self, result: Any, disturbance_time: float) -> Dict[str, Any]:
        """从EMT结果计算DV"""
        try:
            plots = list(result.getPlots())
            if not plots:
                return {"dv_up": [], "dv_down": []}

            # 假设第一个图是电压量测
            voltage_plot = plots[0]
            traces = voltage_plot.get("data", {}).get("traces", [])

            dv_up_list = []
            dv_down_list = []

            for trace in traces:
                vx = trace.get("x", [])
                vy = trace.get("y", [])

                if not vx or not vy:
                    continue

                # 计算稳态电压
                ts = disturbance_time - 0.5
                te = disturbance_time
                ms = get_time_index(vx, ts)
                me = get_time_index(vx, te)
                v_steady = calculate_voltage_average(vy, ms, me)

                # 计算电压裕度
                v_max = max(vy)
                v_min = min(vy)

                dv_up = 1.05 * v_steady - v_max
                dv_down = v_min - 0.95 * v_steady

                dv_up_list.append(dv_up)
                dv_down_list.append(dv_down)

            return {"dv_up": dv_up_list, "dv_down": dv_down_list}

        except Exception as e:
            logger.error(f"计算DV失败: {e}")
            return {"dv_up": [], "dv_down": []}

    def _calculate_adjustments(
        self,
        capacities: List[float],
        dv_up_list: List[float],
        dv_down_list: List[float],
        target_buses: List[Dict],
        speed_ratio: float,
        max_capacity: float,
        min_capacity: float
    ) -> List[float]:
        """计算容量调整量"""
        adjustments = [0.0] * len(capacities)

        for i in range(len(capacities)):
            # 简单的比例调整
            dv_up = dv_up_list[i] if i < len(dv_up_list) else 0
            dv_down = dv_down_list[i] if i < len(dv_down_list) else 0

            # 如果有下限违规，增加容量
            if dv_down < 0:
                adjustment = -dv_down * capacities[i] * speed_ratio
                adjustments[i] = adjustment
            # 如果有上限违规，减少容量
            elif dv_up < 0:
                adjustment = -dv_up * capacities[i] * speed_ratio
                adjustments[i] = -adjustment

        return adjustments

    def _generate_scheme(self, target_buses: List[Dict], capacities: List[float]) -> List[Dict]:
        """生成补偿方案"""
        scheme = []
        for i, bus in enumerate(target_buses):
            scheme.append({
                "bus_label": bus["label"],
                "bus_key": bus["key"],
                "capacity_mvar": capacities[i] if i < len(capacities) else 0,
                "voltage_kv": bus.get("voltage", 0),
                "vsi": bus.get("vsi", 0)
            })
        return scheme

    def _save_scheme_csv(self, target_buses: List[Dict], capacities: List[float], csv_path: Path):
        """保存方案CSV"""
        import csv

        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["母线名称", "母线Key", "补偿容量(MVar)", "电压(kV)", "VSI"])

            for i, bus in enumerate(target_buses):
                capacity = capacities[i] if i < len(capacities) else 0
                writer.writerow([
                    bus["label"],
                    bus["key"],
                    f"{capacity:.2f}",
                    f"{bus.get('voltage', 0):.2f}",
                    f"{bus.get('vsi', 0):.6f}"
                ])

    def _generate_report(self, result_data: Dict[str, Any], report_path: Path):
        """生成Markdown报告"""
        lines = [
            "# 无功补偿设计报告",
            "",
            f"**模型**: {result_data['model_rid']}",
            f"**补偿母线数**: {len(result_data['target_buses'])}",
            f"**迭代次数**: {result_data['iterations']}",
            f"**是否收敛**: {'是' if result_data['converged'] else '否'}",
            f"**设计时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## 补偿方案",
            "",
            "| 母线名称 | 补偿容量(MVar) | 电压(kV) | VSI |",
            "|----------|----------------|----------|-----|"
        ]

        for item in result_data["compensation_scheme"]:
            lines.append(f"| {item['bus_label']} | {item['capacity_mvar']:.2f} | {item['voltage_kv']:.2f} | {item['vsi']:.6f} |")

        lines.extend([
            "",
            "## 迭代历史",
            "",
            "| 迭代次数 | 容量配置 | 上限违规 | 下限违规 |",
            "|----------|----------|----------|----------|"
        ])

        for hist in result_data.get("iteration_history", []):
            capacities_str = ", ".join([f"{c:.1f}" for c in hist["capacities"]])
            lines.append(f"| {hist['iteration']} | {capacities_str} | {hist['upper_violations']} | {hist['lower_violations']} |")

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
