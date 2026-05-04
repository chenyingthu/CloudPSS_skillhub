"""Base handler classes and utilities."""

from __future__ import annotations

from typing import Any
from http.server import BaseHTTPRequestHandler


class ResponseHelper:
    """Response helper for standardized JSON responses."""

    @staticmethod
    def success(data: dict[str, Any], status: int = 200) -> tuple[dict[str, Any], int]:
        """Return a successful response."""
        return {"data": data, "error": None}, status

    @staticmethod
    def error(
        code: str,
        message: str,
        status: int = 400,
        details: dict[str, Any] | None = None,
    ) -> tuple[dict[str, Any], int]:
        """Return an error response."""
        return {
            "error": {"code": code, "message": message, "details": details or {}}
        }, status

    @staticmethod
    def not_found(resource: str, resource_id: str) -> tuple[dict[str, Any], int]:
        """Return a 404 not found response."""
        return ResponseHelper.error(
            "RESOURCE_NOT_FOUND",
            f"{resource} not found: {resource_id}",
            404,
        )

    @staticmethod
    def validation_error(message: str, details: dict[str, Any] | None = None) -> tuple[dict[str, Any], int]:
        """Return a 422 validation error response."""
        return ResponseHelper.error(
            "VALIDATION_ERROR",
            message,
            422,
            details,
        )

    @staticmethod
    def paginated(
        items: list[dict[str, Any]],
        total: int,
        limit: int,
        offset: int,
    ) -> dict[str, Any]:
        """Return a paginated response."""
        return {
            "items": items,
            "pagination": {
                "total": total,
                "limit": limit,
                "offset": offset,
                "has_more": offset + len(items) < total,
            },
        }


class BaseHandler:
    """Base handler class for portal request handlers."""

    def __init__(self, request: BaseHTTPRequestHandler | None = None) -> None:
        """Initialize handler with request context."""
        self.request = request
