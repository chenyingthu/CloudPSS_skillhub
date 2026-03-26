"""
CloudPSS power-flow batch study example.

Run with:
  python examples/analysis/powerflow_batch_study_example.py
  python examples/analysis/powerflow_batch_study_example.py model/holdme/IEEE39
  python examples/analysis/powerflow_batch_study_example.py study-case.yaml

This example shows how an engineer can run several common power-flow study
scenarios on one validated baseline and compare the resulting operating-point
metrics side by side.
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
P_GEN_COLUMN = "<i>P</i><sub>gen</sub> / MW"
Q_GEN_COLUMN = "<i>Q</i><sub>gen</sub> / MVar"
BRANCH_COLUMN = "Branch"
P_IJ_COLUMN = "<i>P</i><sub>ij</sub> / MW"


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
    return None


def run_powerflow_tables(model):
    job = model.runPowerFlow()
    wait_for_completion(job)
    result = job.result
    return table_rows(result.getBuses()[0]), table_rows(result.getBranches()[0])


def apply_load_increase_scenario(model):
    load_39 = next(
        component
        for component in model.getAllComponents().values()
        if component.toJSON().get("definition") == "model/CloudPSS/_newExpLoad_3p"
        and component.toJSON().get("args", {}).get("Name") == "load-39"
    )
    model.updateComponent(
        load_39.id,
        args={
            **load_39.args,
            "p": {"source": "1400", "ɵexp": ""},
            "q": {"source": "350", "ɵexp": ""},
        },
    )


def apply_line_reactance_scenario(model):
    target_line = model.getComponentByKey("canvas_0_126")
    model.updateComponent(
        target_line.id,
        args={**target_line.args, "X1pu": {"source": "0.0600", "ɵexp": ""}},
    )


def apply_line_outage_scenario(model):
    target_line = model.getComponentByKey("canvas_0_126")
    model.removeComponent(target_line.id)


def apply_voltage_control_scenario(model):
    gen30 = model.getComponentByKey("canvas_2_303")
    model.updateComponent(
        gen30.id,
        args={**gen30.args, "pf_V": {"source": "1.070", "ɵexp": ""}},
    )


def apply_active_redispatch_scenario(model):
    gen38 = model.getComponentByKey("canvas_9_384")
    model.updateComponent(
        gen38.id,
        args={**gen38.args, "pf_P": {"source": "900", "ɵexp": ""}},
    )


def apply_load_transfer_scenario(model):
    source_load = model.getComponentByKey("canvas_0_446")
    target_load = model.getComponentByKey("canvas_0_428")
    model.updateComponent(
        source_load.id,
        args={
            **source_load.args,
            "p": {"source": "904", "ɵexp": ""},
            "q": {"source": "190", "ɵexp": ""},
        },
    )
    model.updateComponent(
        target_load.id,
        args={
            **target_load.args,
            "p": {"source": "474", "ɵexp": ""},
            "q": {"source": "175", "ɵexp": ""},
        },
    )


def apply_reactive_stress_scenario(model):
    target_load = model.getComponentByKey("canvas_0_428")
    model.updateComponent(
        target_load.id,
        args={
            **target_load.args,
            "q": {"source": "215", "ɵexp": ""},
        },
    )


def build_scenario_specs():
    return [
        {
            "name": "baseline",
            "description": "基线工况",
            "apply": None,
        },
        {
            "name": "load_up",
            "description": "load-39 提高到 1400/350",
            "apply": apply_load_increase_scenario,
        },
        {
            "name": "line_x_up",
            "description": "line-26-28 X1pu 提高到 0.0600",
            "apply": apply_line_reactance_scenario,
        },
        {
            "name": "line_outage",
            "description": "切除 line-26-28",
            "apply": apply_line_outage_scenario,
        },
        {
            "name": "gen30_v_up",
            "description": "Gen30 pf_V 提高到 1.070",
            "apply": apply_voltage_control_scenario,
        },
        {
            "name": "gen38_p_up",
            "description": "Gen38 pf_P 提高到 900",
            "apply": apply_active_redispatch_scenario,
        },
        {
            "name": "load_shift_39_to_21",
            "description": "从 load-39 向 load-21 转移 200 MW / 60 MVar",
            "apply": apply_load_transfer_scenario,
        },
        {
            "name": "load21_q_up",
            "description": "load-21 无功从 115 提高到 215 MVar",
            "apply": apply_reactive_stress_scenario,
        },
    ]


def extract_study_metrics(bus_rows, branch_rows):
    slack_row = find_bus_row(bus_rows, node_id="canvas_10_399")
    gen30_row = find_bus_row(bus_rows, node_id="canvas_2_303")
    gen38_row = find_bus_row(bus_rows, node_id="canvas_9_384")
    bus21_row = find_bus_row(bus_rows, bus_id="canvas_0_154")
    line_26_28 = find_branch_row(branch_rows, "canvas_0_126")
    line_26_29 = find_branch_row(branch_rows, "canvas_0_134")
    line_28_29 = find_branch_row(branch_rows, "canvas_0_130")
    line_21_22 = find_branch_row(branch_rows, "canvas_0_175")
    line_22_23 = find_branch_row(branch_rows, "canvas_0_182")
    line_23_24 = find_branch_row(branch_rows, "canvas_0_185")

    return {
        "slack_p_gen": slack_row[P_GEN_COLUMN],
        "slack_q_gen": slack_row[Q_GEN_COLUMN],
        "bus30_vm": gen30_row[VM_COLUMN],
        "bus30_q_gen": gen30_row[Q_GEN_COLUMN],
        "gen38_p_gen": gen38_row[P_GEN_COLUMN],
        "gen38_q_gen": gen38_row[Q_GEN_COLUMN],
        "bus21_vm": bus21_row[VM_COLUMN],
        "line_26_28_abs_pij": abs(line_26_28[P_IJ_COLUMN]) if line_26_28 is not None else None,
        "line_26_29_abs_pij": abs(line_26_29[P_IJ_COLUMN]) if line_26_29 is not None else None,
        "line_28_29_abs_pij": abs(line_28_29[P_IJ_COLUMN]) if line_28_29 is not None else None,
        "line_21_22_abs_pij": abs(line_21_22[P_IJ_COLUMN]) if line_21_22 is not None else None,
        "line_22_23_abs_pij": abs(line_22_23[P_IJ_COLUMN]) if line_22_23 is not None else None,
        "line_23_24_abs_pij": abs(line_23_24[P_IJ_COLUMN]) if line_23_24 is not None else None,
    }


def format_metric(value):
    if value is None:
        return "removed"
    return f"{value:.3f}"


def build_summary_rows(results):
    rows = []
    for item in results:
        metrics = item["metrics"]
        rows.append(
            {
                "scenario": item["name"],
                "description": item["description"],
                "slack_p_gen": format_metric(metrics["slack_p_gen"]),
                "slack_q_gen": format_metric(metrics["slack_q_gen"]),
                "bus30_vm": format_metric(metrics["bus30_vm"]),
                "bus30_q_gen": format_metric(metrics["bus30_q_gen"]),
                "gen38_p_gen": format_metric(metrics["gen38_p_gen"]),
                "gen38_q_gen": format_metric(metrics["gen38_q_gen"]),
                "bus21_vm": format_metric(metrics["bus21_vm"]),
                "line_26_28_abs_pij": format_metric(metrics["line_26_28_abs_pij"]),
                "line_26_29_abs_pij": format_metric(metrics["line_26_29_abs_pij"]),
                "line_28_29_abs_pij": format_metric(metrics["line_28_29_abs_pij"]),
                "line_21_22_abs_pij": format_metric(metrics["line_21_22_abs_pij"]),
                "line_22_23_abs_pij": format_metric(metrics["line_22_23_abs_pij"]),
                "line_23_24_abs_pij": format_metric(metrics["line_23_24_abs_pij"]),
            }
        )
    return rows


def print_summary_table(rows):
    headers = [
        "scenario",
        "slack_p_gen",
        "slack_q_gen",
        "bus30_vm",
        "bus30_q_gen",
        "gen38_p_gen",
        "gen38_q_gen",
        "bus21_vm",
        "line_26_28_abs_pij",
        "line_26_29_abs_pij",
        "line_28_29_abs_pij",
        "line_21_22_abs_pij",
        "line_22_23_abs_pij",
        "line_23_24_abs_pij",
    ]
    print("\n=== 多工况潮流研究汇总 ===")
    print(" | ".join(headers))
    print("-" * 180)
    for row in rows:
        print(" | ".join(str(row[header]) for header in headers))


def run_batch_study(model):
    results = []
    for spec in build_scenario_specs():
        working_model = Model(deepcopy(model.toJSON()))
        if spec["apply"] is not None:
            spec["apply"](working_model)
        bus_rows, branch_rows = run_powerflow_tables(working_model)
        results.append(
            {
                "name": spec["name"],
                "description": spec["description"],
                "metrics": extract_study_metrics(bus_rows, branch_rows),
            }
        )
    return results


def main():
    print("CloudPSS 潮流多工况研究示例")
    print("=" * 50)

    token = load_token()
    setToken(token)

    source = sys.argv[1].strip() if len(sys.argv) > 1 else DEFAULT_READONLY_MODEL_RID
    model = load_model_from_source(source)

    print(f"模型来源: {source}")
    print(f"模型名称: {model.name}")
    print(
        "将依次运行: baseline / load_up / line_x_up / line_outage / "
        "gen30_v_up / gen38_p_up / load_shift_39_to_21 / load21_q_up"
    )

    results = run_batch_study(model)
    print_summary_table(build_summary_rows(results))


if __name__ == "__main__":
    main()
