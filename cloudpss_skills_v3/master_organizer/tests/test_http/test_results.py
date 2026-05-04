"""Tests for result HTTP endpoints."""

import pytest
from datetime import datetime
from dataclasses import dataclass, field

from cloudpss_skills_v3.master_organizer.core import (
    ServerRegistry,
    Server,
    CaseRegistry,
    Case,
    TaskRegistry,
    Task,
    ResultRegistry,
    Result,
    IDGenerator,
    EntityType,
    get_path_manager,
)
from cloudpss_skills_v3.master_organizer.core.server_auth import build_auth_metadata
from cloudpss_skills_v3.master_organizer.portal.handlers import ResultHandler, CaseHandler, TaskHandler


@dataclass
class MockResultData:
    """Mock result data for testing."""
    task_id: str
    status: str = "completed"
    success: bool = True
    output: dict = field(default_factory=dict)
    metrics: dict = field(default_factory=dict)
    created_at: str = ""


class TestResultEndpoints:
    """Test result API endpoints."""

    def _setup_full_workflow(self, tmp_path, monkeypatch):
        """Helper to setup server, case, task for result tests."""
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
        result, _ = case_handler.create({
            "name": "Test Case",
            "rid": "model/test/case",
        })
        case_id = result["data"]["id"]

        # Setup task
        task_handler = TaskHandler()
        task_result, _ = task_handler.create({
            "name": "Test Task",
            "case_id": case_id,
            "type": "powerflow",
        })
        task_id = task_result["data"]["id"]

        return server_id, case_id, task_id

    def test_get_result_returns_result_detail(self, tmp_path, monkeypatch):
        """Test GET /api/results/{id} returns result detail."""
        server_id, case_id, task_id = self._setup_full_workflow(tmp_path, monkeypatch)

        # Create result directly
        result_id = IDGenerator.generate(EntityType.RESULT)
        result_data = Result(
            id=result_id,
            task_id=task_id,
            status="completed",
            success=True,
            output={"voltage": [1.0, 0.95, 1.02]},
            metrics={"iterations": 5, "time": 0.5},
        )
        ResultRegistry().create(result_id, result_data)

        handler = ResultHandler()
        result, status = handler.get(result_id)

        assert status == 200
        assert "data" in result
        assert result["data"]["task_id"] == task_id
        assert result["data"]["status"] == "completed"
        assert result["data"]["success"] is True

    def test_get_nonexistent_result_returns_404(self, tmp_path, monkeypatch):
        """Test GET /api/results/{id} returns 404 for non-existent result."""
        monkeypatch.setenv("CLOUDPSS_HOME", str(tmp_path))
        get_path_manager(str(tmp_path))

        handler = ResultHandler()
        result, status = handler.get("nonexistent-result-id")

        assert status == 404
        assert "error" in result
        assert result["error"]["code"] == "RESOURCE_NOT_FOUND"

    def test_list_results_by_task(self, tmp_path, monkeypatch):
        """Test GET /api/results filters by task_id."""
        server_id, case_id, task_id = self._setup_full_workflow(tmp_path, monkeypatch)

        # Create multiple results for the same task
        for i in range(3):
            result_id = IDGenerator.generate(EntityType.RESULT)
            result_data = Result(
                id=result_id,
                task_id=task_id,
                status="completed",
                success=True,
                output={"run": i},
            )
            ResultRegistry().create(result_id, result_data)

        handler = ResultHandler()
        result, status = handler.list(task_id=task_id)

        assert status == 200
        assert "data" in result
        assert "items" in result["data"]
        assert len(result["data"]["items"]) == 3

    def test_list_results_by_status(self, tmp_path, monkeypatch):
        """Test GET /api/results filters by status."""
        server_id, case_id, task_id = self._setup_full_workflow(tmp_path, monkeypatch)

        # Create results with different statuses
        for status in ["completed", "failed", "completed"]:
            result_id = IDGenerator.generate(EntityType.RESULT)
            result_data = Result(
                id=result_id,
                task_id=task_id,
                status=status,
                success=(status == "completed"),
            )
            ResultRegistry().create(result_id, result_data)

        handler = ResultHandler()
        result, status = handler.list(status="completed")

        assert status == 200
        assert len(result["data"]["items"]) == 2

    def test_list_results_with_pagination(self, tmp_path, monkeypatch):
        """Test GET /api/results supports pagination."""
        server_id, case_id, task_id = self._setup_full_workflow(tmp_path, monkeypatch)

        # Create multiple results
        for i in range(5):
            result_id = IDGenerator.generate(EntityType.RESULT)
            result_data = Result(
                id=result_id,
                task_id=task_id,
                status="completed",
                success=True,
            )
            ResultRegistry().create(result_id, result_data)

        handler = ResultHandler()
        result, status = handler.list(limit=2, offset=0)

        assert status == 200
        assert len(result["data"]["items"]) == 2
        assert result["data"]["pagination"]["limit"] == 2

    def test_delete_result_success(self, tmp_path, monkeypatch):
        """Test DELETE /api/results/{id} removes result."""
        server_id, case_id, task_id = self._setup_full_workflow(tmp_path, monkeypatch)

        # Create result
        result_id = IDGenerator.generate(EntityType.RESULT)
        result_data = Result(
            id=result_id,
            task_id=task_id,
            status="completed",
            success=True,
        )
        ResultRegistry().create(result_id, result_data)

        handler = ResultHandler()
        result, status = handler.delete(result_id)

        assert status == 200
        assert result["data"]["deleted"] is True

        # Verify it's gone
        get_result, get_status = handler.get(result_id)
        assert get_status == 404

    def test_delete_nonexistent_result_returns_404(self, tmp_path, monkeypatch):
        """Test DELETE /api/results/{id} returns 404 for non-existent result."""
        monkeypatch.setenv("CLOUDPSS_HOME", str(tmp_path))
        get_path_manager(str(tmp_path))

        handler = ResultHandler()
        result, status = handler.delete("nonexistent-result-id")

        assert status == 404
        assert "error" in result
        assert result["error"]["code"] == "RESOURCE_NOT_FOUND"

    def test_result_with_metrics(self, tmp_path, monkeypatch):
        """Test result includes metrics in response."""
        server_id, case_id, task_id = self._setup_full_workflow(tmp_path, monkeypatch)

        # Create result with metrics
        result_id = IDGenerator.generate(EntityType.RESULT)
        result_data = Result(
            id=result_id,
            task_id=task_id,
            status="completed",
            success=True,
            output={"voltage": [1.0]},
            metrics={
                "iterations": 5,
                "convergence_time": 0.123,
                "memory_usage_mb": 45.6,
            },
        )
        ResultRegistry().create(result_id, result_data)

        handler = ResultHandler()
        result, status = handler.get(result_id)

        assert status == 200
        assert "metrics" in result["data"]
        assert result["data"]["metrics"]["iterations"] == 5

    def test_result_with_output_data(self, tmp_path, monkeypatch):
        """Test result includes output data in response."""
        server_id, case_id, task_id = self._setup_full_workflow(tmp_path, monkeypatch)

        # Create result with output data
        result_id = IDGenerator.generate(EntityType.RESULT)
        result_data = Result(
            id=result_id,
            task_id=task_id,
            status="completed",
            success=True,
            output={
                "buses": [
                    {"id": 1, "v": 1.0, "angle": 0.0},
                    {"id": 2, "v": 0.95, "angle": -5.2},
                ],
                "branches": [
                    {"from": 1, "to": 2, "p": 100.5, "q": 25.3},
                ],
            },
        )
        ResultRegistry().create(result_id, result_data)

        handler = ResultHandler()
        result, status = handler.get(result_id)

        assert status == 200
        assert "output" in result["data"]
        assert len(result["data"]["output"]["buses"]) == 2
