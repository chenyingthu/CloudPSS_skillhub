"""Portal handlers/API tests."""

import sys
import types
from pathlib import Path

import pytest

from cloudpss_skills_v3.master_organizer.core import (
    EntityType,
    IDGenerator,
    Server,
    ServerRegistry,
    get_path_manager,
)
from cloudpss_skills_v3.master_organizer.core.server_auth import build_auth_metadata
from cloudpss_skills_v3.master_organizer.portal.handlers import (
    AuditHandler,
    CaseHandler,
    ModelHandler,
    ResultHandler,
    TaskHandler,
    WorkspaceHandler,
)


@pytest.fixture
def setup_registry(tmp_path, monkeypatch):
    """Setup test environment with clean registry."""
    monkeypatch.setenv("CLOUDPSS_HOME", str(tmp_path))
    get_path_manager(str(tmp_path))

    server_id = IDGenerator.generate(EntityType.SERVER)
    ServerRegistry().create(
        server_id,
        Server(
            id=server_id,
            name="portal-server",
            url="http://portal.test/",
            owner="tester",
            auth=build_auth_metadata("token", {"token_source": "test"}),
            default=True,
        ),
    )

    return {"server_id": server_id}


def test_portal_snapshot_create_and_run_powerflow(tmp_path, monkeypatch):
    """Test complete workflow: create case, task, run, and verify snapshot."""
    monkeypatch.setenv("CLOUDPSS_HOME", str(tmp_path))
    get_path_manager(str(tmp_path))

    # Mock cloudpss module
    class FakeResult:
        def getBuses(self):
            return [{"data": {"columns": [{"name": "bus", "data": ["1"]}, {"name": "v", "data": [1.0]}]}}]

        def getBranches(self):
            return [{"data": {"columns": [{"name": "branch", "data": ["1-2"]}, {"name": "p", "data": [10.0]}]}}]

    class FakeJob:
        id = "portal-job-1"
        result = FakeResult()

        def status(self):
            return 1

    class FakeModel:
        name = "Portal Fake Model"

        @classmethod
        def fetch(cls, rid):
            assert rid == "model/test/portal"
            return cls()

        def runPowerFlow(self):
            return FakeJob()

    monkeypatch.setitem(
        sys.modules,
        "cloudpss",
        types.SimpleNamespace(Model=FakeModel, setToken=lambda token: None),
    )

    # Setup server
    server_id = IDGenerator.generate(EntityType.SERVER)
    ServerRegistry().create(
        server_id,
        Server(
            id=server_id,
            name="portal-server",
            url="http://portal.test/",
            owner="tester",
            auth=build_auth_metadata("token", {"token_source": "test"}),
            default=True,
        ),
    )

    # Create case
    case_handler = CaseHandler()
    result, status = case_handler.create(
        {"name": "Portal Case", "rid": "model/test/portal", "tags": "portal,pf"}
    )
    assert status == 201
    case_id = result["data"]["id"]

    # Create task
    task_handler = TaskHandler()
    result, status = task_handler.create(
        {"case_id": case_id, "name": "Portal PF", "type": "powerflow"}
    )
    assert status == 201
    task_id = result["data"]["id"]

    # Run task
    result, status = task_handler.run(task_id, {"timeout": 10})
    assert status == 200
    result_id = result["data"]["result_id"]

    # Get snapshot
    workspace_handler = WorkspaceHandler()
    result, status = workspace_handler.snapshot()
    assert status == 200
    snapshot = result["data"]

    assert snapshot["workspace"]["counts"]["cases"] == 1
    assert snapshot["workspace"]["counts"]["tasks"] == 1
    assert snapshot["workspace"]["counts"]["results"] == 1
    assert snapshot["servers"][0]["auth"]["encrypted_token"] == "<redacted>"
    assert snapshot["servers"][0]["auth"]["has_encrypted_token"] is True
    assert "ENC:" not in str(snapshot["servers"][0]["auth"])

    # Get result detail
    result_handler = ResultHandler()
    result, status = result_handler.get(result_id)
    assert status == 200
    detail = result["data"]
    # Result fields are now at top level of response
    assert detail["metadata"]["job_id"] == "portal-job-1"
    assert "tables/buses.json" in detail["artifacts"]

    # Generate report
    result, status = result_handler.report(result_id)
    assert status == 200
    assert result["data"]["path"].endswith("report.md")

    # Archive result
    result, status = result_handler.archive(result_id)
    assert status == 200
    assert result["data"]["path"].endswith(".tar.gz")

    # Check audit entries
    audit_handler = AuditHandler()
    result, status = audit_handler.list()
    assert status == 200
    assert len(result["data"]["entries"]) > 0


def test_portal_rejects_and_updates_invalid_case_rid(tmp_path, monkeypatch):
    """Test case validation and update."""
    monkeypatch.setenv("CLOUDPSS_HOME", str(tmp_path))
    get_path_manager(str(tmp_path))

    case_handler = CaseHandler()

    # Try invalid RID
    result, status = case_handler.create({"name": "Bad", "rid": "dd"})
    assert status == 422
    assert "VALIDATION_ERROR" in result.get("error", {}).get("code", "")

    # Create valid case
    result, status = case_handler.create({"name": "Fixable", "rid": "model/test/old"})
    assert status == 201
    case_id = result["data"]["id"]

    # Update case
    result, status = case_handler.update(case_id, {"rid": "model/test/new", "name": "Fixed"})
    assert status == 200
    assert result["data"]["rid"] == "model/test/new"
    assert result["data"]["name"] == "Fixed"


def test_emt_preflight_treats_empty_channels_as_defaultable(tmp_path, monkeypatch):
    """Test EMT task preflight with empty channels."""
    monkeypatch.setenv("CLOUDPSS_HOME", str(tmp_path))
    get_path_manager(str(tmp_path))

    # Setup server
    server_id = IDGenerator.generate(EntityType.SERVER)
    ServerRegistry().create(
        server_id,
        Server(
            id=server_id,
            name="portal-server",
            url="http://portal.test/",
            owner="tester",
            auth=build_auth_metadata("token", {"token_source": "test"}),
            default=True,
        ),
    )

    # Create case
    case_handler = CaseHandler()
    result, status = case_handler.create({"name": "EMT Case", "rid": "model/test/emt"})
    assert status == 201
    case_id = result["data"]["id"]

    # Create EMT task
    task_handler = TaskHandler()
    result, status = task_handler.create({"case_id": case_id, "name": "EMT", "type": "emt"})
    assert status == 201
    task_id = result["data"]["id"]

    # Run preflight
    result, status = task_handler.preflight(task_id)
    assert status == 200
    preflight = result["data"]
    assert preflight["ok"] is True

    channel_check = next(
        item for item in preflight["checks"] if item["name"] == "EMT Channels"
    )
    assert channel_check["ok"] is True
    assert "默认通道" in channel_check["message"]


def test_portal_updates_task_config_and_exposes_case_plan(tmp_path, monkeypatch):
    """Test task update and case detail."""
    monkeypatch.setenv("CLOUDPSS_HOME", str(tmp_path))
    get_path_manager(str(tmp_path))

    # Setup server
    server_id = IDGenerator.generate(EntityType.SERVER)
    ServerRegistry().create(
        server_id,
        Server(
            id=server_id,
            name="portal-server",
            url="http://portal.test/",
            owner="tester",
            auth=build_auth_metadata("token", {"token_source": "test"}),
            default=True,
        ),
    )

    # Create case
    case_handler = CaseHandler()
    result, status = case_handler.create({"name": "Editable", "rid": "model/test/edit"})
    assert status == 201
    case_id = result["data"]["id"]

    # Create task
    task_handler = TaskHandler()
    result, status = task_handler.create(
        {"case_id": case_id, "name": "Editable PF", "type": "powerflow"}
    )
    assert status == 201
    task_id = result["data"]["id"]

    # Update task
    result, status = task_handler.update(
        task_id,
        {
            "name": "Editable EMT",
            "type": "emt",
            "model_source": "examples/basic/ieee3-emt-prepared.yaml",
            "channels": "plot-2/vac:0,plot-0/#wr1:0",
        },
    )
    assert status == 200
    updated = result["data"]
    assert updated["name"] == "Editable EMT"
    assert updated["type"] == "emt"
    assert updated["config"]["channels"] == ["plot-2/vac:0", "plot-0/#wr1:0"]
    assert updated["config"]["model_source"].endswith(
        "examples/basic/ieee3-emt-prepared.yaml"
    )

    # Get case detail
    result, status = case_handler.get(case_id)
    assert status == 200
    detail = result["data"]
    assert detail["model"]["server"]["auth"]["encrypted_token"] == "<redacted>"


def test_result_summary_includes_chart_data(tmp_path, monkeypatch):
    """Test result summary includes chart data."""
    monkeypatch.setenv("CLOUDPSS_HOME", str(tmp_path))
    get_path_manager(str(tmp_path))

    # Mock cloudpss module
    class FakeResult:
        def getBuses(self):
            return [
                {
                    "data": {
                        "columns": [
                            {"name": "bus", "data": ["1", "2"]},
                            {"name": "v", "data": [1.01, 0.98]},
                        ]
                    }
                }
            ]

        def getBranches(self):
            return [
                {
                    "data": {
                        "columns": [
                            {"name": "branch", "data": ["1-2"]},
                            {"name": "p", "data": [10.0]},
                        ]
                    }
                }
            ]

    class FakeJob:
        id = "chart-job"
        result = FakeResult()

        def status(self):
            return 1

    class FakeModel:
        name = "Chart Model"

        @classmethod
        def fetch(cls, _rid):
            return cls()

        def runPowerFlow(self):
            return FakeJob()

    monkeypatch.setitem(
        sys.modules,
        "cloudpss",
        types.SimpleNamespace(Model=FakeModel, setToken=lambda token: None),
    )

    # Setup server
    server_id = IDGenerator.generate(EntityType.SERVER)
    ServerRegistry().create(
        server_id,
        Server(
            id=server_id,
            name="portal-server",
            url="http://portal.test/",
            owner="tester",
            auth=build_auth_metadata("token", {"token_source": "test"}),
            default=True,
        ),
    )

    # Create case and task
    case_handler = CaseHandler()
    result, status = case_handler.create({"name": "Chart", "rid": "model/test/chart"})
    case_id = result["data"]["id"]

    task_handler = TaskHandler()
    result, status = task_handler.create(
        {"case_id": case_id, "name": "Chart PF", "type": "powerflow"}
    )
    task_id = result["data"]["id"]

    # Run task
    result, status = task_handler.run(task_id, {"timeout": 10})
    result_id = result["data"]["result_id"]

    # Get result summary
    result_handler = ResultHandler()
    result, status = result_handler.get(result_id)
    assert status == 200
    summary = result["data"]["summary"]
    assert summary["bus_chart"]["value_key"] == "v"
    assert summary["bus_chart"]["points"][0]["y"] == 1.01
