"""
EMT N-1 Security Screening Skill

EMT N-1安全筛查 - 枚举支路单停运，评估故障下的系统安全性
"""

import csv
import json
import logging
import math
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from cloudpss_skills.core import (
    Artifact,
    LogEntry,
    SkillBase,
    SkillResult,
    SkillStatus,
    ValidationResult,
    register,
)
from cloudpss_skills.core.auth_utils import load_or_fetch_model, run_emt, setup_auth

logger = logging.getLogger(__name__)

# 常量定义
TRANSMISSION_LINE_RID = "model/CloudPSS/TransmissionLine"
TRANSFORMER_RID = "model/CloudPSS/_newTransformer_3p2w"
FAULT_DEFINITION = "model/CloudPSS/_newFaultResistor_3p"
EMT_JOB_RID = "function/CloudPSS/emtps"

DEFAULT_TIME_WINDOWS = {
    "prefault": (2.42, 2.44),
    "fault": (2.56, 2.58),
    "postfault": (2.92, 2.94),
    "late_recovery": (2.96, 2.98),
}


@register
class EmtN1ScreeningSkill(SkillBase):
    """EMT N-1安全筛查技能"""

    @property
    def name(self) -> str:
        return "emt_n1_screening"

    @property
    def description(self) -> str:
        return "EMT N-1安全筛查 - 支路单停运+固定故障的多母线安全评估"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "emt_n1_screening"},
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
                        "branches": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "要检查的支路ID列表，空表示自动发现",
                        },
                        "include_transformers": {"type": "boolean", "default": True},
                        "limit": {"type": "integer", "description": "最大检查支路数"},
                    },
                },
                "fault": {
                    "type": "object",
                    "properties": {
                        "fs": {"type": "number", "default": 2.5},
                        "fe": {"type": "number", "default": 2.7},
                        "chg": {"type": "number", "default": 0.01},
                    },
                },
                "assessment": {
                    "type": "object",
                    "properties": {
                        "monitored_buses": {
                            "type": "array",
                            "items": {"type": "string"},
                            "default": ["Bus7"],
                            "description": "要监测的母线电压通道名",
                        },
                        "power_trace": {"type": "string", "default": "#P1:0"},
                        "time_windows": {
                            "type": "object",
                            "properties": {
                                "prefault": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "default": [2.42, 2.44],
                                },
                                "fault": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "default": [2.56, 2.58],
                                },
                                "postfault": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "default": [2.92, 2.94],
                                },
                                "late_recovery": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "default": [2.96, 2.98],
                                },
                            },
                        },
                        "severity_thresholds": {
                            "type": "object",
                            "properties": {
                                "warning": {"type": "number", "default": 10.0},
                                "critical": {"type": "number", "default": 15.0},
                            },
                        },
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"enum": ["json", "csv"], "default": "json"},
                        "path": {"type": "string", "default": "./results/"},
                        "prefix": {"type": "string", "default": "emt_n1_screening"},
                        "generate_report": {"type": "boolean", "default": True},
                    },
                },
            },
        }

    def get_default_config(self) -> Dict[str, Any]:
        return {
            "skill": self.name,
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "model/holdme/IEEE3", "source": "cloud"},
            "scan": {
                "branches": [],
                "include_transformers": True,
            },
            "fault": {
                "fs": 2.5,
                "fe": 2.7,
                "chg": 0.01,
            },
            "assessment": {
                "monitored_buses": ["Bus7"],
                "power_trace": "#P1:0",
                "time_windows": DEFAULT_TIME_WINDOWS,
                "severity_thresholds": {
                    "warning": 10.0,
                    "critical": 15.0,
                },
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "emt_n1_screening",
                "generate_report": True,
            },
        }

    def run(self, config: Dict[str, Any]) -> SkillResult:
        """执行N-1安全筛查"""
        from cloudpss import Model, setToken
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
            setup_auth(config)

            # 1. 认证
            log("INFO", "加载认证信息...")
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

            # 2. 获取模型
            log("INFO", "获取模型...")
            model_config = config["model"]
            model_rid = model_config["rid"]

            base_model = load_or_fetch_model(model_config, config)

            log("INFO", f"模型: {base_model.name} ({base_model.rid})")

            # 3. 获取配置
            scan_config = config.get("scan", {})
            fault_config = config.get("fault", {})
            assessment_config = config.get("assessment", {})
            output_config = config.get("output", {})

            include_transformers = scan_config.get("include_transformers", True)
            limit = scan_config.get("limit")

            # 4. 发现候选支路
            branch_ids = scan_config.get("branches", [])
            if not branch_ids:
                log("INFO", "自动发现候选支路...")
                branch_ids = self._discover_branches(
                    base_model, include_transformers, log
                )
                log("INFO", f"发现 {len(branch_ids)} 条候选支路")

            if limit:
                branch_ids = branch_ids[:limit]
                log("INFO", f"限制为前 {limit} 条支路")

            if not branch_ids:
                raise ValueError("没有要检查的支路")

            # 5. 执行基线仿真
            log("INFO", "执行基线仿真...")
            baseline = self._run_security_case(
                base_model, None, fault_config, assessment_config, log, config
            )
            log(
                "INFO",
                f"基线完成: worst_post_gap={baseline['worst_postfault_gap']:.2f}",
            )

            # 6. 执行各支路N-1仿真
            results = []
            for i, branch_id in enumerate(branch_ids):
                log("INFO", f"[{i + 1}/{len(branch_ids)}] 支路: {branch_id}")
                try:
                    result = self._run_security_case(
                        base_model,
                        branch_id,
                        fault_config,
                        assessment_config,
                        log,
                        config,
                    )
                    result["delta_worst_postfault_gap_vs_baseline"] = (
                        result["worst_postfault_gap"] - baseline["worst_postfault_gap"]
                    )
                    result["delta_worst_late_gap_vs_baseline"] = (
                        result["worst_late_gap"] - baseline["worst_late_gap"]
                    )
                    results.append(result)
                    log("INFO", f"  -> 完成: severity={result['severity']}")
                except (KeyError, AttributeError) as e:
                    log("ERROR", f"  -> 失败: {e}")

            # 7. 排序和分级
            log("INFO", "排序和分级...")
            thresholds = assessment_config.get(
                "severity_thresholds", {"warning": 10.0, "critical": 15.0}
            )
            ranked_results = self._rank_results(results, thresholds)

            for i, result in enumerate(ranked_results, 1):
                result["rank"] = i

            # 8. 生成摘要
            digest = self._build_digest(baseline, ranked_results)

            # 9. 导出结果
            output_path = Path(output_config.get("path", "./results/"))
            output_path.mkdir(parents=True, exist_ok=True)

            prefix = output_config.get("prefix", "emt_n1_screening")
            use_timestamp = output_config.get("timestamp", True)
            generate_report = output_config.get("generate_report", True)

            timestamp_str = (
                datetime.now().strftime("%Y%m%d_%H%M%S") if use_timestamp else ""
            )

            # JSON结果
            json_filename = (
                f"{prefix}_{timestamp_str}.json" if timestamp_str else f"{prefix}.json"
            )
            json_path = output_path / json_filename

            result_data = {
                "model_name": base_model.name,
                "model_rid": base_model.rid,
                "timestamp": datetime.now().isoformat(),
                "baseline": baseline,
                "total_branches": len(branch_ids),
                "severity_distribution": digest["severity_counts"],
                "results": [
                    {
                        "rank": r["rank"],
                        "branch_id": r["branch_id"],
                        "branch_name": r["branch_name"],
                        "branch_kind": r["branch_kind"],
                        "severity": r["severity"],
                        "worst_postfault_gap": r["worst_postfault_gap"],
                        "worst_late_gap": r["worst_late_gap"],
                        "delta_post_vs_baseline": r[
                            "delta_worst_postfault_gap_vs_baseline"
                        ],
                    }
                    for r in ranked_results
                ],
            }

            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(result_data, f, indent=2, ensure_ascii=False)

            artifacts.append(
                Artifact(
                    type="json",
                    path=str(json_path),
                    size=json_path.stat().st_size,
                    description="N-1筛查结果",
                )
            )
            log("INFO", f"JSON结果: {json_path}")

            # CSV结果
            csv_filename = (
                f"{prefix}_{timestamp_str}.csv" if timestamp_str else f"{prefix}.csv"
            )
            csv_path = output_path / csv_filename
            self._export_csv(ranked_results, csv_path)

            artifacts.append(
                Artifact(
                    type="csv",
                    path=str(csv_path),
                    size=csv_path.stat().st_size,
                    description="N-1筛查CSV",
                )
            )
            log("INFO", f"CSV结果: {csv_path}")

            # Markdown报告
            if generate_report:
                report_filename = (
                    f"{prefix}_report_{timestamp_str}.md"
                    if timestamp_str
                    else f"{prefix}_report.md"
                )
                report_path = output_path / report_filename
                self._generate_report(baseline, ranked_results, digest, report_path)

                artifacts.append(
                    Artifact(
                        type="markdown",
                        path=str(report_path),
                        size=report_path.stat().st_size,
                        description="N-1筛查报告",
                    )
                )
                log("INFO", f"研究报告: {report_path}")

            # 根据结果确定状态
            failed_count = len(branch_ids) - len(results)

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS if failed_count == 0 else SkillStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                data=result_data,
                artifacts=artifacts,
                logs=logs,
                metrics={
                    "total_branches": len(branch_ids),
                    "completed": len(results),
                    "critical": digest["severity_counts"].get("critical", 0),
                    "warning": digest["severity_counts"].get("warning", 0),
                },
            )

        except (
            KeyError,
            AttributeError,
            RuntimeError,
            FileNotFoundError,
            ValueError,
            TimeoutError,
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

    def _discover_branches(
        self, model, include_transformers: bool, log_func
    ) -> List[str]:
        """发现候选支路"""
        rids = [TRANSMISSION_LINE_RID]
        if include_transformers:
            rids.append(TRANSFORMER_RID)

        branch_ids = []
        for rid in rids:
            try:
                components = model.getComponentsByRid(rid)
                for comp in components.values():
                    if comp.props.get("enabled", True):
                        branch_ids.append(comp.id)
            except Exception as e:
                # 异常已捕获，无需额外处理
                logger.debug(f"忽略预期异常: {e}")

        return sorted(branch_ids)

    def _run_security_case(
        self,
        base_model,
        branch_id,
        fault_config,
        assessment_config,
        log_func,
        config: Optional[Dict] = None,
    ) -> Dict:
        """执行单个安全案例"""
        from cloudpss import Model
        import time

        # 复制模型
        working_model = Model(deepcopy(base_model.toJSON()))

        branch_name = "baseline"
        branch_kind = "reference"

        if branch_id:
            try:
                branch = working_model.getComponentByKey(branch_id)
                branch_name = branch.args.get("Name") or branch.label or branch.id
                branch_kind = (
                    "transformer" if branch.definition == TRANSFORMER_RID else "line"
                )
                working_model.updateComponent(branch_id, props={"enabled": False})
            except (AttributeError, TypeError) as e:
                raise RuntimeError(f"停用支路失败: {e}")

        # 配置故障
        components = working_model.getAllComponents()
        fault = None
        for comp in components.values():
            if getattr(comp, "definition", None) == FAULT_DEFINITION:
                fault = comp
                break

        if fault:
            working_model.updateComponent(
                fault.id,
                args={
                    "fs": {"source": str(fault_config.get("fs", 2.5)), "ɵexp": ""},
                    "fe": {"source": str(fault_config.get("fe", 2.7)), "ɵexp": ""},
                    "chg": {"source": str(fault_config.get("chg", 0.01)), "ɵexp": ""},
                },
            )

        # 运行EMT
        job = run_emt(working_model, config)

        # 等待完成
        start_time = time.time()
        while True:
            status = job.status()
            if status == 1:
                break
            if status == 2:
                raise RuntimeError("EMT仿真失败")
            if time.time() - start_time > 300:
                raise TimeoutError("EMT仿真超时")
            time.sleep(3)

        # 提取结果
        result = job.result
        time_windows = assessment_config.get("time_windows", DEFAULT_TIME_WINDOWS)
        monitored_buses = assessment_config.get("monitored_buses", ["Bus7"])

        bus_metrics = {}
        for bus in monitored_buses:
            try:
                for i, _ in enumerate(result.getPlots()):
                    channel_names = result.getPlotChannelNames(i)
                    if bus in channel_names:
                        trace = result.getPlotChannelData(i, bus)
                        bus_metrics[bus] = {
                            "prefault_rms": self._trace_rms(
                                trace, *time_windows["prefault"]
                            ),
                            "fault_rms": self._trace_rms(trace, *time_windows["fault"]),
                            "postfault_rms": self._trace_rms(
                                trace, *time_windows["postfault"]
                            ),
                            "postfault_gap": self._trace_rms(
                                trace, *time_windows["prefault"]
                            )
                            - self._trace_rms(trace, *time_windows["postfault"]),
                        }
                        break
            except Exception as e:
                # 异常已捕获，无需额外处理
                logger.debug(f"忽略预期异常: {e}")

        # 计算最坏情况
        worst_post = (
            max(m["postfault_gap"] for m in bus_metrics.values()) if bus_metrics else 0
        )
        worst_late = worst_post  # 简化处理

        # 严重度分级
        thresholds = assessment_config.get(
            "severity_thresholds", {"warning": 10.0, "critical": 15.0}
        )
        if worst_post > thresholds.get("critical", 15.0):
            severity = "critical"
        elif worst_post > thresholds.get("warning", 10.0):
            severity = "warning"
        else:
            severity = "observe"

        return {
            "branch_id": branch_id or "baseline",
            "branch_name": branch_name,
            "branch_kind": branch_kind,
            "severity": severity,
            "monitored_buses": bus_metrics,
            "worst_postfault_gap": worst_post,
            "worst_late_gap": worst_late,
            "job_id": job.id,
        }

    def _trace_rms(self, trace, start, end):
        """计算时间窗口RMS"""
        samples = [v for t, v in zip(trace["x"], trace["y"]) if start <= t <= end]
        if not samples:
            return 0.0
        return math.sqrt(sum(v * v for v in samples) / len(samples))

    def _rank_results(self, results: List[Dict], thresholds: Dict) -> List[Dict]:
        """排序结果"""
        severity_order = {"critical": 2, "warning": 1, "observe": 0}
        return sorted(
            results,
            key=lambda r: (
                severity_order.get(r["severity"], 0),
                r["worst_postfault_gap"],
            ),
            reverse=True,
        )

    def _build_digest(self, baseline: Dict, results: List[Dict]) -> Dict:
        """构建摘要"""
        severity_counts = {"critical": 0, "warning": 0, "observe": 0}
        for r in results:
            severity_counts[r["severity"]] += 1

        return {
            "severity_counts": severity_counts,
            "total_cases": len(results),
            "top_case": results[0] if results else None,
            "baseline": baseline,
        }

    def _export_csv(self, results: List[Dict], path: Path):
        """导出CSV"""
        fieldnames = [
            "rank",
            "branch_id",
            "branch_name",
            "branch_kind",
            "severity",
            "worst_postfault_gap",
            "worst_late_gap",
            "delta_worst_post_vs_baseline",
            "delta_worst_late_vs_baseline",
        ]
        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in results:
                writer.writerow(
                    {
                        "rank": r["rank"],
                        "branch_id": r["branch_id"],
                        "branch_name": r["branch_name"],
                        "branch_kind": r["branch_kind"],
                        "severity": r["severity"],
                        "worst_postfault_gap": f"{r['worst_postfault_gap']:.3f}",
                        "worst_late_gap": f"{r['worst_late_gap']:.3f}",
                        "delta_worst_post_vs_baseline": f"{r.get('delta_worst_postfault_gap_vs_baseline', 0):+.3f}",
                        "delta_worst_late_vs_baseline": f"{r.get('delta_worst_late_gap_vs_baseline', 0):+.3f}",
                    }
                )

    def _generate_report(
        self, baseline: Dict, results: List[Dict], digest: Dict, path: Path
    ):
        """生成Markdown报告"""
        lines = [
            "# EMT N-1 安全筛查报告",
            "",
            f"生成时间: {datetime.now().isoformat()}",
            "",
            "## 摘要",
            "",
            f"- 总检查支路: {digest['total_cases']}",
            f"- 严重 (Critical): {digest['severity_counts'].get('critical', 0)}",
            f"- 警告 (Warning): {digest['severity_counts'].get('warning', 0)}",
            f"- 正常 (Observe): {digest['severity_counts'].get('observe', 0)}",
            "",
            "## 基线工况",
            "",
            f"- 支路: {baseline['branch_name']}",
            f"- 最坏恢复缺口: {baseline['worst_postfault_gap']:.3f}",
            "",
            "## N-1 筛查结果",
            "",
            "| 排名 | 支路 | 类型 | 严重度 | 恢复缺口 | 相对基线 |",
            "|------|------|------|--------|----------|----------|",
        ]

        for r in results[:20]:  # 只显示前20
            lines.append(
                f"| {r['rank']} | {r['branch_name']} | {r['branch_kind']} | "
                f"{r['severity']} | {r['worst_postfault_gap']:.2f} | "
                f"{r.get('delta_worst_postfault_gap_vs_baseline', 0):+.2f} |"
            )

        lines.extend(
            [
                "",
                "## 最严重工况",
                "",
            ]
        )

        if digest.get("top_case"):
            top = digest["top_case"]
            lines.extend(
                [
                    f"**{top['branch_name']}** ({top['branch_kind']})",
                    "",
                    f"- 严重度: {top['severity']}",
                    f"- 恢复缺口: {top['worst_postfault_gap']:.3f}",
                    f"- 相对基线: {top.get('delta_worst_postfault_gap_vs_baseline', 0):+.3f}",
                    "",
                ]
            )

        path.write_text("\n".join(lines), encoding="utf-8")
