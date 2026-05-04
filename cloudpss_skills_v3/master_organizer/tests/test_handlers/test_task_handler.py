"""Unit tests for TaskHandler."""

import pytest
from unittest.mock import patch, MagicMock

from cloudpss_skills_v3.master_organizer.core import (
    CaseRegistry,
    ServerRegistry,
    Server,
    Case,
    TaskRegistry,
    Task,
    IDGenerator,
    EntityType,
    get_path_manager,
)
from cloudpss_skills_v3.master_organizer.core.server_auth import build_auth_metadata
from cloudpss_skills_v3.master_organizer.portal.handlers import TaskHandler, CaseHandler


class TestTaskHandlerUnit:
    """Unit tests for TaskHandler."""

    @pytest.fixture(autouse=True)
    def setup(self, tmp_path, monkeypatch):
        """Setup test environment."""
        monkeypatch.setenv("CLOUDPSS_HOME", str(tmp_path))
        get_path_manager(str(tmp_path))
        yield
        # Cleanup registries
        CaseRegistry()._data.clear()
        TaskRegistry()._data.clear()
        ServerRegistry()._data.clear()

    def _create_test_case(self):
        """Helper to create a test case."""
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

        # Create case
        case_handler = CaseHandler()
        result, _ = case_handler.create({
            "name": "Test Case",
            "rid": "model/test/case",
        })
        return result["data"]["id"]

    def test_create_task_success(self):
        """Test creating a task with valid data."""
        case_id = self._create_test_case()

        handler = TaskHandler()
        result, status = handler.create({
            "name": "Power Flow Task",
            "case_id": case_id,
            "type": "powerflow",
            "config": {"solver": "newton"},
        })

        assert status == 201
        assert "error" not in result or result["error"] is None
        assert result["data"]["name"] == "Power Flow Task"
        assert result["data"]["type"] == "powerflow"
        assert result["data"]["case_id"] == case_id

    def test_create_task_missing_name(self):
        """Test creating a task without name uses default."""
        case_id = self._create_test_case()

        handler = TaskHandler()
        result, status = handler.create({
            "case_id": case_id,
            "type": "powerflow",
        })

        # Should use default name "{type} task"
        assert status == 201
        assert result["data"]["name"] == "powerflow task"

    def test_create_task_invalid_case(self):
        """Test creating a task with invalid case_id."""
        handler = TaskHandler()
        result, status = handler.create({
            "name": "Test Task",
            "case_id": "nonexistent-case",
            "type": "powerflow",
        })

        assert status == 404
        assert result["error"] is not None
        assert result["error"]["code"] == "RESOURCE_NOT_FOUND"

    def test_create_task_invalid_rid_case(self):
        """Test creating a task for case with invalid RID."""
        # Create case with invalid RID directly
        case_id = IDGenerator.generate(EntityType.CASE)
        invalid_case = Case(
            id=case_id,
            name="Invalid RID Case",
            rid="invalid-rid",
            server_id="",
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
        assert result["error"]["code"] == "VALIDATION_ERROR"

    def test_get_task_success(self):
        """Test getting a task by ID."""
        case_id = self._create_test_case()

        handler = TaskHandler()
        create_result, _ = handler.create({
            "name": "Test Task",
            "case_id": case_id,
            "type": "emt",
        })
        task_id = create_result["data"]["id"]

        result, status = handler.get(task_id)

        assert status == 200
        assert "error" not in result or result["error"] is None
        assert result["data"]["name"] == "Test Task"
        assert result["data"]["type"] == "emt"

    def test_get_task_not_found(self):
        """Test getting non-existent task returns 404."""
        handler = TaskHandler()
        result, status = handler.get("nonexistent-id")

        assert status == 404
        assert result["error"]["code"] == "RESOURCE_NOT_FOUND"

    def test_list_tasks_empty(self):
        """Test listing tasks when none exist."""
        handler = TaskHandler()
        result, status = handler.list()

        assert status == 200
        assert result["data"]["items"] == []

    def test_list_tasks_by_case(self):
        """Test listing tasks filtered by case."""
        case_id = self._create_test_case()

        handler = TaskHandler()
        handler.create({"name": "Task 1", "case_id": case_id, "type": "powerflow"})
        handler.create({"name": "Task 2", "case_id": case_id, "type": "emt"})

        result, status = handler.list(case_id=case_id)

        assert status == 200
        assert len(result["data"]["items"]) == 2

    def test_list_tasks_with_status_filter(self):
        """Test listing tasks with status filter."""
        case_id = self._create_test_case()

        handler = TaskHandler()
        handler.create({"name": "Task 1", "case_id": case_id, "type": "powerflow"})

        result, status = handler.list(status="created")

        assert status == 200
        # New tasks have status "created"
        assert len(result["data"]["items"]) == 1

    def test_update_task_success(self):
        """Test updating a task."""
        case_id = self._create_test_case()

        handler = TaskHandler()
        create_result, _ = handler.create({
            "name": "Original Name",
            "case_id": case_id,
            "type": "powerflow",
        })
        task_id = create_result["data"]["id"]

        result, status = handler.update(task_id, {
            "name": "Updated Name",
            "config": {"solver": "fast_decoupled"},
        })

        assert status == 200
        assert result["data"]["name"] == "Updated Name"

    def test_update_task_not_found(self):
        """Test updating non-existent task returns 404."""
        handler = TaskHandler()
        result, status = handler.update("nonexistent-id", {"name": "New Name"})

        assert status == 404
        assert result["error"]["code"] == "RESOURCE_NOT_FOUND"

    def test_update_task_wrong_state(self):
        """Test updating task in wrong state returns error."""
        case_id = self._create_test_case()

        handler = TaskHandler()
        create_result, _ = handler.create({
            "name": "Test Task",
            "case_id": case_id,
            "type": "powerflow",
        })
        task_id = create_result["data"]["id"]

        # Simulate running state
        TaskRegistry().update(task_id, {"status": "running"})

        result, status = handler.update(task_id, {"name": "New Name"})

        assert status == 409
        assert result["error"]["code"] == "STATE_ERROR"

    @patch("cloudpss_skills_v3.master_organizer.portal.handlers.tasks.execute_task")
    def test_run_task_success(self, mock_execute):
        """Test running a task."""
        from dataclasses import dataclass

        @dataclass
        class MockResult:
            task_id: str
            status: str = "completed"
            success: bool = True
            output: dict = None

        mock_execute.return_value = MockResult(
            task_id="test",
            status="completed",
            success=True,
            output={"voltage": [1.0]},
        )

        case_id = self._create_test_case()

        handler = TaskHandler()
        create_result, _ = handler.create({
            "name": "Runnable Task",
            "case_id": case_id,
            "type": "powerflow",
        })
        task_id = create_result["data"]["id"]

        result, status = handler.run(task_id, {"timeout": 60})

        assert status == 200
        mock_execute.assert_called_once()

    def test_run_task_preflight_fails(self):
        """Test running a task with failing preflight."""
        # Create case without server
        case_id = IDGenerator.generate(EntityType.CASE)
        case = Case(
            id=case_id,
            name="No Server Case",
            rid="model/test/case",
            server_id="",
            status="active",
        )
        CaseRegistry().create(case_id, case)

        handler = TaskHandler()
        create_result, _ = handler.create({
            "name": "Task With Bad Case",
            "case_id": case_id,
            "type": "powerflow",
        })
        task_id = create_result["data"]["id"]

        result, status = handler.run(task_id, {})

        assert status == 422
        assert result["error"]["code"] == "PREFLIGHT_FAILED"

    def test_preflight_checks(self):
        """Test preflight checks."""
        case_id = self._create_test_case()

        handler = TaskHandler()
        create_result, _ = handler.create({
            "name": "Test Task",
            "case_id": case_id,
            "type": "emt",
            "channels": ["bus1", "bus2"],
        })
        task_id = create_result["data"]["id"]

        result, status = handler.preflight(task_id)

        assert status == 200
        assert "data" in result
        assert "checks" in result["data"]
        assert "ok" in result["data"]

        # Check EMT channels check exists
        emt_check = next(
            (c for c in result["data"]["checks"] if c["name"] == "EMT Channels"),
            None
        )
        assert emt_check is not None

    def test_logs_placeholder(self):
        """Test logs endpoint returns placeholder."""
        case_id = self._create_test_case()

        handler = TaskHandler()
        create_result, _ = handler.create({
            "name": "Test Task",
            "case_id": case_id,
            "type": "powerflow",
        })
        task_id = create_result["data"]["id"]

        result, status = handler.logs(task_id)

        assert status == 200
        assert result["data"]["task_id"] == task_id
        assert "logs" in result["data"]

    def test_task_type_validation(self):
        """Test task type is validated during creation."""
        case_id = self._create_test_case()

        handler = TaskHandler()
        result, status = handler.create({
            "name": "Test Task",
            "case_id": case_id,
            "type": "invalid_type",
        })

        # Should fail validation during creation
        assert status == 422
        assert result["error"] is not None
        assert "type" in result["error"]["message"].lower() or "task" in result["error"]["message"].lower()
