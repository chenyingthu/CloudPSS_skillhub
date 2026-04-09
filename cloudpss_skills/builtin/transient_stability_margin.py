#!/usr/bin/env python3
"""
暂态稳定裕度评估技能 (transient_stability_margin)

功能：基于暂态稳定分析，计算稳定裕度指标，包括临界切除时间(CCT)、
      稳定裕度百分比、稳定边界等。

适用：评估系统暂态稳定储备、确定运行极限、稳定性风险评估

作者: Claude Code
日期: 2026-04-01
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

from cloudpss_skills.core.base import SkillBase, SkillResult, SkillStatus, ValidationResult
from cloudpss_skills.core.auth_utils import setup_auth, DEFAULT_TIMEOUT, fetch_model_by_rid
from cloudpss_skills.core.emt_fault_core import clone_model, find_fault_component, apply_fault_parameters, run_emt_and_wait, find_trace, trace_rms
from cloudpss_skills.core.registry import register

logger = logging.getLogger(__name__)


@dataclass
class StabilityMargin:
    """稳定裕度数据"""
    fault_location: str
    cct: float  # Critical Clearing Time (s)
    margin_percent: float
    stability_status: str  # stable/marginal/unstable


@register
class TransientStabilityMarginSkill(SkillBase):
    """
    暂态稳定裕度评估技能

    功能特性:
    1. 临界切除时间(CCT)计算 - 二分法精确计算
    2. 稳定裕度评估 - 基于实际切除时间与CCT的比值
    3. 稳定边界确定 - 找出系统的稳定运行边界
    4. 多场景批量评估 - 支持N-1场景下的裕度评估

    配置示例:
        skill: transient_stability_margin

        model:
          rid: model/holdme/IEEE39

        fault_scenarios:
          - location: BUS_10
            type: three_phase
            duration: 0.1

        generators:
          - GEN_1
          - GEN_2

        analysis:
          compute_cct: true
          compute_margin: true
          margin_baseline: 0.5  # 基准切除时间

        output:
          format: json
          path: ./stability_margin_report.json
    """

    name = "transient_stability_margin"
    description = "暂态稳定裕度评估(CCT/稳定边界/多场景)"
    version = "1.0.0"

    config_schema = {
        "type": "object",
        "required": ["skill", "model"],
        "properties": {
            "skill": {"type": "string", "const": "transient_stability_margin"},
            "auth": {
                "type": "object",
                "properties": {
                    "token": {"type": "string"},
                    "token_file": {"type": "string", "default": ".cloudpss_token"}
                }
            },
            "model": {
                "type": "object",
                "required": ["rid"],
                "properties": {
                    "rid": {"type": "string"},
                    "source": {"enum": ["cloud", "local"], "default": "cloud"}
                }
            },
            "fault_scenarios": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string"},
                        "type": {"enum": ["three_phase", "single_phase", "line_ground"], "default": "three_phase"},
                        "duration": {"type": "number", "default": 0.1}
                    },
                    "required": ["location"]
                }
            },
            "generators": {
                "type": "array",
                "items": {"type": "string"},
                "description": "需要监控的发电机列表"
            },
                "analysis": {
                    "type": "object",
                    "properties": {
                        "compute_cct": {"type": "boolean", "default": True},
                        "compute_margin": {"type": "boolean", "default": True},
                        "margin_baseline": {"type": "number", "default": 0.5},
                        "cct_initial_upper_bound": {"type": "number", "default": 1.0},
                        "cct_search_upper_bound": {"type": "number", "default": 5.0},
                        "cct_bound_expansion_factor": {"type": "number", "default": 2.0},
                        "cct_tolerance": {"type": "number", "default": 0.001},
                        "max_iterations": {"type": "integer", "default": 20},
                        "emt_timeout": {"type": "number", "default": 300.0},
                        "stability_trace_name": {"type": "string", "default": "vac:0"},
                        "postfault_min_ratio": {"type": "number", "default": 0.9},
                        "late_recovery_min_ratio": {"type": "number", "default": 0.95},
                        "prefault_window_offset": {
                            "type": "array",
                            "items": {"type": "number"},
                            "default": [-0.08, -0.06],
                        },
                        "postfault_window_offset": {
                            "type": "array",
                            "items": {"type": "number"},
                            "default": [0.22, 0.24],
                        },
                        "late_recovery_window_offset": {
                            "type": "array",
                            "items": {"type": "number"},
                            "default": [0.46, 0.48],
                        }
                    }
                },
            "output": {
                "type": "object",
                "properties": {
                    "format": {"enum": ["json", "console"], "default": "json"},
                    "path": {"type": "string"}
                }
            }
        }
    }

    def validate(self, config: Dict) -> ValidationResult:
        """验证配置"""
        errors = []
        warnings = []

        model = config.get("model", {})
        if not model.get("rid"):
            errors.append("必须指定 model.rid")

        scenarios = config.get("fault_scenarios", [])
        if not scenarios:
            warnings.append("建议至少指定一个故障场景")

        return ValidationResult(valid=len(errors) == 0, errors=errors, warnings=warnings)

    def run(self, config: Dict) -> SkillResult:
        """执行暂态稳定裕度评估"""
        start_time = datetime.now()

        try:
            setup_auth(config)

            model_config = config.get("model", {})
            model_rid = model_config["rid"]
            scenarios = config.get("fault_scenarios", [])

            logger.info(f"开始暂态稳定裕度评估: {model_rid}")
            logger.info(f"故障场景数: {len(scenarios)}")

            report = {
                "model_rid": model_rid,
                "timestamp": datetime.now().isoformat(),
                "scenarios": []
            }

            for i, scenario in enumerate(scenarios, 1):
                logger.info(f"\n分析场景 {i}/{len(scenarios)}: {scenario['location']}")
                scenario_result = self._analyze_scenario(model_rid, scenario, config)
                report["scenarios"].append(scenario_result)

            # 生成总体评估
            report["summary"] = self._generate_summary(report["scenarios"])
            report["summary"]["verified"] = fully_verified = all(
                scenario.get("cct", {}).get("verified", True) and scenario.get("margin", {}).get("verified", True)
                for scenario in report["scenarios"]
            )
            if not fully_verified:
                report["summary"]["overall_assessment"] = "当前结果仅供初步评估"
                report["summary"]["limitations"] = [
                    "CCT与裕度仍基于简化稳定性判据，不能作为正式暂态稳定结论"
                ]

            # 输出结果
            self._output_results(report, config.get("output", {}))

            logger.info("暂态稳定裕度评估完成")

            final_status = SkillStatus.SUCCESS if fully_verified else SkillStatus.FAILED
            error = None if fully_verified else "当前CCT与稳定裕度仍基于简化稳定性判据，不能作为正式暂态稳定裕度结论"

            return SkillResult(
                skill_name=self.name,
                status=final_status,
                start_time=start_time,
                end_time=datetime.now(),
                data=report,
                error=error,
            )

        except (KeyError, AttributeError, ConnectionError, RuntimeError, TimeoutError, FileNotFoundError, ValueError, TypeError, Exception) as e:
            error_message = str(e)
            if isinstance(e, TimeoutError):
                error_message = (
                    f"{error_message}。当前 CCT 搜索需要多次 EMT 仿真，"
                    "可尝试增大 analysis.emt_timeout，或先减小 analysis.max_iterations / 放宽 analysis.cct_tolerance。"
                )
            logger.error(f"暂态稳定裕度评估失败: {e}", exc_info=True)
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                error=error_message
            )

    def _analyze_scenario(self, model_rid: str, scenario: Dict, config: Dict) -> Dict:
        """分析单个故障场景的裕度"""
        location = scenario["location"]
        fault_type = scenario.get("type", "three_phase")

        result = {
            "fault_location": location,
            "fault_type": fault_type,
            "base_duration": scenario.get("duration", 0.1)
        }

        analysis_config = config.get("analysis", {})

        # 1. 计算临界切除时间(CCT)
        if analysis_config.get("compute_cct", True):
            logger.info(f"  计算CCT...")
            cct = self._compute_cct(model_rid, scenario, config)
            result["cct"] = cct

        # 2. 计算稳定裕度
        if analysis_config.get("compute_margin", True) and "cct" in result:
            logger.info(f"  计算稳定裕度...")
            baseline = analysis_config.get("margin_baseline", 0.5)
            margin = self._compute_margin(result["cct"], baseline)
            result["margin"] = margin

        return result

    def _compute_cct(self, model_rid: str, scenario: Dict, config: Dict) -> Dict:
        """
        计算临界切除时间(Critical Clearing Time)

        使用二分法精确计算CCT：
        1. 确定初始上下界（稳定/不稳定）
        2. 二分查找直到收敛
        3. 返回精确的CCT值
        """
        base_model = fetch_model_by_rid(model_rid, config)
        location = scenario["location"]
        fault_type = scenario.get("type", "three_phase")

        # 初始范围
        t_min = 0.0  # 肯定稳定
        analysis = config.get("analysis", {})
        t_max = float(analysis.get("cct_initial_upper_bound", 1.0))
        search_upper_bound = float(analysis.get("cct_search_upper_bound", 5.0))
        bound_expansion_factor = float(analysis.get("cct_bound_expansion_factor", 2.0))

        tolerance = analysis.get("cct_tolerance", 0.001)
        max_iterations = analysis.get("max_iterations", 20)

        logger.info(f"    二分法搜索CCT...")

        lower_stable = t_min
        upper_unstable = None
        bound_iterations = 0
        upper_bound_evidence = None

        while t_max <= search_upper_bound:
            stable_at_upper, upper_bound_evidence = self._check_stability(base_model, scenario, t_max, config)
            if not stable_at_upper:
                upper_unstable = t_max
                break
            lower_stable = t_max
            bound_iterations += 1
            if t_max >= search_upper_bound:
                break
            expanded = t_max * bound_expansion_factor if t_max > 0 else max(tolerance, 0.1)
            if expanded <= t_max:
                expanded = t_max + max(tolerance, 0.1)
            t_max = min(search_upper_bound, expanded)
            if t_max == lower_stable:
                break

        if upper_unstable is None:
            return {
                "cct_seconds": round(lower_stable, 4),
                "cct_relation": ">=",
                "iterations": bound_iterations,
                "tolerance": tolerance,
                "method": "bound-search",
                "bounded": False,
                "search_upper_bound": search_upper_bound,
                "verified": False,
                "criterion": upper_bound_evidence or {"stable": True},
                "limitation": (
                    "在给定 cct_search_upper_bound 内未找到不稳定上界，当前结果仅能说明 "
                    f"CCT >= {lower_stable:.4f}s。"
                ),
            }

        t_min = lower_stable
        t_max = upper_unstable
        iterations = bound_iterations
        while t_max - t_min > tolerance and iterations < max_iterations:
            t_mid = (t_min + t_max) / 2

            # 仿真检查稳定性
            stable, evidence = self._check_stability(base_model, scenario, t_mid, config)

            if stable:
                t_min = t_mid
            else:
                t_max = t_mid

            iterations += 1

        cct = (t_min + t_max) / 2
        stable_at_cct, evidence = self._check_stability(base_model, scenario, cct, config)

        return {
            "cct_seconds": round(cct, 4),
            "cct_relation": "=",
            "iterations": iterations,
            "tolerance": tolerance,
            "method": "bisection",
            "bounded": True,
            "search_upper_bound": search_upper_bound,
            "verified": False,
            "criterion": evidence,
            "limitation": "当前CCT基于真实电压恢复波形的近似判据，而非正式功角/转速暂稳判据，不能替代完整暂态稳定校核",
        }

    def _check_stability(self, base_model, scenario: Dict, clearing_time: float, config: Dict) -> Tuple[bool, Dict[str, Any]]:
        """
        检查给定切除时间下的稳定性

        基于真实EMT波形的电压恢复判据：
        - 故障后窗口电压恢复到 prefault 的一定比例以上
        - 晚恢复窗口进一步恢复到更高比例
        """
        try:
            analysis = config.get("analysis", {})
            trace_name = analysis.get("stability_trace_name", "vac:0")
            postfault_min_ratio = analysis.get("postfault_min_ratio", 0.9)
            late_recovery_min_ratio = analysis.get("late_recovery_min_ratio", 0.95)
            emt_timeout = analysis.get("emt_timeout", 300.0)
            prefault_offset = analysis.get("prefault_window_offset", [-0.08, -0.06])
            postfault_offset = analysis.get("postfault_window_offset", [0.22, 0.24])
            late_offset = analysis.get("late_recovery_window_offset", [0.46, 0.48])

            working_model = clone_model(base_model)
            fault = find_fault_component(working_model)
            fault_args = getattr(fault, "args", {}) or {}
            fs = float((fault_args.get("fs", {}) or {}).get("source", scenario.get("fault_time", 3.0)))
            chg = float((fault_args.get("chg", {}) or {}).get("source", 0.01))
            fe = fs + clearing_time
            apply_fault_parameters(working_model, fs, fe, chg)

            job = run_emt_and_wait(working_model, timeout=int(emt_timeout), config=config)
            result = job.result
            _, trace = find_trace(result, trace_name)

            prefault_rms = trace_rms(trace, fs + prefault_offset[0], fs + prefault_offset[1])
            postfault_rms = trace_rms(trace, fe + postfault_offset[0], fe + postfault_offset[1])
            late_rms = trace_rms(trace, fe + late_offset[0], fe + late_offset[1])

            postfault_ratio = postfault_rms / prefault_rms if prefault_rms else 0.0
            late_ratio = late_rms / prefault_rms if prefault_rms else 0.0
            stable = postfault_ratio >= postfault_min_ratio and late_ratio >= late_recovery_min_ratio

            return stable, {
                "trace_name": trace_name,
                "fault_start": fs,
                "fault_end": fe,
                "prefault_rms": round(prefault_rms, 4),
                "postfault_rms": round(postfault_rms, 4),
                "late_recovery_rms": round(late_rms, 4),
                "postfault_ratio": round(postfault_ratio, 4),
                "late_recovery_ratio": round(late_ratio, 4),
                "postfault_min_ratio": postfault_min_ratio,
                "late_recovery_min_ratio": late_recovery_min_ratio,
                "stable": stable,
            }

        except (AttributeError, ConnectionError, RuntimeError, TypeError, TimeoutError) as e:
            logger.warning(f"稳定性检查失败: {e}")
            return False, {"stable": False, "error": str(e)}

    def _compute_margin(self, cct_result: Dict, baseline: float) -> Dict:
        """
        计算稳定裕度

        裕度 = (CCT - 实际切除时间) / CCT * 100%
        或
        裕度 = (CCT - 基准时间) / CCT * 100%
        """
        cct = cct_result.get("cct_seconds", 0)
        bounded = cct_result.get("bounded", True)

        if cct <= 0:
            return {"error": "CCT计算无效"}

        # 使用基准时间计算裕度
        margin_seconds = cct - baseline
        margin_percent = (margin_seconds / cct) * 100 if cct > 0 else 0

        # 判断稳定状态
        if margin_percent >= 30:
            status = "高裕度"
        elif margin_percent >= 10:
            status = "中等裕度"
        elif margin_percent > 0:
            status = "低裕度"
        else:
            status = "不稳定"

        return {
            "cct": round(cct, 4),
            "cct_relation": cct_result.get("cct_relation", "="),
            "bounded": bounded,
            "baseline": baseline,
            "margin_seconds": round(margin_seconds, 4),
            "margin_percent": round(margin_percent, 2),
            "stability_status": status,
            "assessment": self._margin_assessment(margin_percent, bounded=bounded),
            "verified": False,
        }

    def _margin_assessment(self, margin_percent: float, *, bounded: bool = True) -> str:
        """裕度评估结论"""
        if not bounded:
            if margin_percent >= 0:
                return "当前仅得到稳定裕度下界，实际裕度可能更高"
            return "当前仅得到稳定裕度下界，不能据此排除不稳定风险"
        if margin_percent >= 30:
            return "系统暂态稳定裕度充足，可承受较大扰动"
        elif margin_percent >= 10:
            return "系统暂态稳定裕度适中，建议关注"
        elif margin_percent > 0:
            return "系统暂态稳定裕度偏低，建议采取措施"
        else:
            return "系统暂态不稳定，需要改进保护措施"

    def _generate_summary(self, scenarios: List[Dict]) -> Dict:
        """生成总体评估"""
        if not scenarios:
            return {"error": "无场景分析结果"}

        total = len(scenarios)

        # 统计CCT
        ccts = [s["cct"]["cct_seconds"] for s in scenarios if "cct" in s]
        margins = [s["margin"]["margin_percent"] for s in scenarios if "margin" in s]

        summary = {
            "total_scenarios": total,
            "cct_statistics": {
                "min": round(min(ccts), 4) if ccts else None,
                "max": round(max(ccts), 4) if ccts else None,
                "avg": round(sum(ccts) / len(ccts), 4) if ccts else None
            },
            "margin_statistics": {
                "min": round(min(margins), 2) if margins else None,
                "max": round(max(margins), 2) if margins else None,
                "avg": round(sum(margins) / len(margins), 2) if margins else None
            }
        }

        # 最薄弱点
        if margins:
            min_margin_idx = margins.index(min(margins))
            summary["weakest_point"] = {
                "location": scenarios[min_margin_idx]["fault_location"],
                "margin_percent": round(margins[min_margin_idx], 2)
            }

        # 总体结论
        if margins and min(margins) < 0:
            summary["overall_assessment"] = "存在不稳定场景，需要改进"
        elif margins and min(margins) < 10:
            summary["overall_assessment"] = "部分场景裕度偏低，建议关注"
        else:
            summary["overall_assessment"] = "系统暂态稳定裕度整体良好"

        summary["recommendations"] = self._generate_recommendations(scenarios, margins)

        return summary

    def _generate_recommendations(self, scenarios: List[Dict], margins: List[float]) -> List[str]:
        """生成建议"""
        recommendations = []

        if not margins:
            return recommendations

        if min(margins) < 0:
            recommendations.append("存在不稳定场景，建议优化保护切除时间")

        if min(margins) < 10:
            recommendations.append("部分场景裕度偏低，建议加强稳定措施")

        if any(m < 0 for m in margins):
            worst = scenarios[margins.index(min(margins))]
            recommendations.append(f"关注最薄弱点: {worst['fault_location']}")

        if not recommendations:
            recommendations.append("系统暂态稳定裕度良好，维持现有运行方式")

        return recommendations

    def _output_results(self, report: Dict, output_config: Dict):
        """输出结果"""
        fmt = output_config.get("format", "json")

        if fmt == "console":
            self._output_console(report)
        elif fmt == "json":
            import json
            path = output_config.get("path", "./stability_margin_report.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            logger.info(f"报告已保存: {path}")

    def _output_console(self, report: Dict):
        """控制台输出"""
        lines = []
        lines.append("\n" + "=" * 70)
        lines.append("暂态稳定裕度评估报告")
        lines.append("=" * 70)
        lines.append(f"模型: {report['model_rid']}")
        lines.append(f"时间: {report['timestamp']}")
        lines.append(f"\n故障场景数: {len(report['scenarios'])}")

        for scenario in report["scenarios"]:
            lines.append(f"\n场景: {scenario['fault_location']}")
            if "cct" in scenario:
                cct = scenario["cct"]
                relation = cct.get("cct_relation", "=")
                lines.append(f"  CCT: {relation} {cct['cct_seconds']:.4f} s")
            if "margin" in scenario:
                m = scenario['margin']
                lines.append(f"  裕度: {m['margin_percent']:.2f}% ({m['stability_status']})")

        summary = report.get("summary", {})
        lines.append(f"\n总体评估: {summary.get('overall_assessment', '未知')}")

        if "cct_statistics" in summary:
            stats = summary["cct_statistics"]
            lines.append("\nCCT统计:")
            lines.append(f"  最小: {stats.get('min', 'N/A')}")
            lines.append(f"  最大: {stats.get('max', 'N/A')}")
            lines.append(f"  平均: {stats.get('avg', 'N/A')}")

        lines.append("=" * 70)

        for line in lines:
            logger.info(line)
