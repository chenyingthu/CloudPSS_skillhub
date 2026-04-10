import os
import sys

os.environ["CLOUDPSS_API_URL"] = "http://166.111.60.76:50001"

from pathlib import Path
import time
import uuid
from importlib import reload

import pytest

from cloudpss import Model, setToken
import cloudpss_skills.builtin

DEFAULT_TEST_MODEL_RID = os.environ.get("TEST_MODEL_RID", "model/chenying/IEEE39")


@pytest.fixture(scope="session", autouse=True)
def ensure_skills_registered():
    """Ensure skills are registered at the start of each test session."""
    reload(cloudpss_skills.builtin)


@pytest.fixture(scope="module", autouse=True)
def reensure_skills_registered():
    """Re-ensure skills are registered for each test module."""
    for key in list(sys.modules.keys()):
        if (
            key.startswith("cloudpss_skills.builtin")
            and key != "cloudpss_skills.builtin"
        ):
            del sys.modules[key]
    reload(cloudpss_skills.builtin)


def load_token():
    token_path = Path(".cloudpss_token_internal")
    if token_path.exists():
        return token_path.read_text().strip()
    token_path = Path(".cloudpss_token")
    if token_path.exists():
        return token_path.read_text().strip()
    return os.environ.get("CLOUDPSS_TOKEN", "").strip()


def pytest_addoption(parser):
    parser.addoption(
        "--run-integration",
        action="store_true",
        default=False,
        help="run tests that call the live CloudPSS API",
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-integration"):
        return

    skip_integration = pytest.mark.skip(
        reason="need --run-integration to run live CloudPSS integration tests"
    )
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip_integration)


@pytest.fixture(scope="session")
def live_auth():
    token = load_token()
    if not token:
        pytest.skip("missing CloudPSS token for integration tests")
    setToken(token)
    return token


@pytest.fixture(scope="session")
def integration_model(live_auth):
    return Model.fetch(DEFAULT_TEST_MODEL_RID)


@pytest.fixture(scope="session")
def integration_ieee3_model(live_auth):
    return Model.fetch("model/chenying/IEEE3")


@pytest.fixture(scope="session")
def integration_save_key_prefix():
    prefix = os.environ.get("TEST_SAVE_KEY_PREFIX", "").strip()
    if not prefix:
        pytest.skip("missing TEST_SAVE_KEY_PREFIX for live save integration test")
    return prefix


@pytest.fixture(scope="session")
def integration_save_key(integration_save_key_prefix):
    suffix = f"{int(time.time())}_{uuid.uuid4().hex[:8]}"
    return f"{integration_save_key_prefix}_{suffix}"
