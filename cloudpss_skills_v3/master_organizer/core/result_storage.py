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


def trace_to_rows(trace: dict[str, Any]) -> list[dict[str, Any]]:
    """Convert an EMT trace with x/y vectors into CSV-friendly rows."""
    xs = trace.get("x", [])
    ys = trace.get("y", [])
    return [
        {"time": x, "value": ys[index] if index < len(ys) else None}
        for index, x in enumerate(xs)
    ]


def safe_artifact_name(value: str) -> str:
    safe = []
    for char in value:
        safe.append(char if char.isalnum() or char in ("-", "_") else "_")
    return "".join(safe).strip("_") or "channel"


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


def store_emt_result(
    result_id: str,
    *,
    plots: list[dict[str, Any]],
    traces: dict[str, dict[str, Any]],
    metadata: dict[str, Any],
    root_dir: Path | None = None,
) -> tuple[list[str], int, dict[str, Any]]:
    """Persist CloudPSS EMT plot/channel traces under results/<result_id>."""
    result_dir = root_dir or get_path_manager().get_result_path(result_id)
    channels_dir = result_dir / "channels"
    csv_dir = result_dir / "csv"

    channel_index = []
    total_points = 0
    files: list[str] = []
    total_size = 0

    for trace_key, trace in traces.items():
        rows = trace_to_rows(trace)
        total_points += len(rows)
        channel_file = f"{safe_artifact_name(trace_key)}.json"
        csv_file = f"{safe_artifact_name(trace_key)}.csv"
        total_size += write_json(channels_dir / channel_file, trace)
        files.append(f"channels/{channel_file}")
        total_size += write_rows_csv(csv_dir / csv_file, rows)
        files.append(f"csv/{csv_file}")
        channel_index.append(
            {
                "trace_key": trace_key,
                "channel_file": f"channels/{channel_file}",
                "csv_file": f"csv/{csv_file}",
                "point_count": len(rows),
            }
        )

    compact_plots = [
        {
            "index": index,
            "key": plot.get("key"),
            "name": plot.get("name"),
            "channels": [trace.get("name") for trace in plot.get("data", {}).get("traces", [])],
        }
        for index, plot in enumerate(plots)
    ]
    total_size += write_json(result_dir / "plots.json", compact_plots)
    files.append("plots.json")
    total_size += write_json(result_dir / "channels.json", channel_index)
    files.append("channels.json")

    artifact_metadata = {
        **metadata,
        "artifact_type": "emt",
        "plot_count": len(plots),
        "channel_count": len(channel_index),
        "sample_points": total_points,
    }
    manifest = {
        "result_id": result_id,
        "format": "emt",
        "metadata": artifact_metadata,
        "files": files,
    }
    total_size += write_json(result_dir / "manifest.json", manifest)
    files.append("manifest.json")
    return files, total_size, artifact_metadata
