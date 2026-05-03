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

from . import state


STATIC_DIR = Path(__file__).resolve().parent / "static"
PORTAL_TOKEN_ENV = "CLOUDPSS_PORTAL_TOKEN"


def _token_required() -> bool:
    return bool(os.environ.get(PORTAL_TOKEN_ENV, ""))


def _request_token(headers, query: dict[str, list[str]]) -> str:
    return headers.get("X-Portal-Token", "") or query.get("token", [""])[0]


def _route_parts(path: str) -> list[str]:
    return [part for part in path.split("/") if part]


class PortalHandler(BaseHTTPRequestHandler):
    server_version = "CloudPSSOrganizerPortal/1.0"

    def do_GET(self):  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        parts = _route_parts(path)
        try:
            if path.startswith("/api/") and not self._authorized(query):
                self._json({"error": "unauthorized"}, status=401)
                return
            if path == "/api/snapshot":
                self._json(state.organizer_snapshot())
            elif len(parts) == 3 and parts[:2] == ["api", "cases"]:
                self._json(state.case_detail(parts[2]))
            elif len(parts) == 3 and parts[:2] == ["api", "results"]:
                self._json(state.result_detail(parts[2]))
            elif len(parts) == 4 and parts[:2] == ["api", "tasks"] and parts[3] == "preflight":
                self._json(state.task_preflight(parts[2]))
            elif path == "/api/audit":
                limit = int(query.get("limit", ["80"])[0])
                self._json({"entries": state.audit_entries(limit)})
            elif path == "/api/health":
                self._json(state.workspace_health())
            else:
                self._static(path)
        except Exception as exc:
            self._json({"error": str(exc)}, status=400)

    def do_POST(self):  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        parts = _route_parts(path)
        try:
            if not self._authorized(query):
                self._json({"error": "unauthorized"}, status=401)
                return
            payload = self._read_json()
            if path == "/api/cases":
                self._json(state.create_case(payload), status=201)
            elif len(parts) == 3 and parts[:2] == ["api", "cases"]:
                self._json(state.update_case(parts[2], payload))
            elif path == "/api/tasks":
                self._json(state.create_task(payload), status=201)
            elif len(parts) == 3 and parts[:2] == ["api", "tasks"]:
                self._json(state.update_task(parts[2], payload))
            elif path == "/api/models/edits":
                self._json(state.save_model_table_edits(payload))
            elif len(parts) == 4 and parts[:2] == ["api", "tasks"] and parts[3] == "run":
                task_id = parts[2]
                timeout = int(payload.get("timeout", 300))
                self._json(state.run_task(task_id, timeout))
            elif len(parts) == 4 and parts[:2] == ["api", "results"] and parts[3] == "report":
                self._json(state.report_result(parts[2]))
            elif len(parts) == 4 and parts[:2] == ["api", "results"] and parts[3] == "archive":
                self._json(state.archive_result_for_portal(parts[2]))
            else:
                self._json({"error": f"unknown endpoint: {path}"}, status=404)
        except Exception as exc:
            self._json({"error": str(exc)}, status=400)

    def log_message(self, format, *args):  # noqa: A002
        if os.environ.get("CLOUDPSS_PORTAL_QUIET") == "1":
            return
        super().log_message(format, *args)

    def _authorized(self, query: dict[str, list[str]]) -> bool:
        expected = os.environ.get(PORTAL_TOKEN_ENV, "")
        if not expected:
            return True
        return secrets.compare_digest(_request_token(self.headers, query), expected)

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        if length == 0:
            return {}
        raw = self.rfile.read(length).decode("utf-8")
        return json.loads(raw) if raw.strip() else {}

    def _json(self, data, *, status: int = 200):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _static(self, request_path: str):
        relative = "index.html" if request_path in {"", "/"} else request_path.lstrip("/")
        path = (STATIC_DIR / relative).resolve()
        if not str(path).startswith(str(STATIC_DIR.resolve())) or not path.is_file():
            path = STATIC_DIR / "index.html"
        content = path.read_bytes()
        content_type = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
        if path.suffix == ".js":
            content_type = "application/javascript"
        elif path.suffix == ".css":
            content_type = "text/css"
        self.send_response(200)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


def run(host: str = "127.0.0.1", port: int = 8765, token: str | None = None):
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
    parser = argparse.ArgumentParser(description="CloudPSS 收纳大师 Portal")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--token", help="访问 Portal API 所需的 token；也可设置 CLOUDPSS_PORTAL_TOKEN")
    args = parser.parse_args(argv)
    run(args.host, args.port, args.token)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
