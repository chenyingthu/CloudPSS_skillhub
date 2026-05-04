"""Tests for model HTTP endpoints."""

import pytest
from unittest.mock import patch, MagicMock

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
from cloudpss_skills_v3.master_organizer.portal.handlers import ModelHandler, CaseHandler


class TestModelEndpoints:
    """Test model API endpoints."""

    def _setup_server_and_case(self, tmp_path, monkeypatch):
        """Helper to setup server and case for model tests."""
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

        # Setup case with RID
        case_handler = CaseHandler()
        result, _ = case_handler.create({
            "name": "Test Case",
            "rid": "model/test/case",
        })
        case_id = result["data"]["id"]

        return server_id, case_id

    @patch("cloudpss_skills_v3.master_organizer.core.model_utils.fetch_model_summary")
    def test_get_model_summary_success(self, mock_fetch, tmp_path, monkeypatch):
        """Test GET /api/models/{rid}/summary returns model summary."""
        # Setup mock
        mock_fetch.return_value = {
            "rid": "model/test/case",
            "name": "Test Model",
            "description": "A test model",
            "components": 15,
            "topology": {"buses": 5, "branches": 4},
        }

        monkeypatch.setenv("CLOUDPSS_HOME", str(tmp_path))
        get_path_manager(str(tmp_path))

        handler = ModelHandler()
        result, status = handler.get_summary("model/test/case")

        assert status == 200
        assert "data" in result
        assert result["data"]["rid"] == "model/test/case"
        assert "name" in result["data"]
        mock_fetch.assert_called_once()

    @patch("cloudpss_skills_v3.master_organizer.core.model_utils.fetch_model_summary")
    def test_get_model_summary_not_found(self, mock_fetch, tmp_path, monkeypatch):
        """Test GET /api/models/{rid}/summary returns 404 for non-existent model."""
        # Setup mock to simulate not found
        mock_fetch.return_value = None

        monkeypatch.setenv("CLOUDPSS_HOME", str(tmp_path))
        get_path_manager(str(tmp_path))

        handler = ModelHandler()
        result, status = handler.get_summary("model/nonexistent/model")

        assert status == 404
        assert "error" in result
        assert result["error"]["code"] == "RESOURCE_NOT_FOUND"

    @patch("cloudpss_skills_v3.master_organizer.core.model_utils.fetch_model_parameters")
    def test_get_model_parameters_success(self, mock_fetch, tmp_path, monkeypatch):
        """Test GET /api/models/{rid}/parameters returns model parameters."""
        # Setup mock
        mock_fetch.return_value = {
            "rid": "model/test/case",
            "parameters": [
                {"name": "baseMVA", "value": 100.0, "unit": "MVA"},
                {"name": "frequency", "value": 50.0, "unit": "Hz"},
            ],
            "component_parameters": {
                "bus": [{"id": 1, "type": "slack", "v": 1.0}],
                "line": [{"from": 1, "to": 2, "r": 0.01, "x": 0.1}],
            },
        }

        monkeypatch.setenv("CLOUDPSS_HOME", str(tmp_path))
        get_path_manager(str(tmp_path))

        handler = ModelHandler()
        result, status = handler.get_parameters("model/test/case")

        assert status == 200
        assert "data" in result
        assert "parameters" in result["data"]
        assert len(result["data"]["parameters"]) == 2
        mock_fetch.assert_called_once()

    @patch("cloudpss_skills_v3.master_organizer.core.model_utils.fetch_model_parameters")
    def test_get_model_parameters_filtered(self, mock_fetch, tmp_path, monkeypatch):
        """Test GET /api/models/{rid}/parameters with component filter."""
        # Setup mock
        mock_fetch.return_value = {
            "rid": "model/test/case",
            "component_parameters": {
                "bus": [{"id": 1, "type": "slack", "v": 1.0}],
            },
        }

        monkeypatch.setenv("CLOUDPSS_HOME", str(tmp_path))
        get_path_manager(str(tmp_path))

        handler = ModelHandler()
        result, status = handler.get_parameters("model/test/case", component="bus")

        assert status == 200
        assert "data" in result
        mock_fetch.assert_called_once()

    @patch("cloudpss_skills_v3.master_organizer.core.model_utils.list_available_models")
    def test_list_available_models_success(self, mock_list, tmp_path, monkeypatch):
        """Test GET /api/models/available returns available models."""
        # Setup mock
        mock_list.return_value = [
            {"rid": "model/user1/ieee14", "name": "IEEE 14 Bus"},
            {"rid": "model/user1/ieee39", "name": "IEEE 39 Bus"},
            {"rid": "model/user2/test", "name": "Test Model"},
        ]

        monkeypatch.setenv("CLOUDPSS_HOME", str(tmp_path))
        get_path_manager(str(tmp_path))

        handler = ModelHandler()
        result, status = handler.list_available()

        assert status == 200
        assert "data" in result
        assert len(result["data"]["models"]) == 3
        mock_list.assert_called_once()

    @patch("cloudpss_skills_v3.master_organizer.core.model_utils.list_available_models")
    def test_list_available_models_empty(self, mock_list, tmp_path, monkeypatch):
        """Test GET /api/models/available returns empty list when no models."""
        # Setup mock
        mock_list.return_value = []

        monkeypatch.setenv("CLOUDPSS_HOME", str(tmp_path))
        get_path_manager(str(tmp_path))

        handler = ModelHandler()
        result, status = handler.list_available()

        assert status == 200
        assert "data" in result
        assert len(result["data"]["models"]) == 0

    @patch("cloudpss_skills_v3.master_organizer.core.model_utils.validate_rid")
    def test_validate_rid_success(self, mock_validate, tmp_path, monkeypatch):
        """Test GET /api/models/validate returns validation result."""
        # Setup mock
        mock_validate.return_value = {
            "valid": True,
            "rid": "model/test/case",
            "message": "RID format is valid",
        }

        monkeypatch.setenv("CLOUDPSS_HOME", str(tmp_path))
        get_path_manager(str(tmp_path))

        handler = ModelHandler()
        result, status = handler.validate_rid("model/test/case")

        assert status == 200
        assert "data" in result
        assert result["data"]["valid"] is True
        mock_validate.assert_called_once()

    @patch("cloudpss_skills_v3.master_organizer.core.model_utils.validate_rid")
    def test_validate_rid_invalid(self, mock_validate, tmp_path, monkeypatch):
        """Test GET /api/models/validate returns false for invalid RID."""
        # Setup mock
        mock_validate.return_value = {
            "valid": False,
            "rid": "invalid-rid",
            "message": "RID must start with 'model/'",
        }

        monkeypatch.setenv("CLOUDPSS_HOME", str(tmp_path))
        get_path_manager(str(tmp_path))

        handler = ModelHandler()
        result, status = handler.validate_rid("invalid-rid")

        assert status == 200
        assert "data" in result
        assert result["data"]["valid"] is False
