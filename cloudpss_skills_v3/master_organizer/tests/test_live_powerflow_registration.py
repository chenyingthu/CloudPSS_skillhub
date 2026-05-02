"""Guarded live CloudPSS smoke test for the v3 master organizer.

This test is intentionally opt-in. It calls the real CloudPSS service, runs a
power-flow job, then registers the live job/result evidence in a v3 workspace
and validates the CLI query/export path.
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

from cloudpss_skills_v3.master_organizer.core import (
    Case,
    CaseRegistry,
    EntityType,
    IDGenerator,
    Result,
    ResultRegistry,
    Server,
    ServerRegistry,
    Task,
    TaskRegistry,
)
from cloudpss_skills_v3.master_organizer.core.server_auth import (
    DEFAULT_INTERNAL_OWNER,
    DEFAULT_INTERNAL_URL,
    TOKEN_SOURCE_INTERNAL,
    build_auth_metadata,
    decrypt_server_token,
    ensure_internal_server,
    get_default_server,
    normalize_server_url,
)


REPO_ROOT = Path(__file__).resolve().parents[3]
CLI_MODULE = "cloudpss_skills_v3.master_organizer.cli.main"
DEFAULT_MODEL_RIDS = ("model/holdme/IEEE39", "model/chenying/IEEE39")


def _read_token_file(name: str) -> str:
    token_path = REPO_ROOT / name
    if token_path.exists():
        return token_path.read_text(encoding="utf-8").strip()
    return ""


def _load_cloudpss_token() -> tuple[str, str, str]:
    for token_path in (REPO_ROOT / ".cloudpss_token_internal", REPO_ROOT / ".cloudpss_token"):
        if token_path.exists():
            token = token_path.read_text(encoding="utf-8").strip()
            if token:
                return token, os.environ.get("CLOUDPSS_API_URL", "https://cloudpss.net/"), ""
    return os.environ.get("CLOUDPSS_TOKEN", "").strip(), os.environ.get("CLOUDPSS_API_URL", "https://cloudpss.net/"), ""


def _table_count(table) -> int:
    columns = table["data"]["columns"]
    return len(columns[0].get("data", [])) if columns else 0


def _fetch_first_available_model(model_cls, candidates: list[str]):
    errors = []
    for rid in dict.fromkeys(candidates):
        try:
            return rid, model_cls.fetch(rid)
        except Exception as exc:  # pragma: no cover - reported with live failure details
            errors.append(f"{rid}: {type(exc).__name__}: {str(exc)[:200]}")
    raise RuntimeError("unable to fetch any candidate CloudPSS model: " + " | ".join(errors))


def _wait_for_job(job, timeout_seconds: int = 240) -> int:
    started = time.time()
    status = job.status()
    while status not in (1, 2):
        if time.time() - started > timeout_seconds:
            raise TimeoutError(f"CloudPSS job timed out: {getattr(job, 'id', 'unknown')} status={status}")
        time.sleep(2)
        status = job.status()
    return status


def _run_cli(env: dict[str, str], *args: str, cwd: Path = REPO_ROOT) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, "-m", CLI_MODULE, *args]
    completed = subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True, check=False)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    return completed


@pytest.mark.integration
def test_live_powerflow_result_can_be_registered_and_exported(tmp_path):
    if os.environ.get("CLOUDPSS_V3_RUN_LIVE") != "1":
        pytest.skip("set CLOUDPSS_V3_RUN_LIVE=1 to run the live CloudPSS smoke test")

    workspace = tmp_path / "workspace"
    registry_dir = workspace / "registry"
    registry_dir.mkdir(parents=True)

    internal_token = _read_token_file(".cloudpss_token_internal")
    if internal_token:
        server_id, server = ensure_internal_server(ServerRegistry(registry_dir), repo_root=REPO_ROOT)
    else:
        token, url, owner = _load_cloudpss_token()
        if not token:
            pytest.skip("missing CloudPSS token")
        server_id = IDGenerator.generate(EntityType.SERVER)
        server = Server(
            id=server_id,
            name="CloudPSS Live",
            url=normalize_server_url(url),
            owner=owner,
            auth=build_auth_metadata(token, {"token_source": "test"}),
            default=True,
        )
        ServerRegistry(registry_dir).create(server_id, server)

    token = decrypt_server_token(server)
    if not token:
        pytest.skip("missing CloudPSS token")

    from cloudpss import Model, setToken

    previous_api_url = os.environ.get("CLOUDPSS_API_URL")
    os.environ["CLOUDPSS_API_URL"] = server.url
    setToken(token)
    try:
        candidates = [os.environ.get("TEST_MODEL_RID", "").strip(), *DEFAULT_MODEL_RIDS]
        model_rid, model = _fetch_first_available_model(Model, [rid for rid in candidates if rid])

        job = model.runPowerFlow()
        status = _wait_for_job(job)
        assert status == 1, f"CloudPSS power-flow job failed: {getattr(job, 'id', 'unknown')}"

        result = job.result
        bus_count = _table_count(result.getBuses()[0])
        branch_count = _table_count(result.getBranches()[0])
        assert bus_count > 0
        assert branch_count > 0
    finally:
        if previous_api_url is None:
            os.environ.pop("CLOUDPSS_API_URL", None)
        else:
            os.environ["CLOUDPSS_API_URL"] = previous_api_url

    case_id = IDGenerator.generate(EntityType.CASE)
    task_id = IDGenerator.generate(EntityType.TASK)
    result_id = IDGenerator.generate(EntityType.RESULT)

    CaseRegistry(registry_dir).create(
        case_id,
        Case(
            id=case_id,
            name="IEEE39 live powerflow",
            rid=model_rid,
            server_id=server_id,
            status="active",
            tags=["live", "powerflow", "ieee39"],
            task_count=1,
            last_task_id=task_id,
        ),
    )
    TaskRegistry(registry_dir).create(
        task_id,
        Task(
            id=task_id,
            name="live powerflow smoke",
            case_id=case_id,
            type="powerflow",
            job_id=getattr(job, "id", None),
            server_id=server_id,
            status="completed",
            completed_at=time.strftime("%Y-%m-%dT%H:%M:%S"),
            result_id=result_id,
            config={"model_rid": model_rid},
        ),
    )
    ResultRegistry(registry_dir).create(
        result_id,
        Result(
            id=result_id,
            name="live powerflow result",
            task_id=task_id,
            case_id=case_id,
            format="json",
            size_bytes=bus_count + branch_count,
            files=[],
            metadata={
                "data_source": "live_cloudpss",
                "server_id": server_id,
                "server_url": server.url,
                "server_owner": server.owner,
                "model_rid": model_rid,
                "model_name": getattr(model, "name", ""),
                "job_id": getattr(job, "id", None),
                "job_status": status,
                "bus_count": bus_count,
                "branch_count": branch_count,
            },
        ),
    )

    home = tmp_path / "home"
    home.mkdir()
    env = {**os.environ, "HOME": str(home), "PYTHONPATH": str(REPO_ROOT), "CLOUDPSS_HOME": str(workspace)}
    export_path = tmp_path / "live-powerflow-result.json"

    server_list = _run_cli(env, "server", "list")
    assert server_id in server_list.stdout
    assert server.url in server_list.stdout
    assert server.owner in server_list.stdout
    assert "encrypted" in server_list.stdout

    task_status = _run_cli(env, "task", "status", task_id)
    assert "状态: completed" in task_status.stdout
    assert f"结果ID: {result_id}" in task_status.stdout

    case_tree = _run_cli(env, "case", "list", "--tree", "--tag", "live")
    assert case_id in case_tree.stdout
    assert task_id in case_tree.stdout
    assert "live powerflow smoke [completed]" in case_tree.stdout

    result_analysis = _run_cli(env, "result", "analyze", result_id)
    assert "data_source: live_cloudpss" in result_analysis.stdout
    assert f"server_url: {server.url}" in result_analysis.stdout
    assert f"job_id: {getattr(job, 'id', None)}" in result_analysis.stdout

    _run_cli(env, "result", "export", result_id, "--output", str(export_path))

    exported = json.loads(export_path.read_text(encoding="utf-8"))
    assert exported["result_id"] == result_id
    assert exported["metadata"]["data_source"] == "live_cloudpss"
    assert exported["metadata"]["server_id"] == server_id
    assert exported["metadata"]["server_url"] == server.url
    assert exported["metadata"]["job_id"] == getattr(job, "id", None)
    assert exported["metadata"]["bus_count"] == bus_count
    assert exported["metadata"]["branch_count"] == branch_count


def test_internal_token_is_bound_to_internal_server(tmp_path):
    token_path = REPO_ROOT / ".cloudpss_token_internal"
    if not token_path.exists() or not token_path.read_text(encoding="utf-8").strip():
        pytest.skip("missing .cloudpss_token_internal")

    registry = ServerRegistry(tmp_path / "registry")
    server_id, server = ensure_internal_server(registry, repo_root=REPO_ROOT)

    assert server.url == DEFAULT_INTERNAL_URL
    assert server.owner == DEFAULT_INTERNAL_OWNER
    assert server.default is True
    assert server.auth["token_source"] == TOKEN_SOURCE_INTERNAL
    assert "encrypted_token" in server.auth
    assert token_path.read_text(encoding="utf-8").strip() not in str(server.auth)
    assert decrypt_server_token(server) == token_path.read_text(encoding="utf-8").strip()
    assert get_default_server(registry) == (server_id, server)
