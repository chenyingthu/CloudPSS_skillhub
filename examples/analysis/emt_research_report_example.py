"""
CloudPSS EMT research report example.

Run with:
  python examples/analysis/emt_research_report_example.py
  python examples/analysis/emt_research_report_example.py model/holdme/IEEE3
  python examples/analysis/emt_research_report_example.py --report=emt-research-report.md

This example aggregates several already validated EMT study paths into a
single Markdown report:
- fault-study comparison
- fault-clearing scan
- fault-severity scan
- measurement workflow
"""

import importlib.util
from pathlib import Path
import sys

from cloudpss import setToken


CURRENT_DIR = Path(__file__).resolve().parent


def load_helper_module(filename, module_name):
    path = CURRENT_DIR / filename
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


FAULT_STUDY_MODULE = load_helper_module(
    "emt_fault_study_example.py",
    "emt_fault_study_example_for_report",
)
FAULT_CLEARING_MODULE = load_helper_module(
    "emt_fault_clearing_scan_example.py",
    "emt_fault_clearing_scan_example_for_report",
)
FAULT_SEVERITY_MODULE = load_helper_module(
    "emt_fault_severity_scan_example.py",
    "emt_fault_severity_scan_example_for_report",
)
MEASUREMENT_MODULE = load_helper_module(
    "emt_measurement_workflow_example.py",
    "emt_measurement_workflow_example_for_report",
)

DEFAULT_MODEL_SOURCE = FAULT_STUDY_MODULE.DEFAULT_MODEL_SOURCE
DEFAULT_REPORT_PATH = "emt-research-report.md"


def parse_args(argv):
    source = DEFAULT_MODEL_SOURCE
    report_path = DEFAULT_REPORT_PATH
    for arg in argv:
        if arg.startswith("--report="):
            report_path = arg.split("=", 1)[1].strip()
            continue
        source = arg
    return source, report_path


def build_report_sections(model):
    fault_study_results = FAULT_STUDY_MODULE.run_fault_study(model)
    fault_study_rows = FAULT_STUDY_MODULE.build_summary_rows(fault_study_results)
    fault_study_report = FAULT_STUDY_MODULE.build_conclusion_report(fault_study_rows)

    clearing_results = FAULT_CLEARING_MODULE.run_fault_clearing_scan(model)
    clearing_rows = FAULT_CLEARING_MODULE.build_summary_rows(clearing_results)
    clearing_report = FAULT_CLEARING_MODULE.build_conclusion_report(clearing_rows)

    severity_results = FAULT_SEVERITY_MODULE.run_fault_severity_scan(model)
    severity_rows = FAULT_SEVERITY_MODULE.build_summary_rows(severity_results)
    severity_report = FAULT_SEVERITY_MODULE.build_conclusion_report(severity_rows)

    measurement_summary = MEASUREMENT_MODULE.run_measurement_workflow(model)
    measurement_rows = MEASUREMENT_MODULE.build_summary_rows(measurement_summary)
    measurement_report = MEASUREMENT_MODULE.build_conclusion_report(measurement_summary)

    return {
        "fault_study": {
            "rows": fault_study_rows,
            "report": fault_study_report,
        },
        "fault_clearing_scan": {
            "rows": clearing_rows,
            "report": clearing_report,
        },
        "fault_severity_scan": {
            "rows": severity_rows,
            "report": severity_report,
        },
        "measurement_workflow": {
            "rows": measurement_rows,
            "report": measurement_report,
        },
    }


def markdown_table(rows):
    if not rows:
        return "_No data_\n"
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines) + "\n"


def report_block(title, rows, report):
    lines = [
        f"## {title}",
        "",
        markdown_table(rows).rstrip(),
        "",
        "### 结论",
        "",
        FAULT_STUDY_MODULE.format_conclusion_report(report),
        "",
    ]
    return "\n".join(lines)


def build_markdown_report(model_rid, sections):
    lines = [
        "# CloudPSS EMT Research Report",
        "",
        f"- Model: `{model_rid}`",
        "- Scope: validated ordinary-cloud EMT studies on IEEE3",
        "",
        "## Executive Summary",
        "",
        "- CloudPSS can compare discrete EMT fault scenarios and turn waveform metrics into explicit study conclusions.",
        "- CloudPSS can run small EMT disturbance scans on clearing time and fault severity with stable ranking criteria.",
        "- CloudPSS can script measurement observability workflows: reuse existing channels, add new measurement points, prune outputs, and still preserve analysis-ready traces.",
        "",
    ]

    lines.append(report_block("Fault Study Comparison", sections["fault_study"]["rows"], sections["fault_study"]["report"]))
    lines.append(report_block("Fault Clearing Scan", sections["fault_clearing_scan"]["rows"], sections["fault_clearing_scan"]["report"]))
    lines.append(report_block("Fault Severity Scan", sections["fault_severity_scan"]["rows"], sections["fault_severity_scan"]["report"]))
    lines.append(report_block("Measurement Workflow", sections["measurement_workflow"]["rows"], sections["measurement_workflow"]["report"]))
    return "\n".join(lines)


def export_report(report_text, path):
    with open(path, "w", encoding="utf-8") as output_file:
        output_file.write(report_text)
        output_file.write("\n")


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    source, report_path = parse_args(argv)

    setToken(FAULT_STUDY_MODULE.load_token())
    model = FAULT_STUDY_MODULE.load_model_from_source(source)

    print(f"研究模型: {model.rid}")
    sections = build_report_sections(model)
    report_text = build_markdown_report(model.rid, sections)
    export_report(report_text, report_path)
    print(f"已导出 EMT 研究报告: {report_path}")


if __name__ == "__main__":
    main()
