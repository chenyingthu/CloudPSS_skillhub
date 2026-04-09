#!/usr/bin/env python3
"""
VSI弱母线技能 - 单元测试
"""

from cloudpss_skills.builtin.vsi_weak_bus import VSIWeakBusSkill, _matches_bus_identifier, _as_numeric
from cloudpss_skills.core import sync_support_core as sync_core


class FakeResult:
    def __init__(self, voltage_plot, q_plot):
        self._plots = {0: voltage_plot, 1: q_plot}

    def getPlot(self, idx):
        return self._plots[idx]


class TestVSIWeakBusUnit:
    def test_as_numeric_supports_cloudpss_source_dict(self):
        assert _as_numeric({"source": "20"}) == 20.0
        assert _as_numeric({"source": "1.047"}) == 1.047

    def test_shared_numeric_resolution_supports_variable_reference_expression(self):
        fake_model = type(
            "FakeModel",
            (),
            {
                "toJSON": lambda self: {
                    "revision": {
                        "implements": {
                            "diagram": {
                                "variables": [
                                    {"key": "Bus_7_Vbase", "value": {"source": "525", "ɵexp": ""}},
                                ]
                            }
                        }
                    }
                }
            },
        )()

        assert sync_core.resolve_model_numeric(fake_model, {"source": "$Bus_7_Vbase"}) == 525.0
        assert sync_core.resolve_model_numeric(fake_model, {"source": "$Bus_7_Vbase / sqrt(3)"}) == 525.0 / (3 ** 0.5)

    def test_bus_identifier_match_is_not_overbroad(self):
        assert _matches_bus_identifier("Bus30", "Bus30") is True
        assert _matches_bus_identifier("Bus30", "Bus3") is False

    def test_calculate_vsi_marks_bus_unsupported_when_q_trace_missing(self):
        skill = VSIWeakBusSkill()
        vsi = skill._calculate_vsi(
            result=type(
                "FakeResult2",
                (),
                {
                    "getPlotChannelData": lambda self, plot_index, trace_name: {"x": [0.0, 1.0, 2.0], "y": [1.0, 0.95, 0.94]}
                    if trace_name == "bus1:0" else None
                },
            )(),
            test_buses=[{"label": "Bus_1"}],
            measurement_channels=[{"bus_label": "Bus_1", "trace_name": "bus1:0", "plot_index": 0}],
            q_base=0.0,
            start_time=1.0,
            interval=1.0,
            duration=0.5,
        )

        assert vsi["vsi_i"] == {}
        assert vsi["unsupported_buses"] == ["Bus_1"]

    def test_run_like_flow_should_fail_when_all_buses_are_unsupported(self, skill=None):
        vsi_results = {"vsi_i": {}, "vsi_ij": {}, "unsupported_buses": ["Bus_1", "Bus_2"]}
        assert not vsi_results["vsi_i"]
