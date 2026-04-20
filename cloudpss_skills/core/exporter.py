"""
Exporter Module - Unified result export utilities.

Provides standardized interfaces for:
- JSON/YAML/CSV output
- Report generation (Markdown)
- Artifact tracking
- Output path management with timestamps
"""

from __future__ import annotations

import csv
import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

from cloudpss_skills.core import Artifact

logger = logging.getLogger(__name__)


class OutputFormat(Enum):
    JSON = "json"
    YAML = "yaml"
    CSV = "csv"
    MARKDOWN = "markdown"


@dataclass
class OutputConfig:
    """Configuration for output export."""

    path: str = "./results/"
    prefix: str = "output"
    format: Union[str, OutputFormat] = "json"
    timestamp: bool = True
    ensure_ascii: bool = False
    indent: int = 2

    def __post_init__(self):
        if isinstance(self.format, str):
            self.format = OutputFormat(self.format.lower())

    def get_filename(self, suffix: str = "") -> str:
        """Generate output filename with optional timestamp."""
        parts = [self.prefix]
        if suffix:
            parts.append(suffix)
        if self.timestamp:
            parts.append(datetime.now().strftime("%Y%m%d_%H%M%S"))
        return "_".join(parts)

    def get_path(self, suffix: str = "", extension: str = "") -> Path:
        """Get full output path."""
        if not extension:
            extension = self.format.value
        filename = f"{self.get_filename(suffix)}.{extension}"
        path = Path(self.path)
        path.mkdir(parents=True, exist_ok=True)
        return path / filename


@dataclass
class ExportResult:
    """Result of export operation."""

    success: bool
    filepath: Optional[Path] = None
    error: Optional[str] = None
    size: int = 0
    artifact: Optional[Artifact] = None


@dataclass
class BatchExportResult:
    """Result of batch export operations."""

    total: int = 0
    succeeded: int = 0
    failed: int = 0
    artifacts: List[Artifact] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


def save_json(
    data: Dict[str, Any],
    output_config: Optional[OutputConfig] = None,
    suffix: str = "",
    description: str = "",
) -> ExportResult:
    """
    Save data as JSON file.

    Args:
        data: Dictionary data to save
        output_config: Output configuration
        suffix: Optional suffix for filename
        description: Description for artifact tracking

    Returns:
        ExportResult with filepath and artifact info
    """
    if output_config is None:
        output_config = OutputConfig()

    try:
        filepath = output_config.get_path(suffix, "json")

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=output_config.indent,
                ensure_ascii=output_config.ensure_ascii,
            )

        size = filepath.stat().st_size

        return ExportResult(
            success=True,
            filepath=filepath,
            size=size,
            artifact=Artifact(
                type="json",
                path=str(filepath),
                size=size,
                description=description or f"JSON export: {filepath.name}",
            ),
        )

    except Exception as e:
        logger.error(f"JSON export failed: {e}")
        return ExportResult(success=False, error=str(e))


def save_csv(
    data: Union[List[Dict], List[List]],
    output_config: Optional[OutputConfig] = None,
    suffix: str = "",
    headers: Optional[List[str]] = None,
    description: str = "",
) -> ExportResult:
    """
    Save data as CSV file.

    Args:
        data: List of dicts (row-oriented) or list of lists
        output_config: Output configuration
        suffix: Optional suffix for filename
        headers: Column headers (for list-of-lists data)
        description: Description for artifact tracking

    Returns:
        ExportResult with filepath and artifact info
    """
    if output_config is None:
        output_config = OutputConfig()

    try:
        filepath = output_config.get_path(suffix, "csv")

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            if headers:
                writer.writerow(headers)

            for row in data:
                if isinstance(row, dict):
                    writer.writerow([row.get(h, "") for h in (headers or row.keys())])
                else:
                    writer.writerow(row)

        size = filepath.stat().st_size

        return ExportResult(
            success=True,
            filepath=filepath,
            size=size,
            artifact=Artifact(
                type="csv",
                path=str(filepath),
                size=size,
                description=description or f"CSV export: {filepath.name}",
            ),
        )

    except Exception as e:
        logger.error(f"CSV export failed: {e}")
        return ExportResult(success=False, error=str(e))


def generate_report(
    content: Union[str, List[str]],
    output_config: Optional[OutputConfig] = None,
    suffix: str = "report",
    description: str = "",
) -> ExportResult:
    """
    Generate Markdown report.

    Args:
        content: Report content (string or list of lines)
        output_config: Output configuration
        suffix: Optional suffix for filename
        description: Description for artifact tracking

    Returns:
        ExportResult with filepath and artifact info
    """
    if output_config is None:
        output_config = OutputConfig()

    try:
        filepath = output_config.get_path(suffix, "md")

        if isinstance(content, list):
            content = "\n".join(content)

        Path(filepath).write_text(content, encoding="utf-8")

        size = filepath.stat().st_size

        return ExportResult(
            success=True,
            filepath=filepath,
            size=size,
            artifact=Artifact(
                type="markdown",
                path=str(filepath),
                size=size,
                description=description or f"Report: {filepath.name}",
            ),
        )

    except Exception as e:
        logger.error(f"Report generation failed: {e}")
        return ExportResult(success=False, error=str(e))


def export_multiple(
    exports: List[Dict[str, Any]],
    output_config: Optional[OutputConfig] = None,
) -> BatchExportResult:
    """
    Export multiple outputs at once.

    Each export dict should have:
    - 'type': 'json' | 'csv' | 'markdown'
    - 'data': the data to export
    - 'suffix': optional filename suffix
    - 'description': optional description
    - 'headers': optional CSV headers

    Args:
        exports: List of export specifications
        output_config: Base output configuration

    Returns:
        BatchExportResult with all artifacts
    """
    if output_config is None:
        output_config = OutputConfig()

    result = BatchExportResult(total=len(exports))

    for exp in exports:
        export_type = exp.get("type", "json")
        data = exp.get("data", {})
        suffix = exp.get("suffix", "")
        description = exp.get("description", "")
        headers = exp.get("headers")

        if export_type == "json":
            export_result = save_json(data, output_config, suffix, description)
        elif export_type == "csv":
            export_result = save_csv(data, output_config, suffix, headers, description)
        elif export_type == "markdown":
            export_result = generate_report(data, output_config, suffix, description)
        else:
            result.errors.append(f"Unknown export type: {export_type}")
            continue

        if export_result.success:
            result.succeeded += 1
            if export_result.artifact:
                result.artifacts.append(export_result.artifact)
        else:
            result.failed += 1
            if export_result.error:
                result.errors.append(export_result.error)

    return result


def build_artifact(
    filepath: Union[str, Path],
    artifact_type: str = "",
    description: str = "",
    metadata: Optional[Dict[str, Any]] = None,
) -> Artifact:
    """
    Build an Artifact from a filepath.

    Args:
        filepath: Path to the file
        artifact_type: Type string (auto-detected from extension if empty)
        description: Description of the artifact
        metadata: Optional metadata dict

    Returns:
        Artifact object
    """
    filepath = Path(filepath)

    if not artifact_type:
        suffix = filepath.suffix.lower().lstrip(".")
        type_map = {
            "json": "json",
            "yaml": "yaml",
            "yml": "yaml",
            "csv": "csv",
            "md": "markdown",
            "markdown": "markdown",
            "png": "image",
            "jpg": "image",
            "jpeg": "image",
            "pdf": "pdf",
            "log": "log",
        }
        artifact_type = type_map.get(suffix, "unknown")

    size = filepath.stat().st_size if filepath.exists() else 0

    return Artifact(
        type=artifact_type,
        path=str(filepath),
        size=size,
        description=description or filepath.name,
        metadata=metadata or {},
    )


def table_to_csv(
    table_data: List[Dict],
    headers: Optional[List[str]] = None,
    output_path: Optional[Path] = None,
) -> ExportResult:
    """
    Convert CloudPSS table format to CSV.

    CloudPSS returns tables in format:
    [{'type': 'table', 'data': {'columns': [{'name': '...', 'data': [...]}]}}]

    Args:
        table_data: CloudPSS table format data
        headers: Optional header override
        output_path: Optional output path

    Returns:
        ExportResult with CSV data or file
    """
    if not table_data or len(table_data) == 0:
        return ExportResult(success=False, error="Empty table data")

    table = table_data[0]
    if not isinstance(table, dict) or table.get("type") != "table":
        return ExportResult(success=False, error="Invalid table format")

    columns = table.get("data", {}).get("columns", [])
    if not columns:
        return ExportResult(success=False, error="No columns in table")

    if headers is None:
        headers = [col.get("name", f"col_{i}") for i, col in enumerate(columns)]

    rows = []
    num_rows = len(columns[0].get("data", [])) if columns else 0
    for i in range(num_rows):
        row = [
            col.get("data", [{}])[i] if i < len(col.get("data", [])) else None
            for col in columns
        ]
        rows.append(row)

    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

        return ExportResult(
            success=True,
            filepath=output_path,
            size=output_path.stat().st_size,
        )

    return ExportResult(success=True)
