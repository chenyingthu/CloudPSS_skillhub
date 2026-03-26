"""
CloudPSS EMT branch N-1 security screening example.

Run with:
  python examples/analysis/emt_n1_security_screening_example.py
  python examples/analysis/emt_n1_security_screening_example.py model/holdme/IEEE3
  python examples/analysis/emt_n1_security_screening_example.py --csv=emt-n1-security-screening.csv
  python examples/analysis/emt_n1_security_screening_example.py --conclusion-txt=emt-n1-security-screening.txt
  python examples/analysis/emt_n1_security_screening_example.py --validated-subset
  python examples/analysis/emt_n1_security_screening_example.py --lines-only --limit=3

This example stays intentionally narrow:
- ordinary cloud EMT only
- fixed validated IEEE3 fault path
- single branch outage (`N-1`) expressed by `props.enabled=False`
- monitored buses limited to `Bus7` (existing `vac`), `Bus2`, and `Bus8`
- generation-support diagnostic limited to `#P1`

The goal is not to claim a full transient-security platform, but to show one
credible EMT workflow that combines:
- branch outage enumeration
- repeated EMT runs under one fixed fault
- multi-bus recovery comparison
- compact engineering ranking and digest
"""

import csv
import importlib.util
from pathlib import Path
import sys

from cloudpss import setToken


CURRENT_DIR = Path(__file__).resolve().parent
STUDY_HELPER_PATH = CURRENT_DIR / "emt_fault_study_example.py"
MEASUREMENT_HELPER_PATH = CURRENT_DIR / "emt_measurement_workflow_example.py"
VOLTAGE_CHAIN_HELPER_PATH = CURRENT_DIR.parent / "basic" / "emt_voltage_meter_chain_example.py"

TRANSMISSION_LINE_RID = "model/CloudPSS/TransmissionLine"
TRANSFORMER_RID = "model/CloudPSS/_newTransformer_3p2w"
DEFAULT_EXPORT_PATH = "emt-n1-security-screening.csv"
DEFAULT_CONCLUSION_PATH = "emt-n1-security-screening.txt"
DEFAULT_VALIDATED_BRANCH_IDS = [
    "canvas_0_1096",  # Trans1
    "canvas_0_1074",  # tline4
    "canvas_0_1071",  # tline6
]
FAULT_BUS_TRACE = "vac:0"
BUS2_SIGNAL_NAME = "#bus2_n1"
BUS2_CHANNEL_NAME = "bus2_n1"
BUS8_SIGNAL_NAME = "#bus8_n1"
BUS8_CHANNEL_NAME = "bus8_n1"
P1_TRACE_NAME = "#P1:0"
P1_PREFAULT_WINDOW = (2.42, 2.44)
P1_FAULT_WINDOW = (2.64, 2.66)
P1_POSTFAULT_WINDOW = (2.96, 2.98)


def load_helper_module(module_path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


_STUDY_MODULE = load_helper_module(
    STUDY_HELPER_PATH,
    "emt_fault_study_example_shared_for_n1_security",
)
_MEASUREMENT_MODULE = load_helper_module(
    MEASUREMENT_HELPER_PATH,
    "emt_measurement_workflow_example_shared_for_n1_security",
)
_CHAIN_MODULE = load_helper_module(
    VOLTAGE_CHAIN_HELPER_PATH,
    "emt_voltage_meter_chain_example_shared_for_n1_security",
)

DEFAULT_MODEL_SOURCE = _STUDY_MODULE.DEFAULT_MODEL_SOURCE
load_model_from_source = _STUDY_MODULE.load_model_from_source
load_token = _STUDY_MODULE.load_token
prepare_fault_study_model = _STUDY_MODULE.prepare_fault_study_model
wait_for_completion = _STUDY_MODULE.wait_for_completion
extract_voltage_recovery_metrics = _STUDY_MODULE.extract_voltage_recovery_metrics
trace_window_rms = _MEASUREMENT_MODULE.trace_window_rms
trace_window_average = _MEASUREMENT_MODULE.trace_window_average
add_voltage_meter_chain = _CHAIN_MODULE.add_voltage_meter_chain


def describe_branch_component(component):
    return component.args.get("Name") or component.label or component.id


def classify_branch_component(component):
    if component.definition == TRANSFORMER_RID:
        return "transformer"
    return "line"


def discover_candidate_branches(model, include_transformers=True):
    rids = [TRANSMISSION_LINE_RID]
    if include_transformers:
        rids.append(TRANSFORMER_RID)

    candidates = []
    for rid in rids:
        for branch in model.getComponentsByRid(rid).values():
            candidates.append(
                {
                    "branch_id": branch.id,
                    "branch_name": describe_branch_component(branch),
                    "branch_kind": classify_branch_component(branch),
                    "enabled": branch.props.get("enabled", True),
                }
            )

    return sorted(candidates, key=lambda item: (item["branch_name"], item["branch_id"]))


def choose_candidate_branch_ids(
    model,
    use_all_discovered=True,
    include_transformers=True,
    limit=None,
):
    discovered = discover_candidate_branches(
        model,
        include_transformers=include_transformers,
    )
    discovered_ids = [item["branch_id"] for item in discovered if item["enabled"]]

    if use_all_discovered:
        chosen = discovered_ids
    else:
        chosen = [branch_id for branch_id in DEFAULT_VALIDATED_BRANCH_IDS if branch_id in discovered_ids]

    if limit is not None:
        chosen = chosen[:limit]

    return chosen


def collect_bus_metrics(trace):
    prefault_rms = trace_window_rms(trace, *_STUDY_MODULE.PREFAULT_WINDOW)
    fault_rms = trace_window_rms(trace, *_STUDY_MODULE.FAULT_WINDOW)
    postfault_rms = trace_window_rms(trace, *_STUDY_MODULE.POSTFAULT_WINDOW)
    late_recovery_rms = trace_window_rms(trace, *_STUDY_MODULE.LATE_RECOVERY_WINDOW)
    return {
        "prefault_rms": prefault_rms,
        "fault_rms": fault_rms,
        "postfault_rms": postfault_rms,
        "late_recovery_rms": late_recovery_rms,
        "fault_drop_vs_prefault": prefault_rms - fault_rms,
        "postfault_gap_vs_prefault": prefault_rms - postfault_rms,
        "late_recovery_gap_vs_prefault": prefault_rms - late_recovery_rms,
    }


def collect_p1_metrics(trace):
    prefault_avg = trace_window_average(trace, *P1_PREFAULT_WINDOW)
    fault_avg = trace_window_average(trace, *P1_FAULT_WINDOW)
    postfault_avg = trace_window_average(trace, *P1_POSTFAULT_WINDOW)
    return {
        "prefault_avg": prefault_avg,
        "fault_avg": fault_avg,
        "postfault_avg": postfault_avg,
    }


def run_security_case(model, branch_id=None):
    working_model = prepare_fault_study_model(
        model,
        fault_end_time="2.7",
        fault_chg="0.01",
        sampling_freq=2000,
    )

    branch_name = "baseline"
    branch_kind = "reference"
    if branch_id is not None:
        branch = working_model.getComponentByKey(branch_id)
        branch_name = describe_branch_component(branch)
        branch_kind = classify_branch_component(branch)
        working_model.updateComponent(branch_id, props={"enabled": False})

    bus2_chain = add_voltage_meter_chain(
        working_model,
        bus_name="Bus2",
        signal_name=BUS2_SIGNAL_NAME,
        channel_name=BUS2_CHANNEL_NAME,
        sampling_freq=2000,
    )
    bus8_chain = add_voltage_meter_chain(
        working_model,
        bus_name="Bus8",
        signal_name=BUS8_SIGNAL_NAME,
        channel_name=BUS8_CHANNEL_NAME,
        sampling_freq=2000,
    )

    job = working_model.runEMT()
    wait_for_completion(job)
    result = job.result

    bus7_metrics = extract_voltage_recovery_metrics(result, trace_name=FAULT_BUS_TRACE)
    bus2_trace = result.getPlotChannelData(bus2_chain["output_group_index"], f"{BUS2_CHANNEL_NAME}:0")
    bus8_trace = result.getPlotChannelData(bus8_chain["output_group_index"], f"{BUS8_CHANNEL_NAME}:0")
    p1_trace = result.getPlotChannelData(1, P1_TRACE_NAME)

    monitored_bus_metrics = {
        "Bus7": {
            **collect_bus_metrics(bus7_metrics["trace"]),
            "trace_name": FAULT_BUS_TRACE,
        },
        "Bus2": {
            **collect_bus_metrics(bus2_trace),
            "trace_name": f"{BUS2_CHANNEL_NAME}:0",
        },
        "Bus8": {
            **collect_bus_metrics(bus8_trace),
            "trace_name": f"{BUS8_CHANNEL_NAME}:0",
        },
    }
    p1_metrics = collect_p1_metrics(p1_trace)
    worst_postfault_gap = max(
        metrics["postfault_gap_vs_prefault"] for metrics in monitored_bus_metrics.values()
    )
    worst_late_gap = max(
        metrics["late_recovery_gap_vs_prefault"] for metrics in monitored_bus_metrics.values()
    )
    generator_support_lost = max(abs(value) for value in p1_metrics.values()) < 1.0

    return {
        "branch_id": branch_id or "baseline",
        "branch_name": branch_name,
        "branch_kind": branch_kind,
        "monitored_buses": monitored_bus_metrics,
        "p1_metrics": p1_metrics,
        "worst_postfault_gap": worst_postfault_gap,
        "worst_late_gap": worst_late_gap,
        "generator_support_lost": generator_support_lost,
    }


def classify_n1_security_severity(result):
    if result["generator_support_lost"]:
        return "critical"
    if result["worst_postfault_gap"] > 10.0 or result["worst_late_gap"] > 7.0:
        return "warning"
    return "observe"


def severity_rank_value(result):
    return {
        "critical": 2,
        "warning": 1,
        "observe": 0,
    }[classify_n1_security_severity(result)]


def rank_n1_security_results(results):
    return sorted(
        results,
        key=lambda item: (
            severity_rank_value(item),
            1 if item["generator_support_lost"] else 0,
            item["worst_postfault_gap"],
            item["worst_late_gap"],
            item["monitored_buses"]["Bus8"]["postfault_gap_vs_prefault"],
            item["monitored_buses"]["Bus7"]["postfault_gap_vs_prefault"],
        ),
        reverse=True,
    )


def run_branch_n1_security_scan(
    model,
    candidate_branch_ids=None,
    *,
    use_all_discovered=True,
    include_transformers=True,
    limit=None,
):
    candidate_branch_ids = candidate_branch_ids or choose_candidate_branch_ids(
        model,
        use_all_discovered=use_all_discovered,
        include_transformers=include_transformers,
        limit=limit,
    )

    baseline = run_security_case(model)
    results = []
    for branch_id in candidate_branch_ids:
        case_result = run_security_case(model, branch_id=branch_id)
        case_result["delta_worst_postfault_gap_vs_baseline"] = (
            case_result["worst_postfault_gap"] - baseline["worst_postfault_gap"]
        )
        case_result["delta_worst_late_gap_vs_baseline"] = (
            case_result["worst_late_gap"] - baseline["worst_late_gap"]
        )
        results.append(case_result)

    ranked_results = rank_n1_security_results(results)
    for index, result in enumerate(ranked_results, start=1):
        result["severity"] = classify_n1_security_severity(result)
        result["rank"] = index

    return baseline, ranked_results


def _format_signed(value):
    return f"{value:+.3f}"


def build_summary_rows(baseline, results):
    rows = []
    for result in results:
        bus7 = result["monitored_buses"]["Bus7"]
        bus2 = result["monitored_buses"]["Bus2"]
        bus8 = result["monitored_buses"]["Bus8"]
        p1 = result["p1_metrics"]
        rows.append(
            {
                "rank": str(result["rank"]),
                "branch_id": result["branch_id"],
                "branch_name": result["branch_name"],
                "branch_kind": result["branch_kind"],
                "severity": result["severity"],
                "generator_support_lost": "yes" if result["generator_support_lost"] else "no",
                "bus7_postfault_gap": f"{bus7['postfault_gap_vs_prefault']:.3f}",
                "bus7_late_gap": f"{bus7['late_recovery_gap_vs_prefault']:.3f}",
                "bus2_postfault_gap": f"{bus2['postfault_gap_vs_prefault']:.3f}",
                "bus8_postfault_gap": f"{bus8['postfault_gap_vs_prefault']:.3f}",
                "bus8_late_gap": f"{bus8['late_recovery_gap_vs_prefault']:.3f}",
                "worst_postfault_gap": f"{result['worst_postfault_gap']:.3f}",
                "worst_late_gap": f"{result['worst_late_gap']:.3f}",
                "delta_worst_postfault_gap_vs_baseline": _format_signed(
                    result["delta_worst_postfault_gap_vs_baseline"]
                ),
                "delta_worst_late_gap_vs_baseline": _format_signed(
                    result["delta_worst_late_gap_vs_baseline"]
                ),
                "p1_prefault_avg": f"{p1['prefault_avg']:.3f}",
                "p1_fault_avg": f"{p1['fault_avg']:.3f}",
                "p1_postfault_avg": f"{p1['postfault_avg']:.3f}",
                "baseline_worst_postfault_gap": f"{baseline['worst_postfault_gap']:.3f}",
            }
        )
    return rows


def build_screening_digest(baseline, results):
    severity_counts = {"critical": 0, "warning": 0, "observe": 0}
    branch_kind_counts = {"line": 0, "transformer": 0}
    for result in results:
        severity_counts[result["severity"]] += 1
        if result["branch_kind"] in branch_kind_counts:
            branch_kind_counts[result["branch_kind"]] += 1

    def first_matching(branch_kind):
        for result in results:
            if result["branch_kind"] == branch_kind:
                return result
        return None

    return {
        "baseline": baseline,
        "total_cases": len(results),
        "severity_counts": severity_counts,
        "branch_kind_counts": branch_kind_counts,
        "top_case": results[0] if results else None,
        "top_line_case": first_matching("line"),
        "top_transformer_case": first_matching("transformer"),
        "largest_worsening_case": (
            max(results, key=lambda item: item["delta_worst_postfault_gap_vs_baseline"])
            if results
            else None
        ),
        "mildest_case": (
            min(
                results,
                key=lambda item: (
                    item["worst_postfault_gap"],
                    item["worst_late_gap"],
                    1 if item["generator_support_lost"] else 0,
                ),
            )
            if results
            else None
        ),
        "max_bus2_gap": (
            max(result["monitored_buses"]["Bus2"]["postfault_gap_vs_prefault"] for result in results)
            if results
            else None
        ),
    }


def build_conclusion_report(baseline, results, digest):
    top_case = digest["top_case"]
    top_line_case = digest["top_line_case"]
    mildest_case = digest["mildest_case"]
    max_bus2_gap = digest["max_bus2_gap"] or 0.0

    findings = []
    if top_case is not None:
        findings.append(
            {
                "title": f"{top_case['branch_name']} 是当前扫描里最不安全的 N-1 工况",
                "supported": top_case["generator_support_lost"]
                and top_case["delta_worst_postfault_gap_vs_baseline"] > 1.0,
                "evidence": (
                    f"worst_post_gap {baseline['worst_postfault_gap']:.3f} -> "
                    f"{top_case['worst_postfault_gap']:.3f} V, "
                    f"#P1 {top_case['p1_metrics']['prefault_avg']:.3f} -> "
                    f"{top_case['p1_metrics']['fault_avg']:.3f} -> "
                    f"{top_case['p1_metrics']['postfault_avg']:.3f}"
                ),
            }
        )

    if top_line_case is not None and mildest_case is not None:
        findings.append(
            {
                "title": f"在线路子集里，{top_line_case['branch_name']} 的恢复压力明显重于 {mildest_case['branch_name']}",
                "supported": top_line_case["worst_postfault_gap"] > mildest_case["worst_postfault_gap"] + 5.0,
                "evidence": (
                    f"{top_line_case['branch_name']} worst_post={top_line_case['worst_postfault_gap']:.3f} V, "
                    f"{mildest_case['branch_name']} worst_post={mildest_case['worst_postfault_gap']:.3f} V"
                ),
            }
        )

    if mildest_case is not None:
        findings.append(
            {
                "title": f"{mildest_case['branch_name']} 是当前扫描里最轻的 N-1 工况",
                "supported": mildest_case["delta_worst_postfault_gap_vs_baseline"] < -5.0,
                "evidence": (
                    f"baseline worst_post={baseline['worst_postfault_gap']:.3f} V, "
                    f"{mildest_case['branch_name']} worst_post={mildest_case['worst_postfault_gap']:.3f} V, "
                    f"worst_late={mildest_case['worst_late_gap']:.3f} V"
                ),
            }
        )

    findings.append(
        {
            "title": "远端支撑母线 Bus2 在当前扫描里始终保持较小的后故障恢复缺口",
            "supported": max_bus2_gap < 0.5,
            "evidence": f"max Bus2 postfault gap across scan = {max_bus2_gap:.3f} V",
        }
    )

    return {
        "research_question": (
            "在同一 IEEE3 固定故障上，如果先执行单支路/单变压器 N-1 停运，"
            "再运行 EMT，那么哪些工况会最明显削弱故障后电压恢复和机组支撑？"
        ),
        "criteria": [
            "若某个停运工况的 `worst_postfault_gap` 与 `worst_late_gap` 更大，则说明在当前监测母线集上恢复更弱。",
            "若 `#P1` 在故障前/中/后都接近零，则把它视为机组支撑路径显著丢失的强告警信号。",
            "若 `Bus2` 的恢复缺口始终很小，则说明当前冲击主要集中在局部故障侧与负荷侧母线，而不是全系统均匀恶化。",
        ],
        "findings": findings,
        "overall_conclusion": (
            "当前 live 结果支持把这条 IEEE3 工作线视为一条可复验的 EMT N-1 安全筛查模板："
            "可先枚举单支路停运，再在固定故障下比较多母线恢复缺口和 `#P1` 支撑读数，"
            "并据此形成排序与研究摘要。"
        ),
        "boundary": (
            "本结论当前只对 model/holdme/IEEE3、固定 `_newFaultResistor_3p` 故障配置、"
            "监测母线 Bus7/Bus2/Bus8、`#P1` 通道、以及默认发现到的 6 条线路 + 3 台变压器 N-1 工况成立。"
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
        "rank",
        "branch_id",
        "branch_name",
        "branch_kind",
        "severity",
        "generator_support_lost",
        "bus7_postfault_gap",
        "bus7_late_gap",
        "bus2_postfault_gap",
        "bus8_postfault_gap",
        "bus8_late_gap",
        "worst_postfault_gap",
        "worst_late_gap",
        "delta_worst_postfault_gap_vs_baseline",
        "delta_worst_late_gap_vs_baseline",
        "p1_prefault_avg",
        "p1_fault_avg",
        "p1_postfault_avg",
        "baseline_worst_postfault_gap",
    ]
    with open(path, "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def export_conclusion_report(report, path):
    with open(path, "w", encoding="utf-8") as output_file:
        output_file.write(format_conclusion_report(report))
        output_file.write("\n")


def print_baseline_reference(baseline):
    bus7 = baseline["monitored_buses"]["Bus7"]
    bus2 = baseline["monitored_buses"]["Bus2"]
    bus8 = baseline["monitored_buses"]["Bus8"]
    p1 = baseline["p1_metrics"]
    print("\n=== 基线故障参考 ===")
    print(
        f"Bus7 post_gap={bus7['postfault_gap_vs_prefault']:.3f} "
        f"late_gap={bus7['late_recovery_gap_vs_prefault']:.3f}"
    )
    print(
        f"Bus2 post_gap={bus2['postfault_gap_vs_prefault']:.3f} "
        f"late_gap={bus2['late_recovery_gap_vs_prefault']:.3f}"
    )
    print(
        f"Bus8 post_gap={bus8['postfault_gap_vs_prefault']:.3f} "
        f"late_gap={bus8['late_recovery_gap_vs_prefault']:.3f}"
    )
    print(
        f"#P1 avg={p1['prefault_avg']:.3f}->{p1['fault_avg']:.3f}->{p1['postfault_avg']:.3f}"
    )
    print(
        f"worst_post_gap={baseline['worst_postfault_gap']:.3f} "
        f"worst_late_gap={baseline['worst_late_gap']:.3f}"
    )


def print_screening_digest(digest):
    if digest["top_case"] is None:
        print("\n=== EMT N-1 安全摘要 ===")
        print("没有可输出的筛查结果。")
        return

    print("\n=== EMT N-1 安全摘要 ===")
    print(
        "工况总数: "
        f"{digest['total_cases']} "
        f"(line={digest['branch_kind_counts']['line']}, "
        f"transformer={digest['branch_kind_counts']['transformer']})"
    )
    print(
        "严重性分布: "
        f"critical={digest['severity_counts']['critical']}, "
        f"warning={digest['severity_counts']['warning']}, "
        f"observe={digest['severity_counts']['observe']}"
    )

    for label, item in [
        ("总榜首位", digest["top_case"]),
        ("线路首位", digest["top_line_case"]),
        ("变压器首位", digest["top_transformer_case"]),
        ("基线最明显恶化工况", digest["largest_worsening_case"]),
        ("最轻工况", digest["mildest_case"]),
    ]:
        if item is None:
            continue
        print(
            f"{label}: {item['branch_name']} ({item['branch_id']}, {item['branch_kind']}) "
            f"severity={item['severity']} "
            f"worst_post={item['worst_postfault_gap']:.3f} "
            f"worst_late={item['worst_late_gap']:.3f} "
            f"delta_post={item['delta_worst_postfault_gap_vs_baseline']:+.3f} "
            f"P1={item['p1_metrics']['prefault_avg']:.1f}->{item['p1_metrics']['fault_avg']:.1f}->{item['p1_metrics']['postfault_avg']:.1f}"
        )


def print_summary_table(rows):
    headers = [
        "rank",
        "branch_name",
        "branch_kind",
        "severity",
        "generator_support_lost",
        "bus7_postfault_gap",
        "bus8_postfault_gap",
        "worst_postfault_gap",
        "worst_late_gap",
        "delta_worst_postfault_gap_vs_baseline",
        "p1_postfault_avg",
    ]
    print("\n=== EMT N-1 安全筛查汇总 ===")
    print(" | ".join(headers))
    print("-" * 128)
    for row in rows:
        print(" | ".join(row[header] for header in headers))


def parse_args(argv):
    source = DEFAULT_MODEL_SOURCE
    csv_path = None
    conclusion_path = None
    use_all_discovered = True
    include_transformers = True
    limit = None

    for arg in argv:
        if arg == "--validated-subset":
            use_all_discovered = False
            continue
        if arg == "--lines-only":
            include_transformers = False
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

    return source, csv_path, conclusion_path, use_all_discovered, include_transformers, limit


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    (
        source,
        csv_path,
        conclusion_path,
        use_all_discovered,
        include_transformers,
        limit,
    ) = parse_args(argv)

    setToken(load_token())
    model = load_model_from_source(source)

    print(f"研究模型: {model.rid}")
    candidate_branch_ids = choose_candidate_branch_ids(
        model,
        use_all_discovered=use_all_discovered,
        include_transformers=include_transformers,
        limit=limit,
    )
    print(f"候选支路总数: {len(candidate_branch_ids)}")
    print(f"筛查支路: {', '.join(candidate_branch_ids)}")
    if use_all_discovered and include_transformers:
        print("说明: 当前默认扫描 IEEE3 已发现的线路和变压器 N-1 工况。")
    elif use_all_discovered:
        print("说明: 当前仅扫描 IEEE3 已发现的线路 N-1 工况。")
    else:
        print("说明: 当前仅扫描较小的已验证代表性子集。")

    baseline, results = run_branch_n1_security_scan(
        model,
        candidate_branch_ids=candidate_branch_ids,
    )
    rows = build_summary_rows(baseline, results)
    digest = build_screening_digest(baseline, results)
    report = build_conclusion_report(baseline, results, digest)

    print_baseline_reference(baseline)
    print_screening_digest(digest)
    print_summary_table(rows)

    csv_path = csv_path or DEFAULT_EXPORT_PATH
    export_summary_rows_csv(rows, csv_path)
    print(f"\n已导出筛查摘要: {csv_path}")

    conclusion_path = conclusion_path or DEFAULT_CONCLUSION_PATH
    export_conclusion_report(report, conclusion_path)
    print(f"已导出研究结论: {conclusion_path}")

    print("\n" + format_conclusion_report(report))


if __name__ == "__main__":
    main()
