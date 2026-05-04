"""Tests for BaseHandler and ResponseHelper."""

import pytest
from cloudpss_skills_v3.master_organizer.portal.handlers.base import BaseHandler, ResponseHelper


class TestResponseHelper:
    """Test ResponseHelper utility methods."""

    def test_success_response(self):
        """Test success response format."""
        data = {"id": "123", "name": "Test"}
        result, status = ResponseHelper.success(data)

        assert status == 200
        assert result["data"] == data
        assert result["error"] is None

    def test_success_response_with_custom_status(self):
        """Test success response with custom status code."""
        data = {"id": "123"}
        result, status = ResponseHelper.success(data, 201)

        assert status == 201
        assert result["data"] == data
        assert result["error"] is None

    def test_error_response(self):
        """Test error response format."""
        result, status = ResponseHelper.error("TEST_ERROR", "Test error message", 400)

        assert status == 400
        assert result["error"]["code"] == "TEST_ERROR"
        assert result["error"]["message"] == "Test error message"

    def test_not_found_response(self):
        """Test not found response."""
        result, status = ResponseHelper.not_found("User", "user-123")

        assert status == 404
        assert result["error"]["code"] == "RESOURCE_NOT_FOUND"
        assert "user-123" in result["error"]["message"]
        assert "User" in result["error"]["message"]

    def test_validation_error_response(self):
        """Test validation error response."""
        result, status = ResponseHelper.validation_error("Field is required", {"field": "name"})

        assert status == 422
        assert result["error"]["code"] == "VALIDATION_ERROR"
        assert result["error"]["details"]["field"] == "name"

    def test_validation_error_without_details(self):
        """Test validation error without details."""
        result, status = ResponseHelper.validation_error("Invalid input")

        assert status == 422
        assert result["error"]["code"] == "VALIDATION_ERROR"
        assert "details" in result["error"]  # Empty dict is still present

    def test_paginated_response(self):
        """Test paginated response structure."""
        items = [{"id": "1"}, {"id": "2"}]
        result = ResponseHelper.paginated(items, total=10, limit=2, offset=0)

        assert result["items"] == items
        assert result["pagination"]["total"] == 10
        assert result["pagination"]["limit"] == 2
        assert result["pagination"]["offset"] == 0
        assert result["pagination"]["has_more"] is True

    def test_paginated_response_no_more(self):
        """Test paginated response when no more items."""
        items = [{"id": "1"}]
        result = ResponseHelper.paginated(items, total=1, limit=10, offset=0)

        assert result["pagination"]["has_more"] is False


class TestBaseHandler:
    """Test BaseHandler functionality."""

    def test_handler_initialization(self):
        """Test handler can be initialized."""
        handler = BaseHandler()
        assert handler is not None

    def test_handler_has_response_helper(self):
        """Test handler has access to ResponseHelper."""
        handler = BaseHandler()

        # Should be able to use ResponseHelper methods
        result, status = ResponseHelper.success({"test": True})
        assert status == 200
