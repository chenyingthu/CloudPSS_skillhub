"""
EMT Fault Study Skill

EMT故障研究 - 三工况对比分析（基线、延迟切除、轻故障）
"""

import csv
import json
import logging
import math
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from cloudpss_skills.core import (
    Artifact,
    LogEntry,
    SkillBase,
    SkillResult,
    SkillStatus,
    ValidationResult,
    register,
)
from cloudpss_skills.core.auth_utils import load_or_fetch_model, setup_auth
from cloudpss_skills.core.emt_fault_core import (
    configure_channel_sampling,
    run_emt_and_wait,
    clone_model,
    apply_fault_parameters,
    find_trace,
    trace_rms,
)

logger = logging.getLogger(__name__)
VOLTAGE_CHANNEL_NAME = "vac"
VOLTAGE_TRACE_NAME = "vac:0"

# 默认时间窗口
DEFAULT_WINDOWS = {
    "prefault": (2.42, 2.44),
    "fault": (2.56, 2.58),
    "postfault": (2.92, 2.94),
    "late_recovery": (2.96, 2.98),
}


@register
class EmtFaultStudySkill(SkillBase):
    """EMT故障研究技能"""

    @property
    def name(self) -> str:
        return "emt_fault_study"

    @property
    def description(self) -> str:
        return "EMT故障三工况对比研究（基线/延迟切除/轻故障）"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "emt_fault_study"},
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
                        "rid": {
                            "type": "string",
                            "description": "模型RID或本地文件路径",
                        },
                        "source": {"enum": ["cloud", "local"], "default": "cloud"},
                    },
                },
                "scenarios": {
                    "type": "object",
                    "properties": {
                        "baseline": {
                            "type": "object",
                            "properties": {
                                "enabled": {"type": "boolean", "default": True},
                                "fs": {"type": "number", "default": 2.5},
                                "fe": {"type": "number", "default": 2.7},
                                "chg": {"type": "number", "default": 0.01},
                                "description": {
                                    "type": "string",
                                    "default": "基线故障",
                                },
                            },
                        },
                        "delayed_clearing": {
                            "type": "object",
                            "properties": {
                                "enabled": {"type": "boolean", "default": True},
                                "fs": {"type": "number", "default": 2.5},
                                "fe": {"type": "number", "default": 2.9},
                                "chg": {"type": "number", "default": 0.01},
                                "description": {
                                    "type": "string",
                                    "default": "延长故障切除时间",
                                },
                            },
                        },
                        "mild_fault": {
                            "type": "object",
                            "properties": {
                                "enabled": {"type": "boolean", "default": True},
                                "fs": {"type": "number", "default": 2.5},
                                "fe": {"type": "number", "default": 2.7},
                                "chg": {"type": "number", "default": 1e4},
                                "description": {
                                    "type": "string",
                                    "default": "较轻故障",
                                },
                            },
                        },
                    },
                },
                "analysis": {
                    "type": "object",
                    "properties": {
                        "trace_name": {"type": "string", "default": "vac:0"},
                        "voltage_channel_name": {"type": "string", "default": "vac"},
                        "sampling_freq": {"type": "integer", "default": 2000},
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
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"enum": ["json", "csv"], "default": "json"},
                        "path": {"type": "string", "default": "./results/"},
                        "prefix": {"type": "string", "default": "emt_fault_study"},
                        "export_waveforms": {"type": "boolean", "default": True},
                        "waveform_window": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "波形导出时间范围，空表示全部",
                        },
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
            "scenarios": {
                "baseline": {
                    "enabled": True,
                    "fs": 2.5,
                    "fe": 2.7,
                    "chg": 0.01,
                    "description": "基线故障: fe=2.7, chg=0.01",
                },
                "delayed_clearing": {
                    "enabled": True,
                    "fs": 2.5,
                    "fe": 2.9,
                    "chg": 0.01,
                    "description": "延长故障切除: fe=2.9, chg=0.01",
                },
                "mild_fault": {
                    "enabled": True,
                    "fs": 2.5,
                    "fe": 2.7,
                    "chg": 1e4,
                    "description": "较轻故障: fe=2.7, chg=1e4",
                },
            },
            "analysis": {
                "trace_name": "vac:0",
                "sampling_freq": 2000,
                "time_windows": DEFAULT_WINDOWS,
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "emt_fault_study",
                "export_waveforms": True,
                "generate_report": True,
            },
        }

    def run(self, config: Dict[str, Any]) -> SkillResult:
        """执行EMT故障研究"""
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

            if model_config.get("source") == "local":
                base_model = Model.load(model_rid)
            else:
                base_model = load_or_fetch_model(model_config, config)

            log("INFO", f"模型: {base_model.name} ({base_model.rid})")

            # 3. 准备工况配置
            scenarios_config = config.get("scenarios", {})
            analysis_config = config.get("analysis", {})
            output_config = config.get("output", {})

            scenarios = []
            for name in ["baseline", "delayed_clearing", "mild_fault"]:
                scenario_cfg = scenarios_config.get(name, {})
                if scenario_cfg.get("enabled", True):
                    scenarios.append(
                        {
                            "name": name,
                            "description": scenario_cfg.get("description", name),
                            "fs": float(scenario_cfg.get("fs", 2.5)),
                            "fe": float(scenario_cfg.get("fe", 2.7)),
                            "chg": float(scenario_cfg.get("chg", 0.01)),
                        }
                    )

            if not scenarios:
                raise ValueError("至少需要一个启用的工况")

            log("INFO", f"将执行 {len(scenarios)} 个工况的仿真")

            # 4. 执行各工况仿真
            study_results = []
            trace_name = analysis_config.get("trace_name", VOLTAGE_TRACE_NAME)
            sampling_freq = analysis_config.get("sampling_freq", 2000)
            time_windows = analysis_config.get("time_windows", DEFAULT_WINDOWS)

            for i, scenario in enumerate(scenarios):
                log(
                    "INFO",
                    f"[{i + 1}/{len(scenarios)}] 工况: {scenario['name']} - {scenario['description']}",
                )
                log(
                    "INFO",
                    f"  故障参数: fs={scenario['fs']}, fe={scenario['fe']}, chg={scenario['chg']}",
                )

                # 准备模型
                voltage_channel_name = analysis_config.get(
                    "voltage_channel_name", VOLTAGE_CHANNEL_NAME
                )
                working_model = self._prepare_model(
                    base_model, scenario, sampling_freq, voltage_channel_name, log
                )

                # 运行EMT
                job = run_emt_and_wait(
                    working_model, timeout=300, log_func=log, config=config
                )
                job_id = getattr(job, "id", None)
                log("INFO", f"  Job ID: {job_id}")

                # 提取结果
                result = job.result
                metrics = self._extract_metrics(result, trace_name, time_windows, log)

                study_results.append(
                    {
                        "name": scenario["name"],
                        "description": scenario["description"],
                        "fault_end_time": scenario["fe"],
                        "fault_chg": scenario["chg"],
                        "job_id": job_id,
                        "metrics": metrics,
                    }
                )

                log(
                    "INFO",
                    f"  完成: 点数={metrics['point_count']}, "
                    f"故障前RMS={metrics['prefault_rms']:.2f}, "
                    f"故障RMS={metrics['fault_rms']:.2f}",
                )

            # 5. 生成汇总
            log("INFO", "生成结果汇总...")
            summary_rows = self._build_summary_rows(study_results)

            # 6. 导出结果
            output_path = Path(output_config.get("path", "./results/"))
            output_path.mkdir(parents=True, exist_ok=True)

            prefix = output_config.get("prefix", "emt_fault_study")
            use_timestamp = output_config.get("timestamp", True)
            export_waveforms = output_config.get("export_waveforms", True)
            generate_report = output_config.get("generate_report", True)

            timestamp_str = (
                datetime.now().strftime("%Y%m%d_%H%M%S") if use_timestamp else ""
            )

            # 导出JSON汇总
            json_filename = (
                f"{prefix}_{timestamp_str}.json" if timestamp_str else f"{prefix}.json"
            )
            json_path = output_path / json_filename

            result_data = {
                "model_name": base_model.name,
                "model_rid": base_model.rid,
                "timestamp": datetime.now().isoformat(),
                "scenarios": summary_rows,
                "summary": self._build_conclusion_report(summary_rows),
            }

            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(result_data, f, indent=2, ensure_ascii=False)

            artifacts.append(
                Artifact(
                    type="json",
                    path=str(json_path),
                    size=json_path.stat().st_size,
                    description="故障研究汇总结果",
                )
            )
            log("INFO", f"JSON结果: {json_path}")

            # 导出CSV汇总
            csv_filename = (
                f"{prefix}_{timestamp_str}.csv" if timestamp_str else f"{prefix}.csv"
            )
            csv_path = output_path / csv_filename
            self._export_summary_csv(summary_rows, csv_path)

            artifacts.append(
                Artifact(
                    type="csv",
                    path=str(csv_path),
                    size=csv_path.stat().st_size,
                    description="故障研究CSV汇总",
                )
            )
            log("INFO", f"CSV结果: {csv_path}")

            # 导出波形对比
            if export_waveforms:
                waveform_filename = (
                    f"{prefix}_waveforms_{timestamp_str}.csv"
                    if timestamp_str
                    else f"{prefix}_waveforms.csv"
                )
                waveform_path = output_path / waveform_filename
                waveform_window = output_config.get("waveform_window")
                self._export_waveform_csv(study_results, waveform_path, waveform_window)

                artifacts.append(
                    Artifact(
                        type="csv",
                        path=str(waveform_path),
                        size=waveform_path.stat().st_size,
                        description="波形对比数据",
                    )
                )
                log("INFO", f"波形数据: {waveform_path}")

            # 生成Markdown报告
            if generate_report:
                report_filename = (
                    f"{prefix}_report_{timestamp_str}.md"
                    if timestamp_str
                    else f"{prefix}_report.md"
                )
                report_path = output_path / report_filename
                self._generate_report(study_results, summary_rows, report_path)

                artifacts.append(
                    Artifact(
                        type="markdown",
                        path=str(report_path),
                        size=report_path.stat().st_size,
                        description="故障研究报告",
                    )
                )
                log("INFO", f"研究报告: {report_path}")

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                start_time=start_time,
                end_time=datetime.now(),
                data=result_data,
                artifacts=artifacts,
                logs=logs,
                metrics={
                    "scenarios": len(scenarios),
                    "successful": len([r for r in study_results if r["metrics"]]),
                },
            )

        except (KeyError, AttributeError, ZeroDivisionError) as e:
            log("ERROR", f"执行失败: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                data={
                    "success": False,
                    "error": str(e),
                    "stage": "emt_fault_study",
                },
                artifacts=artifacts,
                logs=logs,
                error=str(e),
            )

    def _prepare_model(
        self,
        base_model,
        scenario: Dict,
        sampling_freq: int,
        voltage_channel_name: str,
        log_func,
    ) -> Any:
        """准备工况模型"""
        working_model = clone_model(base_model)
        apply_fault_parameters(
            working_model, scenario["fs"], scenario["fe"], scenario["chg"]
        )
        configure_channel_sampling(working_model, voltage_channel_name, sampling_freq)
        return working_model

    def _extract_metrics(
        self, result, trace_name: str, time_windows: Dict, log_func
    ) -> Dict:
        """提取指标"""
        plot_index, trace = find_trace(result, trace_name)
        time_step = trace["x"][1] - trace["x"][0] if len(trace["x"]) > 1 else None

        return {
            "plot_index": plot_index,
            "trace_name": trace_name,
            "trace": trace,
            "point_count": len(trace["x"]),
            "time_step": time_step,
            "prefault_rms": trace_rms(trace, *time_windows["prefault"]),
            "fault_rms": trace_rms(trace, *time_windows["fault"]),
            "postfault_rms": trace_rms(trace, *time_windows["postfault"]),
            "late_recovery_rms": trace_rms(trace, *time_windows["late_recovery"]),
        }

    def _build_summary_rows(self, study_results: List[Dict]) -> List[Dict]:
        """构建汇总行"""
        baseline = next(r for r in study_results if r["name"] == "baseline")
        baseline_metrics = baseline["metrics"]
        rows = []

        for result in study_results:
            metrics = result["metrics"]
            fault_drop = metrics["prefault_rms"] - metrics["fault_rms"]
            postfault_gap = metrics["prefault_rms"] - metrics["postfault_rms"]
            late_gap = metrics["prefault_rms"] - metrics["late_recovery_rms"]

            observation = "reference"
            if result["name"] == "delayed_clearing":
                observation = "same fault depth, weaker post-fault recovery"
            elif result["name"] == "mild_fault":
                observation = "shallower sag, stronger post-fault recovery"

            rows.append(
                {
                    "scenario": result["name"],
                    "description": result["description"],
                    "fault_end_time": result["fault_end_time"],
                    "fault_chg": result["fault_chg"],
                    "point_count": str(metrics["point_count"]),
                    "prefault_rms": f"{metrics['prefault_rms']:.3f}",
                    "fault_rms": f"{metrics['fault_rms']:.3f}",
                    "postfault_rms": f"{metrics['postfault_rms']:.3f}",
                    "late_recovery_rms": f"{metrics['late_recovery_rms']:.3f}",
                    "fault_drop_vs_prefault": f"{fault_drop:.3f}",
                    "postfault_gap_vs_prefault": f"{postfault_gap:.3f}",
                    "late_recovery_gap_vs_prefault": f"{late_gap:.3f}",
                    "delta_fault_rms_vs_baseline": f"{metrics['fault_rms'] - baseline_metrics['fault_rms']:.3f}",
                    "delta_postfault_rms_vs_baseline": f"{metrics['postfault_rms'] - baseline_metrics['postfault_rms']:.3f}",
                    "observation": observation,
                }
            )

        return rows

    def _build_conclusion_report(self, rows: List[Dict]) -> Dict:
        """构建结论报告"""
        rows_by_name = {row["scenario"]: row for row in rows}

        if "baseline" not in rows_by_name:
            return {"error": "缺少基线工况数据"}

        baseline = rows_by_name["baseline"]

        findings = []

        if "delayed_clearing" in rows_by_name:
            delayed = rows_by_name["delayed_clearing"]
            delayed_fault_delta = float(delayed["delta_fault_rms_vs_baseline"])
            delayed_post_gap = float(delayed["postfault_gap_vs_prefault"])
            baseline_post_gap = float(baseline["postfault_gap_vs_prefault"])

            findings.append(
                {
                    "title": "延迟切除主要恶化故障后恢复，而不是改变故障深度",
                    "supported": abs(delayed_fault_delta) <= 0.1
                    and delayed_post_gap > baseline_post_gap,
                    "evidence": f"delta_fault_rms={delayed_fault_delta:.3f}, post_gap: {baseline_post_gap:.3f} -> {delayed_post_gap:.3f}",
                }
            )

        if "mild_fault" in rows_by_name:
            mild = rows_by_name["mild_fault"]
            baseline_fault_drop = float(baseline["fault_drop_vs_prefault"])
            mild_fault_drop = float(mild["fault_drop_vs_prefault"])
            baseline_post_gap = float(baseline["postfault_gap_vs_prefault"])
            mild_post_gap = float(mild["postfault_gap_vs_prefault"])

            findings.append(
                {
                    "title": "较轻故障显著减小故障跌落，并把恢复缺口压回接近零",
                    "supported": baseline_fault_drop - mild_fault_drop > 100
                    and baseline_post_gap - mild_post_gap > 3,
                    "evidence": f"fault_drop: {baseline_fault_drop:.3f} -> {mild_fault_drop:.3f}, post_gap: {baseline_post_gap:.3f} -> {mild_post_gap:.3f}",
                }
            )

        return {
            "research_question": "在同一故障模型上，延迟切除与降低故障严重度如何影响故障深度和恢复缺口？",
            "findings": findings,
        }

    def _export_summary_csv(self, rows: List[Dict], path: Path):
        """导出CSV汇总"""
        fieldnames = [
            "scenario",
            "description",
            "fault_end_time",
            "fault_chg",
            "point_count",
            "prefault_rms",
            "fault_rms",
            "postfault_rms",
            "late_recovery_rms",
            "fault_drop_vs_prefault",
            "postfault_gap_vs_prefault",
            "late_recovery_gap_vs_prefault",
            "delta_fault_rms_vs_baseline",
            "delta_postfault_rms_vs_baseline",
            "observation",
        ]
        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def _export_waveform_csv(
        self, study_results: List[Dict], path: Path, time_window=None
    ):
        """导出波形对比CSV"""
        if not study_results:
            return

        baseline_trace = study_results[0]["metrics"]["trace"]
        baseline_times = baseline_trace["x"]

        rows = []
        for point_index, time_value in enumerate(baseline_times):
            if time_window is not None:
                start_time, end_time = time_window
                if time_value < start_time or time_value > end_time:
                    continue

            row = {"time": f"{time_value:.6f}"}
            for result in study_results:
                trace = result["metrics"]["trace"]
                row[result["name"]] = f"{trace['y'][point_index]:.6f}"
            rows.append(row)

        fieldnames = ["time"] + [r["name"] for r in study_results]
        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def _generate_report(
        self, study_results: List[Dict], summary_rows: List[Dict], path: Path
    ):
        """生成Markdown研究报告"""
        lines = [
            "# EMT 故障研究分析报告",
            "",
            f"生成时间: {datetime.now().isoformat()}",
            "",
            "## 研究概述",
            "",
            "本研究对比分析三种故障工况对系统电压恢复的影响：",
            "- **基线故障**: 标准故障参数",
            "- **延迟切除**: 延长故障切除时间",
            "- **轻故障**: 降低故障严重程度",
            "",
            "## 仿真结果汇总",
            "",
            "| 工况 | 描述 | fe | chg | 故障前RMS | 故障RMS | 故障后RMS | 恢复缺口 |",
            "|------|------|----|-----|----------|---------|----------|----------|",
        ]

        for row in summary_rows:
            lines.append(
                f"| {row['scenario']} | {row['description']} | "
                f"{row['fault_end_time']} | {row['fault_chg']} | "
                f"{row['prefault_rms']} | {row['fault_rms']} | "
                f"{row['postfault_rms']} | {row['postfault_gap_vs_prefault']} |"
            )

        lines.extend(
            [
                "",
                "## 关键发现",
                "",
            ]
        )

        # 添加结论
        conclusion = self._build_conclusion_report(summary_rows)
        for finding in conclusion.get("findings", []):
            status = "✓ 支持" if finding["supported"] else "✗ 未满足"
            lines.extend(
                [
                    f"### {finding['title']}",
                    "",
                    f"**结论**: {status}",
                    "",
                    f"**证据**: {finding['evidence']}",
                    "",
                ]
            )

        lines.extend(
            [
                "",
                "## 详细指标",
                "",
                "### 相对故障前缺口",
                "",
            ]
        )

        for row in summary_rows:
            lines.extend(
                [
                    f"**{row['scenario']}**:",
                    f"- 故障跌落: {row['fault_drop_vs_prefault']} V",
                    f"- 故障后缺口: {row['postfault_gap_vs_prefault']} V",
                    f"- 恢复缺口: {row['late_recovery_gap_vs_prefault']} V",
                    "",
                ]
            )

        lines.extend(
            [
                "",
                "## 工况定义",
                "",
            ]
        )

        for result in study_results:
            lines.extend(
                [
                    f"### {result['name']}",
                    f"- 描述: {result['description']}",
                    f"- 故障结束时间 (fe): {result['fault_end_time']}",
                    f"- 故障电阻 (chg): {result['fault_chg']}",
                    f"- Job ID: {result['job_id']}",
                    "",
                ]
            )

        path.write_text("\n".join(lines), encoding="utf-8")
