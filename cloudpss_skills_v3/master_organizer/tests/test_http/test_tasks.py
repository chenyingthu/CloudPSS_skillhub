"""Tests for task HTTP endpoints."""

import pytest
from unittest.mock import patch, MagicMock
from dataclasses import dataclass, field

from cloudpss_skills_v3.master_organizer.core import (
    ServerRegistry,
    Server,
    CaseRegistry,
    Case,
    IDGenerator,
    EntityType,
    get_path_manager,
)
from cloudpss_skills_v3.master_organizer.core.server_auth import build_auth_metadata
from cloudpss_skills_v3.master_organizer.portal.handlers import TaskHandler, CaseHandler


@dataclass
class MockTaskResult:
    """Mock task execution result."""
    task_id: str = "test-task"
    status: str = "completed"
    success: bool = True
    output: dict = field(default_factory=dict)
    error_message: str = ""


class TestTaskEndpoints:
    """Test task API endpoints."""

    def _setup_server_and_case(self, tmp_path, monkeypatch):
        """Helper to setup server and case for task tests."""
        monkeypatch.setenv("CLOUDPSS_HOME", str(tmp_path))
        get_path_manager(str(tmp_path))

        # Setup server
        server_id = IDGenerator.generate(EntityType.SERVER)
        ServerRegistry().create(
            server_id,
            Server(
                id=server_id,
                name="test-server",
                url="http://test.com/",
                owner="tester",
                auth=build_auth_metadata("token", {"token_source": "test"}),
                default=True,
            ),
        )

        # Setup case
        case_handler = CaseHandler()
        result, status = case_handler.create({
            "name": "Test Case",
            "rid": "model/test/case",
        })
        case_id = result["data"]["id"]

        return server_id, case_id

    def test_create_task_with_valid_data(self, tmp_path, monkeypatch):
        """Test POST /api/tasks creates a task."""
        server_id, case_id = self._setup_server_and_case(tmp_path, monkeypatch)

        handler = TaskHandler()
        result, status = handler.create({
            "name": "Power Flow Task",
            "case_id": case_id,
            "type": "powerflow",
            "config": {"solver": "newton"},
            "channels": ["bus", "line"],
        })

        assert status == 201
        assert "data" in result
        assert result["data"]["name"] == "Power Flow Task"
        assert result["data"]["case_id"] == case_id
        assert result["data"]["type"] == "powerflow"
        assert "id" in result["data"]

    def test_create_task_rejects_invalid_case(self, tmp_path, monkeypatch):
        """Test POST /api/tasks rejects invalid case_id."""
        monkeypatch.setenv("CLOUDPSS_HOME", str(tmp_path))
        get_path_manager(str(tmp_path))

        handler = TaskHandler()
        result, status = handler.create({
            "name": "Test Task",
            "case_id": "nonexistent-case",
            "type": "powerflow",
        })

        assert status == 404
        assert "error" in result
        assert result["error"]["code"] == "RESOURCE_NOT_FOUND"

    def test_create_task_rejects_invalid_rid(self, tmp_path, monkeypatch):
        """Test POST /api/tasks rejects case with invalid RID format."""
        monkeypatch.setenv("CLOUDPSS_HOME", str(tmp_path))
        get_path_manager(str(tmp_path))

        # Setup server
        server_id = IDGenerator.generate(EntityType.SERVER)
        ServerRegistry().create(
            server_id,
            Server(
                id=server_id,
                name="test-server",
                url="http://test.com/",
                owner="tester",
                auth=build_auth_metadata("token", {"token_source": "test"}),
                default=True,
            ),
        )

        # Create case with invalid RID directly in registry (bypassing validation)
        case_id = IDGenerator.generate(EntityType.CASE)
        invalid_case = Case(
            id=case_id,
            name="Invalid RID Case",
            rid="invalid-rid",  # Invalid format
            server_id=server_id,
            status="active",
        )
        CaseRegistry().create(case_id, invalid_case)

        handler = TaskHandler()
        result, status = handler.create({
            "name": "Test Task",
            "case_id": case_id,
            "type": "powerflow",
        })

        assert status == 422
        assert "error" in result
        assert result["error"]["code"] == "VALIDATION_ERROR"

    def test_get_task_returns_task_detail(self, tmp_path, monkeypatch):
        """Test GET /api/tasks/{id} returns task detail."""
        server_id, case_id = self._setup_server_and_case(tmp_path, monkeypatch)

        # Create task
        handler = TaskHandler()
        create_result, _ = handler.create({
            "name": "Test Task",
            "case_id": case_id,
            "type": "emt",
            "config": {"step": 0.001},
        })
        task_id = create_result["data"]["id"]

        # Get task
        result, status = handler.get(task_id)

        assert status == 200
        assert "data" in result
        assert result["data"]["name"] == "Test Task"
        assert result["data"]["type"] == "emt"
        assert result["data"]["case_id"] == case_id

    def test_get_nonexistent_task_returns_404(self, tmp_path, monkeypatch):
        """Test GET /api/tasks/{id} returns 404 for non-existent task."""
        monkeypatch.setenv("CLOUDPSS_HOME", str(tmp_path))
        get_path_manager(str(tmp_path))

        handler = TaskHandler()
        result, status = handler.get("nonexistent-task-id")

        assert status == 404
        assert "error" in result
        assert result["error"]["code"] == "RESOURCE_NOT_FOUND"

    def test_list_tasks_by_case(self, tmp_path, monkeypatch):
        """Test GET /api/tasks filters by case_id."""
        server_id, case_id = self._setup_server_and_case(tmp_path, monkeypatch)

        # Create multiple tasks for the same case
        handler = TaskHandler()
        for i in range(3):
            handler.create({
                "name": f"Task {i}",
                "case_id": case_id,
                "type": "powerflow",
            })

        # List tasks by case
        result, status = handler.list(case_id=case_id)

        assert status == 200
        assert "data" in result
        assert "items" in result["data"]
        assert len(result["data"]["items"]) == 3

    def test_list_tasks_with_pagination(self, tmp_path, monkeypatch):
        """Test GET /api/tasks supports pagination."""
        server_id, case_id = self._setup_server_and_case(tmp_path, monkeypatch)

        # Create multiple tasks
        handler = TaskHandler()
        for i in range(5):
            handler.create({
                "name": f"Task {i}",
                "case_id": case_id,
                "type": "powerflow",
            })

        # List with pagination
        result, status = handler.list(limit=2, offset=0)

        assert status == 200
        assert "data" in result
        assert "items" in result["data"]
        assert "pagination" in result["data"]
        assert len(result["data"]["items"]) == 2
        assert result["data"]["pagination"]["limit"] == 2

    def test_update_task_success(self, tmp_path, monkeypatch):
        """Test POST /api/tasks/{id} updates task."""
        server_id, case_id = self._setup_server_and_case(tmp_path, monkeypatch)

        # Create task
        handler = TaskHandler()
        create_result, _ = handler.create({
            "name": "Original Name",
            "case_id": case_id,
            "type": "powerflow",
        })
        task_id = create_result["data"]["id"]

        # Update task
        result, status = handler.update(task_id, {
            "name": "Updated Name",
            "config": {"solver": "fast_decoupled"},
        })

        assert status == 200
        assert "data" in result
        assert result["data"]["name"] == "Updated Name"

    def test_update_task_rejects_when_running(self, tmp_path, monkeypatch):
        """Test POST /api/tasks/{id} rejects update when task is running."""
        server_id, case_id = self._setup_server_and_case(tmp_path, monkeypatch)

        # Create task
        handler = TaskHandler()
        create_result, _ = handler.create({
            "name": "Running Task",
            "case_id": case_id,
            "type": "powerflow",
        })
        task_id = create_result["data"]["id"]

        # Simulate running state by modifying directly in registry
        from cloudpss_skills_v3.master_organizer.core import TaskRegistry
        registry = TaskRegistry()
        task = registry.get(task_id)
        if task:
            registry.update(task_id, {"status": "running"})

        # Try to update
        result, status = handler.update(task_id, {"name": "New Name"})

        assert status == 409
        assert "error" in result
        assert result["error"]["code"] == "STATE_ERROR"

    @patch("cloudpss_skills_v3.master_organizer.portal.handlers.tasks.execute_task")
    def test_run_task_success(self, mock_execute, tmp_path, monkeypatch):
        """Test POST /api/tasks/{id}/run executes task."""
        # Setup mock
        mock_execute.return_value = MockTaskResult(
            task_id="test-task",
            status="completed",
            success=True,
            output={"voltage": [1.0, 1.02]},
        )

        server_id, case_id = self._setup_server_and_case(tmp_path, monkeypatch)

        # Create task
        handler = TaskHandler()
        create_result, _ = handler.create({
            "name": "Runnable Task",
            "case_id": case_id,
            "type": "powerflow",
        })
        task_id = create_result["data"]["id"]

        # Run task
        result, status = handler.run(task_id, {"timeout": 60})

        assert status == 200
        assert result["data"]["status"] == "completed"
        assert result["data"]["success"] is True
        mock_execute.assert_called_once()

    def test_run_task_fails_preflight(self, tmp_path, monkeypatch):
        """Test POST /api/tasks/{id}/run fails preflight checks."""
        monkeypatch.setenv("CLOUDPSS_HOME", str(tmp_path))
        get_path_manager(str(tmp_path))

        # Create case without server
        case_handler = CaseHandler()
        result, _ = case_handler.create({
            "name": "Case Without Server",
            "rid": "model/test/case",
            "server_id": "",
        })
        case_id = result["data"]["id"]

        # Create task
        handler = TaskHandler()
        create_result, _ = handler.create({
            "name": "Task With Bad Case",
            "case_id": case_id,
            "type": "powerflow",
        })
        task_id = create_result["data"]["id"]

        # Try to run
        result, status = handler.run(task_id, {})

        assert status == 422
        assert "error" in result
        assert result["error"]["code"] == "PREFLIGHT_FAILED"

    def test_preflight_checks(self, tmp_path, monkeypatch):
        """Test GET /api/tasks/{id}/preflight returns checks."""
        server_id, case_id = self._setup_server_and_case(tmp_path, monkeypatch)

        # Create task
        handler = TaskHandler()
        create_result, _ = handler.create({
            "name": "Test Task",
            "case_id": case_id,
            "type": "emt",
            "channels": ["bus1", "bus2"],
        })
        task_id = create_result["data"]["id"]

        # Get preflight
        result, status = handler.preflight(task_id)

        assert status == 200
        assert "data" in result
        assert "ok" in result["data"]
        assert "checks" in result["data"]
        assert len(result["data"]["checks"]) > 0

        # Check EMT channels
        emt_check = next(
            (c for c in result["data"]["checks"] if c["name"] == "EMT Channels"),
            None
        )
        assert emt_check is not None
        assert "bus1, bus2" in emt_check["message"]

    def test_task_logs(self, tmp_path, monkeypatch):
        """Test GET /api/tasks/{id}/logs returns logs placeholder."""
        server_id, case_id = self._setup_server_and_case(tmp_path, monkeypatch)

        # Create task
        handler = TaskHandler()
        create_result, _ = handler.create({
            "name": "Test Task",
            "case_id": case_id,
            "type": "powerflow",
        })
        task_id = create_result["data"]["id"]

        # Get logs
        result, status = handler.logs(task_id)

        assert status == 200
        assert "data" in result
        assert result["data"]["task_id"] == task_id
        assert "logs" in result["data"]
