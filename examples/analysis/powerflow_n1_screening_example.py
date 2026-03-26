"""
CloudPSS constrained N-1 power-flow screening example.

Run with:
  python examples/analysis/powerflow_n1_screening_example.py
  python examples/analysis/powerflow_n1_screening_example.py model/holdme/IEEE39
  python examples/analysis/powerflow_n1_screening_example.py study-case.yaml

Current scope is intentionally constrained:
- ordinary cloud power-flow only
- baseline-active branch outage only
- default candidate set includes TransmissionLine + _newTransformer_3p2w
- full IEEE39 baseline-active branch set has live evidence
- broader models still need their own validation
"""

import os
import csv
from copy import deepcopy
from pathlib import Path
import sys
import time

from cloudpss import Model, setToken


DEFAULT_READONLY_MODEL_RID = os.environ.get("TEST_MODEL_RID", "model/holdme/IEEE39")
DEFAULT_VALIDATED_BRANCH_IDS = ["canvas_0_126", "canvas_0_134", "canvas_0_130", "canvas_0_47"]
TRANSMISSION_LINE_RID = "model/CloudPSS/TransmissionLine"
TRANSFORMER_RID = "model/CloudPSS/_newTransformer_3p2w"
DEFAULT_EXPORT_PATH = "powerflow-n1-screening-summary.csv"
BUS_COLUMN = "Bus"
VM_COLUMN = "<i>V</i><sub>m</sub> / pu"
BRANCH_COLUMN = "Branch"
P_IJ_COLUMN = "<i>P</i><sub>ij</sub> / MW"
VM_LOW_LIMIT = 0.95
VM_HIGH_LIMIT = 1.05


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


def wait_for_completion(job, timeout=300, interval=2):
    start_time = time.time()
    while True:
        status = job.status()
        if status == 1:
            return
        if status == 2:
            raise RuntimeError("潮流计算失败")
        if time.time() - start_time > timeout:
            raise TimeoutError("潮流计算超时")
        time.sleep(interval)


def table_rows(table):
    columns = table["data"]["columns"]
    labels = [column.get("name") or column.get("title") or f"col_{index}" for index, column in enumerate(columns)]
    row_count = len(columns[0].get("data", [])) if columns else 0
    rows = []

    for row_index in range(row_count):
        row = {}
        for label, column in zip(labels, columns):
            row[label] = column.get("data", [None] * row_count)[row_index]
        rows.append(row)

    return rows


def run_powerflow_tables(model):
    job = model.runPowerFlow()
    wait_for_completion(job)
    result = job.result
    return table_rows(result.getBuses()[0]), table_rows(result.getBranches()[0])


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
            branch_data = branch.toJSON()
            candidates.append(
                {
                    "branch_id": branch.id,
                    "branch_name": describe_branch_component(branch),
                    "branch_kind": classify_branch_component(branch),
                    "enabled": branch_data.get("props", {}).get("enabled", True),
                }
            )

    return sorted(candidates, key=lambda item: (item["branch_name"], item["branch_id"]))


def filter_candidate_branches_by_base_presence(candidates, base_branch_ids=None):
    if base_branch_ids is None:
        return list(candidates), []

    active_candidates = []
    skipped_candidates = []
    for candidate in candidates:
        if candidate["branch_id"] in base_branch_ids:
            active_candidates.append(candidate)
        else:
            skipped_candidates.append(candidate)

    return active_candidates, skipped_candidates


def choose_candidate_branch_ids(
    model,
    use_all_discovered=True,
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
    discovered_ids = [item["branch_id"] for item in active_candidates]

    if use_all_discovered:
        chosen = discovered_ids
    else:
        chosen = [branch_id for branch_id in DEFAULT_VALIDATED_BRANCH_IDS if branch_id in discovered_ids]

    if limit is not None:
        chosen = chosen[:limit]

    return chosen


def disable_branch_outage(model, branch_id):
    branch = model.getComponentByKey(branch_id)
    model.updateComponent(branch.id, props={"enabled": False})


def compute_n1_delta_metrics(base_buses, base_branches, outage_buses, outage_branches):
    base_bus_by_id = {row[BUS_COLUMN]: row for row in base_buses}
    outage_bus_by_id = {row[BUS_COLUMN]: row for row in outage_buses}
    base_branch_by_id = {row[BRANCH_COLUMN]: row for row in base_branches}
    outage_branch_by_id = {row[BRANCH_COLUMN]: row for row in outage_branches}
    base_low_voltage_buses = {
        bus_id for bus_id, row in base_bus_by_id.items() if row[VM_COLUMN] < VM_LOW_LIMIT
    }
    base_high_voltage_buses = {
        bus_id for bus_id, row in base_bus_by_id.items() if row[VM_COLUMN] > VM_HIGH_LIMIT
    }
    outage_low_voltage_buses = {
        bus_id for bus_id, row in outage_bus_by_id.items() if row[VM_COLUMN] < VM_LOW_LIMIT
    }
    outage_high_voltage_buses = {
        bus_id for bus_id, row in outage_bus_by_id.items() if row[VM_COLUMN] > VM_HIGH_LIMIT
    }
    missing_bus_ids = sorted(set(base_bus_by_id) - set(outage_bus_by_id))
    missing_branch_ids = sorted(set(base_branch_by_id) - set(outage_branch_by_id))
    new_low_voltage_buses = sorted(outage_low_voltage_buses - base_low_voltage_buses)
    new_high_voltage_buses = sorted(outage_high_voltage_buses - base_high_voltage_buses)

    max_vm_shift = 0.0
    max_vm_shift_bus_id = None
    for bus_id, base_row in base_bus_by_id.items():
        outage_row = outage_bus_by_id.get(bus_id)
        if outage_row is None:
            continue
        candidate_shift = abs(outage_row[VM_COLUMN] - base_row[VM_COLUMN])
        if candidate_shift > max_vm_shift:
            max_vm_shift = candidate_shift
            max_vm_shift_bus_id = bus_id

    max_branch_shift = 0.0
    max_branch_shift_branch_id = None
    for branch_id, base_row in base_branch_by_id.items():
        outage_row = outage_branch_by_id.get(branch_id)
        if outage_row is None:
            continue
        candidate_shift = abs(abs(outage_row[P_IJ_COLUMN]) - abs(base_row[P_IJ_COLUMN]))
        if candidate_shift > max_branch_shift:
            max_branch_shift = candidate_shift
            max_branch_shift_branch_id = branch_id

    min_vm_row = min(outage_buses, key=lambda row: row[VM_COLUMN])

    return {
        "min_vm": min_vm_row[VM_COLUMN],
        "min_vm_bus_id": min_vm_row[BUS_COLUMN],
        "low_voltage_bus_count": len(outage_low_voltage_buses),
        "high_voltage_bus_count": len(outage_high_voltage_buses),
        "new_low_voltage_bus_count": len(new_low_voltage_buses),
        "new_high_voltage_bus_count": len(new_high_voltage_buses),
        "new_low_voltage_buses": new_low_voltage_buses,
        "new_high_voltage_buses": new_high_voltage_buses,
        "missing_bus_count": len(missing_bus_ids),
        "missing_bus_ids": missing_bus_ids,
        "missing_branch_count": len(missing_branch_ids),
        "missing_branch_ids": missing_branch_ids,
        "max_vm_shift": max_vm_shift,
        "max_vm_shift_bus_id": max_vm_shift_bus_id,
        "max_branch_shift": max_branch_shift,
        "max_branch_shift_branch_id": max_branch_shift_branch_id,
    }


def classify_n1_severity(metrics):
    if metrics["new_low_voltage_bus_count"] > 0 or metrics["new_high_voltage_bus_count"] > 0:
        return "critical"
    if metrics["min_vm"] < 0.91 or metrics["max_branch_shift"] > 100.0:
        return "warning"
    return "observe"


def severity_rank_value(metrics):
    severity = classify_n1_severity(metrics)
    return {
        "critical": 2,
        "warning": 1,
        "observe": 0,
    }[severity]


def rank_n1_results(results):
    return sorted(
        results,
        key=lambda item: (
            severity_rank_value(item),
            item["new_low_voltage_bus_count"] + item["new_high_voltage_bus_count"],
            max(0.0, VM_LOW_LIMIT - item["min_vm"]),
            item["max_vm_shift"],
            item["max_branch_shift"],
        ),
        reverse=True,
    )


def screen_n1_branches(model, branch_ids, base_buses=None, base_branches=None):
    if base_buses is None or base_branches is None:
        base_buses, base_branches = run_powerflow_tables(model)

    results = []

    for branch_id in branch_ids:
        working_model = Model(deepcopy(model.toJSON()))
        branch = working_model.getComponentByKey(branch_id)
        branch_name = describe_branch_component(branch)
        branch_kind = classify_branch_component(branch)
        disable_branch_outage(working_model, branch_id)
        outage_buses, outage_branches = run_powerflow_tables(working_model)
        delta_metrics = compute_n1_delta_metrics(
            base_buses=base_buses,
            base_branches=base_branches,
            outage_buses=outage_buses,
            outage_branches=outage_branches,
        )

        results.append(
            {
                "branch_id": branch_id,
                "branch_name": branch_name,
                "branch_kind": branch_kind,
                "branch_present_after_outage": any(
                    row[BRANCH_COLUMN] == branch_id for row in outage_branches
                ),
                "min_vm": delta_metrics["min_vm"],
                "min_vm_bus_id": delta_metrics["min_vm_bus_id"],
                "low_voltage_bus_count": delta_metrics["low_voltage_bus_count"],
                "high_voltage_bus_count": delta_metrics["high_voltage_bus_count"],
                "new_low_voltage_bus_count": delta_metrics["new_low_voltage_bus_count"],
                "new_high_voltage_bus_count": delta_metrics["new_high_voltage_bus_count"],
                "new_low_voltage_buses": delta_metrics["new_low_voltage_buses"],
                "new_high_voltage_buses": delta_metrics["new_high_voltage_buses"],
                "missing_bus_count": delta_metrics["missing_bus_count"],
                "missing_bus_ids": delta_metrics["missing_bus_ids"],
                "missing_branch_count": delta_metrics["missing_branch_count"],
                "missing_branch_ids": delta_metrics["missing_branch_ids"],
                "max_vm_shift": delta_metrics["max_vm_shift"],
                "max_vm_shift_bus_id": delta_metrics["max_vm_shift_bus_id"],
                "max_branch_shift": delta_metrics["max_branch_shift"],
                "max_branch_shift_branch_id": delta_metrics["max_branch_shift_branch_id"],
            }
        )

    ranked_results = rank_n1_results(results)
    for index, result in enumerate(ranked_results, start=1):
        result["severity"] = classify_n1_severity(result)
        result["rank"] = index

    return ranked_results


def _format_id_list(items, limit=3):
    if not items:
        return "-"
    if len(items) <= limit:
        return ",".join(items)
    preview = ",".join(items[:limit])
    return f"{preview},...(+{len(items) - limit})"


def build_summary_rows(results):
    rows = []
    for result in results:
        rows.append(
            {
                "branch_id": result["branch_id"],
                "branch_name": result["branch_name"],
                "branch_kind": result["branch_kind"],
                "severity": result["severity"],
                "rank": str(result["rank"]),
                "branch_present_after_outage": "yes" if result["branch_present_after_outage"] else "no",
                "min_vm": f"{result['min_vm']:.4f}",
                "min_vm_bus_id": result["min_vm_bus_id"],
                "new_low_voltage_bus_count": str(result["new_low_voltage_bus_count"]),
                "new_low_voltage_buses": _format_id_list(result["new_low_voltage_buses"]),
                "new_high_voltage_bus_count": str(result["new_high_voltage_bus_count"]),
                "new_high_voltage_buses": _format_id_list(result["new_high_voltage_buses"]),
                "missing_bus_count": str(result["missing_bus_count"]),
                "missing_bus_ids": _format_id_list(result["missing_bus_ids"]),
                "missing_branch_count": str(result["missing_branch_count"]),
                "missing_branch_ids": _format_id_list(result["missing_branch_ids"]),
                "max_vm_shift": f"{result['max_vm_shift']:.4f}",
                "max_vm_shift_bus_id": result["max_vm_shift_bus_id"] or "-",
                "max_branch_shift": f"{result['max_branch_shift']:.3f}",
                "max_branch_shift_branch_id": result["max_branch_shift_branch_id"] or "-",
            }
        )
    return rows


def build_screening_digest(results):
    severity_counts = {"critical": 0, "warning": 0, "observe": 0}
    branch_kind_counts = {"line": 0, "transformer": 0}
    for result in results:
        severity_counts[result["severity"]] += 1
        branch_kind_counts[result["branch_kind"]] += 1

    def first_matching(branch_kind):
        for result in results:
            if result["branch_kind"] == branch_kind:
                return result
        return None

    return {
        "total_cases": len(results),
        "severity_counts": severity_counts,
        "branch_kind_counts": branch_kind_counts,
        "top_case": results[0] if results else None,
        "top_line_case": first_matching("line"),
        "top_transformer_case": first_matching("transformer"),
        "lowest_voltage_case": min(results, key=lambda item: item["min_vm"]) if results else None,
        "largest_vm_shift_case": max(results, key=lambda item: item["max_vm_shift"]) if results else None,
        "largest_branch_shift_case": (
            max(results, key=lambda item: item["max_branch_shift"]) if results else None
        ),
        "largest_missing_bus_case": (
            max(
                results,
                key=lambda item: (
                    item["missing_bus_count"],
                    item["new_low_voltage_bus_count"] + item["new_high_voltage_bus_count"],
                    item["max_vm_shift"],
                    item["max_branch_shift"],
                ),
            )
            if results
            else None
        ),
    }


def export_summary_rows_csv(rows, path):
    fieldnames = [
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


def summary_rows_to_dataframe(rows):
    try:
        import pandas as pd
    except ImportError as exc:
        raise RuntimeError("未安装 pandas，无法导出 DataFrame") from exc

    return pd.DataFrame(rows)


def print_summary_table(rows):
    headers = [
        "rank",
        "branch_name",
        "branch_kind",
        "severity",
        "min_vm",
        "min_vm_bus_id",
        "new_low_voltage_bus_count",
        "new_high_voltage_bus_count",
        "missing_bus_count",
        "max_vm_shift",
        "max_vm_shift_bus_id",
        "max_branch_shift",
        "max_branch_shift_branch_id",
    ]
    print("\n=== 受限 N-1 潮流筛查汇总 ===")
    print(" | ".join(headers))
    print("-" * 128)
    for row in rows:
        print(" | ".join(row[header] for header in headers))


def print_screening_digest(digest):
    if digest["top_case"] is None:
        print("\n=== N-1 研究摘要 ===")
        print("没有可输出的筛查结果。")
        return

    print("\n=== N-1 研究摘要 ===")
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

    top_case = digest["top_case"]
    print(
        "总榜首位: "
        f"{top_case['branch_name']} ({top_case['branch_id']}, {top_case['branch_kind']}) "
        f"severity={top_case['severity']} min_vm={top_case['min_vm']:.4f}@{top_case['min_vm_bus_id']}"
    )

    for label, item in [
        ("线路首位", digest["top_line_case"]),
        ("变压器首位", digest["top_transformer_case"]),
        ("最低电压工况", digest["lowest_voltage_case"]),
        ("最大电压偏移工况", digest["largest_vm_shift_case"]),
        ("最大潮流偏移工况", digest["largest_branch_shift_case"]),
        ("最大母线缺失工况", digest["largest_missing_bus_case"]),
    ]:
        if item is None:
            continue
        print(
            f"{label}: {item['branch_name']} ({item['branch_id']}) "
            f"severity={item['severity']} "
            f"min_vm={item['min_vm']:.4f}@{item['min_vm_bus_id']} "
            f"missing_bus_count={item['missing_bus_count']} "
            f"max_branch_shift={item['max_branch_shift']:.3f}@{item['max_branch_shift_branch_id'] or '-'}"
        )


def main():
    print("CloudPSS 受限 N-1 潮流筛查示例")
    print("=" * 50)

    token = load_token()
    setToken(token)

    args = sys.argv[1:]
    use_all_discovered = True
    include_transformers = True
    csv_path = None
    limit = None
    source = DEFAULT_READONLY_MODEL_RID

    positional = []
    for arg in args:
        if arg == "--validated-subset":
            use_all_discovered = False
            continue
        if arg == "--all-lines":
            include_transformers = False
            continue
        if arg == "--lines-only":
            include_transformers = False
            continue
        if arg == "--all-branches":
            use_all_discovered = True
            continue
        if arg.startswith("--csv="):
            csv_path = arg.split("=", 1)[1].strip()
            continue
        if arg.startswith("--limit="):
            limit = int(arg.split("=", 1)[1].strip())
            continue
        positional.append(arg)

    if positional:
        source = positional[0].strip()

    model = load_model_from_source(source)

    print(f"模型来源: {source}")
    print(f"模型名称: {model.name}")

    base_buses, base_branches = run_powerflow_tables(model)
    base_branch_ids = {row[BRANCH_COLUMN] for row in base_branches}
    discovered_candidates = discover_candidate_branches(
        model,
        include_transformers=include_transformers,
    )
    active_candidates, skipped_candidates = filter_candidate_branches_by_base_presence(
        discovered_candidates,
        base_branch_ids=base_branch_ids,
    )
    candidate_branch_ids = choose_candidate_branch_ids(
        model,
        use_all_discovered=use_all_discovered,
        include_transformers=include_transformers,
        limit=limit,
        base_branch_ids=base_branch_ids,
    )
    print(f"候选支路总数: {len(active_candidates)}")
    print(f"筛查支路: {', '.join(candidate_branch_ids)}")
    if skipped_candidates:
        skipped_labels = [f"{item['branch_name']} ({item['branch_id']})" for item in skipped_candidates]
        print(
            "说明: 以下组件虽然存在于模型中，但基线潮流支路表中缺席，"
            f"因此不会被纳入当前 N-1 候选集: {', '.join(skipped_labels)}"
        )
    if use_all_discovered and include_transformers:
        print("说明: 当前默认使用 IEEE39 基线在役的全量支路集合，包含线路和变压器。")
    elif use_all_discovered:
        print("说明: 当前使用 IEEE39 基线在役的全量线路集合，不含变压器。")
    else:
        print("说明: 当前使用较小的已验证支路子集，适合做快速复核。")

    results = screen_n1_branches(
        model,
        candidate_branch_ids,
        base_buses=base_buses,
        base_branches=base_branches,
    )
    digest = build_screening_digest(results)
    summary_rows = build_summary_rows(results)
    print_screening_digest(digest)
    print_summary_table(summary_rows)

    if csv_path is None:
        csv_path = DEFAULT_EXPORT_PATH
    export_summary_rows_csv(summary_rows, csv_path)
    print(f"已导出 CSV 摘要: {csv_path}")


if __name__ == "__main__":
    main()
