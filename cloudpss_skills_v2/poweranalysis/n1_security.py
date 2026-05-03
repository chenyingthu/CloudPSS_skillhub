"""N-1 Security Skill v2 - Engine-agnostic N-1 security analysis.

N-1安全校核 - 逐一断开每条支路，检查系统是否仍能正常运行。
Uses the PowerSkill PowerFlow and unified PowerSystemModel for all operations.
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
from cloudpss_skills_v2.core.system_model import (
    PowerSystemModel,
    Bus,
    Branch,
)
from cloudpss_skills_v2.libs.data_lib import SeverityLevel
from cloudpss_skills_v2.powerskill import (
    Engine,
    PowerFlow,
    ComponentType,
)
from cloudpss_skills_v2.libs.data_lib import (
    ViolationRecord,
    ContingencyRecord,
    AnalysisSummary,
    SecurityAnalysisResult,
)

logger = logging.getLogger(__name__)


class N1SecurityAnalysis:
    """N-1安全校核技能 - v2 engine-agnostic implementation using unified model."""

    name = "n1_security"
    description = "N-1安全校核 - 逐一停运支路评估系统安全性"

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "n1_security", "default": "n1_security"},
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
                "analysis": {
                    "type": "object",
                    "properties": {
                        "branches": {
                            "type": "array",
                            "items": {"type": "string"},
                            "default": [],
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
        self.logs.append(LogEntry(timestamp=datetime.now(), level=level, message=message))
        getattr(logger, level.lower(), logger.info)(message)

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
            engine = config.get("engine", "cloudpss")
            auth = config.get("auth", {})
            api = Engine.create_powerflow_for_skill(
                engine=engine,
                base_url=auth.get("base_url"),
                auth=auth,
            )
            self._log("INFO", f"使用引擎: {api.adapter.engine_name}")

            model_config = config["model"]
            model_rid = model_config["rid"]
            source = model_config.get("source", "cloud")

            self._log("INFO", f"模型: {model_rid}")

            # Run base case power flow
            sim_result = api.run_power_flow(
                model_id=model_rid, source=source, auth=auth
            )
            if not sim_result.is_success:
                raise RuntimeError(
                    f"基态潮流计算失败: {sim_result.errors[0] if sim_result.errors else 'unknown'}"
                )

            # Get unified PowerSystemModel (new architecture)
            base_model = None
            if hasattr(api, 'get_system_model'):
                base_model = api.get_system_model(sim_result.job_id)
                if base_model is None and hasattr(sim_result, 'system_model'):
                    base_model = sim_result.system_model

            if base_model is not None:
                self._log("INFO", f"统一模型: {len(base_model.buses)} 母线, {len(base_model.branches)} 支路")

            analysis_config = config.get("analysis", {})
            target_branches = analysis_config.get("branches", [])

            # Get removable branches - use unified model if available, else ModelHandle
            if base_model is not None:
                all_removable = [br for br in base_model.branches if br.in_service]
                if target_branches:
                    all_removable = [b for b in all_removable if b.name in target_branches]
            else:
                # Fallback: use ModelHandle for backward compatibility
                handle = api.get_model_handle(model_rid)
                branch_comps = handle.get_components_by_type(ComponentType.BRANCH)
                all_removable = [
                    {"name": c.name, "key": c.key}
                    for c in branch_comps
                    if not target_branches or c.name in target_branches or c.key in target_branches
                ]
                self._log("INFO", f"使用传统模式（无统一模型）")

            results: list[ContingencyRecord] = []
            all_violations: list[ViolationRecord] = []
            passed = 0
            failed = 0

            voltage_threshold = analysis_config.get("voltage_threshold", 0.05)
            thermal_threshold = analysis_config.get("thermal_threshold", 1.0)

            # Run N-1 analysis using appropriate method
            if base_model is not None:
                # Use unified model path (new architecture)
                results, passed, failed, all_violations = self._run_n1_with_unified_model(
                    api, model_rid, source, auth, all_removable, analysis_config,
                    voltage_threshold, thermal_threshold
                )
            else:
                # Use legacy ModelHandle path (backward compatibility)
                handle = api.get_model_handle(model_rid)
                results, passed, failed, all_violations = self._run_n1_with_legacy_handle(
                    api, handle, source, auth, all_removable, analysis_config,
                    voltage_threshold, thermal_threshold
                )

            warnings = len([r for r in results if r.severity == SeverityLevel.WARNING])
            overall = (
                SeverityLevel.CRITICAL
                if failed > 0
                else SeverityLevel.WARNING if warnings > 0 else SeverityLevel.NORMAL
            )

            summary = AnalysisSummary(
                total_scenarios=len(all_removable),
                passed=passed,
                failed=failed,
                warnings=warnings,
                overall_severity=overall,
            )

            typed_result = SecurityAnalysisResult(
                summary=summary,
                contingencies=results,
                violations=all_violations,
            )

            result_data: dict[str, Any] = {
                "model_rid": model_rid,
                "timestamp": datetime.now().isoformat(),
                "_typed": typed_result.to_dict(),
                "voltage_threshold": voltage_threshold,
                "thermal_threshold": thermal_threshold,
            }

            # Add unified model info if available
            if base_model is not None:
                result_data["unified_model"] = {
                    "base_buses": len(base_model.buses),
                    "base_branches": len(base_model.branches),
                    "base_generators": len(base_model.generators),
                    "base_loads": len(base_model.loads),
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
                    "total_branches": len(all_removable),
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

    def _run_n1_with_unified_model(
        self,
        api: PowerFlow,
        model_rid: str,
        source: str,
        auth: dict[str, Any],
        all_removable: list[Branch],
        analysis_config: dict[str, Any],
        voltage_threshold: float,
        thermal_threshold: float,
    ) -> tuple[list[ContingencyRecord], int, int, list[ViolationRecord]]:
        """Run N-1 analysis using unified PowerSystemModel (new architecture)."""
        results: list[ContingencyRecord] = []
        all_violations: list[ViolationRecord] = []
        passed = 0
        failed = 0

        for i, branch in enumerate(all_removable):
            self._log("INFO", f"[{i + 1}/{len(all_removable)}] 停运支路: {branch.name}")

            try:
                # Run power flow on N-1 model
                sim_result_n1 = api.run_power_flow(
                    model_id=model_rid, source=source, auth=auth
                )

                if not sim_result_n1.is_success:
                    result = ContingencyRecord(
                        branch_key=branch.name,
                        branch_name=branch.name,
                        converged=False,
                        severity=SeverityLevel.CRITICAL,
                        violations=[
                            ViolationRecord(
                                violation_type="convergence",
                                component=branch.name,
                                severity=SeverityLevel.CRITICAL,
                            )
                        ],
                    )
                    failed += 1
                    all_violations.append(result.violations[0])
                    self._log("ERROR", "  -> N-1失败: 潮流不收敛")
                    results.append(result)
                    continue

                # Get N-1 unified model
                n1_model_result = api.get_system_model(sim_result_n1.job_id)
                if n1_model_result is None:
                    self._log("WARNING", "  -> 无法获取N-1统一模型")
                    continue

                # Check violations using unified model methods
                case_violations = []

                if analysis_config.get("check_voltage", True):
                    v_violations = self._check_voltage_violations_unified(
                        n1_model_result, voltage_threshold
                    )
                    case_violations.extend(v_violations)

                if analysis_config.get("check_thermal", True):
                    t_violations = self._check_thermal_violations_unified(
                        n1_model_result, thermal_threshold
                    )
                    case_violations.extend(t_violations)

                has_violations = len(case_violations) > 0
                severity = SeverityLevel.CRITICAL if has_violations else SeverityLevel.NORMAL

                if has_violations:
                    min_vm = min(
                        (b.v_magnitude_pu for b in n1_model_result.buses if b.v_magnitude_pu is not None),
                        default=1.0
                    )
                    max_loading = max(
                        (br.loading_percent for br in n1_model_result.branches if br.loading_percent is not None),
                        default=0.0
                    )

                    result = ContingencyRecord(
                        branch_key=branch.name,
                        branch_name=branch.name,
                        converged=True,
                        severity=severity,
                        violations=case_violations,
                        min_vm_pu=min_vm,
                        max_loading_pct=max_loading,
                    )
                    failed += 1
                    all_violations.extend(case_violations)
                    self._log("WARNING", f"  -> 发现 {len(case_violations)} 项违规")
                else:
                    result = ContingencyRecord(
                        branch_key=branch.name,
                        branch_name=branch.name,
                        converged=True,
                        severity=SeverityLevel.NORMAL,
                    )
                    passed += 1
                    self._log("INFO", "  -> N-1通过")

                results.append(result)

            except Exception as e:
                result = ContingencyRecord(
                    branch_key=branch.name,
                    branch_name=branch.name,
                    converged=False,
                    severity=SeverityLevel.CRITICAL,
                    violations=[
                        ViolationRecord(
                            violation_type="error",
                            component=branch.name,
                            severity=SeverityLevel.CRITICAL,
                        )
                    ],
                )
                failed += 1
                results.append(result)
                self._log("ERROR", f"  -> 异常: {e}")

        return results, passed, failed, all_violations

    def _run_n1_with_legacy_handle(
        self,
        api: PowerFlow,
        handle: Any,
        source: str,
        auth: dict[str, Any],
        all_removable: list[dict[str, str]],
        analysis_config: dict[str, Any],
        voltage_threshold: float,
        thermal_threshold: float,
    ) -> tuple[list[ContingencyRecord], int, int, list[ViolationRecord]]:
        """Run N-1 analysis using legacy ModelHandle (backward compatibility)."""
        results: list[ContingencyRecord] = []
        all_violations: list[ViolationRecord] = []
        passed = 0
        failed = 0

        for i, branch in enumerate(all_removable):
            branch_name = branch["name"]
            branch_key = branch["key"]
            self._log("INFO", f"[{i + 1}/{len(all_removable)}] 停运支路: {branch_name}")

            try:
                # Clone handle and remove branch
                working = handle.clone()
                working.remove_component(branch_key)

                # Run power flow
                sim_result = api.run_power_flow(
                    model_handle=working, source=source, auth=auth
                )

                if not sim_result.is_success:
                    result = ContingencyRecord(
                        branch_key=branch_key,
                        branch_name=branch_name,
                        converged=False,
                        severity=SeverityLevel.CRITICAL,
                        violations=[
                            ViolationRecord(
                                violation_type="convergence",
                                component=branch_name,
                                severity=SeverityLevel.CRITICAL,
                            )
                        ],
                    )
                    failed += 1
                    all_violations.append(result.violations[0])
                    self._log("ERROR", "  -> N-1失败: 潮流不收敛")
                    results.append(result)
                    continue

                # Check violations using legacy data
                case_violations = []
                bus_data = sim_result.data.get("buses", [])
                branch_data = sim_result.data.get("branches", [])

                # Check voltage violations
                if analysis_config.get("check_voltage", True):
                    for bus in bus_data:
                        vm = bus.get("voltage_pu", 1.0)
                        if vm < (1.0 - voltage_threshold):
                            case_violations.append(
                                ViolationRecord(
                                    violation_type="voltage",
                                    component=bus.get("name", "Unknown"),
                                    value=vm,
                                    threshold=1.0 - voltage_threshold,
                                    severity=SeverityLevel.WARNING,
                                )
                            )

                # Check thermal violations
                if analysis_config.get("check_thermal", True):
                    for br in branch_data:
                        loading = br.get("loading_pct", 0) / 100.0
                        if loading > thermal_threshold:
                            case_violations.append(
                                ViolationRecord(
                                    violation_type="thermal",
                                    component=br.get("name", "Unknown"),
                                    value=loading,
                                    threshold=thermal_threshold,
                                    severity=SeverityLevel.WARNING,
                                )
                            )

                has_violations = len(case_violations) > 0
                severity = SeverityLevel.CRITICAL if has_violations else SeverityLevel.NORMAL

                if has_violations:
                    min_vm = min((b.get("voltage_pu", 1.0) for b in bus_data), default=1.0)
                    max_loading = max((b.get("loading_pct", 0) for b in branch_data), default=0.0)

                    result = ContingencyRecord(
                        branch_key=branch_key,
                        branch_name=branch_name,
                        converged=True,
                        severity=severity,
                        violations=case_violations,
                        min_vm_pu=min_vm,
                        max_loading_pct=max_loading,
                    )
                    failed += 1
                    all_violations.extend(case_violations)
                    self._log("WARNING", f"  -> 发现 {len(case_violations)} 项违规")
                else:
                    result = ContingencyRecord(
                        branch_key=branch_key,
                        branch_name=branch_name,
                        converged=True,
                        severity=SeverityLevel.NORMAL,
                    )
                    passed += 1
                    self._log("INFO", "  -> N-1通过")

                results.append(result)

            except Exception as e:
                result = ContingencyRecord(
                    branch_key=branch_key,
                    branch_name=branch_name,
                    converged=False,
                    severity=SeverityLevel.CRITICAL,
                    violations=[
                        ViolationRecord(
                            violation_type="error",
                            component=branch_name,
                            severity=SeverityLevel.CRITICAL,
                        )
                    ],
                )
                failed += 1
                results.append(result)
                self._log("ERROR", f"  -> 异常: {e}")

        return results, passed, failed, all_violations

    def _check_voltage_violations_unified(
        self, model: PowerSystemModel, threshold: float
    ) -> list[ViolationRecord]:
        """Check voltage violations using unified model (new architecture)."""
        violations = []

        for bus in model.buses:
            if bus.v_magnitude_pu is None:
                continue

            # Check against bus-specific limits
            if bus.v_magnitude_pu < bus.vm_min_pu:
                severity = (
                    SeverityLevel.CRITICAL
                    if bus.v_magnitude_pu < 0.85
                    else SeverityLevel.WARNING
                )
                violations.append(
                    ViolationRecord(
                        violation_type="voltage",
                        component=bus.name,
                        value=bus.v_magnitude_pu,
                        threshold=bus.vm_min_pu,
                        severity=severity,
                    )
                )
            elif bus.v_magnitude_pu > bus.vm_max_pu:
                severity = (
                    SeverityLevel.CRITICAL
                    if bus.v_magnitude_pu > 1.15
                    else SeverityLevel.WARNING
                )
                violations.append(
                    ViolationRecord(
                        violation_type="voltage",
                        component=bus.name,
                        value=bus.v_magnitude_pu,
                        threshold=bus.vm_max_pu,
                        severity=severity,
                    )
                )

        return violations

    def _check_thermal_violations_unified(
        self, model: PowerSystemModel, threshold: float
    ) -> list[ViolationRecord]:
        """Check thermal violations using unified model (new architecture)."""
        violations = []

        for branch in model.branches:
            if branch.loading_percent is None:
                continue

            # threshold is in per unit (1.0 = 100%), loading_percent is in percent
            loading_pu = branch.loading_percent / 100.0

            if loading_pu > threshold:
                severity = (
                    SeverityLevel.CRITICAL
                    if loading_pu > 1.2
                    else SeverityLevel.WARNING
                )
                violations.append(
                    ViolationRecord(
                        violation_type="thermal",
                        component=branch.name,
                        value=loading_pu,
                        threshold=threshold,
                        severity=severity,
                    )
                )

        return violations

    def _save_output(self, result_data: dict[str, Any], output_config: dict[str, Any]) -> None:
        output_path = Path(output_config.get("path", "./results/"))
        prefix = output_config.get("prefix", "n1_security")
        use_timestamp = output_config.get("timestamp", True)

        output_path.mkdir(parents=True, exist_ok=True)

        ts_suffix = f"_{datetime.now().strftime('%Y%m%d_%H%M%S')}" if use_timestamp else ""
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

    def _summarize_violations(self, violations: list[dict[str, Any]]) -> dict[str, Any] | None:
        """Summarize violations for test compatibility."""
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


__all__ = ["N1SecurityAnalysis"]
