from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from cloudpss_skills_v2.core.skill_result import (
    Artifact,
    LogEntry,
    SkillResult,
    SkillStatus,
)
from cloudpss_skills_v2.powerskill import Engine

logger = logging.getLogger(__name__)


class PresetBase:
    name: str = ""
    description: str = ""

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

    def _reset_state(self) -> None:
        self.logs = []
        self.artifacts = []

    def _failed_result(self, error: str, start_time: datetime) -> SkillResult:
        return SkillResult(
            skill_name=self.name,
            status=SkillStatus.FAILED,
            error=error,
            logs=self.logs,
            start_time=start_time,
            end_time=datetime.now(),
        )
