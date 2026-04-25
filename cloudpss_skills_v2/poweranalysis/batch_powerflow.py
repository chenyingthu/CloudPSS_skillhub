"""Batch PowerFlow Analysis - Run power flow for multiple models.

批量潮流计算 - 对多个模型进行批量潮流计算。
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any

from cloudpss_skills_v2.core.skill_result import (
    Artifact,
    SkillResult,
    SkillStatus,
)
from cloudpss_skills_v2.powerskill import Engine

logger = logging.getLogger(__name__)


class BatchPowerFlowAnalysis:
    """批量潮流计算技能 - v2 engine-agnostic implementation."""

    name = "batch_powerflow"
    description = "批量潮流计算 - 对多个模型进行批量潮流计算"

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "models"],
            "properties": {
                "skill": {"type": "string", "const": "batch_powerflow"},
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
                "models": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "rid": {"type": "string"},
                            "name": {"type": "string", "default": ""},
                            "source": {"enum": ["cloud", "local"], "default": "cloud"},
                        },
                        "required": ["rid"],
                    },
                    "description": "List of models to calculate",
                },
                "algorithm": {
                    "type": "object",
                    "properties": {
                        "type": {
                            "enum": ["newton_raphson", "fast_decoupled"],
                            "default": "newton_raphson",
                        },
                        "tolerance": {"type": "number", "default": 1e-6},
                        "max_iterations": {"type": "integer", "default": 100},
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"enum": ["json", "csv"], "default": "json"},
                        "path": {"type": "string", "default": "./results/"},
                        "prefix": {"type": "string", "default": "batch_powerflow"},
                        "timestamp": {"type": "boolean", "default": True},
                        "aggregate": {
                            "type": "boolean",
                            "default": True,
                        },
                    },
                },
            },
        }

    def get_default_config(self) -> dict[str, Any]:
        return {
            "skill": self.name,
            "engine": "pandapower",
            "auth": {"token_file": ".cloudpss_token"},
            "models": [{"rid": "case14", "name": "IEEE14", "source": "local"}],
            "algorithm": {
                "type": "newton_raphson",
                "tolerance": 1e-6,
                "max_iterations": 100,
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "batch_powerflow",
                "timestamp": True,
                "aggregate": True,
            },
        }

    def validate(self, config: dict[str, Any] | None) -> tuple[bool, list[str]]:
        errors = []
        if not isinstance(config, dict):
            errors.append("config must be a dictionary")
            return (False, errors)
        models = config.get("models", [])
        if not isinstance(models, list):
            errors.append("models must be a list")
        if len(models) == 0:
            errors.append("models cannot be empty")
        for idx, m in enumerate(models):
            if not m.get("rid"):
                errors.append(f"models[{idx}].rid is required")
        return (len(errors) == 0, errors)

    def _log(self, level: str, message: str) -> None:
        getattr(logger, level.lower(), logger.info)(message)

    def _save_output(self, data: dict[str, Any], config: dict[str, Any]) -> str:
        output_config = config.get("output", {})
        output_path = output_config.get("path", "./results/")
        prefix = output_config.get("prefix", "batch_powerflow")
        timestamp = output_config.get("timestamp", True)

        Path(output_path).mkdir(parents=True, exist_ok=True)
        fname = prefix
        if timestamp:
            fname += f"_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        fname += ".json"
        filepath = os.path.join(output_path, fname)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return filepath

    def _build_batch_result(
        self, models_config: list[dict], results: dict[str, Any]
    ) -> dict[str, Any]:
        total = len(models_config)
        completed = len([r for r in results.values() if r.get("status") == "completed"])
        failed = len([r for r in results.values() if r.get("status") == "failed"])
        return {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total": total,
                "completed": completed,
                "failed": failed,
                "success_rate": completed / total if total else 0,
            },
            "results": results,
        }

    def run(self, config: dict[str, Any]) -> SkillResult:
        start_time = datetime.now()
        logs: list[dict] = []
        artifacts: list[Artifact] = []

        valid, errors = self.validate(config)
        if not valid:
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error="; ".join(errors),
                logs=logs,
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

            models = config.get("models", [])
            self._log("INFO", f"Batch run for {len(models)} models")

            results: dict[str, Any] = {}
            for i, model_cfg in enumerate(models):
                model_rid = model_cfg.get("rid")
                self._log("INFO", f"[{i + 1}/{len(models)}] Model: {model_rid}")

                handle = api.get_model_handle(model_rid)
                sim_result = api.run_power_flow(model_handle=handle)

                results[model_rid] = {
                    "status": "completed" if sim_result.is_success else "failed",
                    "converged": sim_result.is_success,
                    "errors": sim_result.errors,
                }

                if sim_result.is_success:
                    self._log("INFO", f"  -> Converged")
                else:
                    self._log("ERROR", f"  -> Failed: {sim_result.errors}")

            output_data = self._build_batch_result(models, results)

            if config.get("output", {}):
                output_path = self._save_output(output_data, config)
                self._log("INFO", f"Results saved to: {output_path}")
                artifacts.append(
                    Artifact(
                        name="batch_results",
                        data=output_data,
                        description="Batch power flow results",
                    )
                )

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                data=output_data,
                logs=logs,
                artifacts=artifacts,
                start_time=start_time,
                end_time=datetime.now(),
            )

        except Exception as e:
            self._log("ERROR", f"Batch run failed: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error=str(e),
                logs=logs,
                start_time=start_time,
                end_time=datetime.now(),
            )


__all__ = ["BatchPowerFlowAnalysis"]
