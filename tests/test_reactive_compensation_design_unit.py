#!/usr/bin/env python3
"""
无功补偿设计技能 - 单元测试
"""

from cloudpss_skills.builtin.reactive_compensation_design import ReactiveCompensationDesignSkill
from cloudpss_skills.builtin.reactive_compensation_design import _matches_bus_identifier


class TestReactiveCompensationDesignUnit:
    def test_bus_identifier_match_is_not_overbroad(self):
        assert _matches_bus_identifier("Bus30", "Bus30") is True
        assert _matches_bus_identifier("Bus30", "Bus3") is False
        assert _matches_bus_identifier("Bus_30", "Bus30") is True

    def test_calculate_dv_from_result_returns_empty_when_no_voltage_traces(self):
        skill = ReactiveCompensationDesignSkill()
        result = type("FakeResult", (), {"getPlots": lambda self: []})()

        dv = skill._calculate_dv_from_result(result, disturbance_time=4.0)

        assert dv == {"dv_up": [], "dv_down": []}
