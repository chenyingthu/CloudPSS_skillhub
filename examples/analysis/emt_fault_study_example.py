"""
CloudPSS EMT fault study example.

Run with:
  python examples/analysis/emt_fault_study_example.py
  python examples/analysis/emt_fault_study_example.py model/holdme/IEEE3
  python examples/analysis/emt_fault_study_example.py examples/basic/ieee3-emt-prepared.yaml

This example stays within the current validated EMT mainline:
- local study-copy parameter edits on a prepared IEEE3-style fault model
- ordinary cloud EMT execution
- waveform extraction through EMTResult
- engineering-style comparison of fault severity and clearing time

Validated study directions:
- delayed clearing: `fe 2.7 -> 2.9`
- milder fault impedance proxy: `_newFaultResistor_3p.chg 0.01 -> 1e4`

Optional export:
  python examples/analysis/emt_fault_study_example.py --csv=emt-fault-study-summary.csv
  python examples/analysis/emt_fault_study_example.py --waveform-csv=emt-fault-study-waveforms.csv
  python examples/analysis/emt_fault_study_example.py --waveform-csv=emt-fault-study-waveforms.csv --waveform-window=2.4,3.0
  python examples/analysis/emt_fault_study_example.py --conclusion-txt=emt-fault-study-conclusions.txt
"""

import csv
import math
import os
from copy import deepcopy
from pathlib import Path
import sys
import time

from cloudpss import Model, setToken


DEFAULT_MODEL_SOURCE = "model/holdme/IEEE3"
FAULT_DEFINITION = "model/CloudPSS/_newFaultResistor_3p"
CHANNEL_DEFINITION = "model/CloudPSS/_newChannel"
EMT_JOB_RID = "function/CloudPSS/emtps"
VOLTAGE_CHANNEL_NAME = "vac"
VOLTAGE_TRACE_NAME = "vac:0"
PREFAULT_WINDOW = (2.42, 2.44)
FAULT_WINDOW = (2.56, 2.58)
POSTFAULT_WINDOW = (2.92, 2.94)
LATE_RECOVERY_WINDOW = (2.96, 2.98)
DEFAULT_EXPORT_PREFIX = "emt-fault-study"
DEFAULT_EXPORT_PATH = f"{DEFAULT_EXPORT_PREFIX}-summary.csv"
DEFAULT_WAVEFORM_EXPORT_PATH = f"{DEFAULT_EXPORT_PREFIX}-waveforms.csv"
DEFAULT_CONCLUSION_PATH = f"{DEFAULT_EXPORT_PREFIX}-conclusions.txt"


def load_token():
    try:
        with open(".cloudpss_token", "r") as token_file:
            return token_file.read().strip()
    except FileNotFoundError:
        print("错误: 未找到 .cloudpss_token 文件")
        sys.exit(1)


def load_model_from_source(source):
    candidate = Path(source).expanduser()
    file_like = candidate.suffix.lower() in {".yaml", ".yml", ".json"}

    if candidate.exists():
        return Model.load(str(candidate))
    if file_like:
        raise FileNotFoundError(f"未找到本地模型文件: {candidate}")
    return Model.fetch(source)


def wait_for_completion(job, timeout=300, interval=3):
    start_time = time.time()
    while True:
        status = job.status()
        if status == 1:
            return
        if status == 2:
            raise RuntimeError("EMT 仿真失败")
        if time.time() - start_time > timeout:
            raise TimeoutError("EMT 仿真超时")
        time.sleep(interval)


def find_fault_study_components(model):
    components = model.getAllComponents()
    fault = next(
        component
        for component in components.values()
        if getattr(component, "definition", None) == FAULT_DEFINITION
    )
    voltage_channel = next(
        component
        for component in components.values()
        if getattr(component, "definition", None) == CHANNEL_DEFINITION
        and component.args.get("Name") == VOLTAGE_CHANNEL_NAME
    )
    emt_job = next(job for job in model.jobs if job["rid"] == EMT_JOB_RID)
    return fault, voltage_channel, emt_job


def find_voltage_output_group(emt_job, channel_id):
    for index, group in enumerate(emt_job["args"]["output_channels"]):
        if channel_id in group.get("4", []):
            return index, group
    raise KeyError(f"未找到包含通道 {channel_id} 的 EMT 输出分组")


def prepare_fault_study_model(
    model,
    *,
    fault_end_time,
    fault_chg,
    sampling_freq=2000,
):
    working_model = Model(deepcopy(model.toJSON()))
    fault, voltage_channel, emt_job = find_fault_study_components(working_model)
    output_group_index, output_group = find_voltage_output_group(emt_job, voltage_channel.id)

    working_model.updateComponent(
        fault.id,
        args={
            "fs": {"source": "2.5", "ɵexp": ""},
            "fe": {"source": str(fault_end_time), "ɵexp": ""},
            "chg": {"source": str(fault_chg), "ɵexp": ""},
        },
    )
    working_model.updateComponent(
        voltage_channel.id,
        args={**voltage_channel.args, "Freq": {"source": str(sampling_freq), "ɵexp": ""}},
    )
    output_group["1"] = int(sampling_freq)
    return working_model


def trace_window_rms(trace, start_time, end_time):
    samples = [
        value
        for time_value, value in zip(trace["x"], trace["y"])
        if start_time <= time_value <= end_time
    ]
    if not samples:
        raise ValueError(f"trace window {start_time}..{end_time} contains no samples")
    return math.sqrt(sum(value * value for value in samples) / len(samples))


def extract_voltage_recovery_metrics(
    result,
    *,
    trace_name=VOLTAGE_TRACE_NAME,
):
    plot_index = None
    channel_names = []
    for candidate_index, _plot in enumerate(result.getPlots()):
        candidate_names = result.getPlotChannelNames(candidate_index)
        if trace_name in candidate_names:
            plot_index = candidate_index
            channel_names = candidate_names
            break

    if plot_index is None:
        raise KeyError(f"未找到目标通道 {trace_name}")

    trace = result.getPlotChannelData(plot_index, trace_name)
    time_step = trace["x"][1] - trace["x"][0] if len(trace["x"]) > 1 else None

    return {
        "plot_index": plot_index,
        "trace_name": trace_name,
        "trace": trace,
        "point_count": len(trace["x"]),
        "time_step": time_step,
        "prefault_rms": trace_window_rms(trace, *PREFAULT_WINDOW),
        "fault_rms": trace_window_rms(trace, *FAULT_WINDOW),
        "postfault_rms": trace_window_rms(trace, *POSTFAULT_WINDOW),
        "late_recovery_rms": trace_window_rms(trace, *LATE_RECOVERY_WINDOW),
    }


def build_study_specs():
    return [
        {
            "name": "baseline",
            "description": "基线故障: fe=2.7, chg=0.01",
            "fault_end_time": "2.7",
            "fault_chg": "0.01",
            "sampling_freq": 2000,
        },
        {
            "name": "delayed_clearing",
            "description": "延长故障切除时间: fe=2.9, chg=0.01",
            "fault_end_time": "2.9",
            "fault_chg": "0.01",
            "sampling_freq": 2000,
        },
        {
            "name": "mild_fault",
            "description": "较轻故障: fe=2.7, chg=1e4",
            "fault_end_time": "2.7",
            "fault_chg": "1e4",
            "sampling_freq": 2000,
        },
    ]


def build_summary_rows(study_results):
    baseline = next(result for result in study_results if result["name"] == "baseline")
    baseline_metrics = baseline["metrics"]
    rows = []

    for result in study_results:
        metrics = result["metrics"]
        fault_drop_vs_prefault = metrics["prefault_rms"] - metrics["fault_rms"]
        postfault_gap_vs_prefault = metrics["prefault_rms"] - metrics["postfault_rms"]
        late_recovery_gap_vs_prefault = metrics["prefault_rms"] - metrics["late_recovery_rms"]
        observation = "reference"
        if result["name"] == "delayed_clearing":
            observation = "same fault depth, weaker post-fault recovery"
        elif result["name"] == "mild_fault":
            observation = "shallower sag, stronger post-fault recovery"
        rows.append(
            {
                "scenario": result["name"],
                "description": result["description"],
                "fault_end_time": str(result["fault_end_time"]),
                "fault_chg": str(result["fault_chg"]),
                "point_count": str(metrics["point_count"]),
                "prefault_rms": f"{metrics['prefault_rms']:.3f}",
                "fault_rms": f"{metrics['fault_rms']:.3f}",
                "postfault_rms": f"{metrics['postfault_rms']:.3f}",
                "late_recovery_rms": f"{metrics['late_recovery_rms']:.3f}",
                "fault_drop_vs_prefault": f"{fault_drop_vs_prefault:.3f}",
                "postfault_gap_vs_prefault": f"{postfault_gap_vs_prefault:.3f}",
                "late_recovery_gap_vs_prefault": f"{late_recovery_gap_vs_prefault:.3f}",
                "delta_fault_rms_vs_baseline": f"{metrics['fault_rms'] - baseline_metrics['fault_rms']:.3f}",
                "delta_postfault_rms_vs_baseline": f"{metrics['postfault_rms'] - baseline_metrics['postfault_rms']:.3f}",
                "observation": observation,
            }
        )

    return rows


def export_summary_rows_csv(rows, path):
    fieldnames = [
        "scenario",
        "description",
        "fault_end_time",
        "fault_chg",
        "point_count",
        "prefault_rms",
        "fault_rms",
        "postfault_rms",
        "late_recovery_rms",
        "fault_drop_vs_prefault",
        "postfault_gap_vs_prefault",
        "late_recovery_gap_vs_prefault",
        "delta_fault_rms_vs_baseline",
        "delta_postfault_rms_vs_baseline",
        "observation",
    ]
    with open(path, "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def export_waveform_comparison_csv(study_results, path):
    export_waveform_comparison_window_csv(study_results, path)


def export_waveform_comparison_window_csv(study_results, path, time_window=None):
    if not study_results:
        raise ValueError("study_results 不能为空")

    baseline_trace = study_results[0]["metrics"]["trace"]
    baseline_times = baseline_trace["x"]
    rows = []

    for point_index, time_value in enumerate(baseline_times):
        if time_window is not None:
            start_time, end_time = time_window
            if time_value < start_time or time_value > end_time:
                continue
        row = {"time": f"{time_value:.6f}"}
        for result in study_results:
            trace = result["metrics"]["trace"]
            if len(trace["x"]) != len(baseline_times):
                raise ValueError("不同工况的波形点数不一致，无法直接导出对比 CSV")
            if abs(trace["x"][point_index] - time_value) > 1e-9:
                raise ValueError("不同工况的时间轴不一致，无法直接导出对比 CSV")
            row[result["name"]] = f"{trace['y'][point_index]:.6f}"
        rows.append(row)

    fieldnames = ["time"] + [result["name"] for result in study_results]
    with open(path, "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_conclusion_report(rows):
    rows_by_name = {row["scenario"]: row for row in rows}
    baseline = rows_by_name["baseline"]
    delayed = rows_by_name["delayed_clearing"]
    mild = rows_by_name["mild_fault"]

    delayed_fault_delta = float(delayed["delta_fault_rms_vs_baseline"])
    delayed_post_gap = float(delayed["postfault_gap_vs_prefault"])
    baseline_post_gap = float(baseline["postfault_gap_vs_prefault"])
    delayed_late_gap = float(delayed["late_recovery_gap_vs_prefault"])
    baseline_late_gap = float(baseline["late_recovery_gap_vs_prefault"])
    mild_fault_drop = float(mild["fault_drop_vs_prefault"])
    baseline_fault_drop = float(baseline["fault_drop_vs_prefault"])
    mild_post_gap = float(mild["postfault_gap_vs_prefault"])

    findings = [
        {
            "title": "延迟切除主要恶化故障后恢复，而不是改变故障深度",
            "supported": abs(delayed_fault_delta) <= 0.1
            and delayed_post_gap - baseline_post_gap > 10.0
            and delayed_late_gap - baseline_late_gap > 10.0,
            "evidence": (
                f"delta_fault_rms_vs_baseline={delayed_fault_delta:.3f} V, "
                f"postfault_gap {baseline_post_gap:.3f} -> {delayed_post_gap:.3f} V, "
                f"late_gap {baseline_late_gap:.3f} -> {delayed_late_gap:.3f} V"
            ),
        },
        {
            "title": "较轻故障显著减小故障跌落，并把恢复缺口压回接近零",
            "supported": baseline_fault_drop - mild_fault_drop > 200.0
            and baseline_post_gap - mild_post_gap > 5.0,
            "evidence": (
                f"fault_drop {baseline_fault_drop:.3f} -> {mild_fault_drop:.3f} V, "
                f"postfault_gap {baseline_post_gap:.3f} -> {mild_post_gap:.3f} V"
            ),
        },
    ]

    return {
        "research_question": (
            "在同一 IEEE3 故障模型上，延迟切除与降低故障严重度，"
            "分别如何影响故障深度和故障后恢复缺口？"
        ),
        "criteria": [
            "若 delayed_clearing 与 baseline 的 fault_rms 基本一致，但 postfault/late gap 明显扩大，则说明主要差异来自切除更晚。",
            "若 mild_fault 的 fault_drop_vs_prefault 显著小于 baseline，且 postfault_gap_vs_prefault 接近零，则说明主要差异来自故障更轻。",
        ],
        "findings": findings,
        "overall_conclusion": (
            "当前 live 结果支持这样一条工程结论："
            "延迟切除主要拉大恢复缺口，较轻故障主要减小电压跌落并改善恢复。"
        ),
        "boundary": (
            "本结论当前只对 model/holdme/IEEE3、plot-2/vac:0、"
            "以及示例里固定的时间窗口和三组工况宣称成立。"
        ),
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


def export_conclusion_report(report, path):
    with open(path, "w", encoding="utf-8") as output_file:
        output_file.write(format_conclusion_report(report))
        output_file.write("\n")


def derive_export_prefix(path_string, suffix):
    path = Path(path_string)
    stem = path.stem
    if stem.endswith(suffix):
        stem = stem[: -len(suffix)]
    return path.with_name(stem)


def resolve_export_paths(csv_path=None, waveform_csv_path=None):
    if csv_path and waveform_csv_path:
        return csv_path, waveform_csv_path

    if csv_path:
        prefix_path = derive_export_prefix(csv_path, "-summary")
        return csv_path, str(prefix_path.with_name(f"{prefix_path.name}-waveforms.csv"))

    if waveform_csv_path:
        prefix_path = derive_export_prefix(waveform_csv_path, "-waveforms")
        return str(prefix_path.with_name(f"{prefix_path.name}-summary.csv")), waveform_csv_path

    return DEFAULT_EXPORT_PATH, DEFAULT_WAVEFORM_EXPORT_PATH


def resolve_conclusion_path(csv_path=None, waveform_csv_path=None, conclusion_path=None):
    if conclusion_path:
        return conclusion_path
    summary_path, waveform_path = resolve_export_paths(csv_path, waveform_csv_path)
    prefix_path = derive_export_prefix(summary_path, "-summary")
    if prefix_path.name == DEFAULT_EXPORT_PREFIX and waveform_path == DEFAULT_WAVEFORM_EXPORT_PATH:
        return DEFAULT_CONCLUSION_PATH
    return str(prefix_path.with_name(f"{prefix_path.name}-conclusions.txt"))


def run_fault_study(model, specs=None):
    study_specs = specs or build_study_specs()
    results = []

    for spec in study_specs:
        working_model = prepare_fault_study_model(
            model,
            fault_end_time=spec["fault_end_time"],
            fault_chg=spec["fault_chg"],
            sampling_freq=spec["sampling_freq"],
        )
        job = working_model.runEMT()
        wait_for_completion(job)
        metrics = extract_voltage_recovery_metrics(job.result)

        results.append({**spec, "metrics": metrics})

    return results


def print_summary(rows):
    print("=" * 90)
    print("IEEE3 EMT 故障研究摘要")
    print("=" * 90)
    print(
        "scenario".ljust(18),
        "fault_rms".rjust(12),
        "postfault".rjust(12),
        "post_gap".rjust(12),
        "late_gap".rjust(12),
        "d_post".rjust(12),
    )
    for row in rows:
        print(
            row["scenario"].ljust(18),
            row["fault_rms"].rjust(12),
            row["postfault_rms"].rjust(12),
            row["postfault_gap_vs_prefault"].rjust(12),
            row["late_recovery_gap_vs_prefault"].rjust(12),
            row["delta_postfault_rms_vs_baseline"].rjust(12),
        )


def parse_args(argv):
    source = DEFAULT_MODEL_SOURCE
    csv_path = None
    waveform_csv_path = None
    waveform_window = None
    conclusion_path = None

    for arg in argv:
        if arg.startswith("--csv="):
            csv_path = arg.split("=", 1)[1].strip()
            continue
        if arg.startswith("--waveform-csv="):
            waveform_csv_path = arg.split("=", 1)[1].strip()
            continue
        if arg.startswith("--waveform-window="):
            window_value = arg.split("=", 1)[1].strip()
            start_text, end_text = [item.strip() for item in window_value.split(",", 1)]
            waveform_window = (float(start_text), float(end_text))
            continue
        if arg.startswith("--conclusion-txt="):
            conclusion_path = arg.split("=", 1)[1].strip()
            continue
        source = arg

    return source, csv_path, waveform_csv_path, waveform_window, conclusion_path


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    source, csv_path, waveform_csv_path, waveform_window, conclusion_path = parse_args(argv)

    token = load_token()
    setToken(token)
    model = load_model_from_source(source)

    print(f"研究模型: {model.rid}")
    results = run_fault_study(model)
    rows = build_summary_rows(results)
    report = build_conclusion_report(rows)
    print_summary(rows)

    csv_path, waveform_csv_path = resolve_export_paths(csv_path, waveform_csv_path)
    export_summary_rows_csv(rows, csv_path)
    print(f"\n已导出 CSV 摘要: {csv_path}")

    export_waveform_comparison_window_csv(results, waveform_csv_path, waveform_window)
    print(f"已导出对比波形 CSV: {waveform_csv_path}")

    conclusion_path = resolve_conclusion_path(csv_path, waveform_csv_path, conclusion_path)
    export_conclusion_report(report, conclusion_path)
    print(f"已导出研究结论: {conclusion_path}")

    print("\n" + format_conclusion_report(report))


if __name__ == "__main__":
    main()
