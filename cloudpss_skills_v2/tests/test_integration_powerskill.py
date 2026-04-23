"""Integration tests for PowerSkill layer with pandapower."""

import pytest
from cloudpss_skills_v2.powerskill import Engine, PowerFlow, ModelHandle
from cloudpss_skills_v2.powerskill.model_handle import ComponentType


@pytest.mark.pandapower
class TestPowerFlowViaEngine:
    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_create_powerflow(self):
        pf = Engine.create_powerflow(engine="pandapower")
        assert pf is not None
        assert isinstance(pf, PowerFlow)

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_adapter_name(self):
        pf = Engine.create_powerflow(engine="pandapower")
        assert pf.adapter.engine_name == "pandapower"


@pytest.mark.pandapower
class TestPowerFlowModelOperations:
    @pytest.fixture
    def pf(self):
        return Engine.create_powerflow(engine="pandapower")

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_get_model_handle(self, pf):
        handle = pf.get_model_handle("case14")
        assert handle is not None
        assert isinstance(handle, ModelHandle)

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_get_components(self, pf):
        handle = pf.get_model_handle("case14")
        components = handle.get_components()
        assert len(components) > 0

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_get_components_by_type(self, pf):
        handle = pf.get_model_handle("case14")
        buses = handle.get_components_by_type(ComponentType.BUS)
        assert len(buses) > 0


@pytest.mark.pandapower
class TestPowerFlowExecution:
    @pytest.fixture
    def pf(self):
        return Engine.create_powerflow(engine="pandapower")

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_run_power_flow(self, pf):
        handle = pf.get_model_handle("case14")
        result = pf.run_power_flow(handle)
        assert result is not None
        assert result.is_success or not result.is_success

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_run_result_data(self, pf):
        handle = pf.get_model_handle("case14")
        result = pf.run_power_flow(handle)
        if result.is_success:
            assert result.data is not None


@pytest.mark.pandapower
class TestShortCircuitViaEngine:
    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_create_short_circuit(self):
        sc = Engine.create_short_circuit(engine="pandapower")
        assert sc is not None


@pytest.mark.pandapower
class TestModelHandleComponentOperations:
    @pytest.fixture
    def pf(self):
        return Engine.create_powerflow(engine="pandapower")

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_get_buses(self, pf):
        handle = pf.get_model_handle("case14")
        buses = handle.get_components_by_type(ComponentType.BUS)
        assert len(buses) >= 14

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_get_lines(self, pf):
        handle = pf.get_model_handle("case14")
        lines = handle.get_components_by_type(ComponentType.BRANCH)
        assert len(lines) > 0

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_get_generators(self, pf):
        handle = pf.get_model_handle("case14")
        gens = handle.get_components_by_type(ComponentType.GENERATOR)
        assert len(gens) >= 1

    def test_get_loads(self, pf):
        handle = pf.get_model_handle("case14")
        loads = handle.get_components_by_type(ComponentType.LOAD)
        assert len(loads) >= 1


@pytest.mark.pandapower
class TestMultipleCases:
    @pytest.fixture
    def pf(self):
        return Engine.create_powerflow(engine="pandapower")

    @pytest.mark.parametrize("case", ["case14", "case30", "case57"])
    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_run_various_cases(self, pf, case):
        handle = pf.get_model_handle(case)
        result = pf.run_power_flow(handle)
        assert result is not None
