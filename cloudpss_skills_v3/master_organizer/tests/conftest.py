"""Pytest import setup for direct subdirectory test runs."""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import pytest


def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line(
        "markers", "e2e: mark test as end-to-end test requiring browser"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as unit test"
    )


@pytest.fixture
def sample_model_data():
    """Provide sample model data for tests."""
    return {
        "buses": [
            {"id": 1, "type": "slack", "v": 1.0, "angle": 0.0},
            {"id": 2, "type": "pq", "p": 100.0, "q": 20.0},
        ],
        "branches": [
            {"from": 1, "to": 2, "r": 0.01, "x": 0.1, "b": 0.0},
        ],
    }


@pytest.fixture
def sample_powerflow_result():
    """Provide sample powerflow result for tests."""
    return {
        "buses": [
            {"id": 1, "v": 1.0, "angle": 0.0, "p": 0.0, "q": 0.0},
            {"id": 2, "v": 0.95, "angle": -5.2, "p": 100.0, "q": 20.0},
        ],
        "branches": [
            {"from": 1, "to": 2, "p_from": 100.5, "q_from": 25.3, "p_to": -100.0, "q_to": -20.0},
        ],
        "converged": True,
        "iterations": 5,
    }


@pytest.fixture
def mock_server_response():
    """Provide mock server response structure."""
    return {
        "success": True,
        "data": {"job_id": "test-job-123", "status": "completed"},
    }
