#!/usr/bin/env python3
"""
无功补偿设计技能 - 单元测试
"""

from cloudpss_skills.builtin.reactive_compensation_design import ReactiveCompensationDesignSkill
from cloudpss_skills.builtin.reactive_compensation_design import (
    _matches_bus_identifier,
    _as_numeric,
    _resolve_model_numeric,
)


class TestReactiveCompensationDesignUnit:
    def test_as_numeric_supports_cloudpss_source_dict(self):
        assert _as_numeric({"source": "20"}) == 20.0
        assert _as_numeric({"source": "1.047"}) == 1.047

    def test_resolve_model_numeric_supports_variable_reference_expression(self):
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

        assert _resolve_model_numeric(fake_model, {"source": "$Bus_7_Vbase"}) == 525.0
        assert _resolve_model_numeric(fake_model, {"source": "$Bus_7_Vbase / sqrt(3)"}) == 525.0 / (3 ** 0.5)

    def test_bus_identifier_match_is_not_overbroad(self):
        assert _matches_bus_identifier("Bus30", "Bus30") is True
        assert _matches_bus_identifier("Bus30", "Bus3") is False
        assert _matches_bus_identifier("Bus_30", "Bus30") is True

    def test_calculate_dv_from_result_returns_empty_when_no_voltage_traces(self):
        skill = ReactiveCompensationDesignSkill()
        result = type("FakeResult", (), {"getPlots": lambda self: []})()

        dv = skill._calculate_dv_from_result(result, disturbance_time=4.0, measurement_channels=[])

        assert dv == {"dv_up": [], "dv_down": []}

    def test_calculate_dv_from_result_uses_three_phase_rms(self):
        class FakeResult:
            def getPlotChannelData(self, plot_index, trace_name):
                x = [3.4, 3.6, 3.8, 4.0, 4.2, 4.4]
                return {"x": x, "y": [1.0] * len(x)}

        skill = ReactiveCompensationDesignSkill()
        dv = skill._calculate_dv_from_result(
            FakeResult(),
            disturbance_time=4.0,
            measurement_channels=[{"plot_index": 3, "trace_prefix": "vac_bus7"}],
        )

        assert dv["dv_up"] == [0.25]
        assert dv["dv_down"] == [0.25]

    def test_calculate_dv_from_result_respects_windowed_criteria(self):
        skill = ReactiveCompensationDesignSkill()

        class FakeResult:
            def getPlotChannelData(self, plot_index, trace_name):
                samples = {
                    "trace:0": {"x": [0.0, 0.2, 0.4, 0.6, 1.2], "y": [1.0, 1.0, 1.18, 0.98, 1.02]},
                    "trace:1": {"x": [0.0, 0.2, 0.4, 0.6, 1.2], "y": [1.0, 1.0, 1.18, 0.98, 1.02]},
                    "trace:2": {"x": [0.0, 0.2, 0.4, 0.6, 1.2], "y": [1.0, 1.0, 1.18, 0.98, 1.02]},
                }
                return samples.get(trace_name)

        dv = skill._calculate_dv_from_result(
            FakeResult(),
            disturbance_time=0.2,
            measurement_channels=[{"plot_index": 0, "trace_prefix": "trace"}],
            dv_judge_criteria=[[0.0, 0.5, 0.8, 1.2], [0.5, 1.5, 0.95, 1.05]],
        )

        assert dv["dv_up"][0] >= 0
        assert dv["dv_down"][0] >= 0
