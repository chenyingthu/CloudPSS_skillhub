"""Batch Task Manager Skill v2."""
from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from graphlib import CycleError, TopologicalSorter
import importlib
import time
from typing import Any, TypeAlias, cast

from cloudpss_skills_v2.core import Artifact, LogEntry, SkillResult, SkillStatus

TaskPayload: TypeAlias = dict[str, Any]
TaskResultValue: TypeAlias = Any
TaskExecutor: TypeAlias = Callable[["BatchTask", TaskPayload], TaskResultValue]
LogContext: TypeAlias = Mapping[str, object]


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class BatchTask:
    task_id: str = ""
    skill: str = ""
    model_rid: str = ""
    job_type: str = ""
    status: str = TaskStatus.PENDING.value
    result: TaskResultValue = None
    priority: int = 0
    depends_on: list[str] = field(default_factory=list)
    config: TaskPayload = field(default_factory=dict)
    retries: int = 0
    attempts: int = 0
    error: str | None = None


@dataclass
class BatchTaskResult:
    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    cancelled_tasks: int = 0
    running_tasks: int = 0
    pending_tasks: int = 0
    results: dict[str, TaskResultValue] = field(default_factory=dict)
    errors: list[dict[str, object]] = field(default_factory=list)
    execution_time: float = 0.0


class BatchTaskManagerTool:
    name: str = "batch_task_manager"

    def __init__(self) -> None:
        self.logs: list[LogEntry] = []
        self.artifacts: list[Artifact] = []

    def _log(
        self,
        level: str,
        message: str,
        context: LogContext | None = None,
    ) -> None:
        self.logs.append(
            LogEntry(
                timestamp=datetime.now(),
                level=level.lower(),
                message=message,
                context=dict(context) if context is not None else None,
            )
        )

    def validate(self, config: dict[str, Any] | None = None) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if not config:
            errors.append("config is required")
            return (False, errors)

        raw_tasks = config.get("tasks")
        if not isinstance(raw_tasks, list) or not raw_tasks:
            errors.append("tasks must be a non-empty list")
            return (False, errors)

        tasks = cast(list[object], raw_tasks)
        task_ids: set[str] = set()
        for index, raw_task in enumerate(tasks):
            if not isinstance(raw_task, dict):
                errors.append(f"task at index {index} must be a mapping")
                continue

            task = cast(dict[str, Any], raw_task)
            task_id = task.get("id")
            if not isinstance(task_id, str) or not task_id:
                errors.append(f"task at index {index} must define string id")
            elif task_id in task_ids:
                errors.append(f"duplicate task id: {task_id}")
            else:
                task_ids.add(task_id)

            skill = task.get("skill")
            if not isinstance(skill, str) or not skill:
                errors.append(f"task {task.get('id', index)} must define string skill")

            depends_on = task.get("depends_on", [])
            if depends_on is not None and not isinstance(depends_on, list):
                errors.append(f"task {task.get('id', index)} depends_on must be a list")

        if errors:
            return (False, errors)

        graph: dict[str, set[str]] = {}
        for raw_task in tasks:
            task = cast(dict[str, Any], raw_task)
            task_id = cast(str, task["id"])
            dependencies = cast(list[object], task.get("depends_on", []) or [])
            dependency_ids: set[str] = set()
            for dependency in dependencies:
                if not isinstance(dependency, str) or dependency not in task_ids:
                    errors.append(f"task {task_id} depends on unknown task {dependency}")
                else:
                    dependency_ids.add(dependency)
            graph[task_id] = dependency_ids

        if errors:
            return (False, errors)

        try:
            _ = tuple(TopologicalSorter[str](graph).static_order())
        except CycleError as exc:
            cycle_nodes = list(cast(Iterable[object], exc.args[1])) if len(exc.args) > 1 else []
            errors.append(f"circular dependency detected: {cycle_nodes}")

        max_workers = config.get("max_workers", 4)
        if not isinstance(max_workers, int) or max_workers < 1:
            errors.append("max_workers must be a positive integer")

        max_retries = config.get("max_retries", 0)
        if not isinstance(max_retries, int) or max_retries < 0:
            errors.append("max_retries must be a non-negative integer")

        return (len(errors) == 0, errors)

    def _build_tasks(self, config: dict[str, Any]) -> dict[str, BatchTask]:
        tasks: dict[str, BatchTask] = {}
        for raw_item in cast(list[dict[str, Any]], config.get("tasks", [])):
            task_config = dict(raw_item)
            model = task_config.get("model")
            model_rid = ""
            if isinstance(model, dict):
                model_rid = str(model.get("rid", ""))
            elif isinstance(model, str):
                model_rid = model

            task_id = cast(str, task_config["id"])
            skill = cast(str, task_config["skill"])
            batch_task = BatchTask(
                task_id=task_id,
                skill=skill,
                model_rid=model_rid,
                job_type=str(task_config.get("job_type", skill)),
                priority=int(task_config.get("priority", 0)),
                depends_on=list(cast(list[str], task_config.get("depends_on", []) or [])),
                config=task_config,
                retries=int(task_config.get("max_retries", config.get("max_retries", 0))),
            )
            tasks[batch_task.task_id] = batch_task
        return tasks

    def _build_sorter(self, tasks: dict[str, BatchTask]) -> TopologicalSorter[str]:
        sorter: TopologicalSorter[str] = TopologicalSorter()
        for task in tasks.values():
            sorter.add(task.task_id, *task.depends_on)
        return sorter

    def _resolve_executor(self, config: dict[str, Any]) -> TaskExecutor:
        executor = config.get("task_executor")
        if callable(executor):
            return cast(TaskExecutor, executor)

        if isinstance(executor, str):
            module_name, _, attr_name = executor.rpartition(".")
            if not module_name or not attr_name:
                raise ValueError("task_executor string must be a dotted import path")
            module = importlib.import_module(module_name)
            resolved = getattr(module, attr_name)
            if not callable(resolved):
                raise TypeError("resolved task_executor is not callable")
            return cast(TaskExecutor, resolved)

        def _default_executor(task: BatchTask, dependency_results: TaskPayload) -> TaskPayload:
            return {
                "task_id": task.task_id,
                "skill": task.skill,
                "model_rid": task.model_rid,
                "job_type": task.job_type,
                "depends_on_results": dependency_results,
            }

        return _default_executor

    def _run_single_task(
        self,
        task: BatchTask,
        dependency_results: TaskPayload,
        executor: TaskExecutor,
        retry_delay: float,
    ) -> Any:
        last_error: Exception | None = None
        total_attempts = task.retries + 1
        for attempt in range(1, total_attempts + 1):
            task.attempts = attempt
            try:
                return executor(task, dependency_results)
            except Exception as exc:
                last_error = exc
                task.error = str(exc)
                self._log(
                    "warning",
                    f"Task {task.task_id} attempt {attempt}/{total_attempts} failed",
                    {"task_id": task.task_id, "attempt": attempt, "error": str(exc)},
                )
                if attempt < total_attempts and retry_delay > 0:
                    time.sleep(retry_delay)

        if last_error is None:
            raise RuntimeError(f"Task {task.task_id} failed without an exception")
        raise last_error

    def _cancel_blocked_tasks(
        self,
        failed_task_id: str,
        tasks: dict[str, BatchTask],
        dependents: dict[str, set[str]],
        sorter: TopologicalSorter[str],
    ) -> None:
        queue = list(dependents.get(failed_task_id, set()))
        visited: set[str] = set()
        while queue:
            task_id = queue.pop(0)
            if task_id in visited:
                continue
            visited.add(task_id)

            task = tasks[task_id]
            if task.status == TaskStatus.PENDING.value:
                task.status = TaskStatus.CANCELLED.value
                task.error = f"Cancelled because dependency {failed_task_id} failed"
                self._log(
                    "warning",
                    f"Task {task_id} cancelled due to failed dependency",
                    {"task_id": task_id, "failed_dependency": failed_task_id},
                )
            queue.extend(dependents.get(task_id, set()))

    def _snapshot(self, tasks: Iterable[BatchTask]) -> dict[str, str]:
        return {task.task_id: task.status for task in tasks}

    def run(self, config: dict[str, Any] | None = None) -> SkillResult:
        start_time = datetime.now()
        self.logs = []
        self.artifacts = []
        if config is None:
            config = {}

        valid, errors = self.validate(config)
        if not valid:
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error="; ".join(errors),
                logs=self.logs,
                start_time=start_time,
                end_time=datetime.now(),
            )

        batch_tasks = self._build_tasks(config)
        sorter = self._build_sorter(batch_tasks)
        dependents: dict[str, set[str]] = {task_id: set() for task_id in batch_tasks}
        for task in batch_tasks.values():
            for dependency in task.depends_on:
                dependents[dependency].add(task.task_id)

        max_workers = cast(int, config.get("max_workers", 4))
        continue_on_failure = bool(config.get("continue_on_failure", True))
        retry_delay = float(config.get("retry_delay", 0.0))
        executor_fn = self._resolve_executor(config)

        aggregate = BatchTaskResult(total_tasks=len(batch_tasks), pending_tasks=len(batch_tasks))
        task_results: dict[str, TaskResultValue] = {}
        task_errors: list[dict[str, Any]] = []

        sorter.prepare()
        running: dict[Future[Any], str] = {}
        ready_queue: list[str] = []

        def schedule_ready(executor_pool: ThreadPoolExecutor) -> None:
            ready_queue.extend(list(sorter.get_ready()))
            ready_ids = list(dict.fromkeys(ready_queue))
            ready_ids.sort(key=lambda item: (batch_tasks[item].priority, item))
            available_slots = max_workers - len(running)
            ready_to_schedule = ready_ids[:available_slots]
            ready_queue.clear()
            ready_queue.extend(ready_ids[available_slots:])

            for task_id in ready_to_schedule:
                task = batch_tasks[task_id]
                if task.status != TaskStatus.PENDING.value:
                    sorter.done(task_id)
                    continue

                dependency_results = {
                    dependency_id: task_results[dependency_id]
                    for dependency_id in task.depends_on
                    if dependency_id in task_results
                }
                task.status = TaskStatus.RUNNING.value
                aggregate.pending_tasks -= 1
                aggregate.running_tasks += 1
                self._log(
                    "info",
                    f"Starting task {task_id}",
                    {"task_id": task_id, "skill": task.skill, "priority": task.priority},
                )
                future = executor_pool.submit(
                    self._run_single_task,
                    task,
                    dependency_results,
                    executor_fn,
                    retry_delay,
                )
                running[future] = task_id

        try:
            with ThreadPoolExecutor(max_workers=max_workers) as executor_pool:
                while sorter.is_active() or running:
                    schedule_ready(executor_pool)
                    if not running:
                        continue

                    done, _pending = wait(tuple(running.keys()), return_when=FIRST_COMPLETED)
                    for future in done:
                        task_id = running.pop(future)
                        task = batch_tasks[task_id]
                        aggregate.running_tasks -= 1

                        try:
                            task_result = future.result()
                            task.status = TaskStatus.COMPLETED.value
                            task.result = task_result
                            task_results[task_id] = task_result
                            aggregate.completed_tasks += 1
                            self._log(
                                "info",
                                f"Task {task_id} completed",
                                {"task_id": task_id, "attempts": task.attempts},
                            )
                        except Exception as exc:
                            task.status = TaskStatus.FAILED.value
                            task.error = str(exc)
                            aggregate.failed_tasks += 1
                            error_entry = {
                                "task_id": task_id,
                                "error": str(exc),
                                "attempts": task.attempts,
                            }
                            task_errors.append(error_entry)
                            self._log("error", f"Task {task_id} failed", error_entry)

                            if continue_on_failure:
                                self._cancel_blocked_tasks(task_id, batch_tasks, dependents, sorter)
                            else:
                                for other_task in batch_tasks.values():
                                    if other_task.status == TaskStatus.PENDING.value:
                                        other_task.status = TaskStatus.CANCELLED.value
                                        other_task.error = "Cancelled after batch failure"
                                for running_future, running_task_id in list(running.items()):
                                    if running_future.cancel():
                                        _ = running.pop(running_future, None)
                                        aggregate.running_tasks -= 1
                                        cancelled_task = batch_tasks[running_task_id]
                                        cancelled_task.status = TaskStatus.CANCELLED.value
                                        cancelled_task.error = "Cancelled after batch failure"
                                break

                        sorter.done(task_id)

                    if not continue_on_failure and aggregate.failed_tasks:
                        break
        except Exception as exc:
            self._log("error", "Batch execution failed unexpectedly", {"error": str(exc)})
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error=str(exc),
                logs=self.logs,
                start_time=start_time,
                end_time=datetime.now(),
            )

        aggregate.cancelled_tasks = sum(
            1 for task in batch_tasks.values() if task.status == TaskStatus.CANCELLED.value
        )
        aggregate.pending_tasks = sum(
            1 for task in batch_tasks.values() if task.status == TaskStatus.PENDING.value
        )
        aggregate.running_tasks = sum(
            1 for task in batch_tasks.values() if task.status == TaskStatus.RUNNING.value
        )
        aggregate.results = task_results
        aggregate.errors = task_errors
        aggregate.execution_time = (datetime.now() - start_time).total_seconds()

        task_statuses = self._snapshot(batch_tasks.values())
        result_status = SkillStatus.SUCCESS if aggregate.failed_tasks == 0 else SkillStatus.FAILED
        result_data = {
            "summary": asdict(aggregate),
            "task_statuses": task_statuses,
            "tasks": {task_id: asdict(task) for task_id, task in batch_tasks.items()},
        }
        metrics = {
            "total_tasks": aggregate.total_tasks,
            "completed_tasks": aggregate.completed_tasks,
            "failed_tasks": aggregate.failed_tasks,
            "cancelled_tasks": aggregate.cancelled_tasks,
            "execution_time": aggregate.execution_time,
        }

        return SkillResult(
            skill_name=self.name,
            status=result_status,
            data=result_data,
            logs=self.logs,
            artifacts=self.artifacts,
            metrics=metrics,
            error=None if result_status == SkillStatus.SUCCESS else "One or more batch tasks failed",
            start_time=start_time,
            end_time=datetime.now(),
        )


__all__ = ["BatchTaskManagerTool", "TaskStatus", "BatchTask", "BatchTaskResult"]
