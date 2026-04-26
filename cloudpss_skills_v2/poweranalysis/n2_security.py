"""N2 Security Analysis - Check all pairwise contingency scenarios.

N-2安全校核 - 检查所有支路对的同时断开。
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from cloudpss_skills_v2.core.skill_result import (
    Artifact,
    SkillResult,
    SkillStatus,
)
from cloudpss_skills_v2.powerskill import Engine, ModelHandle, ComponentType

logger = logging.getLogger(__name__)


@dataclass
class N2ContingencyResult:
    branch_pair: tuple = ()
    converged: bool = False
    max_violation: float | None = None
    voltage_violation: bool = False
    thermal_violation: bool = False


class N2SecurityAnalysis:
    name = "n2_security"
    description = "N-2安全校核 - 检查支路对同时断开的安全"

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "n2_security"},
                "engine": {
                    "type": "string",
                    "enum": ["cloudpss", "pandapower"],
                    "default": "cloudpss",
                },
                "model": {
                    "type": "object",
                    "required": ["rid"],
                },
                "analysis": {
                    "type": "object",
                    "properties": {
                        "branches": {"type": "array", "items": {"type": "string"}},
                        "check_voltage": {"type": "boolean", "default": True},
                        "voltage_threshold": {"type": "number", "default": 0.05},
                        "thermal_threshold": {"type": "number", "default": 1.0},
                        "max_scenarios": {"type": "integer", "default": 100},
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
            "analysis": {
                "branches": ["line:0", "line:1"],
                "check_voltage": True,
                "voltage_threshold": 0.05,
                "thermal_threshold": 1.0,
                "max_scenarios": 1,
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

    def validate(self, config: dict | None) -> tuple[bool, list[str]]:
        errors = []
        if not config:
            errors.append("config is required")
            return (False, errors)
        if not config.get("model", {}).get("rid"):
            errors.append("model.rid is required")
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

            handle = api.get_model_handle(model_rid)
            branches = handle.get_components_by_type(ComponentType.BRANCH)
            transformers = handle.get_components_by_type(ComponentType.TRANSFORMER)
            all_branches = branches + transformers

            self._log("INFO", f"Found {len(all_branches)} branches for N-2 analysis")

            analysis_config = config.get("analysis", {})
            target_branches = analysis_config.get("branches", [])
            if target_branches:
                all_branches = [
                    b
                    for b in all_branches
                    if b.name in target_branches or b.key in target_branches
                ]
                self._log("INFO", f"Analyzing {len(all_branches)} target branches")

            voltage_threshold = analysis_config.get("voltage_threshold", 0.05)
            thermal_threshold = analysis_config.get("thermal_threshold", 1.0)
            max_scenarios = analysis_config.get("max_scenarios", 100)

            results: list[N2ContingencyResult] = []
            passed = 0
            failed = 0
            scenario_count = 0

            for i, branch1 in enumerate(all_branches):
                for j, branch2 in enumerate(all_branches):
                    if i >= j:
                        continue
                    if scenario_count >= max_scenarios:
                        break

                    self._log(
                        "INFO", f"[{scenario_count}] {branch1.name} + {branch2.name}"
                    )
                    scenario_count += 1

                    working = handle.clone()
                    working.remove_component(branch1.key)
                    working.remove_component(branch2.key)

                    sim_result = api.run_power_flow(model_handle=working)

                    result = N2ContingencyResult(
                        branch_pair=(branch1.key, branch2.key),
                        converged=sim_result.is_success,
                    )

                    if sim_result.is_success and sim_result.data:
                        if "bus_results" in sim_result.data:
                            for bus in sim_result.data["bus_results"]:
                                vm_pu = bus.get("vm_pu", 1.0)
                                if abs(vm_pu - 1.0) > voltage_threshold:
                                    result.voltage_violation = True
                                    result.max_violation = abs(vm_pu - 1.0)
                                    break

                    if not result.converged or result.voltage_violation:
                        failed += 1
                        self._log(
                            "WARNING",
                            f"  -> Failed: converged={result.converged}, v_viol={result.voltage_violation}",
                        )
                    else:
                        passed += 1

                    results.append(result)

                if scenario_count >= max_scenarios:
                    break

            summary = {
                "total_scenarios": scenario_count,
                "passed": passed,
                "failed": failed,
                "success_rate": passed / scenario_count if scenario_count else 0,
            }

            self._log(
                "INFO",
                f"N-2 results: {passed}/{scenario_count} passed, {failed} failed",
            )

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                data={
                    "summary": summary,
                    "results": [
                        {
                            "pair": r.branch_pair,
                            "converged": r.converged,
                            "violation": r.voltage_violation,
                        }
                        for r in results
                    ],
                },
                logs=self.logs,
                start_time=start_time,
                end_time=datetime.now(),
            )

        except Exception as e:
            self._log("ERROR", f"N-2 analysis failed: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error=str(e),
                logs=self.logs,
                start_time=start_time,
                end_time=datetime.now(),
            )


__all__ = ["N2SecurityAnalysis", "N2ContingencyResult"]
