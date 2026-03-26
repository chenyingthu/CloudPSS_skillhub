"""
Fault Clearing Scan Skill

故障清除时间扫描 - 扫描故障切除时间对恢复的影响
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
DEFAULT_WINDOWS = {
    "prefault": (2.42, 2.44),
    "fault": (2.56, 2.58),
    "postfault": (2.92, 2.94),
}


@register
class FaultClearingScanSkill(SkillBase):
    """故障清除时间扫描技能"""

    @property
    def name(self) -> str:
        return "fault_clearing_scan"

    @property
    def description(self) -> str:
        return "故障清除时间扫描 - 扫描fe参数对恢复的影响"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "fault_clearing_scan"},
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
                    "required": ["fe_values"],
                    "properties": {
                        "fs": {"type": "number", "default": 2.5},
                        "fe_values": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "故障结束时间扫描值列表",
                        },
                        "chg": {"type": "number", "default": 0.01},
                    },
                },
                "assessment": {
                    "type": "object",
                    "properties": {
                        "trace_name": {"type": "string", "default": "vac:0"},
                        "study_time": {"type": "number", "default": 2.95},
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"enum": ["json", "csv"], "default": "json"},
                        "path": {"type": "string", "default": "./results/"},
                        "prefix": {"type": "string", "default": "fault_clearing_scan"},
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
                "fe_values": [2.70, 2.75, 2.80, 2.85, 2.90],
                "chg": 0.01,
            },
            "assessment": {
                "trace_name": "vac:0",
                "study_time": 2.95,
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "fault_clearing_scan",
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

            fe_values = scan_config["fe_values"]
            fs = scan_config.get("fs", 2.5)
            chg = scan_config.get("chg", 0.01)
            study_time = assessment_config.get("study_time", 2.95)
            trace_name = assessment_config.get("trace_name", "vac:0")

            log("INFO", f"扫描 {len(fe_values)} 个清除时间点: {fe_values}")

            results = []
            for i, fe in enumerate(fe_values):
                log("INFO", f"[{i+1}/{len(fe_values)}] fe={fe}")
                working_model = Model(deepcopy(base_model.toJSON()))

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
                            "fs": {"source": str(fs), "ɵexp": ""},
                            "fe": {"source": str(fe), "ɵexp": ""},
                            "chg": {"source": str(chg), "ɵexp": ""},
                        },
                    )

                # 运行EMT
                job = working_model.runEMT()
                while True:
                    status = job.status()
                    if status == 1:
                        break
                    if status == 2:
                        raise RuntimeError("EMT仿真失败")
                    time.sleep(3)

                # 提取结果
                result = job.result
                voltage_at_study = self._extract_voltage_at_time(result, trace_name, study_time)

                results.append({
                    "fe": fe,
                    "voltage_at_study": voltage_at_study,
                    "job_id": job.id,
                })
                log("INFO", f"  -> 研究时刻电压: {voltage_at_study:.3f}")

            # 分析趋势
            is_monotonic = all(results[i]["voltage_at_study"] >= results[i+1]["voltage_at_study"]
                              for i in range(len(results)-1))

            # 导出
            output_path = Path(output_config.get("path", "./results/"))
            output_path.mkdir(parents=True, exist_ok=True)
            prefix = output_config.get("prefix", "fault_clearing_scan")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            result_data = {
                "model": base_model.name,
                "study_time": study_time,
                "monotonic_degradation": is_monotonic,
                "results": results,
            }

            # JSON
            json_path = output_path / f"{prefix}_{timestamp}.json"
            with open(json_path, 'w') as f:
                json.dump(result_data, f, indent=2)
            artifacts.append(Artifact(type="json", path=str(json_path), size=json_path.stat().st_size, description="清除时间扫描结果"))

            # CSV
            csv_path = output_path / f"{prefix}_{timestamp}.csv"
            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["fe", "voltage_at_study", "job_id"])
                for r in results:
                    writer.writerow([r["fe"], f"{r['voltage_at_study']:.4f}", r["job_id"]])
            artifacts.append(Artifact(type="csv", path=str(csv_path), size=csv_path.stat().st_size, description="清除时间扫描CSV"))

            # Report
            if output_config.get("generate_report", True):
                report_path = output_path / f"{prefix}_report_{timestamp}.md"
                lines = [
                    "# 故障清除时间扫描报告",
                    "",
                    f"研究时刻: {study_time}s",
                    f"单调恶化: {'是' if is_monotonic else '否'}",
                    "",
                    "| fe (s) | 研究时刻电压 |",
                    "|--------|--------------|",
                ]
                for r in results:
                    lines.append(f"| {r['fe']} | {r['voltage_at_study']:.4f} |")
                lines.append("")
                if is_monotonic:
                    lines.append("**结论**: 清除时间越晚，研究时刻电压越低，恢复越差。")
                report_path.write_text("\n".join(lines), encoding="utf-8")
                artifacts.append(Artifact(type="markdown", path=str(report_path), size=report_path.stat().st_size, description="清除时间扫描报告"))

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

    def _extract_voltage_at_time(self, result, trace_name, study_time):
        for i, _ in enumerate(result.getPlots()):
            channel_names = result.getPlotChannelNames(i)
            if trace_name in channel_names:
                trace = result.getPlotChannelData(i, trace_name)
                for t, v in zip(trace["x"], trace["y"]):
                    if abs(t - study_time) < 0.001:
                        return v
        return 0.0
