"""Case handler for portal."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from cloudpss_skills_v3.master_organizer.core import (
    Case,
    CaseRegistry,
    EntityType,
    IDGenerator,
    ResultRegistry,
    ServerRegistry,
    TaskRegistry,
    VariantRegistry,
    get_path_manager,
)
from cloudpss_skills_v3.master_organizer.core.release_ops import (
    materialize_entity,
    refresh_index,
    write_audit,
)
from cloudpss_skills_v3.master_organizer.core.server_auth import decrypt_server_token

from ..schemas.case import CaseCreate, CaseUpdate, CaseResponse
from .base import BaseHandler, ResponseHelper


class CaseHandler(BaseHandler):
    """Handler for case-related operations."""

    def get(self, case_id: str) -> tuple[dict[str, Any], int]:
        """GET /api/cases/{id} - Get case detail."""
        case = CaseRegistry().get(case_id)
        if not case:
            return ResponseHelper.not_found("Case", case_id)

        result = self._build_case_detail(case_id, case)
        return ResponseHelper.success(result)

    def list(self, status: str = "", tag: str = "", limit: int = 50, offset: int = 0) -> tuple[dict[str, Any], int]:
        """GET /api/cases - List cases with pagination (optimized)."""
        registry = CaseRegistry()

        # Use paginated query for better performance with large datasets
        items, total = registry.list_paginated(limit=limit, offset=offset, sort_by="created_at")

        # Apply filters (on the paginated result for efficiency)
        # Note: For accurate filtering with pagination, we should filter before paginating
        # This is a simplified implementation
        if status:
            items = [(k, v) for k, v in items if v.status == status]
        if tag:
            items = [(k, v) for k, v in items if tag in v.tags]

        cases = []
        for case_id, case in items:
            case_dict = CaseResponse.from_model(case).to_dict()
            case_dict["id"] = case_id
            cases.append(case_dict)

        result = ResponseHelper.paginated(cases, total, limit, offset)
        return ResponseHelper.success(result)

    def create(self, payload: dict[str, Any]) -> tuple[dict[str, Any], int]:
        """POST /api/cases - Create a new case."""
        try:
            data = CaseCreate(
                name=payload.get("name", ""),
                rid=payload.get("rid", ""),
                model_source=payload.get("model_source"),
                tags=payload.get("tags", []),
                description=payload.get("description", ""),
                server_id=payload.get("server_id", ""),
            )
        except ValueError as exc:
            return ResponseHelper.validation_error(str(exc))

        # Get default server if not specified
        server_id = data.server_id
        if not server_id:
            servers = ServerRegistry().list_all()
            default_server = next(
                ((sid, s) for sid, s in servers if getattr(s, "default", False)),
                None,
            )
            server_id = default_server[0] if default_server else ""

        # Process tags
        tags = data.tags
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",") if t.strip()]

        # Build description with model source
        description = self._build_description(data.description, data.model_source)

        # Create case
        case_id = IDGenerator.generate(EntityType.CASE)
        case = Case(
            id=case_id,
            name=data.name,
            rid=data.rid,
            description=description,
            server_id=server_id,
            status="active",
            tags=tags,
        )

        CaseRegistry().create(case_id, case)
        materialize_entity("case", case_id, case)
        write_audit("portal.case.create", case_id, {"name": data.name, "rid": data.rid})
        refresh_index()

        return ResponseHelper.success(CaseResponse.from_model(case).to_dict(), 201)

    def update(self, case_id: str, payload: dict[str, Any]) -> tuple[dict[str, Any], int]:
        """POST /api/cases/{id} - Update a case."""
        registry = CaseRegistry()
        case = registry.get(case_id)
        if not case:
            return ResponseHelper.not_found("Case", case_id)

        try:
            data = CaseUpdate(
                name=payload.get("name"),
                rid=payload.get("rid"),
                model_source=payload.get("model_source"),
                tags=payload.get("tags"),
                description=payload.get("description"),
                server_id=payload.get("server_id"),
                status=payload.get("status"),
            )
            data.validate()
        except ValueError as exc:
            return ResponseHelper.validation_error(str(exc))

        updates = data.to_dict()

        # Handle description + model_source combination
        if "description" in payload or "model_source" in payload:
            current_desc = self._get_description_text(case.description)
            new_desc = payload.get("description", current_desc)
            new_source = payload.get("model_source", self._get_model_source(case))
            updates["description"] = self._build_description(new_desc, new_source)

        if not updates:
            return ResponseHelper.success(CaseResponse.from_model(case).to_dict())

        registry.update(case_id, updates)
        updated = registry.get(case_id)
        if updated:
            materialize_entity("case", case_id, updated)
            write_audit("portal.case.update", case_id, updates)
            refresh_index()
            return ResponseHelper.success(CaseResponse.from_model(updated).to_dict())

        return ResponseHelper.error("UPDATE_FAILED", "Failed to update case", 500)

    def preflight(self, case_id: str) -> tuple[dict[str, Any], int]:
        """GET /api/cases/{id}/preflight - Run preflight checks."""
        case = CaseRegistry().get(case_id)
        checks = []

        if not case:
            checks.append({"name": "case", "ok": False, "message": "Case 不存在"})
            return ResponseHelper.success({"ok": False, "checks": checks})

        # RID check
        rid_ok = case.rid.startswith("model/") and len(case.rid.split("/")) >= 3
        checks.append({
            "name": "CloudPSS RID",
            "ok": rid_ok,
            "message": case.rid if rid_ok else "RID 应类似 model/chenying/IEEE39",
        })

        # Server check
        server = ServerRegistry().get(case.server_id) if case.server_id else None
        checks.append({
            "name": "Server",
            "ok": server is not None,
            "message": f"{server.url} ({server.owner})" if server else "未绑定 server",
        })

        # Token check
        token_ok = False
        token_message = "未检查"
        if server:
            try:
                token_ok = bool(decrypt_server_token(server))
                token_message = "token 可解密"
            except Exception as exc:
                token_message = str(exc)
        checks.append({"name": "Token", "ok": token_ok, "message": token_message})

        # Status check
        checks.append({
            "name": "Case Status",
            "ok": case.status == "active",
            "message": case.status,
        })

        return ResponseHelper.success({
            "ok": all(c["ok"] for c in checks),
            "checks": checks,
        })

    def _build_case_detail(self, case_id: str, case: Case) -> dict[str, Any]:
        """Build detailed case response."""
        tasks = self._with_id(TaskRegistry().filter_by(case_id=case_id))
        variants = self._with_id(VariantRegistry().get_by_case(case_id))

        # Get results for tasks
        results = []
        result_registry = ResultRegistry()
        for task in tasks:
            result_id = task.get("result_id")
            if result_id:
                result = result_registry.get(result_id)
                if result:
                    from dataclasses import asdict
                    row = asdict(result)
                    row["id"] = result_id
                    results.append(row)

        return {
            "case": CaseResponse.from_model(case).to_dict(),
            "model": {
                "rid": case.rid,
                "model_source": self._get_model_source(case),
                "server_id": case.server_id,
                "server": self._get_case_server(case),
                "case_yaml": str(get_path_manager().get_case_path(case_id) / "case.yaml"),
            },
            "tasks": tasks,
            "variants": variants,
            "results": results,
        }

    def _get_model_source(self, case: Case) -> str:
        """Extract model source from case description."""
        try:
            value = json.loads(case.description or "{}")
            if isinstance(value, dict):
                return str(value.get("model_source", ""))
        except json.JSONDecodeError:
            pass
        return ""

    def _get_description_text(self, description: str) -> str:
        """Extract description text from case description."""
        try:
            value = json.loads(description or "{}")
            if isinstance(value, dict) and "description_text" in value:
                return str(value.get("description_text", ""))
        except json.JSONDecodeError:
            pass
        return description

    def _build_description(self, description: str, model_source: str) -> str:
        """Build case description with model source."""
        notes: dict[str, Any] = {}

        desc_text = description.strip()
        if desc_text:
            notes["description_text"] = desc_text

        if model_source:
            model_path = Path(model_source).expanduser().resolve()
            if not model_path.exists():
                raise ValueError(f"模型源文件不存在: {model_path}")
            notes["model_source"] = str(model_path)
        elif desc_text:
            return desc_text

        return json.dumps(notes, ensure_ascii=False, indent=2) if notes else ""

    def _get_case_server(self, case: Case) -> dict[str, Any] | None:
        """Get public server info for case."""
        server = ServerRegistry().get(case.server_id) if case.server_id else None
        if not server:
            return None

        from dataclasses import asdict
        row = asdict(server)
        row["id"] = case.server_id

        # Redact sensitive auth info
        auth = dict(row.get("auth") or {})
        if "encrypted_token" in auth:
            auth["encrypted_token"] = "<redacted>"
            auth["has_encrypted_token"] = True
        row["auth"] = auth

        return row

    def _with_id(self, items: list[tuple[str, Any]]) -> list[dict[str, Any]]:
        """Convert list of (id, entity) to list of dicts with id."""
        from dataclasses import asdict
        rows = []
        for entity_id, entity in items:
            row = asdict(entity) if hasattr(entity, "__dataclass_fields__") else dict(entity)
            row["id"] = entity_id
            rows.append(row)
        return rows
