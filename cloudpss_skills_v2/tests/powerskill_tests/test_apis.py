"""Tests for PowerSkill API layer - SimulationAPI, PowerFlowAPI, EMTAPI, ShortCircuitAPI, APIFactory."""

import pytest
from unittest.mock import MagicMock, patch

from cloudpss_skills_v2.powerapi import (
    EngineAdapter,
    EngineConfig,
    SimulationResult,
    SimulationStatus,
    ValidationResult,
)
from cloudpss_skills_v2.powerskill.base import SimulationAPI
from cloudpss_skills_v2.powerskill.apis.powerflow import PowerFlowAPI
from cloudpss_skills_v2.powerskill.apis.emt import EMTAPI
from cloudpss_skills_v2.powerskill.apis.short_circuit import ShortCircuitAPI
from cloudpss_skills_v2.powerskill.apis.factory import APIFactory


class MockAdapter(EngineAdapter):
    """Mock adapter that records calls and returns configurable results."""

    def __init__(self, config=None):
        super().__init__(config or EngineConfig(engine_name="mock"))
        self._calls = []

    @property
    def engine_name(self) -> str:
        return "mock"

    def _do_connect(self) -> None:
        self._calls.append("connect")

    def _do_disconnect(self) -> None:
        self._calls.append("disconnect")

    def _do_load_model(self, model_id: str) -> bool:
        self._calls.append(("load_model", model_id))
        return True

    def _do_run_simulation(self, config: dict) -> SimulationResult:
        self._calls.append(("run_simulation", config))
        return SimulationResult(
            job_id="test-job-123",
            status=SimulationStatus.COMPLETED,
            data={
                "buses": [{"name": "Bus1", "voltage_pu": 1.02, "generation_mw": 100.0}],
                "branches": [
                    {"name": "Line1", "p_from_mw": 50.0, "power_loss_mw": 0.5}
                ],
                "summary": {
                    "total_generation": {"p_mw": 100, "q_mvar": 20},
                    "total_load": {"p_mw": 98, "q_mvar": 19},
                    "total_loss_mw": 0.5,
                    "voltage_range": {"min_pu": 0.98, "max_pu": 1.05},
                },
            },
        )

    def _do_get_result(self, job_id: str) -> SimulationResult:
        self._calls.append(("get_result", job_id))
        return SimulationResult(
            job_id=job_id,
            status=SimulationStatus.COMPLETED,
            data={
                "buses": [{"name": "Bus1", "voltage_pu": 1.02}],
                "branches": [{"name": "Line1", "power_loss_mw": 0.5}],
                "fault_currents": [{"channel": "I_fault", "current_ka": 15.3}],
                "bus_voltages": [{"channel": "V_bus1", "voltage_pu": 0.85}],
                "summary": {"fault_type": "three_phase"},
            },
        )

    def _do_validate_config(self, config: dict) -> ValidationResult:
        self._calls.append(("validate_config", config))
        return ValidationResult(valid=True)


class TestSimulationAPI:
    def test_init_requires_adapter(self):
        with pytest.raises(TypeError):
            SimulationAPI(adapter="not_an_adapter")

    def test_init_with_adapter(self):
        adapter = MockAdapter()
        api = SimulationAPI(adapter=adapter)
        assert api.adapter is adapter

    def test_context_manager(self):
        adapter = MockAdapter()
        with SimulationAPI(adapter=adapter) as api:
            assert adapter.is_connected()
        assert not adapter.is_connected()
        assert "connect" in adapter._calls
        assert "disconnect" in adapter._calls

    def test_delegates_to_adapter(self):
        adapter = MockAdapter()
        api = SimulationAPI(adapter=adapter)
        api.connect()
        result = api.run(config={"model_id": "test"})
        assert result.status == SimulationStatus.COMPLETED
        assert result.job_id == "test-job-123"
        api.disconnect()

    def test_adapter_property(self):
        adapter = MockAdapter()
        api = SimulationAPI(adapter=adapter)
        assert api.adapter.engine_name == "mock"


class TestPowerFlowAPI:
    def test_run_power_flow(self):
        adapter = MockAdapter()
        api = PowerFlowAPI(adapter=adapter)
        api.connect()
        result = api.run_power_flow(model_id="IEEE39")
        assert result.status == SimulationStatus.COMPLETED
        assert "run_simulation" in [
            c[0] for c in adapter._calls if isinstance(c, tuple)
        ]
        api.disconnect()

    def test_run_power_flow_passes_config(self):
        adapter = MockAdapter()
        api = PowerFlowAPI(adapter=adapter)
        api.connect()
        result = api.run_power_flow(
            model_id="IEEE39",
            algorithm="fast_decoupled",
            tolerance=1e-8,
            max_iterations=200,
        )
        run_call = [
            c
            for c in adapter._calls
            if isinstance(c, tuple) and c[0] == "run_simulation"
        ]
        assert len(run_call) == 1
        config = run_call[0][1]
        assert config["model_id"] == "IEEE39"
        assert config["algorithm"] == "fast_decoupled"
        assert config["tolerance"] == 1e-8
        assert config["max_iterations"] == 200

    def test_get_bus_results(self):
        adapter = MockAdapter()
        api = PowerFlowAPI(adapter=adapter)
        api.connect()
        buses = api.get_bus_results("test-job")
        assert len(buses) == 1

    def test_get_branch_results(self):
        adapter = MockAdapter()
        api = PowerFlowAPI(adapter=adapter)
        api.connect()
        branches = api.get_branch_results("test-job")
        assert len(branches) == 1

    def test_get_summary(self):
        adapter = MockAdapter()
        api = PowerFlowAPI(adapter=adapter)
        api.connect()
        summary = api.get_summary("test-job")
        assert summary is not None

    def test_get_bus_results_empty(self):
        adapter = MockAdapter()
        api = PowerFlowAPI(adapter=adapter)
        api.connect()
        adapter._do_get_result = lambda job_id: SimulationResult(
            job_id=job_id, status=SimulationStatus.COMPLETED, data={}
        )
        buses = api.get_bus_results("empty-job")
        assert buses == []


class TestEMTAPI:
    def test_run_emt(self):
        adapter = MockAdapter()
        api = EMTAPI(adapter=adapter)
        api.connect()
        result = api.run_emt(model_id="IEEE3", duration=1.0)
        assert result.status == SimulationStatus.COMPLETED

    def test_run_emt_with_fault(self):
        adapter = MockAdapter()
        api = EMTAPI(adapter=adapter)
        api.connect()
        fault = {"start_time": 0.5, "end_time": 0.6}
        result = api.run_emt(model_id="IEEE3", fault_config=fault)
        run_call = [
            c
            for c in adapter._calls
            if isinstance(c, tuple) and c[0] == "run_simulation"
        ]
        assert len(run_call) == 1
        assert run_call[0][1]["fault"] == fault

    def test_get_waveforms_empty(self):
        adapter = MockAdapter()
        api = EMTAPI(adapter=adapter)
        api.connect()
        waveforms = api.get_waveforms("no-plots-job")
        assert waveforms == []


class TestShortCircuitAPI:
    def test_run_short_circuit(self):
        adapter = MockAdapter()
        api = ShortCircuitAPI(adapter=adapter)
        api.connect()
        result = api.run_short_circuit(model_id="IEEE39", fault_type="three_phase")
        assert result.status == SimulationStatus.COMPLETED

    def test_fault_currents(self):
        adapter = MockAdapter()
        api = ShortCircuitAPI(adapter=adapter)
        api.connect()
        currents = api.get_fault_currents("test-job")
        assert len(currents) >= 1


class TestAPIFactory:
    def test_create_powerflow_api(self):
        api = APIFactory.create_powerflow_api(engine="cloudpss")
        assert isinstance(api, PowerFlowAPI)
        assert isinstance(api.adapter, EngineAdapter)

    def test_create_emt_api(self):
        api = APIFactory.create_emt_api(engine="cloudpss")
        assert isinstance(api, EMTAPI)
        assert api.adapter.engine_name == "cloudpss_emt"

    def test_create_short_circuit_api(self):
        api = APIFactory.create_short_circuit_api(engine="cloudpss")
        assert isinstance(api, ShortCircuitAPI)
        assert api.adapter.engine_name == "cloudpss_sc"

    def test_create_api_generic(self):
        api = APIFactory.create_api("powerflow", engine="cloudpss")
        assert isinstance(api, PowerFlowAPI)

    def test_create_api_unknown_type_raises(self):
        with pytest.raises(ValueError, match="Unknown API type"):
            APIFactory.create_api("nonexistent")

    def test_each_api_gets_correct_adapter(self):
        pf = APIFactory.create_powerflow_api(engine="cloudpss")
        assert pf.adapter.engine_name == "cloudpss"

        emt = APIFactory.create_emt_api(engine="cloudpss")
        assert emt.adapter.engine_name == "cloudpss_emt"

        sc = APIFactory.create_short_circuit_api(engine="cloudpss")
        assert sc.adapter.engine_name == "cloudpss_sc"
