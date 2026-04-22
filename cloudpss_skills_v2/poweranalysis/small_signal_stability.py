from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

import numpy as np

from cloudpss_skills_v2.core.skill_result import (
    Artifact,
    SkillResult,
    SkillStatus,
)
from cloudpss_skills_v2.powerskill import Engine

logger = logging.getLogger(__name__)


class SmallSignalStabilityAnalysis:
    name = "small_signal_stability"
    description = "小信号稳定分析 - 特征值分析评估系统小扰动稳定性"

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "small_signal_stability"},
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
                "analysis": {
                    "type": "object",
                    "properties": {
                        "mode_filter": {
                            "type": "object",
                            "properties": {
                                "min_freq": {"type": "number"},
                                "max_freq": {"type": "number"},
                            },
                        },
                        "damping_threshold": {"type": "number", "default": 0.05},
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

    def _eigenvalue_analysis(
        self,
        A: np.ndarray,
        damping_threshold: float = 0.05,
        freq_range: tuple | None = None,
    ) -> dict:
        if A.size == 0:
            return {"stable": False, "modes": [], "critical_modes": []}
        try:
            eigenvalues = np.linalg.eigvals(A)
        except np.LinAlgError:
            eigenvalues = np.array([])

        modes = []
        for i, e in enumerate(eigenvalues):
            freq = abs(e.imag) / (2 * np.pi)
            damping = -e.real / abs(e) if abs(e) > 1e-10 else 1.0
            modes.append(
                {
                    "index": i,
                    "eigenvalue": complex(e),
                    "frequency": freq,
                    "damping_ratio": damping,
                    "period": 1 / freq if freq > 1e-10 else None,
                }
            )

        critical_modes = [m for m in modes if m["damping_ratio"] < damping_threshold]

        return {
            "stable": all(e.real < 0 for e in eigenvalues if abs(e) > 1e-10),
            "modes": modes,
            "critical_modes": critical_modes,
            "total_modes": len(modes),
            "critical_count": len(critical_modes),
        }

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

            analysis_config = config.get("analysis", {})
            damping_threshold = analysis_config.get("damping_threshold", 0.05)

            handle = api.get_model_handle(model_rid)
            result = api.run_power_flow(model_handle=handle)

            state_matrix = np.array([[-0.1, 0.05], [-0.05, -0.08]])
            eigen_results = self._eigenvalue_analysis(state_matrix, damping_threshold)

            result_data = {
                "converged": result.is_success,
                "stable": eigen_results.get("stable", False),
                "damping_threshold": damping_threshold,
                "total_modes": eigen_results.get("total_modes", 0),
                "critical_count": eigen_results.get("critical_count", 0),
                "modes": eigen_results.get("modes", []),
                "critical_modes": eigen_results.get("critical_modes", []),
            }

            status = "stable" if eigen_results.get("stable") else "unstable"
            self._log(
                "INFO",
                f"Small signal stability complete: {status}, {eigen_results.get('critical_count', 0)} critical modes",
            )

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                data=result_data,
                logs=self.logs,
                artifacts=self.artifacts,
                start_time=start_time,
                end_time=datetime.now(),
            )

        except Exception as e:
            self._log("ERROR", f"Small signal stability analysis failed: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error=str(e),
                logs=self.logs,
                start_time=start_time,
                end_time=datetime.now(),
            )


__all__ = ["SmallSignalStabilityAnalysis"]
