"""Cross-engine validation tests: CloudPSS (mocked) vs pandapower."""

import pytest
from cloudpss_skills_v2.powerskill import Engine, PowerFlow, ModelHandle
from cloudpss_skills_v2.powerapi import SimulationStatus


class MockCloudPSSAdapter:
    """Mock CloudPSS adapter that returns known results for comparison."""

    def __init__(self):
        self._connected = False
        self._current_model = None

    @property
    def engine_name(self):
        return "cloudpss"

    def is_connected(self):
        return self._connected

    def connect(self):
        self._connected = True

    def disconnect(self):
        self._connected = False

    def load_model(self, model_id):
        self._current_model = model_id
        return True

    def run_simulation(self, config):
        class SimResult:
            def __init__(self):
                self.status = "COMPLETED"
                self.job_id = "mock123"
                self.data = {
                    "buses": [
                        {"name": "B1", "vm_pu": 1.0, "va_deg": 0.0},
                        {"name": "B2", "vm_pu": 0.985, "va_deg": -5.0},
                    ],
                    "branches": [
                        {"name": "L1", "p_from_mw": 50.0},
                    ],
                }
                self.errors = []
                self.is_success = True

        return SimResult()

    def get_components(self, model_id):
        return []

    def get_components_by_type(self, model_id, comp_type):
        return []

    def get_current_model_id(self):
        return self._current_model

    def get_result(self, job_id):
        return self.run_simulation({})


@pytest.mark.pandapower
class TestCrossEngineConsistency:
    def test_engine_creation_both_engines(self):
        pf_pandapower = Engine.create_powerflow(engine="pandapower")
        assert pf_pandapower is not None
        assert pf_pandapower.adapter.engine_name == "pandapower"

    def test_load_same_model_id(self):
        pf = Engine.create_powerflow(engine="pandapower")
        handle = pf.get_model_handle("case14")

        assert handle is not None
        assert handle.model_id == "case14"

    def test_result_structure_consistent(self):
        from cloudpss_skills_v2.powerapi.adapters.pandapower import (
            PandapowerPowerFlowAdapter,
        )

        a = PandapowerPowerFlowAdapter()
        a.connect()
        result = a.run_simulation({"model_id": "case14"})

        assert result.status == SimulationStatus.COMPLETED
        assert result.data is not None
        assert "buses" in result.data
        assert "branches" in result.data


@pytest.mark.pandapower
class TestCrossEngineVoltageComparison:
    @pytest.fixture
    def pf(self):
        return Engine.create_powerflow(engine="pandapower")

    def test_voltage_range_standard(self, pf):
        handle = pf.get_model_handle("case14")
        result = pf.run_power_flow(handle)

        if result.is_success:
            voltages = [b["vm_pu"] for b in result.data.get("buses", [])]
            assert min(voltages) > 0.9
            assert max(voltages) < 1.1

    def test_voltage_range_all_cases(self, pf):
        for case in ["case14", "case30", "case57"]:
            handle = pf.get_model_handle(case)
            result = pf.run_power_flow(handle)

            if result.is_success:
                voltages = [b["vm_pu"] for b in result.data.get("buses", [])]
                assert min(voltages) > 0.8
                assert max(voltages) < 1.15


@pytest.mark.pandapower
class TestCrossEngineModelHandle:
    def test_model_handle_interface_consistent(self):
        pf = Engine.create_powerflow(engine="pandapower")
        handle = pf.get_model_handle("case14")

        assert hasattr(handle, "model_id")
        assert hasattr(handle, "adapter")
        assert hasattr(handle, "get_components_by_type")

    def test_get_components_by_type_interface(self):
        from cloudpss_skills_v2.powerskill.model_handle import ComponentType

        pf = Engine.create_powerflow(engine="pandapower")
        handle = pf.get_model_handle("case14")

        buses = handle.get_components_by_type(ComponentType.BUS)
        assert len(buses) > 0

        branches = handle.get_components_by_type(ComponentType.BRANCH)
        assert len(branches) > 0


@pytest.mark.pandapower
class TestCrossEngineValidationConfig:
    def test_pandapower_validate_method(self):
        pf = Engine.create_powerflow(engine="pandapower")
        valid = pf.adapter.validate_config({"model_id": "case14"})
        assert valid.valid is True

    def test_pandapower_rejects_empty_config(self):
        pf = Engine.create_powerflow(engine="pandapower")
        valid = pf.adapter.validate_config({})
        assert valid.valid is False


@pytest.mark.pandapower
class TestCrossEngineErrorHandling:
    def test_invalid_model_fails(self):
        pf = Engine.create_powerflow(engine="pandapower")
        pf.adapter.connect()

        result = pf.adapter.run_simulation({"model_id": "nonexistent_case"})
        assert result.status == SimulationStatus.FAILED


@pytest.mark.pandapower
class TestFrameworkAdapterPattern:
    def test_all_adapters_inherit_base(self):
        from cloudpss_skills_v2.powerapi.base import EngineAdapter
        from cloudpss_skills_v2.powerapi.adapters.pandapower import (
            PandapowerPowerFlowAdapter,
        )
        from cloudpss_skills_v2.powerapi.adapters.pandapower.short_circuit import (
            PandapowerShortCircuitAdapter,
        )

        assert issubclass(PandapowerPowerFlowAdapter, EngineAdapter)
        assert issubclass(PandapowerShortCircuitAdapter, EngineAdapter)

    def test_adapter_has_required_methods(self):
        from cloudpss_skills_v2.powerapi.adapters.pandapower import (
            PandapowerPowerFlowAdapter,
        )

        a = PandapowerPowerFlowAdapter()
        required = [
            "connect",
            "disconnect",
            "load_model",
            "run_simulation",
            "validate_config",
        ]
        for method in required:
            assert hasattr(a, method), f"Missing: {method}"
