"""
CloudPSS power-flow engineering study example.

Run with:
  python examples/analysis/powerflow_engineering_study_example.py line-outage
  python examples/analysis/powerflow_engineering_study_example.py voltage-control
  python examples/analysis/powerflow_engineering_study_example.py active-redispatch
  python examples/analysis/powerflow_engineering_study_example.py load-transfer
  python examples/analysis/powerflow_engineering_study_example.py reactive-stress

This example stays within the current mainline:
- ordinary cloud power-flow
- local study copy edits
- engineering-style result comparison

Validated scenarios:
- line outage on IEEE39 `line-26-28`
- generator voltage-setpoint adjustment on IEEE39 `Gen30`
- generator active-power redispatch on IEEE39 `Gen38`
- load transfer from IEEE39 `load-39` to `load-21`
- reactive-stress case on IEEE39 `load-21`
"""

import os
from copy import deepcopy
from pathlib import Path
import sys
import time

from cloudpss import Model, setToken


DEFAULT_READONLY_MODEL_RID = os.environ.get("TEST_MODEL_RID", "model/holdme/IEEE39")
BUS_COLUMN = "Bus"
NODE_COLUMN = "Node"
VM_COLUMN = "<i>V</i><sub>m</sub> / pu"
VA_COLUMN = "<i>V</i><sub>a</sub> / deg"
P_GEN_COLUMN = "<i>P</i><sub>gen</sub> / MW"
Q_GEN_COLUMN = "<i>Q</i><sub>gen</sub> / MVar"
BRANCH_COLUMN = "Branch"
P_IJ_COLUMN = "<i>P</i><sub>ij</sub> / MW"
P_JI_COLUMN = "<i>P</i><sub>ji</sub> / MW"


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


def find_bus_row(rows, bus_id=None, node_id=None):
    for row in rows:
        if bus_id is not None and row.get(BUS_COLUMN) == bus_id:
            return row
        if node_id is not None and row.get(NODE_COLUMN) == node_id:
            return row
    raise KeyError(f"未找到母线结果: bus_id={bus_id}, node_id={node_id}")


def find_branch_row(rows, branch_id):
    for row in rows:
        if row.get(BRANCH_COLUMN) == branch_id:
            return row
    raise KeyError(f"未找到支路结果: {branch_id}")


def run_powerflow_tables(model):
    job = model.runPowerFlow()
    wait_for_completion(job)
    result = job.result
    return table_rows(result.getBuses()[0]), table_rows(result.getBranches()[0])


def compute_line_outage_summary(base_buses, base_branches, outage_buses, outage_branches):
    target_branch = find_branch_row(base_branches, "canvas_0_126")
    from_bus = find_bus_row(base_buses, bus_id=target_branch["From bus"])
    to_bus = find_bus_row(base_buses, bus_id=target_branch["To bus"])
    outage_from_bus = find_bus_row(outage_buses, bus_id=target_branch["From bus"])
    outage_to_bus = find_bus_row(outage_buses, bus_id=target_branch["To bus"])

    monitored = {}
    for branch_id in ["canvas_0_123", "canvas_0_130", "canvas_0_134"]:
        base_row = find_branch_row(base_branches, branch_id)
        outage_row = find_branch_row(outage_branches, branch_id)
        monitored[branch_id] = {
            "from_bus": base_row["From bus"],
            "to_bus": base_row["To bus"],
            "base_p_ij": base_row[P_IJ_COLUMN],
            "outage_p_ij": outage_row[P_IJ_COLUMN],
            "base_p_ji": base_row[P_JI_COLUMN],
            "outage_p_ji": outage_row[P_JI_COLUMN],
        }

    return {
        "target_branch": {
            "id": "canvas_0_126",
            "name": "line-26-28",
            "from_bus": target_branch["From bus"],
            "to_bus": target_branch["To bus"],
            "base_p_ij": target_branch[P_IJ_COLUMN],
            "base_p_ji": target_branch[P_JI_COLUMN],
        },
        "from_bus_shift": {
            "bus_id": target_branch["From bus"],
            "base_vm": from_bus[VM_COLUMN],
            "outage_vm": outage_from_bus[VM_COLUMN],
            "base_va": from_bus[VA_COLUMN],
            "outage_va": outage_from_bus[VA_COLUMN],
        },
        "to_bus_shift": {
            "bus_id": target_branch["To bus"],
            "base_vm": to_bus[VM_COLUMN],
            "outage_vm": outage_to_bus[VM_COLUMN],
            "base_va": to_bus[VA_COLUMN],
            "outage_va": outage_to_bus[VA_COLUMN],
        },
        "monitored_branches": monitored,
    }


def compute_voltage_control_summary(base_buses, adjusted_buses):
    base_row = find_bus_row(base_buses, node_id="canvas_2_303")
    adjusted_row = find_bus_row(adjusted_buses, node_id="canvas_2_303")

    nearby_bus_changes = []
    for base_candidate in base_buses:
        adjusted_candidate = find_bus_row(adjusted_buses, bus_id=base_candidate[BUS_COLUMN])
        nearby_bus_changes.append(
            {
                "bus_id": base_candidate[BUS_COLUMN],
                "node_id": base_candidate[NODE_COLUMN],
                "base_vm": base_candidate[VM_COLUMN],
                "adjusted_vm": adjusted_candidate[VM_COLUMN],
                "delta_vm": adjusted_candidate[VM_COLUMN] - base_candidate[VM_COLUMN],
            }
        )

    nearby_bus_changes.sort(key=lambda item: abs(item["delta_vm"]), reverse=True)

    return {
        "generator": "Gen30",
        "generator_node": "canvas_2_303",
        "target_bus": {
            "bus_id": base_row[BUS_COLUMN],
            "base_vm": base_row[VM_COLUMN],
            "adjusted_vm": adjusted_row[VM_COLUMN],
            "base_q_gen": base_row[Q_GEN_COLUMN],
            "adjusted_q_gen": adjusted_row[Q_GEN_COLUMN],
            "base_p_gen": base_row[P_GEN_COLUMN],
            "adjusted_p_gen": adjusted_row[P_GEN_COLUMN],
        },
        "largest_voltage_changes": nearby_bus_changes[:5],
    }


def compute_active_redispatch_summary(base_buses, base_branches, adjusted_buses, adjusted_branches):
    base_bus_by_node = {row[NODE_COLUMN]: row for row in base_buses}
    adjusted_bus_by_node = {row[NODE_COLUMN]: row for row in adjusted_buses}
    base_branch_by_id = {row[BRANCH_COLUMN]: row for row in base_branches}
    adjusted_branch_by_id = {row[BRANCH_COLUMN]: row for row in adjusted_branches}

    monitored_branch_ids = [
        "canvas_0_258",
        "canvas_0_126",
        "canvas_0_134",
        "canvas_0_130",
        "canvas_0_123",
    ]
    monitored_branches = {}
    for branch_id in monitored_branch_ids:
        base_row = base_branch_by_id[branch_id]
        adjusted_row = adjusted_branch_by_id[branch_id]
        monitored_branches[branch_id] = {
            "from_bus": base_row["From bus"],
            "to_bus": base_row["To bus"],
            "base_abs_p_ij": abs(base_row[P_IJ_COLUMN]),
            "adjusted_abs_p_ij": abs(adjusted_row[P_IJ_COLUMN]),
            "delta_abs_p_ij": abs(adjusted_row[P_IJ_COLUMN]) - abs(base_row[P_IJ_COLUMN]),
        }

    return {
        "generator": "Gen38",
        "generator_node": "canvas_9_384",
        "target_bus": {
            "bus_id": base_bus_by_node["canvas_9_384"][BUS_COLUMN],
            "base_p_gen": base_bus_by_node["canvas_9_384"][P_GEN_COLUMN],
            "adjusted_p_gen": adjusted_bus_by_node["canvas_9_384"][P_GEN_COLUMN],
            "base_q_gen": base_bus_by_node["canvas_9_384"][Q_GEN_COLUMN],
            "adjusted_q_gen": adjusted_bus_by_node["canvas_9_384"][Q_GEN_COLUMN],
            "base_vm": base_bus_by_node["canvas_9_384"][VM_COLUMN],
            "adjusted_vm": adjusted_bus_by_node["canvas_9_384"][VM_COLUMN],
        },
        "slack_bus": {
            "bus_id": base_bus_by_node["canvas_10_399"][BUS_COLUMN],
            "base_p_gen": base_bus_by_node["canvas_10_399"][P_GEN_COLUMN],
            "adjusted_p_gen": adjusted_bus_by_node["canvas_10_399"][P_GEN_COLUMN],
            "base_q_gen": base_bus_by_node["canvas_10_399"][Q_GEN_COLUMN],
            "adjusted_q_gen": adjusted_bus_by_node["canvas_10_399"][Q_GEN_COLUMN],
        },
        "monitored_branches": monitored_branches,
    }


def compute_load_transfer_summary(base_buses, base_branches, adjusted_buses, adjusted_branches):
    base_bus_by_id = {row[BUS_COLUMN]: row for row in base_buses}
    adjusted_bus_by_id = {row[BUS_COLUMN]: row for row in adjusted_buses}
    base_branch_by_id = {row[BRANCH_COLUMN]: row for row in base_branches}
    adjusted_branch_by_id = {row[BRANCH_COLUMN]: row for row in adjusted_branches}

    monitored_bus_ids = ["canvas_0_154", "canvas_0_153", "canvas_0_181"]
    monitored_branch_ids = ["canvas_0_175", "canvas_0_182", "canvas_0_185"]

    monitored_buses = {}
    for bus_id in monitored_bus_ids:
        base_row = base_bus_by_id[bus_id]
        adjusted_row = adjusted_bus_by_id[bus_id]
        monitored_buses[bus_id] = {
            "base_vm": base_row[VM_COLUMN],
            "adjusted_vm": adjusted_row[VM_COLUMN],
            "delta_vm": adjusted_row[VM_COLUMN] - base_row[VM_COLUMN],
            "base_va": base_row[VA_COLUMN],
            "adjusted_va": adjusted_row[VA_COLUMN],
            "delta_va": adjusted_row[VA_COLUMN] - base_row[VA_COLUMN],
        }

    monitored_branches = {}
    for branch_id in monitored_branch_ids:
        base_row = base_branch_by_id[branch_id]
        adjusted_row = adjusted_branch_by_id[branch_id]
        monitored_branches[branch_id] = {
            "from_bus": base_row["From bus"],
            "to_bus": base_row["To bus"],
            "base_abs_p_ij": abs(base_row[P_IJ_COLUMN]),
            "adjusted_abs_p_ij": abs(adjusted_row[P_IJ_COLUMN]),
            "delta_abs_p_ij": abs(adjusted_row[P_IJ_COLUMN]) - abs(base_row[P_IJ_COLUMN]),
        }

    base_slack = base_bus_by_id["canvas_0_35"]
    adjusted_slack = adjusted_bus_by_id["canvas_0_35"]

    return {
        "source_load": {
            "name": "load-39",
            "component_id": "canvas_0_446",
            "base_p": 1104.0,
            "adjusted_p": 904.0,
            "base_q": 250.0,
            "adjusted_q": 190.0,
        },
        "target_load": {
            "name": "load-21",
            "component_id": "canvas_0_428",
            "base_p": 274.0,
            "adjusted_p": 474.0,
            "base_q": 115.0,
            "adjusted_q": 175.0,
        },
        "slack_bus": {
            "bus_id": "canvas_0_35",
            "base_p_gen": base_slack[P_GEN_COLUMN],
            "adjusted_p_gen": adjusted_slack[P_GEN_COLUMN],
            "base_q_gen": base_slack[Q_GEN_COLUMN],
            "adjusted_q_gen": adjusted_slack[Q_GEN_COLUMN],
        },
        "monitored_buses": monitored_buses,
        "monitored_branches": monitored_branches,
    }


def compute_reactive_stress_summary(base_buses, base_branches, adjusted_buses, adjusted_branches):
    base_bus_by_id = {row[BUS_COLUMN]: row for row in base_buses}
    adjusted_bus_by_id = {row[BUS_COLUMN]: row for row in adjusted_buses}
    base_branch_by_id = {row[BRANCH_COLUMN]: row for row in base_branches}
    adjusted_branch_by_id = {row[BRANCH_COLUMN]: row for row in adjusted_branches}

    monitored_bus_ids = ["canvas_0_154", "canvas_0_153", "canvas_0_181", "canvas_0_114"]
    monitored_branch_ids = ["canvas_0_175", "canvas_0_182", "canvas_0_185"]

    monitored_buses = {}
    for bus_id in monitored_bus_ids:
        base_row = base_bus_by_id[bus_id]
        adjusted_row = adjusted_bus_by_id[bus_id]
        monitored_buses[bus_id] = {
            "base_vm": base_row[VM_COLUMN],
            "adjusted_vm": adjusted_row[VM_COLUMN],
            "delta_vm": adjusted_row[VM_COLUMN] - base_row[VM_COLUMN],
            "base_va": base_row[VA_COLUMN],
            "adjusted_va": adjusted_row[VA_COLUMN],
            "delta_va": adjusted_row[VA_COLUMN] - base_row[VA_COLUMN],
        }

    monitored_branches = {}
    for branch_id in monitored_branch_ids:
        base_row = base_branch_by_id[branch_id]
        adjusted_row = adjusted_branch_by_id[branch_id]
        monitored_branches[branch_id] = {
            "from_bus": base_row["From bus"],
            "to_bus": base_row["To bus"],
            "base_abs_p_ij": abs(base_row[P_IJ_COLUMN]),
            "adjusted_abs_p_ij": abs(adjusted_row[P_IJ_COLUMN]),
            "delta_abs_p_ij": abs(adjusted_row[P_IJ_COLUMN]) - abs(base_row[P_IJ_COLUMN]),
        }

    reactive_support_changes = []
    for bus_id, base_row in base_bus_by_id.items():
        adjusted_row = adjusted_bus_by_id[bus_id]
        delta_q_gen = adjusted_row[Q_GEN_COLUMN] - base_row[Q_GEN_COLUMN]
        if delta_q_gen > 0.5:
            reactive_support_changes.append(
                {
                    "bus_id": bus_id,
                    "node_id": base_row[NODE_COLUMN],
                    "base_q_gen": base_row[Q_GEN_COLUMN],
                    "adjusted_q_gen": adjusted_row[Q_GEN_COLUMN],
                    "delta_q_gen": delta_q_gen,
                }
            )
    reactive_support_changes.sort(key=lambda item: item["delta_q_gen"], reverse=True)

    base_slack = base_bus_by_id["canvas_0_35"]
    adjusted_slack = adjusted_bus_by_id["canvas_0_35"]

    return {
        "target_load": {
            "name": "load-21",
            "component_id": "canvas_0_428",
            "base_q": 115.0,
            "adjusted_q": 215.0,
        },
        "slack_bus": {
            "bus_id": "canvas_0_35",
            "base_p_gen": base_slack[P_GEN_COLUMN],
            "adjusted_p_gen": adjusted_slack[P_GEN_COLUMN],
            "base_q_gen": base_slack[Q_GEN_COLUMN],
            "adjusted_q_gen": adjusted_slack[Q_GEN_COLUMN],
        },
        "monitored_buses": monitored_buses,
        "monitored_branches": monitored_branches,
        "top_reactive_support_changes": reactive_support_changes[:5],
    }


def run_line_outage_study(model):
    base_buses, base_branches = run_powerflow_tables(model)

    outage_model = Model(deepcopy(model.toJSON()))
    target_line = outage_model.getComponentByKey("canvas_0_126")
    outage_model.removeComponent(target_line.id)
    outage_buses, outage_branches = run_powerflow_tables(outage_model)

    return compute_line_outage_summary(
        base_buses=base_buses,
        base_branches=base_branches,
        outage_buses=outage_buses,
        outage_branches=outage_branches,
    )


def run_voltage_control_study(model):
    base_buses, _ = run_powerflow_tables(model)

    adjusted_model = Model(deepcopy(model.toJSON()))
    gen30 = adjusted_model.getComponentByKey("canvas_2_303")
    adjusted_model.updateComponent(
        gen30.id,
        args={**gen30.args, "pf_V": {"source": "1.070", "ɵexp": ""}},
    )
    adjusted_buses, _ = run_powerflow_tables(adjusted_model)

    return compute_voltage_control_summary(
        base_buses=base_buses,
        adjusted_buses=adjusted_buses,
    )


def run_active_redispatch_study(model):
    base_buses, base_branches = run_powerflow_tables(model)

    adjusted_model = Model(deepcopy(model.toJSON()))
    gen38 = adjusted_model.getComponentByKey("canvas_9_384")
    adjusted_model.updateComponent(
        gen38.id,
        args={**gen38.args, "pf_P": {"source": "900", "ɵexp": ""}},
    )
    adjusted_buses, adjusted_branches = run_powerflow_tables(adjusted_model)

    return compute_active_redispatch_summary(
        base_buses=base_buses,
        base_branches=base_branches,
        adjusted_buses=adjusted_buses,
        adjusted_branches=adjusted_branches,
    )


def run_load_transfer_study(model):
    base_buses, base_branches = run_powerflow_tables(model)

    adjusted_model = Model(deepcopy(model.toJSON()))
    source_load = adjusted_model.getComponentByKey("canvas_0_446")
    target_load = adjusted_model.getComponentByKey("canvas_0_428")
    adjusted_model.updateComponent(
        source_load.id,
        args={
            **source_load.args,
            "p": {"source": "904", "ɵexp": ""},
            "q": {"source": "190", "ɵexp": ""},
        },
    )
    adjusted_model.updateComponent(
        target_load.id,
        args={
            **target_load.args,
            "p": {"source": "474", "ɵexp": ""},
            "q": {"source": "175", "ɵexp": ""},
        },
    )
    adjusted_buses, adjusted_branches = run_powerflow_tables(adjusted_model)

    return compute_load_transfer_summary(
        base_buses=base_buses,
        base_branches=base_branches,
        adjusted_buses=adjusted_buses,
        adjusted_branches=adjusted_branches,
    )


def run_reactive_stress_study(model):
    base_buses, base_branches = run_powerflow_tables(model)

    adjusted_model = Model(deepcopy(model.toJSON()))
    target_load = adjusted_model.getComponentByKey("canvas_0_428")
    adjusted_model.updateComponent(
        target_load.id,
        args={
            **target_load.args,
            "q": {"source": "215", "ɵexp": ""},
        },
    )
    adjusted_buses, adjusted_branches = run_powerflow_tables(adjusted_model)

    return compute_reactive_stress_summary(
        base_buses=base_buses,
        base_branches=base_branches,
        adjusted_buses=adjusted_buses,
        adjusted_branches=adjusted_branches,
    )


def print_line_outage_summary(summary):
    print("\n=== 线路切除研究: line-26-28 ===")
    target = summary["target_branch"]
    print(f"切除支路: {target['id']} ({target['name']})")
    print(
        f"目标支路基线潮流: Pij={target['base_p_ij']:.3f} MW, "
        f"Pji={target['base_p_ji']:.3f} MW"
    )

    for label in ["from_bus_shift", "to_bus_shift"]:
        item = summary[label]
        print(
            f"母线 {item['bus_id']}: Vm {item['base_vm']:.4f} -> {item['outage_vm']:.4f}, "
            f"Va {item['base_va']:.4f} -> {item['outage_va']:.4f}"
        )

    print("相邻走廊潮流再分布:")
    for branch_id, item in summary["monitored_branches"].items():
        print(
            f"  {branch_id} ({item['from_bus']} -> {item['to_bus']}): "
            f"Pij {item['base_p_ij']:.3f} -> {item['outage_p_ij']:.3f} MW, "
            f"Pji {item['base_p_ji']:.3f} -> {item['outage_p_ji']:.3f} MW"
        )


def print_voltage_control_summary(summary):
    print("\n=== 电压控制研究: Gen30 pf_V 上调到 1.070 pu ===")
    target_bus = summary["target_bus"]
    print(
        f"机端母线 {target_bus['bus_id']}: Vm {target_bus['base_vm']:.4f} -> "
        f"{target_bus['adjusted_vm']:.4f}"
    )
    print(
        f"机组无功: Qgen {target_bus['base_q_gen']:.3f} -> "
        f"{target_bus['adjusted_q_gen']:.3f} MVar"
    )
    print(
        f"机组有功: Pgen {target_bus['base_p_gen']:.3f} -> "
        f"{target_bus['adjusted_p_gen']:.3f} MW"
    )
    print("电压变化最大的前 5 个母线:")
    for item in summary["largest_voltage_changes"]:
        print(
            f"  {item['bus_id']} ({item['node_id']}): "
            f"{item['base_vm']:.4f} -> {item['adjusted_vm']:.4f} "
            f"(delta={item['delta_vm']:+.4f})"
        )


def print_active_redispatch_summary(summary):
    print("\n=== 有功再调度研究: Gen38 pf_P 上调到 900 MW ===")
    target_bus = summary["target_bus"]
    slack_bus = summary["slack_bus"]
    print(
        f"Gen38 所在母线 {target_bus['bus_id']}: Pgen {target_bus['base_p_gen']:.3f} -> "
        f"{target_bus['adjusted_p_gen']:.3f} MW, "
        f"Qgen {target_bus['base_q_gen']:.3f} -> {target_bus['adjusted_q_gen']:.3f} MVar, "
        f"Vm {target_bus['base_vm']:.4f} -> {target_bus['adjusted_vm']:.4f}"
    )
    print(
        f"平衡机组 {slack_bus['bus_id']}: Pgen {slack_bus['base_p_gen']:.3f} -> "
        f"{slack_bus['adjusted_p_gen']:.3f} MW, "
        f"Qgen {slack_bus['base_q_gen']:.3f} -> {slack_bus['adjusted_q_gen']:.3f} MVar"
    )
    print("关键走廊有功传输幅值变化:")
    for branch_id, item in summary["monitored_branches"].items():
        print(
            f"  {branch_id} ({item['from_bus']} -> {item['to_bus']}): "
            f"|Pij| {item['base_abs_p_ij']:.3f} -> {item['adjusted_abs_p_ij']:.3f} MW "
            f"(delta={item['delta_abs_p_ij']:+.3f})"
        )


def print_load_transfer_summary(summary):
    print("\n=== 负荷转移研究: load-39 -> load-21 (200 MW / 60 MVar) ===")
    source = summary["source_load"]
    target = summary["target_load"]
    slack = summary["slack_bus"]
    print(
        f"源负荷 {source['name']} ({source['component_id']}): "
        f"P {source['base_p']:.1f} -> {source['adjusted_p']:.1f} MW, "
        f"Q {source['base_q']:.1f} -> {source['adjusted_q']:.1f} MVar"
    )
    print(
        f"目标负荷 {target['name']} ({target['component_id']}): "
        f"P {target['base_p']:.1f} -> {target['adjusted_p']:.1f} MW, "
        f"Q {target['base_q']:.1f} -> {target['adjusted_q']:.1f} MVar"
    )
    print(
        f"平衡机组 {slack['bus_id']}: Pgen {slack['base_p_gen']:.3f} -> "
        f"{slack['adjusted_p_gen']:.3f} MW, "
        f"Qgen {slack['base_q_gen']:.3f} -> {slack['adjusted_q_gen']:.3f} MVar"
    )
    print("负荷口袋母线变化:")
    for bus_id, item in summary["monitored_buses"].items():
        print(
            f"  {bus_id}: Vm {item['base_vm']:.4f} -> {item['adjusted_vm']:.4f} "
            f"(delta={item['delta_vm']:+.4f}), "
            f"Va {item['base_va']:.4f} -> {item['adjusted_va']:.4f} "
            f"(delta={item['delta_va']:+.4f})"
        )
    print("相关走廊有功传输幅值变化:")
    for branch_id, item in summary["monitored_branches"].items():
        print(
            f"  {branch_id} ({item['from_bus']} -> {item['to_bus']}): "
            f"|Pij| {item['base_abs_p_ij']:.3f} -> {item['adjusted_abs_p_ij']:.3f} MW "
            f"(delta={item['delta_abs_p_ij']:+.3f})"
        )


def print_reactive_stress_summary(summary):
    print("\n=== 无功压力研究: load-21 Q 提高到 215 MVar ===")
    target = summary["target_load"]
    slack = summary["slack_bus"]
    print(
        f"目标负荷 {target['name']} ({target['component_id']}): "
        f"Q {target['base_q']:.1f} -> {target['adjusted_q']:.1f} MVar"
    )
    print(
        f"平衡机组 {slack['bus_id']}: Pgen {slack['base_p_gen']:.3f} -> "
        f"{slack['adjusted_p_gen']:.3f} MW, "
        f"Qgen {slack['base_q_gen']:.3f} -> {slack['adjusted_q_gen']:.3f} MVar"
    )
    print("负荷口袋母线变化:")
    for bus_id, item in summary["monitored_buses"].items():
        print(
            f"  {bus_id}: Vm {item['base_vm']:.4f} -> {item['adjusted_vm']:.4f} "
            f"(delta={item['delta_vm']:+.4f}), "
            f"Va {item['base_va']:.4f} -> {item['adjusted_va']:.4f} "
            f"(delta={item['delta_va']:+.4f})"
        )
    print("相关走廊有功传输幅值变化:")
    for branch_id, item in summary["monitored_branches"].items():
        print(
            f"  {branch_id} ({item['from_bus']} -> {item['to_bus']}): "
            f"|Pij| {item['base_abs_p_ij']:.3f} -> {item['adjusted_abs_p_ij']:.3f} MW "
            f"(delta={item['delta_abs_p_ij']:+.3f})"
        )
    print("主要无功支撑来源:")
    for item in summary["top_reactive_support_changes"]:
        print(
            f"  {item['bus_id']} ({item['node_id']}): "
            f"Qgen {item['base_q_gen']:.3f} -> {item['adjusted_q_gen']:.3f} MVar "
            f"(delta={item['delta_q_gen']:+.3f})"
        )


def main():
    print("CloudPSS 潮流工程研究场景示例")
    print("=" * 50)

    token = load_token()
    setToken(token)

    scenario = sys.argv[1].strip() if len(sys.argv) > 1 else "line-outage"
    source = sys.argv[2].strip() if len(sys.argv) > 2 else DEFAULT_READONLY_MODEL_RID

    if scenario not in {
        "line-outage",
        "voltage-control",
        "active-redispatch",
        "load-transfer",
        "reactive-stress",
    }:
        print(
            "错误: 场景必须是 line-outage、voltage-control、active-redispatch、"
            "load-transfer 或 reactive-stress"
        )
        sys.exit(1)

    model = load_model_from_source(source)
    print(f"模型来源: {source}")
    print(f"模型名称: {model.name}")

    if scenario == "line-outage":
        print_line_outage_summary(run_line_outage_study(model))
    elif scenario == "voltage-control":
        print_voltage_control_summary(run_voltage_control_study(model))
    elif scenario == "load-transfer":
        print_load_transfer_summary(run_load_transfer_study(model))
    elif scenario == "reactive-stress":
        print_reactive_stress_summary(run_reactive_stress_study(model))
    else:
        print_active_redispatch_summary(run_active_redispatch_study(model))


if __name__ == "__main__":
    main()
