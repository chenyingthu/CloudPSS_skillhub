"""Task handler for portal."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from cloudpss_skills_v3.master_organizer.core import (
    CaseRegistry,
    EntityType,
    IDGenerator,
    Task,
    TaskRegistry,
)
from cloudpss_skills_v3.master_organizer.core.release_ops import (
    materialize_entity,
    refresh_index,
    write_audit,
)
from cloudpss_skills_v3.master_organizer.core.task_runner import execute_task

from ..schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskRunRequest
from .base import BaseHandler, ResponseHelper


class TaskHandler(BaseHandler):
    """Handler for task-related operations."""

    def get(self, task_id: str) -> tuple[dict[str, Any], int]:
        """GET /api/tasks/{id} - Get task detail."""
        task = TaskRegistry().get(task_id)
        if not task:
            return ResponseHelper.not_found("Task", task_id)

        return ResponseHelper.success(TaskResponse.from_model(task).to_dict())

    def list(self, case_id: str = "", status: str = "", limit: int = 50, offset: int = 0) -> tuple[dict[str, Any], int]:
        """GET /api/tasks - List tasks with pagination (optimized)."""
        registry = TaskRegistry()

        if case_id:
            items = registry.filter_by(case_id=case_id)
            items = list(items)
            total = len(items)
            # Manual pagination for filtered results
            items = items[offset:offset + limit]
        else:
            # Use optimized paginated query
            items, total = registry.list_paginated(limit=limit, offset=offset, sort_by="created_at")

        # Apply status filter
        if status:
            items = [(k, v) for k, v in items if v.status == status]

        tasks = []
        for task_id, task in items:
            task_dict = TaskResponse.from_model(task).to_dict()
            task_dict["id"] = task_id
            tasks.append(task_dict)

        result = ResponseHelper.paginated(tasks, total, limit, offset)
        return ResponseHelper.success(result)

    def create(self, payload: dict[str, Any]) -> tuple[dict[str, Any], int]:
        """POST /api/tasks - Create a new task."""
        try:
            data = TaskCreate(
                case_id=payload.get("case_id", ""),
                name=payload.get("name", ""),
                type=payload.get("type", "powerflow"),
                config=payload.get("config", {}),
                channels=payload.get("channels", []),
                model_source=payload.get("model_source"),
            )
        except ValueError as exc:
            return ResponseHelper.validation_error(str(exc))

        # Validate case exists
        case = CaseRegistry().get(data.case_id)
        if not case:
            return ResponseHelper.not_found("Case", data.case_id)

        # Validate case RID
        if not case.rid.startswith("model/") or len(case.rid.split("/")) < 3:
            return ResponseHelper.validation_error(
                "Case RID format incorrect",
                {"rid": case.rid},
            )

        # Build config
        config = dict(data.config)
        channels = data.channels
        if isinstance(channels, str):
            channels = [c.strip() for c in channels.split(",") if c.strip()]
        if channels:
            config["channels"] = channels
        if data.model_source:
            config["model_source"] = str(Path(data.model_source).expanduser().resolve())

        # Create task
        task_id = IDGenerator.generate(EntityType.TASK)
        task = Task(
            id=task_id,
            name=data.name,
            case_id=data.case_id,
            type=data.type,
            server_id=case.server_id,
            status="created",
            config=config,
        )

        TaskRegistry().create(task_id, task)
        materialize_entity("task", task_id, task)
        write_audit("portal.task.create", task_id, {"case_id": data.case_id, "type": data.type})
        refresh_index()

        return ResponseHelper.success(TaskResponse.from_model(task).to_dict(), 201)

    def update(self, task_id: str, payload: dict[str, Any]) -> tuple[dict[str, Any], int]:
        """POST /api/tasks/{id} - Update a task."""
        registry = TaskRegistry()
        task = registry.get(task_id)
        if not task:
            return ResponseHelper.not_found("Task", task_id)

        # Check if task is editable
        if task.status not in {"created", "submitted", "failed"}:
            return ResponseHelper.error(
                "STATE_ERROR",
                f"任务状态为 {task.status}，不能修改配置",
                409,
            )

        try:
            data = TaskUpdate(
                name=payload.get("name"),
                type=payload.get("type"),
                config=payload.get("config"),
                channels=payload.get("channels"),
                model_source=payload.get("model_source"),
            )
            data.validate()
        except ValueError as exc:
            return ResponseHelper.validation_error(str(exc))

        updates: dict[str, Any] = {}

        if data.name is not None:
            updates["name"] = data.name

        if data.type is not None:
            updates["type"] = data.type

        # Handle config updates
        config = dict(task.config or {})
        if data.config is not None:
            config = data.config

        if "channels" in payload:
            channels = payload.get("channels") or []
            if isinstance(channels, str):
                channels = [c.strip() for c in channels.split(",") if c.strip()]
            if channels:
                config["channels"] = channels
            else:
                config.pop("channels", None)

        if "model_source" in payload:
            model_source = str(payload.get("model_source", "")).strip()
            if model_source:
                config["model_source"] = str(Path(model_source).expanduser().resolve())
            else:
                config.pop("model_source", None)

        updates["config"] = config

        registry.update(task_id, updates)
        updated = registry.get(task_id)
        if updated:
            materialize_entity("task", task_id, updated)
            write_audit("portal.task.update", task_id, updates)
            refresh_index()
            return ResponseHelper.success(TaskResponse.from_model(updated).to_dict())

        return ResponseHelper.error("UPDATE_FAILED", "Failed to update task", 500)

    def run(self, task_id: str, payload: dict[str, Any]) -> tuple[dict[str, Any], int]:
        """POST /api/tasks/{id}/run - Run a task."""
        # Run preflight checks
        preflight_result = self._preflight(task_id)
        if not preflight_result["ok"]:
            messages = "; ".join(
                c["message"] for c in preflight_result["checks"] if not c["ok"]
            )
            return ResponseHelper.error(
                "PREFLIGHT_FAILED",
                f"Preflight 未通过: {messages}",
                422,
            )

        try:
            run_request = TaskRunRequest(timeout=payload.get("timeout", 300))
        except ValueError as exc:
            return ResponseHelper.validation_error(str(exc))

        # Execute task
        try:
            from dataclasses import asdict

            result = execute_task(task_id, timeout_seconds=run_request.timeout)
            return ResponseHelper.success(asdict(result))
        except Exception as exc:
            return ResponseHelper.error(
                "EXECUTION_FAILED",
                str(exc),
                500,
            )

    def preflight(self, task_id: str) -> tuple[dict[str, Any], int]:
        """GET /api/tasks/{id}/preflight - Run preflight checks."""
        return ResponseHelper.success(self._preflight(task_id))

    def _preflight(self, task_id: str) -> dict[str, Any]:
        """Run preflight checks for a task."""
        task = TaskRegistry().get(task_id)
        checks = []

        if not task:
            checks.append({"name": "task", "ok": False, "message": "Task 不存在"})
            return {"ok": False, "checks": checks}

        # Run case preflight
        from .cases import CaseHandler
        case_handler = CaseHandler()
        case_preflight = case_handler.preflight(task.case_id)
        case_preflight_data = case_preflight[0].get("data", {})
        checks.extend(case_preflight_data.get("checks", []))

        # Task type check
        checks.append({
            "name": "Task Type",
            "ok": task.type in {"powerflow", "emt", "stability"},
            "message": task.type,
        })

        # EMT channels check
        if task.type == "emt":
            channels = task.config.get("channels") or []
            checks.append({
                "name": "EMT Channels",
                "ok": True,
                "message": ", ".join(channels) if channels else "未设置，将尝试默认通道",
            })

        return {"ok": all(c["ok"] for c in checks), "checks": checks}

    def logs(self, task_id: str) -> tuple[dict[str, Any], int]:
        """GET /api/tasks/{id}/logs - Get task logs."""
        task = TaskRegistry().get(task_id)
        if not task:
            return ResponseHelper.not_found("Task", task_id)

        # TODO: Implement actual log retrieval from task runner
        return ResponseHelper.success({
            "task_id": task_id,
            "logs": [],
        })
