"""Shared test fixtures for cloudpss_skills_v2 tests."""

from pathlib import Path

import pytest


LOCAL_CLOUDPSS_API_URL = "http://166.111.60.76:50001"
LOCAL_CLOUDPSS_MODEL_RID = "model/chenying/IEEE39"


@pytest.fixture(scope="session")
def cloudpss_token():
    """Get the token for the local CloudPSS integration server."""

    for token_file in [".cloudpss_token_internal"]:
        p = Path(token_file)
        if p.exists():
            return p.read_text().strip()
    return None


@pytest.fixture(scope="session")
def cloudpss_api_url():
    """Get the CloudPSS API URL used by integration tests."""
    return LOCAL_CLOUDPSS_API_URL


@pytest.fixture(scope="session")
def cloudpss_model_rid():
    """Get the CloudPSS model RID used by integration tests."""
    return LOCAL_CLOUDPSS_MODEL_RID


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
