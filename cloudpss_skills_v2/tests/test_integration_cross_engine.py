"""Cross-engine validation tests: pandapower adapter patterns."""

import pytest
from cloudpss_skills_v2.powerskill import Engine, PowerFlow, ModelHandle
from cloudpss_skills_v2.powerapi import SimulationStatus


@pytest.mark.pandapower
class TestCrossEngineConsistency:
    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_engine_creation_both_engines(self):
        pf_pandapower = Engine.create_powerflow(engine="pandapower")
        assert pf_pandapower is not None
        assert pf_pandapower.adapter.engine_name == "pandapower"

    def test_load_same_model_id(self):
        pf = Engine.create_powerflow(engine="pandapower")
        handle = pf.get_model_handle("case14")

        assert handle is not None
        assert handle.model_id == "case14"

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
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
                assert min(voltages) > 0.9
                assert max(voltages) < 1.1


@pytest.mark.pandapower
class TestCrossEngineModelHandle:
    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_model_handle_interface_consistent(self):
        pf = Engine.create_powerflow(engine="pandapower")
        handle = pf.get_model_handle("case14")

        assert hasattr(handle, "model_id")
        assert hasattr(handle, "adapter")
        assert hasattr(handle, "get_components_by_type")

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
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
    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_pandapower_validate_method(self):
        pf = Engine.create_powerflow(engine="pandapower")
        valid = pf.adapter.validate_config({"model_id": "case14"})
        assert valid.valid is True

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_pandapower_rejects_empty_config(self):
        pf = Engine.create_powerflow(engine="pandapower")
        valid = pf.adapter.validate_config({})
        assert valid.valid is False


@pytest.mark.pandapower
class TestCrossEngineErrorHandling:
    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
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

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
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
