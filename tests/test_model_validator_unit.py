#!/usr/bin/env python3
"""
模型验证技能 - 单元测试
"""

import os
import sys
from types import SimpleNamespace
from unittest.mock import patch

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cloudpss_skills.builtin.model_validator import (
    ModelValidatorSkill,
    BUS_COLUMN,
    VM_COLUMN,
    P_GEN_COLUMN,
)


def make_table(column_map):
    return {
        "data": {
            "columns": [
                {"name": name, "data": values}
                for name, values in column_map.items()
            ]
        }
    }


class FakeJob:
    def __init__(self, buses, branches, status=1):
        self.id = "job-test"
        self._status = status
        self.result = SimpleNamespace(
            getBuses=lambda: buses,
            getBranches=lambda: branches,
        )

    def status(self):
        return self._status


class FakeModel:
    def __init__(self, components, buses, branches):
        self._components = components
        self._job = FakeJob(buses, branches)

    def getAllComponents(self):
        return self._components

    def runPowerFlow(self):
        return self._job


def renewable_component(definition, *, label, pins, args=None):
    return SimpleNamespace(
        definition=definition,
        label=label,
        pins=pins,
        args=args or {},
    )


def bus_component(*, label, signal):
    return SimpleNamespace(
        definition="model/CloudPSS/_newBus_3p",
        label=label,
        pins={"0": signal},
        args={"Name": signal},
    )


class TestModelValidatorUnit:
    @pytest.fixture
    def skill(self):
        return ModelValidatorSkill()

    def test_powerflow_fails_on_empty_result_tables(self, skill):
        model = FakeModel(
            components={"canvas_0_45": bus_component(label="Bus10", signal="bus10")},
            buses=[],
            branches=[],
        )

        with patch("cloudpss.Model.fetch", return_value=model):
            result = skill._validate_powerflow({"rid": "model/test"}, tolerance=1e-6, timeout=1)

        assert result["passed"] is False
        assert any("母线表" in error or "支路表" in error for error in result["errors"])

    def test_powerflow_fails_when_renewable_has_zero_injection(self, skill):
        components = {
            "canvas_0_45": bus_component(label="Bus10", signal="bus10"),
            "comp_wind": renewable_component(
                "model/open-cloudpss/WTG_PMSG_01-avm-stdm-v2b1",
                label="WindFarm_Bus10",
                pins={"0": "bus10"},
                args={"pf_P": 80.0, "P_cmd": 80.0},
            ),
        }
        buses = [make_table({
            BUS_COLUMN: ["canvas_0_45"],
            VM_COLUMN: [0.95],
            P_GEN_COLUMN: [0.0],
        })]
        branches = [make_table({"Branch": ["line-1"], "<i>P</i><sub>ij</sub> / MW": [10.0]})]
        model = FakeModel(components=components, buses=buses, branches=branches)

        with patch("cloudpss.Model.fetch", return_value=model):
            result = skill._validate_powerflow({"rid": "model/test"}, tolerance=1e-6, timeout=1)

        assert result["passed"] is False
        assert any("未真实进入潮流结果" in error or "实际潮流出力为" in error for error in result["errors"])

    def test_powerflow_passes_when_renewable_injection_is_present(self, skill):
        components = {
            "canvas_0_45": bus_component(label="Bus10", signal="bus10"),
            "comp_wind": renewable_component(
                "model/open-cloudpss/WTG_PMSG_01-avm-stdm-v2b1",
                label="WindFarm_Bus10",
                pins={"0": "bus10"},
                args={"pf_P": 80.0, "P_cmd": 80.0},
            ),
        }
        buses = [make_table({
            BUS_COLUMN: ["canvas_0_45"],
            VM_COLUMN: [0.9572],
            P_GEN_COLUMN: [80.0],
        })]
        branches = [make_table({"Branch": ["line-1"], "<i>P</i><sub>ij</sub> / MW": [10.0]})]
        model = FakeModel(components=components, buses=buses, branches=branches)

        with patch("cloudpss.Model.fetch", return_value=model):
            result = skill._validate_powerflow({"rid": "model/test"}, tolerance=1e-6, timeout=1)

        assert result["passed"] is True
        assert result["details"]["renewable_rows"][0]["actual_p"] == 80.0

    def test_topology_flags_invalid_display_name_bus_connection(self, skill):
        components = {
            "canvas_0_45": bus_component(label="newBus_3p-21", signal="bus10"),
            "comp_wind": renewable_component(
                "model/open-cloudpss/WTG_PMSG_01-avm-stdm-v2b1",
                label="WindFarm_Bus10",
                pins={"0": "Bus10"},
                args={"pf_P": 80.0, "P_cmd": 80.0},
            ),
        }
        model = FakeModel(components=components, buses=[], branches=[])

        with patch("cloudpss.Model.fetch", return_value=model):
            result = skill._validate_topology({"rid": "model/test"})

        assert result["passed"] is False
        assert any("不是有效母线信号" in error for error in result["errors"])
