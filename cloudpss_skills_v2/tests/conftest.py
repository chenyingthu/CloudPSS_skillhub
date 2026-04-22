"""Shared test fixtures for cloudpss_skills_v2 tests."""

import os
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def cloudpss_token():
    """Get CloudPSS token from env or file."""
    token = os.environ.get("CLOUDPSS_TOKEN")
    if token:
        return token

    for token_file in [".cloudpss_token", ".cloudpss_token_internal"]:
        p = Path(token_file)
        if p.exists():
            return p.read_text().strip()
    return None


@pytest.fixture(scope="session")
def cloudpss_api_url():
    """Get CloudPSS API URL."""
    return os.environ.get("CLOUDPSS_API_URL", "https://internal.cloudpss.com")


@pytest.fixture(scope="session")
def cloudpss_model_rid():
    """Get CloudPSS model RID from env."""
    return os.environ.get("CLOUDPSS_MODEL_RID")


@pytest.fixture(scope="session")
def has_cloudpss_token(cloudpss_token):
    """Check if CloudPSS token is available."""
    return cloudpss_token is not None


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "integration: integration tests requiring external services"
    )
    config.addinivalue_line("markers", "cloudpss: CloudPSS API tests")
    config.addinivalue_line("markers", "pandapower: pandapower tests")
    config.addinivalue_line("markers", "slow: slow tests")
