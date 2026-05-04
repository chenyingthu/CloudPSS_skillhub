"""Result handler for portal."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from cloudpss_skills_v3.master_organizer.core import (
    CaseRegistry,
    Result,
    ResultRegistry,
    TaskRegistry,
    get_path_manager,
)
from cloudpss_skills_v3.master_organizer.core.release_ops import (
    archive_result,
    generate_result_report,
)
from cloudpss_skills_v3.master_organizer.core.csv_streaming import StreamingCSVReader

from ..schemas.result import ResultResponse, ResultSummaryResponse
from .base import BaseHandler, ResponseHelper


class ResultHandler(BaseHandler):
    """Handler for result-related operations."""

    def get(self, result_id: str) -> tuple[dict[str, Any], int]:
        """GET /api/results/{id} - Get result detail."""
        pm = get_path_manager()
        result = ResultRegistry().get(result_id)
        if not result:
            return ResponseHelper.not_found("Result", result_id)

        result_dir = pm.get_result_path(result_id)
        artifacts: dict[str, Any] = {}

        # Load JSON artifacts
        for relative_path in result.files:
            path = result_dir / relative_path
            if path.is_file() and path.suffix == ".json":
                try:
                    artifacts[relative_path] = json.loads(
                        path.read_text(encoding="utf-8")
                    )
                except json.JSONDecodeError:
                    artifacts[relative_path] = {"error": "invalid json"}

        # Load report if exists
        report_path = result_dir / "report.md"
        report = ""
        if report_path.exists():
            report = report_path.read_text(encoding="utf-8")

        # Build response with result fields at top level for API compatibility
        response_data = ResultResponse.from_model(result).to_dict()
        response_data.update({
            "directory": str(result_dir),
            "summary": self._build_summary(result_id, result, result_dir),
            "artifacts": artifacts,
            "report": report,
        })

        return ResponseHelper.success(response_data)

    def list(self, case_id: str = "", task_id: str = "", status: str = "", limit: int = 50, offset: int = 0) -> tuple[dict[str, Any], int]:
        """GET /api/results - List results with pagination (optimized)."""
        registry = ResultRegistry()

        if case_id or task_id or status:
            # Filtered query - get all matching items first
            if case_id:
                items = registry.filter_by(case_id=case_id)
            elif task_id:
                items = registry.filter_by(task_id=task_id)
            else:
                items = registry.filter_by(status=status)
            items = list(items)
            total = len(items)
            items = items[offset:offset + limit]
        else:
            # Use optimized paginated query
            items, total = registry.list_paginated(limit=limit, offset=offset, sort_by="created_at")

        results = []
        for result_id, result in items:
            result_dict = ResultResponse.from_model(result).to_dict()
            result_dict["id"] = result_id
            results.append(result_dict)

        result = ResponseHelper.paginated(results, total, limit, offset)
        return ResponseHelper.success(result)

    def summary(self, result_id: str) -> tuple[dict[str, Any], int]:
        """GET /api/results/{id}/summary - Get result summary."""
        pm = get_path_manager()
        result = ResultRegistry().get(result_id)
        if not result:
            return ResponseHelper.not_found("Result", result_id)

        result_dir = pm.get_result_path(result_id)
        summary = self._build_summary(result_id, result, result_dir)
        return ResponseHelper.success(summary)

    def report(self, result_id: str) -> tuple[dict[str, Any], int]:
        """POST /api/results/{id}/report - Generate result report."""
        try:
            path = generate_result_report(result_id)
            return ResponseHelper.success({"path": str(path)})
        except Exception as exc:
            return ResponseHelper.error(
                "REPORT_GENERATION_FAILED",
                str(exc),
                500,
            )

    def archive(self, result_id: str) -> tuple[dict[str, Any], int]:
        """POST /api/results/{id}/archive - Archive result."""
        try:
            path = archive_result(result_id)
            return ResponseHelper.success({"path": str(path)})
        except Exception as exc:
            return ResponseHelper.error(
                "ARCHIVE_FAILED",
                str(exc),
                500,
            )

    def delete(self, result_id: str) -> tuple[dict[str, Any], int]:
        """DELETE /api/results/{id} - Delete a result."""
        registry = ResultRegistry()
        result = registry.get(result_id)
        if not result:
            return ResponseHelper.not_found("Result", result_id)

        try:
            registry.delete(result_id)
            return ResponseHelper.success({"deleted": True, "id": result_id})
        except Exception as exc:
            return ResponseHelper.error(
                "DELETE_FAILED",
                str(exc),
                500,
            )

    def _build_summary(self, result_id: str, result: Result, result_dir: Path) -> dict[str, Any]:
        """Build result summary based on format."""
        summary = ResultSummaryResponse(
            format=result.format,
            metadata=result.metadata,
            files=result.files,
        )

        if result.format == "powerflow":
            buses = self._safe_read_json(result_dir / "tables" / "buses.json") or []
            branches = self._safe_read_json(result_dir / "tables" / "branches.json") or []

            summary.kind = "powerflow"
            summary.bus_rows = len(buses)
            summary.branch_rows = len(branches)
            summary.buses_preview = buses[:20]
            summary.branches_preview = branches[:20]
            summary.bus_chart = self._build_bus_chart(buses)

        elif result.format == "emt":
            channels = self._safe_read_json(result_dir / "channels.json") or []

            summary.kind = "emt"
            summary.channel_count = len(channels)
            summary.channels = channels
            summary.csv_preview = {
                item.get("csv_file", ""): self._csv_preview(result_dir / item.get("csv_file", ""))
                for item in channels[:6]
                if item.get("csv_file")
            }
            summary.series = {
                item.get("csv_file", ""): self._csv_series(result_dir / item.get("csv_file", ""))
                for item in channels[:6]
                if item.get("csv_file")
            }

        return summary.to_dict()

    def _build_bus_chart(self, rows: list[dict[str, Any]], limit: int = 120) -> dict[str, Any]:
        """Build chart data for powerflow buses."""
        if not rows:
            return {"points": []}

        keys = list(rows[0].keys())
        label_key = next(
            (k for k in keys if k.lower() in {"bus", "name", "id"}),
            keys[0],
        )
        value_key = next(
            (k for k in keys if k.lower() in {"v", "vm", "voltage", "u"}),
            None,
        )

        if not value_key:
            for key in keys:
                if key == label_key:
                    continue
                try:
                    float(rows[0].get(key))
                    value_key = key
                    break
                except (TypeError, ValueError):
                    continue

        if not value_key:
            return {"points": [], "label_key": label_key}

        points = []
        for index, row in enumerate(rows[:limit]):
            try:
                value = float(row.get(value_key))
                points.append({
                    "x": index,
                    "y": value,
                    "label": str(row.get(label_key, index)),
                })
            except (TypeError, ValueError):
                continue

        return {
            "points": points,
            "label_key": label_key,
            "value_key": value_key,
        }

    def _safe_read_json(self, path: Path) -> Any:
        """Safely read JSON file."""
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None

    def _csv_preview(self, path: Path, limit: int = 12) -> dict[str, Any]:
        """Preview CSV file contents using streaming for memory efficiency."""
        reader = StreamingCSVReader(path)
        preview = reader.preview(limit)

        return {
            "headers": preview.headers,
            "rows": preview.rows,
            "path": preview.path,
            "total_lines": preview.total_lines,
            "error": preview.error,
        }

    def _csv_series(self, path: Path, limit: int = 240) -> dict[str, Any]:
        """Extract time series data from CSV using streaming."""
        reader = StreamingCSVReader(path)
        data = reader.extract_time_series(x_column="time", y_column="value", limit=limit)

        return {
            "points": [{"x": p.x, "y": p.y} for p in data.points],
            "path": data.path,
            "total_points": data.total_points,
            "error": data.error,
        }
