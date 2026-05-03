"""Integration tests for PowerFlow with unified model.

This module tests the integration between PowerFlow API and the unified model
to ensure proper result handling and caching.
"""

import pytest
from unittest.mock import MagicMock, patch


def test_powerflow_integration_returns_unified_model():
    """Integration test: PowerFlow skill returns unified model."""
    from cloudpss_skills_v2.powerskill.powerflow import PowerFlow
    from cloudpss_skills_v2.core.system_model import PowerSystemModel, Bus
    from cloudpss_skills_v2.powerapi.base import SimulationResult, SimulationStatus, EngineAdapter

    # Create a mock adapter with spec to pass isinstance check
    mock_adapter = MagicMock(spec=EngineAdapter)

    # Create mock result with unified model
    mock_result = SimulationResult(
        status=SimulationStatus.COMPLETED,
        job_id="test-job-001",
        data={"buses": [], "branches": []},
        errors=[],
        system_model=PowerSystemModel(
            buses=[Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK")],
            base_mva=100.0
        )
    )

    mock_adapter.run_simulation.return_value = mock_result

    # Create PowerFlow with mock adapter
    powerflow = PowerFlow(mock_adapter)

    # Run power flow
    result = powerflow.run_power_flow(model_id="test-model")

    # Verify result contains unified model
    assert result.system_model is not None
    assert isinstance(result.system_model, PowerSystemModel)
    assert len(result.system_model.buses) == 1
    assert result.system_model.buses[0].name == "Bus1"


def test_powerflow_run_power_flow_with_unified():
    """Test run_power_flow_with_unified returns dict with unified model."""
    from cloudpss_skills_v2.powerskill.powerflow import PowerFlow
    from cloudpss_skills_v2.core.system_model import PowerSystemModel, Bus
    from cloudpss_skills_v2.powerapi.base import SimulationResult, SimulationStatus, EngineAdapter

    mock_adapter = MagicMock(spec=EngineAdapter)

    mock_result = SimulationResult(
        status=SimulationStatus.COMPLETED,
        job_id="test-job-001",
        data={"buses": [], "branches": []},
        errors=[],
        system_model=PowerSystemModel(
            buses=[Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK")],
            base_mva=100.0
        )
    )

    mock_adapter.run_simulation.return_value = mock_result

    powerflow = PowerFlow(mock_adapter)
    result = powerflow.run_power_flow_with_unified(model_id="test-model")

    # Verify result structure
    assert "unified_model" in result
    assert result["unified_model"] is not None
    assert result["status"] == "completed"
    assert "buses" in result
    assert len(result["buses"]) == 1
    assert result["buses"][0]["name"] == "Bus1"


def test_powerflow_caches_unified_model():
    """Test that PowerFlow caches the unified model for subsequent access."""
    from cloudpss_skills_v2.powerskill.powerflow import PowerFlow
    from cloudpss_skills_v2.core.system_model import PowerSystemModel, Bus
    from cloudpss_skills_v2.powerapi.base import SimulationResult, SimulationStatus, EngineAdapter

    mock_adapter = MagicMock(spec=EngineAdapter)

    mock_result = SimulationResult(
        status=SimulationStatus.COMPLETED,
        job_id="test-job-001",
        data={},
        errors=[],
        system_model=PowerSystemModel(
            buses=[Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK")],
            base_mva=100.0
        )
    )

    mock_adapter.run_simulation.return_value = mock_result

    powerflow = PowerFlow(mock_adapter)

    # Run power flow
    powerflow.run_power_flow(model_id="test-model")

    # Verify we can get the cached unified model via get_system_model
    cached_model = powerflow.get_system_model("test-job-001")
    assert cached_model is not None
    assert isinstance(cached_model, PowerSystemModel)

    # Verify we can also get via get_cached_result
    cached_result = powerflow.get_cached_result()
    assert cached_result is not None
    assert cached_result.system_model is not None


def test_powerflow_run_power_flow_with_unified_no_model():
    """Test run_power_flow_with_unified handles missing unified model gracefully."""
    from cloudpss_skills_v2.powerskill.powerflow import PowerFlow
    from cloudpss_skills_v2.powerapi.base import SimulationResult, SimulationStatus, EngineAdapter

    mock_adapter = MagicMock(spec=EngineAdapter)

    # Create result without unified model
    mock_result = SimulationResult(
        status=SimulationStatus.COMPLETED,
        job_id="test-job-002",
        data={"buses": [], "branches": []},
        errors=[],
        system_model=None  # No unified model
    )

    mock_adapter.run_simulation.return_value = mock_result

    powerflow = PowerFlow(mock_adapter)
    result = powerflow.run_power_flow_with_unified(model_id="test-model")

    # Verify result structure handles missing model gracefully
    assert "unified_model" in result
    assert result["unified_model"] is None
    assert result["buses"] == []
    assert result["branches"] == []


def test_powerflow_run_power_flow_failure():
    """Test PowerFlow handles failed simulation gracefully."""
    from cloudpss_skills_v2.powerskill.powerflow import PowerFlow
    from cloudpss_skills_v2.powerapi.base import SimulationResult, SimulationStatus, EngineAdapter

    mock_adapter = MagicMock(spec=EngineAdapter)

    # Create failed result
    mock_result = SimulationResult(
        status=SimulationStatus.FAILED,
        job_id="test-job-003",
        data={},
        errors=["Convergence failed"],
        system_model=None
    )

    mock_adapter.run_simulation.return_value = mock_result

    powerflow = PowerFlow(mock_adapter)
    result = powerflow.run_power_flow(model_id="test-model")

    # Verify failed result handling
    assert result.status == SimulationStatus.FAILED
    assert result.system_model is None
    assert len(result.errors) == 1
    assert "Convergence failed" in result.errors[0]


def test_powerflow_get_system_model_from_adapter():
    """Test get_system_model falls back to adapter when not cached."""
    from cloudpss_skills_v2.powerskill.powerflow import PowerFlow
    from cloudpss_skills_v2.core.system_model import PowerSystemModel, Bus
    from cloudpss_skills_v2.powerapi.base import SimulationResult, SimulationStatus, EngineAdapter

    mock_adapter = MagicMock(spec=EngineAdapter)

    # Mock get_result to return a result with unified model
    mock_result = SimulationResult(
        status=SimulationStatus.COMPLETED,
        job_id="test-job-004",
        data={},
        errors=[],
        system_model=PowerSystemModel(
            buses=[Bus(bus_id=0, name="Bus2", base_kv=110.0, bus_type="PQ")],
            base_mva=100.0
        )
    )

    mock_adapter.get_result.return_value = mock_result

    powerflow = PowerFlow(mock_adapter)

    # Get system model without having run simulation
    model = powerflow.get_system_model("test-job-004")

    # Verify we got the model from adapter
    assert model is not None
    assert model.buses[0].name == "Bus2"
    mock_adapter.get_result.assert_called_once_with("test-job-004")


def test_powerflow_run_power_flow_with_unified_dict_conversion():
    """Test that bus and branch dictionaries are correctly formatted."""
    from cloudpss_skills_v2.powerskill.powerflow import PowerFlow
    from cloudpss_skills_v2.core.system_model import PowerSystemModel, Bus, Branch
    from cloudpss_skills_v2.powerapi.base import SimulationResult, SimulationStatus, EngineAdapter

    mock_adapter = MagicMock(spec=EngineAdapter)

    mock_result = SimulationResult(
        status=SimulationStatus.COMPLETED,
        job_id="test-job-005",
        data={"buses": [], "branches": []},
        errors=[],
        system_model=PowerSystemModel(
            buses=[
                Bus(bus_id=0, name="SlackBus", base_kv=230.0, bus_type="SLACK",
                    v_magnitude_pu=1.0, v_angle_degree=0.0),
                Bus(bus_id=1, name="LoadBus", base_kv=230.0, bus_type="PQ",
                    v_magnitude_pu=0.95, v_angle_degree=-2.5)
            ],
            branches=[
                Branch(from_bus=0, to_bus=1, name="Line1", branch_type="LINE",
                       r_pu=0.01, x_pu=0.1, rate_a_mva=100.0)
            ],
            base_mva=100.0
        )
    )

    mock_adapter.run_simulation.return_value = mock_result

    powerflow = PowerFlow(mock_adapter)
    result = powerflow.run_power_flow_with_unified(model_id="test-model")

    # Verify buses are converted to dicts correctly
    assert len(result["buses"]) == 2
    bus_dict = result["buses"][0]
    assert bus_dict["bus_id"] == 0
    assert bus_dict["name"] == "SlackBus"
    assert bus_dict["base_kv"] == 230.0
    assert bus_dict["bus_type"] == "SLACK"
    assert bus_dict["v_magnitude_pu"] == 1.0
    assert bus_dict["v_angle_degree"] == 0.0

    # Verify branches are converted to dicts correctly
    assert len(result["branches"]) == 1
    branch_dict = result["branches"][0]
    assert branch_dict["from_bus"] == 0
    assert branch_dict["to_bus"] == 1
    assert branch_dict["name"] == "Line1"
    assert branch_dict["branch_type"] == "LINE"
    assert branch_dict["r_pu"] == 0.01
    assert branch_dict["x_pu"] == 0.1
