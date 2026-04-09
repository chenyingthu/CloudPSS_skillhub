#!/usr/bin/env python3
"""
EMT量测核心 helper - 单元测试
"""

import math
from unittest.mock import Mock, patch

from cloudpss_skills.core.emt_measurement_core import (
    add_voltage_meter_output_chain,
    average_trace_in_window,
    compute_vsi_from_voltage_channels,
    compute_windowed_dv_metrics,
    get_three_phase_rms_trace,
)


class TestEmtMeasurementCoreUnit:
    @patch("cloudpss.model.implements.component.Component")
    def test_add_voltage_meter_output_chain_appends_output_group(self, mock_component):
        working_model = Mock()
        bus_component = Mock()
        bus_component.id = "bus-id"
        bus_component.canvas = "canvas_0"
        bus_component.position = {"x": 100, "y": 200}
        bus_component.zIndex = 10
        channel_template = Mock()
        channel_template.args = {"Name": "vac"}
        channel_template.canvas = "canvas_0"
        channel_template.position = {"x": 0, "y": 0}
        channel_template.size = {"width": 110, "height": 20}
        channel_template.zIndex = 10

        meter = Mock()
        meter.id = "meter-id"
        meter.zIndex = 9
        channel = Mock()
        channel.id = "channel-id"
        working_model.addComponent.side_effect = [meter, channel]
        working_model.getComponentsByRid.return_value = {"template": channel_template}
        working_model.getAllComponents.return_value = {}
        working_model.jobs = [{"rid": "function/CloudPSS/emtps", "args": {"output_channels": []}}]
        diagram = Mock()
        diagram.cells = {}
        working_model.revision.getImplements.return_value.getDiagram.return_value = diagram

        plot_index, _, _ = add_voltage_meter_output_chain(
            working_model,
            bus_component=bus_component,
            signal_name="#Bus1.VSI_V",
            channel_name="vac_Bus1",
            sampling_freq=2000,
            meter_label="meter",
            channel_label="channel",
        )

        assert plot_index == 0
        assert working_model.jobs[0]["args"]["output_channels"][0]["4"] == ["channel-id"]

    def test_get_three_phase_rms_trace_reconstructs_rms(self):
        result = type(
            "FakeResult",
            (),
            {
                "getPlotChannelData": lambda self, plot_index, trace_name: {
                    "trace:0": {"x": [0.0, 1.0], "y": [1.0, 1.0]},
                    "trace:1": {"x": [0.0, 1.0], "y": [1.0, -1.0]},
                    "trace:2": {"x": [0.0, 1.0], "y": [1.0, 1.0]},
                }.get(trace_name)
            },
        )()

        times, vrms = get_three_phase_rms_trace(result, plot_index=0, trace_prefix="trace")

        assert times == [0.0, 1.0]
        assert vrms == [1.0, 1.0]

    def test_average_trace_in_window_uses_time_bounds(self):
        avg = average_trace_in_window([0.0, 0.2, 0.4, 0.6], [1.0, 2.0, 3.0, 4.0], start=0.2, end=0.6)
        assert avg == 2.5

    def test_compute_windowed_dv_metrics_uses_three_phase_rms(self):
        result = type(
            "FakeResult",
            (),
            {
                "getPlotChannelData": lambda self, plot_index, trace_name: {
                    "trace:0": {"x": [0.0, 0.5, 1.0, 1.5], "y": [1.0, 1.0, 1.1, 1.0]},
                    "trace:1": {"x": [0.0, 0.5, 1.0, 1.5], "y": [1.0, 1.0, 1.1, 1.0]},
                    "trace:2": {"x": [0.0, 0.5, 1.0, 1.5], "y": [1.0, 1.0, 1.1, 1.0]},
                }.get(trace_name)
            },
        )()

        dv = compute_windowed_dv_metrics(
            result,
            disturbance_time=0.5,
            measurement_channels=[{"plot_index": 0, "trace_prefix": "trace"}],
            dv_judge_criteria=[[0.0, 1.0, 0.95, 1.2]],
        )

        assert math.isclose(dv["dv_up"][0], 0.1, rel_tol=0.0, abs_tol=1e-9)
        assert math.isclose(dv["dv_down"][0], 0.05, rel_tol=0.0, abs_tol=1e-9)

    def test_compute_vsi_from_voltage_channels_aggregates_per_bus(self):
        result = type(
            "FakeResult",
            (),
            {
                "getPlotChannelData": lambda self, plot_index, trace_name: {
                    "bus1:0": {"x": [0.0, 0.5, 1.0, 1.5], "y": [1.0, 1.0, 0.9, 0.9]},
                    "bus2:0": {"x": [0.0, 0.5, 1.0, 1.5], "y": [1.0, 1.0, 0.8, 0.8]},
                }.get(trace_name)
            },
        )()

        vsi = compute_vsi_from_voltage_channels(
            result,
            test_buses=[{"label": "Bus_A"}],
            measurement_channels=[
                {"bus_label": "Bus_A", "trace_name": "bus1:0", "plot_index": 0},
                {"bus_label": "Bus_B", "trace_name": "bus2:0", "plot_index": 0},
            ],
            q_base=10.0,
            start_time=1.0,
            interval=1.0,
            duration=0.5,
        )

        assert vsi["unsupported_buses"] == []
        assert math.isclose(vsi["vsi_i"]["Bus_A"], 0.015, rel_tol=0.0, abs_tol=1e-9)
        assert math.isclose(vsi["vsi_ij"]["Bus_A"]["Bus_A"], 0.01, rel_tol=0.0, abs_tol=1e-9)
        assert math.isclose(vsi["vsi_ij"]["Bus_A"]["Bus_B"], 0.02, rel_tol=0.0, abs_tol=1e-9)
