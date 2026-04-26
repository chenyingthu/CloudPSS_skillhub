"""Integration tests for pandapower short circuit adapter."""

import pytest
from cloudpss_skills_v2.powerapi import SimulationStatus
from cloudpss_skills_v2.powerapi.adapters.pandapower.short_circuit import (
    PandapowerShortCircuitAdapter,
)


@pytest.mark.pandapower
class TestShortCircuitAdapterLifecycle:
    @pytest.fixture
    def adapter(self):
        a = PandapowerShortCircuitAdapter()
        a.connect()
        return a

    def test_engine_name(self, adapter):
        assert adapter.engine_name == "pandapower_sc"

    def test_connect_succeeds(self, adapter):
        assert adapter.is_connected() is True


@pytest.mark.pandapower
class TestShortCircuitRun:
    @pytest.fixture
    def adapter(self):
        a = PandapowerShortCircuitAdapter()
        a.connect()
        return a

    def test_run_case9(self, adapter):
        result = adapter.run_simulation({"model_id": "case9"})
        assert result.status == SimulationStatus.COMPLETED

    def test_run_case14(self, adapter):
        result = adapter.run_simulation({"model_id": "case14"})
        assert result.status == SimulationStatus.COMPLETED

    def test_run_case30(self, adapter):
        result = adapter.run_simulation({"model_id": "case30"})
        assert result.status == SimulationStatus.COMPLETED


@pytest.mark.pandapower
class TestShortCircuitResults:
    @pytest.fixture
    def adapter(self):
        a = PandapowerShortCircuitAdapter()
        a.connect()
        return a

    def test_bus_results_exist(self, adapter):
        result = adapter.run_simulation({"model_id": "case14"})
        if result.status == SimulationStatus.COMPLETED:
            assert result.data is not None
            assert "bus_results" in result.data

    def test_line_results_exist(self, adapter):
        result = adapter.run_simulation({"model_id": "case14"})
        if result.status == SimulationStatus.COMPLETED:
            assert "line_results" in result.data

    def test_fault_results_positive(self, adapter):
        result = adapter.run_simulation({"model_id": "case14"})
        if result.status == SimulationStatus.COMPLETED:
            for fc in result.data.get("bus_results", []):
                ikss = fc.get("ikss_ka", 0)
                if ikss:
                    assert ikss > 0


@pytest.mark.pandapower
class TestShortCircuitMultipleCases:
    @pytest.fixture
    def adapter(self):
        a = PandapowerShortCircuitAdapter()
        a.connect()
        return a

    @pytest.mark.parametrize("case", ["case9", "case14", "case30", "case57"])
    def test_various_cases(self, adapter, case):
        result = adapter.run_simulation({"model_id": case})
        assert result.status == SimulationStatus.COMPLETED


@pytest.mark.pandapower
class TestShortCircuitValidation:
    @pytest.fixture
    def adapter(self):
        return PandapowerShortCircuitAdapter()

    def test_validate_empty(self, adapter):
        result = adapter.validate_config({})
        assert result.valid is False

    def test_validate_with_case(self, adapter):
        result = adapter.validate_config({"model_id": "case14"})
        assert result.valid is True


@pytest.mark.pandapower
class TestShortCircuitComponents:
    @pytest.fixture
    def adapter(self):
        a = PandapowerShortCircuitAdapter()
        a.connect()
        return a

    def test_load_model(self, adapter):
        success = adapter.load_model("case14")
        assert success is True
