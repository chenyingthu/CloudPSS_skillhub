"""Case DTO classes."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from cloudpss_skills_v3.master_organizer.core.models import Case


@dataclass
class CaseCreate:
    """Request to create a new case."""

    name: str
    rid: str
    model_source: Optional[str] = None
    tags: list[str] = field(default_factory=list)
    description: str = ""
    server_id: str = ""

    def __post_init__(self) -> None:
        """Validate required fields."""
        if not self.name or not self.name.strip():
            raise ValueError("name is required")
        if not self.rid or not self.rid.strip():
            raise ValueError("rid is required")
        if not self.rid.startswith("model/") or len(self.rid.split("/")) < 3:
            raise ValueError("CloudPSS RID format incorrect, should be like model/chenying/IEEE39")

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name.strip(),
            "rid": self.rid.strip(),
            "model_source": self.model_source,
            "tags": self.tags,
            "description": self.description,
            "server_id": self.server_id,
        }


@dataclass
class CaseUpdate:
    """Request to update a case."""

    name: Optional[str] = None
    rid: Optional[str] = None
    model_source: Optional[str] = None
    tags: Optional[list[str]] = None
    description: Optional[str] = None
    server_id: Optional[str] = None
    status: Optional[str] = None

    def validate(self) -> None:
        """Validate update fields."""
        if self.name is not None and not self.name.strip():
            raise ValueError("name cannot be empty")
        if self.rid is not None:
            if not self.rid.startswith("model/") or len(self.rid.split("/")) < 3:
                raise ValueError("CloudPSS RID format incorrect")

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary with only set fields."""
        result: dict[str, Any] = {}
        if self.name is not None:
            result["name"] = self.name.strip()
        if self.rid is not None:
            result["rid"] = self.rid.strip()
        if self.model_source is not None:
            result["model_source"] = self.model_source
        if self.tags is not None:
            result["tags"] = self.tags
        if self.description is not None:
            result["description"] = self.description
        if self.server_id is not None:
            result["server_id"] = self.server_id
        if self.status is not None:
            result["status"] = self.status
        return result


@dataclass
class CaseResponse:
    """Case response data."""

    id: str
    name: str
    rid: str
    description: str
    server_id: str
    status: str
    tags: list[str]
    task_count: int
    last_task_id: Optional[str]
    created_at: str
    updated_at: str
    model_source: Optional[str] = None

    @classmethod
    def from_model(cls, case: Case, **kwargs: Any) -> "CaseResponse":
        """Create response from Case model."""
        return cls(
            id=case.id,
            name=case.name,
            rid=case.rid,
            description=case.description,
            server_id=case.server_id,
            status=case.status,
            tags=case.tags,
            task_count=getattr(case, "task_count", 0),
            last_task_id=getattr(case, "last_task_id", None),
            created_at=case.created_at,
            updated_at=case.updated_at,
            **kwargs,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "rid": self.rid,
            "description": self.description,
            "server_id": self.server_id,
            "status": self.status,
            "tags": self.tags,
            "task_count": self.task_count,
            "last_task_id": self.last_task_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "model_source": self.model_source,
        }
