"""Tests for workspace HTTP endpoints."""

import pytest
from unittest.mock import patch, MagicMock

from cloudpss_skills_v3.master_organizer.portal.server import PortalHandler


class TestWorkspaceEndpoints:
    """Test workspace API endpoints."""

    def test_get_snapshot_returns_workspace_data(self, tmp_path, monkeypatch):
        """Test GET /api/snapshot returns workspace snapshot."""
        monkeypatch.setenv("CLOUDPSS_HOME", str(tmp_path))

        from cloudpss_skills_v3.master_organizer.core import get_path_manager
        get_path_manager(str(tmp_path))

        # Mock handler
        with patch.object(PortalHandler, '_authorized', return_value=True):
            handler = MagicMock()
            handler.path = "/api/snapshot"
            handler.headers = {}

            # Import and test
            from cloudpss_skills_v3.master_organizer.portal.handlers import WorkspaceHandler
            workspace_handler = WorkspaceHandler()
            result, status = workspace_handler.snapshot()

            assert status == 200
            assert "data" in result
            assert "workspace" in result["data"]
            assert "servers" in result["data"]
            assert "cases" in result["data"]

    def test_get_health_returns_health_status(self, tmp_path, monkeypatch):
        """Test GET /api/health returns health status."""
        monkeypatch.setenv("CLOUDPSS_HOME", str(tmp_path))

        from cloudpss_skills_v3.master_organizer.core import get_path_manager
        get_path_manager(str(tmp_path))

        from cloudpss_skills_v3.master_organizer.portal.handlers import WorkspaceHandler
        workspace_handler = WorkspaceHandler()
        result, status = workspace_handler.health()

        assert status == 200
        assert "data" in result
        assert "summary" in result["data"]
        assert "quotas" in result["data"]
