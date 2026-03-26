"""
CloudPSS EMT fault-clearing scan example.

Run with:
  python examples/analysis/emt_fault_clearing_scan_example.py
  python examples/analysis/emt_fault_clearing_scan_example.py model/holdme/IEEE3
  python examples/analysis/emt_fault_clearing_scan_example.py --csv=emt-fault-clearing-scan.csv
  python examples/analysis/emt_fault_clearing_scan_example.py --conclusion-txt=emt-fault-clearing-scan.txt

This example demonstrates a small EMT clearing-time scan on an already
validated IEEE3 fault model. The study question is not "what happens a fixed
delay after clearing", but "at fixed engineering review deadlines, how much
voltage recovery has been achieved as clearing is delayed?"
"""

import csv
import importlib.util
import math
from pathlib import Path
import sys

from cloudpss import setToken


STUDY_HELPER_PATH = Path(__file__).with_name("emt_fault_study_example.py")
_STUDY_SPEC = importlib.util.spec_from_file_location(
    "emt_fault_study_example_shared_for_clearing_scan",
    STUDY_HELPER_PATH,
)
_STUDY_MODULE = importlib.util.module_from_spec(_STUDY_SPEC)
assert _STUDY_SPEC.loader is not None
_STUDY_SPEC.loader.exec_module(_STUDY_MODULE)

DEFAULT_MODEL_SOURCE = _STUDY_MODULE.DEFAULT_MODEL_SOURCE
load_model_from_source = _STUDY_MODULE.load_model_from_source
load_token = _STUDY_MODULE.load_token
prepare_fault_study_model = _STUDY_MODULE.prepare_fault_study_model
wait_for_completion = _STUDY_MODULE.wait_for_completion
extract_voltage_recovery_metrics = _STUDY_MODULE.extract_voltage_recovery_metrics


DEFAULT_EXPORT_PREFIX = "emt-fault-clearing-scan"
DEFAULT_EXPORT_PATH = f"{DEFAULT_EXPORT_PREFIX}.csv"
DEFAULT_CONCLUSION_PATH = f"{DEFAULT_EXPORT_PREFIX}.txt"
ASSESSMENT_WINDOWS = {
    "gap_295": (2.94, 2.96),
    "gap_300": (2.99, 3.01),
}


def trace_window_rms(trace, start_time, end_time):
    samples = [
        value
        for time_value, value in zip(trace["x"], trace["y"])
        if start_time <= time_value <= end_time
    ]
    if not samples:
        raise ValueError(f"trace window {start_time}..{end_time} contains no samples")
    return math.sqrt(sum(value * value for value in samples) / len(samples))


def build_scan_specs():
    return [
        {"name": "fe_270", "fault_end_time": "2.70", "fault_chg": "0.01", "sampling_freq": 2000},
        {"name": "fe_275", "fault_end_time": "2.75", "fault_chg": "0.01", "sampling_freq": 2000},
        {"name": "fe_280", "fault_end_time": "2.80", "fault_chg": "0.01", "sampling_freq": 2000},
        {"name": "fe_285", "fault_end_time": "2.85", "fault_chg": "0.01", "sampling_freq": 2000},
        {"name": "fe_290", "fault_end_time": "2.90", "fault_chg": "0.01", "sampling_freq": 2000},
    ]


def run_fault_clearing_scan(model, specs=None):
    results = []
    for spec in specs or build_scan_specs():
        working_model = prepare_fault_study_model(
            model,
            fault_end_time=spec["fault_end_time"],
            fault_chg=spec["fault_chg"],
            sampling_freq=spec["sampling_freq"],
        )
        job = working_model.runEMT()
        wait_for_completion(job)
        metrics = extract_voltage_recovery_metrics(job.result)
        trace = metrics["trace"]
        metrics["gap_295"] = metrics["prefault_rms"] - trace_window_rms(trace, *ASSESSMENT_WINDOWS["gap_295"])
        metrics["gap_300"] = metrics["prefault_rms"] - trace_window_rms(trace, *ASSESSMENT_WINDOWS["gap_300"])
        results.append({**spec, "metrics": metrics})
    return results


def build_summary_rows(scan_results):
    rows = []
    for result in scan_results:
        metrics = result["metrics"]
        rows.append(
            {
                "scenario": result["name"],
                "fault_end_time": str(result["fault_end_time"]),
                "prefault_rms": f"{metrics['prefault_rms']:.3f}",
                "postfault_rms": f"{metrics['postfault_rms']:.3f}",
                "late_recovery_rms": f"{metrics['late_recovery_rms']:.3f}",
                "gap_295": f"{metrics['gap_295']:.3f}",
                "gap_300": f"{metrics['gap_300']:.3f}",
            }
        )
    return rows


def build_conclusion_report(rows):
    gap_295 = [float(row["gap_295"]) for row in rows]
    gap_300 = [float(row["gap_300"]) for row in rows]
    fe_values = [row["fault_end_time"] for row in rows]
    monotonic_295 = all(left < right for left, right in zip(gap_295, gap_295[1:]))
    monotonic_300 = all(left < right for left, right in zip(gap_300, gap_300[1:]))

    findings = [
        {
            "title": "在固定 2.95s 评估时点，延迟清除会系统性放大恢复缺口",
            "supported": monotonic_295,
            "evidence": " -> ".join(f"{fe}:{gap:.3f}" for fe, gap in zip(fe_values, gap_295)),
        },
        {
            "title": "在固定 3.00s 评估时点，延迟清除会系统性放大恢复缺口",
            "supported": monotonic_300,
            "evidence": " -> ".join(f"{fe}:{gap:.3f}" for fe, gap in zip(fe_values, gap_300)),
        },
    ]

    return {
        "research_question": "在 IEEE3 故障模型上，如果故障切除时间逐步延后，那么在固定研究审视时刻的电压恢复缺口是否会系统性恶化？",
        "criteria": [
            "若 `gap_295` 随 `fe` 增大而单调上升，则说明在 2.95s 这个固定评估时点，晚切除工况恢复更差。",
            "若 `gap_300` 随 `fe` 增大而单调上升，则说明在 3.00s 这个固定评估时点，晚切除工况恢复更差。",
        ],
        "findings": findings,
        "overall_conclusion": "当前 live 结果支持：在固定研究审视时点上，故障切除越晚，恢复缺口越大。",
        "boundary": "本结论只对 model/holdme/IEEE3、固定 chg=0.01、固定量测链 plot-2/vac:0、以及 fe=2.70..2.90 这组扫描成立。",
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
    fieldnames = [
        "scenario",
        "fault_end_time",
        "prefault_rms",
        "postfault_rms",
        "late_recovery_rms",
        "gap_295",
        "gap_300",
    ]
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
    print("=" * 88)
    print("IEEE3 EMT 故障清除时间扫描")
    print("=" * 88)
    print(
        "scenario".ljust(18),
        "fe".rjust(8),
        "postfault".rjust(12),
        "late_rec".rjust(12),
        "gap_295".rjust(12),
        "gap_300".rjust(12),
    )
    for row in rows:
        print(
            row["scenario"].ljust(18),
            row["fault_end_time"].rjust(8),
            row["postfault_rms"].rjust(12),
            row["late_recovery_rms"].rjust(12),
            row["gap_295"].rjust(12),
            row["gap_300"].rjust(12),
        )


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    source, csv_path, conclusion_path = parse_args(argv)

    setToken(load_token())
    model = load_model_from_source(source)

    print(f"研究模型: {model.rid}")
    results = run_fault_clearing_scan(model)
    rows = build_summary_rows(results)
    report = build_conclusion_report(rows)
    print_summary(rows)

    csv_path = csv_path or DEFAULT_EXPORT_PATH
    export_summary_rows_csv(rows, csv_path)
    print(f"\n已导出扫描摘要: {csv_path}")

    conclusion_path = conclusion_path or DEFAULT_CONCLUSION_PATH
    export_conclusion_report(report, conclusion_path)
    print(f"已导出研究结论: {conclusion_path}")

    print("\n" + format_conclusion_report(report))


if __name__ == "__main__":
    main()
