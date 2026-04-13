#!/usr/bin/env python3
"""
Thevenin Equivalent Skill - Integration Tests

使用真实 CloudPSS API 验证 PCC 戴维南等值阻抗计算。
"""

import pytest

import cloudpss_skills.builtin
from cloudpss_skills import get_skill


@pytest.mark.integration
class TestTheveninEquivalentSkill:
    @pytest.fixture
    def skill(self):
        skill = get_skill("thevenin_equivalent")
        assert skill is not None
        return skill

    @pytest.fixture
    def base_config(self, live_auth):
        return {
            "skill": "thevenin_equivalent",
            "auth": {"token": live_auth, },
            "model": {"rid": "model/holdme/IEEE39", "source": "cloud"},
            "pcc": {"bus": "bus8"},
            "equivalent": {"system_base_mva": 100.0, "rating_mva": 50.0},
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "test_thevenin_equivalent",
                "timestamp": True,
            },
        }

    def test_skill_registration(self, skill):
        assert skill.name == "thevenin_equivalent"
        assert "戴维南等值" in skill.description

    def test_validation_success(self, skill, base_config):
        result = skill.validate(base_config)
        assert result.valid is True

    def test_validation_missing_bus(self, skill, base_config):
        base_config["pcc"].pop("bus")
        result = skill.validate(base_config)
        assert result.valid is False

    def test_real_execution(self, skill, base_config):
        result = skill.run(base_config)
        assert result.status.value == "success", result.error

        data = result.data
        assert data["verified"] is True
        assert data["pcc_bus"] == "bus8"
        assert data["short_circuit_capacity_mva"] > 0
        assert data["z_th_pu"]["magnitude"] > 0
        assert data["scr"] > 0

        print(
            f"\n✅ PCC={data['pcc_bus']} Zth={data['z_th_pu']} "
            f"Ssc={data['short_circuit_capacity_mva']}MVA SCR={data['scr']}"
        )
