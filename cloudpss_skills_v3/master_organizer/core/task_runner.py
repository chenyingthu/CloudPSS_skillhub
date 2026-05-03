"""Production CloudPSS task execution for the master organizer."""

from __future__ import annotations

import os
import time
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from .id_generator import EntityType, IDGenerator
from .models import Result, Task
from .registries import CaseRegistry, ResultRegistry, ServerRegistry, TaskRegistry
from .result_storage import safe_artifact_name, store_emt_result, store_powerflow_result
from .server_auth import decrypt_server_token, get_default_server, migrate_server_token_to_workspace_key
from .release_ops import materialize_entity, refresh_index, transition_task, write_audit


class TaskExecutionError(RuntimeError):
    """Raised when a task cannot be executed against CloudPSS."""


@dataclass
class TaskExecutionResult:
    task_id: str
    result_id: str
    job_id: str | None
    status: str
    files: list[str]
    metadata: dict[str, Any]


@contextmanager
def _cloudpss_server_context(server_url: str):
    previous_api_url = os.environ.get("CLOUDPSS_API_URL")
    os.environ["CLOUDPSS_API_URL"] = server_url
    try:
        yield
    finally:
        if previous_api_url is None:
            os.environ.pop("CLOUDPSS_API_URL", None)
        else:
            os.environ["CLOUDPSS_API_URL"] = previous_api_url


def _wait_for_job(job: Any, *, timeout_seconds: int, poll_interval: float) -> int:
    started = time.time()
    status = job.status()
    while status not in (1, 2):
        if time.time() - started > timeout_seconds:
            raise TimeoutError(f"CloudPSS job timed out: {getattr(job, 'id', 'unknown')} status={status}")
        time.sleep(poll_interval)
        status = job.status()
    return status


def _table_row_count(table: dict[str, Any]) -> int:
    columns = table.get("data", {}).get("columns", [])
    return len(columns[0].get("data", [])) if columns else 0


def _resolve_server(task: Task, case_server_id: str, servers: ServerRegistry):
    server_id = task.server_id or case_server_id
    if server_id:
        server = servers.get(server_id)
        if not server:
            raise TaskExecutionError(f"服务器不存在: {server_id}")
        return server_id, server

    default_server = get_default_server(servers)
    if not default_server:
        raise TaskExecutionError("没有可用服务器，请先执行 server add 或 server internal")
    return default_server


def execute_task(
    task_id: str,
    *,
    timeout_seconds: int = 300,
    poll_interval: float = 2.0,
) -> TaskExecutionResult:
    """Execute a registered task against CloudPSS and persist its result artifacts."""
    tasks = TaskRegistry()
    cases = CaseRegistry()
    servers = ServerRegistry()
    results = ResultRegistry()

    task = tasks.get(task_id)
    if not task:
        raise TaskExecutionError(f"任务不存在: {task_id}")
    if task.status not in {"created", "submitted", "failed"}:
        raise TaskExecutionError(f"任务状态为 {task.status}，不能提交执行")

    case = cases.get(task.case_id)
    if not case:
        raise TaskExecutionError(f"算例不存在: {task.case_id}")
    if not case.rid:
        raise TaskExecutionError(f"算例缺少 CloudPSS RID: {task.case_id}")

    server_id, server = _resolve_server(task, case.server_id, servers)
    token = decrypt_server_token(server)
    migrate_server_token_to_workspace_key(server_id, servers)

    submitted_at = datetime.now().isoformat()
    transition_task(task_id, "submitted", {"submitted_at": submitted_at, "server_id": server_id}, tasks)

    try:
        try:
            from cloudpss import Model, setToken
        except ImportError as exc:
            raise TaskExecutionError("缺少 cloudpss SDK，无法执行生产任务") from exc

        with _cloudpss_server_context(server.url):
            setToken(token)
            model = _load_task_model(Model, task, case.rid)

            transition_task(task_id, "running", {"started_at": datetime.now().isoformat()}, tasks)
            if task.type == "powerflow":
                job = model.runPowerFlow()
                job_status = _wait_for_job(job, timeout_seconds=timeout_seconds, poll_interval=poll_interval)
                if job_status != 1:
                    raise TaskExecutionError(f"CloudPSS 潮流任务失败: {getattr(job, 'id', 'unknown')}")
                result_id = IDGenerator.generate(EntityType.RESULT)
                cloudpss_result = job.result
                buses_table = cloudpss_result.getBuses()[0]
                branches_table = cloudpss_result.getBranches()[0]
                metadata = {
                    "data_source": "live_cloudpss",
                    "server_id": server_id,
                    "server_url": server.url,
                    "server_owner": server.owner,
                    "model_rid": case.rid,
                    "model_name": getattr(model, "name", ""),
                    "job_id": getattr(job, "id", None),
                    "job_status": job_status,
                    "bus_rows": _table_row_count(buses_table),
                    "branch_rows": _table_row_count(branches_table),
                }
                artifact_files, artifact_size, artifact_metadata = store_powerflow_result(
                    result_id,
                    buses_table=buses_table,
                    branches_table=branches_table,
                    metadata=metadata,
                )
                result_format = "powerflow"

            elif task.type == "emt":
                job = model.runEMT()
                job_status = _wait_for_job(job, timeout_seconds=timeout_seconds, poll_interval=poll_interval)
                if job_status != 1:
                    raise TaskExecutionError(f"CloudPSS EMT 任务失败: {getattr(job, 'id', 'unknown')}")
                result_id = IDGenerator.generate(EntityType.RESULT)
                cloudpss_result = job.result
                plots = list(cloudpss_result.getPlots())
                traces = _collect_emt_traces(cloudpss_result, plots, task.config)
                metadata = {
                    "data_source": "live_cloudpss",
                    "server_id": server_id,
                    "server_url": server.url,
                    "server_owner": server.owner,
                    "model_rid": case.rid,
                    "model_name": getattr(model, "name", ""),
                    "job_id": getattr(job, "id", None),
                    "job_status": job_status,
                }
                artifact_files, artifact_size, artifact_metadata = store_emt_result(
                    result_id,
                    plots=plots,
                    traces=traces,
                    metadata=metadata,
                )
                result_format = "emt"

            else:
                raise TaskExecutionError(f"暂不支持生产执行的任务类型: {task.type}")
    except TaskExecutionError:
        current = tasks.get(task_id)
        if current and current.status != "failed":
            transition_task(task_id, "failed", registry=tasks)
        raise
    except Exception as exc:
        current = tasks.get(task_id)
        if current and current.status != "failed":
            transition_task(task_id, "failed", registry=tasks)
        raise TaskExecutionError(f"CloudPSS 任务执行异常: {exc}") from exc

    result = Result(
        id=result_id,
        name=f"{task.name} result",
        task_id=task_id,
        case_id=task.case_id,
        format=result_format,
        size_bytes=artifact_size,
        files=artifact_files,
        metadata=artifact_metadata,
    )
    results.create(result_id, result)
    materialize_entity("result", result_id, result)
    completed_at = datetime.now().isoformat()
    transition_task(
        task_id,
        "completed",
        {
            "completed_at": completed_at,
            "result_id": result_id,
            "job_id": artifact_metadata.get("job_id"),
            "server_id": server_id,
        },
        tasks,
    )
    task_count = len(tasks.filter_by(case_id=task.case_id))
    cases.update(task.case_id, {"status": "active", "last_task_id": task_id, "task_count": task_count})
    updated_case = cases.get(task.case_id)
    if updated_case:
        materialize_entity("case", task.case_id, updated_case)
    write_audit("task.execute", task_id, {"result_id": result_id, "job_id": artifact_metadata.get("job_id")})
    refresh_index()

    return TaskExecutionResult(
        task_id=task_id,
        result_id=result_id,
        job_id=artifact_metadata.get("job_id"),
        status="completed",
        files=artifact_files,
        metadata=artifact_metadata,
    )


def _collect_emt_traces(
    cloudpss_result: Any,
    plots: list[dict[str, Any]],
    config: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    requested = config.get("channels") or config.get("emt_channels")
    selected: list[tuple[int, str]] = []

    if isinstance(requested, str):
        requested = [item.strip() for item in requested.split(",") if item.strip()]

    if requested:
        for item in requested:
            if isinstance(item, dict):
                selected.append((int(item.get("plot", 0)), str(item["channel"])))
            else:
                value = str(item)
                if "/" in value:
                    plot_part, channel = value.split("/", 1)
                    plot_index = int(plot_part.replace("plot-", ""))
                else:
                    plot_index, channel = 0, value
                selected.append((plot_index, channel))
    else:
        for plot_index, plot in enumerate(plots):
            for trace in plot.get("data", {}).get("traces", [])[:1]:
                name = trace.get("name")
                if name:
                    selected.append((plot_index, str(name)))

    traces: dict[str, dict[str, Any]] = {}
    for plot_index, channel in selected:
        trace = cloudpss_result.getPlotChannelData(plot_index, channel)
        if trace is not None:
            traces[f"plot-{plot_index}/{channel}"] = trace

    if not traces:
        raise TaskExecutionError("EMT 任务完成，但未能提取任何波形通道")
    return traces


def _load_task_model(model_cls: Any, task: Task, case_rid: str):
    model_source = task.config.get("model_source")
    if model_source:
        load = getattr(model_cls, "load", None)
        if not load:
            raise TaskExecutionError("当前 cloudpss SDK 不支持 Model.load，无法加载本地模型源")
        return load(str(Path(model_source).expanduser().resolve()))
    return model_cls.fetch(case_rid)


__all__ = [
    "TaskExecutionError",
    "TaskExecutionResult",
    "execute_task",
    "safe_artifact_name",
]
