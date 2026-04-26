"""Bounded live integration tests for PowerAnalysis skills.

These tests intentionally use the local CloudPSS server and one or two known
IEEE39 components. They are not smoke tests: each test runs the real skill
entrypoint through the CloudPSS adapter and asserts shaped outputs.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from cloudpss_skills_v2.core.skill_result import SkillStatus
from cloudpss_skills_v2.poweranalysis.contingency_analysis import ContingencyAnalysis
from cloudpss_skills_v2.poweranalysis.n1_security import N1SecurityAnalysis
from cloudpss_skills_v2.poweranalysis.voltage_stability import VoltageStabilityAnalysis

LOCAL_BASE_URL = "http://166.111.60.76:50001"
IEEE39_RID = "model/chenying/IEEE39"
KNOWN_BRANCH_KEY = "canvas_0_105"


def get_token() -> str:
    token_file = Path(".cloudpss_token_internal")
    if token_file.exists():
        return token_file.read_text(encoding="utf-8").strip()
    return os.environ.get("CLOUDPSS_TOKEN", "")


@pytest.fixture(scope="session")
def live_auth() -> dict[str, str]:
    token = get_token()
    if len(token) < 100:
        pytest.skip("No valid local CloudPSS token available")
    return {"token": token, "base_url": LOCAL_BASE_URL}


@pytest.fixture
def output_dir(tmp_path):
    return {"path": str(tmp_path), "generate_report": False, "timestamp": False}


def base_config(skill: str, live_auth: dict[str, str], output_dir: dict[str, str]):
    return {
        "skill": skill,
        "engine": "cloudpss",
        "auth": live_auth,
        "model": {"rid": IEEE39_RID, "source": "cloud"},
        "output": output_dir,
    }


def assert_finished_with_data(result, required_keys: set[str]) -> None:
    assert result.status in {SkillStatus.SUCCESS, SkillStatus.FAILED}
    assert isinstance(result.data, dict)
    assert required_keys <= set(result.data.keys())
    assert result.artifacts


class TestN1SecurityAnalysis:
    def test_validation_rejects_missing_model(self):
        result = N1SecurityAnalysis().run({})
        assert result.status == SkillStatus.FAILED
        assert result.error

    def test_single_known_branch_live(self, live_auth, output_dir):
        result = N1SecurityAnalysis().run(
            {
                **base_config("n1_security", live_auth, output_dir),
                "analysis": {
                    "branches": [KNOWN_BRANCH_KEY],
                    "check_voltage": True,
                    "check_thermal": False,
                },
            }
        )

        assert_finished_with_data(result, {"model_rid", "_typed", "voltage_threshold"})
        typed = result.data["_typed"]
        assert typed["summary"]["total_scenarios"] == 1
        assert typed["contingencies"]


class TestVoltageStabilityAnalysis:
    def test_validation_rejects_missing_model(self):
        result = VoltageStabilityAnalysis().run({})
        assert result.status == SkillStatus.FAILED
        assert result.error

    def test_two_point_live_scan(self, live_auth, output_dir):
        result = VoltageStabilityAnalysis().run(
            {
                **base_config("voltage_stability", live_auth, output_dir),
                "scan": {
                    "load_scaling": [1.0, 1.01],
                    "load_target": "newExpLoad-2",
                    "scale_generation": False,
                },
                "monitoring": {
                    "buses": [],
                    "collapse_threshold": 0.7,
                },
            }
        )

        assert_finished_with_data(result, {"model_rid", "total_cases", "results"})
        assert result.data["total_cases"] == 2
        assert len(result.data["results"]) == 2


class TestContingencyAnalysis:
    def test_validation_rejects_missing_model(self):
        result = ContingencyAnalysis().run({})
        assert result.status == SkillStatus.FAILED
        assert result.error

    def test_single_known_branch_live(self, live_auth, output_dir):
        result = ContingencyAnalysis().run(
            {
                **base_config("contingency_analysis", live_auth, output_dir),
                "contingency": {
                    "level": "N-1",
                    "components": [KNOWN_BRANCH_KEY],
                    "component_types": ["branch"],
                    "max_combinations": 1,
                },
                "analysis": {
                    "check_voltage": True,
                    "check_thermal": False,
                    "voltage_limit": {"min": 0.7, "max": 1.3},
                    "severity_threshold": 0.8,
                },
                "ranking": {"top_n": 1},
            }
        )

        assert_finished_with_data(result, {"model_rid", "summary", "all_results"})
        assert result.data["summary"]["total_cases"] == 1
        assert len(result.data["all_results"]) == 1
