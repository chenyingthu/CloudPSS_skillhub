"""Release-grade workspace operations for the master organizer."""

from __future__ import annotations

import json
import shutil
import tarfile
from dataclasses import asdict, is_dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from .config_manager import get_config_manager
from .models import Case, Result, Task, Variant
from .path_manager import get_path_manager
from .registries import CaseRegistry, ResultRegistry, ServerRegistry, TaskRegistry, VariantRegistry


CASE_TRANSITIONS = {
    "draft": {"active", "deleted"},
    "active": {"archived", "deleted"},
    "archived": {"active", "deleted"},
    "deleted": set(),
}

TASK_TRANSITIONS = {
    "created": {"submitted", "running", "cancelled", "failed"},
    "submitted": {"running", "cancelled", "failed"},
    "running": {"completed", "failed", "cancelled"},
    "completed": {"exported", "registered"},
    "failed": {"submitted"},
    "cancelled": set(),
    "exported": {"registered"},
    "registered": set(),
}


class LifecycleError(ValueError):
    """Raised when an entity state transition is not allowed."""


class QuotaError(ValueError):
    """Raised when a workspace quota would be exceeded."""


def can_transition(kind: str, from_state: str, to_state: str) -> bool:
    transitions = CASE_TRANSITIONS if kind == "case" else TASK_TRANSITIONS
    return to_state in transitions.get(from_state, set())


def require_transition(kind: str, from_state: str, to_state: str):
    if from_state == to_state:
        return
    if not can_transition(kind, from_state, to_state):
        raise LifecycleError(f"{kind} 状态不能从 {from_state} 转为 {to_state}")


def transition_case(case_id: str, to_state: str, registry: CaseRegistry | None = None) -> Case:
    registry = registry or CaseRegistry()
    case = registry.get(case_id)
    if not case:
        raise LifecycleError(f"算例不存在: {case_id}")
    require_transition("case", case.status, to_state)
    registry.update(case_id, {"status": to_state})
    updated = registry.get(case_id)
    assert updated is not None
    materialize_entity("case", case_id, updated)
    write_audit("case.transition", case_id, {"from": case.status, "to": to_state})
    refresh_index()
    return updated


def transition_task(task_id: str, to_state: str, updates: dict[str, Any] | None = None, registry: TaskRegistry | None = None) -> Task:
    registry = registry or TaskRegistry()
    task = registry.get(task_id)
    if not task:
        raise LifecycleError(f"任务不存在: {task_id}")
    require_transition("task", task.status, to_state)
    payload = dict(updates or {})
    payload["status"] = to_state
    registry.update(task_id, payload)
    updated = registry.get(task_id)
    assert updated is not None
    materialize_entity("task", task_id, updated)
    write_audit("task.transition", task_id, {"from": task.status, "to": to_state, **(updates or {})})
    refresh_index()
    return updated


def _to_plain_dict(value: Any) -> dict[str, Any]:
    if is_dataclass(value):
        return asdict(value)
    return dict(value)


def write_yaml(path: Path, data: dict[str, Any]):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")


def materialize_entity(kind: str, entity_id: str, entity: Any):
    pm = get_path_manager()
    now = datetime.now().isoformat()
    entity_data = _to_plain_dict(entity)
    document = {
        "api_version": "v1.0",
        "metadata": {
            "created_at": entity_data.get("created_at", now),
            "updated_at": now,
            "version": "1.0.0",
        },
        kind: entity_data,
    }

    if kind == "case":
        write_yaml(pm.get_case_path(entity_id) / "case.yaml", document)
    elif kind == "task":
        write_yaml(pm.get_task_path(entity_id) / "task.yaml", document)
    elif kind == "result":
        write_yaml(pm.get_result_path(entity_id) / "result.yaml", document)
    elif kind == "variant":
        case_id = getattr(entity, "case_id")
        write_yaml(pm.get_variant_path(case_id, entity_id), document)


def materialize_workspace_entities():
    for case_id, case in CaseRegistry().list_all():
        materialize_entity("case", case_id, case)
    for task_id, task in TaskRegistry().list_all():
        materialize_entity("task", task_id, task)
    for result_id, result in ResultRegistry().list_all():
        materialize_entity("result", result_id, result)
    for variant_id, variant in VariantRegistry().list_all():
        materialize_entity("variant", variant_id, variant)


def refresh_index() -> Path:
    pm = get_path_manager()
    servers = ServerRegistry()
    cases = CaseRegistry()
    tasks = TaskRegistry()
    results = ResultRegistry()
    variants = VariantRegistry()

    recent_cases = [case_id for case_id, _case in sorted(cases.list_all(), key=lambda item: item[1].created_at, reverse=True)[:10]]
    recent_tasks = [task_id for task_id, _task in sorted(tasks.list_all(), key=lambda item: item[1].created_at, reverse=True)[:10]]

    document = {
        "api_version": "v1.0",
        "metadata": {
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "version": "1.0.0",
        },
        "stats": {
            "total_servers": servers.count(),
            "total_cases": cases.count(),
            "total_tasks": tasks.count(),
            "total_results": results.count(),
            "total_variants": variants.count(),
        },
        "quick_access": {
            "recent_cases": recent_cases,
            "recent_tasks": recent_tasks,
            "favorite_cases": [],
        },
        "registries": {
            "servers": "registry/servers.yaml",
            "cases": "registry/cases.yaml",
            "tasks": "registry/tasks.yaml",
            "results": "registry/results.yaml",
            "variants": "registry/variants.yaml",
        },
    }
    index_path = pm.registry_dir / "index.yaml"
    write_yaml(index_path, document)
    return index_path


def write_audit(action: str, entity_id: str, details: dict[str, Any] | None = None):
    pm = get_path_manager()
    entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "entity_id": entity_id,
        "details": details or {},
    }
    pm.logs_dir.mkdir(parents=True, exist_ok=True)
    with open(pm.logs_dir / "audit.log", "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n")


def check_workspace_quotas():
    pm = get_path_manager()
    quotas = get_config_manager().get_user_config().quotas
    cases = CaseRegistry()
    tasks = TaskRegistry()
    results = ResultRegistry()

    if cases.count() > quotas.max_cases:
        raise QuotaError(f"算例数量超过配额: {cases.count()} > {quotas.max_cases}")
    for case_id, _case in cases.list_all():
        task_count = len(tasks.filter_by(case_id=case_id))
        if task_count > quotas.max_tasks_per_case:
            raise QuotaError(f"算例 {case_id} 任务数超过配额: {task_count} > {quotas.max_tasks_per_case}")
    for task_id, _task in tasks.list_all():
        result_count = len(results.filter_by(task_id=task_id))
        if result_count > quotas.max_results_per_task:
            raise QuotaError(f"任务 {task_id} 结果数超过配额: {result_count} > {quotas.max_results_per_task}")

    storage_bytes = pm.get_storage_usage().get("total", 0)
    max_bytes = quotas.max_storage_gb * 1024 * 1024 * 1024
    if storage_bytes > max_bytes:
        raise QuotaError(f"存储空间超过配额: {storage_bytes} > {max_bytes} bytes")


def archive_result(result_id: str, output: Path | None = None) -> Path:
    pm = get_path_manager()
    result = ResultRegistry().get(result_id)
    if not result:
        raise ValueError(f"结果不存在: {result_id}")
    result_dir = pm.get_result_path(result_id)
    if not result_dir.exists():
        raise ValueError(f"结果目录不存在: {result_dir}")
    archive_path = output or (result_dir / f"{result_id}.tar.gz")
    archive_path = archive_path.expanduser().resolve()
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive_path, "w:gz") as tar:
        tar.add(result_dir, arcname=result_id, filter=lambda info: None if Path(info.name).name == archive_path.name else info)
    write_audit("result.archive", result_id, {"path": str(archive_path)})
    return archive_path


def generate_result_report(result_id: str, output: Path | None = None) -> Path:
    pm = get_path_manager()
    result = ResultRegistry().get(result_id)
    if not result:
        raise ValueError(f"结果不存在: {result_id}")
    result_dir = pm.get_result_path(result_id)
    case = CaseRegistry().get(result.case_id)
    task = TaskRegistry().get(result.task_id)
    report_path = output or (result_dir / "report.md")
    report_path = report_path.expanduser().resolve()
    report_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        f"# CloudPSS Result Report: {result.name}",
        "",
        f"- Result ID: `{result.id}`",
        f"- Task ID: `{result.task_id}`",
        f"- Case ID: `{result.case_id}`",
        f"- Format: `{result.format}`",
        f"- Created At: `{result.created_at}`",
        f"- Size: `{result.size_bytes}` bytes",
        "",
        "## Case",
    ]
    if case:
        lines.extend(
            [
                f"- Name: `{case.name}`",
                f"- RID: `{case.rid}`",
                f"- Server ID: `{case.server_id}`",
                f"- Status: `{case.status}`",
                f"- Tags: `{', '.join(case.tags)}`",
            ]
        )
    else:
        lines.append("- Case registry entry not found")

    lines.extend(["", "## Task"])
    if task:
        lines.extend(
            [
                f"- Name: `{task.name}`",
                f"- Type: `{task.type}`",
                f"- Status: `{task.status}`",
                f"- Job ID: `{task.job_id}`",
                f"- Submitted At: `{task.submitted_at}`",
                f"- Completed At: `{task.completed_at}`",
                "",
                "### Task Config",
                "",
                "```json",
                json.dumps(task.config, ensure_ascii=False, indent=2),
                "```",
            ]
        )
    else:
        lines.append("- Task registry entry not found")

    lines.extend(
        [
            "",
            "## Result Summary",
            f"- Data Source: `{result.metadata.get('data_source', '-')}`",
            f"- Server URL: `{result.metadata.get('server_url', '-')}`",
            f"- Server Owner: `{result.metadata.get('server_owner', '-')}`",
            f"- Model RID: `{result.metadata.get('model_rid', '-')}`",
        ]
    )
    if result.format == "powerflow":
        lines.extend(
            [
                f"- Bus Rows: `{result.metadata.get('bus_rows', '-')}`",
                f"- Branch Rows: `{result.metadata.get('branch_rows', '-')}`",
            ]
        )
    if result.format == "emt":
        lines.extend(
            [
                f"- Plot Count: `{result.metadata.get('plot_count', '-')}`",
                f"- Channel Count: `{result.metadata.get('channel_count', '-')}`",
                f"- Sample Points: `{result.metadata.get('sample_points', '-')}`",
            ]
        )

    lines.extend(
        [
            "",
            "## Metadata",
        ]
    )
    if result.metadata:
        for key, value in result.metadata.items():
            lines.append(f"- `{key}`: `{value}`")
    else:
        lines.append("- None")

    lines.extend(["", "## Files"])
    for file_name in result.files:
        lines.append(f"- `{file_name}`")

    manifest_path = result_dir / "manifest.json"
    if manifest_path.exists():
        lines.extend(["", "## Manifest", "", "```json"])
        lines.append(manifest_path.read_text(encoding="utf-8"))
        lines.append("```")

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    write_audit("result.report", result_id, {"path": str(report_path)})
    return report_path


def move_to_trash(entity_id: str, source: Path):
    pm = get_path_manager()
    if not source.exists():
        return
    trash_path = pm.get_trash_path(entity_id)
    if trash_path.exists():
        shutil.rmtree(trash_path)
    trash_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(trash_path))
    (trash_path / ".deleted_at").write_text(datetime.now().isoformat(), encoding="utf-8")


__all__ = [
    "LifecycleError",
    "QuotaError",
    "archive_result",
    "check_workspace_quotas",
    "generate_result_report",
    "materialize_entity",
    "materialize_workspace_entities",
    "move_to_trash",
    "refresh_index",
    "transition_case",
    "transition_task",
    "write_audit",
]
