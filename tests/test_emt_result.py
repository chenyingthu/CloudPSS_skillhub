from copy import deepcopy
import importlib.util
import math
from pathlib import Path
import time

import pytest

from cloudpss import Model
from cloudpss.job.result import EMTResult
from cloudpss.model.implements.component import Component


REPO_ROOT = Path(__file__).resolve().parents[1]
EMT_FAULT_STUDY_EXAMPLE_PATH = (
    REPO_ROOT / "examples" / "analysis" / "emt_fault_study_example.py"
)
EMT_FAULT_SEVERITY_SCAN_EXAMPLE_PATH = (
    REPO_ROOT / "examples" / "analysis" / "emt_fault_severity_scan_example.py"
)
EMT_FAULT_CLEARING_SCAN_EXAMPLE_PATH = (
    REPO_ROOT / "examples" / "analysis" / "emt_fault_clearing_scan_example.py"
)
EMT_MEASUREMENT_WORKFLOW_EXAMPLE_PATH = (
    REPO_ROOT / "examples" / "analysis" / "emt_measurement_workflow_example.py"
)
EMT_N1_SECURITY_SCREENING_EXAMPLE_PATH = (
    REPO_ROOT / "examples" / "analysis" / "emt_n1_security_screening_example.py"
)
EMT_RESEARCH_REPORT_EXAMPLE_PATH = (
    REPO_ROOT / "examples" / "analysis" / "emt_research_report_example.py"
)
EMT_N1_SECURITY_REPORT_EXAMPLE_PATH = (
    REPO_ROOT / "examples" / "analysis" / "emt_n1_security_report_example.py"
)
EMT_N1_FULL_REPORT_EXAMPLE_PATH = (
    REPO_ROOT / "examples" / "analysis" / "emt_n1_full_report_example.py"
)


def load_module(module_path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class DummyReceiver:
    def __init__(self, messages):
        self.messages = list(messages)

    def __iter__(self):
        return self

    def __next__(self):
        raise StopIteration

    def waitFor(self, timeout):
        return True


class DummySender:
    def __init__(self):
        self.writes = []

    def write(self, message):
        self.writes.append(message)


class DummyJob:
    def __init__(self, sender=None):
        self._sender = sender or DummySender()

    def write(self):
        return self._sender


def build_plot_message(key, trace_name, xs, ys):
    return {
        "type": "plot",
        "key": key,
        "data": {
            "traces": [
                {
                    "name": trace_name,
                    "type": "scatter",
                    "mode": "lines",
                    "x": list(xs),
                    "y": list(ys),
                    "yaxis": "y",
                }
            ]
        },
    }


def wait_for_completion(job, timeout=300, interval=5):
    start = time.time()
    while True:
        status = job.status()
        if status == 1:
            return
        if status == 2:
            pytest.fail("EMT job failed on CloudPSS")
        if time.time() - start > timeout:
            pytest.fail("EMT job timed out")
        time.sleep(interval)


def nearest_trace_value(trace, target_time):
    best_index = min(
        range(len(trace["x"])),
        key=lambda index: abs(trace["x"][index] - target_time),
    )
    return trace["x"][best_index], trace["y"][best_index]


def trace_window_rms(trace, start_time, end_time):
    samples = [
        y
        for x, y in zip(trace["x"], trace["y"])
        if start_time <= x <= end_time
    ]
    if not samples:
        pytest.fail(f"trace window {start_time}..{end_time} contains no samples")
    return math.sqrt(sum(y * y for y in samples) / len(samples))


def table_rows(table):
    columns = table["data"]["columns"]
    labels = [column.get("name") or column.get("title") or f"col_{index}" for index, column in enumerate(columns)]
    row_count = len(columns[0].get("data", [])) if columns else 0
    rows = []

    for row_index in range(row_count):
        row = {}
        for label, column in zip(labels, columns):
            row[label] = column.get("data", [None] * row_count)[row_index]
        rows.append(row)

    return rows


def build_powerflow_modified_model(model):
    powerflow_job = model.runPowerFlow()
    wait_for_completion(powerflow_job)

    model_dict = deepcopy(model.toJSON())
    powerflow_job.result.powerFlowModify(model_dict)
    return Model(model_dict), powerflow_job.result


def build_prepared_ieee3_model(
    integration_ieee3_model,
    fault_end_time="2.7",
    sampling_freq="2000",
    fault_chg="0.01",
):
    working_model = Model(deepcopy(integration_ieee3_model.toJSON()))
    components = working_model.getAllComponents()

    fault = next(
        component
        for component in components.values()
        if getattr(component, "definition", None)
        == "model/CloudPSS/_newFaultResistor_3p"
    )
    voltage_channel = next(
        component
        for component in components.values()
        if getattr(component, "definition", None)
        == "model/CloudPSS/_newChannel"
        and component.args.get("Name") == "vac"
    )
    emt_job = next(
        job for job in working_model.jobs if job["rid"] == "function/CloudPSS/emtps"
    )

    working_model.updateComponent(
        fault.id,
        args={
            "fs": {"source": "2.5", "ɵexp": ""},
            "fe": {"source": fault_end_time, "ɵexp": ""},
            "chg": {"source": fault_chg, "ɵexp": ""},
        },
    )
    working_model.updateComponent(
        voltage_channel.id,
        args={"Freq": {"source": sampling_freq, "ɵexp": ""}},
    )
    emt_job["args"]["output_channels"][0]["1"] = int(sampling_freq)

    return working_model


def build_fault_ready_ieee3_model(integration_ieee3_model, fault_end_time="2.7", fault_chg="0.01"):
    working_model = Model(deepcopy(integration_ieee3_model.toJSON()))
    components = working_model.getAllComponents()

    fault = next(
        component
        for component in components.values()
        if getattr(component, "definition", None)
        == "model/CloudPSS/_newFaultResistor_3p"
    )
    working_model.updateComponent(
        fault.id,
        args={
            "fs": {"source": "2.5", "ɵexp": ""},
            "fe": {"source": fault_end_time, "ɵexp": ""},
            "chg": {"source": fault_chg, "ɵexp": ""},
        },
    )

    return working_model


def resolved_bus_args(working_model, bus_name):
    topology = working_model.fetchTopology("emtp").toJSON()["components"]
    matching_bus = next(
        component
        for component in topology.values()
        if component.get("definition") == "model/CloudPSS/_newBus_3p"
        and component.get("args", {}).get("Name") == bus_name
    )
    return matching_bus["args"]


def add_voltage_meter_output_chain(
    working_model,
    *,
    bus_component,
    channel_template,
    signal_name,
    channel_name,
    sampling_freq,
    meter_label,
    channel_label,
    meter_position,
    channel_position,
    meter_size=None,
    channel_size=None,
    edge_template=None,
    edge_vertex=None,
):
    new_meter = working_model.addComponent(
        "model/CloudPSS/_NewVoltageMeter",
        meter_label,
        args={"Dim": "3", "V": signal_name},
        pins={"0": ""},
        canvas=bus_component.canvas,
        position=meter_position,
        size=meter_size or {"width": 30, "height": 50},
    )
    new_channel = working_model.addComponent(
        "model/CloudPSS/_newChannel",
        channel_label,
        args={
            **channel_template.args,
            "Name": channel_name,
            "Dim": {"source": "3", "ɵexp": ""},
            "Freq": {"source": str(sampling_freq), "ɵexp": ""},
        },
        pins={"0": signal_name},
        canvas=channel_template.canvas,
        position=channel_position,
        size=channel_size or channel_template.size,
    )

    new_edge_id = f"edge_{new_meter.id}"
    if edge_template is not None:
        new_edge = deepcopy(edge_template.toJSON())
        new_edge["id"] = new_edge_id
        new_edge["source"] = {"cell": new_meter.id, "port": "0"}
        new_edge["target"] = deepcopy(edge_template.target)
        new_edge["target"]["cell"] = bus_component.id
        if edge_vertex is not None:
            new_edge["vertices"] = [edge_vertex]
    else:
        new_edge = {
            "id": new_edge_id,
            "shape": "diagram-edge",
            "canvas": bus_component.canvas,
            "attrs": {
                "line": {
                    "sourceMarker": {"args": {"cx": 0, "r": 0.5}, "name": "circle"},
                    "stroke": "var(--stroke)",
                    "strokeWidth": "var(--stroke-width)",
                    "targetMarker": {"args": {"cx": 0, "r": 0.5}, "name": "circle"},
                },
                "lines": {"connection": True, "strokeLinejoin": "round"},
                "root": {"style": {"--stroke-width": 2}},
            },
            "source": {"cell": new_meter.id, "port": "0"},
            "target": {
                "anchor": {
                    "args": {"dx": "-20%", "dy": "0%", "rotate": True},
                    "name": "center",
                },
                "cell": bus_component.id,
                "port": "0",
                "selector": "> path:nth-child(2)",
            },
            "vertices": [edge_vertex] if edge_vertex is not None else [],
            "zIndex": min(
                getattr(new_meter, "zIndex", 0),
                getattr(bus_component, "zIndex", 0),
            )
            - 1,
        }
    working_model.revision.getImplements().getDiagram().cells[new_edge_id] = Component(
        new_edge
    )

    emt_job = next(
        job for job in working_model.jobs if job["rid"] == "function/CloudPSS/emtps"
    )
    emt_job["args"]["output_channels"].append(
        {
            "0": f"{channel_name}_group",
            "1": int(sampling_freq),
            "2": "compressed",
            "3": 0,
            "4": [new_channel.id],
        }
    )
    return len(emt_job["args"]["output_channels"]) - 1, new_meter, new_channel


class TestEMTResultUnit:
    def test_get_messages_by_key_filters_receiver_cache(self):
        result = EMTResult(
            DummyJob(),
            DummyReceiver(
                [
                    {"key": "summary", "type": "log", "data": {"value": "ignore"}},
                    {"key": "error", "type": "log", "data": {"value": "E1"}},
                    {"key": "error", "type": "log", "data": {"value": "E2"}},
                ]
            ),
        )

        messages = result.getMessagesByKey("error")

        assert messages == [
            {"key": "error", "type": "log", "data": {"value": "E1"}},
            {"key": "error", "type": "log", "data": {"value": "E2"}},
        ]

    def test_get_plots_merges_segments_using_real_sdk_class(self):
        result = EMTResult(
            DummyJob(),
            DummyReceiver(
                [
                    build_plot_message("plot-0", "Ia", [0.0, 0.1], [1.0, 1.1]),
                    build_plot_message("plot-0", "Ia", [0.2], [1.2]),
                ]
            ),
        )

        plots = list(result.getPlots())

        assert len(plots) == 1
        assert plots[0]["data"]["traces"][0]["x"] == [0.0, 0.1, 0.2]
        assert plots[0]["data"]["traces"][0]["y"] == [1.0, 1.1, 1.2]

    def test_plot_channel_helpers_return_trace_data(self):
        result = EMTResult(
            DummyJob(),
            DummyReceiver([build_plot_message("plot-0", "Va", [0.0, 0.1], [2.0, 2.1])]),
        )

        plot = result.getPlot(0)
        names = result.getPlotChannelNames(0)
        data = result.getPlotChannelData(0, "Va")

        assert plot["key"] == "plot-0"
        assert names == ["Va"]
        assert data["x"] == [0.0, 0.1]
        assert data["y"] == [2.0, 2.1]

    def test_get_plot_channel_data_falls_back_to_last_trace_for_unknown_name(self):
        result = EMTResult(
            DummyJob(),
            DummyReceiver(
                [
                    {
                        "type": "plot",
                        "key": "plot-0",
                        "data": {
                            "traces": [
                                {
                                    "name": "Va",
                                    "type": "scatter",
                                    "mode": "lines",
                                    "x": [0.0],
                                    "y": [1.0],
                                    "yaxis": "y",
                                },
                                {
                                    "name": "Ia",
                                    "type": "scatter",
                                    "mode": "lines",
                                    "x": [0.0],
                                    "y": [2.0],
                                    "yaxis": "y",
                                },
                            ]
                        },
                    }
                ]
            ),
        )

        data = result.getPlotChannelData(0, "missing-channel")

        assert data["name"] == "Ia"
        assert data["y"] == [2.0]

    def test_next_writes_debug_message(self):
        sender = DummySender()
        result = EMTResult(DummyJob(sender), DummyReceiver([]))

        result.next()

        assert sender.writes == [{"type": "debug", "step": -1}]

    def test_goto_writes_requested_step(self):
        sender = DummySender()
        result = EMTResult(DummyJob(sender), DummyReceiver([]))

        result.goto(42)

        assert sender.writes == [{"type": "debug", "step": 42}]

    def test_send_writes_virtual_input_payload(self):
        sender = DummySender()
        result = EMTResult(DummyJob(sender), DummyReceiver([]))

        result.send({"breaker": "open"})

        assert sender.writes == [
            {"type": "virtual_input", "data": {"breaker": "open"}}
        ]

    def test_write_shm_writes_memory_message(self):
        sender = DummySender()
        result = EMTResult(DummyJob(sender), DummyReceiver([]))

        result.writeShm("/tmp/buffer", b"abc", 4)

        assert sender.writes == [
            {
                "type": "memory",
                "path": "/tmp/buffer",
                "buffer": b"abc",
                "offset": 4,
            }
        ]

    def test_control_writes_eventchain_message(self):
        sender = DummySender()
        result = EMTResult(DummyJob(sender), DummyReceiver([]))

        result.control({"key": "R1", "value": 200, "uuid": "ctrl-1"})

        event = sender.writes[0]["event"][0]
        payload = event["defaultApp"]["para"]["R1"]["Value"]
        assert sender.writes[0]["type"] == "eventchain"
        assert event["eventType"] == "time"
        assert payload["value"] == 200
        assert payload["uuid"] == "ctrl-1"

    def test_monitor_writes_eventchain_message(self):
        sender = DummySender()
        result = EMTResult(DummyJob(sender), DummyReceiver([]))

        result.monitor(
            {
                "key": "Ia",
                "uuid": "monitor-1",
                "function": "abs",
                "period": 1,
                "value": 2.0,
                "freq": 50,
                "condition": ">",
                "cycle": 1,
                "nCount": 1,
            }
        )

        event = sender.writes[0]["event"][0]
        payload = event["defaultApp"]["para"]["Ia"]["a"]
        assert sender.writes[0]["type"] == "eventchain"
        assert event["eventType"] == "time"
        assert payload["uuid"] == "monitor-1"
        assert payload["function"] == "abs"
        assert payload["value"] == 2.0

    def test_stop_simulation_writes_control_event(self):
        sender = DummySender()
        result = EMTResult(DummyJob(sender), DummyReceiver([]))

        result.stopSimulation()

        event = sender.writes[0]["event"][0]
        payload = event["defaultApp"]["SimuCtrl"]["SimuCtrl"]
        assert sender.writes[0]["type"] == "eventchain"
        assert payload["ctrl_type"] == "0"
        assert "uuid" in payload

    def test_snapshot_controls_write_eventchain_messages(self):
        sender = DummySender()
        result = EMTResult(DummyJob(sender), DummyReceiver([]))

        result.saveSnapshot(1)
        result.loadSnapshot(2)

        save_event = sender.writes[0]["event"][0]
        save_payload = save_event["defaultApp"]["SnapshotCtrl"]["SnapshotCtrl"]
        load_event = sender.writes[1]["event"][0]
        load_payload = load_event["defaultApp"]["SnapshotCtrl"]["SnapshotCtrl"]

        assert sender.writes[0]["type"] == "eventchain"
        assert sender.writes[1]["type"] == "eventchain"
        assert save_payload["ctrl_type"] == "0"
        assert save_payload["snapshot_number"] == 1
        assert load_payload["ctrl_type"] == "1"
        assert load_payload["snapshot_number"] == 2


@pytest.fixture(scope="module")
def completed_emt_job(integration_model):
    job = integration_model.runEMT()
    wait_for_completion(job)
    return job


@pytest.mark.integration
class TestEMTResultIntegration:
    def test_get_messages_by_key_returns_raw_plot_segments(self, completed_emt_job):
        result = completed_emt_job.result
        first_plot = result.getPlot(0)
        messages = result.getMessagesByKey(first_plot["key"])

        assert isinstance(messages, list)
        assert messages
        assert all(message["key"] == first_plot["key"] for message in messages)
        assert all(message["type"] == "plot" for message in messages)
        assert "traces" in messages[0]["data"]

    def test_get_plots_returns_iterable_of_plot_dicts(self, completed_emt_job):
        result = completed_emt_job.result
        plots = list(result.getPlots())

        assert isinstance(result, EMTResult)
        assert plots
        assert isinstance(plots[0], dict)
        assert "key" in plots[0]
        assert "traces" in plots[0]["data"]

    def test_channel_accessors_return_real_trace_data(self, completed_emt_job):
        result = completed_emt_job.result
        plot = result.getPlot(0)
        names = result.getPlotChannelNames(0)
        data = result.getPlotChannelData(0, names[0])

        assert plot is not None
        assert isinstance(names, list)
        assert names
        assert isinstance(data, dict)
        assert "x" in data
        assert "y" in data

    def test_prepared_local_ieee3_yaml_can_run_emt_and_return_plots(
        self, integration_ieee3_model, tmp_path
    ):
        working_model = build_prepared_ieee3_model(
            integration_ieee3_model,
            fault_end_time="2.7",
            sampling_freq="2000",
        )
        components = working_model.getAllComponents()
        fault = next(
            component
            for component in components.values()
            if getattr(component, "definition", None)
            == "model/CloudPSS/_newFaultResistor_3p"
        )
        voltage_channel = next(
            component
            for component in components.values()
            if getattr(component, "definition", None)
            == "model/CloudPSS/_newChannel"
            and component.args.get("Name") == "vac"
        )
        emt_job = next(
            job for job in working_model.jobs if job["rid"] == "function/CloudPSS/emtps"
        )

        export_path = tmp_path / "ieee3-prepared.yaml"
        Model.dump(working_model, str(export_path), compress=None)
        prepared_model = Model.load(str(export_path))

        prepared_fault = prepared_model.getComponentByKey(fault.id)
        prepared_channel = prepared_model.getComponentByKey(voltage_channel.id)
        prepared_emt_job = next(
            job for job in prepared_model.jobs if job["rid"] == "function/CloudPSS/emtps"
        )

        assert prepared_fault.args["fs"]["source"] == "2.5"
        assert prepared_fault.args["fe"]["source"] == "2.7"
        assert prepared_channel.args["Freq"]["source"] == "2000"
        assert prepared_emt_job["args"]["output_channels"][0]["1"] == 2000

        job = prepared_model.runEMT()
        wait_for_completion(job)

        assert job.status() == 1

        result = job.result
        plots = list(result.getPlots())
        channel_names = result.getPlotChannelNames(0)

        assert plots
        assert channel_names

    def test_ieee3_fault_clearing_time_change_affects_post_fault_voltage_trace(
        self, integration_ieee3_model
    ):
        baseline_job = build_prepared_ieee3_model(
            integration_ieee3_model,
            fault_end_time="2.7",
            sampling_freq="2000",
        ).runEMT()
        wait_for_completion(baseline_job)
        baseline_result = baseline_job.result
        baseline_names = baseline_result.getPlotChannelNames(0)
        baseline_trace = baseline_result.getPlotChannelData(0, baseline_names[0])

        long_fault_job = build_prepared_ieee3_model(
            integration_ieee3_model,
            fault_end_time="2.9",
            sampling_freq="2000",
        ).runEMT()
        wait_for_completion(long_fault_job)
        long_fault_result = long_fault_job.result
        long_fault_names = long_fault_result.getPlotChannelNames(0)
        long_fault_trace = long_fault_result.getPlotChannelData(0, long_fault_names[0])

        assert baseline_names == long_fault_names
        assert len(baseline_trace["x"]) == len(long_fault_trace["x"]) == 20001

        _, baseline_mid_fault = nearest_trace_value(baseline_trace, 2.6)
        _, long_mid_fault = nearest_trace_value(long_fault_trace, 2.6)
        _, baseline_after_clear = nearest_trace_value(baseline_trace, 2.95)
        _, long_after_clear = nearest_trace_value(long_fault_trace, 2.95)

        # 故障尚未切除前，两种工况应基本一致；延长切除时间后，后故障时刻波形应明显偏离。
        assert long_mid_fault == pytest.approx(baseline_mid_fault, abs=1e-9)
        assert baseline_after_clear - long_after_clear > 0.003

    def test_ieee3_output_sampling_frequency_changes_trace_resolution(
        self, integration_ieee3_model
    ):
        low_freq_job = build_prepared_ieee3_model(
            integration_ieee3_model,
            fault_end_time="2.7",
            sampling_freq="1000",
        ).runEMT()
        wait_for_completion(low_freq_job)
        low_result = low_freq_job.result
        low_names = low_result.getPlotChannelNames(0)
        low_trace = low_result.getPlotChannelData(0, low_names[0])

        high_freq_job = build_prepared_ieee3_model(
            integration_ieee3_model,
            fault_end_time="2.7",
            sampling_freq="2000",
        ).runEMT()
        wait_for_completion(high_freq_job)
        high_result = high_freq_job.result
        high_names = high_result.getPlotChannelNames(0)
        high_trace = high_result.getPlotChannelData(0, high_names[0])

        assert low_names == high_names
        assert len(low_trace["x"]) == 10001
        assert len(high_trace["x"]) == 20001
        assert high_trace["x"][1] - high_trace["x"][0] == pytest.approx(
            (low_trace["x"][1] - low_trace["x"][0]) / 2,
            rel=1e-9,
            abs=1e-12,
        )
        assert high_trace["x"][-1] == pytest.approx(low_trace["x"][-1], abs=1e-9)

    def test_ieee3_fault_chg_parameter_changes_fault_depth_and_post_fault_recovery(
        self, integration_ieee3_model
    ):
        low_chg_job = build_prepared_ieee3_model(
            integration_ieee3_model,
            fault_end_time="2.7",
            sampling_freq="2000",
            fault_chg="1e-6",
        ).runEMT()
        wait_for_completion(low_chg_job)
        low_result = low_chg_job.result
        low_names = low_result.getPlotChannelNames(0)
        low_trace = low_result.getPlotChannelData(0, low_names[0])

        high_chg_job = build_prepared_ieee3_model(
            integration_ieee3_model,
            fault_end_time="2.7",
            sampling_freq="2000",
            fault_chg="1e4",
        ).runEMT()
        wait_for_completion(high_chg_job)
        high_result = high_chg_job.result
        high_names = high_result.getPlotChannelNames(0)
        high_trace = high_result.getPlotChannelData(0, high_names[0])

        assert low_names == high_names
        assert len(low_trace["x"]) == len(high_trace["x"]) == 20001

        _, low_prefault = nearest_trace_value(low_trace, 2.45)
        _, high_prefault = nearest_trace_value(high_trace, 2.45)
        _, low_mid_fault = nearest_trace_value(low_trace, 2.6)
        _, high_mid_fault = nearest_trace_value(high_trace, 2.6)
        _, low_post_fault = nearest_trace_value(low_trace, 2.95)
        _, high_post_fault = nearest_trace_value(high_trace, 2.95)

        # 在故障前，两种工况应保持相同初始状态；
        # 增大当前算例中的 chg 参数后，故障期间和故障后的电压跌落都会明显减轻。
        assert high_prefault == pytest.approx(low_prefault, abs=1e-12)
        assert high_mid_fault - low_mid_fault > 0.0015
        assert high_post_fault - low_post_fault > 0.004

    def test_ieee3_powerflow_modified_model_can_feed_emt_with_shifted_prefault_generator_power(
        self, integration_ieee3_model
    ):
        baseline_pf_model, baseline_pf_result = build_powerflow_modified_model(
            Model(deepcopy(integration_ieee3_model.toJSON()))
        )
        baseline_bus_rows = table_rows(baseline_pf_result.getBuses()[0])
        baseline_bus7 = next(row for row in baseline_bus_rows if row["Bus"] == "canvas_0_1091")

        baseline_emt_job = build_prepared_ieee3_model(
            baseline_pf_model,
            fault_end_time="2.7",
            sampling_freq="2000",
        ).runEMT()
        wait_for_completion(baseline_emt_job)
        baseline_emt_result = baseline_emt_job.result
        baseline_plot1_names = baseline_emt_result.getPlotChannelNames(1)
        baseline_p1_trace = baseline_emt_result.getPlotChannelData(1, "#P1:0")
        baseline_q1_trace = baseline_emt_result.getPlotChannelData(1, "#Q1:0")

        perturbed_working_model = Model(deepcopy(integration_ieee3_model.toJSON()))
        load_7 = perturbed_working_model.getComponentByKey("canvas_0_1083")
        perturbed_working_model.updateComponent(
            load_7.id,
            args={
                **load_7.args,
                "p": {"source": "180", "ɵexp": ""},
                "q": {"source": "80", "ɵexp": ""},
            },
        )
        perturbed_pf_model, perturbed_pf_result = build_powerflow_modified_model(
            perturbed_working_model
        )
        perturbed_bus_rows = table_rows(perturbed_pf_result.getBuses()[0])
        perturbed_bus7 = next(row for row in perturbed_bus_rows if row["Bus"] == "canvas_0_1091")

        perturbed_emt_job = build_prepared_ieee3_model(
            perturbed_pf_model,
            fault_end_time="2.7",
            sampling_freq="2000",
        ).runEMT()
        wait_for_completion(perturbed_emt_job)
        perturbed_emt_result = perturbed_emt_job.result
        perturbed_plot1_names = perturbed_emt_result.getPlotChannelNames(1)
        perturbed_p1_trace = perturbed_emt_result.getPlotChannelData(1, "#P1:0")
        perturbed_q1_trace = perturbed_emt_result.getPlotChannelData(1, "#Q1:0")

        _, baseline_prefault_p1 = nearest_trace_value(baseline_p1_trace, 2.45)
        _, baseline_prefault_q1 = nearest_trace_value(baseline_q1_trace, 2.45)
        _, perturbed_prefault_p1 = nearest_trace_value(perturbed_p1_trace, 2.45)
        _, perturbed_prefault_q1 = nearest_trace_value(perturbed_q1_trace, 2.45)

        assert baseline_plot1_names == perturbed_plot1_names
        assert "#P1:0" in baseline_plot1_names
        assert "#Q1:0" in baseline_plot1_names
        assert baseline_bus7["<i>P</i><sub>load</sub> / MW"] == pytest.approx(125.0)
        assert baseline_bus7["<i>Q</i><sub>load</sub> / MVar"] == pytest.approx(50.0)
        assert perturbed_bus7["<i>P</i><sub>load</sub> / MW"] == pytest.approx(180.0)
        assert perturbed_bus7["<i>Q</i><sub>load</sub> / MVar"] == pytest.approx(80.0)
        assert baseline_bus7["<i>V</i><sub>m</sub> / pu"] - perturbed_bus7["<i>V</i><sub>m</sub> / pu"] > 0.03

        # 先用潮流把更重的 7 号母线负荷重新平衡，再把结果写回模型后，
        # EMT 在故障前的机端功率通道应落到新的稳态工作点。
        assert perturbed_prefault_p1 - baseline_prefault_p1 > 50.0
        assert perturbed_prefault_q1 - baseline_prefault_q1 > 20.0

    def test_ieee3_meter_signal_rename_updates_plot_channel_names_without_changing_waveform(
        self, integration_ieee3_model
    ):
        baseline_job = build_prepared_ieee3_model(
            integration_ieee3_model,
            fault_end_time="2.7",
            sampling_freq="2000",
        ).runEMT()
        wait_for_completion(baseline_job)
        baseline_result = baseline_job.result
        baseline_names = baseline_result.getPlotChannelNames(2)
        baseline_trace = baseline_result.getPlotChannelData(2, baseline_names[0])

        working_model = build_prepared_ieee3_model(
            integration_ieee3_model,
            fault_end_time="2.7",
            sampling_freq="2000",
        )
        components = working_model.getAllComponents()
        voltage_meter = next(
            component
            for component in components.values()
            if getattr(component, "definition", None)
            == "model/CloudPSS/_NewVoltageMeter"
        )
        voltage_channel = next(
            component
            for component in components.values()
            if getattr(component, "definition", None)
            == "model/CloudPSS/_newChannel"
            and component.args.get("Name") == "vac"
        )

        working_model.updateComponent(
            voltage_meter.id,
            args={**voltage_meter.args, "V": "#bus7_voltage"},
        )
        working_model.updateComponent(
            voltage_channel.id,
            args={
                **voltage_channel.args,
                "Name": "bus7_voltage",
                "Freq": {"source": "2000", "ɵexp": ""},
            },
            pins={"0": "#bus7_voltage"},
        )

        renamed_job = working_model.runEMT()
        wait_for_completion(renamed_job)
        renamed_result = renamed_job.result
        renamed_names = renamed_result.getPlotChannelNames(2)
        renamed_trace = renamed_result.getPlotChannelData(2, renamed_names[0])

        _, baseline_prefault = nearest_trace_value(baseline_trace, 2.45)
        _, renamed_prefault = nearest_trace_value(renamed_trace, 2.45)
        _, baseline_postfault = nearest_trace_value(baseline_trace, 2.95)
        _, renamed_postfault = nearest_trace_value(renamed_trace, 2.95)

        assert baseline_names == ["vac:0", "vac:1", "vac:2"]
        assert renamed_names == ["bus7_voltage:0", "bus7_voltage:1", "bus7_voltage:2"]
        assert renamed_prefault == pytest.approx(baseline_prefault, abs=1e-9)
        assert renamed_postfault == pytest.approx(baseline_postfault, abs=1e-9)

    def test_ieee3_output_group_can_be_pruned_to_active_power_channels(
        self, integration_ieee3_model
    ):
        baseline_job = build_fault_ready_ieee3_model(
            integration_ieee3_model,
            fault_end_time="2.7",
            fault_chg="0.01",
        ).runEMT()
        wait_for_completion(baseline_job)
        baseline_result = baseline_job.result
        baseline_names = baseline_result.getPlotChannelNames(1)
        baseline_p1_trace = baseline_result.getPlotChannelData(1, "#P1:0")

        working_model = build_fault_ready_ieee3_model(
            integration_ieee3_model,
            fault_end_time="2.7",
            fault_chg="0.01",
        )
        emt_job = next(
            job for job in working_model.jobs if job["rid"] == "function/CloudPSS/emtps"
        )
        pq_group = emt_job["args"]["output_channels"][1]
        pq_group["4"] = [
            component_id
            for component_id in pq_group["4"]
            if working_model.getComponentByKey(component_id).args.get("Name", "").startswith("#P")
        ]

        pruned_job = working_model.runEMT()
        wait_for_completion(pruned_job)
        pruned_result = pruned_job.result
        pruned_names = pruned_result.getPlotChannelNames(1)
        pruned_p1_trace = pruned_result.getPlotChannelData(1, "#P1:0")

        _, baseline_prefault_p1 = nearest_trace_value(baseline_p1_trace, 2.45)
        _, pruned_prefault_p1 = nearest_trace_value(pruned_p1_trace, 2.45)
        _, baseline_postfault_p1 = nearest_trace_value(baseline_p1_trace, 2.95)
        _, pruned_postfault_p1 = nearest_trace_value(pruned_p1_trace, 2.95)

        assert baseline_names == ["#P2:0", "#Q2:0", "#P1:0", "#Q1:0", "#P3:0", "#Q3:0"]
        assert pruned_names == ["#P2:0", "#P1:0", "#P3:0"]
        assert pruned_prefault_p1 == pytest.approx(baseline_prefault_p1, abs=1e-9)
        assert pruned_postfault_p1 == pytest.approx(baseline_postfault_p1, abs=1e-9)

    def test_ieee3_can_add_new_output_channel_for_existing_meter_signal(
        self, integration_ieee3_model
    ):
        baseline_job = build_prepared_ieee3_model(
            integration_ieee3_model,
            fault_end_time="2.7",
            sampling_freq="2000",
        ).runEMT()
        wait_for_completion(baseline_job)
        baseline_result = baseline_job.result
        baseline_names = baseline_result.getPlotChannelNames(2)
        baseline_trace = baseline_result.getPlotChannelData(2, "vac:0")

        working_model = build_prepared_ieee3_model(
            integration_ieee3_model,
            fault_end_time="2.7",
            sampling_freq="2000",
        )
        existing_channel = next(
            component
            for component in working_model.getAllComponents().values()
            if getattr(component, "definition", None)
            == "model/CloudPSS/_newChannel"
            and component.args.get("Name") == "vac"
        )
        new_channel = working_model.addComponent(
            "model/CloudPSS/_newChannel",
            "newChannel-bus7-voltage-copy",
            args={
                **existing_channel.args,
                "Name": "vac_copy",
                "Freq": {"source": "2000", "ɵexp": ""},
            },
            pins={"0": "#vac"},
            canvas=existing_channel.canvas,
            position={
                "x": existing_channel.position["x"] + 40,
                "y": existing_channel.position["y"],
            },
            size=existing_channel.size,
        )
        emt_job = next(
            job for job in working_model.jobs if job["rid"] == "function/CloudPSS/emtps"
        )
        emt_job["args"]["output_channels"][2]["4"].append(new_channel.id)
        emt_job["args"]["output_channels"][2]["1"] = 2000

        expanded_job = working_model.runEMT()
        wait_for_completion(expanded_job)
        expanded_result = expanded_job.result
        expanded_names = expanded_result.getPlotChannelNames(2)
        expanded_trace = expanded_result.getPlotChannelData(2, "vac_copy:0")

        _, baseline_prefault = nearest_trace_value(baseline_trace, 2.45)
        _, expanded_prefault = nearest_trace_value(expanded_trace, 2.45)
        _, baseline_postfault = nearest_trace_value(baseline_trace, 2.95)
        _, expanded_postfault = nearest_trace_value(expanded_trace, 2.95)

        assert baseline_names == ["vac:0", "vac:1", "vac:2"]
        assert expanded_names == [
            "vac:0",
            "vac:1",
            "vac:2",
            "vac_copy:0",
            "vac_copy:1",
            "vac_copy:2",
        ]
        assert expanded_prefault == pytest.approx(baseline_prefault, abs=1e-9)
        assert expanded_postfault == pytest.approx(baseline_postfault, abs=1e-9)

    def test_ieee3_can_add_new_voltage_meter_when_meter_bus_edge_is_injected(
        self, integration_ieee3_model
    ):
        baseline_job = build_prepared_ieee3_model(
            integration_ieee3_model,
            fault_end_time="2.7",
            sampling_freq="2000",
        ).runEMT()
        wait_for_completion(baseline_job)
        baseline_result = baseline_job.result
        baseline_names = baseline_result.getPlotChannelNames(2)
        baseline_trace = baseline_result.getPlotChannelData(2, "vac:0")

        working_model = build_prepared_ieee3_model(
            integration_ieee3_model,
            fault_end_time="2.7",
            sampling_freq="2000",
        )
        components = working_model.getAllComponents()
        existing_meter = next(
            component
            for component in components.values()
            if getattr(component, "definition", None)
            == "model/CloudPSS/_NewVoltageMeter"
        )
        existing_channel = next(
            component
            for component in components.values()
            if getattr(component, "definition", None)
            == "model/CloudPSS/_newChannel"
            and component.args.get("Name") == "vac"
        )
        bus7 = next(
            component
            for component in components.values()
            if getattr(component, "definition", None)
            == "model/CloudPSS/_newBus_3p"
            and component.args.get("Name") == "Bus7"
        )
        existing_edge = next(
            component
            for component in components.values()
            if getattr(component, "shape", None) == "diagram-edge"
            and component.source.get("cell") == existing_meter.id
            and component.target.get("cell") == bus7.id
        )

        new_meter = working_model.addComponent(
            "model/CloudPSS/_NewVoltageMeter",
            "newVoltageMeter-bus7-voltage-copy",
            args={"Dim": "3", "V": "#vac_added"},
            pins={"0": ""},
            canvas=existing_meter.canvas,
            position={
                "x": existing_meter.position["x"] + 90,
                "y": existing_meter.position["y"],
            },
            size=existing_meter.size,
        )
        new_channel = working_model.addComponent(
            "model/CloudPSS/_newChannel",
            "newChannel-bus7-voltage-added",
            args={
                **existing_channel.args,
                "Name": "vac_added",
                "Freq": {"source": "2000", "ɵexp": ""},
            },
            pins={"0": "#vac_added"},
            canvas=existing_channel.canvas,
            position={
                "x": existing_channel.position["x"] + 140,
                "y": existing_channel.position["y"],
            },
            size=existing_channel.size,
        )

        new_edge_id = f"edge_{new_meter.id}"
        new_edge = deepcopy(existing_edge.toJSON())
        new_edge["id"] = new_edge_id
        new_edge["source"] = {"cell": new_meter.id, "port": "0"}
        new_edge["target"] = deepcopy(existing_edge.target)
        new_edge["vertices"] = [
            {
                "x": existing_edge.vertices[0]["x"] + 45,
                "y": existing_edge.vertices[0]["y"],
            }
        ]
        new_edge["zIndex"] = min(
            getattr(existing_edge, "zIndex", -118),
            getattr(new_meter, "zIndex", 0),
            getattr(bus7, "zIndex", 0),
        ) - 1
        working_model.revision.getImplements().getDiagram().cells[new_edge_id] = Component(
            new_edge
        )

        emt_job = next(
            job for job in working_model.jobs if job["rid"] == "function/CloudPSS/emtps"
        )
        emt_job["args"]["output_channels"][2]["4"].append(new_channel.id)
        emt_job["args"]["output_channels"][2]["1"] = 2000

        expanded_job = working_model.runEMT()
        wait_for_completion(expanded_job)
        expanded_result = expanded_job.result
        expanded_names = expanded_result.getPlotChannelNames(2)
        expanded_trace = expanded_result.getPlotChannelData(2, "vac_added:0")

        _, baseline_prefault = nearest_trace_value(baseline_trace, 2.45)
        _, expanded_prefault = nearest_trace_value(expanded_trace, 2.45)
        _, baseline_postfault = nearest_trace_value(baseline_trace, 2.95)
        _, expanded_postfault = nearest_trace_value(expanded_trace, 2.95)

        assert baseline_names == ["vac:0", "vac:1", "vac:2"]
        assert expanded_names == [
            "vac:0",
            "vac:1",
            "vac:2",
            "vac_added:0",
            "vac_added:1",
            "vac_added:2",
        ]
        assert expanded_prefault == pytest.approx(baseline_prefault, abs=1e-9)
        assert expanded_postfault == pytest.approx(baseline_postfault, abs=1e-9)

    def test_ieee3_can_add_new_voltage_meter_to_bus2_and_match_bus_base_rms(
        self, integration_ieee3_model
    ):
        working_model = build_prepared_ieee3_model(
            integration_ieee3_model,
            fault_end_time="2.7",
            sampling_freq="2000",
        )
        components = working_model.getAllComponents()
        existing_meter = next(
            component
            for component in components.values()
            if getattr(component, "definition", None)
            == "model/CloudPSS/_NewVoltageMeter"
        )
        existing_channel = next(
            component
            for component in components.values()
            if getattr(component, "definition", None)
            == "model/CloudPSS/_newChannel"
            and component.args.get("Name") == "vac"
        )
        bus7 = next(
            component
            for component in components.values()
            if getattr(component, "definition", None)
            == "model/CloudPSS/_newBus_3p"
            and component.args.get("Name") == "Bus7"
        )
        bus2 = next(
            component
            for component in components.values()
            if getattr(component, "definition", None)
            == "model/CloudPSS/_newBus_3p"
            and component.args.get("Name") == "Bus2"
        )
        existing_edge = next(
            component
            for component in components.values()
            if getattr(component, "shape", None) == "diagram-edge"
            and component.source.get("cell") == existing_meter.id
            and component.target.get("cell") == bus7.id
        )

        plot_index, _, _ = add_voltage_meter_output_chain(
            working_model,
            bus_component=bus2,
            channel_template=existing_channel,
            signal_name="#bus2_added",
            channel_name="bus2_added",
            sampling_freq=2000,
            meter_label="newVoltageMeter-bus2-added",
            channel_label="newChannel-bus2-added",
            meter_position={"x": bus2.position["x"] + 15, "y": bus2.position["y"] + 100},
            channel_position={
                "x": existing_channel.position["x"] + 180,
                "y": existing_channel.position["y"],
            },
            meter_size=existing_meter.size,
            channel_size=existing_channel.size,
            edge_template=existing_edge,
            edge_vertex={"x": bus2.position["x"] - 10, "y": bus2.position["y"] + 40},
        )

        expanded_job = working_model.runEMT()
        wait_for_completion(expanded_job)
        expanded_result = expanded_job.result
        expanded_names = expanded_result.getPlotChannelNames(plot_index)
        expanded_trace = expanded_result.getPlotChannelData(plot_index, "bus2_added:0")
        measured_rms = trace_window_rms(expanded_trace, 2.42, 2.44)

        bus2_args = resolved_bus_args(working_model, "Bus2")
        expected_rms = bus2_args["V"] * bus2_args["VBase"] / math.sqrt(3)

        assert expanded_names == ["bus2_added:0", "bus2_added:1", "bus2_added:2"]
        assert measured_rms == pytest.approx(expected_rms, rel=0.01)

    def test_ieee39_can_add_new_voltage_meter_without_existing_meter_template(
        self, integration_model
    ):
        working_model = Model(deepcopy(integration_model.toJSON()))
        components = working_model.getAllComponents()
        bus37 = next(
            component
            for component in components.values()
            if getattr(component, "definition", None)
            == "model/CloudPSS/_newBus_3p"
            and component.args.get("Name") == "bus37"
        )
        channel_template = next(
            component
            for component in components.values()
            if getattr(component, "definition", None)
            == "model/CloudPSS/_newChannel"
        )

        plot_index, _, _ = add_voltage_meter_output_chain(
            working_model,
            bus_component=bus37,
            channel_template=channel_template,
            signal_name="#bus37_added",
            channel_name="bus37_added",
            sampling_freq=2000,
            meter_label="newVoltageMeter-bus37-added",
            channel_label="newChannel-bus37-added",
            meter_position={"x": bus37.position["x"] + 20, "y": bus37.position["y"] - 120},
            channel_position={"x": bus37.position["x"] + 150, "y": bus37.position["y"] - 120},
            edge_vertex={"x": bus37.position["x"] + 10, "y": bus37.position["y"] - 40},
        )

        expanded_job = working_model.runEMT()
        wait_for_completion(expanded_job)
        expanded_result = expanded_job.result
        expanded_names = expanded_result.getPlotChannelNames(plot_index)
        expanded_trace = expanded_result.getPlotChannelData(plot_index, "bus37_added:0")
        measured_rms = trace_window_rms(expanded_trace, 0.12, 0.14)

        bus37_args = resolved_bus_args(working_model, "bus37")
        expected_rms = bus37_args["V"] * bus37_args["VBase"] / math.sqrt(3)

        assert expanded_names == ["bus37_added:0", "bus37_added:1", "bus37_added:2"]
        assert measured_rms == pytest.approx(expected_rms, rel=0.02)

    @pytest.mark.slow_emt
    def test_ieee3_fault_study_summary_distinguishes_clearing_time_and_fault_severity(
        self, integration_ieee3_model
    ):
        module = load_module(
            EMT_FAULT_STUDY_EXAMPLE_PATH,
            "emt_fault_study_example_integration",
        )

        results = module.run_fault_study(integration_ieee3_model)
        by_name = {item["name"]: item for item in results}

        baseline = by_name["baseline"]["metrics"]
        delayed = by_name["delayed_clearing"]["metrics"]
        mild = by_name["mild_fault"]["metrics"]
        rows = module.build_summary_rows(results)
        rows_by_name = {row["scenario"]: row for row in rows}

        assert baseline["point_count"] == delayed["point_count"] == mild["point_count"] == 20001
        assert delayed["prefault_rms"] == pytest.approx(baseline["prefault_rms"], abs=1e-9)
        assert delayed["fault_rms"] == pytest.approx(baseline["fault_rms"], abs=1e-6)
        assert baseline["postfault_rms"] - delayed["postfault_rms"] > 10.0
        assert baseline["late_recovery_rms"] - delayed["late_recovery_rms"] > 15.0
        assert mild["fault_rms"] - baseline["fault_rms"] > 200.0
        assert mild["postfault_rms"] - baseline["postfault_rms"] > 8.0
        assert mild["prefault_rms"] == pytest.approx(baseline["prefault_rms"], abs=1e-9)
        assert rows_by_name["delayed_clearing"]["delta_fault_rms_vs_baseline"] == "0.000"
        assert float(rows_by_name["mild_fault"]["delta_fault_rms_vs_baseline"]) > 200.0

    @pytest.mark.slow_emt
    def test_ieee3_fault_severity_scan_orders_fault_drop_and_recovery_gap_by_chg(
        self, integration_ieee3_model
    ):
        module = load_module(
            EMT_FAULT_SEVERITY_SCAN_EXAMPLE_PATH,
            "emt_fault_severity_scan_example_integration",
        )

        results = module.run_fault_severity_scan(integration_ieee3_model)
        rows = module.build_summary_rows(results)
        report = module.build_conclusion_report(rows)
        rows_by_name = {row["scenario"]: row for row in rows}

        severe_fault_drop = float(rows_by_name["severe_fault"]["fault_drop_vs_prefault"])
        intermediate_fault_drop = float(rows_by_name["intermediate_fault"]["fault_drop_vs_prefault"])
        mild_fault_drop = float(rows_by_name["mild_fault"]["fault_drop_vs_prefault"])
        severe_post_gap = float(rows_by_name["severe_fault"]["postfault_gap_vs_prefault"])
        intermediate_post_gap = float(rows_by_name["intermediate_fault"]["postfault_gap_vs_prefault"])
        mild_post_gap = float(rows_by_name["mild_fault"]["postfault_gap_vs_prefault"])

        assert severe_fault_drop > intermediate_fault_drop > mild_fault_drop
        assert severe_post_gap > intermediate_post_gap > mild_post_gap
        assert all(finding["supported"] for finding in report["findings"])

    @pytest.mark.slow_emt
    def test_ieee3_fault_clearing_scan_orders_fixed_deadline_recovery_gaps_by_fe(
        self, integration_ieee3_model
    ):
        module = load_module(
            EMT_FAULT_CLEARING_SCAN_EXAMPLE_PATH,
            "emt_fault_clearing_scan_example_integration",
        )

        results = module.run_fault_clearing_scan(integration_ieee3_model)
        rows = module.build_summary_rows(results)
        report = module.build_conclusion_report(rows)

        gap_295 = [float(row["gap_295"]) for row in rows]
        gap_300 = [float(row["gap_300"]) for row in rows]

        assert all(left < right for left, right in zip(gap_295, gap_295[1:]))
        assert all(left < right for left, right in zip(gap_300, gap_300[1:]))
        assert all(finding["supported"] for finding in report["findings"])

    @pytest.mark.slow_emt
    def test_ieee3_measurement_workflow_can_add_prune_and_use_channels_together(
        self, integration_ieee3_model
    ):
        module = load_module(
            EMT_MEASUREMENT_WORKFLOW_EXAMPLE_PATH,
            "emt_measurement_workflow_example_integration",
        )

        summary = module.run_measurement_workflow(integration_ieee3_model)
        report = module.build_conclusion_report(summary)

        assert abs(summary["bus2_prefault_rms"] - summary["bus2_expected_rms"]) / summary["bus2_expected_rms"] < 0.02
        assert summary["retained_p_channels"] == ["#P2:0", "#P1:0", "#P3:0"]
        assert "#P1:0" in summary["retained_p_channels"]
        assert summary["bus7_prefault_rms"] - summary["bus7_fault_rms"] > 10.0 * (
            summary["bus2_prefault_rms"] - summary["bus2_fault_rms"]
        )
        assert summary["bus7_prefault_rms"] - summary["bus7_postfault_rms"] > 10.0 * (
            summary["bus2_prefault_rms"] - summary["bus2_postfault_rms"]
        )
        assert summary["p1_fault_avg"] > summary["p1_prefault_avg"]
        assert summary["p1_postfault_avg"] < summary["p1_fault_avg"]
        assert all(item["supported"] for item in report["findings"])

    @pytest.mark.slow_emt
    def test_ieee3_branch_n1_security_scan_ranks_representative_outages(
        self, integration_ieee3_model
    ):
        module = load_module(
            EMT_N1_SECURITY_SCREENING_EXAMPLE_PATH,
            "emt_n1_security_screening_example_integration",
        )

        baseline, results = module.run_branch_n1_security_scan(
            integration_ieee3_model,
            candidate_branch_ids=["canvas_0_1096", "canvas_0_1074", "canvas_0_1071"],
        )
        rows = module.build_summary_rows(baseline, results)
        digest = module.build_screening_digest(baseline, results)
        report = module.build_conclusion_report(baseline, results, digest)
        by_id = {item["branch_id"]: item for item in results}
        rows_by_id = {row["branch_id"]: row for row in rows}

        assert baseline["worst_postfault_gap"] > 10.0
        assert baseline["monitored_buses"]["Bus2"]["postfault_gap_vs_prefault"] < 0.5

        assert by_id["canvas_0_1096"]["generator_support_lost"]
        assert by_id["canvas_0_1096"]["worst_postfault_gap"] > baseline["worst_postfault_gap"] + 1.0
        assert max(abs(value) for value in by_id["canvas_0_1096"]["p1_metrics"].values()) < 1.0

        assert by_id["canvas_0_1074"]["worst_postfault_gap"] > by_id["canvas_0_1071"]["worst_postfault_gap"] + 5.0
        assert by_id["canvas_0_1071"]["worst_postfault_gap"] < 1.5
        assert by_id["canvas_0_1071"]["worst_late_gap"] < 0.5
        assert max(
            item["monitored_buses"]["Bus2"]["postfault_gap_vs_prefault"] for item in results
        ) < 0.5

        assert digest["top_case"]["branch_id"] == "canvas_0_1096"
        assert digest["top_line_case"]["branch_id"] == "canvas_0_1074"
        assert digest["mildest_case"]["branch_id"] == "canvas_0_1071"
        assert rows_by_id["canvas_0_1096"]["delta_worst_postfault_gap_vs_baseline"].startswith("+")
        assert rows_by_id["canvas_0_1071"]["delta_worst_postfault_gap_vs_baseline"].startswith("-")
        assert all(item["supported"] for item in report["findings"])

    @pytest.mark.slow_emt
    def test_ieee3_research_report_wrapper_aggregates_live_sections_into_markdown(
        self, integration_ieee3_model, tmp_path
    ):
        module = load_module(
            EMT_RESEARCH_REPORT_EXAMPLE_PATH,
            "emt_research_report_example_integration",
        )

        sections = module.build_report_sections(integration_ieee3_model)
        report_text = module.build_markdown_report(integration_ieee3_model.rid, sections)
        export_path = tmp_path / "emt-research-report.md"
        module.export_report(report_text, export_path)

        assert set(sections.keys()) == {
            "fault_study",
            "fault_clearing_scan",
            "fault_severity_scan",
            "measurement_workflow",
        }
        assert all(item["supported"] for item in sections["fault_study"]["report"]["findings"])
        assert all(item["supported"] for item in sections["fault_clearing_scan"]["report"]["findings"])
        assert all(item["supported"] for item in sections["fault_severity_scan"]["report"]["findings"])
        assert all(item["supported"] for item in sections["measurement_workflow"]["report"]["findings"])
        assert "# CloudPSS EMT Research Report" in report_text
        assert "## Fault Study Comparison" in report_text
        assert "## Fault Clearing Scan" in report_text
        assert "## Fault Severity Scan" in report_text
        assert "## Measurement Workflow" in report_text
        assert "validated ordinary-cloud EMT studies on IEEE3" in report_text
        assert export_path.read_text(encoding="utf-8") == report_text + "\n"

    @pytest.mark.slow_emt
    def test_ieee3_n1_security_report_wrapper_exports_live_representative_markdown(
        self, integration_ieee3_model, tmp_path
    ):
        module = load_module(
            EMT_N1_SECURITY_REPORT_EXAMPLE_PATH,
            "emt_n1_security_report_example_integration",
        )

        sections = module.build_report_sections(
            integration_ieee3_model,
            use_all_discovered=False,
            include_transformers=True,
            limit=None,
        )
        report_text = module.build_markdown_report(
            integration_ieee3_model.rid,
            sections,
            use_all_discovered=False,
        )
        export_path = tmp_path / "emt-n1-security-report.md"
        module.export_report(report_text, export_path)

        digest = sections["digest"]

        assert digest["total_cases"] == 3
        assert digest["top_case"]["branch_name"] == "Trans1"
        assert digest["top_line_case"]["branch_name"] == "tline4"
        assert digest["mildest_case"]["branch_name"] == "tline6"
        assert all(item["supported"] for item in sections["conclusion_report"]["findings"])
        assert "# CloudPSS EMT N-1 Security Report" in report_text
        assert "validated representative IEEE3 N-1 subset" in report_text
        assert "## Representative Cases" in report_text
        assert "## Ranked Screening Table" in report_text
        assert "Trans1" in report_text
        assert "tline4" in report_text
        assert "tline6" in report_text
        assert export_path.read_text(encoding="utf-8") == report_text + "\n"

    @pytest.mark.slow_emt
    def test_ieee3_n1_full_report_wrapper_exports_live_full_scan_markdown(
        self, integration_ieee3_model, tmp_path
    ):
        module = load_module(
            EMT_N1_FULL_REPORT_EXAMPLE_PATH,
            "emt_n1_full_report_example_integration",
        )

        sections = module.build_full_report_sections(
            integration_ieee3_model,
            include_transformers=True,
            limit=None,
        )
        report_text = module.build_markdown_report(
            integration_ieee3_model.rid,
            sections,
            include_transformers=True,
        )
        export_path = tmp_path / "emt-n1-full-report.md"
        module.export_report(report_text, export_path)

        digest = sections["digest"]

        assert digest["total_cases"] == 9
        assert digest["top_case"]["branch_name"] == "Trans1"
        assert digest["top_line_case"]["branch_name"] == "tline4"
        assert digest["mildest_case"]["branch_name"] == "tline6"
        assert all(item["supported"] for item in sections["conclusion_report"]["findings"])
        assert "# CloudPSS EMT N-1 Full Screening Report" in report_text
        assert "full discovered IEEE3 lines + transformers subset" in report_text
        assert "## Severity Distribution" in report_text
        assert "## Full Ranked Table" in report_text
        assert "Trans1" in report_text
        assert "tline4" in report_text
        assert "tline6" in report_text
        assert export_path.read_text(encoding="utf-8") == report_text + "\n"
