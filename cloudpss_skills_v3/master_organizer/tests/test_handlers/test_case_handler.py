"""Unit tests for CaseHandler."""

import pytest
from unittest.mock import patch, MagicMock

from cloudpss_skills_v3.master_organizer.core import (
    CaseRegistry,
    ServerRegistry,
    Server,
    Case,
    IDGenerator,
    EntityType,
    get_path_manager,
)
from cloudpss_skills_v3.master_organizer.core.server_auth import build_auth_metadata
from cloudpss_skills_v3.master_organizer.portal.handlers import CaseHandler


class TestCaseHandlerUnit:
    """Unit tests for CaseHandler."""

    @pytest.fixture(autouse=True)
    def setup(self, tmp_path, monkeypatch):
        """Setup test environment."""
        monkeypatch.setenv("CLOUDPSS_HOME", str(tmp_path))
        get_path_manager(str(tmp_path))
        yield
        # Cleanup registries
        CaseRegistry()._data.clear()
        ServerRegistry()._data.clear()

    def test_create_case_success(self):
        """Test creating a case with valid data."""
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

        handler = CaseHandler()
        result, status = handler.create({
            "name": "Test Case",
            "rid": "model/test/case",
            "tags": ["test", "powerflow"],
        })

        assert status == 201
        assert "error" not in result or result["error"] is None
        assert result["data"]["name"] == "Test Case"
        assert result["data"]["rid"] == "model/test/case"
        assert "id" in result["data"]

    def test_create_case_missing_name(self):
        """Test creating a case without name fails."""
        handler = CaseHandler()
        result, status = handler.create({
            "rid": "model/test/case",
        })

        assert status == 422
        assert result["error"] is not None
        assert result["error"]["code"] == "VALIDATION_ERROR"

    def test_create_case_invalid_rid(self):
        """Test creating a case with invalid RID fails."""
        handler = CaseHandler()
        result, status = handler.create({
            "name": "Test Case",
            "rid": "invalid-rid",
        })

        assert status == 422
        assert result["error"] is not None

    def test_get_case_success(self):
        """Test getting a case by ID."""
        # Setup server and case
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

        handler = CaseHandler()
        create_result, _ = handler.create({
            "name": "Test Case",
            "rid": "model/test/case",
        })
        case_id = create_result["data"]["id"]

        # Get case
        result, status = handler.get(case_id)

        assert status == 200
        assert "error" not in result or result["error"] is None
        assert result["data"]["case"]["name"] == "Test Case"

    def test_get_case_not_found(self):
        """Test getting non-existent case returns 404."""
        handler = CaseHandler()
        result, status = handler.get("nonexistent-id")

        assert status == 404
        assert result["error"] is not None
        assert result["error"]["code"] == "RESOURCE_NOT_FOUND"

    def test_list_cases_empty(self):
        """Test listing cases when none exist."""
        handler = CaseHandler()
        result, status = handler.list()

        assert status == 200
        assert "error" not in result or result["error"] is None
        assert result["data"]["items"] == []
        assert result["data"]["pagination"]["total"] == 0

    def test_list_cases_with_data(self):
        """Test listing cases with data."""
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

        handler = CaseHandler()
        handler.create({"name": "Case 1", "rid": "model/test/case1"})
        handler.create({"name": "Case 2", "rid": "model/test/case2"})

        result, status = handler.list()

        assert status == 200
        assert len(result["data"]["items"]) == 2
        assert result["data"]["pagination"]["total"] == 2

    def test_update_case_success(self):
        """Test updating a case."""
        # Setup server and case
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

        handler = CaseHandler()
        create_result, _ = handler.create({
            "name": "Original Name",
            "rid": "model/test/case",
        })
        case_id = create_result["data"]["id"]

        # Update case
        result, status = handler.update(case_id, {"name": "Updated Name"})

        assert status == 200
        assert result["data"]["name"] == "Updated Name"

    def test_update_case_not_found(self):
        """Test updating non-existent case returns 404."""
        handler = CaseHandler()
        result, status = handler.update("nonexistent-id", {"name": "New Name"})

        assert status == 404
        assert result["error"]["code"] == "RESOURCE_NOT_FOUND"

    def test_list_cases_with_status_filter(self):
        """Test listing cases with status filter."""
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

        handler = CaseHandler()
        handler.create({"name": "Case 1", "rid": "model/test/case1"})
        handler.create({"name": "Case 2", "rid": "model/test/case2"})

        result, status = handler.list(status="active")

        assert status == 200
        # Both cases should be active by default
        assert len(result["data"]["items"]) == 2

    def test_list_cases_pagination(self):
        """Test case listing pagination."""
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

        handler = CaseHandler()
        for i in range(5):
            handler.create({"name": f"Case {i}", "rid": f"model/test/case{i}"})

        result, status = handler.list(limit=2, offset=0)

        assert status == 200
        assert len(result["data"]["items"]) == 2
        assert result["data"]["pagination"]["has_more"] is True

    def test_preflight_checks(self):
        """Test preflight checks for a case."""
        # Setup server and case
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

        handler = CaseHandler()
        create_result, _ = handler.create({
            "name": "Test Case",
            "rid": "model/test/case",
        })
        case_id = create_result["data"]["id"]

        result, status = handler.preflight(case_id)

        assert status == 200
        assert "data" in result
        assert "checks" in result["data"]
        assert "ok" in result["data"]
