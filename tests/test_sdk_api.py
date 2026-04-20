import os
from copy import deepcopy

import pytest

from cloudpss import Job, Model, setToken
from cloudpss.model import ModelRevision
from cloudpss.model.implements import ModelImplement
from cloudpss.model.implements.component import Component


def build_local_model(with_diagram=True):
    implements = {}
    if with_diagram:
        implements["diagram"] = {
            "canvas": [{"key": "canvas_0"}],
            "cells": {},
        }

    return Model(
        {
            "name": "local-model",
            "rid": "model/test/local-model",
            "jobs": [],
            "configs": [],
            "context": {"currentJob": 0, "currentConfig": 0},
            "revision": {
                "hash": "local-hash",
                "version": 4,
                "implements": implements,
                "parameters": [],
                "pins": {},
                "documentation": {},
            },
        }
    )


def build_local_runnable_model():
    return Model(
        {
            "name": "local-runnable-model",
            "rid": "model/test/local-runnable-model",
            "jobs": [
                {
                    "name": "power flow",
                    "rid": "function/CloudPSS/power-flow",
                    "args": {"solver": "nr"},
                }
            ],
            "configs": [{"name": "default", "args": {}}],
            "context": {"currentJob": 0, "currentConfig": 0},
            "revision": {
                "hash": "local-runnable-hash",
                "version": 4,
                "implements": {
                    "diagram": {
                        "canvas": [{"key": "canvas_0"}],
                        "cells": {},
                    }
                },
                "parameters": [
                    {
                        "items": [
                            {"key": "base_kv", "value": 110},
                        ]
                    }
                ],
                "pins": {},
                "documentation": {},
            },
        }
    )


def build_local_job(**overrides):
    payload = {
        "id": "job-local-1",
        "args": {},
        "createTime": "2026-03-16T00:00:00Z",
        "startTime": None,
        "endTime": None,
        "status": 0,
        "context": ["function/CloudPSS/emtp"],
        "user": "holdme",
        "priority": 0,
        "policy": {},
        "machine": {"id": "machine-1", "name": "local"},
        "input": "ws://input",
        "output": "ws://output",
        "position": 0,
    }
    payload.update(overrides)
    return Job(**payload)


class TestLocalModelBehavior:
    def test_set_token_only_updates_environment(self, monkeypatch):
        monkeypatch.delenv("CLOUDPSS_TOKEN", raising=False)

        setToken("unit-test-token")

        assert os.environ["CLOUDPSS_TOKEN"] == "unit-test-token"

    def test_component_lifecycle_on_local_model(self):
        model = build_local_model()

        component = model.addComponent(
            "model/CloudPSS/resistor",
            "R1",
            {"resistance": 10},
            {"p": {}, "n": {}},
        )

        assert isinstance(component, Component)
        assert model.getComponentByKey(component.id).label == "R1"
        assert component.id in model.getComponentsByRid("model/CloudPSS/resistor")

        update_result = model.updateComponent(component.id, args={"resistance": 20})
        assert update_result is None
        assert model.getComponentByKey(component.id).args["resistance"] == 20

        assert model.removeComponent(component.id) is True
        assert model.getAllComponents() == {}

    def test_model_without_diagram_rejects_component_operations(self):
        model = build_local_model(with_diagram=False)

        with pytest.raises(ValueError):
            model.getAllComponents()

        with pytest.raises(ValueError):
            model.addComponent("model/CloudPSS/resistor", "R1", {}, {})

    def test_model_dump_and_load_roundtrip(self, tmp_path):
        model = build_local_model()
        model.addComponent(
            "model/CloudPSS/resistor",
            "R1",
            {"resistance": 10},
            {"p": {}, "n": {}},
        )
        export_path = tmp_path / "local-model.yaml"

        Model.dump(model, str(export_path), compress=None)
        loaded_model = Model.load(str(export_path))

        assert export_path.exists()
        assert loaded_model.name == model.name
        assert loaded_model.rid == model.rid
        assert len(loaded_model.getAllComponents()) == 1

    def test_model_fetch_many_builds_expected_query_variables(self, monkeypatch):
        captured = {}

        def fake_graphql_request(query, variables, **kwargs):
            captured["query"] = query
            captured["variables"] = variables
            captured["kwargs"] = kwargs
            return {
                "data": {
                    "models": {
                        "items": [
                            {
                                "rid": "model/holdme/IEEE39",
                                "name": "IEEE39",
                                "description": "verified case",
                                "owner": "holdme",
                                "tags": [],
                                "updatedAt": "2026-03-16T00:00:00Z",
                            }
                        ]
                    }
                }
            }

        monkeypatch.setattr(
            "cloudpss.model.model.graphql_request", fake_graphql_request
        )
        monkeypatch.setattr("cloudpss.model.model.userName", lambda: "holdme")

        result = Model.fetchMany(
            name="IEEE",
            cursor=["next-page"],
            pageSize=5,
            owner="*",
            baseUrl="https://example.test",
        )

        assert len(result) == 1
        assert "models" in captured["query"]
        assert captured["variables"]["input"]["cursor"] == ["next-page"]
        assert captured["variables"]["input"]["limit"] == 5
        assert captured["variables"]["input"]["owner"] is None
        assert captured["variables"]["input"]["_search"] == "IEEE"
        assert captured["kwargs"]["baseUrl"] == "https://example.test"

    def test_model_fetch_many_raises_first_graphql_error_message(self, monkeypatch):
        def fake_graphql_request(query, variables, **kwargs):
            return {"errors": [{"message": "permission denied"}]}

        monkeypatch.setattr(
            "cloudpss.model.model.graphql_request", fake_graphql_request
        )
        monkeypatch.setattr("cloudpss.model.model.userName", lambda: "holdme")

        with pytest.raises(Exception, match="permission denied"):
            Model.fetchMany(pageSize=1)

    def test_model_revision_serialization_uses_real_sdk_object(self):
        revision = build_local_model().revision
        revision_dict = revision.toJSON()

        assert isinstance(revision, ModelRevision)
        assert revision_dict["hash"] == "local-hash"
        assert "diagram" in revision_dict["implements"]

    def test_model_revision_get_implements_returns_real_sdk_wrapper(self):
        revision = build_local_model().revision

        implements = revision.getImplements()

        assert isinstance(implements, ModelImplement)
        assert implements.getDiagram() is not None
        assert "diagram" in implements.toJSON()

    def test_model_revision_create_omits_existing_hash_from_payload(self, monkeypatch):
        revision = build_local_model().revision
        captured = {}

        def fake_graphql_request(query, variables, **kwargs):
            captured["query"] = query
            captured["variables"] = variables
            captured["kwargs"] = kwargs
            return {"data": {"createModelRevision": {"hash": "created-hash"}}}

        monkeypatch.setattr(
            "cloudpss.model.revision.graphql_request", fake_graphql_request
        )

        created = ModelRevision.create(
            revision,
            parentHash="parent-hash",
            baseUrl="https://example.test",
        )

        assert created["hash"] == "created-hash"
        assert "createModelRevision" in captured["query"]
        assert captured["variables"]["a"]["parent"] == "parent-hash"
        assert "hash" not in captured["variables"]["a"]
        assert (
            captured["variables"]["a"]["implements"]["diagram"]["canvas"][0]["key"]
            == "canvas_0"
        )
        assert captured["kwargs"]["baseUrl"] == "https://example.test"

    def test_model_revision_run_creates_revision_then_job(self, monkeypatch):
        revision = build_local_model().revision
        job = {
            "rid": "function/CloudPSS/power-flow",
            "name": "power flow",
            "args": {"@queue": 1},
        }
        config = {"name": "default", "args": {}}
        captured = {}

        def fake_create(revision_obj, **kwargs):
            captured["create_revision"] = revision_obj
            captured["create_kwargs"] = kwargs
            return {"hash": "created-hash"}

        def fake_job_create(
            revision_hash,
            job_payload,
            config_payload,
            name=None,
            rid=None,
            policy=None,
            **kwargs,
        ):
            captured["job_call"] = {
                "revision_hash": revision_hash,
                "job": job_payload,
                "config": config_payload,
                "name": name,
                "rid": rid,
                "policy": policy,
                "kwargs": kwargs,
            }
            return {"id": "job-123"}

        monkeypatch.setattr(ModelRevision, "create", staticmethod(fake_create))
        monkeypatch.setattr("cloudpss.model.revision.Job.create", fake_job_create)

        result = revision.run(
            job,
            config,
            name="local revision run",
            policy={"queue": "test"},
            stop_on_entry=True,
            rid="model/test/local-model",
            baseUrl="https://example.test",
        )

        assert result == {"id": "job-123"}
        assert captured["create_revision"] is revision
        assert captured["create_kwargs"]["baseUrl"] == "https://example.test"
        assert captured["job_call"]["revision_hash"] == "created-hash"
        assert captured["job_call"]["job"]["args"]["stop_on_entry"] is True
        assert captured["job_call"]["config"] is config
        assert captured["job_call"]["name"] == "local revision run"
        assert captured["job_call"]["rid"] == "model/test/local-model"
        assert captured["job_call"]["policy"] == {"queue": "test"}
        assert captured["job_call"]["kwargs"]["baseUrl"] == "https://example.test"

    def test_model_run_uses_context_defaults_and_revision_delegate(self, monkeypatch):
        model = build_local_runnable_model()
        captured = {}

        def fake_revision_run(job, config, name=None, rid=None, **kwargs):
            captured["job"] = job
            captured["config"] = config
            captured["name"] = name
            captured["rid"] = rid
            captured["kwargs"] = kwargs
            return {"id": "delegated-job"}

        monkeypatch.setattr(model.revision, "run", fake_revision_run)

        result = model.run(name="delegated model run", baseUrl="https://example.test")

        assert result == {"id": "delegated-job"}
        assert captured["job"] is model.jobs[0]
        assert captured["config"] is model.configs[0]
        assert captured["config"]["args"]["base_kv"] == 110
        assert captured["name"] == "delegated model run"
        assert captured["rid"] == model.rid
        assert captured["kwargs"]["baseUrl"] == "https://example.test"

    def test_model_fetch_topology_uses_default_implement_type_and_config(
        self, monkeypatch
    ):
        model = build_local_runnable_model()
        captured = {}

        def fake_fetch_topology(implement_type, config, maximum_depth, **kwargs):
            captured["implement_type"] = implement_type
            captured["config"] = config
            captured["maximum_depth"] = maximum_depth
            captured["kwargs"] = kwargs
            return {"components": {}}

        monkeypatch.setattr(model.revision, "fetchTopology", fake_fetch_topology)

        topology = model.fetchTopology(maximumDepth=2, baseUrl="https://example.test")

        assert topology == {"components": {}}
        assert captured["implement_type"] == "emtp"
        assert captured["config"] is model.configs[0]
        assert captured["maximum_depth"] == 2
        assert captured["kwargs"]["baseUrl"] == "https://example.test"

    def test_model_run_sfemt_selects_sfemt_job_and_delegates(self, monkeypatch):
        model = build_local_runnable_model()
        model.jobs = [
            {
                "name": "power flow",
                "rid": "function/CloudPSS/power-flow",
                "args": {},
            },
            {
                "name": "sfemt",
                "rid": "function/CloudPSS/sfemt",
                "args": {},
            },
        ]
        captured = {}

        def fake_run(job=None, config=None, **kwargs):
            captured["job"] = job
            captured["config"] = config
            captured["kwargs"] = kwargs
            return {"id": "sfemt-job"}

        monkeypatch.setattr(model, "run", fake_run)

        result = model.runSFEMT(baseUrl="https://example.test")

        assert result == {"id": "sfemt-job"}
        assert captured["job"]["rid"] == "function/CloudPSS/sfemt"
        assert captured["config"] is model.configs[0]
        assert captured["kwargs"]["baseUrl"] == "https://example.test"

    def test_model_save_with_key_updates_rid_and_calls_update(self, monkeypatch):
        model = build_local_model()
        captured = {}

        monkeypatch.setattr("cloudpss.model.model.userName", lambda: "holdme")

        def fake_update(model_obj):
            captured["model"] = model_obj
            return {"updated": True}

        monkeypatch.setattr(Model, "update", staticmethod(fake_update))

        result = model.save("saved-model")

        assert result == {"updated": True}
        assert model.rid == "model/holdme/saved-model"
        assert captured["model"] is model

    def test_model_save_with_key_falls_back_to_create_on_update_failure(
        self, monkeypatch
    ):
        model = build_local_model()
        captured = {}

        monkeypatch.setattr("cloudpss.model.model.userName", lambda: "holdme")

        def fake_update(model_obj):
            captured["update_model"] = model_obj
            raise Exception("update failed")

        def fake_create(model_obj):
            captured["create_model"] = model_obj
            return {"created": True}

        monkeypatch.setattr(Model, "update", staticmethod(fake_update))
        monkeypatch.setattr(Model, "create", staticmethod(fake_create))

        result = model.save("branch-v2")

        assert result == {"created": True}
        assert model.rid == "model/holdme/branch-v2"
        assert captured["update_model"] is model
        assert captured["create_model"] is model

    def test_model_save_without_key_updates_existing_owned_model(self, monkeypatch):
        model = build_local_model()
        model.rid = "model/holdme/existing-model"
        captured = {}

        monkeypatch.setattr("cloudpss.model.model.userName", lambda: "holdme")

        def fake_update(model_obj):
            captured["model"] = model_obj
            return {"updated": True}

        monkeypatch.setattr(Model, "update", staticmethod(fake_update))

        result = model.save()

        assert result == {"updated": True}
        assert captured["model"] is model

    def test_job_read_builds_receiver_and_connects(self, monkeypatch):
        job = build_local_job(baseUrl="https://example.test")
        captured = {}

        class FakeReceiver:
            def __init__(self, output, baseUrl=None, job=None):
                captured["output"] = output
                captured["baseUrl"] = baseUrl
                captured["job"] = job

            def connect(self, **kwargs):
                captured["connect_kwargs"] = kwargs

        monkeypatch.setattr("cloudpss.job.job.MessageStreamReceiver", FakeReceiver)

        receiver = job.read(timeout=5)

        assert isinstance(receiver, FakeReceiver)
        assert captured["output"] == "ws://output"
        assert captured["baseUrl"] == "https://example.test"
        assert captured["job"] is job
        assert captured["connect_kwargs"] == {"timeout": 5}

    def test_job_write_builds_sender_and_connects(self, monkeypatch):
        job = build_local_job(baseUrl="https://example.test")
        captured = {}

        class FakeSender:
            def __init__(self, input_url, baseUrl=None):
                captured["input"] = input_url
                captured["baseUrl"] = baseUrl

            def connect_legacy(self, **kwargs):
                captured["connect_kwargs"] = kwargs

        monkeypatch.setattr("cloudpss.job.job.MessageStreamSender", FakeSender)

        sender = job.write(timeout=5)

        assert isinstance(sender, FakeSender)
        assert captured["input"] == "ws://input"
        assert captured["baseUrl"] == "https://example.test"
        assert captured["connect_kwargs"] == {"timeout": 5}

    def test_job_abort_calls_graphql_with_timeout(self, monkeypatch):
        job = build_local_job()
        captured = {}

        def fake_graphql_request(query, variables, **kwargs):
            captured["query"] = query
            captured["variables"] = variables
            captured["kwargs"] = kwargs
            return {"data": {"job": {"id": job.id, "status": 2}}}

        monkeypatch.setattr("cloudpss.job.job.graphql_request", fake_graphql_request)

        result = job.abort(timeout=7, baseUrl="https://example.test")

        assert result is None
        assert "abortJob" in captured["query"]
        assert captured["variables"] == {"input": {"id": job.id, "timeout": 7}}
        assert captured["kwargs"]["baseUrl"] == "https://example.test"

    def test_job_dump_and_load_roundtrip_raw_data(self, tmp_path):
        payload = {
            "id": "job-local-1",
            "status": 0,
            "context": ["function/CloudPSS/power-flow"],
        }
        export_path = tmp_path / "job.yaml"

        Job.dump(payload, str(export_path), compress=None)
        loaded = Job.load(str(export_path))

        assert export_path.exists()
        assert isinstance(loaded, dict)
        assert loaded == payload


@pytest.mark.integration
class TestLiveCloudPSSModelAndJob:
    def test_fetch_model_returns_expected_rid(self, integration_model):
        assert integration_model.rid == os.environ.get(
            "TEST_MODEL_RID", "model/chenying/IEEE39"
        )
        assert integration_model.name
        assert integration_model.jobs
        assert integration_model.configs

    def test_fetch_invalid_model_rid_raises(self, live_auth):
        with pytest.raises(Exception):
            Model.fetch("model/CloudPSS/example-resistor")

    def test_fetch_many_filters_by_owner_and_name(self, integration_model):
        matches = Model.fetchMany(
            owner="chenying",
            name="IEEE39",
            pageSize=10,
        )

        assert isinstance(matches, list)
        assert matches
        assert integration_model.rid in {item["rid"] for item in matches}
        assert all(item["owner"] == "chenying" for item in matches)
        assert all(
            {"rid", "name", "owner", "description", "tags", "updatedAt"} <= item.keys()
            for item in matches
        )

    def test_run_emt_job_can_be_fetched(self, integration_model):
        job = integration_model.runEMT()
        fetched_job = Job.fetch(job.id)

        assert job.id
        assert job.status() in {0, 1, 2}
        assert fetched_job.id == job.id

    def test_model_save_with_key_creates_disposable_branch_when_opted_in(
        self, integration_model, integration_save_key
    ):
        working_model = Model(deepcopy(integration_model.toJSON()))

        response = working_model.save(integration_save_key)

        assert working_model.rid.endswith(f"/{integration_save_key}")
        assert "data" in response
        assert (
            response["data"].get("createModel", {}).get("rid") == working_model.rid
            or response["data"].get("updateModel", {}).get("rid") == working_model.rid
        )


@pytest.mark.integration
class TestLiveEMTPreparationStructure:
    def test_ieee3_contains_fault_meter_and_output_channel_chain(
        self, integration_ieee3_model
    ):
        components = integration_ieee3_model.getAllComponents()

        faults = [
            component
            for component in components.values()
            if getattr(component, "definition", None)
            == "model/CloudPSS/_newFaultResistor_3p"
        ]
        voltage_meters = [
            component
            for component in components.values()
            if getattr(component, "definition", None)
            == "model/CloudPSS/_NewVoltageMeter"
        ]

        assert len(faults) == 1
        assert len(voltage_meters) == 1
        assert {"fs", "fe", "chg", "ft"} <= faults[0].args.keys()

        voltage_signal = voltage_meters[0].args["V"]
        assert voltage_signal.startswith("#")

        output_channels = [
            component
            for component in components.values()
            if getattr(component, "definition", None) == "model/CloudPSS/_newChannel"
        ]
        matching_channels = [
            component
            for component in output_channels
            if component.args.get("Name") == voltage_signal.lstrip("#")
        ]

        assert len(matching_channels) == 1
        assert matching_channels[0].pins["0"] == voltage_signal

        emt_job = next(
            job
            for job in integration_ieee3_model.jobs
            if job["rid"] == "function/CloudPSS/emtps"
        )
        assert any(
            matching_channels[0].id in group["4"]
            for group in emt_job["args"]["output_channels"]
        )

    def test_ieee3_working_copy_can_adjust_fault_and_output_config_locally(
        self, integration_ieee3_model
    ):
        working_model = Model(deepcopy(integration_ieee3_model.toJSON()))
        components = working_model.getAllComponents()

        fault = next(
            component
            for component in components.values()
            if getattr(component, "definition", None)
            == "model/CloudPSS/_newFaultResistor_3p"
        )
        voltage_channel = next(
            component
            for component in components.values()
            if getattr(component, "definition", None) == "model/CloudPSS/_newChannel"
            and component.args.get("Name") == "vac"
        )

        working_model.updateComponent(
            fault.id,
            args={
                "fs": {"source": "2.5", "ɵexp": ""},
                "fe": {"source": "2.7", "ɵexp": ""},
            },
        )
        working_model.updateComponent(
            voltage_channel.id,
            args={"Freq": {"source": "2000", "ɵexp": ""}},
        )

        updated_fault = working_model.getComponentByKey(fault.id)
        updated_channel = working_model.getComponentByKey(voltage_channel.id)
        emt_job = next(
            job for job in working_model.jobs if job["rid"] == "function/CloudPSS/emtps"
        )
        emt_job["args"]["output_channels"][0]["1"] = 2000
        emt_job["args"]["output_curve"][0]["1"] = "oscilloscope"

        assert updated_fault.args["fs"]["source"] == "2.5"
        assert updated_fault.args["fe"]["source"] == "2.7"
        assert updated_channel.args["Freq"]["source"] == "2000"
        assert emt_job["args"]["output_channels"][0]["1"] == 2000
        assert emt_job["args"]["output_curve"][0]["1"] == "oscilloscope"


@pytest.mark.integration
class TestLiveComponentWorkflow:
    def test_local_working_copy_supports_component_lifecycle_and_topology_fetch(
        self, integration_model
    ):
        working_model = Model(deepcopy(integration_model.toJSON()))
        original_resistors = working_model.getComponentsByRid("model/CloudPSS/resistor")

        component = working_model.addComponent(
            "model/CloudPSS/resistor",
            "R_codex_integration",
            {"resistance": 10},
            {"p": {"x": 0, "y": 0}, "n": {"x": 50, "y": 0}},
            position={"x": 100, "y": 200},
        )

        updated_resistors = working_model.getComponentsByRid("model/CloudPSS/resistor")
        assert len(updated_resistors) == len(original_resistors) + 1
        assert (
            working_model.getComponentByKey(component.id).label == "R_codex_integration"
        )

        working_model.updateComponent(component.id, args={"resistance": 50})
        assert working_model.getComponentByKey(component.id).args["resistance"] == 50

        topology = working_model.fetchTopology(implementType="powerFlow")
        topology_dict = topology.toJSON()
        # 这里只证明 fetched 工作副本仍能取回拓扑结果；是否反映未保存本地改动，
        # 需要由下面的负向 live 测试单独界定。
        assert "components" in topology_dict
        assert topology_dict["components"]

        assert working_model.removeComponent(component.id) is True
        with pytest.raises(KeyError):
            working_model.getComponentByKey(component.id)

    def test_fetch_topology_on_fetched_working_copy_does_not_reflect_unsaved_local_additions(
        self, integration_model
    ):
        working_model = Model(deepcopy(integration_model.toJSON()))
        component = working_model.addComponent(
            "model/CloudPSS/resistor",
            "R_codex_topology_probe",
            {"resistance": 10},
            {"p": {"x": 0, "y": 0}, "n": {"x": 50, "y": 0}},
            position={"x": 100, "y": 200},
        )

        topology = working_model.fetchTopology(implementType="powerFlow").toJSON()

        # 当前 SDK 的 fetchTopology() 对 fetched 模型仍基于 revision.hash 拉取远端拓扑，
        # 不会把本地工作副本中尚未保存的 add/update/remove 直接投影进返回结果。
        assert component.id not in topology["components"]
        assert f"/{component.id}" not in topology["components"]


@pytest.mark.integration
class TestLiveModelRevisionBehavior:
    @pytest.mark.parametrize("implement_type", ["emtp", "powerFlow"])
    def test_fetch_topology_returns_components_and_mappings(
        self, integration_model, implement_type
    ):
        topology = integration_model.revision.fetchTopology(
            implement_type,
            integration_model.configs[0],
            1,
        )
        topology_dict = topology.toJSON()

        assert "components" in topology_dict
        assert "mappings" in topology_dict
        assert isinstance(topology_dict["components"], dict)
        assert topology_dict["components"]

    def test_revision_run_creates_fetchable_job(self, integration_model):
        job = integration_model.revision.run(
            integration_model.jobs[0],
            integration_model.configs[0],
            name="codex revision.run integration test",
            rid=integration_model.rid,
        )
        fetched_job = Job.fetch(job.id)

        assert job.id
        assert job.status() in {0, 1, 2}
        assert fetched_job.id == job.id
        assert fetched_job.context[0].startswith("function/CloudPSS/")
