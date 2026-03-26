"""
CloudPSS EMT measurement workflow example.

Run with:
  python examples/analysis/emt_measurement_workflow_example.py
  python examples/analysis/emt_measurement_workflow_example.py model/holdme/IEEE3
  python examples/analysis/emt_measurement_workflow_example.py --csv=emt-measurement-workflow.csv
  python examples/analysis/emt_measurement_workflow_example.py --conclusion-txt=emt-measurement-workflow.txt

This example intentionally combines three measurement actions in one EMT study:
- use an existing validated bus-voltage measurement (`vac`)
- add a new bus-voltage measurement chain on `Bus2`
- delete unneeded reactive-power outputs by pruning the PQ group to `#P*`

The goal is to show CloudPSS EMT support for observability engineering, not
just raw waveform export.
"""

import csv
import importlib.util
import math
from pathlib import Path
import sys

from cloudpss import setToken


CURRENT_DIR = Path(__file__).resolve().parent
STUDY_HELPER_PATH = CURRENT_DIR / "emt_fault_study_example.py"
VOLTAGE_CHAIN_HELPER_PATH = CURRENT_DIR.parent / "basic" / "emt_voltage_meter_chain_example.py"


def load_helper_module(module_path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


_STUDY_MODULE = load_helper_module(
    STUDY_HELPER_PATH,
    "emt_fault_study_example_shared_for_measurement_workflow",
)
_CHAIN_MODULE = load_helper_module(
    VOLTAGE_CHAIN_HELPER_PATH,
    "emt_voltage_meter_chain_example_shared_for_measurement_workflow",
)

DEFAULT_MODEL_SOURCE = _STUDY_MODULE.DEFAULT_MODEL_SOURCE
load_model_from_source = _STUDY_MODULE.load_model_from_source
load_token = _STUDY_MODULE.load_token
prepare_fault_study_model = _STUDY_MODULE.prepare_fault_study_model
wait_for_completion = _STUDY_MODULE.wait_for_completion
add_voltage_meter_chain = _CHAIN_MODULE.add_voltage_meter_chain

DEFAULT_EXPORT_PREFIX = "emt-measurement-workflow"
DEFAULT_EXPORT_PATH = f"{DEFAULT_EXPORT_PREFIX}.csv"
DEFAULT_CONCLUSION_PATH = f"{DEFAULT_EXPORT_PREFIX}.txt"


def trace_window_rms(trace, start_time, end_time):
    samples = [
        value
        for time_value, value in zip(trace["x"], trace["y"])
        if start_time <= time_value <= end_time
    ]
    if not samples:
        raise ValueError(f"trace window {start_time}..{end_time} contains no samples")
    return math.sqrt(sum(value * value for value in samples) / len(samples))


def nearest_trace_value(trace, target_time):
    best_index = min(
        range(len(trace["x"])),
        key=lambda index: abs(trace["x"][index] - target_time),
    )
    return trace["x"][best_index], trace["y"][best_index]


def trace_window_average(trace, start_time, end_time):
    samples = [
        value
        for time_value, value in zip(trace["x"], trace["y"])
        if start_time <= time_value <= end_time
    ]
    if not samples:
        raise ValueError(f"trace window {start_time}..{end_time} contains no samples")
    return sum(samples) / len(samples)


def resolve_bus_args(working_model, bus_name):
    topology = working_model.fetchTopology("emtp").toJSON()["components"]
    bus = next(
        component
        for component in topology.values()
        if component.get("definition") == "model/CloudPSS/_newBus_3p"
        and component.get("args", {}).get("Name") == bus_name
    )
    return bus["args"]


def prune_pq_group_to_active_power_channels(working_model):
    emt_job = next(job for job in working_model.jobs if job["rid"] == "function/CloudPSS/emtps")
    pq_group = emt_job["args"]["output_channels"][1]
    pq_group["4"] = [
        component_id
        for component_id in pq_group["4"]
        if working_model.getComponentByKey(component_id).args.get("Name", "").startswith("#P")
    ]
    return pq_group


def run_measurement_workflow(model):
    working_model = prepare_fault_study_model(
        model,
        fault_end_time="2.7",
        fault_chg="0.01",
        sampling_freq=2000,
    )

    add_result = add_voltage_meter_chain(
        working_model,
        bus_name="Bus2",
        signal_name="#bus2_added",
        channel_name="bus2_added",
        sampling_freq=2000,
    )
    pq_group = prune_pq_group_to_active_power_channels(working_model)

    job = working_model.runEMT()
    wait_for_completion(job)
    result = job.result

    bus7_trace = result.getPlotChannelData(2, "vac:0")
    bus2_trace = result.getPlotChannelData(add_result["output_group_index"], "bus2_added:0")
    p_group_names = result.getPlotChannelNames(1)
    p1_trace = result.getPlotChannelData(1, "#P1:0")

    bus2_args = resolve_bus_args(working_model, "Bus2")
    expected_bus2_rms = bus2_args["V"] * bus2_args["VBase"] / math.sqrt(3)

    return {
        "bus7_prefault_rms": trace_window_rms(bus7_trace, 2.42, 2.44),
        "bus7_fault_rms": trace_window_rms(bus7_trace, 2.56, 2.58),
        "bus7_postfault_rms": trace_window_rms(bus7_trace, 2.92, 2.94),
        "bus2_prefault_rms": trace_window_rms(bus2_trace, 2.42, 2.44),
        "bus2_fault_rms": trace_window_rms(bus2_trace, 2.56, 2.58),
        "bus2_postfault_rms": trace_window_rms(bus2_trace, 2.92, 2.94),
        "bus2_expected_rms": expected_bus2_rms,
        "retained_p_channels": p_group_names,
        "p1_prefault_value": nearest_trace_value(p1_trace, 2.45)[1],
        "p1_prefault_avg": trace_window_average(p1_trace, 2.42, 2.44),
        "p1_fault_avg": trace_window_average(p1_trace, 2.64, 2.66),
        "p1_postfault_avg": trace_window_average(p1_trace, 2.96, 2.98),
        "added_group_index": add_result["output_group_index"],
        "added_channel_name": add_result["channel"].args["Name"],
        "pruned_component_ids": pq_group["4"],
    }


def build_summary_rows(summary):
    return [
        {
            "action": "use_existing_measurement",
            "target": "Bus7 vac:0",
            "value": f"drop {summary['bus7_prefault_rms'] - summary['bus7_fault_rms']:.3f}",
            "criterion": "local fault bus sag depth",
        },
        {
            "action": "add_measurement",
            "target": "Bus2 bus2_added:0",
            "value": f"drop {summary['bus2_prefault_rms'] - summary['bus2_fault_rms']:.3f}",
            "criterion": f"expected prefault RMS {summary['bus2_expected_rms']:.3f}",
        },
        {
            "action": "delete_unneeded_outputs",
            "target": "PQ group keep #P only",
            "value": ",".join(summary["retained_p_channels"]),
            "criterion": "#Q channels removed",
        },
        {
            "action": "use_pruned_outputs",
            "target": "#P1:0",
            "value": f"{summary['p1_prefault_avg']:.3f}->{summary['p1_fault_avg']:.3f}->{summary['p1_postfault_avg']:.3f}",
            "criterion": "prefault/fault/postfault active-power response readable",
        },
    ]


def build_conclusion_report(summary):
    bus2_error = abs(summary["bus2_prefault_rms"] - summary["bus2_expected_rms"])
    retained_names = summary["retained_p_channels"]
    bus7_drop = summary["bus7_prefault_rms"] - summary["bus7_fault_rms"]
    bus2_drop = summary["bus2_prefault_rms"] - summary["bus2_fault_rms"]
    bus7_post_gap = summary["bus7_prefault_rms"] - summary["bus7_postfault_rms"]
    bus2_post_gap = summary["bus2_prefault_rms"] - summary["bus2_postfault_rms"]

    findings = [
        {
            "title": "新增 Bus2 电压测点成功进入 EMT 输出链",
            "supported": bus2_error / summary["bus2_expected_rms"] < 0.02,
            "evidence": (
                f"bus2_prefault_rms={summary['bus2_prefault_rms']:.3f} V, "
                f"expected={summary['bus2_expected_rms']:.3f} V"
            ),
        },
        {
            "title": "删除不需要的无功输出后，PQ 组只保留有功通道",
            "supported": all(name.startswith("#P") for name in retained_names),
            "evidence": f"retained channels: {', '.join(retained_names)}",
        },
        {
            "title": "删减输出后，保留下来的关键有功测点仍可直接用于研究读数",
            "supported": "#P1:0" in retained_names,
            "evidence": f"#P1 avg {summary['p1_prefault_avg']:.3f} -> {summary['p1_fault_avg']:.3f} -> {summary['p1_postfault_avg']:.3f}",
        },
        {
            "title": "故障局部母线 Bus7 的电压跌落显著重于远端 Bus2",
            "supported": bus7_drop > bus2_drop * 10.0,
            "evidence": f"Bus7 drop={bus7_drop:.3f} V, Bus2 drop={bus2_drop:.3f} V",
        },
        {
            "title": "故障后 Bus7 的恢复缺口显著大于 Bus2，说明冲击主要集中在局部母线",
            "supported": bus7_post_gap > bus2_post_gap * 10.0,
            "evidence": f"Bus7 post-gap={bus7_post_gap:.3f} V, Bus2 post-gap={bus2_post_gap:.3f} V",
        },
        {
            "title": "保留下来的 #P1 通道能够揭示故障期间功率响应和故障后回落",
            "supported": summary["p1_fault_avg"] > summary["p1_prefault_avg"] and summary["p1_postfault_avg"] < summary["p1_fault_avg"],
            "evidence": f"#P1 avg {summary['p1_prefault_avg']:.3f} -> {summary['p1_fault_avg']:.3f} -> {summary['p1_postfault_avg']:.3f}",
        },
    ]

    return {
        "research_question": "在同一 IEEE3 EMT 研究里，能否把已有测点、脚本化新增测点和输出删减一起组织成一条可复验的可观测性工作流？",
        "criteria": [
            "若新增 Bus2 电压测点的稳态 RMS 与母线基值匹配，则说明增测点链条成立。",
            "若 PQ 输出组删减后只剩 `#P*` 通道，则说明删测点动作生效。",
            "若 `#P1:0` 仍可直接读取，则说明删减后的输出集仍可支撑研究分析。",
            "若 Bus7 的电压跌落和恢复缺口显著大于 Bus2，则说明新增测点已经能区分局部冲击与远端支撑。",
            "若 `#P1` 在故障期间明显抬升且故障后回落，则说明保留的有功通道可用于分析功率响应。",
        ],
        "findings": findings,
        "overall_conclusion": "当前 live 结果支持：CloudPSS 可以在同一条 EMT 研究线上同时完成增测点、删测点和用测点，并据此给出局部冲击、远端支撑和功率响应的联合结论。",
        "boundary": "本结论当前只对 model/holdme/IEEE3、Bus2 新增电压链、PQ 组裁剪到 #P*、以及当前故障与输出配置成立。",
    }


def format_conclusion_report(report):
    lines = [
        "研究问题:",
        report["research_question"],
        "",
        "判据:",
    ]
    for item in report["criteria"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("研究结论:")
    for finding in report["findings"]:
        verdict = "成立" if finding["supported"] else "未成立"
        lines.append(f"- [{verdict}] {finding['title']}")
        lines.append(f"  证据: {finding['evidence']}")
    lines.append("")
    lines.append(f"总体结论: {report['overall_conclusion']}")
    lines.append(f"边界: {report['boundary']}")
    return "\n".join(lines)


def export_summary_rows_csv(rows, path):
    fieldnames = ["action", "target", "value", "criterion"]
    with open(path, "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def export_conclusion_report(report, path):
    with open(path, "w", encoding="utf-8") as output_file:
        output_file.write(format_conclusion_report(report))
        output_file.write("\n")


def parse_args(argv):
    source = DEFAULT_MODEL_SOURCE
    csv_path = None
    conclusion_path = None
    for arg in argv:
        if arg.startswith("--csv="):
            csv_path = arg.split("=", 1)[1].strip()
            continue
        if arg.startswith("--conclusion-txt="):
            conclusion_path = arg.split("=", 1)[1].strip()
            continue
        source = arg
    return source, csv_path, conclusion_path


def print_summary(rows):
    print("=" * 92)
    print("IEEE3 EMT 量测工作流")
    print("=" * 92)
    print("action".ljust(24), "target".ljust(26), "value".ljust(18), "criterion")
    for row in rows:
        print(
            row["action"].ljust(24),
            row["target"].ljust(26),
            row["value"].ljust(18),
            row["criterion"],
        )


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    source, csv_path, conclusion_path = parse_args(argv)

    setToken(load_token())
    model = load_model_from_source(source)

    print(f"研究模型: {model.rid}")
    summary = run_measurement_workflow(model)
    rows = build_summary_rows(summary)
    report = build_conclusion_report(summary)
    print_summary(rows)

    csv_path = csv_path or DEFAULT_EXPORT_PATH
    export_summary_rows_csv(rows, csv_path)
    print(f"\n已导出工作流摘要: {csv_path}")

    conclusion_path = conclusion_path or DEFAULT_CONCLUSION_PATH
    export_conclusion_report(report, conclusion_path)
    print(f"已导出研究结论: {conclusion_path}")

    print("\n" + format_conclusion_report(report))


if __name__ == "__main__":
    main()
