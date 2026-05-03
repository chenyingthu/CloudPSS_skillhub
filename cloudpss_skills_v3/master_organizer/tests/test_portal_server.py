"""Portal HTTP server behavior tests."""

from cloudpss_skills_v3.master_organizer.portal import server


class _Headers(dict):
    def get(self, key, default=None):
        return super().get(key, default)


def test_portal_token_request_sources(monkeypatch):
    monkeypatch.setenv(server.PORTAL_TOKEN_ENV, "secret")

    assert server._request_token(_Headers({"X-Portal-Token": "secret"}), {}) == "secret"
    assert server._request_token(_Headers(), {"token": ["secret"]}) == "secret"
    assert server._token_required() is True


def test_portal_route_parts_are_exact():
    assert server._route_parts("/api/cases/case_123") == ["api", "cases", "case_123"]
    assert server._route_parts("/api/tasks/task_123/run") == ["api", "tasks", "task_123", "run"]


def test_edit_case_form_has_model_source_field():
    html = (server.STATIC_DIR / "index.html").read_text(encoding="utf-8")
    start = html.index('id="editCaseForm"')
    end = html.index('id="taskDialog"')
    edit_case_form = html[start:end]

    assert 'name="model_source"' in edit_case_form
