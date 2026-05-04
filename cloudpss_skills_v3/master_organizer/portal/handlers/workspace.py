"""Workspace handler for portal."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

from cloudpss_skills_v3.master_organizer.core import (
    CaseRegistry,
    ResultRegistry,
    ServerRegistry,
    TaskRegistry,
    VariantRegistry,
    get_path_manager,
)
from cloudpss_skills_v3.master_organizer.core.config_manager import get_config_manager
from cloudpss_skills_v3.master_organizer.core.release_ops import check_workspace_quotas

from .base import BaseHandler, ResponseHelper


def _plain(value: Any) -> Any:
    """Convert dataclass or complex types to plain Python types."""
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, list):
        return [_plain(item) for item in value]
    if isinstance(value, dict):
        return {key: _plain(item) for key, item in value.items()}
    return value


def _with_id(items: list[tuple[str, Any]]) -> list[dict[str, Any]]:
    """Convert list of (id, entity) tuples to list of dicts with id field."""
    rows = []
    for entity_id, entity in items:
        row = _plain(entity)
        if isinstance(row, dict):
            row["id"] = entity_id
        rows.append(row)
    return rows


def _public_server(server: dict[str, Any]) -> dict[str, Any]:
    """Return server metadata safe for the browser API."""
    public = dict(server)
    auth = dict(public.get("auth") or {})
    if "encrypted_token" in auth:
        auth["encrypted_token"] = "<redacted>"
        auth["has_encrypted_token"] = True
    public["auth"] = auth
    return public


class WorkspaceHandler(BaseHandler):
    """Handler for workspace-related operations."""

    def snapshot(self) -> tuple[dict[str, Any], int]:
        """GET /api/snapshot - Get full workspace snapshot."""
        return ResponseHelper.success(self._get_snapshot())

    def health(self) -> tuple[dict[str, Any], int]:
        """GET /api/health - Get workspace health status."""
        pm = get_path_manager()
        from cloudpss_skills_v3.master_organizer.core.release_ops import refresh_index

        index_path = refresh_index()
        config = get_config_manager().get_user_config()

        quota_status: dict[str, Any] = {"ok": True, "message": "正常"}
        try:
            check_workspace_quotas()
        except Exception as exc:
            quota_status = {"ok": False, "message": str(exc)}

        return ResponseHelper.success({
            "summary": self._get_summary(),
            "index_path": str(index_path),
            "quotas": _plain(config.quotas),
            "audit": self._get_audit_entries(20),
        })

    def _get_summary(self) -> dict[str, Any]:
        """Get workspace summary."""
        pm = get_path_manager()
        servers = ServerRegistry()
        cases = CaseRegistry()
        tasks = TaskRegistry()
        results = ResultRegistry()
        variants = VariantRegistry()
        usage = pm.get_storage_usage()

        quota_status: dict[str, Any] = {"ok": True, "message": "正常"}
        try:
            check_workspace_quotas()
        except Exception as exc:
            quota_status = {"ok": False, "message": str(exc)}

        return {
            "root": str(pm.root),
            "counts": {
                "servers": servers.count(),
                "cases": cases.count(),
                "tasks": tasks.count(),
                "results": results.count(),
                "variants": variants.count(),
            },
            "storage": {
                "total_bytes": usage.get("total", 0),
                "total_mb": round(usage.get("total", 0) / (1024 * 1024), 3),
                "by_dir": usage,
            },
            "quota": quota_status,
        }

    def _get_snapshot(self) -> dict[str, Any]:
        """Get full organizer snapshot."""
        servers = [_public_server(s) for s in _with_id(ServerRegistry().list_all())]
        cases = _with_id(CaseRegistry().list_all())
        tasks = _with_id(TaskRegistry().list_all())
        results = _with_id(ResultRegistry().list_all())
        variants = _with_id(VariantRegistry().list_all())

        # Build relationships
        tasks_by_case: dict[str, list[dict[str, Any]]] = {}
        variants_by_case: dict[str, list[dict[str, Any]]] = {}
        results_by_task: dict[str, list[dict[str, Any]]] = {}

        for task in tasks:
            case_id = task.get("case_id")
            if case_id:
                tasks_by_case.setdefault(case_id, []).append(task)

        for variant in variants:
            case_id = variant.get("case_id")
            if case_id:
                variants_by_case.setdefault(case_id, []).append(variant)

        for result in results:
            task_id = result.get("task_id")
            if task_id:
                results_by_task.setdefault(task_id, []).append(result)

        # Get recent items
        recent_tasks = sorted(
            tasks,
            key=lambda item: item.get("created_at", ""),
            reverse=True,
        )[:8]
        recent_results = sorted(
            results,
            key=lambda item: item.get("created_at", ""),
            reverse=True,
        )[:8]

        return {
            "workspace": self._get_summary(),
            "servers": servers,
            "cases": cases,
            "tasks": tasks,
            "results": results,
            "variants": variants,
            "tasks_by_case": tasks_by_case,
            "variants_by_case": variants_by_case,
            "results_by_task": results_by_task,
            "recent_tasks": recent_tasks,
            "recent_results": recent_results,
        }

    def _get_audit_entries(self, limit: int) -> list[dict[str, Any]]:
        """Get recent audit log entries."""
        import json

        audit_path = get_path_manager().logs_dir / "audit.log"
        if not audit_path.exists():
            return []

        lines = audit_path.read_text(encoding="utf-8").splitlines()[-limit:]
        entries = []
        for line in lines:
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                entries.append({"raw": line})
        return list(reversed(entries))
