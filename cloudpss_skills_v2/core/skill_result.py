"""
SkillResult - Standard Result Container for cloudpss_skills_v2

Following the output standard defined in docs/skills/output-standard.md
"""

from __future__ import annotations
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class SkillStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Artifact:
    name: str = ""
    path: str = ""
    type: str = ""
    size_bytes: int | None = None
    description: str | None = None
    data: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            k: getattr(self, k)
            for k in ("name", "path", "type", "size_bytes", "description")
        }


@dataclass
class LogEntry:
    timestamp: datetime = field(default_factory=datetime.now)
    level: str = "info"
    message: str = ""
    context: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "level": self.level,
            "message": self.message,
            "context": self.context,
        }


@dataclass
class SkillResult:
    skill_name: str = ""
    status: SkillStatus = SkillStatus.PENDING
    data: dict[str, Any] = field(default_factory=dict)
    artifacts: list[Artifact] = field(default_factory=list)
    logs: list[LogEntry] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None

    def __post_init__(self):
        if self.end_time is None and self.start_time is not None:
            self.end_time = datetime.now()

    @property
    def is_success(self) -> bool:
        return self.status == SkillStatus.SUCCESS

    @property
    def duration_seconds(self) -> float | None:
        if self.start_time is not None and self.end_time is not None:
            return (self.end_time - self.start_time).total_seconds()
        return None

    @property
    def has_error(self) -> bool:
        return self.error is not None

    # Compatibility properties for SimulationResult naming
    @property
    def started_at(self) -> datetime | None:
        """Alias for start_time (consistent with SimulationResult)."""
        return self.start_time

    @property
    def completed_at(self) -> datetime | None:
        """Alias for end_time (consistent with SimulationResult)."""
        return self.end_time

    @property
    def job_id(self) -> str:
        """Alias for skill_name (consistent with SimulationResult)."""
        return self.skill_name

    @property
    def is_completed(self) -> bool:
        """Check if status is SUCCESS or FAILED (consistent with SimulationResult)."""
        return self.status in (SkillStatus.SUCCESS, SkillStatus.FAILED)

    def add_log(self, level: str, message: str, context: dict[str, Any] | None = None):
        self.logs.append(
            LogEntry(
                timestamp=datetime.now(),
                level=level,
                message=message,
                context=context,
            )
        )

    def add_artifact(
        self,
        name: str,
        path: str,
        type_: str | None = None,
        size_bytes: int | None = None,
        description: str | None = None,
    ):
        self.artifacts.append(
            Artifact(
                name=name,
                path=path,
                type=type_ or "",
                size_bytes=size_bytes,
                description=description,
            )
        )

    def to_dict(self) -> dict[str, Any]:
        def artifact_to_dict(artifact: Artifact | dict[str, Any]) -> dict[str, Any]:
            if hasattr(artifact, "to_dict"):
                return artifact.to_dict()
            if isinstance(artifact, dict):
                return artifact
            return {"name": str(artifact)}

        def log_to_dict(log: LogEntry | dict[str, Any]) -> dict[str, Any]:
            if hasattr(log, "to_dict"):
                return log.to_dict()
            if isinstance(log, dict):
                return log
            return {"message": str(log)}

        return {
            "skill_name": self.skill_name,
            "status": self.status.value,
            "success": self.is_success,
            "data": self.data,
            "artifacts": [artifact_to_dict(a) for a in self.artifacts],
            "logs": [log_to_dict(l) for l in self.logs],
            "metrics": self.metrics,
            "error": self.error,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_seconds": self.duration_seconds,
        }

    @classmethod
    def success(
        cls,
        skill_name: str,
        data: dict[str, Any] | None = None,
        artifacts: list[Artifact] | None = None,
        logs: list[LogEntry] | None = None,
        metrics: dict[str, Any] | None = None,
    ) -> SkillResult:
        now = datetime.now()
        return cls(
            skill_name=skill_name,
            status=SkillStatus.SUCCESS,
            data=data or {},
            artifacts=artifacts or [],
            logs=logs or [],
            metrics=metrics or {},
            start_time=now,
            end_time=now,
        )

    @classmethod
    def failure(
        cls,
        skill_name: str,
        error: str,
        data: dict[str, Any] | None = None,
        stage: str | None = None,
    ) -> SkillResult:
        now = datetime.now()
        result_data = data or {}
        if stage:
            result_data["stage"] = stage
        return cls(
            skill_name=skill_name,
            status=SkillStatus.FAILED,
            data=result_data,
            error=error,
            start_time=now,
            end_time=now,
        )

    @classmethod
    def running(
        cls, skill_name: str, data: dict[str, Any] | None = None
    ) -> SkillResult:
        return cls(
            skill_name=skill_name,
            status=SkillStatus.RUNNING,
            data=data or {},
            start_time=datetime.now(),
        )

    def to_simulation_result_dict(self) -> dict[str, Any]:
        """Convert to SimulationResult-compatible dictionary format.

        This method provides a dictionary that matches the SimulationResult.to_dict()
        format for interoperability between PowerSkill and PowerAPI layers.
        """
        # Map SkillStatus to SimulationStatus string values
        status_map = {
            "pending": "pending",
            "running": "running",
            "success": "completed",
            "failed": "failed",
            "cancelled": "cancelled",
        }
        status_value = status_map.get(self.status.value if self.status else "", None)

        return {
            "job_id": self.skill_name,
            "status": status_value,
            "data": self.data,
            "metadata": self.metrics,
            "errors": [self.error] if self.error else [],
            "warnings": [],
            "started_at": self.start_time.isoformat() if self.start_time else None,
            "completed_at": self.end_time.isoformat() if self.end_time else None,
            "duration_seconds": self.duration_seconds,
            # Consistent naming
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "skill_name": self.skill_name,
            "success": self.is_success,
        }


FIELD_NAME_MAPPING = {
    "busCount": "bus_count",
    "branchCount": "branch_count",
    "genCount": "generator_count",
    "generatorCount": "generator_count",
    "totalLoss": "total_loss",
    "passRate": "pass_rate",
    "isConverged": "converged",
    "pMW": "p_mw",
    "qMVar": "q_mvar",
    "voltagePu": "voltage_pu",
    "Vpu": "voltage_pu",
    "loadingPct": "loading_pct",
    "loadPercent": "loading_pct",
}


def normalize_field_name(name: str) -> str:
    if name in FIELD_NAME_MAPPING:
        return FIELD_NAME_MAPPING[name]
    result = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    result = re.sub(r"([a-z])([A-Z])", r"\1_\2", result)
    return result.lower().strip("_")


def normalize_data(data: dict[str, Any]) -> dict[str, Any]:
    result = {}
    for key, value in data.items():
        normalized_key = normalize_field_name(key)
        if isinstance(value, dict):
            result[normalized_key] = normalize_data(value)
        elif isinstance(value, list):
            result[normalized_key] = [
                normalize_data(v) if isinstance(v, dict) else v for v in value
            ]
        else:
            result[normalized_key] = value
    return result
