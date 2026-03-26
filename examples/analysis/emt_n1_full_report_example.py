"""
CloudPSS EMT N-1 full-scan report example.

Run with:
  python examples/analysis/emt_n1_full_report_example.py
  python examples/analysis/emt_n1_full_report_example.py model/holdme/IEEE3
  python examples/analysis/emt_n1_full_report_example.py --report=emt-n1-full-report.md
  python examples/analysis/emt_n1_full_report_example.py --lines-only

This example is a report-oriented wrapper around the validated EMT N-1
screening path. Unlike `emt_n1_security_report_example.py`, it defaults to the
full discovered IEEE3 candidate set.
"""

import importlib.util
from pathlib import Path
import sys

from cloudpss import setToken


CURRENT_DIR = Path(__file__).resolve().parent
REPORT_MODULE_PATH = CURRENT_DIR / "emt_n1_security_report_example.py"


def load_helper_module(module_path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


REPORT_MODULE = load_helper_module(
    REPORT_MODULE_PATH,
    "emt_n1_security_report_example_for_full_scan",
)

DEFAULT_MODEL_SOURCE = REPORT_MODULE.DEFAULT_MODEL_SOURCE
DEFAULT_REPORT_PATH = "emt-n1-full-report.md"


def parse_args(argv):
    source = DEFAULT_MODEL_SOURCE
    report_path = DEFAULT_REPORT_PATH
    include_transformers = True
    limit = None

    for arg in argv:
        if arg == "--lines-only":
            include_transformers = False
            continue
        if arg.startswith("--report="):
            report_path = arg.split("=", 1)[1].strip()
            continue
        if arg.startswith("--limit="):
            limit = int(arg.split("=", 1)[1].strip())
            continue
        source = arg

    return source, report_path, include_transformers, limit


def build_full_report_sections(model, *, include_transformers, limit):
    sections = REPORT_MODULE.build_report_sections(
        model,
        use_all_discovered=True,
        include_transformers=include_transformers,
        limit=limit,
    )
    summary_rows = sections["summary_rows"]
    top_rank_rows = summary_rows[:5]
    severity_rows = [
        {
            "severity": severity,
            "count": str(sections["digest"]["severity_counts"][severity]),
        }
        for severity in ["critical", "warning", "observe"]
    ]
    sections["top_rank_rows"] = top_rank_rows
    sections["severity_rows"] = severity_rows
    return sections


def build_markdown_report(model_rid, sections, *, include_transformers):
    digest = sections["digest"]
    monitored_scope = "lines + transformers" if include_transformers else "lines only"
    lines = [
        "# CloudPSS EMT N-1 Full Screening Report",
        "",
        f"- Model: `{model_rid}`",
        f"- Scope: full discovered IEEE3 {monitored_scope} subset",
        "",
        "## Executive Summary",
        "",
        "- This report organizes the full discovered IEEE3 EMT N-1 scan into a conclusion-first deliverable.",
        "- It keeps the same validated monitors: Bus7, Bus2, Bus8, and `#P1`.",
        f"- Total scanned cases = `{digest['total_cases']}`.",
        "",
        "## Severity Distribution",
        "",
        REPORT_MODULE.markdown_table(sections["severity_rows"]).rstrip(),
        "",
        "## Case Highlights",
        "",
        REPORT_MODULE.markdown_table(sections["highlight_rows"]).rstrip(),
        "",
        "## Top Ranked Cases",
        "",
        REPORT_MODULE.markdown_table(sections["top_rank_rows"]).rstrip(),
        "",
        "## Full Ranked Table",
        "",
        REPORT_MODULE.markdown_table(sections["summary_rows"]).rstrip(),
        "",
        "## Conclusions",
        "",
        REPORT_MODULE.N1_MODULE.format_conclusion_report(sections["conclusion_report"]),
        "",
    ]
    return "\n".join(lines)


def export_report(report_text, path):
    with open(path, "w", encoding="utf-8") as output_file:
        output_file.write(report_text)
        output_file.write("\n")


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    source, report_path, include_transformers, limit = parse_args(argv)

    setToken(REPORT_MODULE.N1_MODULE.load_token())
    model = REPORT_MODULE.N1_MODULE.load_model_from_source(source)

    print(f"研究模型: {model.rid}")
    sections = build_full_report_sections(
        model,
        include_transformers=include_transformers,
        limit=limit,
    )
    report_text = build_markdown_report(
        model.rid,
        sections,
        include_transformers=include_transformers,
    )
    export_report(report_text, report_path)
    print(f"已导出 EMT N-1 全扫描报告: {report_path}")


if __name__ == "__main__":
    main()
