"""Zero-dependency local web server for the master organizer portal."""

from __future__ import annotations

import argparse
import secrets
import json
import mimetypes
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .handlers import (
    AuditHandler,
    CaseHandler,
    ModelHandler,
    ResultHandler,
    TaskHandler,
    WorkspaceHandler,
)


STATIC_DIR = Path(__file__).resolve().parent / "static"
PORTAL_TOKEN_ENV = "CLOUDPSS_PORTAL_TOKEN"


def _token_required() -> bool:
    """Check if token authentication is required."""
    return bool(os.environ.get(PORTAL_TOKEN_ENV, ""))


def _request_token(headers: dict[str, str], query: dict[str, list[str]]) -> str:
    """Get token from headers or query parameters."""
    return headers.get("X-Portal-Token", "") or query.get("token", [""])[0]


def _route_parts(path: str) -> list[str]:
    """Split route path into parts."""
    return [part for part in path.split("/") if part]


class PortalHandler(BaseHTTPRequestHandler):
    """Portal HTTP request handler."""

    server_version = "CloudPSSOrganizerPortal/2.0"

    def do_GET(self) -> None:  # noqa: N802
        """Handle GET requests."""
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        parts = _route_parts(path)

        try:
            # Check authorization for API routes
            if path.startswith("/api/") and not self._authorized(query):
                self._json({"error": {"code": "UNAUTHORIZED", "message": "Unauthorized"}}, 401)
                return

            # Route to handlers
            if path == "/api/snapshot":
                handler = WorkspaceHandler(self)
                result, status = handler.snapshot()
                self._json(result, status)

            elif path == "/api/health":
                handler = WorkspaceHandler(self)
                result, status = handler.health()
                self._json(result, status)

            elif path == "/api/cases":
                handler = CaseHandler(self)
                result, status = handler.list(
                    status=query.get("status", [""])[0],
                    tag=query.get("tag", [""])[0],
                    limit=int(query.get("limit", ["50"])[0]),
                    offset=int(query.get("offset", ["0"])[0]),
                )
                self._json(result, status)

            elif len(parts) == 3 and parts[:2] == ["api", "cases"]:
                handler = CaseHandler(self)
                result, status = handler.get(parts[2])
                self._json(result, status)

            elif len(parts) == 4 and parts[:3] == ["api", "cases", "preflight"]:
                handler = CaseHandler(self)
                result, status = handler.preflight(parts[2])
                self._json(result, status)

            elif len(parts) == 4 and parts[:3] == ["api", "cases", "model"]:
                handler = ModelHandler(self)
                result, status = handler.get_editor(parts[2])
                self._json(result, status)

            elif path == "/api/results":
                handler = ResultHandler(self)
                result, status = handler.list(
                    case_id=query.get("case_id", [""])[0],
                    task_id=query.get("task_id", [""])[0],
                    limit=int(query.get("limit", ["50"])[0]),
                    offset=int(query.get("offset", ["0"])[0]),
                )
                self._json(result, status)

            elif len(parts) == 3 and parts[:2] == ["api", "results"]:
                handler = ResultHandler(self)
                result, status = handler.get(parts[2])
                self._json(result, status)

            elif path == "/api/tasks":
                handler = TaskHandler(self)
                result, status = handler.list(
                    case_id=query.get("case_id", [""])[0],
                    status=query.get("status", [""])[0],
                    limit=int(query.get("limit", ["50"])[0]),
                    offset=int(query.get("offset", ["0"])[0]),
                )
                self._json(result, status)

            elif len(parts) == 3 and parts[:2] == ["api", "tasks"]:
                handler = TaskHandler(self)
                result, status = handler.get(parts[2])
                self._json(result, status)

            elif len(parts) == 4 and parts[:2] == ["api", "tasks"] and parts[3] == "preflight":
                handler = TaskHandler(self)
                result, status = handler.preflight(parts[2])
                self._json(result, status)

            elif len(parts) == 4 and parts[:2] == ["api", "tasks"] and parts[3] == "logs":
                handler = TaskHandler(self)
                result, status = handler.logs(parts[2])
                self._json(result, status)

            elif path == "/api/audit":
                handler = AuditHandler(self)
                result, status = handler.list(
                    limit=int(query.get("limit", ["80"])[0]),
                )
                self._json(result, status)

            else:
                # Static file serving
                self._static(path)

        except Exception as exc:
            self._json({"error": {"code": "INTERNAL_ERROR", "message": str(exc)}}, 500)

    def do_POST(self) -> None:  # noqa: N802
        """Handle POST requests."""
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        parts = _route_parts(path)

        try:
            # Check authorization
            if not self._authorized(query):
                self._json({"error": {"code": "UNAUTHORIZED", "message": "Unauthorized"}}, 401)
                return

            payload = self._read_json()

            # Route to handlers
            if path == "/api/cases":
                handler = CaseHandler(self)
                result, status = handler.create(payload)
                self._json(result, status)

            elif len(parts) == 3 and parts[:2] == ["api", "cases"]:
                handler = CaseHandler(self)
                result, status = handler.update(parts[2], payload)
                self._json(result, status)

            elif path == "/api/tasks":
                handler = TaskHandler(self)
                result, status = handler.create(payload)
                self._json(result, status)

            elif len(parts) == 3 and parts[:2] == ["api", "tasks"]:
                handler = TaskHandler(self)
                result, status = handler.update(parts[2], payload)
                self._json(result, status)

            elif len(parts) == 4 and parts[:2] == ["api", "tasks"] and parts[3] == "run":
                handler = TaskHandler(self)
                result, status = handler.run(parts[2], payload)
                self._json(result, status)

            elif path == "/api/models/edits":
                handler = ModelHandler(self)
                result, status = handler.save_edits(payload)
                self._json(result, status)

            elif len(parts) == 4 and parts[:2] == ["api", "results"] and parts[3] == "report":
                handler = ResultHandler(self)
                result, status = handler.report(parts[2])
                self._json(result, status)

            elif len(parts) == 4 and parts[:2] == ["api", "results"] and parts[3] == "archive":
                handler = ResultHandler(self)
                result, status = handler.archive(parts[2])
                self._json(result, status)

            else:
                self._json(
                    {"error": {"code": "NOT_FOUND", "message": f"Unknown endpoint: {path}"}},
                    404,
                )

        except Exception as exc:
            self._json({"error": {"code": "INTERNAL_ERROR", "message": str(exc)}}, 500)

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
        """Log a message."""
        if os.environ.get("CLOUDPSS_PORTAL_QUIET") == "1":
            return
        super().log_message(format, *args)

    def _authorized(self, query: dict[str, list[str]]) -> bool:
        """Check if request is authorized."""
        expected = os.environ.get(PORTAL_TOKEN_ENV, "")
        if not expected:
            return True
        return secrets.compare_digest(
            _request_token(dict(self.headers), query),
            expected,
        )

    def _read_json(self) -> dict[str, Any]:
        """Read JSON from request body."""
        length = int(self.headers.get("Content-Length", "0"))
        if length == 0:
            return {}
        raw = self.rfile.read(length).decode("utf-8")
        return json.loads(raw) if raw.strip() else {}

    def _json(self, data: dict[str, Any], *, status: int = 200) -> None:
        """Send JSON response."""
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _static(self, request_path: str) -> None:
        """Serve static files."""
        relative = "index.html" if request_path in {"", "/"} else request_path.lstrip("/")
        path = (STATIC_DIR / relative).resolve()

        # Security: ensure path is within STATIC_DIR
        if not str(path).startswith(str(STATIC_DIR.resolve())) or not path.is_file():
            path = STATIC_DIR / "index.html"

        content = path.read_bytes()
        content_type = mimetypes.guess_type(str(path))[0] or "application/octet-stream"

        # Override MIME types
        if path.suffix == ".js":
            content_type = "application/javascript"
        elif path.suffix == ".css":
            content_type = "text/css"

        self.send_response(200)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


def run(
    host: str = "127.0.0.1",
    port: int = 8765,
    token: str | None = None,
) -> None:
    """Run the portal server."""
    if token:
        os.environ[PORTAL_TOKEN_ENV] = token
    elif host in {"0.0.0.0", ""} and not _token_required():
        os.environ[PORTAL_TOKEN_ENV] = secrets.token_urlsafe(24)

    server = ThreadingHTTPServer((host, port), PortalHandler)
    display_host = "127.0.0.1" if host in {"0.0.0.0", ""} else host

    if _token_required():
        print(f"CloudPSS 收纳大师 Portal: http://{display_host}:{port}/?token={os.environ[PORTAL_TOKEN_ENV]}")
        if host in {"0.0.0.0", ""}:
            print("局域网访问时请使用同一个 token 查询参数；API 请求未带 token 会返回 401。")
    else:
        print(f"CloudPSS 收纳大师 Portal: http://{display_host}:{port}")
        if host in {"0.0.0.0", ""}:
            print("警告：当前未设置访问 token，局域网内设备可以访问 Portal API。")

    print("按 Ctrl+C 停止")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def main(argv: list[str] | None = None) -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="CloudPSS 收纳大师 Portal")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--token", help="访问 Portal API 所需的 token；也可设置 CLOUDPSS_PORTAL_TOKEN")
    args = parser.parse_args(argv)
    run(args.host, args.port, args.token)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
