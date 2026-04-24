"""Tests for cloudpss_skills_v2.tools.batch_task_manager."""

from __future__ import annotations

import threading
import time
from typing import Any

from cloudpss_skills_v2.core import SkillStatus
from cloudpss_skills_v2.tools.batch_task_manager import BatchTask, BatchTaskManagerTool


def test_validate_rejects_cycle() -> None:
    tool = BatchTaskManagerTool()

    valid, errors = tool.validate(
        {
            "tasks": [
                {"id": "task1", "skill": "power_flow", "depends_on": ["task2"]},
                {"id": "task2", "skill": "power_flow", "depends_on": ["task1"]},
            ]
        }
    )

    assert valid is False
    assert any("circular dependency detected" in error for error in errors)


def test_run_executes_dependencies_in_topological_order() -> None:
    tool = BatchTaskManagerTool()
    execution_order: list[str] = []

    def executor(task: BatchTask, dependency_results: dict[str, Any]) -> dict[str, Any]:
        execution_order.append(task.task_id)
        return {
            "task_id": task.task_id,
            "dependencies": sorted(dependency_results),
        }

    result = tool.run(
        {
            "max_workers": 3,
            "task_executor": executor,
            "tasks": [
                {"id": "root", "skill": "power_flow", "priority": 1},
                {
                    "id": "child_a",
                    "skill": "power_flow",
                    "depends_on": ["root"],
                    "priority": 1,
                },
                {
                    "id": "child_b",
                    "skill": "power_flow",
                    "depends_on": ["root"],
                    "priority": 2,
                },
            ],
        }
    )

    assert result.status == SkillStatus.SUCCESS
    assert execution_order[0] == "root"
    assert set(execution_order[1:]) == {"child_a", "child_b"}
    assert result.data["summary"]["completed_tasks"] == 3
    assert result.data["task_statuses"] == {
        "root": "completed",
        "child_a": "completed",
        "child_b": "completed",
    }
    assert result.data["summary"]["results"]["child_a"]["dependencies"] == ["root"]
    assert result.data["summary"]["results"]["child_b"]["dependencies"] == ["root"]


def test_run_executes_independent_tasks_concurrently() -> None:
    tool = BatchTaskManagerTool()
    started = threading.Event()
    release = threading.Event()
    active = 0
    peak_active = 0
    lock = threading.Lock()

    def executor(task: BatchTask, dependency_results: dict[str, Any]) -> dict[str, str]:
        nonlocal active, peak_active
        with lock:
            active += 1
            peak_active = max(peak_active, active)
            if active >= 2:
                started.set()

        assert started.wait(timeout=1)
        assert release.wait(timeout=1)

        with lock:
            active -= 1
        return {"task_id": task.task_id}

    timer = threading.Timer(0.2, release.set)
    timer.start()
    try:
        result = tool.run(
            {
                "max_workers": 2,
                "task_executor": executor,
                "tasks": [
                    {"id": "task1", "skill": "power_flow", "priority": 1},
                    {"id": "task2", "skill": "power_flow", "priority": 1},
                    {"id": "task3", "skill": "power_flow", "priority": 2},
                ],
            }
        )
    finally:
        timer.cancel()
        release.set()

    assert result.status == SkillStatus.SUCCESS
    assert peak_active >= 2
    assert result.data["summary"]["completed_tasks"] == 3


def test_run_retries_failed_task_until_success() -> None:
    tool = BatchTaskManagerTool()
    attempts = {"retry_me": 0}

    def executor(task: BatchTask, dependency_results: dict[str, Any]) -> dict[str, int]:
        attempts[task.task_id] += 1
        if attempts[task.task_id] < 3:
            raise RuntimeError("temporary failure")
        return {"attempts": attempts[task.task_id]}

    result = tool.run(
        {
            "max_retries": 2,
            "task_executor": executor,
            "tasks": [{"id": "retry_me", "skill": "power_flow"}],
        }
    )

    assert result.status == SkillStatus.SUCCESS
    assert attempts["retry_me"] == 3
    assert result.data["summary"]["completed_tasks"] == 1
    assert result.data["tasks"]["retry_me"]["attempts"] == 3
    assert result.data["summary"]["errors"] == []


def test_run_cancels_dependents_after_failure_when_continuing() -> None:
    tool = BatchTaskManagerTool()

    def executor(task: BatchTask, dependency_results: dict[str, Any]) -> dict[str, str]:
        if task.task_id == "root":
            raise RuntimeError("boom")
        return {"task_id": task.task_id}

    result = tool.run(
        {
            "continue_on_failure": True,
            "task_executor": executor,
            "tasks": [
                {"id": "root", "skill": "power_flow"},
                {"id": "child", "skill": "power_flow", "depends_on": ["root"]},
                {"id": "independent", "skill": "power_flow"},
            ],
        }
    )

    assert result.status == SkillStatus.FAILED
    assert result.data["task_statuses"]["root"] == "failed"
    assert result.data["task_statuses"]["child"] == "cancelled"
    assert result.data["task_statuses"]["independent"] == "completed"
    assert result.data["summary"]["failed_tasks"] == 1
    assert result.data["summary"]["cancelled_tasks"] == 1
    assert result.data["summary"]["completed_tasks"] == 1
    assert result.data["summary"]["errors"][0]["task_id"] == "root"


def test_run_stops_batch_when_continue_on_failure_is_disabled() -> None:
    tool = BatchTaskManagerTool()
    executed: list[str] = []

    def executor(task: BatchTask, dependency_results: dict[str, Any]) -> dict[str, str]:
        executed.append(task.task_id)
        if task.task_id == "first":
            raise RuntimeError("stop batch")
        time.sleep(0.05)
        return {"task_id": task.task_id}

    result = tool.run(
        {
            "max_workers": 1,
            "continue_on_failure": False,
            "task_executor": executor,
            "tasks": [
                {"id": "first", "skill": "power_flow"},
                {"id": "second", "skill": "power_flow"},
            ],
        }
    )

    assert result.status == SkillStatus.FAILED
    assert executed == ["first"]
    assert result.data["task_statuses"]["first"] == "failed"
    assert result.data["task_statuses"]["second"] == "cancelled"
