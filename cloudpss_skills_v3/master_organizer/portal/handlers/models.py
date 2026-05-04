"""Model handler for portal."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from cloudpss_skills_v3.master_organizer.core import CaseRegistry, TaskRegistry
from cloudpss_skills_v3.master_organizer.core.release_ops import write_audit
from cloudpss_skills_v3.master_organizer.core.cache import cached, get_model_cache
from cloudpss_skills_v3.master_organizer.portal.model_editor import (
    model_summary,
    save_model_edits,
)

from .base import BaseHandler, ResponseHelper


class ModelHandler(BaseHandler):
    """Handler for model editing operations."""

    def get_editor(self, case_id: str) -> tuple[dict[str, Any], int]:
        """GET /api/cases/{id}/model - Get model editor data."""
        case = CaseRegistry().get(case_id)
        if not case:
            return ResponseHelper.not_found("Case", case_id)

        model_source = self._get_model_source(case)
        if not model_source:
            return ResponseHelper.success({
                "editable": False,
                "reason": "当前 Case 使用远端 RID。请先在任务中配置本地 model_source，Portal 才能表格化编辑模型文件。",
            })

        try:
            summary = model_summary(model_source)
            return ResponseHelper.success({
                "editable": True,
                "case_id": case_id,
                "model_source": model_source,
                **summary,
            })
        except Exception as exc:
            return ResponseHelper.success({
                "editable": False,
                "path": model_source,
                "reason": str(exc),
            })

    def save_edits(self, payload: dict[str, Any]) -> tuple[dict[str, Any], int]:
        """POST /api/models/edits - Save model table edits."""
        case_id = str(payload.get("case_id", "")).strip()
        path = str(payload.get("path", "")).strip()
        updates = payload.get("updates") or []

        if not case_id:
            return ResponseHelper.validation_error("case_id is required")
        if not path:
            return ResponseHelper.validation_error("path is required")
        if not isinstance(updates, list):
            return ResponseHelper.validation_error("updates must be a list")

        case = CaseRegistry().get(case_id)
        if not case:
            return ResponseHelper.not_found("Case", case_id)

        # Verify path matches case's model source
        tasks = self._with_id(TaskRegistry().filter_by(case_id=case_id))
        expected_path = self._get_model_source(case, tasks)

        if not expected_path:
            return ResponseHelper.error(
                "NO_MODEL_SOURCE",
                "Case 未绑定本地模型源，不能保存模型修改",
                422,
            )

        requested_path = Path(path).expanduser().resolve()
        bound_path = Path(expected_path).expanduser().resolve()

        if requested_path != bound_path:
            return ResponseHelper.error(
                "PATH_MISMATCH",
                "模型保存路径必须匹配当前 Case 绑定的本地模型源",
                422,
            )

        # Save edits
        try:
            result = save_model_edits(path, updates)
            write_audit(
                "portal.model.update",
                result["path"],
                {"changed": result["changed"], "backup": result["backup_path"]},
            )
            return ResponseHelper.success(result)
        except Exception as exc:
            return ResponseHelper.error(
                "SAVE_FAILED",
                str(exc),
                500,
            )

    def _get_model_source(
        self,
        case: Any,
        tasks: list[dict[str, Any]] | None = None,
    ) -> str:
        """Extract model source from case."""
        import json

        # Try to get from case description
        try:
            value = json.loads(case.description or "{}")
            if isinstance(value, dict):
                model_source = value.get("model_source", "")
                if model_source:
                    return str(model_source)
        except json.JSONDecodeError:
            pass

        # Try to get from tasks
        if tasks is None:
            tasks = self._with_id(TaskRegistry().filter_by(case_id=case.id))

        for task in tasks:
            config = task.get("config") or {}
            source = config.get("model_source")
            if source:
                return str(source)

        return ""

    def _with_id(self, items: list[tuple[str, Any]]) -> list[dict[str, Any]]:
        """Convert list of (id, entity) to list of dicts with id."""
        from dataclasses import asdict
        rows = []
        for entity_id, entity in items:
            row = asdict(entity) if hasattr(entity, "__dataclass_fields__") else dict(entity)
            row["id"] = entity_id
            rows.append(row)
        return rows

    # Model API methods
    @cached(cache=get_model_cache(), ttl=600)
    def _fetch_model_summary_cached(self, rid: str) -> dict[str, Any] | None:
        """Cached model summary fetch."""
        from cloudpss_skills_v3.master_organizer.core.model_utils import fetch_model_summary
        return fetch_model_summary(rid)

    def get_summary(self, rid: str) -> tuple[dict[str, Any], int]:
        """GET /api/models/{rid}/summary - Get model summary."""
        try:
            summary = self._fetch_model_summary_cached(rid)
            if summary is None:
                return ResponseHelper.not_found("Model", rid)
            return ResponseHelper.success(summary)
        except Exception as exc:
            return ResponseHelper.error(
                "FETCH_FAILED",
                str(exc),
                500,
            )

    def get_parameters(self, rid: str, component: str = "") -> tuple[dict[str, Any], int]:
        """GET /api/models/{rid}/parameters - Get model parameters."""
        from cloudpss_skills_v3.master_organizer.core.model_utils import fetch_model_parameters

        try:
            params = fetch_model_parameters(rid, component)
            return ResponseHelper.success(params)
        except Exception as exc:
            return ResponseHelper.error(
                "FETCH_FAILED",
                str(exc),
                500,
            )

    def list_available(self) -> tuple[dict[str, Any], int]:
        """GET /api/models/available - List available models."""
        from cloudpss_skills_v3.master_organizer.core.model_utils import list_available_models

        try:
            models = list_available_models()
            return ResponseHelper.success({"models": models})
        except Exception as exc:
            return ResponseHelper.error(
                "LIST_FAILED",
                str(exc),
                500,
            )

    def validate_rid(self, rid: str) -> tuple[dict[str, Any], int]:
        """GET /api/models/validate - Validate RID format."""
        from cloudpss_skills_v3.master_organizer.core.model_utils import validate_rid

        try:
            result = validate_rid(rid)
            return ResponseHelper.success(result)
        except Exception as exc:
            return ResponseHelper.error(
                "VALIDATION_FAILED",
                str(exc),
                500,
            )
