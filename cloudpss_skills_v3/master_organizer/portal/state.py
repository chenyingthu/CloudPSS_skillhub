"""Read/write helpers used by the local organizer portal."""

from __future__ import annotations

import json
import csv
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

from cloudpss_skills_v3.master_organizer.core import (
    Case,
    CaseRegistry,
    EntityType,
    IDGenerator,
    ResultRegistry,
    ServerRegistry,
    Task,
    TaskRegistry,
    VariantRegistry,
    get_path_manager,
)
from cloudpss_skills_v3.master_organizer.core.config_manager import get_config_manager
from cloudpss_skills_v3.master_organizer.core.release_ops import (
    QuotaError,
    archive_result,
    check_workspace_quotas,
    generate_result_report,
    materialize_entity,
    refresh_index,
    write_audit,
)
from cloudpss_skills_v3.master_organizer.core.server_auth import decrypt_server_token
from cloudpss_skills_v3.master_organizer.core.task_runner import execute_task
from cloudpss_skills_v3.master_organizer.portal.model_editor import model_summary, save_model_edits


def validate_resource_id(rid: str):
    if not rid.startswith("model/") or len(rid.split("/")) < 3:
        raise ValueError("CloudPSS RID 格式不正确，应类似 model/chenying/IEEE39")


def _safe_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _csv_preview(path: Path, limit: int = 12) -> dict[str, Any]:
    if not path.exists():
        return {"headers": [], "rows": [], "path": str(path)}
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    if not rows:
        return {"headers": [], "rows": [], "path": str(path)}
    headers = rows[0]
    preview_rows = rows[1 : limit + 1]
    return {"headers": headers, "rows": preview_rows, "path": str(path), "total_lines": len(rows)}


def _csv_series(path: Path, limit: int = 240) -> dict[str, Any]:
    if not path.exists():
        return {"points": [], "path": str(path)}
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    points = []
    for row in rows[:limit]:
        try:
            points.append({"x": float(row.get("time", "")), "y": float(row.get("value", ""))})
        except (TypeError, ValueError):
            continue
    return {"points": points, "path": str(path), "total_points": len(rows)}


def _plain(value: Any) -> Any:
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
    rows = []
    for entity_id, entity in items:
        row = _plain(entity)
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


def _task_editable(task: dict[str, Any]) -> bool:
    return task.get("status") in {"created", "submitted", "failed"}


def _case_server(case: Case) -> dict[str, Any] | None:
    server = ServerRegistry().get(case.server_id) if case.server_id else None
    if not server:
        return None
    row = _plain(server)
    row["id"] = case.server_id
    return _public_server(row)


def _case_notes(case: Case) -> dict[str, Any]:
    try:
        value = json.loads(case.description or "{}")
        return value if isinstance(value, dict) else {}
    except json.JSONDecodeError:
        return {}


def _case_description_text(case_or_description: Case | str | None) -> str:
    description = case_or_description.description if isinstance(case_or_description, Case) else str(case_or_description or "")
    try:
        value = json.loads(description or "{}")
    except json.JSONDecodeError:
        return description
    if isinstance(value, dict) and "description_text" in value:
        return str(value.get("description_text") or "")
    return description


def _case_description_with_model_source(description: str, model_source: str) -> str:
    description_text = _case_description_text(description).strip()
    notes: dict[str, Any] = {}
    if description_text:
        notes["description_text"] = description_text
    model_source = str(model_source or "").strip()
    if model_source:
        model_path = Path(model_source).expanduser().resolve()
        if not model_path.exists():
            raise ValueError(f"模型源文件不存在: {model_path}")
        notes["model_source"] = str(model_path)
    elif description_text:
        return description_text
    return json.dumps(notes, ensure_ascii=False, indent=2) if notes else ""


def _case_model_source(case: Case, tasks: list[dict[str, Any]]) -> str:
    notes = _case_notes(case)
    model_source = str(notes.get("model_source", "")).strip()
    if model_source:
        return model_source
    for task in tasks:
        candidate = (task.get("config") or {}).get("model_source")
        if candidate:
            return str(candidate)
    return ""


def workspace_summary() -> dict[str, Any]:
    pm = get_path_manager()
    servers = ServerRegistry()
    cases = CaseRegistry()
    tasks = TaskRegistry()
    results = ResultRegistry()
    variants = VariantRegistry()
    usage = pm.get_storage_usage()
    quota_status = {"ok": True, "message": "正常"}
    try:
        check_workspace_quotas()
    except QuotaError as exc:
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


def organizer_snapshot() -> dict[str, Any]:
    servers = [_public_server(server) for server in _with_id(ServerRegistry().list_all())]
    cases = _with_id(CaseRegistry().list_all())
    tasks = _with_id(TaskRegistry().list_all())
    results = _with_id(ResultRegistry().list_all())
    variants = _with_id(VariantRegistry().list_all())

    tasks_by_case: dict[str, list[dict[str, Any]]] = {}
    variants_by_case: dict[str, list[dict[str, Any]]] = {}
    results_by_task: dict[str, list[dict[str, Any]]] = {}
    for task in tasks:
        tasks_by_case.setdefault(task["case_id"], []).append(task)
    for variant in variants:
        variants_by_case.setdefault(variant["case_id"], []).append(variant)
    for result in results:
        results_by_task.setdefault(result["task_id"], []).append(result)

    recent_tasks = sorted(tasks, key=lambda item: item.get("created_at", ""), reverse=True)[:8]
    recent_results = sorted(results, key=lambda item: item.get("created_at", ""), reverse=True)[:8]

    return {
        "workspace": workspace_summary(),
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


def case_detail(case_id: str) -> dict[str, Any]:
    case = CaseRegistry().get(case_id)
    if not case:
        raise ValueError(f"case not found: {case_id}")
    tasks = _with_id(TaskRegistry().filter_by(case_id=case_id))
    variants = _with_id(VariantRegistry().get_by_case(case_id))
    results = []
    result_registry = ResultRegistry()
    for task in tasks:
        if task.get("result_id"):
            result = result_registry.get(task["result_id"])
            if result:
                row = _plain(result)
                row["id"] = task["result_id"]
                results.append(row)
    return {
        "case": {"id": case_id, **_plain(case)},
        "model": {
            "rid": case.rid,
            "model_source": _case_model_source(case, tasks),
            "server_id": case.server_id,
            "server": _case_server(case),
            "case_yaml": str(get_path_manager().get_case_path(case_id) / "case.yaml"),
            "editor": case_model_editor(case_id, tasks),
        },
        "tasks": tasks,
        "variants": variants,
        "results": results,
        "simulation_plan": case_simulation_plan(case_id, tasks, results),
        "preflight": case_preflight(case_id),
    }


def case_model_editor(case_id: str, tasks: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    case = CaseRegistry().get(case_id)
    if not case:
        return {"editable": False, "reason": "Case 不存在"}
    tasks = tasks if tasks is not None else _with_id(TaskRegistry().filter_by(case_id=case_id))
    model_source = _case_model_source(case, tasks)
    if not model_source:
        return {
            "editable": False,
            "reason": "当前 Case 使用远端 RID。请先在任务中配置本地 model_source，Portal 才能表格化编辑模型文件。",
        }
    try:
        return model_summary(model_source)
    except Exception as exc:
        return {"editable": False, "path": model_source, "reason": str(exc)}


def case_simulation_plan(
    case_id: str,
    tasks: list[dict[str, Any]] | None = None,
    results: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    tasks = tasks if tasks is not None else _with_id(TaskRegistry().filter_by(case_id=case_id))
    results = results if results is not None else _with_id(ResultRegistry().filter_by(case_id=case_id))
    completed = [task for task in tasks if task.get("status") == "completed"]
    runnable = [task for task in tasks if _task_editable(task)]
    latest_result = sorted(results, key=lambda item: item.get("created_at", ""), reverse=True)[:1]
    task_types = sorted({task.get("type", "-") for task in tasks})
    return {
        "task_count": len(tasks),
        "completed_count": len(completed),
        "runnable_count": len(runnable),
        "result_count": len(results),
        "task_types": task_types,
        "latest_result_id": latest_result[0]["id"] if latest_result else None,
        "next_action": "创建仿真任务" if not tasks else ("运行待执行任务" if runnable else "查看结果或生成报告"),
    }


def result_detail(result_id: str) -> dict[str, Any]:
    pm = get_path_manager()
    result = ResultRegistry().get(result_id)
    if not result:
        raise ValueError(f"result not found: {result_id}")
    result_dir = pm.get_result_path(result_id)
    artifacts: dict[str, Any] = {}
    for relative_path in result.files:
        path = result_dir / relative_path
        if path.is_file() and path.suffix == ".json":
            try:
                artifacts[relative_path] = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                artifacts[relative_path] = {"error": "invalid json"}
    report_path = result_dir / "report.md"
    summary = result_summary(result_id, result_dir=result_dir)
    return {
        "result": {"id": result_id, **_plain(result)},
        "directory": str(result_dir),
        "summary": summary,
        "artifacts": artifacts,
        "report": report_path.read_text(encoding="utf-8") if report_path.exists() else "",
    }


def result_summary(result_id: str, *, result_dir: Path | None = None) -> dict[str, Any]:
    pm = get_path_manager()
    result = ResultRegistry().get(result_id)
    if not result:
        raise ValueError(f"result not found: {result_id}")
    result_dir = result_dir or pm.get_result_path(result_id)
    summary: dict[str, Any] = {
        "format": result.format,
        "metadata": result.metadata,
        "files": result.files,
    }
    if result.format == "powerflow":
        buses = _safe_read_json(result_dir / "tables" / "buses.json") or []
        branches = _safe_read_json(result_dir / "tables" / "branches.json") or []
        summary.update(
            {
                "kind": "powerflow",
                "bus_rows": len(buses),
                "branch_rows": len(branches),
                "buses_preview": buses[:20],
                "branches_preview": branches[:20],
                "bus_chart": _powerflow_bus_chart(buses),
            }
        )
    elif result.format == "emt":
        channels = _safe_read_json(result_dir / "channels.json") or []
        summary.update(
            {
                "kind": "emt",
                "channel_count": len(channels),
                "channels": channels,
                "csv_preview": {
                    item.get("csv_file", ""): _csv_preview(result_dir / item.get("csv_file", ""))
                    for item in channels[:6]
                    if item.get("csv_file")
                },
                "series": {
                    item.get("csv_file", ""): _csv_series(result_dir / item.get("csv_file", ""))
                    for item in channels[:6]
                    if item.get("csv_file")
                },
            }
        )
    return summary


def _powerflow_bus_chart(rows: list[dict[str, Any]], limit: int = 120) -> dict[str, Any]:
    if not rows:
        return {"points": []}
    keys = list(rows[0].keys())
    label_key = next((key for key in keys if key.lower() in {"bus", "name", "id"}), keys[0])
    value_key = next((key for key in keys if key.lower() in {"v", "vm", "voltage", "u"}), None)
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
        except (TypeError, ValueError):
            continue
        points.append({"x": index, "y": value, "label": str(row.get(label_key, index))})
    return {"points": points, "label_key": label_key, "value_key": value_key}


def case_preflight(case_id: str) -> dict[str, Any]:
    case = CaseRegistry().get(case_id)
    checks = []
    if not case:
        return {"ok": False, "checks": [{"name": "case", "ok": False, "message": "Case 不存在"}]}
    rid_ok = case.rid.startswith("model/") and len(case.rid.split("/")) >= 3
    checks.append({"name": "CloudPSS RID", "ok": rid_ok, "message": case.rid if rid_ok else "RID 应类似 model/chenying/IEEE39"})
    server = ServerRegistry().get(case.server_id) if case.server_id else None
    checks.append({"name": "Server", "ok": server is not None, "message": f"{server.url} ({server.owner})" if server else "未绑定 server"})
    token_ok = False
    token_message = "未检查"
    if server:
        try:
            token_ok = bool(decrypt_server_token(server))
            token_message = "token 可解密"
        except Exception as exc:
            token_message = str(exc)
    checks.append({"name": "Token", "ok": token_ok, "message": token_message})
    checks.append({"name": "Case Status", "ok": case.status == "active", "message": case.status})
    return {"ok": all(item["ok"] for item in checks), "checks": checks}


def task_preflight(task_id: str) -> dict[str, Any]:
    task = TaskRegistry().get(task_id)
    if not task:
        return {"ok": False, "checks": [{"name": "task", "ok": False, "message": "Task 不存在"}]}
    preflight = case_preflight(task.case_id)
    checks = list(preflight["checks"])
    checks.append({"name": "Task Type", "ok": task.type in {"powerflow", "emt"}, "message": task.type})
    if task.type == "emt":
        channels = task.config.get("channels") or []
        checks.append({"name": "EMT Channels", "ok": True, "message": ", ".join(channels) if channels else "未设置，将尝试默认通道"})
    return {"ok": all(item["ok"] for item in checks), "checks": checks}


def audit_entries(limit: int = 80) -> list[dict[str, Any]]:
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


def create_case(payload: dict[str, Any]) -> dict[str, Any]:
    name = str(payload.get("name", "")).strip()
    rid = str(payload.get("rid", "")).strip()
    if not name or not rid:
        raise ValueError("name and rid are required")
    validate_resource_id(rid)
    server_id = str(payload.get("server_id", "")).strip()
    if not server_id:
        servers = ServerRegistry().list_all()
        default_server = next(((sid, server) for sid, server in servers if getattr(server, "default", False)), None)
        server_id = default_server[0] if default_server else ""
    tags = payload.get("tags") or []
    if isinstance(tags, str):
        tags = [item.strip() for item in tags.split(",") if item.strip()]
    description = _case_description_with_model_source(
        str(payload.get("description", "")).strip(),
        str(payload.get("model_source", "")).strip(),
    )
    case_id = IDGenerator.generate(EntityType.CASE)
    case = Case(
        id=case_id,
        name=name,
        rid=rid,
        description=description,
        server_id=server_id,
        status="active",
        tags=tags,
    )
    CaseRegistry().create(case_id, case)
    materialize_entity("case", case_id, case)
    write_audit("portal.case.create", case_id, {"name": name, "rid": rid})
    refresh_index()
    return {"id": case_id, **_plain(case)}


def update_case(case_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    registry = CaseRegistry()
    case = registry.get(case_id)
    if not case:
        raise ValueError(f"case not found: {case_id}")
    updates: dict[str, Any] = {}
    if "name" in payload:
        name = str(payload.get("name", "")).strip()
        if not name:
            raise ValueError("name cannot be empty")
        updates["name"] = name
    if "rid" in payload:
        rid = str(payload.get("rid", "")).strip()
        validate_resource_id(rid)
        updates["rid"] = rid
    if "description" in payload or "model_source" in payload:
        description = str(payload.get("description", _case_description_text(case))).strip()
        model_source = str(payload.get("model_source", _case_model_source(case, []))).strip()
        updates["description"] = _case_description_with_model_source(description, model_source)
    if "tags" in payload:
        tags = payload.get("tags") or []
        if isinstance(tags, str):
            tags = [item.strip() for item in tags.split(",") if item.strip()]
        updates["tags"] = tags
    if not updates:
        return {"id": case_id, **_plain(case)}
    registry.update(case_id, updates)
    updated = registry.get(case_id)
    materialize_entity("case", case_id, updated)
    write_audit("portal.case.update", case_id, updates)
    refresh_index()
    return {"id": case_id, **_plain(updated)}


def create_task(payload: dict[str, Any]) -> dict[str, Any]:
    case_id = str(payload.get("case_id", "")).strip()
    task_type = str(payload.get("type", "powerflow")).strip()
    name = str(payload.get("name", "")).strip() or f"{task_type} task"
    case = CaseRegistry().get(case_id)
    if not case:
        raise ValueError(f"case not found: {case_id}")
    validate_resource_id(case.rid)
    config = payload.get("config") or {}
    if not isinstance(config, dict):
        raise ValueError("config must be an object")
    channels = payload.get("channels") or []
    if isinstance(channels, str):
        channels = [item.strip() for item in channels.split(",") if item.strip()]
    if channels:
        config["channels"] = channels
    model_source = str(payload.get("model_source", "")).strip()
    if model_source:
        config["model_source"] = str(Path(model_source).expanduser().resolve())

    task_id = IDGenerator.generate(EntityType.TASK)
    task = Task(
        id=task_id,
        name=name,
        case_id=case_id,
        type=task_type,
        server_id=case.server_id,
        status="created",
        config=config,
    )
    TaskRegistry().create(task_id, task)
    materialize_entity("task", task_id, task)
    write_audit("portal.task.create", task_id, {"case_id": case_id, "type": task_type})
    refresh_index()
    return {"id": task_id, **_plain(task)}


def update_task(task_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    registry = TaskRegistry()
    task = registry.get(task_id)
    if not task:
        raise ValueError(f"task not found: {task_id}")
    if task.status not in {"created", "submitted", "failed"}:
        raise ValueError(f"任务状态为 {task.status}，不能修改配置")

    updates: dict[str, Any] = {}
    if "name" in payload:
        name = str(payload.get("name", "")).strip()
        if not name:
            raise ValueError("name cannot be empty")
        updates["name"] = name
    if "type" in payload:
        task_type = str(payload.get("type", "")).strip()
        if task_type not in {"powerflow", "emt"}:
            raise ValueError("task type must be powerflow or emt")
        updates["type"] = task_type

    config = dict(task.config or {})
    if "config" in payload:
        incoming = payload.get("config") or {}
        if not isinstance(incoming, dict):
            raise ValueError("config must be an object")
        config = incoming
    if "channels" in payload:
        channels = payload.get("channels") or []
        if isinstance(channels, str):
            channels = [item.strip() for item in channels.split(",") if item.strip()]
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
    materialize_entity("task", task_id, updated)
    write_audit("portal.task.update", task_id, updates)
    refresh_index()
    return {"id": task_id, **_plain(updated)}


def save_model_table_edits(payload: dict[str, Any]) -> dict[str, Any]:
    case_id = str(payload.get("case_id", "")).strip()
    path = str(payload.get("path", "")).strip()
    updates = payload.get("updates") or []
    if not case_id:
        raise ValueError("case_id is required")
    if not path:
        raise ValueError("path is required")
    if not isinstance(updates, list):
        raise ValueError("updates must be a list")
    case = CaseRegistry().get(case_id)
    if not case:
        raise ValueError(f"case not found: {case_id}")
    tasks = _with_id(TaskRegistry().filter_by(case_id=case_id))
    expected_path = _case_model_source(case, tasks)
    if not expected_path:
        raise ValueError("Case 未绑定本地模型源，不能保存模型修改")
    requested_path = Path(path).expanduser().resolve()
    bound_path = Path(expected_path).expanduser().resolve()
    if requested_path != bound_path:
        raise ValueError("模型保存路径必须匹配当前 Case 绑定的本地模型源")
    result = save_model_edits(path, updates)
    write_audit("portal.model.update", result["path"], {"changed": result["changed"], "backup": result["backup_path"]})
    return result


def run_task(task_id: str, timeout_seconds: int = 300) -> dict[str, Any]:
    preflight = task_preflight(task_id)
    if not preflight["ok"]:
        messages = "; ".join(f"{item['name']}: {item['message']}" for item in preflight["checks"] if not item["ok"])
        raise ValueError(f"Preflight 未通过: {messages}")
    result = execute_task(task_id, timeout_seconds=timeout_seconds)
    return _plain(result)


def report_result(result_id: str) -> dict[str, str]:
    path = generate_result_report(result_id)
    return {"path": str(path)}


def archive_result_for_portal(result_id: str) -> dict[str, str]:
    path = archive_result(result_id)
    return {"path": str(path)}


def workspace_health() -> dict[str, Any]:
    index_path = refresh_index()
    config = get_config_manager().get_user_config()
    return {
        "summary": workspace_summary(),
        "index_path": str(index_path),
        "quotas": _plain(config.quotas),
        "audit": audit_entries(20),
    }
