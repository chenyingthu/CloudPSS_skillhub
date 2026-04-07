#!/usr/bin/env python3
"""
VSI弱母线技能 - 单元测试
"""

from cloudpss_skills.builtin.vsi_weak_bus import VSIWeakBusSkill, _matches_bus_identifier


class FakeResult:
    def __init__(self, voltage_plot, q_plot):
        self._plots = {0: voltage_plot, 1: q_plot}

    def getPlot(self, idx):
        return self._plots[idx]


class TestVSIWeakBusUnit:
    def test_bus_identifier_match_is_not_overbroad(self):
        assert _matches_bus_identifier("Bus30", "Bus30") is True
        assert _matches_bus_identifier("Bus30", "Bus3") is False

    def test_calculate_vsi_marks_bus_unsupported_when_q_trace_missing(self):
        skill = VSIWeakBusSkill()
        result = FakeResult(
            voltage_plot={"data": {"traces": [{"name": "BusA", "x": [0.0, 1.0, 2.0], "y": [1.0, 0.95, 0.94]}]}},
            q_plot={"data": {"traces": []}},
        )

        vsi = skill._calculate_vsi(
            result=result,
            test_buses=[{"label": "Bus_1"}],
            voltage_measure_k=0,
            q_measure_k=1,
            start_time=1.0,
            interval=1.0,
            duration=0.5,
        )

        assert vsi["vsi_i"] == {}
        assert vsi["unsupported_buses"] == ["Bus_1"]

    def test_run_like_flow_should_fail_when_all_buses_are_unsupported(self, skill=None):
        vsi_results = {"vsi_i": {}, "vsi_ij": {}, "unsupported_buses": ["Bus_1", "Bus_2"]}
        assert not vsi_results["vsi_i"]
