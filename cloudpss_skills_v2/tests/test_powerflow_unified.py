"""Tests for PowerFlow skill unified model integration.

This module tests that the PowerFlow skill properly returns unified model
in results, enabling engine-agnostic result access.
"""

from unittest.mock import MagicMock, patch
import pytest

from cloudpss_skills_v2.powerapi import SimulationResult, SimulationStatus, EngineAdapter
from cloudpss_skills_v2.core.system_model import PowerSystemModel, Bus, Branch


class MockEngineAdapter(EngineAdapter):
    """Mock EngineAdapter for testing."""

    @property
    def engine_name(self) -> str:
        return "mock_engine"

    def _do_connect(self) -> None:
        pass

    def _do_disconnect(self) -> None:
        pass

    def _do_load_model(self, model_id: str) -> bool:
        return True

    def _do_run_simulation(self, config: dict) -> SimulationResult:
        return SimulationResult(job_id="mock-job", status=SimulationStatus.COMPLETED)

    def _do_get_result(self, job_id: str) -> SimulationResult:
        return SimulationResult(job_id=job_id, status=SimulationStatus.COMPLETED)

    def _do_validate_config(self, config: dict):
        from cloudpss_skills_v2.powerapi import ValidationResult
        return ValidationResult(valid=True)


class TestPowerFlowUnifiedModel:
    """Test PowerFlow skill unified model integration."""

    def test_powerflow_returns_unified_model_in_result(self):
        """Test that PowerFlow skill result includes unified model."""
        from cloudpss_skills_v2.powerskill.powerflow import PowerFlow

        # Create mock adapter that passes isinstance check
        mock_adapter = MockEngineAdapter()
        mock_adapter.connect()  # Connect the adapter

        # Create a mock result with unified model
        unified_model = PowerSystemModel(
            buses=[
                Bus(bus_id=0, name="Bus 0", base_kv=110.0, bus_type="SLACK"),
                Bus(bus_id=1, name="Bus 1", base_kv=110.0, bus_type="PQ"),
            ],
            branches=[
                Branch(from_bus=0, to_bus=1, name="Line 0-1"),
            ],
            base_mva=100.0,
        )

        mock_result = SimulationResult(
            job_id="test-job-123",
            status=SimulationStatus.COMPLETED,
            system_model=unified_model,
            data={
                "buses": [{"id": 0, "name": "Bus 0"}],
                "branches": [{"from": 0, "to": 1}],
            },
        )
        mock_adapter._do_run_simulation = lambda config: mock_result

        # Create PowerFlow skill with mock adapter
        skill = PowerFlow(mock_adapter)

        # Run power flow
        result = skill.run_power_flow(
            model_id="test-model",
            algorithm="newton_raphson",
        )

        # Verify result includes unified model
        assert result.system_model is not None
        assert isinstance(result.system_model, PowerSystemModel)
        assert len(result.system_model.buses) == 2
        assert len(result.system_model.branches) == 1
        assert result.system_model.base_mva == 100.0

    def test_powerflow_get_system_model_method(self):
        """Test get_system_model method retrieves unified model."""
        from cloudpss_skills_v2.powerskill.powerflow import PowerFlow

        # Create mock adapter
        mock_adapter = MockEngineAdapter()
        mock_adapter.connect()  # Connect the adapter

        # Create a mock result with unified model
        unified_model = PowerSystemModel(
            buses=[
                Bus(bus_id=0, name="Bus 0", base_kv=110.0, bus_type="SLACK"),
            ],
            base_mva=100.0,
        )

        mock_result = SimulationResult(
            job_id="test-job-456",
            status=SimulationStatus.COMPLETED,
            system_model=unified_model,
        )
        mock_adapter._do_get_result = lambda job_id: mock_result

        # Create PowerFlow skill with mock adapter
        skill = PowerFlow(mock_adapter)

        # Get system model
        model = skill.get_system_model("test-job-456")

        # Verify model is returned correctly
        assert model is not None
        assert isinstance(model, PowerSystemModel)
        assert len(model.buses) == 1
        assert model.buses[0].name == "Bus 0"

    def test_powerflow_get_system_model_none_when_not_available(self):
        """Test get_system_model returns None when model not available."""
        from cloudpss_skills_v2.powerskill.powerflow import PowerFlow

        # Create mock adapter
        mock_adapter = MockEngineAdapter()
        mock_adapter.connect()  # Connect the adapter

        # Create a mock result WITHOUT unified model
        mock_result = SimulationResult(
            job_id="test-job-789",
            status=SimulationStatus.COMPLETED,
            system_model=None,
        )
        mock_adapter._do_get_result = lambda job_id: mock_result

        # Create PowerFlow skill with mock adapter
        skill = PowerFlow(mock_adapter)

        # Get system model
        model = skill.get_system_model("test-job-789")

        # Verify None is returned when no unified model
        assert model is None

    def test_powerflow_unified_model_has_correct_bus_data(self):
        """Test that unified model contains correct bus data."""
        from cloudpss_skills_v2.powerskill.powerflow import PowerFlow

        # Create mock adapter
        mock_adapter = MockEngineAdapter()
        mock_adapter.connect()  # Connect the adapter

        # Create buses with power flow results
        buses = [
            Bus(
                bus_id=0,
                name="Slack Bus",
                base_kv=110.0,
                bus_type="SLACK",
                v_magnitude_pu=1.0,
                v_angle_degree=0.0,
                p_injected_mw=100.0,
                q_injected_mvar=50.0,
            ),
            Bus(
                bus_id=1,
                name="Load Bus",
                base_kv=110.0,
                bus_type="PQ",
                v_magnitude_pu=0.95,
                v_angle_degree=-5.0,
                p_injected_mw=-80.0,
                q_injected_mvar=-30.0,
            ),
        ]

        unified_model = PowerSystemModel(
            buses=buses,
            branches=[],
            base_mva=100.0,
        )

        mock_result = SimulationResult(
            job_id="test-job-bus",
            status=SimulationStatus.COMPLETED,
            system_model=unified_model,
        )
        mock_adapter._do_run_simulation = lambda config: mock_result

        # Create PowerFlow skill with mock adapter
        skill = PowerFlow(mock_adapter)

        # Run power flow
        result = skill.run_power_flow(model_id="test-model")

        # Verify bus data is correct
        model = result.system_model
        assert model is not None
        assert len(model.buses) == 2

        slack_bus = model.get_bus_by_id(0)
        assert slack_bus is not None
        assert slack_bus.is_slack()
        assert slack_bus.v_magnitude_pu == 1.0
        assert slack_bus.v_angle_degree == 0.0

        load_bus = model.get_bus_by_id(1)
        assert load_bus is not None
        assert load_bus.v_magnitude_pu == 0.95
        assert load_bus.v_angle_degree == -5.0

    def test_powerflow_unified_model_has_correct_branch_data(self):
        """Test that unified model contains correct branch data."""
        from cloudpss_skills_v2.powerskill.powerflow import PowerFlow

        # Create mock adapter
        mock_adapter = MockEngineAdapter()
        mock_adapter.connect()  # Connect the adapter

        # Create branches with power flow results
        branches = [
            Branch(
                from_bus=0,
                to_bus=1,
                name="Line 0-1",
                branch_type="LINE",
                r_pu=0.01,
                x_pu=0.1,
                p_from_mw=80.0,
                q_from_mvar=30.0,
                p_to_mw=-78.0,
                q_to_mvar=-28.0,
                loading_percent=85.0,
            ),
        ]

        unified_model = PowerSystemModel(
            buses=[
                Bus(bus_id=0, name="Bus 0", base_kv=110.0, bus_type="SLACK"),
                Bus(bus_id=1, name="Bus 1", base_kv=110.0, bus_type="PQ"),
            ],
            branches=branches,
            base_mva=100.0,
        )

        mock_result = SimulationResult(
            job_id="test-job-branch",
            status=SimulationStatus.COMPLETED,
            system_model=unified_model,
        )
        mock_adapter._do_run_simulation = lambda config: mock_result

        # Create PowerFlow skill with mock adapter
        skill = PowerFlow(mock_adapter)

        # Run power flow
        result = skill.run_power_flow(model_id="test-model")

        # Verify branch data is correct
        model = result.system_model
        assert model is not None
        assert len(model.branches) == 1

        branch = model.branches[0]
        assert branch.from_bus == 0
        assert branch.to_bus == 1
        assert branch.p_from_mw == 80.0
        assert branch.p_to_mw == -78.0
        assert branch.loading_percent == 85.0

    def test_powerflow_run_power_flow_with_unified(self):
        """Test the run_power_flow_with_unified method."""
        from cloudpss_skills_v2.powerskill.powerflow import PowerFlow

        # Create mock adapter
        mock_adapter = MockEngineAdapter()
        mock_adapter.connect()  # Connect the adapter

        # Create unified model
        unified_model = PowerSystemModel(
            buses=[
                Bus(bus_id=0, name="Bus 0", base_kv=110.0, bus_type="SLACK", v_magnitude_pu=1.0),
                Bus(bus_id=1, name="Bus 1", base_kv=110.0, bus_type="PQ", v_magnitude_pu=0.95),
            ],
            branches=[
                Branch(from_bus=0, to_bus=1, name="Line 0-1", p_from_mw=80.0, loading_percent=85.0),
            ],
            base_mva=100.0,
        )

        mock_result = SimulationResult(
            job_id="test-job-unified",
            status=SimulationStatus.COMPLETED,
            system_model=unified_model,
            data={"summary": {"converged": True}},
        )
        mock_adapter._do_run_simulation = lambda config: mock_result

        # Create PowerFlow skill with mock adapter
        skill = PowerFlow(mock_adapter)

        # Call run_power_flow_with_unified
        result = skill.run_power_flow_with_unified(
            model_id="test-model",
            algorithm="newton_raphson",
        )

        # Verify result structure
        assert "status" in result
        assert result["status"] == "completed"
        assert "job_id" in result
        assert result["job_id"] == "test-job-unified"
        assert "unified_model" in result
        assert result["unified_model"] is not None
        assert isinstance(result["unified_model"], PowerSystemModel)

        # Verify buses and branches are included as dictionaries
        assert "buses" in result
        assert len(result["buses"]) == 2
        assert result["buses"][0]["name"] == "Bus 0"
        assert result["buses"][0]["v_magnitude_pu"] == 1.0

        assert "branches" in result
        assert len(result["branches"]) == 1
        assert result["branches"][0]["name"] == "Line 0-1"
        assert result["branches"][0]["loading_percent"] == 85.0

        # Verify data and errors are included
        assert "data" in result
        assert "errors" in result
        assert "warnings" in result

    def test_powerflow_run_power_flow_with_unified_no_model(self):
        """Test run_power_flow_with_unified when no unified model available."""
        from cloudpss_skills_v2.powerskill.powerflow import PowerFlow

        # Create mock adapter
        mock_adapter = MockEngineAdapter()
        mock_adapter.connect()  # Connect the adapter

        # Create result without unified model
        mock_result = SimulationResult(
            job_id="test-job-no-model",
            status=SimulationStatus.COMPLETED,
            system_model=None,
            data={"summary": {"converged": True}},
        )
        mock_adapter._do_run_simulation = lambda config: mock_result

        # Create PowerFlow skill with mock adapter
        skill = PowerFlow(mock_adapter)

        # Call run_power_flow_with_unified
        result = skill.run_power_flow_with_unified(
            model_id="test-model",
        )

        # Verify result structure even without unified model
        assert result["status"] == "completed"
        assert result["unified_model"] is None
        assert result["buses"] == []
        assert result["branches"] == []

    def test_powerflow_run_power_flow_with_unified_failed_simulation(self):
        """Test run_power_flow_with_unified when simulation fails."""
        from cloudpss_skills_v2.powerskill.powerflow import PowerFlow

        # Create mock adapter
        mock_adapter = MockEngineAdapter()
        mock_adapter.connect()  # Connect the adapter

        # Create failed result
        mock_result = SimulationResult(
            job_id="test-job-failed",
            status=SimulationStatus.FAILED,
            system_model=None,
            errors=["Convergence failed after 100 iterations"],
        )
        mock_adapter._do_run_simulation = lambda config: mock_result

        # Create PowerFlow skill with mock adapter
        skill = PowerFlow(mock_adapter)

        # Call run_power_flow_with_unified
        result = skill.run_power_flow_with_unified(
            model_id="test-model",
        )

        # Verify failed result structure
        assert result["status"] == "failed"
        assert result["unified_model"] is None
        assert len(result["errors"]) == 1
        assert "Convergence failed" in result["errors"][0]


class TestPowerFlowUnifiedModelEdgeCases:
    """Test edge cases for unified model integration."""

    def test_powerflow_failed_simulation_no_model(self):
        """Test that failed simulations don't have unified model."""
        from cloudpss_skills_v2.powerskill.powerflow import PowerFlow

        # Create mock adapter
        mock_adapter = MockEngineAdapter()
        mock_adapter.connect()  # Connect the adapter

        # Create a failed result
        mock_result = SimulationResult(
            job_id="test-job-failed",
            status=SimulationStatus.FAILED,
            system_model=None,
            errors=["Convergence failed"],
        )
        mock_adapter._do_run_simulation = lambda config: mock_result

        # Create PowerFlow skill with mock adapter
        skill = PowerFlow(mock_adapter)

        # Run power flow
        result = skill.run_power_flow(model_id="test-model")

        # Verify result shows failure
        assert result.status == SimulationStatus.FAILED
        # Unified model should be None for failed runs
        assert result.system_model is None

    def test_powerflow_get_system_model_with_fallback(self):
        """Test get_system_model fallback to adapter's get_unified_model."""
        from cloudpss_skills_v2.powerskill.powerflow import PowerFlow

        # Create mock adapter with get_unified_model method
        mock_adapter = MockEngineAdapter()
        mock_adapter.connect()  # Connect the adapter

        unified_model = PowerSystemModel(
            buses=[Bus(bus_id=0, name="Bus 0", base_kv=110.0)],
            base_mva=100.0,
        )
        mock_adapter.get_unified_model = lambda job_id: unified_model

        # Create result without system_model to trigger fallback
        mock_result = SimulationResult(
            job_id="test-job-fallback",
            status=SimulationStatus.COMPLETED,
            system_model=None,
        )
        mock_adapter._do_get_result = lambda job_id: mock_result

        # Create PowerFlow skill with mock adapter
        skill = PowerFlow(mock_adapter)

        # Get system model - should use fallback
        model = skill.get_system_model("test-job-fallback")

        # Verify fallback was used
        assert model is not None
        assert isinstance(model, PowerSystemModel)

    def test_powerflow_empty_model(self):
        """Test handling of empty unified model."""
        from cloudpss_skills_v2.powerskill.powerflow import PowerFlow

        # Create mock adapter
        mock_adapter = MockEngineAdapter()
        mock_adapter.connect()  # Connect the adapter

        # Create empty unified model
        unified_model = PowerSystemModel(
            buses=[],
            branches=[],
            base_mva=100.0,
        )

        mock_result = SimulationResult(
            job_id="test-job-empty",
            status=SimulationStatus.COMPLETED,
            system_model=unified_model,
        )
        mock_adapter._do_run_simulation = lambda config: mock_result

        # Create PowerFlow skill with mock adapter
        skill = PowerFlow(mock_adapter)

        # Run power flow
        result = skill.run_power_flow(model_id="test-model")

        # Verify empty model is handled correctly
        assert result.system_model is not None
        assert len(result.system_model.buses) == 0
        assert len(result.system_model.branches) == 0


class TestPowerFlowCachedResult:
    """Test the cached result functionality."""

    def test_powerflow_get_cached_result(self):
        """Test that get_cached_result returns the last result."""
        from cloudpss_skills_v2.powerskill.powerflow import PowerFlow

        # Create mock adapter
        mock_adapter = MockEngineAdapter()
        mock_adapter.connect()  # Connect the adapter

        unified_model = PowerSystemModel(
            buses=[Bus(bus_id=0, name="Bus 0", base_kv=110.0)],
            base_mva=100.0,
        )

        mock_result = SimulationResult(
            job_id="test-job-cached",
            status=SimulationStatus.COMPLETED,
            system_model=unified_model,
        )
        mock_adapter._do_run_simulation = lambda config: mock_result

        # Create PowerFlow skill with mock adapter
        skill = PowerFlow(mock_adapter)

        # Initially no cached result
        assert skill.get_cached_result() is None

        # Run power flow
        result = skill.run_power_flow(model_id="test-model")

        # Cached result should now be available
        cached = skill.get_cached_result()
        assert cached is not None
        assert cached.job_id == "test-job-cached"
        assert cached.system_model is not None

    def test_powerflow_get_system_model_uses_cache(self):
        """Test that get_system_model uses cached result when available."""
        from cloudpss_skills_v2.powerskill.powerflow import PowerFlow

        # Create mock adapter
        mock_adapter = MockEngineAdapter()
        mock_adapter.connect()  # Connect the adapter

        unified_model = PowerSystemModel(
            buses=[Bus(bus_id=0, name="Cached Bus", base_kv=110.0)],
            base_mva=100.0,
        )

        mock_result = SimulationResult(
            job_id="test-job-cache-hit",
            status=SimulationStatus.COMPLETED,
            system_model=unified_model,
        )
        mock_adapter._do_run_simulation = lambda config: mock_result

        # Create PowerFlow skill with mock adapter
        skill = PowerFlow(mock_adapter)

        # Run power flow to populate cache
        skill.run_power_flow(model_id="test-model")

        # get_system_model should use cached result without calling adapter.get_result
        # Reset the mock to verify it's not called
        original_get_result = mock_adapter._do_get_result
        mock_adapter._do_get_result = lambda job_id: SimulationResult(
            job_id=job_id, status=SimulationStatus.COMPLETED, system_model=None
        )

        model = skill.get_system_model("test-job-cache-hit")

        # Should get the model from cache, not from the new empty result
        assert model is not None
        assert model.buses[0].name == "Cached Bus"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
