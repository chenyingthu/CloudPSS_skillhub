"""
Voltage Stability Analysis Skill

电压稳定性分析 - 通过连续潮流计算PV曲线，识别电压崩溃点
支持负荷增长扫描和关键母线电压监测
"""

import csv
import json
import logging
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional

from cloudpss_skills.core import (
    Artifact,
    LogEntry,
    SkillBase,
    SkillResult,
    SkillStatus,
    ValidationResult,
    register,
)
from cloudpss_skills.core.utils import parse_cloudpss_table
from cloudpss_skills.core.auth_utils import load_or_fetch_model, run_powerflow

logger = logging.getLogger(__name__)


@register
class VoltageStabilitySkill(SkillBase):
    """电压稳定性分析技能"""

    @property
    def name(self) -> str:
        return "voltage_stability"

    @property
    def description(self) -> str:
        return "电压稳定性分析 - 通过连续潮流计算PV曲线，识别电压崩溃点"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "voltage_stability"},
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
                    "properties": {
                        "load_scaling": {
                            "type": "array",
                            "items": {"type": "number"},
                            "default": [1.0, 1.2, 1.4, 1.6, 1.8, 2.0],
                            "description": "负荷增长倍数列表",
                        },
                        "load_target": {
                            "type": "string",
                            "description": "目标负荷组件标签（可选，默认所有负荷）",
                        },
                        "scale_generation": {
                            "type": "boolean",
                            "default": True,
                            "description": "是否同时调整发电机出力",
                        },
                    },
                },
                "monitoring": {
                    "type": "object",
                    "properties": {
                        "buses": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "监测电压的母线列表",
                        },
                        "collapse_threshold": {
                            "type": "number",
                            "default": 0.7,
                            "description": "电压崩溃阈值(pu)",
                        },
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"enum": ["json", "csv"], "default": "json"},
                        "path": {"type": "string", "default": "./results/"},
                        "prefix": {"type": "string", "default": "voltage_stability"},
                        "generate_report": {"type": "boolean", "default": True},
                        "export_pv_curve": {"type": "boolean", "default": True},
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
                "load_scaling": [1.0, 1.2, 1.4, 1.6, 1.8, 2.0],
                "scale_generation": True,
            },
            "monitoring": {
                "buses": ["Bus30", "Bus38"],
                "collapse_threshold": 0.7,
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "voltage_stability",
                "generate_report": True,
                "export_pv_curve": True,
            },
        }

    def run(self, config: Dict[str, Any]) -> SkillResult:
        import time

        start_time = datetime.now()
        logs = []
        artifacts = []

        def log(level: str, message: str):
            logs.append(
                LogEntry(timestamp=datetime.now(), level=level, message=message)
            )
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
            base_model = load_or_fetch_model(model_config)
            log("INFO", f"模型: {base_model.name}")

            scan_config = config.get("scan", {})
            monitoring_config = config.get("monitoring", {})
            output_config = config.get("output", {})

            load_scaling = scan_config.get(
                "load_scaling", [1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
            )
            load_target = scan_config.get("load_target")
            scale_generation = scan_config.get("scale_generation", True)

            target_buses = monitoring_config.get("buses", [])
            collapse_threshold = monitoring_config.get("collapse_threshold", 0.7)

            log("INFO", f"电压稳定性分析: {len(load_scaling)}个负荷水平")
            log("INFO", f"负荷增长范围: {min(load_scaling)}x ~ {max(load_scaling)}x")
            log("INFO", f"监测母线: {target_buses}")
            log("INFO", f"电压崩溃阈值: {collapse_threshold} pu")

            # 获取基线负荷和发电机信息
            base_loads, base_gens = self._get_base_components(base_model, load_target)
            log("INFO", f"基线负荷数: {len(base_loads)}, 发电机数: {len(base_gens)}")

            # 连续潮流计算
            results = []
            converged_cases = []
            collapse_point = None
            max_loadability = None

            for i, scale in enumerate(load_scaling):
                log("INFO", f"[{i + 1}/{len(load_scaling)}] 负荷水平={scale}x")
                working_model = Model(deepcopy(base_model.toJSON()))

                # 调整负荷和发电机
                self._scale_loads_and_generation(
                    working_model, base_loads, base_gens, scale, scale_generation, log
                )

                # 运行潮流
                try:
                    job = run_powerflow(working_model, config)
                    log("INFO", f"  Job ID: {job.id}")

                    # 等待完成
                    max_wait = 60
                    waited = 0
                    while waited < max_wait:
                        status = job.status()
                        if status == 1:
                            break
                        if status == 2:
                            raise RuntimeError("潮流计算失败")
                        time.sleep(1)
                        waited += 1

                    if job.status() != 1:
                        log("WARNING", f"  潮流计算超时或失败")
                        results.append(
                            {
                                "scale": scale,
                                "converged": False,
                                "voltages": {},
                            }
                        )
                        continue

                    # 提取结果
                    result = job.result
                    voltages = self._extract_bus_voltages(result, target_buses)
                    if target_buses and len(voltages) == 0:
                        raise RuntimeError("未从潮流结果中提取到任何目标母线电压")
                    min_voltage = min(voltages.values()) if voltages else 1.0

                    case_result = {
                        "scale": scale,
                        "converged": True,
                        "job_id": job.id,
                        "voltages": voltages,
                        "min_voltage": min_voltage,
                    }
                    results.append(case_result)
                    converged_cases.append(case_result)

                    log("INFO", f"  -> 最小电压: {min_voltage:.4f} pu")

                    # 检查电压崩溃
                    if min_voltage < collapse_threshold:
                        if collapse_point is None:
                            collapse_point = scale
                        log("WARNING", f"  电压低于崩溃阈值!")

                except (
                    AttributeError,
                    ConnectionError,
                    RuntimeError,
                    FileNotFoundError,
                    ValueError,
                ) as e:
                    log("ERROR", f"  计算失败: {e}")
                    results.append(
                        {
                            "scale": scale,
                            "converged": False,
                            "error": str(e),
                        }
                    )
                    # 记录失败但继续下一个负荷水平，不中断扫描
                    continue

            # 计算最大负荷能力
            if converged_cases:
                max_loadability = converged_cases[-1]["scale"]

            # 生成PV曲线数据点
            pv_curve_data = self._generate_pv_curve(converged_cases, target_buses)

            # 导出结果
            output_path = Path(output_config.get("path", "./results/"))
            output_path.mkdir(parents=True, exist_ok=True)
            prefix = output_config.get("prefix", "voltage_stability")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            result_data = {
                "model": base_model.name,
                "collapse_threshold": collapse_threshold,
                "collapse_point": collapse_point,
                "max_loadability": max_loadability,
                "total_cases": len(results),
                "converged_cases": len(converged_cases),
                "results": results,
                "pv_curve": pv_curve_data,
            }

            # JSON输出
            json_path = output_path / f"{prefix}_{timestamp}.json"
            with open(json_path, "w") as f:
                json.dump(result_data, f, indent=2)
            artifacts.append(
                Artifact(
                    type="json",
                    path=str(json_path),
                    size=json_path.stat().st_size,
                    description="电压稳定性分析结果",
                )
            )

            # CSV输出
            csv_path = output_path / f"{prefix}_{timestamp}.csv"
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                headers = ["load_scale", "converged", "min_voltage"] + [
                    f"V_{bus}" for bus in target_buses
                ]
                writer.writerow(headers)
                for r in results:
                    row = [
                        r["scale"],
                        r.get("converged", False),
                        r.get("min_voltage", 0),
                    ]
                    for bus in target_buses:
                        row.append(r.get("voltages", {}).get(bus, 0))
                    writer.writerow(row)
            artifacts.append(
                Artifact(
                    type="csv",
                    path=str(csv_path),
                    size=csv_path.stat().st_size,
                    description="电压稳定性CSV",
                )
            )

            # PV曲线数据
            if output_config.get("export_pv_curve", True) and pv_curve_data:
                pv_path = output_path / f"{prefix}_pv_curve_{timestamp}.csv"
                with open(pv_path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["bus", "load_scale", "voltage_pu"])
                    for point in pv_curve_data:
                        writer.writerow(
                            [point["bus"], point["scale"], point["voltage"]]
                        )
                artifacts.append(
                    Artifact(
                        type="csv",
                        path=str(pv_path),
                        size=pv_path.stat().st_size,
                        description="PV曲线数据",
                    )
                )

            # 生成报告
            if output_config.get("generate_report", True):
                report_path = output_path / f"{prefix}_report_{timestamp}.md"
                self._generate_report(result_data, report_path, target_buses)
                artifacts.append(
                    Artifact(
                        type="markdown",
                        path=str(report_path),
                        size=report_path.stat().st_size,
                        description="电压稳定性分析报告",
                    )
                )

            overall_status = (
                SkillStatus.SUCCESS if converged_cases else SkillStatus.FAILED
            )
            return SkillResult(
                skill_name=self.name,
                status=overall_status,
                start_time=start_time,
                end_time=datetime.now(),
                data=result_data,
                artifacts=artifacts,
                logs=logs,
            )

        except (
            AttributeError,
            ConnectionError,
            RuntimeError,
            FileNotFoundError,
            ValueError,
            TypeError,
        ) as e:
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

    def _get_base_components(
        self, model, load_target: Optional[str]
    ) -> Tuple[List, List]:
        """获取基线负荷和发电机组件"""
        components = model.getAllComponents()
        loads = []
        gens = []

        for key, comp in components.items():
            if not hasattr(comp, "args"):
                continue

            comp_def = getattr(comp, "definition", "")
            comp_label = getattr(comp, "label", "")

            # 识别负荷 - 支持多种负荷定义
            if any(x in comp_def for x in ["Load", "_newExpLoad", "_newLoad"]):
                if (
                    load_target is None
                    or comp_label == load_target
                    or load_target in key
                ):
                    loads.append({"key": key, "component": comp, "label": comp_label})

            # 识别发电机（用于调整出力）
            if "Generator" in comp_def or "Gen" in comp_def:
                gens.append({"key": key, "component": comp, "label": comp_label})

        return loads, gens

    def _scale_loads_and_generation(
        self, model, loads: List, gens: List, scale: float, scale_gen: bool, log_func
    ):
        """调整负荷和发电机出力"""
        import logging

        logger = logging.getLogger(__name__)

        total_load_p = 0

        # 调整负荷
        for load_info in loads:
            comp = load_info["component"]
            key = load_info["key"]

            if not hasattr(comp, "args") or comp.args is None:
                continue

            # 尝试获取负荷参数（支持多种参数名）
            # IEEE39使用 _newExpLoad_3p: 参数是 'p' 和 'q'
            # IEEE3使用 _newLoad: 参数是 'pf_P' 和 'pf_Q'

            # 检查负荷类型
            comp_def = getattr(comp, "definition", "")

            if "_newExpLoad" in comp_def:
                # 指数负荷模型 - 使用 p, q 参数
                p_source = comp.args.get("p", {}).get("source", "1")
                q_source = comp.args.get("q", {}).get("source", "0")

                try:
                    base_P = float(p_source)
                    base_Q = float(q_source)
                except (ValueError, TypeError):
                    continue

                new_P = base_P * scale
                new_Q = base_Q * scale

                args = {
                    "p": {"source": str(new_P), "ɵexp": ""},
                    "q": {"source": str(new_Q), "ɵexp": ""},
                }

                try:
                    model.updateComponent(key, args=args)
                    total_load_p += new_P
                except (AttributeError, TypeError) as e:
                    logger.debug(f"Failed to update load {key}: {e}")

            else:
                # 标准负荷模型 - 使用 pf_P, pf_Q 参数
                pf_P = comp.args.get("pf_P", {}).get("source", "1")
                pf_Q = comp.args.get("pf_Q", {}).get("source", "0")

                try:
                    base_P = float(pf_P)
                    base_Q = float(pf_Q)
                except (ValueError, TypeError):
                    continue

                new_P = base_P * scale
                new_Q = base_Q * scale

                args = {
                    "pf_P": {"source": str(new_P), "ɵexp": ""},
                    "pf_Q": {"source": str(new_Q), "ɵexp": ""},
                }

                try:
                    model.updateComponent(key, args=args)
                    total_load_p += new_P
                except (AttributeError, TypeError) as e:
                    logger.debug(f"Failed to update load {key}: {e}")

        # 同时调整发电机出力（维持功率平衡）
        if scale_gen and gens and scale > 1.0 and total_load_p > 0:
            # 按比例调整发电机出力
            for gen_info in gens:
                comp = gen_info["component"]
                key = gen_info["key"]

                if not hasattr(comp, "args") or comp.args is None:
                    continue

                # 检查发电机类型
                comp_def = getattr(comp, "definition", "")

                if "_newGenerator" in comp_def or "SyncGenerator" in comp_def:
                    # 同步发电机 - 使用 pf_P 参数
                    pf_P = comp.args.get("pf_P", {}).get("source", "1")
                    try:
                        base_P = float(pf_P)
                    except (ValueError, TypeError):
                        continue

                    new_P = base_P * scale
                    args = {
                        "pf_P": {"source": str(new_P), "ɵexp": ""},
                    }

                    try:
                        model.updateComponent(key, args=args)
                    except (AttributeError, TypeError) as e:
                        logger.debug(f"Failed to update generator {key}: {e}")

    def _extract_bus_voltages(
        self, result, target_buses: List[str]
    ) -> Dict[str, float]:
        """提取母线电压"""
        voltages = {}
        if not target_buses:
            return voltages

        bus_rows = parse_cloudpss_table(result.getBuses())
        for row in bus_rows:
            bus_id = str(row.get("Bus", "") or "")
            bus_name = str(row.get("Node", "") or row.get("name", "") or "")
            vm = row.get("Vm")
            if vm is None:
                vm = row.get("<i>V</i><sub>m</sub> / pu")

            try:
                vm_value = float(vm)
            except (TypeError, ValueError):
                continue

            for target_bus in target_buses:
                if self._matches_bus_identifier(
                    target_bus, bus_id
                ) or self._matches_bus_identifier(target_bus, bus_name):
                    voltages[target_bus] = vm_value

        return voltages

    @staticmethod
    def _matches_bus_identifier(target: str, candidate: str) -> bool:
        target_norm = str(target or "").strip().lower()
        candidate_norm = str(candidate or "").strip().lower()
        if not target_norm or not candidate_norm:
            return False
        if target_norm == candidate_norm:
            return True
        return target_norm in candidate_norm or candidate_norm in target_norm

    def _generate_pv_curve(
        self, converged_cases: List, target_buses: List[str]
    ) -> List[Dict]:
        """生成PV曲线数据点"""
        pv_data = []
        for case in converged_cases:
            scale = case["scale"]
            for bus, voltage in case.get("voltages", {}).items():
                pv_data.append(
                    {
                        "bus": bus,
                        "scale": scale,
                        "voltage": voltage,
                    }
                )
        return pv_data

    def _generate_report(self, data: Dict, path: Path, target_buses: List[str]):
        """生成Markdown报告"""
        lines = [
            "# 电压稳定性分析报告",
            "",
            f"**模型**: {data['model']}",
            f"**电压崩溃阈值**: {data['collapse_threshold']} pu",
            f"**总计算工况**: {data['total_cases']}",
            f"**收敛工况**: {data['converged_cases']}",
            "",
        ]

        if data.get("collapse_point"):
            lines.extend(
                [
                    "## 电压稳定性评估",
                    "",
                    f"⚠️ **电压崩溃点**: 约在负荷水平 **{data['collapse_point']}x** 处",
                    f"**最大负荷能力**: {data.get('max_loadability', 'N/A')}x",
                    "",
                ]
            )
        else:
            lines.extend(
                [
                    "## 电压稳定性评估",
                    "",
                    f"✅ 在给定负荷范围内未发生电压崩溃",
                    f"**最大负荷能力**: {data.get('max_loadability', 'N/A')}x",
                    "",
                ]
            )

        lines.extend(
            [
                "## 电压变化情况",
                "",
                "| 负荷水平 | 收敛 | 最小电压(pu) | "
                + " | ".join([f"{b}(pu)" for b in target_buses])
                + " |",
                "|----------|------|--------------|"
                + "|".join(["--------"] * len(target_buses))
                + "|",
            ]
        )

        for r in data.get("results", []):
            conv_str = "是" if r.get("converged") else "否"
            min_v = f"{r.get('min_voltage', 0):.4f}" if r.get("converged") else "-"
            bus_voltages = []
            for bus in target_buses:
                v = r.get("voltages", {}).get(bus, 0)
                bus_voltages.append(f"{v:.4f}" if r.get("converged") else "-")
            lines.append(
                f"| {r['scale']:.2f} | {conv_str} | {min_v} | "
                + " | ".join(bus_voltages)
                + " |"
            )

        lines.extend(
            [
                "",
                "## PV曲线数据",
                "",
                "负荷增长过程中的母线电压变化可用于绘制PV曲线。",
                "",
                "## 结论",
                "",
            ]
        )

        if data.get("collapse_point"):
            lines.append(
                f"系统在负荷增长至 {data['collapse_point']}x 时接近电压崩溃，建议加强电压支撑措施。"
            )
        else:
            lines.append(
                f"系统在测试范围内保持电压稳定，最大负荷能力约为 {data.get('max_loadability', 'N/A')}x。"
            )

        path.write_text("\n".join(lines), encoding="utf-8")
