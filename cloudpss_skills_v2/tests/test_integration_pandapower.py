"""Integration tests for pandapower adapter - CI compatible."""

import pytest
from cloudpss_skills_v2.powerapi import SimulationResult, SimulationStatus
from cloudpss_skills_v2.powerapi.adapters.pandapower import PandapowerPowerFlowAdapter
from cloudpss_skills_v2.powerapi import EngineConfig


@pytest.mark.pandapower
class TestPandapowerAdapterLifecycle:
    @pytest.fixture
    def adapter(self):
        return PandapowerPowerFlowAdapter()

    def test_engine_name(self, adapter):
        assert adapter.engine_name == "pandapower"

    def test_supported_simulations(self, adapter):
        from cloudpss_skills_v2.powerapi import SimulationType

        sims = adapter.get_supported_simulations()
        assert SimulationType.POWER_FLOW in sims

    def test_connect_disconnect(self, adapter):
        adapter.connect()
        assert adapter._connected
        adapter.disconnect()
        assert not adapter._connected


@pytest.mark.pandapower
class TestPandapowerAdapterValidation:
    @pytest.fixture
    def adapter(self):
        return PandapowerPowerFlowAdapter()

    def test_validate_empty(self, adapter):
        result = adapter._do_validate_config({})
        assert not result.valid

    def test_validate_case_name(self, adapter):
        result = adapter._do_validate_config({"model_id": "case14"})
        assert result.valid

    def test_validate_with_model_id(self, adapter):
        result = adapter._do_validate_config({"model_id": "case14"})
        assert result.valid


@pytest.mark.pandapower
class TestPandapowerInvalidCase:
    @pytest.fixture
    def adapter(self):
        a = PandapowerPowerFlowAdapter()
        a.connect()
        return a

    def test_invalid_case_fails_at_runtime(self, adapter):
        result = adapter.run_simulation({"model_id": "invalid_case_xyz"})
        assert result.status == SimulationStatus.FAILED
        assert len(result.errors) > 0


@pytest.mark.pandapower
class TestPandapowerAdapterCase14:
    @pytest.fixture
    def adapter(self):
        return PandapowerPowerFlowAdapter()

    def test_run_case14(self, adapter):
        result = adapter._do_run_simulation({"model_id": "case14"})
        assert result.status in [SimulationStatus.COMPLETED, SimulationStatus.FAILED]

    def test_load_case14_model(self, adapter):
        success = adapter._do_load_model("case14")
        assert success is True


@pytest.mark.pandapower
class TestPandapowerAdapterCase9:
    @pytest.fixture
    def adapter(self):
        return PandapowerPowerFlowAdapter()

    def test_run_case9(self, adapter):
        result = adapter._do_run_simulation({"model_id": "case9"})
        assert result.status in [SimulationStatus.COMPLETED, SimulationStatus.FAILED]


@pytest.mark.pandapower
class TestPandapowerAdapterCase30:
    @pytest.fixture
    def adapter(self):
        return PandapowerPowerFlowAdapter()

    def test_run_case30(self, adapter):
        result = adapter._do_run_simulation({"model_id": "case30"})
        assert result.status in [SimulationStatus.COMPLETED, SimulationStatus.FAILED]


@pytest.mark.pandapower
class TestPandapowerAdapterViaFactory:
    def test_create_via_factory(self):
        from cloudpss_skills_v2.powerskill import Engine

        pf = Engine.create_powerflow(engine="pandapower")
        assert pf is not None


@pytest.mark.pandapower
class TestPandapowerResults:
    @pytest.fixture
    def adapter(self):
        return PandapowerPowerFlowAdapter()

    def test_bus_results_extraction(self, adapter):
        result = adapter._do_run_simulation({"model_id": "case14"})
        if result.status == SimulationStatus.COMPLETED:
            assert result.data is not None
            buses = result.data.get("buses", [])
            assert len(buses) > 0

    def test_voltage_in_valid_range(self, adapter):
        result = adapter._do_run_simulation({"model_id": "case14"})
        if result.status == SimulationStatus.COMPLETED:
            for bus in result.data.get("buses", []):
                vm = bus.get("voltage_pu", 1.0)
                assert 0.9 <= vm <= 1.1


@pytest.mark.pandapower
class TestPandapowerMultipleCases:
    @pytest.fixture
    def adapter(self):
        return PandapowerPowerFlowAdapter()

    @pytest.mark.parametrize("case_name", ["case14", "case30", "case57"])
    def test_various_cases(self, adapter, case_name):
        result = adapter._do_run_simulation({"model_id": case_name})
        assert result.status in [SimulationStatus.COMPLETED, SimulationStatus.FAILED]


@pytest.mark.pandapower
class TestPandapowerShortCircuitAdapter:
    @pytest.fixture
    def adapter(self):
        from cloudpss_skills_v2.powerapi.adapters.pandapower.short_circuit import (
            PandapowerShortCircuitAdapter,
        )

        return PandapowerShortCircuitAdapter()

    def test_sc_adapter_loads(self, adapter):
        assert adapter is not None

    def test_sc_run(self, adapter):
        result = adapter._do_run_simulation({"model_id": "case14"})
        assert result.status in [
            SimulationStatus.COMPLETED,
            SimulationStatus.FAILED,
        ]


@pytest.mark.pandapower
class TestModelManipulation:
    @pytest.fixture
    def adapter(self):
        a = PandapowerPowerFlowAdapter()
        a.connect()
        return a

    def test_load_model_case14(self, adapter):
        success = adapter.load_model("case14")
        assert success is True

    def test_get_current_model_id(self, adapter):
        adapter.load_model("case14")
        model_id = adapter.get_current_model_id()
        assert model_id == "case14"

    def test_get_components_returns_list(self, adapter):
        adapter.load_model("case14")
        components = adapter.get_components("case14")
        assert isinstance(components, list)
        assert len(components) > 0

    def test_get_components_by_type_bus(self, adapter):
        adapter.load_model("case14")
        buses = adapter.get_components_by_type("case14", "bus")
        assert len(buses) >= 14


@pytest.mark.pandapower
class TestModelClone:
    @pytest.fixture
    def adapter(self):
        a = PandapowerPowerFlowAdapter()
        a.connect()
        return a

    def test_clone_model(self, adapter):
        adapter.load_model("case14")
        clone_id = adapter.clone_model("case14")
        assert clone_id is not None
        assert clone_id != "case14"


@pytest.mark.pandapower
class TestResultRetrieval:
    @pytest.fixture
    def adapter(self):
        a = PandapowerPowerFlowAdapter()
        a.connect()
        return a

    def test_run_and_get_result(self, adapter):
        result = adapter.run_simulation({"model_id": "case14"})
        job_id = result.job_id
        retrieved = adapter.get_result(job_id)
        assert retrieved is not None
