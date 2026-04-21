"""Contingency Analysis Skill v2 - Engine-agnostic N-K contingency analysis.

预想事故分析 - 系统性评估电网在多种故障工况下的安全裕度
支持N-1、N-2、N-K故障，故障排序，薄弱环节识别
"""

from __future__ import annotations

import csv
import json
import logging
from datetime import datetime
from itertools import combinations
from pathlib import Path
from typing import Any

from cloudpss_skills_v2.core.skill_result import (
    Artifact,
    LogEntry,
    SkillResult,
    SkillStatus,
)
from cloudpss_skills_v2.powerskill import (
    APIFactory,
    PowerFlowAPI,
    ModelHandle,
    ComponentType,
)

logger = logging.getLogger(__name__)


def _as_float(value, default=0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


class ContingencyAnalysisSkill:
    """预想事故分析技能 - v2 engine-agnostic implementation."""

    name = "contingency_analysis"
    description = "预想事故分析 - 评估N-K故障下的系统安全裕度，识别薄弱环节"

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "contingency_analysis"},
                "engine": {
                    "type": "string",
                    "enum": ["cloudpss", "pandapower", "algolib"],
                    "default": "cloudpss",
                },
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
                "contingency": {
                    "type": "object",
                    "properties": {
                        "level": {
                            "enum": ["N-1", "N-2", "N-K"],
                            "default": "N-1",
                        },
                        "k": {"type": "integer", "default": 1},
                        "components": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "component_types": {
                            "type": "array",
                            "items": {
                                "enum": [
                                    "branch",
                                    "generator",
                                    "load",
                                    "transformer",
                                ]
                            },
                            "default": ["branch"],
                        },
                        "max_combinations": {
                            "type": "integer",
                            "default": 100,
                        },
                    },
                },
                "analysis": {
                    "type": "object",
                    "properties": {
                        "check_voltage": {"type": "boolean", "default": True},
                        "check_thermal": {"type": "boolean", "default": True},
                        "voltage_limit": {
                            "type": "object",
                            "properties": {
                                "min": {"type": "number", "default": 0.95},
                                "max": {"type": "number", "default": 1.05},
                            },
                        },
                        "thermal_limit": {"type": "number", "default": 1.0},
                        "severity_threshold": {"type": "number", "default": 0.8},
                    },
                },
                "ranking": {
                    "type": "object",
                    "properties": {
                        "method": {
                            "enum": ["severity", "overload", "violation_count"],
                            "default": "severity",
                        },
                        "top_n": {"type": "integer", "default": 10},
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"enum": ["json", "csv"], "default": "json"},
                        "path": {"type": "string", "default": "./results/"},
                        "prefix": {"type": "string", "default": "contingency"},
                        "generate_report": {"type": "boolean", "default": True},
                    },
                },
            },
        }

    def get_default_config(self) -> dict[str, Any]:
        return {
            "skill": self.name,
            "engine": "cloudpss",
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "model/holdme/IEEE39", "source": "cloud"},
            "contingency": {
                "level": "N-1",
                "k": 1,
                "components": [],
                "component_types": ["branch"],
                "max_combinations": 100,
            },
            "analysis": {
                "check_voltage": True,
                "check_thermal": True,
                "voltage_limit": {"min": 0.95, "max": 1.05},
                "thermal_limit": 1.0,
                "severity_threshold": 0.8,
            },
            "ranking": {"method": "severity", "top_n": 10},
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "contingency",
                "generate_report": True,
            },
        }

    def __init__(self):
        self.logs: list[LogEntry] = []
        self.artifacts: list[Artifact] = []

    def _log(self, level: str, message: str) -> None:
        self.logs.append(
            LogEntry(timestamp=datetime.now(), level=level, message=message)
        )
        getattr(logger, level.lower(), logger.info)(message)

    def validate(self, config: dict[str, Any]) -> tuple[bool, list[str]]:
        errors = []
        if not config.get("model", {}).get("rid"):
            errors.append("必须提供 model.rid")
        auth = config.get("auth", {})
        if not auth.get("token") and not auth.get("token_file"):
            errors.append("必须提供 auth.token 或 auth.token_file")
        return len(errors) == 0, errors

    def run(self, config: dict[str, Any]) -> SkillResult:
        start_time = datetime.now()
        self.logs = []
        self.artifacts = []

        valid, errors = self.validate(config)
        if not valid:
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error="; ".join(errors),
                logs=self.logs,
                start_time=start_time,
                end_time=datetime.now(),
            )

        try:
            engine = config.get("engine", "cloudpss")
            api = APIFactory.create_powerflow_api(engine=engine)
            self._log("INFO", f"使用引擎: {api.adapter.engine_name}")

            model_config = config["model"]
            model_rid = model_config["rid"]
            source = model_config.get("source", "cloud")
            auth = config.get("auth", {})

            contingency_config = config.get("contingency", {})
            analysis_config = config.get("analysis", {})
            ranking_config = config.get("ranking", {})
            output_config = config.get("output", {})

            level = contingency_config.get("level", "N-1")
            k = contingency_config.get("k", 1)
            component_types = contingency_config.get("component_types", ["branch"])
            max_combinations = contingency_config.get("max_combinations", 100)

            voltage_limit = analysis_config.get(
                "voltage_limit", {"min": 0.95, "max": 1.05}
            )
            thermal_limit = analysis_config.get("thermal_limit", 1.0)
            severity_threshold = analysis_config.get("severity_threshold", 0.8)
            top_n = ranking_config.get("top_n", 10)

            self._log("INFO", f"预想事故分析: {level}")
            self._log("INFO", f"故障元件类型: {', '.join(component_types)}")

            self._log("INFO", "计算基态潮流...")
            base_result = api.run_power_flow(
                model_id=model_rid, source=source, auth=auth
            )
            if not base_result.is_success:
                raise RuntimeError(
                    f"基态潮流计算失败: {base_result.errors[0] if base_result.errors else 'unknown'}"
                )

            base_buses = base_result.data.get("buses", [])
            base_branches = base_result.data.get("branches", [])
            self._log(
                "INFO",
                f"基态: {len(base_buses)} 节点, {len(base_branches)} 支路",
            )

            handle = api.get_model_handle(model_rid)
            self._log("INFO", "生成故障组合...")
            contingencies = self._generate_contingencies(
                handle,
                component_types,
                level,
                k,
                contingency_config.get("components", []),
                max_combinations,
            )
            self._log("INFO", f"共 {len(contingencies)} 个故障场景")

            if not contingencies:
                raise ValueError("未生成有效的故障场景")

            self._log("INFO", "开始故障评估...")
            results = []
            passed = 0
            failed = 0

            for i, contingency in enumerate(contingencies, 1):
                try:
                    self._log(
                        "INFO", f"[{i}/{len(contingencies)}] {contingency['name']}"
                    )
                    result = self._evaluate_contingency(
                        handle,
                        contingency,
                        analysis_config,
                        voltage_limit,
                        thermal_limit,
                        api,
                        source,
                        auth,
                    )
                    results.append(result)
                    if result["status"] == "PASS":
                        passed += 1
                    else:
                        failed += 1
                except (KeyError, AttributeError) as e:
                    self._log("WARNING", f"故障评估失败 {contingency['name']}: {e}")
                    results.append(
                        {
                            "name": contingency["name"],
                            "components": contingency["components"],
                            "status": "ERROR",
                            "error": str(e),
                        }
                    )

            self._log("INFO", "计算严重度并排序...")
            for result in results:
                if result.get("status") not in ["ERROR"]:
                    result["severity"] = self._calculate_severity(
                        result, voltage_limit, thermal_limit
                    )

            valid_results = [r for r in results if "severity" in r]
            valid_results.sort(key=lambda x: x["severity"], reverse=True)

            summary = {
                "total_cases": len(contingencies),
                "passed": passed,
                "failed": failed,
                "errors": len(contingencies) - passed - failed,
                "pass_rate": round(passed / len(contingencies) * 100, 2)
                if contingencies
                else 0,
                "severe_cases": len(
                    [
                        r
                        for r in valid_results
                        if r.get("severity", 0) >= severity_threshold
                    ]
                ),
            }

            weak_points = self._identify_weak_points(valid_results, top_n)

            self._log(
                "INFO",
                f"通过: {passed}/{len(contingencies)} ({summary['pass_rate']}%)",
            )
            self._log("INFO", f"严重故障: {summary['severe_cases']} 个")

            result_data = {
                "model_rid": model_rid,
                "contingency_level": level,
                "summary": summary,
                "weak_points": weak_points,
                "top_severe_cases": valid_results[:top_n],
                "all_results": results,
                "base_case": {
                    "bus_count": len(base_buses),
                    "branch_count": len(base_branches),
                },
                "timestamp": datetime.now().isoformat(),
            }

            self._save_output(result_data, output_config, voltage_limit, thermal_limit)

            has_failures = failed > 0 or summary.get("errors", 0) > 0
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS if not has_failures else SkillStatus.FAILED,
                data=result_data,
                artifacts=self.artifacts,
                logs=self.logs,
                metrics={
                    "total_cases": len(contingencies),
                    "passed": passed,
                    "failed": failed,
                    "severe_cases": summary["severe_cases"],
                },
                start_time=start_time,
                end_time=datetime.now(),
            )

        except Exception as e:
            self._log("ERROR", f"执行失败: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                data={
                    "success": False,
                    "error": str(e),
                    "stage": "contingency_analysis",
                },
                artifacts=self.artifacts,
                logs=self.logs,
                error=str(e),
                start_time=start_time,
                end_time=datetime.now(),
            )

    def _generate_contingencies(
        self,
        handle: ModelHandle,
        component_types: list[str],
        level: str,
        k: int,
        specified_components: list[str],
        max_combinations: int,
    ) -> list[dict]:
        if level == "N-1":
            k = 1
        elif level == "N-2":
            k = 2

        available = self._discover_components(
            handle, component_types, specified_components
        )
        if not available:
            return []

        k = min(k, len(available))
        contingencies = []
        for combo in combinations(available, k):
            keys = [c["key"] for c in combo]
            names = [c["name"] for c in combo]
            contingencies.append({"name": " + ".join(names), "components": keys})
            if len(contingencies) >= max_combinations:
                break

        return contingencies

    def _discover_components(
        self,
        handle: ModelHandle,
        component_types: list[str],
        specified_components: list[str],
    ) -> list[dict]:
        type_map = {
            "branch": ComponentType.BRANCH,
            "transformer": ComponentType.TRANSFORMER,
            "generator": ComponentType.GENERATOR,
            "load": ComponentType.LOAD,
        }

        available = []
        for comp_type_str in component_types:
            comp_type = type_map.get(comp_type_str, ComponentType.OTHER)
            comps = handle.get_components_by_type(comp_type)
            for c in comps:
                if (
                    not specified_components
                    or c.name in specified_components
                    or c.key in specified_components
                ):
                    available.append(
                        {"key": c.key, "name": c.name, "type": comp_type_str}
                    )

        return available

    def _evaluate_contingency(
        self,
        handle: ModelHandle,
        contingency: dict,
        analysis_config: dict,
        voltage_limit: dict,
        thermal_limit: float,
        api: PowerFlowAPI,
        source: str,
        auth: dict,
    ) -> dict:
        result = {
            "name": contingency["name"],
            "components": contingency["components"],
            "status": "PASS",
            "violations": [],
        }

        check_voltage = analysis_config.get("check_voltage", True)
        check_thermal = analysis_config.get("check_thermal", True)

        try:
            working = handle.clone()

            for comp_key in contingency["components"]:
                working.remove_component(comp_key)

            sim_result = api.run_power_flow(
                model_handle=working, source=source, auth=auth
            )

            if not sim_result.is_success:
                result["status"] = "FAIL"
                result["violations"].append(
                    {"type": "CONVERGENCE", "description": "潮流计算不收敛"}
                )
                return result

            bus_data = sim_result.data.get("buses", [])
            branch_data = sim_result.data.get("branches", [])

            min_voltage = float("inf")
            max_voltage = float("-inf")

            if check_voltage:
                for bus in bus_data:
                    vm = _as_float(bus.get("voltage_pu"), 1.0)
                    bus_name = bus.get("name", "Unknown")
                    min_voltage = min(min_voltage, vm)
                    max_voltage = max(max_voltage, vm)

                    if vm < voltage_limit["min"]:
                        result["violations"].append(
                            {
                                "type": "VOLTAGE",
                                "details": {
                                    "bus": bus_name,
                                    "voltage": round(vm, 4),
                                    "limit": f"<{voltage_limit['min']}",
                                },
                            }
                        )
                    elif vm > voltage_limit["max"]:
                        result["violations"].append(
                            {
                                "type": "VOLTAGE",
                                "details": {
                                    "bus": bus_name,
                                    "voltage": round(vm, 4),
                                    "limit": f">{voltage_limit['max']}",
                                },
                            }
                        )

                result["min_voltage"] = (
                    round(min_voltage, 4) if min_voltage != float("inf") else 1.0
                )
                result["max_voltage"] = (
                    round(max_voltage, 4) if max_voltage != float("-inf") else 1.0
                )

            if check_voltage and any(
                v.get("type") == "VOLTAGE" for v in result["violations"]
            ):
                result["status"] = "VIOLATION"

            if check_thermal:
                for branch in branch_data:
                    branch_name = branch.get("name", "unknown")
                    loading_val = _as_float(branch.get("loading_pct"), 0)
                    loading = (
                        loading_val / 100.0
                        if loading_val > 0
                        else max(
                            abs(_as_float(branch.get("p_from_mw"))),
                            abs(_as_float(branch.get("p_to_mw"))),
                        )
                    )

                    if loading > thermal_limit:
                        result["violations"].append(
                            {
                                "type": "THERMAL",
                                "details": {
                                    "branch": branch_name,
                                    "loading": round(loading * 100, 2),
                                    "limit": f"{thermal_limit * 100}%",
                                },
                            }
                        )
                        break

                if any(v.get("type") == "THERMAL" for v in result["violations"]):
                    result["status"] = "VIOLATION"

        except Exception as e:
            result["status"] = "ERROR"
            result["error"] = str(e)

        return result

    def _calculate_severity(
        self, result: dict, voltage_limit: dict, thermal_limit: float
    ) -> float:
        if result.get("status") == "FAIL":
            return 1.0

        severity = 0.0
        min_v = result.get("min_voltage", 1.0)
        max_v = result.get("max_voltage", 1.0)

        if min_v < voltage_limit["min"]:
            severity = max(
                severity, (voltage_limit["min"] - min_v) / voltage_limit["min"]
            )
        if max_v > voltage_limit["max"]:
            severity = max(
                severity,
                (max_v - voltage_limit["max"]) / (1.1 - voltage_limit["max"]),
            )

        for v in result.get("violations", []):
            if v.get("type") == "THERMAL":
                loading = v.get("details", {}).get("loading", 0) / 100.0
                if loading > thermal_limit:
                    severity = max(severity, (loading - thermal_limit) / thermal_limit)

        return round(min(severity, 1.0), 4)

    def _identify_weak_points(self, results: list[dict], top_n: int) -> list[dict]:
        component_count: dict[str, int] = {}
        for result in results[:top_n]:
            for comp in result.get("components", []):
                component_count[comp] = component_count.get(comp, 0) + 1

        return [
            {"component": comp, "critical_cases": count}
            for comp, count in sorted(
                component_count.items(), key=lambda x: x[1], reverse=True
            )
        ][:top_n]

    def _save_output(
        self,
        result_data: dict,
        output_config: dict,
        voltage_limit: dict,
        thermal_limit: float,
    ) -> None:
        output_format = output_config.get("format", "json")
        output_path = Path(output_config.get("path", "./results/"))
        prefix = output_config.get("prefix", "contingency")

        output_path.mkdir(parents=True, exist_ok=True)

        ts_suffix = f"_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        if output_format == "json":
            filename = f"{prefix}{ts_suffix}.json"
            filepath = output_path / filename
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(result_data, f, indent=2, ensure_ascii=False, default=str)
            self.artifacts.append(
                Artifact(
                    name=filename,
                    path=str(filepath),
                    type="json",
                    size_bytes=filepath.stat().st_size,
                    description="预想事故分析结果",
                )
            )

        csv_path = output_path / f"{prefix}{ts_suffix}.csv"
        self._export_csv(result_data.get("top_severe_cases", []), csv_path)
        self.artifacts.append(
            Artifact(
                name=f"{prefix}{ts_suffix}.csv",
                path=str(csv_path),
                type="csv",
                size_bytes=csv_path.stat().st_size,
                description="故障案例汇总",
            )
        )

        if output_config.get("generate_report", True):
            report_path = output_path / f"{prefix}_report{ts_suffix}.md"
            self._generate_report(
                result_data, report_path, voltage_limit, thermal_limit
            )
            self.artifacts.append(
                Artifact(
                    name=f"{prefix}_report{ts_suffix}.md",
                    path=str(report_path),
                    type="markdown",
                    size_bytes=report_path.stat().st_size,
                    description="预想事故分析报告",
                )
            )

    def _export_csv(self, results: list[dict], path: Path) -> None:
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "rank",
                    "contingency",
                    "status",
                    "severity",
                    "min_voltage_pu",
                    "max_voltage_pu",
                    "violation_count",
                ]
            )
            for i, result in enumerate(results, 1):
                writer.writerow(
                    [
                        i,
                        result.get("name", ""),
                        result.get("status", ""),
                        result.get("severity", 0),
                        result.get("min_voltage", ""),
                        result.get("max_voltage", ""),
                        len(result.get("violations", [])),
                    ]
                )

    def _generate_report(
        self,
        data: dict,
        path: Path,
        voltage_limit: dict,
        thermal_limit: float,
    ) -> None:
        summary = data.get("summary", {})
        weak_points = data.get("weak_points", [])
        top_cases = data.get("top_severe_cases", [])

        lines = [
            "# 预想事故分析报告",
            "",
            f"**模型**: {data.get('model_rid', 'Unknown')}",
            f"**故障级别**: {data.get('contingency_level', 'N-1')}",
            f"**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## 执行摘要",
            "",
            f"- **总故障场景**: {summary.get('total_cases', 0)}",
            f"- **通过**: {summary.get('passed', 0)} ({summary.get('pass_rate', 0)}%)",
            f"- **失败/越限**: {summary.get('failed', 0)}",
            f"- **严重故障**: {summary.get('severe_cases', 0)}",
            "",
            "### 安全裕度评估",
            "",
        ]

        pass_rate = summary.get("pass_rate", 0)
        if pass_rate >= 95:
            lines.append("**系统N-1安全裕度充足**")
        elif pass_rate >= 80:
            lines.append("**系统N-1安全裕度一般，存在局部风险**")
        else:
            lines.append("**系统N-1安全裕度不足，需加强网架结构**")

        lines.extend(
            [
                "",
                "## 评判标准",
                "",
                f"- **电压限值**: {voltage_limit['min']:.3f} - {voltage_limit['max']:.3f} pu",
                f"- **热稳定限值**: {thermal_limit * 100:.1f}%",
                "",
                "## 系统薄弱环节",
                "",
                "| 排名 | 元件 | 关键故障次数 |",
                "|------|------|--------------|",
            ]
        )

        for i, wp in enumerate(weak_points, 1):
            lines.append(
                f"| {i} | {wp.get('component', 'N/A')} | {wp.get('critical_cases', 0)} |"
            )

        lines.extend(
            [
                "",
                "## 最严重故障场景 (Top 10)",
                "",
                "| 排名 | 故障场景 | 严重度 | 状态 | 最低电压 |",
                "|------|----------|--------|------|----------|",
            ]
        )

        for i, case in enumerate(top_cases[:10], 1):
            lines.append(
                f"| {i} | {case.get('name', 'N/A')} | "
                f"{case.get('severity', 0):.4f} | {case.get('status', 'N/A')} | "
                f"{case.get('min_voltage', 'N/A')} |"
            )

        lines.extend(
            [
                "",
                "## 建议措施",
                "",
            ]
        )

        if summary.get("severe_cases", 0) > 0:
            lines.append("1. **加强薄弱环节**: 对排名前列的元件进行加固或冗余设计")
            lines.append("2. **电压支撑**: 在电压薄弱节点配置无功补偿装置")
            lines.append("3. **负载均衡**: 优化运行方式，避免线路过载")
        elif pass_rate == 100.0:
            lines.append("当前系统满足N-1安全准则，无需额外措施")

        path.write_text("\n".join(lines), encoding="utf-8")


__all__ = ["ContingencyAnalysisSkill"]
