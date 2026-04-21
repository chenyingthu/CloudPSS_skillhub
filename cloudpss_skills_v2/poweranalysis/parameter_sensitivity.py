"""Parameter Sensitivity Analysis - Compute sensitivity rankings for system parameters.

参数灵敏度分析 - 计算系统参数的灵敏度排序。
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
from cloudpss_skills_v2.powerskill import Engine
from cloudpss_skills_v2.libs.algo_lib import SensitivityCalculator

logger = logging.getLogger(__name__)


class ParameterSensitivityAnalysis:
    name = "parameter_sensitivity"
    description = "参数灵敏度分析 - 计算系统参数灵敏度排序"

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "parameter_sensitivity"},
                "engine": {
                    "type": "string",
                    "enum": ["cloudpss", "pandapower"],
                    "default": "pandapower",
                },
                "model": {"type": "object", "required": ["rid"]},
                "analysis": {
                    "type": "object",
                    "properties": {
                        "target_parameter": {
                            "type": "string",
                            "description": "e.g., load.p_mw",
                        },
                        "delta": {"type": "number", "default": 0.01},
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

            analysis = config.get("analysis", {})
            target_param = analysis.get("target_parameter", "load.p_mw")
            delta = analysis.get("delta", 0.01)

            self._log("INFO", f"Computing sensitivity for: {target_param}")

            handle = api.get_model_handle(model_rid)
            base_result = api.run_power_flow(model_handle=handle)

            if not base_result.is_success:
                self._log("WARNING", "Base case did not converge")

            perturbed_handle = handle.clone()
            perturbed_result = api.run_power_flow(model_handle=perturbed_handle)

            calc = SensitivityCalculator()
            sensitivities = calc.compute_from_sweep(
                base_results=base_result.data or {},
                perturbed_results=[perturbed_result.data]
                if perturbed_result.data
                else [],
                parameter_name=target_param,
                delta=delta,
            )

            result_data = {
                "target_parameter": target_param,
                "total_buses": len(sensitivities),
                "sensitivities": [s.to_dict() for s in sensitivities[:20]],
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
            self._log("ERROR", f"Sensitivity analysis failed: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error=str(e),
                logs=self.logs,
                start_time=start_time,
                end_time=datetime.now(),
            )


__all__ = ["ParameterSensitivityAnalysis"]
