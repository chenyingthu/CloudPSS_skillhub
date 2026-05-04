"""Common DTO classes."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class Pagination:
    """Pagination information."""

    total: int
    limit: int
    offset: int
    has_more: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "total": self.total,
            "limit": self.limit,
            "offset": self.offset,
            "has_more": self.has_more,
        }


@dataclass
class BaseResponse:
    """Base response wrapper."""

    data: dict[str, Any] | list[dict[str, Any]] | None = None
    pagination: Pagination | None = None
    error: ErrorResponse | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        result: dict[str, Any] = {}
        if self.data is not None:
            result["data"] = self.data
        if self.pagination is not None:
            result["pagination"] = self.pagination.to_dict()
        if self.error is not None:
            result["error"] = self.error.to_dict()
        return result


@dataclass
class ErrorResponse:
    """Error response."""

    code: str
    message: str
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "code": self.code,
            "message": self.message,
            "details": self.details,
        }


@dataclass
class WorkspaceSnapshot:
    """Workspace snapshot response."""

    root: str
    counts: dict[str, int]
    storage: dict[str, Any]
    quota: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "root": self.root,
            "counts": self.counts,
            "storage": self.storage,
            "quota": self.quota,
        }
