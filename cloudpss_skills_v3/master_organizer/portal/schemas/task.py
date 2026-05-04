"""Task DTO classes."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from cloudpss_skills_v3.master_organizer.core.models import Task


@dataclass
class TaskCreate:
    """Request to create a new task."""

    case_id: str
    name: str = ""
    type: str = "powerflow"  # powerflow, emt, stability
    config: dict[str, Any] = field(default_factory=dict)
    channels: list[str] = field(default_factory=list)
    model_source: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate required fields."""
        if not self.case_id or not self.case_id.strip():
            raise ValueError("case_id is required")
        if not self.name:
            self.name = f"{self.type} task"
        if self.type not in {"powerflow", "emt", "stability"}:
            raise ValueError("task type must be powerflow, emt, or stability")

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "case_id": self.case_id.strip(),
            "name": self.name,
            "type": self.type,
            "config": self.config,
            "channels": self.channels,
            "model_source": self.model_source,
        }


@dataclass
class TaskUpdate:
    """Request to update a task."""

    name: Optional[str] = None
    type: Optional[str] = None
    config: Optional[dict[str, Any]] = None
    channels: Optional[list[str]] = None
    model_source: Optional[str] = None

    def validate(self) -> None:
        """Validate update fields."""
        if self.name is not None and not self.name.strip():
            raise ValueError("name cannot be empty")
        if self.type is not None and self.type not in {"powerflow", "emt", "stability"}:
            raise ValueError("task type must be powerflow, emt, or stability")

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary with only set fields."""
        result: dict[str, Any] = {}
        if self.name is not None:
            result["name"] = self.name.strip()
        if self.type is not None:
            result["type"] = self.type
        if self.config is not None:
            result["config"] = self.config
        if self.channels is not None:
            result["channels"] = self.channels
        if self.model_source is not None:
            result["model_source"] = self.model_source
        return result


@dataclass
class TaskRunRequest:
    """Request to run a task."""

    timeout: int = 300

    def __post_init__(self) -> None:
        """Validate timeout."""
        if self.timeout < 1:
            raise ValueError("timeout must be positive")
        if self.timeout > 3600:
            raise ValueError("timeout cannot exceed 3600 seconds")


@dataclass
class TaskResponse:
    """Task response data."""

    id: str
    name: str
    case_id: str
    variant_id: Optional[str]
    type: str
    job_id: Optional[str]
    server_id: str
    status: str
    result_id: Optional[str]
    config: dict[str, Any]
    created_at: str
    submitted_at: Optional[str]
    started_at: Optional[str]
    completed_at: Optional[str]

    @classmethod
    def from_model(cls, task: Task) -> "TaskResponse":
        """Create response from Task model."""
        return cls(
            id=task.id,
            name=task.name,
            case_id=task.case_id,
            variant_id=task.variant_id,
            type=task.type,
            job_id=task.job_id,
            server_id=task.server_id,
            status=task.status,
            result_id=task.result_id,
            config=task.config,
            created_at=task.created_at,
            submitted_at=task.submitted_at,
            started_at=task.started_at,
            completed_at=task.completed_at,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "case_id": self.case_id,
            "variant_id": self.variant_id,
            "type": self.type,
            "job_id": self.job_id,
            "server_id": self.server_id,
            "status": self.status,
            "result_id": self.result_id,
            "config": self.config,
            "created_at": self.created_at,
            "submitted_at": self.submitted_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
        }


@dataclass
class TaskPreflightResponse:
    """Task preflight check response."""

    ok: bool
    checks: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "ok": self.ok,
            "checks": self.checks,
        }
