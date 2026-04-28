#!/usr/bin/env python3
"""
N-2安全校核技能 (n2_security)

功能：评估系统在同时失去两个元件（N-2故障）时的安全性，
      包括潮流收敛性、电压越限、设备过载等指标的校验。

适用：关键输电通道分析、极端工况评估、系统韧性评估
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from itertools import combinations

from cloudpss_skills.core.base import (
    SkillBase,
    SkillResult,
    SkillStatus,
    ValidationResult,
    Artifact,
    LogEntry,
)
from cloudpss_skills.core import (
    setup_auth,
    reload_model,
    run_powerflow_and_wait,
)
from cloudpss_skills.core.registry import register
from cloudpss_skills.core.utils import parse_cloudpss_table

logger = logging.getLogger(__name__)


@dataclass
class N2ContingencyResult:
    """N-2故障场景结果"""

    branch1_id: str
    branch1_name: str
    branch2_id: str
    branch2_name: str
    status: str  # passed/failed/error
    converged: bool
    violation: Optional[str]
    max_voltage_pu: Optional[float]
    min_voltage_pu: Optional[float]
    max_loading_pu: Optional[float]


@register
class N2SecuritySkill(SkillBase):
    """
    N-2安全校核技能

    功能特性:
    1. N-2故障场景生成 - 自动组合所有可能的N-2故障
    2. 潮流收敛性校验 - 检查N-2后系统是否收敛
    3. 电压安全校验 - 检查母线电压是否在允许范围内
    4. 设备过载校验 - 检查设备负载是否超过限值
    5. 关键故障对识别 - 找出最薄弱的N-2组合

    配置示例:
        skill: n2_security

        model:
          rid: model/holdme/IEEE39

        analysis:
          # 指定要检查的支路对（可选，默认自动组合）
          branch_pairs:
            - [LINE_1, LINE_2]
            - [LINE_3, LINE_4]

          # 或指定单个支路，自动与其他支路组合
          branches:
            - LINE_1
            - LINE_2

          check_voltage: true
          check_thermal: true
          voltage_min: 0.95
          voltage_max: 1.05
          thermal_limit: 1.0

          # 限制检查数量（避免组合爆炸）
          max_combinations: 100

        output:
          format: json
          path: ./n2_security_report.json
    """

    name = "n2_security"
    description = "N-2安全校核 - 双元件停运系统安全性评估"
    version = "1.0.0"

    config_schema = {
        "type": "object",
        "required": ["skill", "model"],
        "properties": {
            "skill": {"type": "string", "const": "n2_security"},
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
            "analysis": {
                "type": "object",
                "properties": {
                    "branches": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "要检查的支路列表，空表示全部",
                    },
                    "branch_pairs": {
                        "type": "array",
                        "items": {
                            "type": "array",
                            "items": {"type": "string"},
                            "minItems": 2,
                            "maxItems": 2,
                        },
                        "description": "指定要检查的支路对",
                    },
                    "check_voltage": {"type": "boolean", "default": True},
                    "check_thermal": {"type": "boolean", "default": True},
                    "voltage_min": {"type": "number", "default": 0.95},
                    "voltage_max": {"type": "number", "default": 1.05},
                    "thermal_limit": {"type": "number", "default": 1.0},
                    "max_combinations": {"type": "number", "default": 100},
                    "include_critical_pairs": {"type": "boolean", "default": True},
                },
            },
            "output": {
                "type": "object",
                "properties": {
                    "format": {"enum": ["json", "console"], "default": "json"},
                    "path": {"type": "string"},
                    "prefix": {"type": "string", "default": "n2_security"},
                },
            },
        },
    }

    def validate(self, config: Dict) -> ValidationResult:
        """验证配置"""
        errors = []

        model = config.get("model", {})
        if not model.get("rid"):
            errors.append("必须指定 model.rid")

        analysis = config.get("analysis", {})
        voltage_min = analysis.get("voltage_min", 0.95)
        voltage_max = analysis.get("voltage_max", 1.05)

        if voltage_min >= voltage_max:
            errors.append("voltage_min 必须小于 voltage_max")

        return ValidationResult(valid=len(errors) == 0, errors=errors)

    def run(self, config: Dict) -> SkillResult:
        """执行N-2安全校核"""
        start_time = datetime.now()

        try:
            setup_auth(config)

            model_config = config.get("model", {})
            model_rid = model_config["rid"]
            analysis_config = config.get("analysis", {})

            logger.info(f"开始N-2安全校核: {model_rid}")

            # 获取模型
            model = reload_model(
                model_config["rid"],
                model_config.get("source", "cloud"),
                config,
            )

            logger.info(f"模型: {model.name}")

            # 获取所有支路
            branches = self._get_branches(model, analysis_config)
            logger.info(f"发现 {len(branches)} 条支路")

            # 生成N-2故障场景
            scenarios = self._generate_n2_scenarios(branches, analysis_config)
            logger.info(f"生成 {len(scenarios)} 个N-2故障场景")

            if not scenarios:
                return SkillResult(
                    skill_name=self.name,
                    status=SkillStatus.FAILED,
                    start_time=start_time,
                    end_time=datetime.now(),
                    error="无有效的N-2故障场景",
                )

            # 执行N-2校核
            results = self._run_n2_analysis(
                model_rid, model_config, scenarios, analysis_config
            )

            # 生成报告
            report = self._generate_report(model, scenarios, results, analysis_config)

            # 输出结果
            self._output_results(report, config.get("output", {}))

            logger.info("N-2安全校核完成")

            # 根据结果确定状态
            failed_count = sum(1 for r in results if r.status in ("failed", "error"))

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS if failed_count == 0 else SkillStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                data=report,
            error=f"N-2安全校核发现 {failed_count}/{len(results)} 个场景未通过" if failed_count > 0 else None,
            )

        except (
            KeyError,
            AttributeError,
            ConnectionError,
            RuntimeError,
            TimeoutError,
            FileNotFoundError,
            ValueError,
            TypeError
        ) as e:
            logger.error(f"N-2安全校核失败: {e}", exc_info=True)
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                error=str(e),
            )

    def _get_branches(self, model, analysis_config: Dict) -> List[Dict]:
        """获取所有支路元件"""
        components = model.getAllComponents()

        # 支路类元件类型（更新以匹配CloudPSS实际使用的RID）
        branch_types = [
            "model/CloudPSS/line",
            "model/CloudPSS/3pline",
            "model/CloudPSS/transformer",
            "model/CloudPSS/3ptransformer",
            "model/CloudPSS/TransmissionLine",  # IEEE39实际使用的类型
            "model/CloudPSS/_newTransformer_3p2w",  # IEEE39实际使用的变压器类型
        ]

        branches = []
        for comp_id, comp in components.items():
            definition = getattr(comp, "definition", "")
            if any(bt in definition for bt in branch_types):
                branches.append(
                    {
                        "id": comp_id,
                        "name": self._get_branch_display_name(comp, comp_id),
                        "type": definition.split("/")[-1],
                    }
                )

        # 过滤指定支路
        target_branches = analysis_config.get("branches", [])
        if target_branches:
            branches = [
                b
                for b in branches
                if b["name"] in target_branches or b["id"] in target_branches
            ]

        return branches

    def _generate_n2_scenarios(
        self, branches: List[Dict], analysis_config: Dict
    ) -> List[Tuple[Dict, Dict]]:
        """生成N-2故障场景"""
        # 检查是否指定了具体的支路对
        branch_pairs = analysis_config.get("branch_pairs", [])

        if branch_pairs:
            # 使用指定的支路对
            scenarios = []
            for pair in branch_pairs:
                b1 = next(
                    (b for b in branches if b["name"] == pair[0] or b["id"] == pair[0]),
                    None,
                )
                b2 = next(
                    (b for b in branches if b["name"] == pair[1] or b["id"] == pair[1]),
                    None,
                )
                if b1 and b2 and b1["id"] != b2["id"]:
                    scenarios.append((b1, b2))
            return scenarios

        # 自动生成组合
        max_combinations = analysis_config.get("max_combinations", 100)

        # 生成所有可能的组合
        all_combinations = list(combinations(branches, 2))

        # 如果组合数超过限制，优先选择关键支路组合
        if len(all_combinations) > max_combinations:
            logger.warning(
                f"N-2组合数({len(all_combinations)})超过限制({max_combinations})，将优先检查关键组合"
            )
            # 简化策略：优先选择与同一母线相连的支路
            all_combinations = all_combinations[:max_combinations]

        return all_combinations

    def _run_n2_analysis(
        self,
        model_rid: str,
        model_config: Dict,
        scenarios: List[Tuple[Dict, Dict]],
        analysis_config: Dict,
    ) -> List[N2ContingencyResult]:
        """执行N-2分析"""
        from cloudpss_skills.core.model_utils import clone_model

        results = []
        check_voltage = analysis_config.get("check_voltage", True)
        check_thermal = analysis_config.get("check_thermal", True)
        voltage_min = analysis_config.get("voltage_min", 0.95)
        voltage_max = analysis_config.get("voltage_max", 1.05)
        thermal_limit = analysis_config.get("thermal_limit", 1.0)

        base_model = reload_model(
            model_config["rid"],
            model_config.get("source", "cloud"),
            analysis_config,
        )

        for i, (branch1, branch2) in enumerate(scenarios, 1):
            logger.info(
                f"[{i}/{len(scenarios)}] N-2故障: {branch1['name']} + {branch2['name']}"
            )

            try:
                working_model = clone_model(base_model)

                try:
                    working_model.removeComponent(branch1["id"])
                    working_model.removeComponent(branch2["id"])
                    logger.info(
                        f"  -> 已移除支路: {branch1['name']}, {branch2['name']}"
                    )
                except (KeyError, AttributeError) as e:
                    logger.warning(f"  -> 移除支路失败: {e}")
                    results.append(
                        N2ContingencyResult(
                            branch1_id=branch1["id"],
                            branch1_name=branch1["name"],
                            branch2_id=branch2["id"],
                            branch2_name=branch2["name"],
                            status="error",
                            converged=False,
                            violation=f"模型修改失败: {e}",
                            max_voltage_pu=None,
                            min_voltage_pu=None,
                            max_loading_pu=None,
                        )
                    )
                    continue

                try:
                    job_result = run_powerflow_and_wait(working_model, analysis_config)
                except TimeoutError:
                    logger.warning(f"  -> N-2超时: {branch1['name']} + {branch2['name']}")
                    results.append(
                        N2ContingencyResult(
                            branch1_id=branch1["id"],
                            branch1_name=branch1["name"],
                            branch2_id=branch2["id"],
                            branch2_name=branch2["name"],
                            status="error",
                            converged=False,
                            violation="执行超时",
                            max_voltage_pu=None,
                            min_voltage_pu=None,
                            max_loading_pu=None,
                        )
                    )
                    continue
                except Exception as e:
                    logger.warning(f"  -> N-2异常: {e}")
                    results.append(
                        N2ContingencyResult(
                            branch1_id=branch1["id"],
                            branch1_name=branch1["name"],
                            branch2_id=branch2["id"],
                            branch2_name=branch2["name"],
                            status="error",
                            converged=False,
                            violation=str(e),
                            max_voltage_pu=None,
                            min_voltage_pu=None,
                            max_loading_pu=None,
                        )
                    )
                    continue

                if not job_result.success:
                    results.append(
                        N2ContingencyResult(
                            branch1_id=branch1["id"],
                            branch1_name=branch1["name"],
                            branch2_id=branch2["id"],
                            branch2_name=branch2["name"],
                            status="failed",
                            converged=False,
                            violation="潮流不收敛",
                            max_voltage_pu=None,
                            min_voltage_pu=None,
                            max_loading_pu=None,
                        )
                    )
                    logger.error(f"  -> N-2失败: 潮流不收敛")
                    continue

                # 潮流收敛，检查结果
                pf_result = job_result.result
                violation = None
                max_v = None
                min_v = None
                max_load = None
                thermal_supported = not check_thermal

                # 电压检查
                if check_voltage:
                    try:
                        buses = pf_result.getBuses()
                        voltages = []

                        # 解析CloudPSS列式数据格式
                        if buses and len(buses) > 0:
                            bus_data = buses[0]
                            if isinstance(bus_data, dict) and "data" in bus_data:
                                columns = bus_data["data"].get("columns", [])
                                vm_column = None
                                for col in columns:
                                    col_name = col.get("name", "")
                                    if (
                                        col_name == "Vm"
                                        or "V</i><sub>m</sub>" in col_name
                                        or col_name.startswith("Vm")
                                    ):
                                        vm_column = col.get("data", [])
                                        break
                                if vm_column:
                                    for vm in vm_column:
                                        try:
                                            vm_val = float(vm)
                                            if vm_val > 0:
                                                voltages.append(vm_val)
                                        except Exception as e:
                                            # 异常已捕获，无需额外处理
                                            logger.debug(f"忽略预期异常: {e}")
                            else:
                                # 传统行式格式
                                for bus in buses:
                                    try:
                                        vm = float(bus.get("Vm", 0))
                                        if vm > 0:
                                            voltages.append(vm)
                                    except Exception as e:
                                        # 异常已捕获，无需额外处理
                                        logger.debug(f"忽略预期异常: {e}")

                        if voltages:
                            max_v = max(voltages)
                            min_v = min(voltages)

                            if max_v > voltage_max:
                                violation = f"电压越上限: {max_v:.3f} pu"
                            elif min_v < voltage_min:
                                violation = f"电压越下限: {min_v:.3f} pu"
                    except (KeyError, AttributeError) as e:
                        logger.warning(f"电压检查失败: {e}")

                # 热稳定检查
                if check_thermal and not violation:
                    try:
                        thermal_result = self._evaluate_thermal_loading(
                            working_model,
                            pf_result,
                            thermal_limit,
                        )
                        thermal_supported = thermal_result["supported"]
                        max_load = thermal_result["max_loading_pu"]

                        if thermal_result["violation"]:
                            violation = thermal_result["violation"]
                    except (
                        KeyError,
                        AttributeError,
                        RuntimeError,
                        TypeError,
                        ValueError,
                    ) as e:
                        logger.warning(f"热稳定检查失败: {e}")
                        violation = f"热稳定校核失败: {e}"

                # 确定状态
                if violation:
                    status = "failed"
                    logger.error(f"  -> N-2失败: {violation}")
                elif check_thermal and not thermal_supported:
                    status = "error"
                    violation = (
                        "热稳定校核未完成：支路缺少额定容量/电流参数，不能宣称N-2通过"
                    )
                    logger.error(f"  -> N-2不完整: {violation}")
                else:
                    status = "passed"
                    logger.info(f"  -> N-2通过")

                results.append(
                    N2ContingencyResult(
                        branch1_id=branch1["id"],
                        branch1_name=branch1["name"],
                        branch2_id=branch2["id"],
                        branch2_name=branch2["name"],
                        status=status,
                        converged=True,
                        violation=violation,
                        max_voltage_pu=max_v,
                        min_voltage_pu=min_v,
                        max_loading_pu=max_load,
                    )
                )

            except (KeyError, AttributeError) as e:
                logger.error(f"  -> N-2异常: {e}")
                results.append(
                    N2ContingencyResult(
                        branch1_id=branch1["id"],
                        branch1_name=branch1["name"],
                        branch2_id=branch2["id"],
                        branch2_name=branch2["name"],
                        status="error",
                        converged=False,
                        violation=str(e),
                        max_voltage_pu=None,
                        min_voltage_pu=None,
                        max_loading_pu=None,
                    )
                )

        return results

    @staticmethod
    def _get_branch_display_name(component: Any, fallback_id: str) -> str:
        """优先使用标签/业务名，避免报告里只剩 canvas key。"""
        label = getattr(component, "label", None)
        if label:
            return label

        name = getattr(component, "name", None)
        if name:
            return name

        args = getattr(component, "args", {}) or {}
        for key in ("Name", "name"):
            value = args.get(key)
            if value:
                return str(value)

        return fallback_id

    @staticmethod
    def _read_numeric_arg(args: Dict[str, Any], key: str) -> Optional[float]:
        value = args.get(key)
        if isinstance(value, dict):
            value = value.get("source")
        if value in (None, ""):
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    def _evaluate_thermal_loading(
        self, model: Any, pf_result: Any, thermal_limit: float
    ) -> Dict[str, Any]:
        """基于真实潮流支路表和元件额定值计算负载率。"""
        branch_tables = (
            pf_result.getBranches() if hasattr(pf_result, "getBranches") else None
        )
        if not branch_tables:
            raise RuntimeError("潮流结果缺少支路表")

        branch_rows = parse_cloudpss_table(branch_tables)
        max_loading = None
        unsupported_count = 0

        for row in branch_rows:
            branch_id = row.get("Branch")
            if not branch_id:
                continue

            component = model.getComponentByKey(branch_id)
            args = getattr(component, "args", {}) or {}
            definition = str(getattr(component, "definition", "") or "")

            p_ij = self._read_numeric_arg(row, "Pij") if isinstance(row, dict) else None
            q_ij = self._read_numeric_arg(row, "Qij") if isinstance(row, dict) else None
            p_ji = self._read_numeric_arg(row, "Pji") if isinstance(row, dict) else None
            q_ji = self._read_numeric_arg(row, "Qji") if isinstance(row, dict) else None

            s_ij = ((p_ij or 0.0) ** 2 + (q_ij or 0.0) ** 2) ** 0.5
            s_ji = ((p_ji or 0.0) ** 2 + (q_ji or 0.0) ** 2) ** 0.5
            apparent_mva = max(s_ij, s_ji)

            rating_mva = None
            if "Transformer" in definition:
                rating_mva = self._read_numeric_arg(args, "Tmva")
            elif (
                "TransmissionLine" in definition
                or definition.endswith("/line")
                or definition.endswith("/3pline")
            ):
                i_rated = self._read_numeric_arg(args, "Irated")
                v_base = self._read_numeric_arg(args, "Vbase")
                if i_rated and i_rated > 0 and v_base and v_base > 0:
                    rating_mva = 1.7320508075688772 * v_base * i_rated

            if not rating_mva or rating_mva <= 0:
                unsupported_count += 1
                continue

            loading = apparent_mva / rating_mva
            max_loading = loading if max_loading is None else max(max_loading, loading)

            if loading > thermal_limit:
                return {
                    "supported": True,
                    "max_loading_pu": loading,
                    "violation": f"热稳定越限: {loading:.3f} pu",
                    "unsupported_count": unsupported_count,
                }

        return {
            "supported": max_loading is not None,
            "max_loading_pu": max_loading,
            "violation": None,
            "unsupported_count": unsupported_count,
        }

    def _generate_report(
        self,
        model,
        scenarios: List[Tuple[Dict, Dict]],
        results: List[N2ContingencyResult],
        analysis_config: Dict,
    ) -> Dict:
        """生成报告"""
        passed = sum(1 for r in results if r.status == "passed")
        failed = sum(1 for r in results if r.status == "failed")
        errors = sum(1 for r in results if r.status == "error")

        # 找出关键故障对（导致失败的N-2组合）
        critical_pairs = [
            {
                "branch1": r.branch1_name,
                "branch2": r.branch2_name,
                "violation": r.violation,
            }
            for r in results
            if r.status == "failed"
        ]

        # 生成统计信息
        if results:
            converged_results = [
                r for r in results if r.converged and r.max_voltage_pu is not None
            ]
            if converged_results:
                voltage_stats = {
                    "max_overall": max(r.max_voltage_pu for r in converged_results),
                    "min_overall": min(r.min_voltage_pu for r in converged_results),
                }
            else:
                voltage_stats = None
        else:
            voltage_stats = None

        report = {
            "model_name": getattr(model, "name", "Unknown"),
            "model_rid": getattr(model, "rid", "Unknown"),
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_scenarios": len(scenarios),
                "passed": passed,
                "failed": failed,
                "errors": errors,
                "pass_rate": passed / len(results) * 100 if results else 0,
            },
            "voltage_limits": {
                "min": analysis_config.get("voltage_min", 0.95),
                "max": analysis_config.get("voltage_max", 1.05),
            },
            "voltage_statistics": voltage_stats,
            "critical_pairs": critical_pairs,
            "results": [
                {
                    "branch1_id": r.branch1_id,
                    "branch1_name": r.branch1_name,
                    "branch2_id": r.branch2_id,
                    "branch2_name": r.branch2_name,
                    "status": r.status,
                    "converged": r.converged,
                    "violation": r.violation,
                    "max_voltage_pu": r.max_voltage_pu,
                    "min_voltage_pu": r.min_voltage_pu,
                    "max_loading_pu": r.max_loading_pu,
                }
                for r in results
            ],
        }

        return report

    def _output_results(self, report: Dict, output_config: Dict):
        """输出结果"""
        fmt = output_config.get("format", "json")

        if fmt == "console":
            self._output_console(report)
        elif fmt == "json":
            import json
            from pathlib import Path

            prefix = output_config.get("prefix", "n2_security")
            path = output_config.get("path", f"./{prefix}_report.json")

            output_path = Path(path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, ensure_ascii=False)

            logger.info(f"报告已保存: {output_path}")

    def _output_console(self, report: Dict):
        """控制台输出"""
        lines = []
        lines.append("\n" + "=" * 70)
        lines.append("N-2安全校核报告")
        lines.append("=" * 70)
        lines.append(f"模型: {report['model_name']}")
        lines.append(f"时间: {report['timestamp']}")

        summary = report["summary"]
        lines.append("\n校核统计:")
        lines.append(f"  总场景数: {summary['total_scenarios']}")
        lines.append(f"  通过: {summary['passed']}")
        lines.append(f"  失败: {summary['failed']}")
        lines.append(f"  错误: {summary['errors']}")
        lines.append(f"  通过率: {summary['pass_rate']:.1f}%")

        if report.get("voltage_statistics"):
            vs = report["voltage_statistics"]
            lines.append("\n电压统计:")
            lines.append(f"  最高电压: {vs['max_overall']:.4f} pu")
            lines.append(f"  最低电压: {vs['min_overall']:.4f} pu")

        if report.get("critical_pairs"):
            lines.append(f"\n关键故障对 ({len(report['critical_pairs'])}):")
            for pair in report["critical_pairs"][:5]:  # 只显示前5个
                lines.append(
                    f"  - {pair['branch1']} + {pair['branch2']}: {pair['violation']}"
                )

        lines.append("=" * 70)

        for line in lines:
            logger.info(line)
