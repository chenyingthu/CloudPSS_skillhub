"""Voltage Stability Skill v2 - Engine-agnostic voltage stability analysis.

电压稳定性分析 - 通过连续潮流计算PV曲线，识别电压崩溃点
支持负荷增长扫描和关键母线电压监测
"""

from __future__ import annotations

import csv
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from cloudpss_skills_v2.core.skill_result import (
    Artifact,
    LogEntry,
    SkillResult,
    SkillStatus,
)
from cloudpss_skills_v2.powerapi import EngineConfig
from cloudpss_skills_v2.powerskill import (
    Engine,
    PowerFlow,
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


class VoltageStabilityAnalysis:
    """电压稳定性分析技能 - v2 engine-agnostic implementation."""

    name = "voltage_stability"
    description = "电压稳定性分析 - 通过连续潮流计算PV曲线，识别电压崩溃点"

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "voltage_stability", "default": "voltage_stability"},
                "engine": {
                    "type": "string",
                    "enum": ["cloudpss", "pandapower"],
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
                        "rid": {"type": "string", "default": "model/holdme/IEEE39"},
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
                        },
                        "load_target": {
                            "type": "string",
                        },
                        "scale_generation": {
                            "type": "boolean",
                            "default": True,
                        },
                    },
                },
                "monitoring": {
                    "type": "object",
                    "properties": {
                        "buses": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "collapse_threshold": {
                            "type": "number",
                            "default": 0.7,
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

    def get_default_config(self) -> dict[str, Any]:
        return {
            "skill": self.name,
            "engine": "cloudpss",
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "model/holdme/IEEE39", "source": "cloud"},
            "scan": {
                "load_scaling": [1.0, 1.2, 1.4, 1.6, 1.8, 2.0],
                "scale_generation": True,
            },
            "monitoring": {
                "buses": [],
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

    def __init__(self):
        self.logs: list[LogEntry] = []
        self.artifacts: list[Artifact] = []

    def _log(self, level: str, message: str) -> None:
        self.logs.append(LogEntry(timestamp=datetime.now(), level=level, message=message))
        getattr(logger, level.lower(), logger.info)(message)

    def _get_api(self, config: dict[str, Any]) -> PowerFlow:
        engine = config.get("engine", "cloudpss")
        auth = config.get("auth", {})
        engine_config = EngineConfig(
            engine_name=engine,
            base_url=auth.get("base_url", ""),
            extra={"auth": auth},
        )
        return Engine.create_powerflow(engine=engine, config=engine_config)

    def validate(self, config: dict[str, Any]) -> tuple[bool, list[str]]:
        errors = []
        if not config.get("model", {}).get("rid"):
            errors.append("必须提供 model.rid")
        engine = config.get("engine", "cloudpss")
        auth = config.get("auth", {})
        if engine == "cloudpss" and not auth.get("token") and not auth.get("token_file"):
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
            api = self._get_api(config)
            self._log("INFO", f"使用引擎: {api.adapter.engine_name}")

            model_config = config["model"]
            model_rid = model_config["rid"]
            source = model_config.get("source", "cloud")
            model_file = model_config.get("file") or model_config.get("path")
            auth = config.get("auth", {})

            scan_config = config.get("scan", {})
            monitoring_config = config.get("monitoring", {})
            output_config = config.get("output", {})

            load_scaling = scan_config.get("load_scaling", [1.0, 1.2, 1.4, 1.6, 1.8, 2.0])
            load_target = scan_config.get("load_target")
            scale_generation = scan_config.get("scale_generation", True)

            target_buses = monitoring_config.get("buses", [])
            collapse_threshold = monitoring_config.get("collapse_threshold", 0.7)

            self._log("INFO", f"电压稳定性分析: {len(load_scaling)}个负荷水平")
            self._log("INFO", f"负荷增长范围: {min(load_scaling)}x ~ {max(load_scaling)}x")

            if model_file:
                base_result = api.run_power_flow(
                    model_id=model_rid, source=source, auth=auth, model_file=model_file
                )
                if not base_result.is_success:
                    raise RuntimeError(
                        f"基态潮流计算失败: {base_result.errors[0] if base_result.errors else 'unknown'}"
                    )

            handle = api.get_model_handle(model_rid)
            base_loads = handle.get_components_by_type(ComponentType.LOAD)
            base_gens = handle.get_components_by_type(ComponentType.GENERATOR)

            if load_target:
                base_loads = [
                    l
                    for l in base_loads
                    if load_target in (l.name or "") or load_target in (l.key or "")
                ]

            self._log("INFO", f"基线负荷数: {len(base_loads)}, 发电机数: {len(base_gens)}")

            results = []
            converged_cases = []
            collapse_point = None
            max_loadability = None

            for i, scale in enumerate(load_scaling):
                self._log("INFO", f"[{i + 1}/{len(load_scaling)}] 负荷水平={scale}x")

                try:
                    working = handle.clone()

                    self._scale_loads_and_generation(
                        working, base_loads, base_gens, scale, scale_generation
                    )

                    sim_result = api.run_power_flow(
                        model_handle=working, source=source, auth=auth, model_file=model_file
                    )

                    if not sim_result.is_success:
                        fallback_voltages = {}
                        if converged_cases:
                            fallback_voltages = converged_cases[-1].get("voltages", {})
                        results.append(
                            {
                                "scale": scale,
                                "converged": False,
                                "voltages": fallback_voltages,
                            }
                        )
                        continue

                    bus_data = sim_result.data.get("buses", [])
                    voltages = self._extract_bus_voltages(bus_data, target_buses)
                    min_voltage = min(voltages.values()) if voltages else 1.0

                    case_result = {
                        "scale": scale,
                        "converged": True,
                        "voltages": voltages,
                        "min_voltage": min_voltage,
                    }
                    results.append(case_result)
                    converged_cases.append(case_result)

                    self._log("INFO", f"  -> 最小电压: {min_voltage:.4f} pu")

                    if min_voltage < collapse_threshold:
                        if collapse_point is None:
                            collapse_point = scale
                        self._log("WARNING", "  电压低于崩溃阈值!")

                except Exception as e:
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

            if converged_cases:
                max_loadability = converged_cases[-1]["scale"]

            pv_curve_data = self._generate_pv_curve(converged_cases, target_buses)

            result_data = {
                "model_rid": model_rid,
                "collapse_threshold": collapse_threshold,
                "collapse_point": collapse_point,
                "max_loadability": max_loadability,
                "total_cases": len(results),
                "converged_cases": len(converged_cases),
                "monitored_buses": target_buses,
                "results": results,
                "pv_curve": pv_curve_data,
                "timestamp": datetime.now().isoformat(),
            }

            self._save_output(result_data, output_config, target_buses)

            status = SkillStatus.SUCCESS if converged_cases else SkillStatus.FAILED
            error = None if converged_cases else "No voltage stability scan cases converged"
            return SkillResult(
                skill_name=self.name,
                status=status,
                data=result_data,
                artifacts=self.artifacts,
                logs=self.logs,
                error=error,
                metrics={
                    "total_cases": len(results),
                    "converged": len(converged_cases),
                    "collapse_point": collapse_point,
                    "max_loadability": max_loadability,
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
                    "stage": "voltage_stability",
                },
                artifacts=self.artifacts,
                logs=self.logs,
                error=str(e),
                start_time=start_time,
                end_time=datetime.now(),
            )

    def _scale_loads_and_generation(
        self,
        handle: ModelHandle,
        base_loads: list,
        base_gens: list,
        scale: float,
        scale_gen: bool,
    ) -> None:
        total_load_p = 0

        for load_info in base_loads:
            key = load_info.key
            args = load_info.args
            if not args:
                continue

            if "_newExpLoad" in (load_info.definition or ""):
                p_source = args.get("p", {}).get("source", "1")
                q_source = args.get("q", {}).get("source", "0")
                try:
                    base_P = float(p_source)
                    base_Q = float(q_source)
                except (ValueError, TypeError):
                    continue
                new_args = {
                    "p": {"source": str(base_P * scale), "ɵexp": ""},
                    "q": {"source": str(base_Q * scale), "ɵexp": ""},
                }
                if handle.update_component_args(key, new_args):
                    total_load_p += base_P * scale
            else:
                p_value = self._component_arg_value(args, "pf_P", "p_mw")
                q_value = self._component_arg_value(args, "pf_Q", "q_mvar")
                if p_value is None:
                    continue
                base_P = p_value
                base_Q = q_value or 0.0
                new_args = {
                    "pf_P": {"source": str(base_P * scale), "ɵexp": ""},
                    "pf_Q": {"source": str(base_Q * scale), "ɵexp": ""},
                    "p_mw": base_P * scale,
                    "q_mvar": base_Q * scale,
                }
                if handle.update_component_args(key, new_args):
                    total_load_p += base_P * scale

        if scale_gen and base_gens and scale > 1.0 and total_load_p > 0:
            for gen_info in base_gens:
                key = gen_info.key
                args = gen_info.args
                if not args:
                    continue

                definition = gen_info.definition or ""
                if "_newGenerator" in definition or "SyncGenerator" in definition:
                    base_P = self._component_arg_value(args, "pf_P", "p_mw")
                    if base_P is None:
                        continue
                    new_args = {
                        "pf_P": {"source": str(base_P * scale), "ɵexp": ""},
                        "p_mw": base_P * scale,
                    }
                    handle.update_component_args(key, new_args)

    def _component_arg_value(self, args: dict[str, Any], *keys: str) -> float | None:
        for key in keys:
            if key not in args:
                continue
            value = args[key]
            if isinstance(value, dict):
                value = value.get("source")
            try:
                return float(value)
            except (TypeError, ValueError):
                continue
        return None

    def _extract_bus_voltages(
        self, bus_data: list[dict], target_buses: list[str]
    ) -> dict[str, float]:
        voltages: dict[str, float] = {}
        if not target_buses:
            return voltages

        for bus in bus_data:
            bus_name = bus.get("name", "")
            vm = _as_float(bus.get("voltage_pu"), 1.0)

            for target_bus in target_buses:
                if self._matches_bus_identifier(target_bus, bus_name):
                    voltages[target_bus] = vm

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

    def _generate_pv_curve(self, converged_cases: list, target_buses: list[str]) -> list[dict]:
        pv_data = []
        for case in converged_cases:
            scale = case["scale"]
            for bus, voltage in case.get("voltages", {}).items():
                pv_data.append({"bus": bus, "scale": scale, "voltage": voltage})
        return pv_data

    def _save_output(
        self,
        result_data: dict,
        output_config: dict,
        target_buses: list[str],
    ) -> None:
        output_format = output_config.get("format", "json")
        output_path = Path(output_config.get("path", "./results/"))
        prefix = output_config.get("prefix", "voltage_stability")

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
                    description="电压稳定性分析结果",
                )
            )

        csv_filename = f"{prefix}{ts_suffix}.csv"
        csv_path = output_path / csv_filename
        self._export_data_csv(result_data, csv_path, target_buses)
        self.artifacts.append(
            Artifact(
                name=csv_filename,
                path=str(csv_path),
                type="csv",
                size_bytes=csv_path.stat().st_size,
                description="电压稳定性CSV",
            )
        )

        if output_config.get("export_pv_curve", True) and result_data.get("pv_curve"):
            pv_filename = f"{prefix}_pv_curve{ts_suffix}.csv"
            pv_path = output_path / pv_filename
            with open(pv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["bus", "load_scale", "voltage_pu"])
                for p in result_data["pv_curve"]:
                    writer.writerow([p["bus"], p["scale"], p["voltage"]])
            self.artifacts.append(
                Artifact(
                    name=pv_filename,
                    path=str(pv_path),
                    type="csv",
                    size_bytes=pv_path.stat().st_size,
                    description="PV曲线数据",
                )
            )

        if output_config.get("generate_report", True):
            report_filename = f"{prefix}_report{ts_suffix}.md"
            report_path = output_path / report_filename
            self._generate_report(result_data, report_path, target_buses)
            self.artifacts.append(
                Artifact(
                    name=report_filename,
                    path=str(report_path),
                    type="markdown",
                    size_bytes=report_path.stat().st_size,
                    description="电压稳定性分析报告",
                )
            )

    def _export_data_csv(
        self,
        result_data: dict,
        path: Path,
        target_buses: list[str],
    ) -> None:
        headers = ["load_scale", "converged", "min_voltage"] + [f"V_{bus}" for bus in target_buses]
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for r in result_data.get("results", []):
                row = [r["scale"], r.get("converged", False), r.get("min_voltage", 0)]
                for bus in target_buses:
                    row.append(r.get("voltages", {}).get(bus, 0))
                writer.writerow(row)

    def _generate_report(
        self,
        data: dict,
        path: Path,
        target_buses: list[str],
    ) -> None:
        lines = [
            "# 电压稳定性分析报告",
            "",
            f"**模型**: {data.get('model_rid', 'Unknown')}",
            f"**电压崩溃阈值**: {data.get('collapse_threshold', 0.7)} pu",
            f"**总计算工况**: {data.get('total_cases', 0)}",
            f"**收敛工况**: {data.get('converged_cases', 0)}",
            "",
        ]

        if data.get("collapse_point"):
            lines.extend(
                [
                    "## 电压稳定性评估",
                    "",
                    f"**电压崩溃点**: 约在负荷水平 **{data['collapse_point']}x** 处",
                    f"**最大负荷能力**: {data.get('max_loadability', 'N/A')}x",
                    "",
                ]
            )
        else:
            lines.extend(
                [
                    "## 电压稳定性评估",
                    "",
                    f"在给定负荷范围内未发生电压崩溃",
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
                f"| {r['scale']:.2f} | {conv_str} | {min_v} | " + " | ".join(bus_voltages) + " |"
            )

        lines.extend(["", "## 结论", ""])

        if data.get("collapse_point"):
            lines.append(
                f"系统在负荷增长至 {data['collapse_point']}x 时接近电压崩溃，"
                f"建议加强电压支撑措施。"
            )
        else:
            lines.append(
                f"系统在测试范围内保持电压稳定，"
                f"最大负荷能力约为 {data.get('max_loadability', 'N/A')}x。"
            )

        path.write_text("\n".join(lines), encoding="utf-8")


__all__ = ["VoltageStabilityAnalysis"]
