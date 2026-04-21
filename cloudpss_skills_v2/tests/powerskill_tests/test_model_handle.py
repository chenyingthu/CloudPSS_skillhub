"""Tests for ModelHandle, ComponentInfo, and model manipulation API.

Verifies the architectural fix: skills can manipulate models through the
engine-agnostic ModelHandle abstraction without importing engine SDKs.
"""

from __future__ import annotations

import pytest
from unittest.mock import MagicMock, patch, PropertyMock

from cloudpss_skills_v2.powerskill.model_handle import (
    ModelHandle,
    ComponentInfo,
    ComponentType,
)
from cloudpss_skills_v2.powerapi.base import (
    EngineAdapter,
    EngineConfig,
    SimulationResult,
    SimulationStatus,
    ValidationResult,
)


class StubAdapter(EngineAdapter):
    """Minimal adapter with model manipulation support for testing."""

    def __init__(self, config=None):
        super().__init__(config or EngineConfig(engine_name="stub"))
        self._models: dict = {}
        self._clone_counter = 0

    @property
    def engine_name(self) -> str:
        return "stub"

    def _do_connect(self) -> None:
        pass

    def _do_disconnect(self) -> None:
        self._models.clear()

    def _do_load_model(self, model_id: str) -> bool:
        self._models[model_id] = {
            "line_1": ComponentInfo(
                key="line_1",
                name="Line 1",
                definition="model/CloudPSS/line",
                component_type=ComponentType.BRANCH,
            ),
            "load_1": ComponentInfo(
                key="load_1",
                name="Load 1",
                definition="model/CloudPSS/_newLoad",
                component_type=ComponentType.LOAD,
            ),
            "gen_1": ComponentInfo(
                key="gen_1",
                name="Gen 1",
                definition="model/CloudPSS/_newGenerator",
                component_type=ComponentType.GENERATOR,
            ),
            "tr_1": ComponentInfo(
                key="tr_1",
                name="Transformer 1",
                definition="model/CloudPSS/_newTransformer_3p2w",
                component_type=ComponentType.TRANSFORMER,
            ),
        }
        return True

    def _do_run_simulation(self, config: dict) -> SimulationResult:
        return SimulationResult(
            job_id="test-job",
            status=SimulationStatus.COMPLETED,
            data={"buses": [], "branches": []},
        )

    def _do_get_result(self, job_id: str) -> SimulationResult:
        return SimulationResult(
            job_id=job_id, status=SimulationStatus.COMPLETED, data={}
        )

    def _do_validate_config(self, config: dict) -> ValidationResult:
        return ValidationResult.success()

    def _do_get_components(self, model_id: str) -> list[ComponentInfo]:
        model = self._models.get(model_id, {})
        return list(model.values())

    def _do_remove_component(self, model_id: str, component_key: str) -> bool:
        model = self._models.get(model_id)
        if model and component_key in model:
            del model[component_key]
            return True
        return False

    def _do_update_component_args(
        self, model_id: str, component_key: str, args: dict
    ) -> bool:
        model = self._models.get(model_id)
        if model and component_key in model:
            model[component_key].args = args
            return True
        return False

    def _do_clone_model(self, model_id: str) -> str:
        import copy

        self._clone_counter += 1
        clone_id = f"{model_id}__clone_{self._clone_counter}"
        original = self._models.get(model_id, {})
        self._models[clone_id] = copy.deepcopy(original)
        return clone_id


class BareAdapter(EngineAdapter):
    """Adapter WITHOUT model manipulation support."""

    @property
    def engine_name(self) -> str:
        return "bare"

    def _do_connect(self) -> None:
        pass

    def _do_disconnect(self) -> None:
        pass

    def _do_load_model(self, model_id: str) -> bool:
        return True

    def _do_run_simulation(self, config: dict) -> SimulationResult:
        return SimulationResult(
            job_id="bare-job", status=SimulationStatus.COMPLETED, data={}
        )

    def _do_get_result(self, job_id: str) -> SimulationResult:
        return SimulationResult(
            job_id=job_id, status=SimulationStatus.COMPLETED, data={}
        )

    def _do_validate_config(self, config: dict) -> ValidationResult:
        return ValidationResult.success()


# ---- ComponentInfo tests ----


class TestComponentInfo:
    def test_creation(self):
        ci = ComponentInfo(
            key="line_1",
            name="Line 1",
            definition="model/CloudPSS/line",
            component_type=ComponentType.BRANCH,
        )
        assert ci.key == "line_1"
        assert ci.component_type == ComponentType.BRANCH
        assert ci.args is None

    def test_default_type_is_other(self):
        ci = ComponentInfo(key="x")
        assert ci.component_type == ComponentType.OTHER

    def test_to_dict_roundtrip(self):
        ci = ComponentInfo(
            key="gen_1",
            name="Gen",
            definition="model/CloudPSS/Generator",
            component_type=ComponentType.GENERATOR,
            args={"pf_P": {"source": "100"}},
        )
        d = ci.to_dict()
        ci2 = ComponentInfo.from_dict(d)
        assert ci2.key == ci.key
        assert ci2.name == ci.name
        assert ci2.component_type == ci.component_type
        assert ci2.args == ci.args

    def test_from_dict_defaults(self):
        ci = ComponentInfo.from_dict({})
        assert ci.key == ""
        assert ci.component_type == ComponentType.OTHER


# ---- ComponentType constants ----


class TestComponentType:
    def test_type_constants(self):
        assert ComponentType.BRANCH == "branch"
        assert ComponentType.TRANSFORMER == "transformer"
        assert ComponentType.GENERATOR == "generator"
        assert ComponentType.LOAD == "load"
        assert ComponentType.SHUNT == "shunt"
        assert ComponentType.OTHER == "other"


# ---- ModelHandle tests ----


class TestModelHandle:
    @pytest.fixture
    def adapter(self):
        a = StubAdapter()
        a.connect()
        a.load_model("model/test/IEEE39")
        return a

    def test_creation(self, adapter):
        handle = ModelHandle(adapter, "model/test/IEEE39")
        assert handle.model_id == "model/test/IEEE39"
        assert handle.adapter is adapter

    def test_creation_type_check(self):
        with pytest.raises(TypeError, match="Expected EngineAdapter"):
            ModelHandle("not_an_adapter", "model/test")

    def test_get_components(self, adapter):
        handle = ModelHandle(adapter, "model/test/IEEE39")
        comps = handle.get_components()
        assert len(comps) == 4
        types = {c.component_type for c in comps}
        assert ComponentType.BRANCH in types
        assert ComponentType.LOAD in types
        assert ComponentType.GENERATOR in types
        assert ComponentType.TRANSFORMER in types

    def test_get_components_by_type_branch(self, adapter):
        handle = ModelHandle(adapter, "model/test/IEEE39")
        branches = handle.get_components_by_type(ComponentType.BRANCH)
        assert len(branches) == 1
        assert branches[0].key == "line_1"

    def test_get_components_by_type_generator(self, adapter):
        handle = ModelHandle(adapter, "model/test/IEEE39")
        gens = handle.get_components_by_type(ComponentType.GENERATOR)
        assert len(gens) == 1
        assert gens[0].key == "gen_1"

    def test_get_components_by_type_empty(self, adapter):
        handle = ModelHandle(adapter, "model/test/IEEE39")
        shunts = handle.get_components_by_type(ComponentType.SHUNT)
        assert len(shunts) == 0

    def test_remove_component(self, adapter):
        handle = ModelHandle(adapter, "model/test/IEEE39")
        assert len(handle.get_components()) == 4
        ok = handle.remove_component("line_1")
        assert ok is True
        assert len(handle.get_components()) == 3

    def test_remove_component_nonexistent(self, adapter):
        handle = ModelHandle(adapter, "model/test/IEEE39")
        ok = handle.remove_component("no_such_component")
        assert ok is False
        assert len(handle.get_components()) == 4

    def test_update_component_args(self, adapter):
        handle = ModelHandle(adapter, "model/test/IEEE39")
        ok = handle.update_component_args("gen_1", {"pf_P": {"source": "200"}})
        assert ok is True
        comps = handle.get_components()
        gen = next(c for c in comps if c.key == "gen_1")
        assert gen.args == {"pf_P": {"source": "200"}}

    def test_update_component_nonexistent(self, adapter):
        handle = ModelHandle(adapter, "model/test/IEEE39")
        ok = handle.update_component_args("no_such", {"x": 1})
        assert ok is False

    def test_clone_independence(self, adapter):
        handle = ModelHandle(adapter, "model/test/IEEE39")
        clone = handle.clone()

        assert clone.model_id != handle.model_id
        assert "clone" in clone.model_id

        assert len(clone.get_components()) == 4

        clone.remove_component("line_1")
        assert len(clone.get_components()) == 3

        assert len(handle.get_components()) == 4

    def test_repr(self, adapter):
        handle = ModelHandle(adapter, "model/test/IEEE39")
        r = repr(handle)
        assert "model/test/IEEE39" in r
        assert "stub" in r


# ---- Bare adapter (no model manipulation) ----


class TestBareAdapterModelHandle:
    @pytest.fixture
    def adapter(self):
        a = BareAdapter()
        a.connect()
        return a

    def test_get_components_returns_empty(self, adapter):
        handle = ModelHandle(adapter, "model/test")
        comps = handle.get_components()
        assert comps == []

    def test_remove_component_returns_false(self, adapter):
        handle = ModelHandle(adapter, "model/test")
        ok = handle.remove_component("any")
        assert ok is False

    def test_update_component_returns_false(self, adapter):
        handle = ModelHandle(adapter, "model/test")
        ok = handle.update_component_args("any", {"x": 1})
        assert ok is False

    def test_clone_raises(self, adapter):
        handle = ModelHandle(adapter, "model/test")
        with pytest.raises(NotImplementedError):
            handle.clone()

    def test_get_components_by_type_fallback(self, adapter):
        handle = ModelHandle(adapter, "model/test")
        result = handle.get_components_by_type(ComponentType.BRANCH)
        assert result == []


# ---- SimulationAPI.get_model_handle integration ----


class TestSimulationAPIModelHandle:
    def test_get_model_handle_via_api(self):
        adapter = StubAdapter()
        adapter.connect()
        from cloudpss_skills_v2.powerskill.apis.powerflow import PowerFlowAPI

        api = PowerFlowAPI(adapter)

        handle = api.get_model_handle("model/test/IEEE39")
        assert isinstance(handle, ModelHandle)
        assert handle.model_id == "model/test/IEEE39"

    def test_run_power_flow_with_model_handle(self):
        adapter = StubAdapter()
        adapter.connect()
        from cloudpss_skills_v2.powerskill.apis.powerflow import PowerFlowAPI

        api = PowerFlowAPI(adapter)

        handle = api.get_model_handle("model/test/IEEE39")
        result = api.run_power_flow(model_handle=handle)
        assert result.is_success

    def test_run_power_flow_with_model_id(self):
        adapter = StubAdapter()
        adapter.connect()
        from cloudpss_skills_v2.powerskill.apis.powerflow import PowerFlowAPI

        api = PowerFlowAPI(adapter)

        result = api.run_power_flow(model_id="model/test/IEEE39")
        assert result.is_success

    def test_run_power_flow_no_model_fails(self):
        adapter = StubAdapter()
        adapter.connect()
        from cloudpss_skills_v2.powerskill.apis.powerflow import PowerFlowAPI

        api = PowerFlowAPI(adapter)

        result = api.run_power_flow()
        assert result.status == SimulationStatus.FAILED

    def test_n1_pattern_clone_remove_simulate(self):
        adapter = StubAdapter()
        adapter.connect()
        adapter.load_model("model/test/IEEE39")
        from cloudpss_skills_v2.powerskill.apis.powerflow import PowerFlowAPI

        api = PowerFlowAPI(adapter)

        handle = api.get_model_handle("model/test/IEEE39")
        branches = handle.get_components_by_type(ComponentType.BRANCH)

        for branch in branches:
            working = handle.clone()
            working.remove_component(branch.key)
            result = api.run_power_flow(model_handle=working)
            assert result.is_success


# ---- CloudPSS adapter model manipulation (with mocked SDK) ----


class TestCloudPSSAdapterModelManipulation:
    @pytest.fixture
    def mock_sdk(self):
        with patch("cloudpss.Model") as MockModel, patch("cloudpss.setToken"):
            comp_line = MagicMock()
            comp_line.definition = "model/CloudPSS/line"
            comp_line.name = "Line 1"
            comp_line.label = "Line 1"
            comp_line.args = {"R": {"source": "0.01"}}

            comp_load = MagicMock()
            comp_load.definition = "model/CloudPSS/_newLoad"
            comp_load.name = "Load 1"
            comp_load.label = "Load 1"
            comp_load.args = {"pf_P": {"source": "100"}, "pf_Q": {"source": "20"}}

            comp_gen = MagicMock()
            comp_gen.definition = "model/CloudPSS/_newGenerator"
            comp_gen.name = "Gen 1"
            comp_gen.label = "Gen 1"
            comp_gen.args = {"pf_P": {"source": "200"}}

            mock_model = MagicMock()
            mock_model.name = "IEEE39"
            mock_model.rid = "model/holdme/IEEE39"
            mock_model.getAllComponents.return_value = {
                "line_1": comp_line,
                "load_1": comp_load,
                "gen_1": comp_gen,
            }
            mock_model.removeComponent.return_value = True
            mock_model.updateComponent.return_value = True

            MockModel.fetch.return_value = mock_model
            MockModel.load.return_value = mock_model
            yield MockModel, mock_model

    def test_get_components(self, mock_sdk):
        from cloudpss_skills_v2.powerapi.adapters.cloudpss.powerflow import (
            CloudPSSPowerFlowAdapter,
        )

        adapter = CloudPSSPowerFlowAdapter()
        adapter.connect()
        adapter.load_model("model/holdme/IEEE39")

        comps = adapter.get_components("model/holdme/IEEE39")
        assert len(comps) == 3
        types = {c.component_type for c in comps}
        assert ComponentType.BRANCH in types
        assert ComponentType.LOAD in types
        assert ComponentType.GENERATOR in types

    def test_get_components_by_type(self, mock_sdk):
        from cloudpss_skills_v2.powerapi.adapters.cloudpss.powerflow import (
            CloudPSSPowerFlowAdapter,
        )

        adapter = CloudPSSPowerFlowAdapter()
        adapter.connect()
        adapter.load_model("model/holdme/IEEE39")

        branches = adapter.get_components_by_type(
            "model/holdme/IEEE39", ComponentType.BRANCH
        )
        assert len(branches) == 1
        assert branches[0].name == "Line 1"

    def test_remove_component(self, mock_sdk):
        MockModel, mock_model = mock_sdk
        from cloudpss_skills_v2.powerapi.adapters.cloudpss.powerflow import (
            CloudPSSPowerFlowAdapter,
        )

        adapter = CloudPSSPowerFlowAdapter()
        adapter.connect()
        adapter.load_model("model/holdme/IEEE39")

        ok = adapter.remove_component("model/holdme/IEEE39", "line_1")
        assert ok is True
        mock_model.removeComponent.assert_called_with("line_1")

    def test_update_component_args(self, mock_sdk):
        MockModel, mock_model = mock_sdk
        from cloudpss_skills_v2.powerapi.adapters.cloudpss.powerflow import (
            CloudPSSPowerFlowAdapter,
        )

        adapter = CloudPSSPowerFlowAdapter()
        adapter.connect()
        adapter.load_model("model/holdme/IEEE39")

        ok = adapter.update_component_args(
            "model/holdme/IEEE39", "load_1", {"pf_P": {"source": "150"}}
        )
        assert ok is True
        mock_model.updateComponent.assert_called()

    def test_clone_model(self, mock_sdk):
        MockModel, mock_model = mock_sdk
        from cloudpss_skills_v2.powerapi.adapters.cloudpss.powerflow import (
            CloudPSSPowerFlowAdapter,
        )

        adapter = CloudPSSPowerFlowAdapter()
        adapter.connect()
        adapter.load_model("model/holdme/IEEE39")

        clone_id = adapter.clone_model("model/holdme/IEEE39")
        assert clone_id != "model/holdme/IEEE39"
        assert "clone" in clone_id
        assert MockModel.fetch.call_count >= 2

    def test_model_handle_n1_pattern(self, mock_sdk):
        from cloudpss_skills_v2.powerapi.adapters.cloudpss.powerflow import (
            CloudPSSPowerFlowAdapter,
        )
        from cloudpss_skills_v2.powerskill.apis.powerflow import PowerFlowAPI

        adapter = CloudPSSPowerFlowAdapter()
        adapter.connect()

        api = PowerFlowAPI(adapter)
        handle = api.get_model_handle("model/holdme/IEEE39")

        branches = handle.get_components_by_type(ComponentType.BRANCH)
        assert len(branches) >= 1

        for branch in branches:
            working = handle.clone()
            ok = working.remove_component(branch.key)
            assert ok is True


# ---- Architectural compliance check ----


class TestArchitecturalCompliance:
    def test_model_handle_has_no_cloudpss_import(self):
        import inspect

        src = inspect.getsource(ModelHandle)
        assert "from cloudpss" not in src
        assert "import cloudpss" not in src

    def test_component_info_has_no_cloudpss_import(self):
        import inspect

        src = inspect.getsource(ComponentInfo)
        assert "cloudpss" not in src

    def test_simulation_api_has_no_cloudpss_import(self):
        import inspect
        from cloudpss_skills_v2.powerskill.base import SimulationAPI

        src = inspect.getsource(SimulationAPI)
        assert "from cloudpss" not in src
