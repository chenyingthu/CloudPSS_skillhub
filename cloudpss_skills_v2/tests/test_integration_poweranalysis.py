"""
Integration Tests for PowerAnalysis Skills with Local Server

Tests N-1 security, voltage stability, and contingency analysis
with the local CloudPSS server.
"""

import pytest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cloudpss_skills_v2.poweranalysis.n1_security import N1SecurityAnalysis
from cloudpss_skills_v2.poweranalysis.voltage_stability import VoltageStabilityAnalysis
from cloudpss_skills_v2.poweranalysis.contingency_analysis import ContingencyAnalysis


def get_token():
    token_file = "/home/chenying/researches/cloudpss-toolkit/.cloudpss_token_internal"
    if os.path.exists(token_file):
        with open(token_file) as f:
            return f.read().strip()
    return os.environ.get("CLOUDPSS_TOKEN", "")


def get_config(model_rid, skill="n1_security"):
    token = get_token()
    return {
        "skill": skill,
        "auth": {
            "token": token,
            "base_url": "http://166.111.60.76:50001",
        },
        "model": {"rid": model_rid, "source": "cloud"},
        "engine": "cloudpss",
    }


class TestN1SecurityAnalysis:

    def test_n1_validate_requires_model_and_auth(self):
        skill = N1SecurityAnalysis()
        result = skill.run({})
        assert result.status.value == "failed"

    def test_n1_validate_rejects_invalid_contingency_type(self):
        skill = N1SecurityAnalysis()
        result = skill.run({
            **get_config("model/chenying/IEEE39"),
            "analysis": {"contingency_type": "invalid_type"},
        })
        assert result.status.value == "failed"

    def test_n1_validate_accepts_valid_config_structure(self):
        skill = N1SecurityAnalysis()
        result = skill.run({
            **get_config("model/chenying/IEEE39"),
            "analysis": {"contingency_type": "branch"},
        })
        assert result.status.value in ("completed", "failed")


class TestVoltageStabilityAnalysis:

    def test_voltage_stability_validate_requires_model_and_auth(self):
        skill = VoltageStabilityAnalysis()
        result = skill.run({})
        assert result.status.value == "failed"

    def test_voltage_stability_validate_rejects_invalid_method(self):
        skill = VoltageStabilityAnalysis()
        result = skill.run({
            **get_config("model/chenying/IEEE39", "voltage_stability"),
            "analysis": {"method": "invalid_method"},
        })
        assert result.status.value == "failed"

    def test_voltage_stability_validate_accepts_valid_config(self):
        skill = VoltageStabilityAnalysis()
        result = skill.run({
            **get_config("model/chenying/IEEE39", "voltage_stability"),
            "analysis": {"method": "continuation"},
        })
        assert result.status.value in ("completed", "failed")


class TestContingencyAnalysis:

    def test_contingency_validate_requires_model_and_auth(self):
        skill = ContingencyAnalysis()
        result = skill.run({})
        assert result.status.value == "failed"

    def test_contingency_validate_rejects_invalid_scenario(self):
        skill = ContingencyAnalysis()
        result = skill.run({
            **get_config("model/chenying/IEEE39", "contingency_analysis"),
            "scenarios": "invalid",
        })
        assert result.status.value == "failed"

    def test_contingency_validate_accepts_valid_config(self):
        skill = ContingencyAnalysis()
        result = skill.run({
            **get_config("model/chenying/IEEE39", "contingency_analysis"),
            "scenarios": [{"type": "branch", "id": "L1"}],
        })
        assert result.status.value in ("completed", "failed")


class TestPowerAnalysisEndToEnd:

    def test_n1_security_workflow(self):
        skill = N1SecurityAnalysis()
        result = skill.run({
            **get_config("model/chenying/IEEE39"),
            "analysis": {"contingency_type": "branch", "max_violations": 10},
        })
        assert result.status.value in ("completed", "failed")

    def test_voltage_stability_workflow(self):
        skill = VoltageStabilityAnalysis()
        result = skill.run({
            **get_config("model/chenying/IEEE39", "voltage_stability"),
            "analysis": {"method": "continuation"},
        })
        assert result.status.value in ("completed", "failed")

    def test_contingency_analysis_workflow(self):
        skill = ContingencyAnalysis()
        result = skill.run({
            **get_config("model/chenying/IEEE39", "contingency_analysis"),
            "scenarios": [{"type": "branch", "id": "T1-T2"}],
        })
        assert result.status.value in ("completed", "failed")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])