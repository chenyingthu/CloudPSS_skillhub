"""Result artifact storage for the master organizer."""

import csv
import json
from pathlib import Path
from typing import Any

from .path_manager import get_path_manager


def table_to_rows(table: dict[str, Any]) -> list[dict[str, Any]]:
    """Convert a CloudPSS columnar table payload into row dictionaries."""
    columns = table.get("data", {}).get("columns", [])
    labels = [
        column.get("name") or column.get("title") or f"col_{index}"
        for index, column in enumerate(columns)
    ]
    row_count = len(columns[0].get("data", [])) if columns else 0
    rows = []
    for row_index in range(row_count):
        row = {}
        for label, column in zip(labels, columns):
            values = column.get("data", [])
            row[label] = values[row_index] if row_index < len(values) else None
        rows.append(row)
    return rows


def write_json(path: Path, data: Any) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return path.stat().st_size


def write_rows_csv(path: Path, rows: list[dict[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path.stat().st_size


def store_powerflow_result(
    result_id: str,
    *,
    buses_table: dict[str, Any],
    branches_table: dict[str, Any],
    metadata: dict[str, Any],
    root_dir: Path | None = None,
) -> tuple[list[str], int, dict[str, Any]]:
    """Persist CloudPSS power-flow result tables under results/<result_id>."""
    result_dir = root_dir or get_path_manager().get_result_path(result_id)
    tables_dir = result_dir / "tables"

    bus_rows = table_to_rows(buses_table)
    branch_rows = table_to_rows(branches_table)
    artifact_metadata = {
        **metadata,
        "artifact_type": "powerflow",
        "bus_rows": len(bus_rows),
        "branch_rows": len(branch_rows),
    }

    files: list[str] = []
    total_size = 0

    artifacts = [
        ("tables/buses.json", bus_rows),
        ("tables/branches.json", branch_rows),
        ("raw/buses_table.json", buses_table),
        ("raw/branches_table.json", branches_table),
    ]
    for relative_path, data in artifacts:
        total_size += write_json(result_dir / relative_path, data)
        files.append(relative_path)

    total_size += write_rows_csv(tables_dir / "buses.csv", bus_rows)
    files.append("tables/buses.csv")
    total_size += write_rows_csv(tables_dir / "branches.csv", branch_rows)
    files.append("tables/branches.csv")

    manifest = {
        "result_id": result_id,
        "format": "powerflow",
        "metadata": artifact_metadata,
        "files": files,
    }
    total_size += write_json(result_dir / "manifest.json", manifest)
    files.append("manifest.json")
    return files, total_size, artifact_metadata
