"""Result DTO classes."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from cloudpss_skills_v3.master_organizer.core.models import Result


@dataclass
class ResultResponse:
    """Result response data."""

    id: str
    name: str
    task_id: str
    case_id: str
    format: str
    status: str
    success: bool
    created_at: str
    size_bytes: int
    files: list[str]
    metadata: dict[str, Any]
    output: dict[str, Any]
    metrics: dict[str, Any]
    export_format: Optional[str]
    export_path: Optional[str]
    exported_at: Optional[str]

    @classmethod
    def from_model(cls, result: Result) -> "ResultResponse":
        """Create response from Result model."""
        return cls(
            id=result.id,
            name=result.name,
            task_id=result.task_id,
            case_id=result.case_id,
            format=result.format,
            status=result.status,
            success=result.success,
            created_at=result.created_at,
            size_bytes=result.size_bytes,
            files=result.files,
            metadata=result.metadata,
            output=result.output,
            metrics=result.metrics,
            export_format=result.export_format,
            export_path=result.export_path,
            exported_at=result.exported_at,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "task_id": self.task_id,
            "case_id": self.case_id,
            "format": self.format,
            "status": self.status,
            "success": self.success,
            "created_at": self.created_at,
            "size_bytes": self.size_bytes,
            "files": self.files,
            "metadata": self.metadata,
            "output": self.output,
            "metrics": self.metrics,
            "export_format": self.export_format,
            "export_path": self.export_path,
            "exported_at": self.exported_at,
        }


@dataclass
class ResultSummaryResponse:
    """Result summary response."""

    format: str
    metadata: dict[str, Any]
    files: list[str]
    kind: Optional[str] = None
    bus_rows: int = 0
    branch_rows: int = 0
    buses_preview: list[dict[str, Any]] = field(default_factory=list)
    branches_preview: list[dict[str, Any]] = field(default_factory=list)
    bus_chart: dict[str, Any] = field(default_factory=dict)
    channel_count: int = 0
    channels: list[dict[str, Any]] = field(default_factory=list)
    csv_preview: dict[str, Any] = field(default_factory=dict)
    series: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        result: dict[str, Any] = {
            "format": self.format,
            "metadata": self.metadata,
            "files": self.files,
        }
        if self.kind:
            result["kind"] = self.kind
        if self.format == "powerflow":
            result.update({
                "bus_rows": self.bus_rows,
                "branch_rows": self.branch_rows,
                "buses_preview": self.buses_preview,
                "branches_preview": self.branches_preview,
                "bus_chart": self.bus_chart,
            })
        elif self.format == "emt":
            result.update({
                "channel_count": self.channel_count,
                "channels": self.channels,
                "csv_preview": self.csv_preview,
                "series": self.series,
            })
        return result


@dataclass
class ResultReportResponse:
    """Result report generation response."""

    path: str

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {"path": self.path}


@dataclass
class ResultArchiveResponse:
    """Result archive generation response."""

    path: str

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {"path": self.path}
