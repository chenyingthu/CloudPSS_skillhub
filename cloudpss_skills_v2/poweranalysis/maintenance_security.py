"""Maintenance Security Analysis - Assess security during planned outage.

检修安全校核 - 评估计划检修期间的系统安全性。
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from cloudpss_skills_v2.core.skill_result import (
    Artifact,
    SkillResult,
    SkillStatus,
)
from cloudpss_skills_v2.powerskill import Engine, ModelHandle, ComponentType

logger = logging.getLogger(__name__)


class MaintenanceSecurityAnalysis:
    name = "maintenance_security"
    description = "检修安全校核 - 评估计划检修期间的系统安全性"

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model", "maintenance"],
            "properties": {
                "skill": {"type": "string", "const": "maintenance_security", "default": "maintenance_security"},
                "engine": {
                    "type": "string",
                    "enum": ["cloudpss", "pandapower"],
                    "default": "pandapower",
                },
                "auth": {
                    "type": "object",
                    "properties": {
                        "token": {"type": "string", "default": "local-pandapower-token"},
                    },
                },
                "model": {
                    "type": "object",
                    "required": ["rid"],
                    "properties": {
                        "rid": {"type": "string", "default": "case14"},
                        "source": {"enum": ["cloud", "local"], "default": "local"},
                    },
                },
                "maintenance": {
                    "type": "object",
                    "required": ["branch_id"],
                    "properties": {
                        "branch_id": {"type": "string", "default": "line:0"},
                        "description": {"type": "string", "default": "Default N-1 branch outage"},
                        "duration_hours": {"type": "number", "default": 8},
                    },
                },
                "analysis": {
                    "type": "object",
                    "properties": {
                        "voltage_threshold": {"type": "number", "default": 0.05},
                        "thermal_threshold": {"type": "number", "default": 1.0},
                    },
                },
            },
        }

    def get_default_config(self) -> dict[str, Any]:
        return {
            "skill": self.name,
            "engine": "pandapower",
            "auth": {"token": "local-pandapower-token"},
            "model": {"rid": "case14", "source": "local"},
            "maintenance": {
                "branch_id": "line:0",
                "description": "Default N-1 branch outage",
                "duration_hours": 8,
            },
            "analysis": {
                "voltage_threshold": 0.05,
                "thermal_threshold": 1.0,
            },
        }

    def __init__(self):
        self.logs = []
        self.artifacts = []

    def _log(self, level: str, message: str) -> None:
        self.logs.append(
            {
                "timestamp": datetime.now().isoformat(),
                "level": level,
                "message": message,
            }
        )
        getattr(logger, level.lower(), logger.info)(message)

    def _classify_severity(
        self, min_vm: float | None, max_loading: float | None
    ) -> str:
        if min_vm is None or max_loading is None:
            return "unknown"
        if min_vm < 0.85 or max_loading > 1.2:
            return "critical"
        if min_vm < 0.9 or max_loading > 1.0:
            return "warning"
        return "normal"

    def validate(self, config: dict | None) -> tuple[bool, list[str]]:
        errors = []
        if not config:
            errors.append("config is required")
            return (False, errors)
        model = config.get("model", {})
        if not model.get("rid"):
            errors.append("model.rid is required")
        maintenance = config.get("maintenance", {})
        if not maintenance.get("branch_id"):
            errors.append("maintenance.branch_id is required")
        return (len(errors) == 0, errors)

    def run(self, config: dict | None) -> SkillResult:
        start_time = datetime.now()
        if config is None:
            config = {}
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
            self._log("INFO", f"Using engine: {api.adapter.engine_name}")

            model_config = config["model"]
            model_rid = model_config["rid"]
            self._log("INFO", f"Model: {model_rid}")

            maintenance_config = config["maintenance"]
            maintenance_branch = maintenance_config["branch_id"]
            self._log("INFO", f"Maintenance branch: {maintenance_branch}")

            handle = api.get_model_handle(model_rid)

            maintenance_handle = handle.clone()
            removed = maintenance_handle.remove_component(maintenance_branch)
            if not removed:
                self._log("WARNING", f"Could not remove branch: {maintenance_branch}")

            base_result = api.run_power_flow(model_handle=handle)
            post_result = api.run_power_flow(model_handle=maintenance_handle)

            analysis_config = config.get("analysis", {})
            voltage_threshold = analysis_config.get("voltage_threshold", 0.05)
            thermal_threshold = analysis_config.get("thermal_threshold", 1.0)

            severity = "normal"
            violations = []

            if post_result.is_success and post_result.data:
                if "bus_results" in post_result.data:
                    for bus in post_result.data["bus_results"]:
                        vm_pu = bus.get("vm_pu", 1.0)
                        if abs(vm_pu - 1.0) > voltage_threshold:
                            violations.append(
                                {
                                    "type": "voltage",
                                    "bus": bus.get("bus"),
                                    "vm_pu": vm_pu,
                                }
                            )
                            severity = "warning"

                if "branch_results" in post_result.data:
                    for branch in post_result.data["branch_results"]:
                        loading = branch.get("loading_pct", 0)
                        if loading > thermal_threshold:
                            violations.append(
                                {
                                    "type": "thermal",
                                    "branch": branch.get("branch"),
                                    "loading": loading,
                                }
                            )
                            severity = "critical"

            self._log("INFO", f"Severity: {severity}, violations: {len(violations)}")

            data = {
                "maintenance_branch": maintenance_branch,
                "severity": severity,
                "base_converged": base_result.is_success,
                "post_converged": post_result.is_success,
                "violations": violations,
            }

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                data=data,
                logs=self.logs,
                artifacts=self.artifacts,
                start_time=start_time,
                end_time=datetime.now(),
            )

        except Exception as e:
            self._log("ERROR", f"Maintenance security analysis failed: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error=str(e),
                logs=self.logs,
                start_time=start_time,
                end_time=datetime.now(),
            )


__all__ = ["MaintenanceSecurityAnalysis"]
