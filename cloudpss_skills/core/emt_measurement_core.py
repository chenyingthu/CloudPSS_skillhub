"""
Shared helpers for adding EMT measurement output chains.
"""

from copy import deepcopy
import math
from typing import Any, Callable, Dict, List, Optional, Tuple
import uuid

from cloudpss_skills.core.utils import calculate_voltage_average, get_time_index


CHANNEL_DEFINITION = "model/CloudPSS/_newChannel"
VOLTAGE_METER_DEFINITION = "model/CloudPSS/_NewVoltageMeter"
EMT_JOB_RID = "function/CloudPSS/emtps"


def find_channel_template(model):
    channels = model.getComponentsByRid(CHANNEL_DEFINITION)
    if not channels:
        raise ValueError("模型中不存在可复用的 _newChannel 模板")
    return next(iter(channels.values()))


def find_voltage_meter_edge_template(model):
    components = list(model.getAllComponents().values())
    voltage_meters = [
        component
        for component in components
        if getattr(component, "definition", None) == VOLTAGE_METER_DEFINITION
    ]
    buses = {
        component.id: component
        for component in components
        if getattr(component, "definition", None) == "model/CloudPSS/_newBus_3p"
    }
    for edge in components:
        if getattr(edge, "shape", None) != "diagram-edge":
            continue
        source = getattr(edge, "source", {})
        target = getattr(edge, "target", {})
        source_meter = next(
            (meter for meter in voltage_meters if meter.id == source.get("cell")),
            None,
        )
        target_bus = buses.get(target.get("cell"))
        if source_meter is not None and target_bus is not None:
            return source_meter, edge
    return None, None


def build_generic_bus_edge(meter_component, bus_component, edge_vertex=None):
    return {
        "id": f"edge_{uuid.uuid4().hex[:8]}",
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
        "source": {"cell": meter_component.id, "port": "0"},
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
            getattr(meter_component, "zIndex", 0), getattr(bus_component, "zIndex", 0)
        )
        - 1,
    }


def add_voltage_meter_output_chain(
    working_model,
    *,
    bus_component,
    signal_name: str,
    channel_name: str,
    sampling_freq: int,
    meter_label: str,
    channel_label: str,
    meter_position: Optional[Dict[str, float]] = None,
    channel_position: Optional[Dict[str, float]] = None,
):
    from cloudpss.model.implements.component import Component

    channel_template = find_channel_template(working_model)
    meter_template, edge_template = find_voltage_meter_edge_template(working_model)

    meter_position = meter_position or {
        "x": bus_component.position["x"] + 20,
        "y": bus_component.position["y"] - 120,
    }
    channel_position = channel_position or {
        "x": bus_component.position["x"] + 150,
        "y": bus_component.position["y"] - 120,
    }

    new_meter = working_model.addComponent(
        VOLTAGE_METER_DEFINITION,
        meter_label,
        args={"Dim": "3", "V": signal_name},
        pins={"0": ""},
        canvas=bus_component.canvas,
        position=meter_position,
        size=meter_template.size
        if meter_template is not None
        else {"width": 30, "height": 50},
    )
    new_channel = working_model.addComponent(
        CHANNEL_DEFINITION,
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
        size=channel_template.size,
    )

    edge_vertex = {
        "x": bus_component.position["x"] + 10,
        "y": bus_component.position["y"] - 40,
    }
    new_edge_id = f"edge_{uuid.uuid4().hex[:8]}"
    if edge_template is not None:
        new_edge = deepcopy(edge_template.toJSON())
        new_edge["id"] = new_edge_id
        new_edge["source"] = {"cell": new_meter.id, "port": "0"}
        new_edge["target"] = deepcopy(edge_template.target)
        new_edge["target"]["cell"] = bus_component.id
        new_edge["vertices"] = [edge_vertex]
    else:
        new_edge = build_generic_bus_edge(new_meter, bus_component, edge_vertex)
    working_model.revision.getImplements().getDiagram().cells[new_edge_id] = Component(
        new_edge
    )

    emt_job = next(job for job in working_model.jobs if job["rid"] == EMT_JOB_RID)
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


def find_bus_component(model, bus_name: str) -> Optional[Any]:
    """
    Find a bus component by name using multiple matching strategies.

    Strategies:
    1. Exact match (case insensitive)
    2. Number extraction: BUS_1 matches newBus_3p-1
    3. Partial match: bus1 matches newbus3p1

    Args:
        model: The model to search
        bus_name: The bus name to find

    Returns:
        The bus component if found, None otherwise
    """
    components = list(model.getAllComponents().values())
    buses = {
        c.id: c
        for c in components
        if getattr(c, "definition", None) == "model/CloudPSS/_newBus_3p"
    }

    bus_name_lower = bus_name.lower()

    for bus_id, bus_comp in buses.items():
        bus_label = getattr(bus_comp, "label", "") or ""
        bus_label_lower = bus_label.lower()

        if bus_name_lower == bus_label_lower:
            return bus_comp

        bus_num = bus_name_lower.replace("bus_", "").replace("_", "-")
        if bus_num in bus_label_lower:
            return bus_comp

        if bus_name_lower.replace("_", "") in bus_label_lower.replace("_", "").replace(
            "-", ""
        ):
            return bus_comp

    if buses:
        return next(iter(buses.values()))
    return None


def ensure_voltage_meter(
    working_model,
    bus_name: str,
    trace_name: str,
    sampling_freq: int = 12800,
    log_func: Optional[Callable[[str], None]] = None,
) -> str:
    """
    Ensure the model has a voltage measurement channel for the target bus.

    If the channel already exists, this is a no-op.
    Otherwise, adds a voltage meter -> channel -> output chain.

    Args:
        working_model: The working copy model to modify
        bus_name: Target bus name (e.g., "BUS_1", "newBus_3p-1")
        trace_name: Expected trace name (e.g., "vac:0")
        sampling_freq: Sampling frequency in Hz
        log_func: Optional logging function

    Returns:
        The trace name (e.g., "vac:0")
    """
    channel_base_name = trace_name.split(":")[0]

    target_bus = find_bus_component(working_model, bus_name)
    if target_bus is None:
        raise ValueError(f"未找到目标母线: {bus_name}")

    signal_name = f"#{channel_base_name}"
    meter_label = f"VM-{bus_name}"
    channel_label = f"CH-{channel_base_name}"

    add_voltage_meter_output_chain(
        working_model,
        bus_component=target_bus,
        signal_name=signal_name,
        channel_name=channel_base_name,
        sampling_freq=sampling_freq,
        meter_label=meter_label,
        channel_label=channel_label,
    )

    if log_func:
        log_func(
            f"已添加电压表 {meter_label} 到母线 {getattr(target_bus, 'label', bus_name)}，通道 {channel_base_name}"
        )

    return trace_name


def add_bus_voltage_measurements(
    working_model,
    *,
    buses: List[Dict[str, Any]],
    sampling_freq: int,
    signal_name_builder: Callable[[Dict[str, Any]], str],
    channel_name_builder: Callable[[Dict[str, Any]], str],
    meter_label_builder: Callable[[Dict[str, Any]], str],
    channel_label_builder: Callable[[Dict[str, Any]], str],
) -> List[Dict[str, Any]]:
    measurement_channels: List[Dict[str, Any]] = []
    for bus in buses:
        bus_component = working_model.getComponentByKey(bus["key"])
        channel_name = channel_name_builder(bus)
        plot_index, _meter, _channel = add_voltage_meter_output_chain(
            working_model,
            bus_component=bus_component,
            signal_name=signal_name_builder(bus),
            channel_name=channel_name,
            sampling_freq=int(sampling_freq),
            meter_label=meter_label_builder(bus),
            channel_label=channel_label_builder(bus),
        )
        measurement_channels.append(
            {
                "bus_label": bus.get("label", ""),
                "trace_name": f"{channel_name}:0",
                "trace_prefix": channel_name,
                "plot_index": plot_index,
            }
        )
    return measurement_channels


def get_three_phase_rms_trace(
    result: Any, *, plot_index: int, trace_prefix: str
) -> Optional[Tuple[List[float], List[float]]]:
    phase_traces = []
    for phase in range(3):
        trace = result.getPlotChannelData(plot_index, f"{trace_prefix}:{phase}")
        if not trace:
            return None
        phase_traces.append(trace)

    time_values = phase_traces[0].get("x", [])
    phase_values = [trace.get("y", []) for trace in phase_traces]
    if not time_values or any(not values for values in phase_values):
        return None

    sample_count = min(len(time_values), *(len(values) for values in phase_values))
    if sample_count == 0:
        return None

    time_values = time_values[:sample_count]
    vrms = [
        math.sqrt(
            (
                phase_values[0][idx] ** 2
                + phase_values[1][idx] ** 2
                + phase_values[2][idx] ** 2
            )
            / 3.0
        )
        for idx in range(sample_count)
    ]
    return time_values, vrms


def average_trace_in_window(
    time_values: List[float], values: List[float], *, start: float, end: float
) -> float:
    start_idx = get_time_index(time_values, start)
    end_idx = get_time_index(time_values, end)
    return calculate_voltage_average(values, start_idx, end_idx)


def compute_windowed_dv_metrics(
    result: Any,
    *,
    disturbance_time: float,
    measurement_channels: List[Dict[str, Any]],
    dv_judge_criteria: Optional[List[List[float]]] = None,
) -> Dict[str, List[float]]:
    criteria = dv_judge_criteria or [[0.1, 3.0, 0.75, 1.25], [3.0, 999.0, 0.95, 1.05]]
    dv_up_list: List[float] = []
    dv_down_list: List[float] = []

    for channel in measurement_channels:
        rms_trace = get_three_phase_rms_trace(
            result,
            plot_index=channel["plot_index"],
            trace_prefix=channel["trace_prefix"],
        )
        if rms_trace is None:
            continue
        time_values, vrms = rms_trace

        steady_voltage = average_trace_in_window(
            time_values,
            vrms,
            start=disturbance_time - 0.5,
            end=disturbance_time,
        )
        if steady_voltage <= 0:
            continue

        window_dv_up = []
        window_dv_down = []
        for criterion in criteria:
            if len(criterion) != 4:
                continue
            start_offset, end_offset, lower_ratio, upper_ratio = criterion
            start_idx = get_time_index(time_values, disturbance_time + start_offset)
            end_idx = get_time_index(time_values, disturbance_time + end_offset)
            window = vrms[start_idx:end_idx] if end_idx > start_idx else []
            if not window:
                continue
            window_dv_up.append(upper_ratio * steady_voltage - max(window))
            window_dv_down.append(min(window) - lower_ratio * steady_voltage)

        if not window_dv_up or not window_dv_down:
            continue

        dv_up_list.append(min(window_dv_up))
        dv_down_list.append(min(window_dv_down))

    return {"dv_up": dv_up_list, "dv_down": dv_down_list}


def compute_vsi_from_voltage_channels(
    result: Any,
    *,
    test_buses: List[Dict[str, Any]],
    measurement_channels: List[Dict[str, Any]],
    q_base: float,
    start_time: float,
    interval: float,
    duration: float,
) -> Dict[str, Any]:
    vsi_i = {}
    vsi_ij = {}
    unsupported_buses = []

    for index, bus in enumerate(test_buses):
        bus_label = bus["label"]
        inject_start = start_time + index * interval
        inject_end = inject_start + duration
        before_start = inject_start - duration

        vsi_values = []
        for channel in measurement_channels:
            trace = result.getPlotChannelData(
                channel["plot_index"], channel["trace_name"]
            )
            if not trace:
                continue
            time_values = trace.get("x", [])
            values = trace.get("y", [])
            if not time_values or not values:
                continue

            voltage_before = average_trace_in_window(
                time_values, values, start=before_start, end=inject_start
            )
            voltage_after = average_trace_in_window(
                time_values, values, start=inject_start, end=inject_end
            )

            injected_q = abs(q_base)
            if injected_q == 0:
                continue

            vsi = abs(voltage_before - voltage_after) / injected_q
            vsi_values.append(vsi)

            vsi_ij.setdefault(bus_label, {})[channel["bus_label"]] = vsi

        if vsi_values:
            vsi_i[bus_label] = sum(vsi_values) / len(vsi_values)
        else:
            unsupported_buses.append(bus_label)

    return {"vsi_i": vsi_i, "vsi_ij": vsi_ij, "unsupported_buses": unsupported_buses}
