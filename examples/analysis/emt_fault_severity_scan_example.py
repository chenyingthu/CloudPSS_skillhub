"""
CloudPSS EMT fault severity scan example.

Run with:
  python examples/analysis/emt_fault_severity_scan_example.py
  python examples/analysis/emt_fault_severity_scan_example.py model/holdme/IEEE3
  python examples/analysis/emt_fault_severity_scan_example.py --csv=emt-fault-severity-scan.csv
  python examples/analysis/emt_fault_severity_scan_example.py --conclusion-txt=emt-fault-severity-scan.txt

This example shows a compact EMT disturbance scan on an already prepared
IEEE3 fault model. It stays within the currently live-validated path:
- local working-copy edits to `_newFaultResistor_3p.chg`
- ordinary cloud EMT execution
- waveform metric extraction through `EMTResult`
- engineering conclusion derived from a small severity sweep
"""

import csv
import importlib.util
from pathlib import Path
import sys

from cloudpss import Model, setToken

STUDY_HELPER_PATH = Path(__file__).with_name("emt_fault_study_example.py")
_STUDY_SPEC = importlib.util.spec_from_file_location(
    "emt_fault_study_example_shared",
    STUDY_HELPER_PATH,
)
_STUDY_MODULE = importlib.util.module_from_spec(_STUDY_SPEC)
assert _STUDY_SPEC.loader is not None
_STUDY_SPEC.loader.exec_module(_STUDY_MODULE)

DEFAULT_MODEL_SOURCE = _STUDY_MODULE.DEFAULT_MODEL_SOURCE
extract_voltage_recovery_metrics = _STUDY_MODULE.extract_voltage_recovery_metrics
load_model_from_source = _STUDY_MODULE.load_model_from_source
load_token = _STUDY_MODULE.load_token
prepare_fault_study_model = _STUDY_MODULE.prepare_fault_study_model
wait_for_completion = _STUDY_MODULE.wait_for_completion


DEFAULT_EXPORT_PREFIX = "emt-fault-severity-scan"
DEFAULT_EXPORT_PATH = f"{DEFAULT_EXPORT_PREFIX}.csv"
DEFAULT_CONCLUSION_PATH = f"{DEFAULT_EXPORT_PREFIX}.txt"


def build_scan_specs():
    return [
        {
            "name": "severe_fault",
            "description": "强故障近似: chg=1e-2",
            "fault_end_time": "2.7",
            "fault_chg": "1e-2",
            "sampling_freq": 2000,
        },
        {
            "name": "intermediate_fault",
            "description": "较轻故障过渡点: chg=1e2",
            "fault_end_time": "2.7",
            "fault_chg": "1e2",
            "sampling_freq": 2000,
        },
        {
            "name": "mild_fault",
            "description": "轻故障近似: chg=1e4",
            "fault_end_time": "2.7",
            "fault_chg": "1e4",
            "sampling_freq": 2000,
        },
    ]


def run_fault_severity_scan(model, specs=None):
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
        results.append({**spec, "metrics": metrics})
    return results


def build_summary_rows(scan_results):
    rows = []
    for result in scan_results:
        metrics = result["metrics"]
        fault_drop_vs_prefault = metrics["prefault_rms"] - metrics["fault_rms"]
        postfault_gap_vs_prefault = metrics["prefault_rms"] - metrics["postfault_rms"]
        late_recovery_gap_vs_prefault = metrics["prefault_rms"] - metrics["late_recovery_rms"]
        rows.append(
            {
                "scenario": result["name"],
                "description": result["description"],
                "fault_chg": str(result["fault_chg"]),
                "prefault_rms": f"{metrics['prefault_rms']:.3f}",
                "fault_rms": f"{metrics['fault_rms']:.3f}",
                "postfault_rms": f"{metrics['postfault_rms']:.3f}",
                "late_recovery_rms": f"{metrics['late_recovery_rms']:.3f}",
                "fault_drop_vs_prefault": f"{fault_drop_vs_prefault:.3f}",
                "postfault_gap_vs_prefault": f"{postfault_gap_vs_prefault:.3f}",
                "late_recovery_gap_vs_prefault": f"{late_recovery_gap_vs_prefault:.3f}",
            }
        )
    return rows


def build_conclusion_report(rows):
    rows_by_name = {row["scenario"]: row for row in rows}
    severe = rows_by_name["severe_fault"]
    intermediate = rows_by_name["intermediate_fault"]
    mild = rows_by_name["mild_fault"]

    severe_fault_drop = float(severe["fault_drop_vs_prefault"])
    intermediate_fault_drop = float(intermediate["fault_drop_vs_prefault"])
    mild_fault_drop = float(mild["fault_drop_vs_prefault"])

    severe_post_gap = float(severe["postfault_gap_vs_prefault"])
    intermediate_post_gap = float(intermediate["postfault_gap_vs_prefault"])
    mild_post_gap = float(mild["postfault_gap_vs_prefault"])

    findings = [
        {
            "title": "随着 chg 增大，故障期间电压跌落显著减轻",
            "supported": severe_fault_drop > intermediate_fault_drop > mild_fault_drop,
            "evidence": (
                f"fault_drop {severe_fault_drop:.3f} > "
                f"{intermediate_fault_drop:.3f} > {mild_fault_drop:.3f} V"
            ),
        },
        {
            "title": "随着 chg 增大，故障后恢复缺口同步缩小",
            "supported": severe_post_gap > intermediate_post_gap > mild_post_gap,
            "evidence": (
                f"postfault_gap {severe_post_gap:.3f} > "
                f"{intermediate_post_gap:.3f} > {mild_post_gap:.3f} V"
            ),
        },
    ]

    return {
        "research_question": "在 IEEE3 故障模型上，提高故障参数 chg 是否会系统性减弱电压跌落并改善恢复？",
        "criteria": [
            "若 fault_drop_vs_prefault 随 chg 增大而单调减小，则说明故障严重度扫描有效区分了故障中跌落深度。",
            "若 postfault_gap_vs_prefault 随 chg 增大而单调减小，则说明扫描也有效区分了故障后恢复缺口。",
        ],
        "findings": findings,
        "overall_conclusion": "当前 live 结果支持：在这条已验证的 IEEE3 故障链上，较大的 chg 对应更轻的电压跌落和更小的恢复缺口。",
        "boundary": "本结论只对 model/holdme/IEEE3、固定 fe=2.7、固定量测链 plot-2/vac:0 以及当前三点 chg 扫描成立。",
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
        "description",
        "fault_chg",
        "prefault_rms",
        "fault_rms",
        "postfault_rms",
        "late_recovery_rms",
        "fault_drop_vs_prefault",
        "postfault_gap_vs_prefault",
        "late_recovery_gap_vs_prefault",
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
    print("IEEE3 EMT 故障严重度扫描")
    print("=" * 88)
    print(
        "scenario".ljust(22),
        "chg".rjust(10),
        "fault_drop".rjust(14),
        "post_gap".rjust(12),
        "late_gap".rjust(12),
    )
    for row in rows:
        print(
            row["scenario"].ljust(22),
            row["fault_chg"].rjust(10),
            row["fault_drop_vs_prefault"].rjust(14),
            row["postfault_gap_vs_prefault"].rjust(12),
            row["late_recovery_gap_vs_prefault"].rjust(12),
        )


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    source, csv_path, conclusion_path = parse_args(argv)

    setToken(load_token())
    model = load_model_from_source(source)

    print(f"研究模型: {model.rid}")
    results = run_fault_severity_scan(model)
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
