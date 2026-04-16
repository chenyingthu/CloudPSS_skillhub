"""
Voltage Stability Analysis Skill

电压稳定性分析 - 通过连续潮流计算PV曲线，识别电压崩溃点
支持负荷增长扫描和关键母线电压监测
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from cloudpss_skills.core import (
    Artifact,
    LogEntry,
    SkillBase,
    SkillResult,
    SkillStatus,
    ValidationResult,
    register,
)
from cloudpss_skills.core import (
    setup_auth,
    clone_model,
    reload_model,
    run_powerflow_and_wait,
    OutputConfig,
    save_json,
    save_csv,
    generate_report,
)
from cloudpss_skills.core.utils import parse_cloudpss_table

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
        start_time = datetime.now()
        logs = []
        artifacts = []

        def log(level: str, message: str):
            logs.append(
                LogEntry(timestamp=datetime.now(), level=level, message=message)
            )
            getattr(logger, level.lower(), logger.info)(message)

        try:
            setup_auth(config)
            log("INFO", "认证成功")

            model_config = config["model"]
            base_model = reload_model(
                model_config["rid"],
                model_config.get("source", "cloud"),
                config,
            )
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

            base_loads, base_gens = self._get_base_components(base_model, load_target)
            log("INFO", f"基线负荷数: {len(base_loads)}, 发电机数: {len(base_gens)}")

            results = []
            converged_cases = []
            collapse_point = None
            max_loadability = None

            for i, scale in enumerate(load_scaling):
                log("INFO", f"[{i + 1}/{len(load_scaling)}] 负荷水平={scale}x")

                working_model = clone_model(base_model)

                self._scale_loads_and_generation(
                    working_model, base_loads, base_gens, scale, scale_generation, log
                )

                try:
                    job_result = run_powerflow_and_wait(
                        working_model, config, log_func=log
                    )

                    if not job_result.success:
                        log("WARNING", f"  潮流计算失败")
                        fallback_voltages = {}
                        if converged_cases:
                            fallback_voltages = converged_cases[-1].get("voltages", {})
                        results.append(
                            {
                                "scale": scale,
                                "converged": False,
                                "voltages": fallback_voltages,
                                "note": "潮流计算失败，使用上一个收敛水平的电压值作为参考",
                            }
                        )
                        continue

                    result = job_result.result
                    voltages = self._extract_bus_voltages(result, target_buses)
                    if target_buses and len(voltages) == 0:
                        raise RuntimeError("未从潮流结果中提取到任何目标母线电压")
                    min_voltage = min(voltages.values()) if voltages else 1.0

                    job_id = getattr(getattr(job_result, "job", None), "id", None)
                    case_result = {
                        "scale": scale,
                        "converged": True,
                        "job_id": job_id,
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
                    ValueError,
                ) as e:
                    log("ERROR", f"  计算失败: {e}")
                    fallback_voltages = {}
                    if converged_cases:
                        fallback_voltages = converged_cases[-1].get("voltages", {})
                    results.append(
                        {
                            "scale": scale,
                            "converged": False,
                            "voltages": fallback_voltages,
                            "error": str(e),
                        }
                    )
                    continue

            # 计算最大负荷能力
            if converged_cases:
                max_loadability = converged_cases[-1]["scale"]

            # 生成PV曲线数据点
            pv_curve_data = self._generate_pv_curve(converged_cases, target_buses)

            # 导出结果
            output = OutputConfig(
                path=output_config.get("path", "./results/"),
                prefix=output_config.get("prefix", "voltage_stability"),
                timestamp=True,
            )

            result_data = {
                "model": base_model.name,
                "model_rid": base_model.rid,
                "collapse_threshold": collapse_threshold,
                "collapse_point": collapse_point,
                "max_loadability": max_loadability,
                "total_cases": len(results),
                "converged_cases": len(converged_cases),
                "monitored_buses": target_buses,
                "results": results,
                "pv_curve": pv_curve_data,
            }

            # JSON输出
            export_result = save_json(
                result_data, output, description="电压稳定性分析结果"
            )
            if export_result.artifact:
                artifacts.append(export_result.artifact)

            # CSV输出
            csv_data = []
            headers = ["load_scale", "converged", "min_voltage"] + [
                f"V_{bus}" for bus in target_buses
            ]
            for r in results:
                row = [r["scale"], r.get("converged", False), r.get("min_voltage", 0)]
                for bus in target_buses:
                    row.append(r.get("voltages", {}).get(bus, 0))
                csv_data.append(row)
            export_csv = save_csv(
                csv_data,
                output,
                suffix="data",
                headers=headers,
                description="电压稳定性CSV",
            )
            if export_csv.artifact:
                artifacts.append(export_csv.artifact)

            # PV曲线数据
            if output_config.get("export_pv_curve", True) and pv_curve_data:
                pv_data = [[p["bus"], p["scale"], p["voltage"]] for p in pv_curve_data]
                export_pv = save_csv(
                    pv_data,
                    output,
                    suffix="pv_curve",
                    headers=["bus", "load_scale", "voltage_pu"],
                    description="PV曲线数据",
                )
                if export_pv.artifact:
                    artifacts.append(export_pv.artifact)

            # 生成报告
            if output_config.get("generate_report", True):
                report_content = self._generate_report_content(
                    result_data, target_buses
                )
                export_md = generate_report(
                    report_content,
                    output,
                    suffix="report",
                    description="电压稳定性分析报告",
                )
                if export_md.artifact:
                    artifacts.append(export_md.artifact)

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
                data={
                    "success": False,
                    "error": str(e),
                    "stage": "voltage_stability",
                },
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

    def _generate_report_content(self, data: Dict, target_buses: List[str]) -> str:
        """生成Markdown报告内容"""
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

        return "\n".join(lines)
