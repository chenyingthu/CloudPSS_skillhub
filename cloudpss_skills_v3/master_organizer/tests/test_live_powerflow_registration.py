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


REPO_ROOT = Path(__file__).resolve().parents[3]
CLI_MODULE = "cloudpss_skills_v3.master_organizer.cli.main"
DEFAULT_MODEL_RIDS = ("model/holdme/IEEE39", "model/chenying/IEEE39")


def _load_cloudpss_token() -> str:
    for token_path in (REPO_ROOT / ".cloudpss_token_internal", REPO_ROOT / ".cloudpss_token"):
        if token_path.exists():
            token = token_path.read_text(encoding="utf-8").strip()
            if token:
                return token
    return os.environ.get("CLOUDPSS_TOKEN", "").strip()


def _table_count(table) -> int:
    try:
        return len(table)
    except TypeError:
        return len(list(table))


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


@pytest.mark.integration
def test_live_powerflow_result_can_be_registered_and_exported(tmp_path):
    if os.environ.get("CLOUDPSS_V3_RUN_LIVE") != "1":
        pytest.skip("set CLOUDPSS_V3_RUN_LIVE=1 to run the live CloudPSS smoke test")

    token = _load_cloudpss_token()
    if not token:
        pytest.skip("missing CloudPSS token")

    from cloudpss import Model, setToken

    setToken(token)
    candidates = [os.environ.get("TEST_MODEL_RID", "").strip(), *DEFAULT_MODEL_RIDS]
    model_rid, model = _fetch_first_available_model(Model, [rid for rid in candidates if rid])

    job = model.runPowerFlow()
    status = _wait_for_job(job)
    assert status == 1, f"CloudPSS power-flow job failed: {getattr(job, 'id', 'unknown')}"

    result = job.result
    bus_count = _table_count(result.getBuses())
    branch_count = _table_count(result.getBranches())
    assert bus_count > 0
    assert branch_count > 0

    workspace = tmp_path / "workspace"
    registry_dir = workspace / "registry"
    registry_dir.mkdir(parents=True)

    server_id = IDGenerator.generate(EntityType.SERVER)
    case_id = IDGenerator.generate(EntityType.CASE)
    task_id = IDGenerator.generate(EntityType.TASK)
    result_id = IDGenerator.generate(EntityType.RESULT)

    ServerRegistry(registry_dir).create(
        server_id,
        Server(
            id=server_id,
            name="CloudPSS Live",
            url=os.environ.get("CLOUDPSS_API_URL", "https://cloudpss.net/"),
            default=True,
        ),
    )
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
    command = [sys.executable, "-m", CLI_MODULE, "result", "export", result_id, "--output", str(export_path)]
    completed = subprocess.run(command, env=env, text=True, capture_output=True, check=False)
    assert completed.returncode == 0, completed.stdout + completed.stderr

    exported = json.loads(export_path.read_text(encoding="utf-8"))
    assert exported["result_id"] == result_id
    assert exported["metadata"]["data_source"] == "live_cloudpss"
    assert exported["metadata"]["job_id"] == getattr(job, "id", None)
    assert exported["metadata"]["bus_count"] == bus_count
    assert exported["metadata"]["branch_count"] == branch_count
