"""Tests for case HTTP endpoints."""

import pytest
from cloudpss_skills_v3.master_organizer.core import (
    ServerRegistry,
    Server,
    IDGenerator,
    EntityType,
    get_path_manager,
)
from cloudpss_skills_v3.master_organizer.core.server_auth import build_auth_metadata
from cloudpss_skills_v3.master_organizer.portal.handlers import CaseHandler


class TestCaseEndpoints:
    """Test case API endpoints."""

    def test_create_case_with_valid_data(self, tmp_path, monkeypatch):
        """Test POST /api/cases creates a case."""
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

        handler = CaseHandler()
        result, status = handler.create({
            "name": "Test Case",
            "rid": "model/test/case",
            "tags": ["test", "powerflow"],
        })

        assert status == 201
        assert "data" in result
        assert result["data"]["name"] == "Test Case"
        assert result["data"]["rid"] == "model/test/case"
        assert "id" in result["data"]

    def test_create_case_rejects_invalid_rid(self, tmp_path, monkeypatch):
        """Test POST /api/cases rejects invalid RID."""
        monkeypatch.setenv("CLOUDPSS_HOME", str(tmp_path))
        get_path_manager(str(tmp_path))

        handler = CaseHandler()
        result, status = handler.create({
            "name": "Test Case",
            "rid": "invalid-rid",
        })

        assert status == 422
        assert "error" in result
        assert result["error"]["code"] == "VALIDATION_ERROR"

    def test_get_case_returns_case_detail(self, tmp_path, monkeypatch):
        """Test GET /api/cases/{id} returns case detail."""
        monkeypatch.setenv("CLOUDPSS_HOME", str(tmp_path))
        get_path_manager(str(tmp_path))

        # Setup server and create case
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
        assert "data" in result
        assert result["data"]["case"]["name"] == "Test Case"

    def test_get_nonexistent_case_returns_404(self, tmp_path, monkeypatch):
        """Test GET /api/cases/{id} returns 404 for non-existent case."""
        monkeypatch.setenv("CLOUDPSS_HOME", str(tmp_path))
        get_path_manager(str(tmp_path))

        handler = CaseHandler()
        result, status = handler.get("nonexistent-case-id")

        assert status == 404
        assert "error" in result
        assert result["error"]["code"] == "RESOURCE_NOT_FOUND"

    def test_list_cases_returns_paginated_results(self, tmp_path, monkeypatch):
        """Test GET /api/cases returns paginated case list."""
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

        # Create multiple cases
        handler = CaseHandler()
        for i in range(3):
            handler.create({
                "name": f"Case {i}",
                "rid": f"model/test/case{i}",
            })

        # List cases
        result, status = handler.list(limit=2, offset=0)

        assert status == 200
        assert "data" in result
        assert "items" in result["data"]
        assert "pagination" in result["data"]
        assert len(result["data"]["items"]) <= 2
