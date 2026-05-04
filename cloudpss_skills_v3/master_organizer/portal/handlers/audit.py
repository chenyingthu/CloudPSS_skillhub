"""Audit handler for portal."""

from __future__ import annotations

import json
from typing import Any

from cloudpss_skills_v3.master_organizer.core import get_path_manager

from .base import BaseHandler, ResponseHelper


class AuditHandler(BaseHandler):
    """Handler for audit log operations."""

    def list(self, limit: int = 80) -> tuple[dict[str, Any], int]:
        """GET /api/audit - Get audit log entries."""
        audit_path = get_path_manager().logs_dir / "audit.log"

        if not audit_path.exists():
            return ResponseHelper.success({"entries": []})

        try:
            lines = audit_path.read_text(encoding="utf-8").splitlines()[-limit:]
            entries = []
            for line in lines:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    entries.append({"raw": line})

            return ResponseHelper.success({"entries": list(reversed(entries))})
        except Exception as exc:
            return ResponseHelper.error(
                "READ_FAILED",
                f"Failed to read audit log: {str(exc)}",
                500,
            )
