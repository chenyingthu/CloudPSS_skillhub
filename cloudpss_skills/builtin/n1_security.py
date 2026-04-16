"""
N-1 Security Check Skill

N-1安全校核 - 逐一断开每条支路，检查系统是否仍能正常运行。
"""

import json
import logging
from datetime import datetime
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
from cloudpss_skills.core import (
    setup_auth,
    reload_model,
    run_powerflow_and_wait,
    OutputConfig,
    save_json,
)
from cloudpss_skills.core.model_utils import remove_component_safe

logger = logging.getLogger(__name__)


@register
class N1SecuritySkill(SkillBase):
    """N-1安全校核技能"""

    @property
    def name(self) -> str:
        return "n1_security"

    @property
    def description(self) -> str:
        return "N-1安全校核 - 逐一停运支路评估系统安全性"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "n1_security"},
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
                        "check_voltage": {"type": "boolean", "default": True},
                        "check_thermal": {"type": "boolean", "default": True},
                        "voltage_threshold": {
                            "type": "number",
                            "default": 0.05,
                            "description": "电压越限阈值(标幺值)",
                        },
                        "thermal_threshold": {
                            "type": "number",
                            "default": 1.0,
                            "description": "热稳定阈值(标幺值)",
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

    def get_default_config(self) -> Dict[str, Any]:
        return {
            "skill": self.name,
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

    def run(self, config: Dict[str, Any]) -> SkillResult:
        """执行N-1安全校核"""
        from cloudpss import Model

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
            log("INFO", "认证成功")

            model_config = config["model"]
            model = reload_model(
                model_config["rid"],
                model_config.get("source", "cloud"),
                config,
            )
            log("INFO", f"模型: {model.name} ({model.rid})")

            components = model.getAllComponents()
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

            log("INFO", f"发现 {len(branches)} 条支路")

            analysis_config = config.get("analysis", {})
            target_branches = analysis_config.get("branches", [])

            if target_branches:
                branches = [
                    b
                    for b in branches
                    if b["name"] in target_branches or b["id"] in target_branches
                ]
                log("INFO", f"将检查 {len(branches)} 条指定支路")

            results = []
            passed = 0
            failed = 0
            violations_found = []

            voltage_threshold = analysis_config.get("voltage_threshold", 0.05)
            thermal_threshold = analysis_config.get("thermal_threshold", 1.0)

            for i, branch in enumerate(branches):
                log("INFO", f"[{i + 1}/{len(branches)}] 停运支路: {branch['name']}")

                working_model = reload_model(
                    model_config["rid"],
                    model_config.get("source", "cloud"),
                    config,
                )

                if not remove_component_safe(working_model, branch["id"]):
                    log("WARNING", f"  -> 移除支路失败")
                    continue

                job_result = run_powerflow_and_wait(working_model, config, log_func=log)

                case_violations = []

                if job_result.success:
                    # 检查电压和热稳定违规
                    if analysis_config.get("check_voltage", True):
                        voltage_violations = self._check_voltage_violations(
                            job_result.result, voltage_threshold
                        )
                        case_violations.extend(voltage_violations)

                    if analysis_config.get("check_thermal", True):
                        thermal_violations = self._check_thermal_violations(
                            job_result.result, thermal_threshold
                        )
                        case_violations.extend(thermal_violations)

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
                        log("WARNING", f"  -> 发现电压/热稳定违规")
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
                        log("INFO", f"  -> N-1通过")

                    pf_result = job_result.result
                    bus_voltages = self._extract_bus_voltages(pf_result)
                    branch_loadings = self._extract_branch_loadings(pf_result)
                    result["bus_voltages"] = bus_voltages
                    result["branch_loadings"] = branch_loadings
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
                    log("ERROR", f"  -> N-1失败: 潮流不收敛")

                results.append(result)

            log("INFO", f"N-1校核完成: 通过 {passed}, 失败 {failed}")
            log(
                "INFO",
                f"通过率: {passed / len(branches) * 100:.1f}%" if branches else "N/A",
            )

            output_config = config.get("output", {})
            output = OutputConfig(
                path=output_config.get("path", "./results/"),
                prefix=output_config.get("prefix", "n1_security"),
                timestamp=output_config.get("timestamp", True),
            )

            result_data = {
                "model_name": model.name,
                "model_rid": model.rid,
                "timestamp": datetime.now().isoformat(),
                "summary": {
                    "total_branches": len(branches),
                    "passed": passed,
                    "failed": failed,
                    "pass_rate": passed / len(branches) if branches else 0,
                },
                "results": results,
                "failed_branches": [r for r in results if r["status"] != "passed"],
            }

            export_result = save_json(
                result_data, output, description="N-1安全校核报告"
            )
            if export_result.artifact:
                artifacts.append(export_result.artifact)

            # Add detailed violations to result_data for completeness
            result_data["all_violations"] = violations_found
            result_data["voltage_threshold"] = voltage_threshold
            result_data["thermal_threshold"] = thermal_threshold

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS if failed == 0 else SkillStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                data=result_data,
                artifacts=artifacts,
                logs=logs,
                metrics={
                    "total_branches": len(branches),
                    "passed": passed,
                    "failed": failed,
                },
            )

        except (KeyError, AttributeError, ConnectionError) as e:
            log("ERROR", f"执行失败: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                data={
                    "success": False,
                    "error": str(e),
                    "stage": "n1_security",
                },
                artifacts=artifacts,
                logs=logs,
                error=str(e),
            )

    def _check_voltage_violations(
        self, result: Any, threshold: float
    ) -> List[Dict[str, Any]]:
        """检查电压越限违规

        Args:
            result: 潮流结果对象
            threshold: 电压偏差阈值(标幺值)，正常范围为 [1-threshold, 1+threshold]

        Returns:
            电压违规列表，每项包含:
            - type: "voltage"
            - bus_name: 母线名称
            - bus_id: 母线ID
            - voltage: 实际电压(标幺值)
            - deviation: 偏离正常值的程度
            - message: 违规描述
        """
        violations = []

        # Try to get bus data from result
        try:
            buses = result.get("buses", [])
            if not buses:
                # Try alternative method: get from result directly
                pf_result = getattr(result, "_data", {}) or result
                buses = pf_result.get("buses", pf_result.get("Bus", []))
        except (AttributeError, TypeError):
            buses = []

        for bus in buses:
            # Handle both dict and object formats
            try:
                bus_name = bus.get(
                    "name", bus.get("busName", f"Bus_{bus.get('id', 'unknown')}")
                )
                bus_id = bus.get("id", bus.get("bus", "unknown"))
                voltage = bus.get("voltage", bus.get("V", None))

                if voltage is None:
                    continue

                # Check if voltage is outside normal range
                lower_limit = 1.0 - threshold
                upper_limit = 1.0 + threshold

                if voltage < lower_limit:
                    deviation = lower_limit - voltage
                    violations.append(
                        {
                            "type": "voltage",
                            "bus_name": str(bus_name),
                            "bus_id": str(bus_id),
                            "voltage": round(voltage, 4),
                            "limit": lower_limit,
                            "deviation": round(deviation, 4),
                            "direction": "undervoltage",
                            "message": f"电压偏低: {bus_name} 电压={voltage:.4f}pu (下限={lower_limit:.4f})",
                        }
                    )
                elif voltage > upper_limit:
                    deviation = voltage - upper_limit
                    violations.append(
                        {
                            "type": "voltage",
                            "bus_name": str(bus_name),
                            "bus_id": str(bus_id),
                            "voltage": round(voltage, 4),
                            "limit": upper_limit,
                            "deviation": round(deviation, 4),
                            "direction": "overvoltage",
                            "message": f"电压偏高: {bus_name} 电压={voltage:.4f}pu (上限={upper_limit:.4f})",
                        }
                    )
            except (KeyError, TypeError, AttributeError):
                continue

        return violations

    def _check_thermal_violations(
        self, result: Any, threshold: float
    ) -> List[Dict[str, Any]]:
        """检查热稳定(线路过载)违规

        Args:
            result: 潮流结果对象
            threshold: 热稳定阈值(标幺值)，线路电流/功率超过此值视为过载

        Returns:
            热稳定违规列表，每项包含:
            - type: "thermal"
            - branch_name: 支路名称
            - branch_id: 支路ID
            - loading: 实际负载率
            - limit: 限制值
            - utilization: 利用率百分比
            - message: 违规描述
        """
        violations = []

        # Try to get branch/line data from result
        try:
            branches = result.get("branches", [])
            if not branches:
                pf_result = getattr(result, "_data", {}) or result
                branches = pf_result.get("branches", pf_result.get("Branch", []))
        except (AttributeError, TypeError):
            branches = []

        for branch in branches:
            try:
                branch_name = branch.get(
                    "name",
                    branch.get("branchName", f"Branch_{branch.get('id', 'unknown')}"),
                )
                branch_id = branch.get("id", branch.get("branch", "unknown"))

                # Get loading/utilization data
                loading = branch.get("loading", branch.get("utilization", None))

                # Try to calculate loading from current or power
                if loading is None:
                    current = branch.get("current", branch.get("I", None))
                    rating = branch.get("rating", branch.get("limit", 1.0))
                    power = branch.get("power", branch.get("S", None))
                    power_rating = branch.get("powerRating", branch.get("rating", 1.0))

                    if current is not None and rating:
                        loading = current / rating
                    elif power is not None and power_rating:
                        loading = abs(power) / power_rating

                if loading is None:
                    continue

                # Check if loading exceeds threshold
                if loading > threshold:
                    utilization_pct = loading * 100
                    violations.append(
                        {
                            "type": "thermal",
                            "branch_name": str(branch_name),
                            "branch_id": str(branch_id),
                            "loading": round(loading, 4),
                            "threshold": threshold,
                            "utilization": round(utilization_pct, 2),
                            "excess": round(loading - threshold, 4),
                            "message": f"线路过载: {branch_name} 负载率={utilization_pct:.1f}% (阈值={threshold * 100:.0f}%)",
                        }
                    )
            except (KeyError, TypeError, AttributeError):
                continue

        return violations

    def _extract_bus_voltages(self, pf_result) -> Dict[str, float]:
        try:
            buses_raw = pf_result.getBuses()
            if not buses_raw:
                return {}
            buses = self._parse_table(buses_raw)
            voltage_col = None
            if buses and len(buses) > 0:
                for key in buses[0].keys():
                    lowered = key.lower()
                    if ("vm" in lowered or "v" in lowered) and "pu" in lowered:
                        voltage_col = key
                        break
            return {
                bus.get("Bus", bus.get("name", f"bus_{i}")): round(
                    abs(bus.get(voltage_col, 1.0)), 4
                )
                if voltage_col
                else 1.0
                for i, bus in enumerate(buses)
            }
        except (AttributeError, TypeError):
            return {}

    def _extract_branch_loadings(self, pf_result) -> Dict[str, float]:
        try:
            branches_raw = pf_result.getBranches()
            if not branches_raw:
                return {}
            branches = self._parse_table(branches_raw)
            loading_col = None
            if branches and len(branches) > 0:
                for key in branches[0].keys():
                    lowered = key.lower()
                    if "loading" in lowered or "load" in lowered or "%" in lowered:
                        loading_col = key
                        break
            return {
                branch.get("Branch", branch.get("name", f"branch_{i}")): round(
                    branch.get(loading_col, 0.0), 4
                )
                if loading_col
                else 0.0
                for i, branch in enumerate(branches)
            }
        except (AttributeError, TypeError):
            return {}
            buses = self._parse_table(buses_raw)
            voltage_col = None
            if buses and len(buses) > 0:
                for key in buses[0].keys():
                    lowered = key.lower()
                    if ("vm" in lowered or "v" in lowered) and "pu" in lowered:
                        voltage_col = key
                        break
            return {
                bus.get("Bus", bus.get("name", f"bus_{i}")): round(
                    abs(bus.get(voltage_col, 1.0)), 4
                )
                if voltage_col
                else 1.0
                for i, bus in enumerate(buses)
            }
        except (AttributeError, TypeError):
            return {}

    def _extract_branch_loadings(self, pf_result) -> Dict[str, float]:
        """提取支路负载率数据"""
        try:
            branches_raw = pf_result.getBranches()
            if not branches_raw:
                return {}
            branches = self._parse_table(branches_raw)
            loading_col = None
            if branches and len(branches) > 0:
                for key in branches[0].keys():
                    lowered = key.lower()
                    if "loading" in lowered or "load" in lowered or "%" in lowered:
                        loading_col = key
                        break
            return {
                branch.get("Branch", branch.get("name", f"branch_{i}")): round(
                    branch.get(loading_col, 0.0), 4
                )
                if loading_col
                else 0.0
                for i, branch in enumerate(branches)
            }
        except (AttributeError, TypeError):
            return {}

    def _summarize_violations(self, violations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """汇总违规信息

        Args:
            violations: 违规列表

        Returns:
            违规汇总统计，包含:
            - total_violations: 违规总数
            - by_type: 按类型分组的违规统计
            - by_bus/branch: 按设备分组的违规详情
            - severity: 严重程度评估
        """
        if not violations:
            return None

        summary = {
            "total_violations": len(violations),
            "by_type": {},
            "affected_devices": [],
            "severity": "low",
            "messages": [],
        }

        # Group by type
        voltage_count = 0
        thermal_count = 0
        convergence_count = 0

        for v in violations:
            v_type = v.get("type", "unknown")
            summary["by_type"][v_type] = summary["by_type"].get(v_type, 0) + 1

            if v_type == "voltage":
                voltage_count += 1
            elif v_type == "thermal":
                thermal_count += 1
            elif v_type == "convergence":
                convergence_count += 1

            # Track affected devices
            if v_type == "voltage":
                device = v.get("bus_name", v.get("bus_id", "unknown"))
                device_type = "bus"
            else:
                device = v.get("branch_name", v.get("branch_id", "unknown"))
                device_type = "branch"

            summary["affected_devices"].append(
                {
                    "name": device,
                    "type": device_type,
                    "violation_type": v_type,
                }
            )

            # Add message if present
            msg = v.get("message")
            if msg:
                summary["messages"].append(msg)

        # Calculate severity
        if convergence_count > 0:
            summary["severity"] = "critical"
        elif voltage_count > 0 and thermal_count > 0:
            summary["severity"] = "high"
        elif thermal_count > 0:
            summary["severity"] = "medium"
        elif voltage_count > 0:
            summary["severity"] = "low"

        # Add counts to summary
        summary["voltage_violations"] = voltage_count
        summary["thermal_violations"] = thermal_count
        summary["convergence_failures"] = convergence_count

        return summary
