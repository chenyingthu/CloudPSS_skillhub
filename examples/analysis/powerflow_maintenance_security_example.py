"""
CloudPSS maintenance-state power-flow security check example.

Run with:
  python examples/analysis/powerflow_maintenance_security_example.py
  python examples/analysis/powerflow_maintenance_security_example.py model/holdme/IEEE39
  python examples/analysis/powerflow_maintenance_security_example.py --maintenance-branch=canvas_0_126
  python examples/analysis/powerflow_maintenance_security_example.py --maintenance-branch=canvas_0_47
  python examples/analysis/powerflow_maintenance_security_example.py --csv=maintenance-security.csv
  python examples/analysis/powerflow_maintenance_security_example.py --conclusion-txt=maintenance-security.txt
  python examples/analysis/powerflow_maintenance_security_example.py --all-discovered
  python examples/analysis/powerflow_maintenance_security_example.py --lines-only --limit=5

Current scope is intentionally constrained:
- ordinary cloud power-flow only
- one planned branch outage expressed by `props.enabled=False`
- residual N-1 review stays on IEEE39 and reuses the current constrained criteria
- default follow-up subset stays inside the already validated branch universe
- validated planned-outage samples currently include one line and one transformer
"""

import csv
from copy import deepcopy
import importlib.util
from pathlib import Path
import sys

from cloudpss import Model, setToken


CURRENT_DIR = Path(__file__).resolve().parent
N1_MODULE_PATH = CURRENT_DIR / "powerflow_n1_screening_example.py"


def load_helper_module(module_path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


N1_MODULE = load_helper_module(
    N1_MODULE_PATH,
    "powerflow_n1_screening_example_for_maintenance_security",
)

DEFAULT_MODEL_SOURCE = N1_MODULE.DEFAULT_READONLY_MODEL_RID
DEFAULT_MAINTENANCE_BRANCH_ID = "canvas_0_126"
DEFAULT_VALIDATED_FOLLOWUP_BRANCH_IDS = [
    "canvas_0_134",
    "canvas_0_130",
    "canvas_0_47",
]
DEFAULT_EXPORT_PATH = "powerflow-maintenance-security-summary.csv"
DEFAULT_CONCLUSION_PATH = "powerflow-maintenance-security.txt"

load_token = N1_MODULE.load_token
load_model_from_source = N1_MODULE.load_model_from_source
run_powerflow_tables = N1_MODULE.run_powerflow_tables
discover_candidate_branches = N1_MODULE.discover_candidate_branches
filter_candidate_branches_by_base_presence = N1_MODULE.filter_candidate_branches_by_base_presence
describe_branch_component = N1_MODULE.describe_branch_component
classify_branch_component = N1_MODULE.classify_branch_component
disable_branch_outage = N1_MODULE.disable_branch_outage
compute_n1_delta_metrics = N1_MODULE.compute_n1_delta_metrics
classify_n1_severity = N1_MODULE.classify_n1_severity
screen_n1_branches = N1_MODULE.screen_n1_branches
build_screening_digest = N1_MODULE.build_screening_digest
print_screening_digest = N1_MODULE.print_screening_digest
print_summary_table = N1_MODULE.print_summary_table


def parse_args(argv):
    source = DEFAULT_MODEL_SOURCE
    maintenance_branch_id = DEFAULT_MAINTENANCE_BRANCH_ID
    use_all_discovered = False
    include_transformers = True
    limit = None
    csv_path = DEFAULT_EXPORT_PATH
    conclusion_path = DEFAULT_CONCLUSION_PATH

    for arg in argv:
        if arg == "--all-discovered":
            use_all_discovered = True
            continue
        if arg == "--validated-subset":
            use_all_discovered = False
            continue
        if arg == "--lines-only":
            include_transformers = False
            continue
        if arg.startswith("--maintenance-branch="):
            maintenance_branch_id = arg.split("=", 1)[1].strip()
            continue
        if arg.startswith("--csv="):
            csv_path = arg.split("=", 1)[1].strip()
            continue
        if arg.startswith("--conclusion-txt="):
            conclusion_path = arg.split("=", 1)[1].strip()
            continue
        if arg.startswith("--limit="):
            limit = int(arg.split("=", 1)[1].strip())
            continue
        source = arg

    return (
        source,
        maintenance_branch_id,
        use_all_discovered,
        include_transformers,
        limit,
        csv_path,
        conclusion_path,
    )


def choose_followup_branch_ids(
    model,
    maintenance_branch_id,
    *,
    use_all_discovered=False,
    include_transformers=True,
    limit=None,
    base_branch_ids=None,
):
    discovered = discover_candidate_branches(
        model,
        include_transformers=include_transformers,
    )
    active_candidates, _ = filter_candidate_branches_by_base_presence(
        discovered,
        base_branch_ids=base_branch_ids,
    )
    active_ids = [
        item["branch_id"]
        for item in active_candidates
        if item["enabled"] and item["branch_id"] != maintenance_branch_id
    ]

    if use_all_discovered:
        chosen = active_ids
    else:
        chosen = [
            branch_id
            for branch_id in DEFAULT_VALIDATED_FOLLOWUP_BRANCH_IDS
            if branch_id in active_ids and branch_id != maintenance_branch_id
        ]

    if limit is not None:
        chosen = chosen[:limit]

    return chosen


def assess_maintenance_case(model, maintenance_branch_id, *, base_buses=None, base_branches=None):
    if base_buses is None or base_branches is None:
        base_buses, base_branches = run_powerflow_tables(model)

    working_model = Model(deepcopy(model.toJSON()))
    maintenance_branch = working_model.getComponentByKey(maintenance_branch_id)
    maintenance_branch_name = describe_branch_component(maintenance_branch)
    maintenance_branch_kind = classify_branch_component(maintenance_branch)

    disable_branch_outage(working_model, maintenance_branch_id)
    outage_buses, outage_branches = run_powerflow_tables(working_model)
    delta_metrics = compute_n1_delta_metrics(
        base_buses=base_buses,
        base_branches=base_branches,
        outage_buses=outage_buses,
        outage_branches=outage_branches,
    )

    maintenance_case = {
        "branch_id": maintenance_branch_id,
        "branch_name": maintenance_branch_name,
        "branch_kind": maintenance_branch_kind,
        "branch_present_after_outage": any(
            row[N1_MODULE.BRANCH_COLUMN] == maintenance_branch_id for row in outage_branches
        ),
        **delta_metrics,
    }
    maintenance_case["severity"] = classify_n1_severity(maintenance_case)

    return working_model, maintenance_case, outage_buses, outage_branches


def build_summary_rows(assessment):
    maintenance_case = assessment["maintenance_case"]
    rows = []
    for row in N1_MODULE.build_summary_rows(assessment["followup_results"]):
        rows.append(
            {
                "maintenance_branch_id": maintenance_case["branch_id"],
                "maintenance_branch_name": maintenance_case["branch_name"],
                "maintenance_branch_kind": maintenance_case["branch_kind"],
                "maintenance_severity": maintenance_case["severity"],
                "maintenance_min_vm": f"{maintenance_case['min_vm']:.4f}",
                **row,
            }
        )
    return rows


def build_conclusion_report(assessment):
    maintenance_case = assessment["maintenance_case"]
    digest = assessment["followup_digest"]
    top_case = digest["top_case"]

    findings = [
        {
            "title": f"计划停运 {maintenance_case['branch_name']} 后仍可形成一组可复核的潮流结果",
            "supported": not maintenance_case["branch_present_after_outage"],
            "evidence": (
                f"severity={maintenance_case['severity']}, "
                f"min_vm={maintenance_case['min_vm']:.4f}@{maintenance_case['min_vm_bus_id']}, "
                f"missing_bus_count={maintenance_case['missing_bus_count']}, "
                f"max_branch_shift={maintenance_case['max_branch_shift']:.3f}"
            ),
        }
    ]

    if top_case is not None:
        findings.append(
            {
                "title": f"检修状态下最重的残余 N-1 工况是 {top_case['branch_name']}",
                "supported": True,
                "evidence": (
                    f"severity={top_case['severity']}, "
                    f"min_vm={top_case['min_vm']:.4f}@{top_case['min_vm_bus_id']}, "
                    f"new_low_voltage_bus_count={top_case['new_low_voltage_bus_count']}, "
                    f"max_branch_shift={top_case['max_branch_shift']:.3f}@"
                    f"{top_case['max_branch_shift_branch_id'] or '-'}"
                ),
            }
        )
        findings.append(
            {
                "title": "残余 N-1 复核会在当前检修基线上继续暴露更弱的支路停运组合",
                "supported": (
                    top_case["new_low_voltage_bus_count"] > 0
                    or top_case["new_high_voltage_bus_count"] > 0
                    or top_case["min_vm"] < maintenance_case["min_vm"] - 1e-6
                    or top_case["max_branch_shift"] > maintenance_case["max_branch_shift"] + 1.0
                ),
                "evidence": (
                    f"maintenance min_vm={maintenance_case['min_vm']:.4f}, "
                    f"top residual min_vm={top_case['min_vm']:.4f}; "
                    f"maintenance max_branch_shift={maintenance_case['max_branch_shift']:.3f}, "
                    f"top residual max_branch_shift={top_case['max_branch_shift']:.3f}"
                ),
            }
        )
    else:
        findings.append(
            {
                "title": "当前检修工况下仍有可继续复核的残余 N-1 候选支路",
                "supported": False,
                "evidence": "当前筛查候选集为空，无法继续形成残余 N-1 排序。",
            }
        )

    return {
        "research_question": (
            "在 IEEE39 的一个计划检修停运工况下，系统本身是否仍可形成可读潮流结果，"
            "并且在该检修状态上继续做受限 N-1 复核时，哪些残余支路会成为更敏感的风险点？"
        ),
        "criteria": [
            "先对计划检修支路执行 `props.enabled=False`，确认停运后潮流结果表仍可读取。",
            "再把检修态作为新的比较基线，对剩余候选支路逐条执行受限 N-1 筛查。",
            "严重性仍按当前仓库的受限判据解释：新增电压越限、最低电压、最大电压偏移和最大潮流偏移。",
        ],
        "findings": findings,
        "overall_conclusion": (
            "当前结果支持把这条 IEEE39 检修方式校核路径视为现有潮流主线的受限增强："
            "可先建立一个计划停运工况，再在该工况上继续做残余 N-1 复核，并输出排序与简要结论。"
        ),
        "boundary": (
            "本结论当前只对 model/holdme/IEEE39、普通云潮流、`props.enabled=False` 的计划停运表达、"
            "以及当前示例所使用的残余支路候选集成立，不等价于完整的调度级检修校核平台。"
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


def export_summary_rows_csv(rows, path):
    fieldnames = [
        "maintenance_branch_id",
        "maintenance_branch_name",
        "maintenance_branch_kind",
        "maintenance_severity",
        "maintenance_min_vm",
        "rank",
        "branch_id",
        "branch_name",
        "branch_kind",
        "severity",
        "branch_present_after_outage",
        "min_vm",
        "min_vm_bus_id",
        "new_low_voltage_bus_count",
        "new_low_voltage_buses",
        "new_high_voltage_bus_count",
        "new_high_voltage_buses",
        "missing_bus_count",
        "missing_bus_ids",
        "missing_branch_count",
        "missing_branch_ids",
        "max_vm_shift",
        "max_vm_shift_bus_id",
        "max_branch_shift",
        "max_branch_shift_branch_id",
    ]
    with open(path, "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def export_conclusion_report(report, path):
    with open(path, "w", encoding="utf-8") as output_file:
        output_file.write(format_conclusion_report(report))
        output_file.write("\n")


def print_maintenance_reference(maintenance_case):
    print("\n=== 检修态参考 ===")
    print(
        f"planned_outage={maintenance_case['branch_name']} "
        f"({maintenance_case['branch_id']}, {maintenance_case['branch_kind']})"
    )
    print(
        f"severity={maintenance_case['severity']} "
        f"min_vm={maintenance_case['min_vm']:.4f}@{maintenance_case['min_vm_bus_id']} "
        f"missing_bus_count={maintenance_case['missing_bus_count']} "
        f"max_vm_shift={maintenance_case['max_vm_shift']:.4f}@"
        f"{maintenance_case['max_vm_shift_bus_id'] or '-'} "
        f"max_branch_shift={maintenance_case['max_branch_shift']:.3f}@"
        f"{maintenance_case['max_branch_shift_branch_id'] or '-'}"
    )


def run_maintenance_security_assessment(
    model,
    *,
    maintenance_branch_id=DEFAULT_MAINTENANCE_BRANCH_ID,
    use_all_discovered=False,
    include_transformers=True,
    limit=None,
):
    base_buses, base_branches = run_powerflow_tables(model)
    maintenance_model, maintenance_case, maintenance_buses, maintenance_branches = assess_maintenance_case(
        model,
        maintenance_branch_id,
        base_buses=base_buses,
        base_branches=base_branches,
    )

    maintenance_branch_ids = {row[N1_MODULE.BRANCH_COLUMN] for row in maintenance_branches}
    followup_branch_ids = choose_followup_branch_ids(
        maintenance_model,
        maintenance_branch_id,
        use_all_discovered=use_all_discovered,
        include_transformers=include_transformers,
        limit=limit,
        base_branch_ids=maintenance_branch_ids,
    )
    followup_results = screen_n1_branches(
        maintenance_model,
        followup_branch_ids,
        base_buses=maintenance_buses,
        base_branches=maintenance_branches,
    )
    followup_digest = build_screening_digest(followup_results)

    assessment = {
        "maintenance_case": maintenance_case,
        "followup_branch_ids": followup_branch_ids,
        "followup_results": followup_results,
        "followup_digest": followup_digest,
    }
    assessment["summary_rows"] = build_summary_rows(assessment)
    assessment["conclusion_report"] = build_conclusion_report(assessment)
    return assessment


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    (
        source,
        maintenance_branch_id,
        use_all_discovered,
        include_transformers,
        limit,
        csv_path,
        conclusion_path,
    ) = parse_args(argv)

    setToken(load_token())
    model = load_model_from_source(source)

    print("CloudPSS 检修方式潮流安全校核示例")
    print("=" * 50)
    print(f"模型来源: {source}")
    print(f"模型名称: {model.name}")
    print(f"计划停运支路: {maintenance_branch_id}")
    if use_all_discovered and include_transformers:
        print("残余复核范围: 检修态下全部已发现线路和变压器")
    elif use_all_discovered:
        print("残余复核范围: 检修态下全部已发现线路")
    else:
        print("残余复核范围: 检修态下已验证的小子集")

    assessment = run_maintenance_security_assessment(
        model,
        maintenance_branch_id=maintenance_branch_id,
        use_all_discovered=use_all_discovered,
        include_transformers=include_transformers,
        limit=limit,
    )
    print_maintenance_reference(assessment["maintenance_case"])
    print_screening_digest(assessment["followup_digest"])
    print_summary_table(assessment["summary_rows"])

    export_summary_rows_csv(assessment["summary_rows"], csv_path)
    export_conclusion_report(assessment["conclusion_report"], conclusion_path)
    print(f"已导出检修态残余 N-1 摘要: {csv_path}")
    print(f"已导出检修方式结论: {conclusion_path}")


if __name__ == "__main__":
    main()
