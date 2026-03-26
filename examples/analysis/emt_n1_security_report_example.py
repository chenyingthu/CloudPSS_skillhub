"""
CloudPSS EMT N-1 security report example.

Run with:
  python examples/analysis/emt_n1_security_report_example.py
  python examples/analysis/emt_n1_security_report_example.py model/holdme/IEEE3
  python examples/analysis/emt_n1_security_report_example.py --report=emt-n1-security-report.md
  python examples/analysis/emt_n1_security_report_example.py --all-discovered

This example turns the validated EMT N-1 screening path into a report-style
deliverable. By default it focuses on the representative validated subset:
- `Trans1`: most severe transformer outage
- `tline4`: most severe line outage
- `tline6`: mildest outage
"""

import importlib.util
from pathlib import Path
import sys

from cloudpss import setToken


CURRENT_DIR = Path(__file__).resolve().parent
N1_MODULE_PATH = CURRENT_DIR / "emt_n1_security_screening_example.py"


def load_helper_module(module_path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


N1_MODULE = load_helper_module(
    N1_MODULE_PATH,
    "emt_n1_security_screening_example_for_report",
)

DEFAULT_MODEL_SOURCE = N1_MODULE.DEFAULT_MODEL_SOURCE
DEFAULT_REPORT_PATH = "emt-n1-security-report.md"


def parse_args(argv):
    source = DEFAULT_MODEL_SOURCE
    report_path = DEFAULT_REPORT_PATH
    use_all_discovered = False
    include_transformers = True
    limit = None

    for arg in argv:
        if arg == "--all-discovered":
            use_all_discovered = True
            continue
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

    return source, report_path, use_all_discovered, include_transformers, limit


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


def build_case_highlights(digest):
    highlights = []
    for label, item in [
        ("Top Case", digest["top_case"]),
        ("Top Line", digest["top_line_case"]),
        ("Top Transformer", digest["top_transformer_case"]),
        ("Mildest Case", digest["mildest_case"]),
    ]:
        if item is None:
            continue
        highlights.append(
            {
                "label": label,
                "branch_name": item["branch_name"],
                "branch_kind": item["branch_kind"],
                "severity": item["severity"],
                "worst_postfault_gap": f"{item['worst_postfault_gap']:.3f}",
                "worst_late_gap": f"{item['worst_late_gap']:.3f}",
                "p1_postfault_avg": f"{item['p1_metrics']['postfault_avg']:.3f}",
            }
        )
    return highlights


def build_report_sections(model, *, use_all_discovered, include_transformers, limit):
    baseline, results = N1_MODULE.run_branch_n1_security_scan(
        model,
        use_all_discovered=use_all_discovered,
        include_transformers=include_transformers,
        limit=limit,
    )
    summary_rows = N1_MODULE.build_summary_rows(baseline, results)
    digest = N1_MODULE.build_screening_digest(baseline, results)
    conclusion_report = N1_MODULE.build_conclusion_report(baseline, results, digest)

    baseline_rows = [
        {
            "bus": "Bus7",
            "postfault_gap": f"{baseline['monitored_buses']['Bus7']['postfault_gap_vs_prefault']:.3f}",
            "late_gap": f"{baseline['monitored_buses']['Bus7']['late_recovery_gap_vs_prefault']:.3f}",
        },
        {
            "bus": "Bus2",
            "postfault_gap": f"{baseline['monitored_buses']['Bus2']['postfault_gap_vs_prefault']:.3f}",
            "late_gap": f"{baseline['monitored_buses']['Bus2']['late_recovery_gap_vs_prefault']:.3f}",
        },
        {
            "bus": "Bus8",
            "postfault_gap": f"{baseline['monitored_buses']['Bus8']['postfault_gap_vs_prefault']:.3f}",
            "late_gap": f"{baseline['monitored_buses']['Bus8']['late_recovery_gap_vs_prefault']:.3f}",
        },
    ]

    return {
        "baseline": baseline,
        "baseline_rows": baseline_rows,
        "digest": digest,
        "highlight_rows": build_case_highlights(digest),
        "summary_rows": summary_rows,
        "conclusion_report": conclusion_report,
    }


def build_markdown_report(model_rid, sections, *, use_all_discovered):
    scope = (
        "full discovered IEEE3 line + transformer N-1 scan"
        if use_all_discovered
        else "validated representative IEEE3 N-1 subset"
    )
    baseline = sections["baseline"]
    digest = sections["digest"]

    lines = [
        "# CloudPSS EMT N-1 Security Report",
        "",
        f"- Model: `{model_rid}`",
        f"- Scope: {scope}",
        "",
        "## Executive Summary",
        "",
        "- This report turns the validated IEEE3 EMT N-1 screening path into a conclusion-first study deliverable.",
        "- It compares outage severity through multi-bus recovery gaps on Bus7, Bus2, and Bus8, while retaining `#P1` as a generator-support diagnostic.",
        f"- Baseline worst post-fault gap = `{baseline['worst_postfault_gap']:.3f}` V; worst late gap = `{baseline['worst_late_gap']:.3f}` V.",
        "",
        "## Baseline Reference",
        "",
        markdown_table(sections["baseline_rows"]).rstrip(),
        "",
        "## Representative Cases",
        "",
        markdown_table(sections["highlight_rows"]).rstrip(),
        "",
        "## Ranked Screening Table",
        "",
        markdown_table(sections["summary_rows"]).rstrip(),
        "",
        "## Screening Digest",
        "",
        f"- Total cases: `{digest['total_cases']}`",
        f"- Severity counts: `critical={digest['severity_counts']['critical']}`, `warning={digest['severity_counts']['warning']}`, `observe={digest['severity_counts']['observe']}`",
        "",
        "## Conclusions",
        "",
        N1_MODULE.format_conclusion_report(sections["conclusion_report"]),
        "",
    ]
    return "\n".join(lines)


def export_report(report_text, path):
    with open(path, "w", encoding="utf-8") as output_file:
        output_file.write(report_text)
        output_file.write("\n")


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    source, report_path, use_all_discovered, include_transformers, limit = parse_args(argv)

    setToken(N1_MODULE.load_token())
    model = N1_MODULE.load_model_from_source(source)

    print(f"研究模型: {model.rid}")
    sections = build_report_sections(
        model,
        use_all_discovered=use_all_discovered,
        include_transformers=include_transformers,
        limit=limit,
    )
    report_text = build_markdown_report(
        model.rid,
        sections,
        use_all_discovered=use_all_discovered,
    )
    export_report(report_text, report_path)
    print(f"已导出 EMT N-1 研究报告: {report_path}")


if __name__ == "__main__":
    main()
