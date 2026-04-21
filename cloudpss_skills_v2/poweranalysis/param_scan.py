"""Parametric Scan Analysis - Scan parameter values and analyze system response.

参数扫描分析 - 扫描参数值并分析系统响应。
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
from cloudpss_skills_v2.powerskill import Engine, PowerFlow

logger = logging.getLogger(__name__)


class ParamScanAnalysis:
    name = "param_scan"
    description = "参数扫描分析 - 扫描参数值分析系统响应"

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model", "scan"],
            "properties": {
                "skill": {"type": "string", "const": "param_scan"},
                "engine": {
                    "type": "string",
                    "enum": ["cloudpss", "pandapower"],
                    "default": "pandapower",
                },
                "model": {
                    "type": "object",
                    "required": ["rid"],
                    "properties": {"rid": {"type": "string"}},
                },
                "scan": {
                    "type": "object",
                    "required": ["parameter", "values"],
                    "properties": {
                        "parameter": {
                            "type": "string",
                            "description": "e.g., load.p_mw, gen.p_mw",
                        },
                        "values": {"type": "array", "items": {"type": "number"}},
                        "component": {
                            "type": "string",
                            "description": "Component key to modify",
                        },
                    },
                },
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
        scan = config.get("scan", {})
        if not scan.get("parameter"):
            errors.append("scan.parameter is required")
        if not scan.get("values"):
            errors.append("scan.values is required")
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
            engine = config.get("engine", "pandapower")
            api = Engine.create_powerflow(engine=engine)
            self._log("INFO", f"Using engine: {api.adapter.engine_name}")

            model_rid = config["model"]["rid"]
            self._log("INFO", f"Model: {model_rid}")

            scan_config = config["scan"]
            parameter = scan_config["parameter"]
            values = scan_config["values"]
            component_key = scan_config.get("component")

            self._log("INFO", f"Scanning {parameter} across {len(values)} values")

            handle = api.get_model_handle(model_rid)
            results = []

            for i, value in enumerate(values):
                self._log("INFO", f"[{i + 1}/{len(values)}] {parameter}={value}")

                working = handle.clone()
                if component_key:
                    working.update_component_args(component_key, parameter, value)

                sim_result = api.run_power_flow(model_handle=working)

                results.append(
                    {
                        "index": i,
                        "parameter": parameter,
                        "value": value,
                        "converged": sim_result.is_success,
                        "errors": sim_result.errors,
                    }
                )

                if sim_result.is_success:
                    self._log("INFO", f"  -> Converged")
                else:
                    self._log("ERROR", f"  -> Failed: {sim_result.errors}")

            passed = len([r for r in results if r["converged"]])

            result_data = {
                "parameter": parameter,
                "total_values": len(values),
                "converged": passed,
                "failed": len(values) - passed,
                "results": results,
            }

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.COMPLETED,
                data=result_data,
                logs=self.logs,
                artifacts=self.artifacts,
                start_time=start_time,
                end_time=datetime.now(),
            )

        except Exception as e:
            self._log("ERROR", f"Param scan failed: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error=str(e),
                logs=self.logs,
                start_time=start_time,
                end_time=datetime.now(),
            )


__all__ = ["ParamScanAnalysis"]
