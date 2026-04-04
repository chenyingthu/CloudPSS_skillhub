"""
Fault Severity Scan Skill

故障严重度扫描 - 扫描故障电阻对电压跌落的影响
"""

import csv
import json
import logging
import math
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from cloudpss_skills.core import Artifact, LogEntry, SkillBase, SkillResult, SkillStatus, ValidationResult, register

logger = logging.getLogger(__name__)

FAULT_DEFINITION = "model/CloudPSS/_newFaultResistor_3p"


@register
class FaultSeverityScanSkill(SkillBase):
    """故障严重度扫描技能"""

    @property
    def name(self) -> str:
        return "fault_severity_scan"

    @property
    def description(self) -> str:
        return "故障严重度扫描 - 扫描chg参数对故障跌落和恢复的影响"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "fault_severity_scan"},
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
                    "required": ["chg_values"],
                    "properties": {
                        "fs": {"type": "number", "default": 2.5},
                        "fe": {"type": "number", "default": 2.7},
                        "chg_values": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "故障电阻扫描值列表",
                        },
                    },
                },
                "assessment": {
                    "type": "object",
                    "properties": {
                        "trace_name": {"type": "string", "default": "vac:0"},
                        "time_windows": {
                            "type": "object",
                            "properties": {
                                "prefault": {"type": "array", "items": {"type": "number"}, "default": [2.42, 2.44]},
                                "fault": {"type": "array", "items": {"type": "number"}, "default": [2.56, 2.58]},
                                "postfault": {"type": "array", "items": {"type": "number"}, "default": [2.92, 2.94]},
                            },
                        },
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"enum": ["json", "csv"], "default": "json"},
                        "path": {"type": "string", "default": "./results/"},
                        "prefix": {"type": "string", "default": "fault_severity_scan"},
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
                "fs": 2.5,
                "fe": 2.7,
                "chg_values": [0.01, 100.0, 10000.0],
            },
            "assessment": {
                "trace_name": "vac:0",
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "fault_severity_scan",
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
            assessment_config = config.get("assessment", {})
            output_config = config.get("output", {})

            chg_values = scan_config["chg_values"]
            fs = scan_config.get("fs", 2.5)
            fe = scan_config.get("fe", 2.7)
            trace_name = assessment_config.get("trace_name", "vac:0")
            time_windows = assessment_config.get("time_windows", {
                "prefault": (2.42, 2.44),
                "fault": (2.56, 2.58),
                "postfault": (2.92, 2.94),
            })

            log("INFO", f"扫描 {len(chg_values)} 个故障电阻值: {chg_values}")

            results = []
            for i, chg in enumerate(chg_values):
                log("INFO", f"[{i+1}/{len(chg_values)}] chg={chg}")
                working_model = Model(deepcopy(base_model.toJSON()))

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
                            "fs": {"source": str(fs), "ɵexp": ""},
                            "fe": {"source": str(fe), "ɵexp": ""},
                            "chg": {"source": str(chg), "ɵexp": ""},
                        },
                    )

                job = working_model.runEMT()
                while True:
                    status = job.status()
                    if status == 1:
                        break
                    if status == 2:
                        raise RuntimeError("EMT仿真失败")
                    time.sleep(3)

                result = job.result
                metrics = self._extract_metrics(result, trace_name, time_windows)

                results.append({
                    "chg": chg,
                    "prefault_rms": metrics["prefault_rms"],
                    "fault_rms": metrics["fault_rms"],
                    "postfault_rms": metrics["postfault_rms"],
                    "fault_drop": metrics["prefault_rms"] - metrics["fault_rms"],
                    "postfault_gap": metrics["prefault_rms"] - metrics["postfault_rms"],
                    "job_id": job.id,
                })
                log("INFO", f"  -> 故障跌落: {results[-1]['fault_drop']:.3f}, 恢复缺口: {results[-1]['postfault_gap']:.3f}")

            # 排序
            results_sorted = sorted(results, key=lambda r: r["chg"])

            # 分析趋势
            fault_drops = [r["fault_drop"] for r in results_sorted]
            post_gaps = [r["postfault_gap"] for r in results_sorted]
            fault_trend = "decreasing" if all(fault_drops[i] >= fault_drops[i+1] for i in range(len(fault_drops)-1)) else "mixed"
            gap_trend = "decreasing" if all(post_gaps[i] >= post_gaps[i+1] for i in range(len(post_gaps)-1)) else "mixed"

            # 导出
            output_path = Path(output_config.get("path", "./results/"))
            output_path.mkdir(parents=True, exist_ok=True)
            prefix = output_config.get("prefix", "fault_severity_scan")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            result_data = {
                "model": base_model.name,
                "fault_trend": fault_trend,
                "gap_trend": gap_trend,
                "results": results_sorted,
            }

            json_path = output_path / f"{prefix}_{timestamp}.json"
            with open(json_path, 'w') as f:
                json.dump(result_data, f, indent=2)
            artifacts.append(Artifact(type="json", path=str(json_path), size=json_path.stat().st_size, description="严重度扫描结果"))

            csv_path = output_path / f"{prefix}_{timestamp}.csv"
            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["chg", "prefault_rms", "fault_rms", "postfault_rms", "fault_drop", "postfault_gap"])
                for r in results_sorted:
                    writer.writerow([
                        r["chg"], f"{r['prefault_rms']:.4f}", f"{r['fault_rms']:.4f}",
                        f"{r['postfault_rms']:.4f}", f"{r['fault_drop']:.4f}", f"{r['postfault_gap']:.4f}"
                    ])
            artifacts.append(Artifact(type="csv", path=str(csv_path), size=csv_path.stat().st_size, description="严重度扫描CSV"))

            if output_config.get("generate_report", True):
                report_path = output_path / f"{prefix}_report_{timestamp}.md"
                lines = [
                    "# 故障严重度扫描报告",
                    "",
                    f"故障电阻趋势: {fault_trend}",
                    f"恢复缺口趋势: {gap_trend}",
                    "",
                    "| chg | 故障前RMS | 故障RMS | 故障后RMS | 跌落 | 缺口 |",
                    "|-----|-----------|---------|-----------|------|------|",
                ]
                for r in results_sorted:
                    lines.append(f"| {r['chg']} | {r['prefault_rms']:.3f} | {r['fault_rms']:.3f} | "
                               f"{r['postfault_rms']:.3f} | {r['fault_drop']:.3f} | {r['postfault_gap']:.3f} |")
                lines.append("")
                if fault_trend == "decreasing" and gap_trend == "decreasing":
                    lines.append("**结论**: 故障电阻越大（故障越轻），故障跌落越小，恢复越好。")
                report_path.write_text("\n".join(lines), encoding="utf-8")
                artifacts.append(Artifact(type="markdown", path=str(report_path), size=report_path.stat().st_size, description="严重度扫描报告"))

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                start_time=start_time,
                end_time=datetime.now(),
                data=result_data,
                artifacts=artifacts,
                logs=logs,
            )

        except (KeyError, AttributeError, ZeroDivisionError) as e:
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

    def _trace_rms(self, trace, start, end):
        samples = [v for t, v in zip(trace["x"], trace["y"]) if start <= t <= end]
        if not samples:
            return 0.0
        return math.sqrt(sum(v * v for v in samples) / len(samples))

    def _extract_metrics(self, result, trace_name, time_windows):
        for i, _ in enumerate(result.getPlots()):
            channel_names = result.getPlotChannelNames(i)
            if trace_name in channel_names:
                trace = result.getPlotChannelData(i, trace_name)
                return {
                    "prefault_rms": self._trace_rms(trace, *time_windows["prefault"]),
                    "fault_rms": self._trace_rms(trace, *time_windows["fault"]),
                    "postfault_rms": self._trace_rms(trace, *time_windows["postfault"]),
                }
        return {"prefault_rms": 0, "fault_rms": 0, "postfault_rms": 0}
