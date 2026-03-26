"""
Add a voltage meter -> output channel chain for a `_newBus_3p` bus.

Run with: python examples/basic/emt_voltage_meter_chain_example.py
Prerequisite: a valid CloudPSS token stored in .cloudpss_token

This example is intentionally narrow:
- it only supports `_newBus_3p` bus components
- it prepares a local working copy first
- it injects a `diagram-edge` because the current SDK exposes no public addEdge API
- it does not claim universal compatibility for arbitrary EMT models
"""

from copy import deepcopy
from pathlib import Path
import os
import sys
import uuid

from cloudpss import Model, setToken
from cloudpss.model.implements.component import Component


DEFAULT_MODEL_SOURCE = "model/holdme/IEEE3"
DEFAULT_WORKING_COPY = "examples/basic/emt-voltage-meter-working-copy.yaml"
DEFAULT_PREPARED_COPY = "examples/basic/emt-voltage-meter-prepared.yaml"


def load_token():
    """Read the CloudPSS token from the project root."""
    token_path = Path(".cloudpss_token")
    if not token_path.exists():
        print("错误: 未找到 .cloudpss_token 文件")
        print("请先把 CloudPSS API token 写入项目根目录的 .cloudpss_token")
        sys.exit(1)
    return token_path.read_text().strip()


def load_model_from_source(source):
    """Load a model from local YAML/JSON or a cloud RID."""
    candidate = Path(source).expanduser()
    file_like = candidate.suffix.lower() in {".yaml", ".yml", ".json"}

    if candidate.exists():
        return Model.load(str(candidate))
    if file_like:
        raise FileNotFoundError(f"未找到本地模型文件: {candidate}")
    return Model.fetch(source)


def suggest_working_copy_path(source):
    """Avoid overwriting a local source file by default."""
    candidate = Path(source).expanduser()
    if candidate.exists() and candidate.suffix.lower() in {".yaml", ".yml", ".json"}:
        return str(candidate.with_name(f"{candidate.stem}-branch{candidate.suffix}"))
    return DEFAULT_WORKING_COPY


def create_local_working_copy(model, export_path):
    """Persist a local-only branch before any topology edits."""
    Model.dump(model, export_path, compress=None)
    return Model.load(export_path), export_path


def find_bus_component(model, bus_name):
    """Locate a three-phase bus by its Name argument."""
    components = model.getAllComponents()
    return next(
        component
        for component in components.values()
        if getattr(component, "definition", None) == "model/CloudPSS/_newBus_3p"
        and component.args.get("Name") == bus_name
    )


def find_channel_template(model):
    """Pick an existing output channel as the argument template."""
    components = model.getAllComponents()
    return next(
        component
        for component in components.values()
        if getattr(component, "definition", None) == "model/CloudPSS/_newChannel"
    )


def find_voltage_meter_edge_template(model):
    """Reuse a working meter -> bus edge when the model already has one."""
    components = list(model.getAllComponents().values())
    voltage_meters = [
        component
        for component in components
        if getattr(component, "definition", None) == "model/CloudPSS/_NewVoltageMeter"
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
    """Fallback edge scaffold for `_newBus_3p` when no template is available."""
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
            "anchor": {"args": {"dx": "-20%", "dy": "0%", "rotate": True}, "name": "center"},
            "cell": bus_component.id,
            "port": "0",
            "selector": "> path:nth-child(2)",
        },
        "vertices": [edge_vertex] if edge_vertex is not None else [],
        "zIndex": min(getattr(meter_component, "zIndex", 0), getattr(bus_component, "zIndex", 0)) - 1,
    }


def add_voltage_meter_chain(
    model,
    bus_name,
    signal_name,
    channel_name,
    sampling_freq=2000,
):
    """
    Add `_NewVoltageMeter` + `_newChannel` + `diagram-edge` for one `_newBus_3p` bus.

    Returns a dict describing the created chain.
    """
    if not signal_name.startswith("#"):
        raise ValueError("signal_name must start with '#'")
    if channel_name.startswith("#"):
        raise ValueError("channel_name must not start with '#'")

    bus_component = find_bus_component(model, bus_name)
    channel_template = find_channel_template(model)
    meter_template, edge_template = find_voltage_meter_edge_template(model)

    meter_size = meter_template.size if meter_template is not None else {"width": 30, "height": 50}
    meter_position = {
        "x": bus_component.position["x"] + 20,
        "y": bus_component.position["y"] - 120,
    }
    channel_position = {
        "x": bus_component.position["x"] + 150,
        "y": bus_component.position["y"] - 120,
    }

    new_meter = model.addComponent(
        "model/CloudPSS/_NewVoltageMeter",
        f"newVoltageMeter-{channel_name}",
        args={"Dim": "3", "V": signal_name},
        pins={"0": ""},
        canvas=bus_component.canvas,
        position=meter_position,
        size=meter_size,
    )
    new_channel = model.addComponent(
        "model/CloudPSS/_newChannel",
        f"newChannel-{channel_name}",
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
    if edge_template is not None:
        new_edge = deepcopy(edge_template.toJSON())
        new_edge["id"] = f"edge_{uuid.uuid4().hex[:8]}"
        new_edge["source"] = {"cell": new_meter.id, "port": "0"}
        new_edge["target"] = deepcopy(edge_template.target)
        new_edge["target"]["cell"] = bus_component.id
        new_edge["vertices"] = [edge_vertex]
    else:
        new_edge = build_generic_bus_edge(new_meter, bus_component, edge_vertex)
    model.revision.getImplements().getDiagram().cells[new_edge["id"]] = Component(new_edge)

    emt_job = next(job for job in model.jobs if job["rid"] == "function/CloudPSS/emtps")
    emt_job["args"]["output_channels"].append(
        {
            "0": f"{channel_name}_group",
            "1": int(sampling_freq),
            "2": "compressed",
            "3": 0,
            "4": [new_channel.id],
        }
    )
    return {
        "bus": bus_component,
        "meter": new_meter,
        "channel": new_channel,
        "edge_id": new_edge["id"],
        "output_group_index": len(emt_job["args"]["output_channels"]) - 1,
        "used_edge_template": edge_template is not None,
    }


def save_prepared_copy(model, export_path):
    """Persist the prepared local branch."""
    Model.dump(model, export_path, compress=None)
    return export_path


def main():
    """Prepare a local study branch with one new bus-voltage output chain."""
    print("CloudPSS SDK - `_newBus_3p` 电压量测链准备示例")
    print("=" * 60)

    setToken(load_token())
    print("Token 已设置")

    source = input(
        "请输入云端模型 RID 或本地 YAML，直接回车使用 "
        f"[{DEFAULT_MODEL_SOURCE}]: "
    ).strip() or DEFAULT_MODEL_SOURCE
    model = load_model_from_source(source)

    working_copy_path = (
        input(
            "请输入本地工作副本路径，直接回车使用 "
            f"[{suggest_working_copy_path(source)}]: "
        ).strip()
        or suggest_working_copy_path(source)
    )
    working_model, _ = create_local_working_copy(model, working_copy_path)

    bus_name = input("请输入目标母线 Name [Bus7]: ").strip() or "Bus7"
    signal_name = input("请输入量测信号名 [#bus_voltage_added]: ").strip() or "#bus_voltage_added"
    channel_name = input("请输入输出通道名 [bus_voltage_added]: ").strip() or "bus_voltage_added"
    sampling_freq = input("请输入采样频率 [2000]: ").strip() or "2000"

    result = add_voltage_meter_chain(
        working_model,
        bus_name=bus_name,
        signal_name=signal_name,
        channel_name=channel_name,
        sampling_freq=int(sampling_freq),
    )

    prepared_copy_path = (
        input(
            "请输入准备后副本保存路径，直接回车使用 "
            f"[{DEFAULT_PREPARED_COPY}]: "
        ).strip()
        or DEFAULT_PREPARED_COPY
    )
    save_prepared_copy(working_model, prepared_copy_path)

    print("\n已新增电压量测链:")
    print(f"- bus: {result['bus'].args['Name']} ({result['bus'].id})")
    print(f"- meter: {result['meter'].id}")
    print(f"- channel: {result['channel'].args['Name']} ({result['channel'].id})")
    print(f"- edge: {result['edge_id']}")
    print(f"- output group index: {result['output_group_index']}")
    print(f"- edge mode: {'template clone' if result['used_edge_template'] else 'generic scaffold'}")
    print(f"- saved local branch: {prepared_copy_path}")
    print("\n边界说明:")
    print("- 当前示例只支持 `_newBus_3p` 母线")
    print("- 当前 SDK 无公开 `addEdge()`，因此这里直接注入 `diagram-edge`")
    print("- 该脚本用于研究分支准备，不代表任意模型都可无条件复用")
    print("- 下一步建议用真实 EMT 运行和 RMS 判据继续校核")


if __name__ == "__main__":
    main()
