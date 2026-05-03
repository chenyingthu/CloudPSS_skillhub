"""Portal state/API helper tests."""

import sys
import types
from pathlib import Path

from cloudpss_skills_v3.master_organizer.core import (
    EntityType,
    IDGenerator,
    Server,
    ServerRegistry,
    get_path_manager,
)
from cloudpss_skills_v3.master_organizer.core.server_auth import build_auth_metadata
from cloudpss_skills_v3.master_organizer.portal import state


def test_portal_snapshot_create_and_run_powerflow(tmp_path, monkeypatch):
    monkeypatch.setenv("CLOUDPSS_HOME", str(tmp_path))
    get_path_manager(str(tmp_path))

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

    monkeypatch.setitem(sys.modules, "cloudpss", types.SimpleNamespace(Model=FakeModel, setToken=lambda token: None))

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

    created_case = state.create_case({"name": "Portal Case", "rid": "model/test/portal", "tags": "portal,pf"})
    created_task = state.create_task({"case_id": created_case["id"], "name": "Portal PF", "type": "powerflow"})
    execution = state.run_task(created_task["id"], timeout_seconds=10)

    snapshot = state.organizer_snapshot()
    detail = state.result_detail(execution["result_id"])
    report = state.report_result(execution["result_id"])
    archive = state.archive_result_for_portal(execution["result_id"])

    assert snapshot["workspace"]["counts"]["cases"] == 1
    assert snapshot["workspace"]["counts"]["tasks"] == 1
    assert snapshot["workspace"]["counts"]["results"] == 1
    assert snapshot["servers"][0]["auth"]["encrypted_token"] == "<redacted>"
    assert snapshot["servers"][0]["auth"]["has_encrypted_token"] is True
    assert "ENC:" not in str(snapshot["servers"][0]["auth"])
    assert detail["result"]["metadata"]["job_id"] == "portal-job-1"
    assert "tables/buses.json" in detail["artifacts"]
    assert report["path"].endswith("report.md")
    report_text = (tmp_path / "results" / execution["result_id"] / "report.md").read_text(encoding="utf-8")
    assert "## Case" in report_text
    assert "## Task" in report_text
    assert "### Task Config" in report_text
    assert "## Result Summary" in report_text
    assert archive["path"].endswith(".tar.gz")
    assert state.audit_entries()


def test_portal_rejects_and_updates_invalid_case_rid(tmp_path, monkeypatch):
    monkeypatch.setenv("CLOUDPSS_HOME", str(tmp_path))
    get_path_manager(str(tmp_path))

    try:
        state.create_case({"name": "Bad", "rid": "dd"})
    except ValueError as exc:
        assert "RID" in str(exc)
    else:
        raise AssertionError("invalid RID was accepted")

    case = state.create_case({"name": "Fixable", "rid": "model/test/old"})
    updated = state.update_case(case["id"], {"rid": "model/test/new", "name": "Fixed"})

    assert updated["rid"] == "model/test/new"
    assert updated["name"] == "Fixed"


def test_csv_preview_handles_quoted_cells(tmp_path):
    csv_path = tmp_path / "trace.csv"
    csv_path.write_text('time,value,label\n0,"1,234","a,b"\n1,2,c\n', encoding="utf-8")

    preview = state._csv_preview(Path(csv_path))

    assert preview["headers"] == ["time", "value", "label"]
    assert preview["rows"][0] == ["0", "1,234", "a,b"]


def test_emt_preflight_treats_empty_channels_as_defaultable(tmp_path, monkeypatch):
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
    case = state.create_case({"name": "EMT Case", "rid": "model/test/emt"})
    task = state.create_task({"case_id": case["id"], "name": "EMT", "type": "emt"})

    preflight = state.task_preflight(task["id"])

    assert preflight["ok"] is True
    channel_check = next(item for item in preflight["checks"] if item["name"] == "EMT Channels")
    assert channel_check["ok"] is True
    assert "默认通道" in channel_check["message"]


def test_portal_updates_task_config_and_exposes_case_plan(tmp_path, monkeypatch):
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
    case = state.create_case({"name": "Editable", "rid": "model/test/edit"})
    task = state.create_task({"case_id": case["id"], "name": "Editable PF", "type": "powerflow"})

    updated = state.update_task(
        task["id"],
        {
            "name": "Editable EMT",
            "type": "emt",
            "model_source": "examples/basic/ieee3-emt-prepared.yaml",
            "channels": "plot-2/vac:0,plot-0/#wr1:0",
        },
    )
    detail = state.case_detail(case["id"])

    assert updated["name"] == "Editable EMT"
    assert updated["type"] == "emt"
    assert updated["config"]["channels"] == ["plot-2/vac:0", "plot-0/#wr1:0"]
    assert updated["config"]["model_source"].endswith("examples/basic/ieee3-emt-prepared.yaml")
    assert detail["simulation_plan"]["task_count"] == 1
    assert detail["simulation_plan"]["runnable_count"] == 1
    assert detail["model"]["server"]["auth"]["encrypted_token"] == "<redacted>"


def test_result_summary_includes_chart_data(tmp_path, monkeypatch):
    monkeypatch.setenv("CLOUDPSS_HOME", str(tmp_path))
    get_path_manager(str(tmp_path))

    class FakeResult:
        def getBuses(self):
            return [{"data": {"columns": [{"name": "bus", "data": ["1", "2"]}, {"name": "v", "data": [1.01, 0.98]}]}}]

        def getBranches(self):
            return [{"data": {"columns": [{"name": "branch", "data": ["1-2"]}, {"name": "p", "data": [10.0]}]}}]

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

    monkeypatch.setitem(sys.modules, "cloudpss", types.SimpleNamespace(Model=FakeModel, setToken=lambda token: None))
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
    case = state.create_case({"name": "Chart", "rid": "model/test/chart"})
    task = state.create_task({"case_id": case["id"], "name": "Chart PF", "type": "powerflow"})
    execution = state.run_task(task["id"], timeout_seconds=10)

    summary = state.result_summary(execution["result_id"])

    assert summary["bus_chart"]["value_key"] == "v"
    assert summary["bus_chart"]["points"][0]["y"] == 1.01


def _write_demo_model(path: Path, *, cell_key: str = "line_1", cell_id: str = "line_1"):
    path.write_text(
        f"""
name: Demo
revision:
  implements:
    diagram:
      cells:
        bus_1:
          id: bus_1
          label: Bus 1
          definition: model/CloudPSS/_newBus_3p
          args:
            Name: BUS1
            v: 1.0
        {cell_key}:
          id: {cell_id}
          label: Line 1
          definition: model/CloudPSS/TransmissionLine
          args:
            R: 0.01
            X: 0.1
""",
        encoding="utf-8",
    )


def test_model_editor_groups_and_saves_component_args(tmp_path):
    model_path = tmp_path / "model.yaml"
    _write_demo_model(model_path)
    case = state.create_case({"name": "Bound Model", "rid": "model/test/bound", "model_source": str(model_path)})

    summary = state.model_summary(model_path)
    saved = state.save_model_table_edits(
        {"case_id": case["id"], "path": str(model_path), "updates": [{"cell_key": "line_1", "arg": "R", "value": 0.02}]}
    )
    updated = state.model_summary(model_path)

    assert summary["component_count"] == 2
    assert "Bus" in summary["groups"]
    assert "Line" in summary["groups"]
    assert saved["changed"] == 1
    assert Path(saved["backup_path"]).exists()
    line = updated["groups"]["Line"]["rows"][0]
    assert line["args"]["R"] == 0.02


def test_model_editor_saves_by_cell_key_when_cell_id_differs(tmp_path):
    model_path = tmp_path / "model.yaml"
    _write_demo_model(model_path, cell_key="line_key", cell_id="display-line-id")
    case = state.create_case({"name": "Keyed Model", "rid": "model/test/keyed", "model_source": str(model_path)})

    saved = state.save_model_table_edits(
        {
            "case_id": case["id"],
            "path": str(model_path),
            "updates": [{"id": "display-line-id", "cell_key": "line_key", "arg": "R", "value": 0.03}],
        }
    )
    updated = state.model_summary(model_path)

    assert saved["changed"] == 1
    assert updated["groups"]["Line"]["rows"][0]["args"]["R"] == 0.03


def test_model_editor_rejects_unbound_paths(tmp_path):
    bound_path = tmp_path / "bound.yaml"
    other_path = tmp_path / "other.yaml"
    _write_demo_model(bound_path)
    _write_demo_model(other_path)
    case = state.create_case({"name": "Bound Model", "rid": "model/test/bound", "model_source": str(bound_path)})

    try:
        state.save_model_table_edits(
            {"case_id": case["id"], "path": str(other_path), "updates": [{"cell_key": "line_1", "arg": "R", "value": 0.02}]}
        )
    except ValueError as exc:
        assert "匹配当前 Case" in str(exc)
    else:
        raise AssertionError("unbound model path was accepted")

    assert state.model_summary(other_path)["groups"]["Line"]["rows"][0]["args"]["R"] == 0.01


def test_case_can_bind_local_model_source_for_editor(tmp_path, monkeypatch):
    monkeypatch.setenv("CLOUDPSS_HOME", str(tmp_path / "workspace"))
    get_path_manager(str(tmp_path / "workspace"))
    model_path = tmp_path / "model.yaml"
    model_path.write_text(
        """
name: Demo
revision:
  implements:
    diagram:
      cells:
        bus_1:
          id: bus_1
          label: Bus 1
          definition: model/CloudPSS/_newBus_3p
          args:
            Name: BUS1
""",
        encoding="utf-8",
    )
    case = state.create_case({"name": "Local Model", "rid": "model/test/local"})
    updated = state.update_case(case["id"], {"model_source": str(model_path)})
    detail = state.case_detail(case["id"])

    assert str(model_path.resolve()) in updated["description"]
    assert detail["model"]["model_source"] == str(model_path.resolve())
    assert detail["model"]["editor"]["editable"] is True
    assert detail["model"]["editor"]["component_count"] == 1


def test_create_case_persists_model_source_and_description_text(tmp_path, monkeypatch):
    monkeypatch.setenv("CLOUDPSS_HOME", str(tmp_path / "workspace"))
    get_path_manager(str(tmp_path / "workspace"))
    model_path = tmp_path / "model.yaml"
    _write_demo_model(model_path)

    case = state.create_case(
        {
            "name": "Created Local",
            "rid": "model/test/created",
            "description": "research note",
            "model_source": str(model_path),
        }
    )
    detail = state.case_detail(case["id"])

    assert detail["model"]["model_source"] == str(model_path.resolve())
    assert state._case_description_text(detail["case"]["description"]) == "research note"
