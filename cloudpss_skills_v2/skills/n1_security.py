"""N-1 Security Skill v2 - Engine-agnostic N-1 security analysis.

N-1安全校核 - 逐一断开每条支路，检查系统是否仍能正常运行。
Uses the PowerSkill PowerFlowAPI to run power flow after each contingency.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from cloudpss_skills_v2.core.skill_result import (
    Artifact,
    LogEntry,
    SkillResult,
    SkillStatus,
)
from cloudpss_skills_v2.powerskill import APIFactory, PowerFlowAPI
from cloudpss_skills_v2.powerapi.adapters.cloudpss._component_utils import (
    remove_component_safe,
)

logger = logging.getLogger(__name__)


def _as_float(value, default=0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


class N1SecuritySkill:
    """N-1安全校核技能 - v2 engine-agnostic implementation."""

    name = "n1_security"
    description = "N-1安全校核 - 逐一停运支路评估系统安全性"

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "n1_security"},
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
                "analysis": {
                    "type": "object",
                    "properties": {
                        "branches": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "check_voltage": {"type": "boolean", "default": True},
                        "check_thermal": {"type": "boolean", "default": True},
                        "voltage_threshold": {
                            "type": "number",
                            "default": 0.05,
                        },
                        "thermal_threshold": {
                            "type": "number",
                            "default": 1.0,
                        },
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"enum": ["json", "yaml"], "default": "json"},
                        "path": {"type": "string", "default": "./results/"},
                        "prefix": {"type": "string", "default": "n1_security"},
                        "timestamp": {"type": "boolean", "default": True},
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
            "analysis": {
                "branches": [],
                "check_voltage": True,
                "check_thermal": True,
                "voltage_threshold": 0.05,
                "thermal_threshold": 1.0,
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "n1_security",
                "timestamp": True,
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

            self._log("INFO", f"模型: {model_rid}")

            # Run base power flow to discover branches
            base_kwargs = {"source": source, "auth": auth}
            base_result = api.run_power_flow(
                model_id=model_rid,
                **base_kwargs,
            )

            if not base_result.is_success:
                raise RuntimeError(
                    f"基础潮流计算失败: {base_result.errors[0] if base_result.errors else 'unknown'}"
                )

            base_branches = base_result.data.get("branches", [])
            branch_names = [
                b.get("name", f"branch_{i}") for i, b in enumerate(base_branches)
            ]

            self._log("INFO", f"发现 {len(branch_names)} 条支路")

            # Get CloudPSS model object for component manipulation
            model = self._get_model_object(api, model_rid, source, auth)
            if model is None:
                raise RuntimeError("无法获取模型对象，N-1校核需要修改模型拓扑")

            components = model.getAllComponents() if model else {}
            branch_types = [
                "model/CloudPSS/line",
                "model/CloudPSS/3pline",
                "model/CloudPSS/transformer",
                "model/CloudPSS/3ptransformer",
                "model/CloudPSS/TransmissionLine",
                "model/CloudPSS/_newTransformer_3p2w",
            ]

            branches = []
            for comp_id, comp in components.items():
                definition = getattr(comp, "definition", "")
                if any(bt in definition for bt in branch_types):
                    branches.append(
                        {
                            "id": comp_id,
                            "name": getattr(comp, "name", comp_id),
                            "type": definition.split("/")[-1],
                        }
                    )

            analysis_config = config.get("analysis", {})
            target_branches = analysis_config.get("branches", [])
            if target_branches:
                branches = [
                    b
                    for b in branches
                    if b["name"] in target_branches or b["id"] in target_branches
                ]
                self._log("INFO", f"将检查 {len(branches)} 条指定支路")

            results = []
            passed = 0
            failed = 0
            violations_found = []

            voltage_threshold = analysis_config.get("voltage_threshold", 0.05)
            thermal_threshold = analysis_config.get("thermal_threshold", 1.0)

            for i, branch in enumerate(branches):
                self._log(
                    "INFO", f"[{i + 1}/{len(branches)}] 停运支路: {branch['name']}"
                )

                # Reload fresh model for each contingency
                working_model = self._get_model_object(api, model_rid, source, auth)
                if working_model is None:
                    self._log("WARNING", "  -> 无法重新加载模型")
                    continue

                if not remove_component_safe(working_model, branch["id"]):
                    self._log("WARNING", "  -> 移除支路失败")
                    continue

                # Run power flow on modified model
                try:
                    from cloudpss_skills_v2.powerapi.adapters.cloudpss._component_utils import (
                        get_components_by_definition,
                    )

                    kwargs = {"source": source, "auth": auth}
                    from cloudpss import Model

                    model_fetch_kwargs = {}
                    base_url = auth.get("base_url") or auth.get("baseUrl")
                    if base_url:
                        model_fetch_kwargs["baseUrl"] = base_url

                    job = working_model.runPowerFlow(**model_fetch_kwargs)
                    max_wait = config.get("timeout", 120)
                    waited = 0
                    poll_interval = 2
                    sdk_status = 0

                    while waited < max_wait:
                        sdk_status = job.status()
                        if sdk_status == 1:
                            break
                        if sdk_status == 2:
                            break
                        import time

                        time.sleep(poll_interval)
                        waited += poll_interval

                    case_violations = []

                    if sdk_status == 1:
                        pf_result = job.result
                        if pf_result is not None:
                            if analysis_config.get("check_voltage", True):
                                v_violations = (
                                    self._check_voltage_violations_from_result(
                                        pf_result, voltage_threshold
                                    )
                                )
                                case_violations.extend(v_violations)

                            if analysis_config.get("check_thermal", True):
                                t_violations = (
                                    self._check_thermal_violations_from_result(
                                        pf_result, thermal_threshold
                                    )
                                )
                                case_violations.extend(t_violations)

                        if case_violations:
                            result = {
                                "branch_id": branch["id"],
                                "branch_name": branch["name"],
                                "status": "failed",
                                "converged": True,
                                "violations": case_violations,
                                "violation_summary": self._summarize_violations(
                                    case_violations
                                ),
                            }
                            failed += 1
                            violations_found.extend(case_violations)
                            self._log("WARNING", "  -> 发现电压/热稳定违规")
                        else:
                            result = {
                                "branch_id": branch["id"],
                                "branch_name": branch["name"],
                                "status": "passed",
                                "converged": True,
                                "violations": [],
                                "violation_summary": None,
                            }
                            passed += 1
                            self._log("INFO", "  -> N-1通过")
                    else:
                        result = {
                            "branch_id": branch["id"],
                            "branch_name": branch["name"],
                            "status": "failed",
                            "converged": False,
                            "violations": [
                                {"type": "convergence", "message": "潮流不收敛"}
                            ],
                            "violation_summary": "潮流不收敛",
                        }
                        failed += 1
                        violations_found.append(
                            {"type": "convergence", "branch": branch["name"]}
                        )
                        self._log("ERROR", "  -> N-1失败: 潮流不收敛")

                    results.append(result)

                except Exception as e:
                    result = {
                        "branch_id": branch["id"],
                        "branch_name": branch["name"],
                        "status": "failed",
                        "converged": False,
                        "violations": [{"type": "error", "message": str(e)}],
                        "violation_summary": str(e),
                    }
                    failed += 1
                    results.append(result)
                    self._log("ERROR", f"  -> 异常: {e}")

            pass_rate = passed / len(branches) * 100 if branches else 0
            self._log("INFO", f"N-1校核完成: 通过 {passed}, 失败 {failed}")
            self._log("INFO", f"通过率: {pass_rate:.1f}%")

            result_data = {
                "model_rid": model_rid,
                "timestamp": datetime.now().isoformat(),
                "summary": {
                    "total_branches": len(branches),
                    "passed": passed,
                    "failed": failed,
                    "pass_rate": passed / len(branches) if branches else 0,
                },
                "results": results,
                "failed_branches": [r for r in results if r["status"] != "passed"],
                "all_violations": violations_found,
                "voltage_threshold": voltage_threshold,
                "thermal_threshold": thermal_threshold,
            }

            output_config = config.get("output", {})
            self._save_output(result_data, output_config)

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS if failed == 0 else SkillStatus.FAILED,
                data=result_data,
                artifacts=self.artifacts,
                logs=self.logs,
                metrics={
                    "total_branches": len(branches),
                    "passed": passed,
                    "failed": failed,
                },
                start_time=start_time,
                end_time=datetime.now(),
            )

        except Exception as e:
            self._log("ERROR", f"执行失败: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                data={"success": False, "error": str(e), "stage": "n1_security"},
                artifacts=self.artifacts,
                logs=self.logs,
                error=str(e),
                start_time=start_time,
                end_time=datetime.now(),
            )

    def _get_model_object(
        self, api: PowerFlowAPI, model_rid: str, source: str, auth: dict
    ) -> Any:
        """Get the CloudPSS Model object for topology modification."""
        try:
            from cloudpss import Model

            kwargs = {}
            base_url = auth.get("base_url") or auth.get("baseUrl")
            if base_url:
                kwargs["baseUrl"] = base_url
            if source == "local":
                return Model.load(model_rid)
            return Model.fetch(model_rid, **kwargs)
        except ImportError:
            return None
        except Exception:
            return None

    def _check_voltage_violations_from_result(
        self, pf_result, threshold: float
    ) -> list[dict]:
        """Check voltage violations from CloudPSS power flow result object."""
        violations = []
        try:
            from cloudpss_skills_v2.powerapi.adapters.cloudpss.powerflow import (
                _parse_cloudpss_table,
                _normalize_bus_row,
            )

            bus_rows = _parse_cloudpss_table(pf_result.getBuses())
            normalized = [_normalize_bus_row(b) for b in bus_rows]

            lower_limit = 1.0 - threshold
            upper_limit = 1.0 + threshold

            for bus in normalized:
                vm = _as_float(bus.get("voltage_pu"), 1.0)
                bus_name = bus.get("name", "unknown")

                if vm < lower_limit:
                    violations.append(
                        {
                            "type": "voltage",
                            "bus_name": bus_name,
                            "voltage": round(vm, 4),
                            "limit": lower_limit,
                            "deviation": round(lower_limit - vm, 4),
                            "direction": "undervoltage",
                            "message": f"电压偏低: {bus_name} 电压={vm:.4f}pu (下限={lower_limit:.4f})",
                        }
                    )
                elif vm > upper_limit:
                    violations.append(
                        {
                            "type": "voltage",
                            "bus_name": bus_name,
                            "voltage": round(vm, 4),
                            "limit": upper_limit,
                            "deviation": round(vm - upper_limit, 4),
                            "direction": "overvoltage",
                            "message": f"电压偏高: {bus_name} 电压={vm:.4f}pu (上限={upper_limit:.4f})",
                        }
                    )
        except (AttributeError, TypeError):
            pass
        return violations

    def _check_thermal_violations_from_result(
        self, pf_result, threshold: float
    ) -> list[dict]:
        """Check thermal (overload) violations from CloudPSS power flow result object."""
        violations = []
        try:
            from cloudpss_skills_v2.powerapi.adapters.cloudpss.powerflow import (
                _parse_cloudpss_table,
                _normalize_branch_row,
            )

            branch_rows = _parse_cloudpss_table(pf_result.getBranches())
            normalized = [_normalize_branch_row(b) for b in branch_rows]

            for branch in normalized:
                branch_name = branch.get("name", "unknown")
                p_from = _as_float(branch.get("p_from_mw"))
                p_to = _as_float(branch.get("p_to_mw"))
                loading = max(abs(p_from), abs(p_to))

                # Use power_loss as a proxy for thermal loading if available
                loading_val = _as_float(branch.get("loading_pct"), 0)
                if loading_val > 0:
                    loading = loading_val / 100.0

                if loading > threshold:
                    utilization_pct = loading * 100
                    violations.append(
                        {
                            "type": "thermal",
                            "branch_name": branch_name,
                            "loading": round(loading, 4),
                            "threshold": threshold,
                            "utilization": round(utilization_pct, 2),
                            "message": f"线路过载: {branch_name} 负载率={utilization_pct:.1f}%",
                        }
                    )
        except (AttributeError, TypeError):
            pass
        return violations

    def _summarize_violations(self, violations: list[dict]) -> dict[str, Any]:
        if not violations:
            return None

        by_type = {}
        for v in violations:
            v_type = v.get("type", "unknown")
            by_type[v_type] = by_type.get(v_type, 0) + 1

        voltage_count = by_type.get("voltage", 0)
        thermal_count = by_type.get("thermal", 0)
        convergence_count = by_type.get("convergence", 0)

        if convergence_count > 0:
            severity = "critical"
        elif voltage_count > 0 and thermal_count > 0:
            severity = "high"
        elif thermal_count > 0:
            severity = "medium"
        else:
            severity = "low"

        return {
            "total_violations": len(violations),
            "by_type": by_type,
            "voltage_violations": voltage_count,
            "thermal_violations": thermal_count,
            "convergence_failures": convergence_count,
            "severity": severity,
            "messages": [v.get("message", "") for v in violations if v.get("message")],
        }

    def _save_output(self, result_data: dict, output_config: dict) -> None:
        output_path = Path(output_config.get("path", "./results/"))
        prefix = output_config.get("prefix", "n1_security")
        use_timestamp = output_config.get("timestamp", True)

        output_path.mkdir(parents=True, exist_ok=True)

        ts_suffix = (
            f"_{datetime.now().strftime('%Y%m%d_%H%M%S')}" if use_timestamp else ""
        )
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
                description="N-1安全校核报告",
            )
        )
        self._log("INFO", f"导出: {filepath}")


__all__ = ["N1SecuritySkill"]
