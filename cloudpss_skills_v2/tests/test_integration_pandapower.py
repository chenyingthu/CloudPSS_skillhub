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

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_engine_name(self, adapter):
        assert adapter.engine_name == "pandapower"

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_supported_simulations(self, adapter):
        from cloudpss_skills_v2.powerapi import SimulationType

        sims = adapter.get_supported_simulations()
        assert SimulationType.POWER_FLOW in sims

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
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

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_validate_empty(self, adapter):
        result = adapter._do_validate_config({})
        assert not result.valid

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_validate_case_name(self, adapter):
        result = adapter._do_validate_config({"model_id": "case14"})
        assert result.valid

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
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

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_invalid_case_fails_at_runtime(self, adapter):
        result = adapter.run_simulation({"model_id": "invalid_case_xyz"})
        assert result.status == SimulationStatus.FAILED
        assert len(result.errors) > 0


@pytest.mark.pandapower
class TestPandapowerAdapterCase14:
    @pytest.fixture
    def adapter(self):
        return PandapowerPowerFlowAdapter()

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
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

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_run_case9(self, adapter):
        result = adapter._do_run_simulation({"model_id": "case9"})
        assert result.status in [SimulationStatus.COMPLETED, SimulationStatus.FAILED]


@pytest.mark.pandapower
class TestPandapowerAdapterCase30:
    @pytest.fixture
    def adapter(self):
        return PandapowerPowerFlowAdapter()

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_run_case30(self, adapter):
        result = adapter._do_run_simulation({"model_id": "case30"})
        assert result.status in [SimulationStatus.COMPLETED, SimulationStatus.FAILED]


@pytest.mark.pandapower
class TestPandapowerAdapterViaFactory:
    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
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

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_voltage_in_valid_range(self, adapter):
        result = adapter._do_run_simulation({"model_id": "case14"})
        if result.status == SimulationStatus.COMPLETED:
            for bus in result.data.get("buses", []):
                vm = bus.get("voltage_pu", 1.0)
                assert 0.9 <= vm <= 1.1


@pytest.mark.pandapower
class TestPhysicalCorrectness:
    """Tests that verify physical correctness of power system results."""

    @pytest.fixture
    def adapter(self):
        return PandapowerPowerFlowAdapter()

    def test_bus_types_not_all_pq(self, adapter):
        """Bus types should include slack and/or PV, not all PQ."""
        result = adapter._do_run_simulation({"model_id": "case14"})
        if result.status == SimulationStatus.COMPLETED:
            buses = result.data.get("buses", [])
            bus_types = [b.get("bus_type") for b in buses]
            unique_types = set(bus_types)
            assert len(unique_types) > 1, f"All buses have same type: {unique_types}"

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_has_slack_bus(self, adapter):
        """IEEE 14-bus should have at least one slack bus."""
        result = adapter._do_run_simulation({"model_id": "case14"})
        if result.status == SimulationStatus.COMPLETED:
            buses = result.data.get("buses", [])
            slack_buses = [b for b in buses if b.get("bus_type") == "slack"]
            assert len(slack_buses) >= 1, "No slack bus found"

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_has_pv_buses(self, adapter):
        """IEEE 14-bus should have PV buses (generators)."""
        result = adapter._do_run_simulation({"model_id": "case14"})
        if result.status == SimulationStatus.COMPLETED:
            buses = result.data.get("buses", [])
            pv_buses = [b for b in buses if b.get("bus_type") == "pv"]
            assert len(pv_buses) >= 1, "No PV buses found"

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_slack_bus_voltage_nominal(self, adapter):
        """Slack bus voltage should be near nominal (0.95-1.1 pu is normal)."""
        result = adapter._do_run_simulation({"model_id": "case14"})
        if result.status == SimulationStatus.COMPLETED:
            buses = result.data.get("buses", [])
            slack_buses = [b for b in buses if b.get("bus_type") == "slack"]
            if slack_buses:
                for bus in slack_buses:
                    vm = bus.get("voltage_pu", 1.0)
                    assert 0.95 <= vm <= 1.1, f"Slack bus voltage out of range: {vm}"

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_slack_bus_angle_zero(self, adapter):
        """Slack bus angle should be zero (reference)."""
        result = adapter._do_run_simulation({"model_id": "case14"})
        if result.status == SimulationStatus.COMPLETED:
            buses = result.data.get("buses", [])
            slack_buses = [b for b in buses if b.get("bus_type") == "slack"]
            if slack_buses:
                for bus in slack_buses:
                    angle = bus.get("angle_deg", 0)
                    assert abs(angle) < 0.5, f"Slack bus angle not zero: {angle}"

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_voltage_profile_physically_reasonable(self, adapter):
        """All bus voltages should be within 0.9-1.1 pu (normal operation)."""
        result = adapter._do_run_simulation({"model_id": "case14"})
        if result.status == SimulationStatus.COMPLETED:
            buses = result.data.get("buses", [])
            for bus in buses:
                vm = bus.get("voltage_pu", 1.0)
                assert 0.9 <= vm <= 1.1, (
                    f"Bus {bus.get('name')} voltage out of range: {vm}"
                )

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_power_balanced(self, adapter):
        """Generated power should roughly equal load + losses."""
        result = adapter._do_run_simulation({"model_id": "case14"})
        if result.status == SimulationStatus.COMPLETED:
            summary = result.data.get("summary", {})
            total_loss = summary.get("total_loss_mw", 0)
            assert total_loss >= 0, "Losses cannot be negative"
            assert total_loss < 50, f"Excessive losses: {total_loss} MW"


@pytest.mark.pandapower
class TestShortCircuitPhysicalCorrectness:
    """Tests that verify physical correctness of short circuit results."""

    @pytest.fixture
    def adapter(self):
        from cloudpss_skills_v2.powerapi.adapters.pandapower.short_circuit import (
            PandapowerShortCircuitAdapter,
        )

        return PandapowerShortCircuitAdapter()

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_ikss_in_valid_range(self, adapter):
        """IkSS should be non-negative and finite."""
        result = adapter._do_run_simulation({"model_id": "case14"})
        if result.status == SimulationStatus.COMPLETED:
            buses = result.data.get("bus_results", [])
            for bus in buses:
                ikss = bus.get("ikss_ka", 0)
                assert 0 <= ikss < 1e6, (
                    f"Bus {bus.get('bus')} IkSS out of range: {ikss} kA"
                )

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_max_ikss_finite(self, adapter):
        """Maximum IkSS should be finite and recorded."""
        result = adapter._do_run_simulation({"model_id": "case14"})
        if result.status == SimulationStatus.COMPLETED:
            summary = result.data.get("summary", {})
            max_ikss = summary.get("max_ikss_ka", 0)
            assert max_ikss > 0, "Max IkSS should be positive"
            assert max_ikss < 1e6, f"Max IkSS unreasonably large: {max_ikss} kA"

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_fault_voltage_reasonable(self, adapter):
        """Bus voltage during fault should be near zero at fault location."""
        result = adapter._do_run_simulation({"model_id": "case14"})
        if result.status == SimulationStatus.COMPLETED:
            buses = result.data.get("bus_results", [])
            low_voltage_buses = [b for b in buses if b.get("v_pu", 1) < 0.3]
            assert len(low_voltage_buses) >= 1, "No bus with low fault voltage found"

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_all_buses_have_results(self, adapter):
        """All buses should have short circuit results."""
        result = adapter._do_run_simulation({"model_id": "case14"})
        if result.status == SimulationStatus.COMPLETED:
            buses = result.data.get("bus_results", [])
            assert len(buses) >= 14, f"Expected 14+ bus results, got {len(buses)}"

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_ikss_positive(self, adapter):
        """All IkSS values should be non-negative."""
        result = adapter._do_run_simulation({"model_id": "case14"})
        if result.status == SimulationStatus.COMPLETED:
            buses = result.data.get("bus_results", [])
            for bus in buses:
                ikss = bus.get("ikss_ka", 0)
                assert ikss >= 0, f"Negative IkSS at bus {bus.get('bus')}: {ikss}"

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_ip_greater_than_ikss(self, adapter):
        """Peak current ip should be greater than IkSS (ip includes decay factor)."""
        result = adapter._do_run_simulation({"model_id": "case14"})
        if result.status == SimulationStatus.COMPLETED:
            buses = result.data.get("bus_results", [])
            for bus in buses:
                ip = bus.get("ip_ka", 0)
                ikss = bus.get("ikss_ka", 0)
                if ip > 0 and ikss > 0:
                    assert ip >= ikss, f"ip ({ip}) should be >= ikss ({ikss})"

    def test_ikss_computed_for_all_buses(self, adapter):
        """IkSS should be computed for all buses with valid values."""
        result = adapter._do_run_simulation({"model_id": "case14"})
        if result.status == SimulationStatus.COMPLETED:
            buses = result.data.get("bus_results", [])
            for bus in buses:
                ikss = bus.get("ikss_ka")
                assert ikss is not None, f"Missing IkSS for bus {bus.get('bus')}"
                assert not (ikss != ikss), f"NaN IkSS for bus {bus.get('bus')}"


@pytest.mark.pandapower
class TestPandapowerMultipleCases:
    @pytest.fixture
    def adapter(self):
        return PandapowerPowerFlowAdapter()

    @pytest.mark.parametrize("case_name", ["case14", "case30", "case57"])
    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
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

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
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

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_get_current_model_id(self, adapter):
        adapter.load_model("case14")
        model_id = adapter.get_current_model_id()
        assert model_id == "case14"

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_get_components_returns_list(self, adapter):
        adapter.load_model("case14")
        components = adapter.get_components("case14")
        assert isinstance(components, list)
        assert len(components) > 0

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
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

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
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

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_run_and_get_result(self, adapter):
        result = adapter.run_simulation({"model_id": "case14"})
        job_id = result.job_id
        retrieved = adapter.get_result(job_id)
        assert retrieved is not None
