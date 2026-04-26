"""Config batch runner tool."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from cloudpss_skills_v2.core import SkillResult, SkillStatus


@dataclass
class ConfigRunResult:
    config_name: str = ""
    status: str = "pending"
    result: Any = None
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "config_name": self.config_name,
            "status": self.status,
            "result": self.result,
            "error": self.error,
        }


class ConfigBatchRunnerTool:
    name = "config_batch_runner"

    def __init__(self):
        self.logs = []
        self.artifacts = []

    def validate(self, config: dict[str, Any] | None = None) -> tuple[bool, list[str]]:
        errors = []
        if not isinstance(config, dict):
            return False, ["config is required"]
        configs = config.get("configs")
        if not isinstance(configs, list) or not configs:
            errors.append("configs must be a non-empty list")
        else:
            for index, item in enumerate(configs):
                if not isinstance(item, dict):
                    errors.append(f"configs[{index}] must be an object")
                    continue
                if not item.get("name"):
                    errors.append(f"configs[{index}].name is required")
                if "config" not in item:
                    errors.append(f"configs[{index}].config is required")
        return (len(errors) == 0, errors)

    def run(self, config: dict[str, Any] | None = None) -> SkillResult:
        start_time = datetime.now()
        config = config or {}
        valid, errors = self.validate(config)
        if not valid:
            return SkillResult.failure(
                skill_name=self.name,
                error="; ".join(errors),
                data={"stage": "validation", "errors": errors},
            )

        results = []
        for item in config["configs"]:
            name = str(item["name"])
            payload = item.get("config", {})
            try:
                if callable(config.get("runner")):
                    value = config["runner"](payload)
                else:
                    value = payload
                results.append(
                    ConfigRunResult(
                        config_name=name,
                        status="completed",
                        result=value,
                    )
                )
            except Exception as exc:
                results.append(
                    ConfigRunResult(
                        config_name=name,
                        status="failed",
                        error=str(exc),
                    )
                )

        failed = len([item for item in results if item.status == "failed"])
        return SkillResult(
            skill_name=self.name,
            status=SkillStatus.SUCCESS if failed == 0 else SkillStatus.FAILED,
            data={
                "total_configs": len(results),
                "completed": len(results) - failed,
                "failed": failed,
                "results": [item.to_dict() for item in results],
            },
            metrics={"total_configs": len(results), "failed": failed},
            error=None if failed == 0 else "One or more configs failed",
            start_time=start_time,
            end_time=datetime.now(),
        )


__all__ = ["ConfigBatchRunnerTool", "ConfigRunResult"]
