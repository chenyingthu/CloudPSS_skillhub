"""
Parameter Sensitivity Analysis Skill

参数灵敏度分析 - 识别关键参数对系统指标的影响程度
通过参数扫描和潮流/EMT计算，量化参数-指标灵敏度关系
"""

import csv
import json
import logging
import re
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional

from cloudpss_skills.core import Artifact, LogEntry, SkillBase, SkillResult, SkillStatus, ValidationResult, register

logger = logging.getLogger(__name__)

# 发电机RID
GENERATOR_RID = "model/CloudPSS/_newGenerator"
# 线路RID
TRANSMISSION_LINE_RID = "model/CloudPSS/TransmissionLine"


@register
class ParameterSensitivitySkill(SkillBase):
    """参数灵敏度分析技能"""

    @property
    def name(self) -> str:
        return "parameter_sensitivity"

    @property
    def description(self) -> str:
        return "参数灵敏度分析 - 识别关键参数对系统指标的影响程度"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model", "scan"],
            "properties": {
                "skill": {"type": "string", "const": "parameter_sensitivity"},
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
                "scan": {
                    "type": "object",
                    "required": ["target", "values"],
                    "properties": {
                        "target": {"type": "string", "description": "目标参数 (e.g., Gen2.pf_P, line_1.X)"},
                        "values": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "参数扫描值列表",
                        },
                        "reference": {"type": "number", "description": "参考值，用于计算相对变化"},
                        "simulation_type": {"enum": ["power_flow", "emt"], "default": "power_flow"},
                    },
                },
                "metrics": {
                    "type": "object",
                    "properties": {
                        "voltage_buses": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "监测电压的母线列表",
                        },
                        "power_branches": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "监测功率的支路列表",
                        },
                        "custom_expressions": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "自定义指标表达式",
                        },
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"enum": ["json", "csv"], "default": "json"},
                        "path": {"type": "string", "default": "./results/"},
                        "prefix": {"type": "string", "default": "parameter_sensitivity"},
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
            "scan": {
                "target": "Gen38.pf_P",
                "values": [800, 850, 900],
                "simulation_type": "power_flow",
            },
            "metrics": {
                "voltage_buses": ["Bus30", "Bus38"],
                "power_branches": ["line-30-2"],
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "parameter_sensitivity",
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

            scan_config = config["scan"]
            metrics_config = config.get("metrics", {})
            output_config = config.get("output", {})

            target = scan_config["target"]
            values = scan_config["values"]
            reference = scan_config.get("reference")
            sim_type = scan_config.get("simulation_type", "power_flow")

            # 解析目标参数
            target_info = self._parse_target(target)
            log("INFO", f"目标参数: {target} -> {target_info}")

            # 获取参考值
            if reference is None and values:
                reference = values[len(values) // 2]  # 中间值作为参考

            log("INFO", f"参数扫描: {len(values)}个值, 参考值={reference}")
            log("INFO", f"仿真类型: {sim_type}")

            # 基线计算
            log("INFO", "计算基线...")
            base_result = self._run_simulation(base_model, sim_type)
            base_metrics = self._extract_metrics(base_result, metrics_config, sim_type)
            log("INFO", f"基线指标: {base_metrics}")

            # 参数扫描
            results = []
            for i, val in enumerate(values):
                log("INFO", f"[{i+1}/{len(values)}] 参数值={val}")
                working_model = Model(deepcopy(base_model.toJSON()))

                # 修改参数
                if not self._apply_parameter(working_model, target_info, val):
                    log("WARNING", f"  参数应用失败: {target}={val}")
                    continue

                # 运行仿真
                result = self._run_simulation(working_model, sim_type)
                metrics = self._extract_metrics(result, metrics_config, sim_type)

                # 计算相对变化
                relative_changes = {}
                for key in metrics:
                    base_val = base_metrics.get(key, 0)
                    if base_val != 0:
                        relative_changes[key] = (metrics[key] - base_val) / base_val
                    else:
                        relative_changes[key] = metrics[key]

                results.append({
                    "parameter_value": val,
                    "metrics": metrics,
                    "relative_changes": relative_changes,
                })

                log("INFO", f"  -> 指标变化: {relative_changes}")

            # 计算灵敏度
            sensitivities = self._calculate_sensitivities(results, target, reference)
            log("INFO", f"灵敏度分析完成: {len(sensitivities)}个指标")

            # 导出结果
            output_path = Path(output_config.get("path", "./results/"))
            output_path.mkdir(parents=True, exist_ok=True)
            prefix = output_config.get("prefix", "parameter_sensitivity")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            result_data = {
                "model": base_model.name,
                "target_parameter": target,
                "reference_value": reference,
                "simulation_type": sim_type,
                "sensitivities": sensitivities,
                "results": results,
            }

            # JSON输出
            json_path = output_path / f"{prefix}_{timestamp}.json"
            with open(json_path, 'w') as f:
                json.dump(result_data, f, indent=2)
            artifacts.append(Artifact(type="json", path=str(json_path), size=json_path.stat().st_size, description="参数灵敏度分析结果"))

            # CSV输出
            csv_path = output_path / f"{prefix}_{timestamp}.csv"
            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["parameter", "metric", "sensitivity", "sensitivity_rank"])
                for s in sorted(sensitivities, key=lambda x: abs(x["sensitivity"]), reverse=True):
                    writer.writerow([
                        s["parameter"],
                        s["metric"],
                        f"{s['sensitivity']:.6f}",
                        s["rank"],
                    ])
            artifacts.append(Artifact(type="csv", path=str(csv_path), size=csv_path.stat().st_size, description="灵敏度分析CSV"))

            # 生成报告
            if output_config.get("generate_report", True):
                report_path = output_path / f"{prefix}_report_{timestamp}.md"
                self._generate_report(result_data, report_path)
                artifacts.append(Artifact(type="markdown", path=str(report_path), size=report_path.stat().st_size, description="灵敏度分析报告"))

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                start_time=start_time,
                end_time=datetime.now(),
                data=result_data,
                artifacts=artifacts,
                logs=logs,
            )

        except Exception as e:
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

    def _parse_target(self, target: str) -> Dict[str, Any]:
        """解析目标参数字符串"""
        # 格式: Gen38.pf_P 或 component_id.arg_name
        parts = target.split(".")
        if len(parts) == 2:
            return {
                "component": parts[0],
                "arg": parts[1],
                "type": "generator_arg" if parts[1].startswith("pf_") else "component_arg",
            }
        return {"component": target, "arg": None, "type": "unknown"}

    def _apply_parameter(self, model, target_info: Dict, value: float) -> bool:
        """应用参数值到模型"""
        comp_id = target_info["component"]
        arg_name = target_info["arg"]

        components = model.getAllComponents()

        # 查找组件 - 只找有args属性的真正组件
        target_comp_key = None
        for key, comp in components.items():
            if not hasattr(comp, 'args'):
                continue  # Skip edges/shapes
            comp_label = getattr(comp, "label", "")
            if comp_label == comp_id or comp_id in key:
                target_comp_key = key
                break

        if target_comp_key is None:
            # 尝试模糊匹配
            for key, comp in components.items():
                if not hasattr(comp, 'args'):
                    continue
                comp_label = getattr(comp, "label", "")
                if comp_id.lower() in key.lower() or comp_id.lower() in comp_label.lower():
                    target_comp_key = key
                    break

        if target_comp_key is None:
            return False

        # 应用参数
        if arg_name:
            # 修改组件参数
            args = {arg_name: {"source": str(value), "ɵexp": ""}}
            model.updateComponent(target_comp_key, args=args)
        else:
            # 修改整个组件参数（如R、X等）
            model.updateComponent(target_comp_key, args={"value": {"source": str(value), "ɵexp": ""}})

        return True

    def _run_simulation(self, model, sim_type: str):
        """运行仿真"""
        import time

        if sim_type == "power_flow":
            job = model.runPowerFlow()
        else:
            job = model.runEMT()

        while True:
            status = job.status()
            if status == 1:
                break
            if status == 2:
                raise RuntimeError(f"{sim_type}仿真失败")
            time.sleep(2)

        return job.result

    def _extract_metrics(self, result, metrics_config: Dict, sim_type: str) -> Dict[str, float]:
        """提取指标"""
        metrics = {}

        if sim_type == "power_flow":
            # 潮流结果 - 解析表格数据
            buses_data = result.getBuses()
            branches_data = result.getBranches()

            # 解析母线数据
            if buses_data and isinstance(buses_data, list) and len(buses_data) > 0:
                bus_table = buses_data[0]  # 第一个元素是母线表
                if bus_table.get("type") == "table":
                    columns = bus_table.get("data", {}).get("columns", [])
                    col_data = {col["name"]: col.get("data", []) for col in columns}

                    # 找指定母线
                    bus_names = col_data.get("Bus", [])
                    vm_data = col_data.get("<i>V</i><sub>m</sub> / pu", [])

                    for target_bus in metrics_config.get("voltage_buses", []):
                        for i, bus in enumerate(bus_names):
                            if target_bus in bus and i < len(vm_data):
                                metrics[f"{target_bus}.Vm"] = vm_data[i]
                                break

                    # 全局指标
                    if vm_data:
                        metrics["min_Vm"] = min(vm_data) if vm_data else 1.0

            # 解析支路数据
            if branches_data and isinstance(branches_data, list) and len(branches_data) > 0:
                branch_table = branches_data[0]
                if branch_table.get("type") == "table":
                    columns = branch_table.get("data", {}).get("columns", [])
                    col_data = {col["name"]: col.get("data", []) for col in columns}

                    p_ij_data = col_data.get("<i>P</i><sub>ij</sub> / MW", [])
                    if p_ij_data:
                        metrics["max_P_transfer"] = max(abs(p) for p in p_ij_data if p is not None)

        else:
            # EMT结果 - 提取最后时间点的值
            for plot_idx in range(len(result.getPlots())):
                channel_names = result.getPlotChannelNames(plot_idx)
                for ch_name in channel_names:
                    trace = result.getPlotChannelData(plot_idx, ch_name)
                    if trace and "y" in trace and trace["y"]:
                        # 取最后100个点的平均值
                        metrics[ch_name] = sum(trace["y"][-100:]) / 100

        return metrics

    def _calculate_sensitivities(self, results: List[Dict], target: str, reference: float) -> List[Dict]:
        """计算灵敏度"""
        if not results or len(results) < 2:
            return []

        sensitivities = []

        # 获取所有指标名
        all_metrics = set()
        for r in results:
            all_metrics.update(r["metrics"].keys())

        for metric in all_metrics:
            # 收集 (参数值, 指标值) 对
            points = [(r["parameter_value"], r["metrics"].get(metric, 0)) for r in results]
            points.sort(key=lambda x: x[0])

            # 线性回归求灵敏度 (dy/dx)
            n = len(points)
            if n < 2:
                continue

            x_vals = [p[0] for p in points]
            y_vals = [p[1] for p in points]

            x_mean = sum(x_vals) / n
            y_mean = sum(y_vals) / n

            numerator = sum((x - x_mean) * (y - y_mean) for x, y in points)
            denominator = sum((x - x_mean) ** 2 for x in x_vals)

            if denominator != 0:
                sensitivity = numerator / denominator
            else:
                sensitivity = 0

            # 归一化灵敏度 (相对变化率)
            if reference != 0 and y_mean != 0:
                normalized_sens = sensitivity * reference / y_mean
            else:
                normalized_sens = sensitivity

            sensitivities.append({
                "parameter": target,
                "metric": metric,
                "sensitivity": sensitivity,
                "normalized_sensitivity": normalized_sens,
                "rank": 0,  # 稍后排序
            })

        # 排序并分配rank
        sensitivities.sort(key=lambda x: abs(x["sensitivity"]), reverse=True)
        for i, s in enumerate(sensitivities):
            s["rank"] = i + 1

        return sensitivities

    def _generate_report(self, data: Dict, path: Path):
        """生成Markdown报告"""
        lines = [
            "# 参数灵敏度分析报告",
            "",
            f"**模型**: {data['model']}",
            f"**目标参数**: {data['target_parameter']}",
            f"**参考值**: {data['reference_value']}",
            f"**仿真类型**: {data['simulation_type']}",
            "",
            "## 灵敏度排序",
            "",
            "| 排名 | 指标 | 灵敏度 | 归一化灵敏度 |",
            "|------|------|--------|--------------|",
        ]

        for s in sorted(data.get("sensitivities", []), key=lambda x: x["rank"]):
            lines.append(
                f"| {s['rank']} | {s['metric']} | {s['sensitivity']:.6f} | {s.get('normalized_sensitivity', 0):.6f} |"
            )

        lines.extend([
            "",
            "## 扫描结果",
            "",
            "| 参数值 | " + " | ".join(data.get("results", [{}])[0].get("metrics", {}).keys()) + " |",
            "|--------|" + "|".join(["--------"] * len(data.get("results", [{}])[0].get("metrics", {}))) + "|",
        ])

        for r in data.get("results", []):
            metrics_str = " | ".join(f"{v:.4f}" for v in r.get("metrics", {}).values())
            lines.append(f"| {r['parameter_value']} | {metrics_str} |")

        lines.extend([
            "",
            "## 结论",
            "",
        ])

        top_sens = data.get("sensitivities", [])[:3]
        if top_sens:
            lines.append(f"**最敏感指标**: {top_sens[0]['metric']} (灵敏度={top_sens[0]['sensitivity']:.6f})")
            lines.append("")
            lines.append("**关键发现**:")
            for s in top_sens:
                direction = "增加" if s['sensitivity'] > 0 else "减少"
                lines.append(f"- {s['metric']}: 随{data['target_parameter']}增加而{direction}")

        path.write_text("\n".join(lines), encoding="utf-8")
