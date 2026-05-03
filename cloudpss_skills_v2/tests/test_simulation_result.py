"""Tests for SimulationResult class."""

import pytest
from datetime import datetime

from cloudpss_skills_v2.powerapi.base import SimulationResult, SimulationStatus
from cloudpss_skills_v2.core.system_model import PowerSystemModel, Bus


def test_simulation_result_has_unified_model():
    """Test that SimulationResult can hold a unified PowerSystemModel."""
    model = PowerSystemModel(
        buses=[Bus(
            bus_id=0,
            name="Bus1",
            base_kv=230.0,
            bus_type="SLACK",
            v_magnitude_pu=1.0,
            v_angle_degree=0.0
        )],
        base_mva=100.0
    )

    result = SimulationResult(
        job_id="test-001",
        status=SimulationStatus.COMPLETED,
        system_model=model
    )

    assert result.system_model is not None
    assert result.system_model.buses[0].name == "Bus1"


def test_simulation_result_get_unified_model_method():
    """Test that SimulationResult has get_unified_model() method."""
    model = PowerSystemModel(
        buses=[Bus(
            bus_id=0,
            name="Bus1",
            base_kv=230.0,
            bus_type="SLACK",
            v_magnitude_pu=1.0,
            v_angle_degree=0.0
        )],
        base_mva=100.0
    )

    result = SimulationResult(
        job_id="test-002",
        status=SimulationStatus.COMPLETED,
        system_model=model
    )

    # Test the get_unified_model method
    unified_model = result.get_unified_model()
    assert unified_model is not None
    assert unified_model.buses[0].bus_id == 0
    assert unified_model.base_mva == 100.0


def test_simulation_result_without_system_model():
    """Test that SimulationResult works without system_model (backward compatible)."""
    result = SimulationResult(
        job_id="test-003",
        status=SimulationStatus.COMPLETED,
        data={"voltage": [1.0, 1.02, 0.98]}
    )

    assert result.system_model is None
    assert result.get_unified_model() is None


def test_simulation_result_default_values():
    """Test SimulationResult default values."""
    result = SimulationResult(
        job_id="test-004",
        status=SimulationStatus.PENDING
    )

    assert result.job_id == "test-004"
    assert result.status == SimulationStatus.PENDING
    assert result.data == {}
    assert result.metadata == {}
    assert result.errors == []
    assert result.warnings == []
    assert result.started_at is None
    assert result.completed_at is None
    assert result.system_model is None


def test_simulation_result_is_success_property():
    """Test SimulationResult is_success property."""
    # Success case
    success_result = SimulationResult(
        job_id="test-005",
        status=SimulationStatus.COMPLETED
    )
    assert success_result.is_success is True

    # Failed case - wrong status
    failed_status = SimulationResult(
        job_id="test-006",
        status=SimulationStatus.FAILED
    )
    assert failed_status.is_success is False

    # Failed case - has errors
    with_errors = SimulationResult(
        job_id="test-007",
        status=SimulationStatus.COMPLETED,
        errors=["Something went wrong"]
    )
    assert with_errors.is_success is False


def test_simulation_result_duration_seconds():
    """Test SimulationResult duration_seconds property."""
    start = datetime(2024, 1, 1, 12, 0, 0)
    end = datetime(2024, 1, 1, 12, 0, 5)

    result = SimulationResult(
        job_id="test-008",
        status=SimulationStatus.COMPLETED,
        started_at=start,
        completed_at=end
    )

    assert result.duration_seconds == 5.0

    # Test with missing timestamps
    incomplete = SimulationResult(
        job_id="test-009",
        status=SimulationStatus.PENDING
    )
    assert incomplete.duration_seconds is None


def test_simulation_result_to_dict():
    """Test SimulationResult to_dict method."""
    start = datetime(2024, 1, 1, 12, 0, 0)
    end = datetime(2024, 1, 1, 12, 0, 5)

    result = SimulationResult(
        job_id="test-010",
        status=SimulationStatus.COMPLETED,
        data={"voltage": [1.0, 1.02]},
        started_at=start,
        completed_at=end
    )

    d = result.to_dict()
    assert d["job_id"] == "test-010"
    assert d["status"] == "completed"
    assert d["data"] == {"voltage": [1.0, 1.02]}
    assert d["duration_seconds"] == 5.0


def test_simulation_result_to_skill_result_dict():
    """Test SimulationResult to_skill_result_dict method."""
    start = datetime(2024, 1, 1, 12, 0, 0)
    end = datetime(2024, 1, 1, 12, 0, 5)

    result = SimulationResult(
        job_id="test-011",
        status=SimulationStatus.COMPLETED,
        data={"voltage": [1.0, 1.02]},
        started_at=start,
        completed_at=end
    )

    d = result.to_skill_result_dict()
    assert d["skill_name"] == "test-011"
    assert d["status"] == "completed"
    assert d["success"] is True
    assert d["data"] == {"voltage": [1.0, 1.02]}
    assert d["duration_seconds"] == 5.0
