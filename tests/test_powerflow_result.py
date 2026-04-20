import time
from copy import deepcopy

import pytest

from cloudpss import Model
from cloudpss.job.result import PowerFlowResult


BUS_COLUMN = "Bus"
NODE_COLUMN = "Node"
VM_COLUMN = "<i>V</i><sub>m</sub> / pu"
VA_COLUMN = "<i>V</i><sub>a</sub> / deg"
P_GEN_COLUMN = "<i>P</i><sub>gen</sub> / MW"
Q_GEN_COLUMN = "<i>Q</i><sub>gen</sub> / MVar"
P_LOAD_COLUMN = "<i>P</i><sub>load</sub> / MW"
Q_LOAD_COLUMN = "<i>Q</i><sub>load</sub> / MVar"
BRANCH_COLUMN = "Branch"
P_IJ_COLUMN = "<i>P</i><sub>ij</sub> / MW"
P_JI_COLUMN = "<i>P</i><sub>ji</sub> / MW"
TRANSMISSION_LINE_RID = "model/CloudPSS/TransmissionLine"
TRANSFORMER_RID = "model/CloudPSS/_newTransformer_3p2w"
IEEE39_BASE_ABSENT_LINE_ID = "comp_4727e04b_4e82_48b2_bff0_8cd383d4d70d"


class DummyReceiver:
    def __init__(self, messages):
        self.messages = list(messages)

    def __iter__(self):
        return self

    def __next__(self):
        raise StopIteration

    def waitFor(self, timeout):
        return True


class DummyJob:
    def write(self):
        raise AssertionError("PowerFlowResult tests do not use sender")


def build_local_model():
    return Model(
        {
            "name": "local-model",
            "rid": "model/test/local-model",
            "jobs": [],
            "configs": [],
            "context": {"currentJob": 0, "currentConfig": 0},
            "revision": {
                "hash": "local-hash",
                "version": 4,
                "implements": {
                    "diagram": {
                        "canvas": [{"key": "canvas_0"}],
                        "cells": {},
                    }
                },
                "parameters": [],
                "pins": {},
                "documentation": {},
            },
        }
    )


def wait_for_completion(job, timeout=300, interval=5):
    start = time.time()
    while True:
        status = job.status()
        if status == 1:
            return
        if status == 2:
            pytest.fail("power flow job failed on CloudPSS")
        if time.time() - start > timeout:
            pytest.fail("power flow job timed out")
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


def bus_row_by_bus_id(rows, bus_id):
    return next(row for row in rows if row[BUS_COLUMN] == bus_id)


def bus_row_by_node_id(rows, node_id):
    return next(row for row in rows if row[NODE_COLUMN] == node_id)


def branch_row_by_id(rows, branch_id):
    return next(row for row in rows if row[BRANCH_COLUMN] == branch_id)


def run_powerflow_tables(model):
    job = model.runPowerFlow()
    wait_for_completion(job)
    return table_rows(job.result.getBuses()[0]), table_rows(job.result.getBranches()[0])


def ieee39_study_metrics(bus_rows, branch_rows):
    slack_bus = bus_row_by_node_id(bus_rows, "canvas_10_399")
    gen30_bus = bus_row_by_node_id(bus_rows, "canvas_2_303")
    gen38_bus = bus_row_by_node_id(bus_rows, "canvas_9_384")
    bus21 = bus_row_by_bus_id(bus_rows, "canvas_0_154")
    line_26_28 = next((row for row in branch_rows if row[BRANCH_COLUMN] == "canvas_0_126"), None)
    line_26_29 = branch_row_by_id(branch_rows, "canvas_0_134")
    line_28_29 = branch_row_by_id(branch_rows, "canvas_0_130")
    line_21_22 = branch_row_by_id(branch_rows, "canvas_0_175")
    line_22_23 = branch_row_by_id(branch_rows, "canvas_0_182")
    line_23_24 = branch_row_by_id(branch_rows, "canvas_0_185")

    return {
        "slack_p_gen": slack_bus[P_GEN_COLUMN],
        "slack_q_gen": slack_bus[Q_GEN_COLUMN],
        "bus30_vm": gen30_bus[VM_COLUMN],
        "bus30_q_gen": gen30_bus[Q_GEN_COLUMN],
        "gen38_p_gen": gen38_bus[P_GEN_COLUMN],
        "gen38_q_gen": gen38_bus[Q_GEN_COLUMN],
        "bus21_vm": bus21[VM_COLUMN],
        "line_26_28_abs_pij": abs(line_26_28[P_IJ_COLUMN]) if line_26_28 is not None else None,
        "line_26_29_abs_pij": abs(line_26_29[P_IJ_COLUMN]),
        "line_28_29_abs_pij": abs(line_28_29[P_IJ_COLUMN]),
        "line_21_22_abs_pij": abs(line_21_22[P_IJ_COLUMN]),
        "line_22_23_abs_pij": abs(line_22_23[P_IJ_COLUMN]),
        "line_23_24_abs_pij": abs(line_23_24[P_IJ_COLUMN]),
    }


def ieee39_n1_metrics(base_bus_rows, base_branch_rows, outage_bus_rows, outage_branch_rows):
    base_bus_by_id = {row[BUS_COLUMN]: row for row in base_bus_rows}
    outage_bus_by_id = {row[BUS_COLUMN]: row for row in outage_bus_rows}
    base_branch_ids = {row[BRANCH_COLUMN] for row in base_branch_rows}
    outage_branch_ids = {row[BRANCH_COLUMN] for row in outage_branch_rows}

    base_low_voltage_buses = {
        bus_id for bus_id, row in base_bus_by_id.items() if row[VM_COLUMN] < 0.95
    }
    outage_low_voltage_buses = {
        row[BUS_COLUMN] for row in outage_bus_rows if row[VM_COLUMN] < 0.95
    }
    base_high_voltage_buses = {
        bus_id for bus_id, row in base_bus_by_id.items() if row[VM_COLUMN] > 1.05
    }
    outage_high_voltage_buses = {
        row[BUS_COLUMN] for row in outage_bus_rows if row[VM_COLUMN] > 1.05
    }
    missing_bus_ids = sorted(set(base_bus_by_id) - set(outage_bus_by_id))
    missing_branch_ids = sorted(base_branch_ids - outage_branch_ids)

    comparable_bus_ids = set(base_bus_by_id).intersection(outage_bus_by_id)
    max_vm_shift = 0.0
    max_vm_shift_bus_id = None
    for bus_id in comparable_bus_ids:
        candidate_shift = abs(outage_bus_by_id[bus_id][VM_COLUMN] - base_bus_by_id[bus_id][VM_COLUMN])
        if candidate_shift > max_vm_shift:
            max_vm_shift = candidate_shift
            max_vm_shift_bus_id = bus_id

    comparable_branch_ids = base_branch_ids.intersection(outage_branch_ids)
    max_branch_shift = 0.0
    max_branch_shift_branch_id = None
    for branch_id in comparable_branch_ids:
        candidate_shift = abs(
            abs(branch_row_by_id(outage_branch_rows, branch_id)[P_IJ_COLUMN])
            - abs(branch_row_by_id(base_branch_rows, branch_id)[P_IJ_COLUMN])
        )
        if candidate_shift > max_branch_shift:
            max_branch_shift = candidate_shift
            max_branch_shift_branch_id = branch_id

    min_vm_row = min(outage_bus_rows, key=lambda row: row[VM_COLUMN])

    return {
        "min_vm": min_vm_row[VM_COLUMN],
        "min_vm_bus_id": min_vm_row[BUS_COLUMN],
        "new_low_voltage_bus_count": len(outage_low_voltage_buses - base_low_voltage_buses),
        "new_high_voltage_bus_count": len(outage_high_voltage_buses - base_high_voltage_buses),
        "missing_bus_count": len(missing_bus_ids),
        "missing_bus_ids": missing_bus_ids,
        "missing_branch_count": len(missing_branch_ids),
        "missing_branch_ids": missing_branch_ids,
        "max_vm_shift": max_vm_shift,
        "max_vm_shift_bus_id": max_vm_shift_bus_id,
        "max_branch_shift": max_branch_shift,
        "max_branch_shift_branch_id": max_branch_shift_branch_id,
    }


def classify_ieee39_n1_severity(metrics):
    if metrics["new_low_voltage_bus_count"] > 0 or metrics["new_high_voltage_bus_count"] > 0:
        return "critical"
    if metrics["min_vm"] < 0.91 or metrics["max_branch_shift"] > 100.0:
        return "warning"
    return "observe"


def ieee39_n1_severity_rank(metrics):
    return {
        "critical": 2,
        "warning": 1,
        "observe": 0,
    }[classify_ieee39_n1_severity(metrics)]


def study_branch_name(component):
    return component.args.get("Name") or component.label or component.id


def study_branch_kind(component):
    if component.definition == TRANSFORMER_RID:
        return "transformer"
    return "line"


def ieee39_active_branch_components(model, base_branch_rows, include_transformers=True):
    base_branch_ids = {row[BRANCH_COLUMN] for row in base_branch_rows}
    candidate_components = list(model.getComponentsByRid(TRANSMISSION_LINE_RID).values())
    if include_transformers:
        candidate_components.extend(model.getComponentsByRid(TRANSFORMER_RID).values())

    return sorted(
        [
            component
            for component in candidate_components
            if component.id in base_branch_ids
        ],
        key=lambda component: (study_branch_name(component), component.id),
    )


@pytest.fixture(scope="module")
def ieee39_full_active_branch_n1_results(integration_model):
    base_bus_rows, base_branch_rows = run_powerflow_tables(Model(deepcopy(integration_model.toJSON())))
    all_active_branch_components = ieee39_active_branch_components(
        integration_model,
        base_branch_rows=base_branch_rows,
        include_transformers=True,
    )

    full_results = []
    for branch in all_active_branch_components:
        working_model = Model(deepcopy(integration_model.toJSON()))
        target_branch = working_model.getComponentByKey(branch.id)
        working_model.updateComponent(target_branch.id, props={"enabled": False})

        outage_job = working_model.runPowerFlow()
        wait_for_completion(outage_job)
        outage_bus_rows = table_rows(outage_job.result.getBuses()[0])
        outage_branch_rows = table_rows(outage_job.result.getBranches()[0])
        metrics = ieee39_n1_metrics(
            base_bus_rows=base_bus_rows,
            base_branch_rows=base_branch_rows,
            outage_bus_rows=outage_bus_rows,
            outage_branch_rows=outage_branch_rows,
        )

        full_results.append(
            {
                "branch_id": branch.id,
                "branch_name": study_branch_name(branch),
                "branch_kind": study_branch_kind(branch),
                "branch_present_after_outage": any(
                    row[BRANCH_COLUMN] == branch.id for row in outage_branch_rows
                ),
                **metrics,
                "severity": classify_ieee39_n1_severity(metrics),
            }
        )

    ranked_results = sorted(
        full_results,
        key=lambda item: (
            ieee39_n1_severity_rank(item),
            item["new_low_voltage_bus_count"] + item["new_high_voltage_bus_count"],
            max(0.0, 0.95 - item["min_vm"]),
            item["max_vm_shift"],
            item["max_branch_shift"],
        ),
        reverse=True,
    )

    return ranked_results


class TestPowerFlowResultUnit:
    def test_get_messages_by_key_returns_matching_entries(self):
        result = PowerFlowResult(
            DummyJob(),
            DummyReceiver(
                [
                    {"key": "summary", "data": {"value": "ignore"}},
                    {"key": "buses-table", "data": {"value": 1}},
                    {"key": "buses-table", "data": {"value": 2}},
                ]
            ),
        )

        messages = result.getMessagesByKey("buses-table")

        assert messages == [
            {"key": "buses-table", "data": {"value": 1}},
            {"key": "buses-table", "data": {"value": 2}},
        ]

    def test_get_buses_strips_html_wrappers(self):
        result = PowerFlowResult(
            DummyJob(),
            DummyReceiver(
                [
                    {
                        "key": "buses-table",
                        "data": {
                            "columns": [
                                {"title": "Bus", "type": "html", "data": ['<input value="1/"/>']},
                                {"title": "V(pu)", "type": "text", "data": ["1.00"]},
                            ]
                        },
                    }
                ]
            ),
        )

        buses = result.getBuses()

        assert isinstance(buses, list)
        assert buses[0]["data"]["columns"][0]["data"] == ["1"]

    def test_get_branches_strips_html_wrappers(self):
        result = PowerFlowResult(
            DummyJob(),
            DummyReceiver(
                [
                    {
                        "key": "branches-table",
                        "data": {
                            "columns": [
                                {"title": "From", "type": "html", "data": ['<input value="1/"/>']},
                                {"title": "To", "type": "text", "data": ["2"]},
                            ]
                        },
                    }
                ]
            ),
        )

        branches = result.getBranches()

        assert isinstance(branches, list)
        assert branches[0]["data"]["columns"][0]["data"] == ["1"]

    def test_powerflow_modify_applies_payload(self):
        model_dict = build_local_model().toJSON()
        result = PowerFlowResult(
            DummyJob(),
            DummyReceiver(
                [
                    {
                        "key": "power-flow-modify",
                        "data": {"payload": {"name": "modified-name", "context": {"currentConfig": 2}}},
                    }
                ]
            ),
        )

        return_value = result.powerFlowModify(model_dict)

        assert return_value is None
        assert model_dict["name"] == "modified-name"
        assert model_dict["context"]["currentConfig"] == 2

    def test_powerflow_modify_raises_when_modify_message_is_missing(self):
        model_dict = build_local_model().toJSON()
        result = PowerFlowResult(
            DummyJob(),
            DummyReceiver(
                [
                    {
                        "key": "buses-table",
                        "data": {"columns": []},
                    }
                ]
            ),
        )

        with pytest.raises(Exception, match="未找到到数据"):
            result.powerFlowModify(model_dict)


@pytest.fixture(scope="module")
def completed_powerflow_job(integration_model):
    job = integration_model.runPowerFlow()
    wait_for_completion(job)
    return job


@pytest.mark.integration
class TestPowerFlowResultIntegration:
    def test_get_messages_by_key_returns_raw_tables(self, completed_powerflow_job):
        result = completed_powerflow_job.result
        messages = result.getMessagesByKey("buses-table")

        assert isinstance(messages, list)
        assert messages
        assert messages[0]["key"] == "buses-table"
        assert "columns" in messages[0]["data"]

    def test_get_buses_returns_parsed_tables(self, completed_powerflow_job):
        result = completed_powerflow_job.result
        buses = result.getBuses()

        assert isinstance(result, PowerFlowResult)
        assert isinstance(buses, list)
        assert buses
        assert "columns" in buses[0]["data"]

    def test_get_branches_returns_parsed_tables(self, completed_powerflow_job):
        result = completed_powerflow_job.result
        branches = result.getBranches()

        assert isinstance(branches, list)
        assert branches
        assert "columns" in branches[0]["data"]

    def test_powerflow_modify_updates_local_model_dict_from_live_result(
        self, integration_model, completed_powerflow_job
    ):
        result = completed_powerflow_job.result
        original_model_dict = integration_model.toJSON()
        modified_model_dict = deepcopy(original_model_dict)

        result.powerFlowModify(modified_model_dict)
        rebuilt_model = Model(modified_model_dict)

        assert isinstance(rebuilt_model, Model)
        assert modified_model_dict != original_model_dict
        assert rebuilt_model.name == modified_model_dict["name"]
        assert rebuilt_model.context == modified_model_dict["context"]

    def test_local_yaml_copy_can_run_powerflow_and_return_tables(
        self, integration_model, tmp_path
    ):
        export_path = tmp_path / "ieee39-working-copy.yaml"
        Model.dump(integration_model, str(export_path), compress=None)
        local_model = Model.load(str(export_path))

        job = local_model.runPowerFlow()
        wait_for_completion(job)

        assert job.status() == 1

        result = job.result
        buses = result.getBuses()
        branches = result.getBranches()

        assert buses
        assert branches

    def test_ieee39_load_perturbation_rebalances_local_slack_bus_generation(
        self, integration_model, completed_powerflow_job
    ):
        base_rows = table_rows(completed_powerflow_job.result.getBuses()[0])
        base_row = next(row for row in base_rows if row[NODE_COLUMN] == "canvas_10_399")

        working_model = Model(deepcopy(integration_model.toJSON()))
        load_39 = next(
            component
            for component in working_model.getAllComponents().values()
            if component.toJSON().get("definition") == "model/CloudPSS/_newExpLoad_3p"
            and component.toJSON().get("args", {}).get("Name") == "load-39"
        )
        working_model.updateComponent(
            load_39.id,
            args={
                **load_39.args,
                "p": {"source": "1400", "ɵexp": ""},
                "q": {"source": "350", "ɵexp": ""},
            },
        )

        perturbed_job = working_model.runPowerFlow()
        wait_for_completion(perturbed_job)

        perturbed_rows = table_rows(perturbed_job.result.getBuses()[0])
        perturbed_row = next(row for row in perturbed_rows if row[BUS_COLUMN] == base_row[BUS_COLUMN])

        assert perturbed_row[P_LOAD_COLUMN] == pytest.approx(1400.0)
        assert perturbed_row[Q_LOAD_COLUMN] == pytest.approx(350.0)
        assert perturbed_row[P_LOAD_COLUMN] - base_row[P_LOAD_COLUMN] == pytest.approx(296.0)
        assert perturbed_row[Q_LOAD_COLUMN] - base_row[Q_LOAD_COLUMN] == pytest.approx(100.0)

        # IEEE39 的这个研究场景把更大的负荷加在与平衡机组同母线的位置。
        # 对当前已验证算例，平衡机组有功/无功出力会同步抬升来平衡系统。
        assert perturbed_row[P_GEN_COLUMN] - base_row[P_GEN_COLUMN] == pytest.approx(296.0, abs=1e-3)
        assert perturbed_row[Q_GEN_COLUMN] - base_row[Q_GEN_COLUMN] == pytest.approx(100.0, abs=1e-3)

    def test_powerflow_modify_written_model_can_rerun_with_nearly_identical_bus_results(
        self, integration_model, completed_powerflow_job
    ):
        original_rows = table_rows(completed_powerflow_job.result.getBuses()[0])
        modified_model_dict = deepcopy(integration_model.toJSON())
        completed_powerflow_job.result.powerFlowModify(modified_model_dict)
        modified_model = Model(modified_model_dict)

        rerun_job = modified_model.runPowerFlow()
        wait_for_completion(rerun_job)
        rerun_rows = table_rows(rerun_job.result.getBuses()[0])

        for bus_id in ["canvas_0_35", "canvas_0_10", "canvas_0_43"]:
            original_row = next(row for row in original_rows if row[BUS_COLUMN] == bus_id)
            rerun_row = next(row for row in rerun_rows if row[BUS_COLUMN] == bus_id)

            assert rerun_row[VM_COLUMN] == pytest.approx(
                original_row[VM_COLUMN],
                abs=1e-9,
            )
            assert rerun_row[VA_COLUMN] == pytest.approx(
                original_row[VA_COLUMN],
                abs=2e-6,
            )
            assert rerun_row[P_GEN_COLUMN] == pytest.approx(
                original_row[P_GEN_COLUMN],
                abs=5e-4,
            )
            assert rerun_row[Q_GEN_COLUMN] == pytest.approx(
                original_row[Q_GEN_COLUMN],
                abs=5e-4,
            )

    def test_ieee39_line_reactance_perturbation_redistributes_branch_flow_and_bus_angle(
        self, integration_model, completed_powerflow_job
    ):
        base_branch_rows = table_rows(completed_powerflow_job.result.getBranches()[0])
        base_bus_rows = table_rows(completed_powerflow_job.result.getBuses()[0])
        base_branch = next(
            row for row in base_branch_rows if row[BRANCH_COLUMN] == "canvas_0_126"
        )
        base_from_bus = next(
            row for row in base_bus_rows if row[BUS_COLUMN] == base_branch["From bus"]
        )
        base_to_bus = next(
            row for row in base_bus_rows if row[BUS_COLUMN] == base_branch["To bus"]
        )

        working_model = Model(deepcopy(integration_model.toJSON()))
        target_line = working_model.getComponentByKey("canvas_0_126")

        working_model.updateComponent(
            target_line.id,
            args={
                **target_line.args,
                "X1pu": {"source": "0.0600", "ɵexp": ""},
            },
        )

        perturbed_job = working_model.runPowerFlow()
        wait_for_completion(perturbed_job)

        perturbed_branch_rows = table_rows(perturbed_job.result.getBranches()[0])
        perturbed_bus_rows = table_rows(perturbed_job.result.getBuses()[0])
        perturbed_branch = next(
            row for row in perturbed_branch_rows if row[BRANCH_COLUMN] == "canvas_0_126"
        )
        perturbed_from_bus = next(
            row for row in perturbed_bus_rows if row[BUS_COLUMN] == perturbed_branch["From bus"]
        )
        perturbed_to_bus = next(
            row for row in perturbed_bus_rows if row[BUS_COLUMN] == perturbed_branch["To bus"]
        )

        # IEEE39 的 line-26-28 在提高串联电抗后，线路传输能力下降，
        # 邻近母线相角与电压会出现可观测偏移。
        assert abs(base_branch[P_IJ_COLUMN]) - abs(perturbed_branch[P_IJ_COLUMN]) > 10.0
        assert abs(base_branch[P_JI_COLUMN]) - abs(perturbed_branch[P_JI_COLUMN]) > 10.0
        assert perturbed_from_bus[VM_COLUMN] < base_from_bus[VM_COLUMN] - 1e-4
        assert perturbed_to_bus[VA_COLUMN] > base_to_bus[VA_COLUMN] + 0.3

    def test_ieee39_line_outage_redistributes_corridor_flow_and_shifts_local_bus_state(
        self, integration_model, completed_powerflow_job
    ):
        base_branch_rows = table_rows(completed_powerflow_job.result.getBranches()[0])
        base_bus_rows = table_rows(completed_powerflow_job.result.getBuses()[0])
        target_branch = branch_row_by_id(base_branch_rows, "canvas_0_126")
        base_from_bus = bus_row_by_bus_id(base_bus_rows, target_branch["From bus"])
        base_to_bus = bus_row_by_bus_id(base_bus_rows, target_branch["To bus"])

        working_model = Model(deepcopy(integration_model.toJSON()))
        target_line = working_model.getComponentByKey("canvas_0_126")
        working_model.removeComponent(target_line.id)

        outage_job = working_model.runPowerFlow()
        wait_for_completion(outage_job)

        outage_branch_rows = table_rows(outage_job.result.getBranches()[0])
        outage_bus_rows = table_rows(outage_job.result.getBuses()[0])
        outage_from_bus = bus_row_by_bus_id(outage_bus_rows, target_branch["From bus"])
        outage_to_bus = bus_row_by_bus_id(outage_bus_rows, target_branch["To bus"])
        rerouted_branch = branch_row_by_id(outage_branch_rows, "canvas_0_134")
        base_rerouted_branch = branch_row_by_id(base_branch_rows, "canvas_0_134")
        relieved_branch = branch_row_by_id(outage_branch_rows, "canvas_0_130")
        base_relieved_branch = branch_row_by_id(base_branch_rows, "canvas_0_130")

        assert not any(row[BRANCH_COLUMN] == "canvas_0_126" for row in outage_branch_rows)

        # 切除 IEEE39 的 line-26-28 后，26-29 走廊会明显增载，28-29 走廊会明显卸载，
        # 同时被切除支路两端母线电压与相角也会出现可观测偏移。
        assert abs(rerouted_branch[P_IJ_COLUMN]) - abs(base_rerouted_branch[P_IJ_COLUMN]) > 100.0
        assert abs(base_relieved_branch[P_IJ_COLUMN]) - abs(relieved_branch[P_IJ_COLUMN]) > 100.0
        assert outage_from_bus[VM_COLUMN] < base_from_bus[VM_COLUMN] - 0.01
        assert outage_to_bus[VM_COLUMN] < base_to_bus[VM_COLUMN] - 0.005
        assert outage_to_bus[VA_COLUMN] > base_to_bus[VA_COLUMN] + 5.0

    def test_ieee39_generator_voltage_setpoint_adjustment_changes_local_bus_voltage_and_q_support(
        self, integration_model, completed_powerflow_job
    ):
        base_bus_rows = table_rows(completed_powerflow_job.result.getBuses()[0])
        base_generator_bus = bus_row_by_node_id(base_bus_rows, "canvas_2_303")
        nearby_bus = bus_row_by_bus_id(base_bus_rows, "canvas_0_27")

        working_model = Model(deepcopy(integration_model.toJSON()))
        gen30 = working_model.getComponentByKey("canvas_2_303")
        working_model.updateComponent(
            gen30.id,
            args={
                **gen30.args,
                "pf_V": {"source": "1.070", "ɵexp": ""},
            },
        )

        adjusted_job = working_model.runPowerFlow()
        wait_for_completion(adjusted_job)

        adjusted_bus_rows = table_rows(adjusted_job.result.getBuses()[0])
        adjusted_generator_bus = bus_row_by_node_id(adjusted_bus_rows, "canvas_2_303")
        adjusted_nearby_bus = bus_row_by_bus_id(adjusted_bus_rows, "canvas_0_27")

        # IEEE39 的 Gen30 是一个干净的电压控制场景：提高 pf_V 后，
        # 机端母线电压应基本跟随设定值抬升，机组无功支撑同步增加，邻近母线电压也会被带动上升。
        assert adjusted_generator_bus[VM_COLUMN] == pytest.approx(1.07, abs=1e-9)
        assert adjusted_generator_bus[VM_COLUMN] - base_generator_bus[VM_COLUMN] > 0.02
        assert adjusted_generator_bus[Q_GEN_COLUMN] - base_generator_bus[Q_GEN_COLUMN] > 60.0
        assert adjusted_generator_bus[P_GEN_COLUMN] == pytest.approx(
            base_generator_bus[P_GEN_COLUMN],
            abs=1e-6,
        )
        assert adjusted_nearby_bus[VM_COLUMN] > nearby_bus[VM_COLUMN] + 0.01

    def test_ieee39_generator_active_power_redispatch_shifts_slack_and_key_transfer_corridors(
        self, integration_model, completed_powerflow_job
    ):
        base_bus_rows = table_rows(completed_powerflow_job.result.getBuses()[0])
        base_branch_rows = table_rows(completed_powerflow_job.result.getBranches()[0])
        base_gen38_bus = bus_row_by_node_id(base_bus_rows, "canvas_9_384")
        base_slack_bus = bus_row_by_node_id(base_bus_rows, "canvas_10_399")
        base_transformer = branch_row_by_id(base_branch_rows, "canvas_0_258")
        base_line_26_28 = branch_row_by_id(base_branch_rows, "canvas_0_126")
        base_line_26_29 = branch_row_by_id(base_branch_rows, "canvas_0_134")
        base_line_28_29 = branch_row_by_id(base_branch_rows, "canvas_0_130")
        base_line_26_27 = branch_row_by_id(base_branch_rows, "canvas_0_123")

        working_model = Model(deepcopy(integration_model.toJSON()))
        gen38 = working_model.getComponentByKey("canvas_9_384")
        working_model.updateComponent(
            gen38.id,
            args={**gen38.args, "pf_P": {"source": "900", "ɵexp": ""}},
        )

        adjusted_job = working_model.runPowerFlow()
        wait_for_completion(adjusted_job)

        adjusted_bus_rows = table_rows(adjusted_job.result.getBuses()[0])
        adjusted_branch_rows = table_rows(adjusted_job.result.getBranches()[0])
        adjusted_gen38_bus = bus_row_by_node_id(adjusted_bus_rows, "canvas_9_384")
        adjusted_slack_bus = bus_row_by_node_id(adjusted_bus_rows, "canvas_10_399")
        adjusted_transformer = branch_row_by_id(adjusted_branch_rows, "canvas_0_258")
        adjusted_line_26_28 = branch_row_by_id(adjusted_branch_rows, "canvas_0_126")
        adjusted_line_26_29 = branch_row_by_id(adjusted_branch_rows, "canvas_0_134")
        adjusted_line_28_29 = branch_row_by_id(adjusted_branch_rows, "canvas_0_130")
        adjusted_line_26_27 = branch_row_by_id(adjusted_branch_rows, "canvas_0_123")

        # IEEE39 的 Gen38 有功上调会形成一个很干净的转移场景：
        # 机组自身增发、平衡机组减发，同时 33 侧送出和 26-27-28-29 走廊潮流都会明显抬升。
        assert adjusted_gen38_bus[P_GEN_COLUMN] == pytest.approx(900.0, abs=1e-9)
        assert base_slack_bus[P_GEN_COLUMN] - adjusted_slack_bus[P_GEN_COLUMN] > 60.0
        assert adjusted_gen38_bus[Q_GEN_COLUMN] - base_gen38_bus[Q_GEN_COLUMN] > 15.0
        assert abs(adjusted_transformer[P_IJ_COLUMN]) - abs(base_transformer[P_IJ_COLUMN]) > 60.0
        assert abs(adjusted_line_26_28[P_IJ_COLUMN]) - abs(base_line_26_28[P_IJ_COLUMN]) > 30.0
        assert abs(adjusted_line_26_29[P_IJ_COLUMN]) - abs(base_line_26_29[P_IJ_COLUMN]) > 30.0
        assert abs(adjusted_line_28_29[P_IJ_COLUMN]) - abs(base_line_28_29[P_IJ_COLUMN]) > 30.0
        assert abs(adjusted_line_26_27[P_IJ_COLUMN]) - abs(base_line_26_27[P_IJ_COLUMN]) > 30.0

    def test_ieee39_load_transfer_from_bus39_to_bus21_shifts_remote_corridor_with_nearly_constant_total_demand(
        self, integration_model, completed_powerflow_job
    ):
        base_bus_rows = table_rows(completed_powerflow_job.result.getBuses()[0])
        base_branch_rows = table_rows(completed_powerflow_job.result.getBranches()[0])
        baseline_metrics = ieee39_study_metrics(base_bus_rows, base_branch_rows)

        transfer_model = Model(deepcopy(integration_model.toJSON()))
        source_load = transfer_model.getComponentByKey("canvas_0_446")
        target_load = transfer_model.getComponentByKey("canvas_0_428")
        transfer_model.updateComponent(
            source_load.id,
            args={
                **source_load.args,
                "p": {"source": "904", "ɵexp": ""},
                "q": {"source": "190", "ɵexp": ""},
            },
        )
        transfer_model.updateComponent(
            target_load.id,
            args={
                **target_load.args,
                "p": {"source": "474", "ɵexp": ""},
                "q": {"source": "175", "ɵexp": ""},
            },
        )

        transfer_job = transfer_model.runPowerFlow()
        wait_for_completion(transfer_job)
        transfer_metrics = ieee39_study_metrics(
            table_rows(transfer_job.result.getBuses()[0]),
            table_rows(transfer_job.result.getBranches()[0]),
        )

        assert abs(transfer_metrics["slack_p_gen"] - baseline_metrics["slack_p_gen"]) < 2.0
        assert transfer_metrics["slack_q_gen"] < baseline_metrics["slack_q_gen"] - 50.0
        assert transfer_metrics["bus21_vm"] < baseline_metrics["bus21_vm"] - 0.008
        assert (
            transfer_metrics["line_21_22_abs_pij"]
            - baseline_metrics["line_21_22_abs_pij"]
            > 30.0
        )
        assert (
            baseline_metrics["line_22_23_abs_pij"]
            - transfer_metrics["line_22_23_abs_pij"]
            > 30.0
        )
        assert (
            baseline_metrics["line_23_24_abs_pij"]
            - transfer_metrics["line_23_24_abs_pij"]
            > 30.0
        )

    def test_ieee39_reactive_stress_on_load21_depresses_local_voltage_and_raises_system_q_support(
        self, integration_model, completed_powerflow_job
    ):
        base_bus_rows = table_rows(completed_powerflow_job.result.getBuses()[0])
        base_branch_rows = table_rows(completed_powerflow_job.result.getBranches()[0])
        baseline_metrics = ieee39_study_metrics(base_bus_rows, base_branch_rows)
        base_bus_by_id = {row[BUS_COLUMN]: row for row in base_bus_rows}

        stressed_model = Model(deepcopy(integration_model.toJSON()))
        target_load = stressed_model.getComponentByKey("canvas_0_428")
        stressed_model.updateComponent(
            target_load.id,
            args={
                **target_load.args,
                "q": {"source": "215", "ɵexp": ""},
            },
        )

        stressed_job = stressed_model.runPowerFlow()
        wait_for_completion(stressed_job)
        stressed_bus_rows = table_rows(stressed_job.result.getBuses()[0])
        stressed_branch_rows = table_rows(stressed_job.result.getBranches()[0])
        stressed_metrics = ieee39_study_metrics(stressed_bus_rows, stressed_branch_rows)
        stressed_bus_by_id = {row[BUS_COLUMN]: row for row in stressed_bus_rows}

        reactive_support_changes = sorted(
            [
                (
                    row[BUS_COLUMN],
                    row[Q_GEN_COLUMN] - base_bus_by_id[row[BUS_COLUMN]][Q_GEN_COLUMN],
                )
                for row in stressed_bus_rows
                if row[Q_GEN_COLUMN] - base_bus_by_id[row[BUS_COLUMN]][Q_GEN_COLUMN] > 0.5
            ],
            key=lambda item: item[1],
            reverse=True,
        )

        # 这条场景强调“无功压力导致的局部电压走弱”，而不是有功转移。
        # 预期是 bus21 附近母线电压明显下探，平衡机组和远端发电机群提供更多无功支撑，
        # 但关键有功走廊只出现很小的幅值变化。
        assert stressed_metrics["bus21_vm"] < baseline_metrics["bus21_vm"] - 0.013
        assert stressed_metrics["slack_q_gen"] > baseline_metrics["slack_q_gen"] + 4.0
        assert abs(stressed_metrics["slack_p_gen"] - baseline_metrics["slack_p_gen"]) < 1.0
        assert abs(
            stressed_metrics["line_21_22_abs_pij"] - baseline_metrics["line_21_22_abs_pij"]
        ) < 2.0
        assert reactive_support_changes[0][0] == "canvas_0_152"
        assert reactive_support_changes[0][1] > 40.0
        assert reactive_support_changes[1][0] == "canvas_0_189"

    def test_ieee39_batch_powerflow_study_summaries_capture_expected_directional_changes(
        self, integration_model, completed_powerflow_job
    ):
        base_bus_rows = table_rows(completed_powerflow_job.result.getBuses()[0])
        base_branch_rows = table_rows(completed_powerflow_job.result.getBranches()[0])
        baseline_metrics = ieee39_study_metrics(base_bus_rows, base_branch_rows)

        scenario_metrics = {"baseline": baseline_metrics}

        load_model = Model(deepcopy(integration_model.toJSON()))
        load_39 = next(
            component
            for component in load_model.getAllComponents().values()
            if component.toJSON().get("definition") == "model/CloudPSS/_newExpLoad_3p"
            and component.toJSON().get("args", {}).get("Name") == "load-39"
        )
        load_model.updateComponent(
            load_39.id,
            args={
                **load_39.args,
                "p": {"source": "1400", "ɵexp": ""},
                "q": {"source": "350", "ɵexp": ""},
            },
        )
        load_job = load_model.runPowerFlow()
        wait_for_completion(load_job)
        scenario_metrics["load_up"] = ieee39_study_metrics(
            table_rows(load_job.result.getBuses()[0]),
            table_rows(load_job.result.getBranches()[0]),
        )

        reactance_model = Model(deepcopy(integration_model.toJSON()))
        target_line = reactance_model.getComponentByKey("canvas_0_126")
        reactance_model.updateComponent(
            target_line.id,
            args={**target_line.args, "X1pu": {"source": "0.0600", "ɵexp": ""}},
        )
        reactance_job = reactance_model.runPowerFlow()
        wait_for_completion(reactance_job)
        scenario_metrics["line_x_up"] = ieee39_study_metrics(
            table_rows(reactance_job.result.getBuses()[0]),
            table_rows(reactance_job.result.getBranches()[0]),
        )

        outage_model = Model(deepcopy(integration_model.toJSON()))
        outage_model.removeComponent("canvas_0_126")
        outage_job = outage_model.runPowerFlow()
        wait_for_completion(outage_job)
        scenario_metrics["line_outage"] = ieee39_study_metrics(
            table_rows(outage_job.result.getBuses()[0]),
            table_rows(outage_job.result.getBranches()[0]),
        )

        voltage_model = Model(deepcopy(integration_model.toJSON()))
        gen30 = voltage_model.getComponentByKey("canvas_2_303")
        voltage_model.updateComponent(
            gen30.id,
            args={**gen30.args, "pf_V": {"source": "1.070", "ɵexp": ""}},
        )
        voltage_job = voltage_model.runPowerFlow()
        wait_for_completion(voltage_job)
        scenario_metrics["gen30_v_up"] = ieee39_study_metrics(
            table_rows(voltage_job.result.getBuses()[0]),
            table_rows(voltage_job.result.getBranches()[0]),
        )

        redispatch_model = Model(deepcopy(integration_model.toJSON()))
        gen38 = redispatch_model.getComponentByKey("canvas_9_384")
        redispatch_model.updateComponent(
            gen38.id,
            args={**gen38.args, "pf_P": {"source": "900", "ɵexp": ""}},
        )
        redispatch_job = redispatch_model.runPowerFlow()
        wait_for_completion(redispatch_job)
        scenario_metrics["gen38_p_up"] = ieee39_study_metrics(
            table_rows(redispatch_job.result.getBuses()[0]),
            table_rows(redispatch_job.result.getBranches()[0]),
        )

        transfer_model = Model(deepcopy(integration_model.toJSON()))
        source_load = transfer_model.getComponentByKey("canvas_0_446")
        target_load = transfer_model.getComponentByKey("canvas_0_428")
        transfer_model.updateComponent(
            source_load.id,
            args={
                **source_load.args,
                "p": {"source": "904", "ɵexp": ""},
                "q": {"source": "190", "ɵexp": ""},
            },
        )
        transfer_model.updateComponent(
            target_load.id,
            args={
                **target_load.args,
                "p": {"source": "474", "ɵexp": ""},
                "q": {"source": "175", "ɵexp": ""},
            },
        )
        transfer_job = transfer_model.runPowerFlow()
        wait_for_completion(transfer_job)
        scenario_metrics["load_shift_39_to_21"] = ieee39_study_metrics(
            table_rows(transfer_job.result.getBuses()[0]),
            table_rows(transfer_job.result.getBranches()[0]),
        )

        reactive_model = Model(deepcopy(integration_model.toJSON()))
        target_load = reactive_model.getComponentByKey("canvas_0_428")
        reactive_model.updateComponent(
            target_load.id,
            args={
                **target_load.args,
                "q": {"source": "215", "ɵexp": ""},
            },
        )
        reactive_job = reactive_model.runPowerFlow()
        wait_for_completion(reactive_job)
        scenario_metrics["load21_q_up"] = ieee39_study_metrics(
            table_rows(reactive_job.result.getBuses()[0]),
            table_rows(reactive_job.result.getBranches()[0]),
        )

        # 这条批量研究场景把当前已验证的高频潮流动作串成一份汇总表，
        # 重点不是“每个工况都成功”，而是各工况的关键指标变化方向与工程直觉一致。
        assert scenario_metrics["load_up"]["slack_p_gen"] - baseline_metrics["slack_p_gen"] == pytest.approx(
            296.0,
            abs=1e-3,
        )
        assert (
            baseline_metrics["line_26_28_abs_pij"]
            - scenario_metrics["line_x_up"]["line_26_28_abs_pij"]
            > 10.0
        )
        assert scenario_metrics["line_outage"]["line_26_28_abs_pij"] is None
        assert (
            scenario_metrics["line_outage"]["line_26_29_abs_pij"]
            - baseline_metrics["line_26_29_abs_pij"]
            > 100.0
        )
        assert (
            baseline_metrics["line_28_29_abs_pij"]
            - scenario_metrics["line_outage"]["line_28_29_abs_pij"]
            > 100.0
        )
        assert scenario_metrics["gen30_v_up"]["bus30_vm"] > baseline_metrics["bus30_vm"] + 0.02
        assert scenario_metrics["gen30_v_up"]["bus30_q_gen"] > baseline_metrics["bus30_q_gen"] + 60.0
        assert scenario_metrics["gen38_p_up"]["gen38_p_gen"] == pytest.approx(900.0, abs=1e-9)
        assert baseline_metrics["slack_p_gen"] - scenario_metrics["gen38_p_up"]["slack_p_gen"] > 60.0
        assert (
            scenario_metrics["gen38_p_up"]["line_26_28_abs_pij"]
            - baseline_metrics["line_26_28_abs_pij"]
            > 30.0
        )
        assert (
            abs(scenario_metrics["load_shift_39_to_21"]["slack_p_gen"] - baseline_metrics["slack_p_gen"])
            < 2.0
        )
        assert (
            scenario_metrics["load_shift_39_to_21"]["bus21_vm"]
            < baseline_metrics["bus21_vm"] - 0.008
        )
        assert (
            scenario_metrics["load_shift_39_to_21"]["line_21_22_abs_pij"]
            - baseline_metrics["line_21_22_abs_pij"]
            > 30.0
        )
        assert (
            baseline_metrics["line_22_23_abs_pij"]
            - scenario_metrics["load_shift_39_to_21"]["line_22_23_abs_pij"]
            > 30.0
        )
        assert (
            scenario_metrics["load21_q_up"]["bus21_vm"]
            < baseline_metrics["bus21_vm"] - 0.013
        )
        assert (
            scenario_metrics["load21_q_up"]["slack_q_gen"]
            > baseline_metrics["slack_q_gen"] + 4.0
        )
        assert (
            abs(
                scenario_metrics["load21_q_up"]["line_21_22_abs_pij"]
                - baseline_metrics["line_21_22_abs_pij"]
            )
            < 2.0
        )

    def test_ieee39_line_disable_via_props_enabled_matches_component_removal_for_validated_outage(
        self, integration_model, completed_powerflow_job
    ):
        base_branch_rows = table_rows(completed_powerflow_job.result.getBranches()[0])
        target_branch = branch_row_by_id(base_branch_rows, "canvas_0_126")

        removed_model = Model(deepcopy(integration_model.toJSON()))
        removed_model.removeComponent("canvas_0_126")
        removed_job = removed_model.runPowerFlow()
        wait_for_completion(removed_job)
        removed_bus_rows = table_rows(removed_job.result.getBuses()[0])
        removed_branch_rows = table_rows(removed_job.result.getBranches()[0])

        disabled_model = Model(deepcopy(integration_model.toJSON()))
        target_line = disabled_model.getComponentByKey("canvas_0_126")
        disabled_model.updateComponent(target_line.id, props={"enabled": False})
        disabled_job = disabled_model.runPowerFlow()
        wait_for_completion(disabled_job)
        disabled_bus_rows = table_rows(disabled_job.result.getBuses()[0])
        disabled_branch_rows = table_rows(disabled_job.result.getBranches()[0])

        removed_from_bus = bus_row_by_bus_id(removed_bus_rows, target_branch["From bus"])
        removed_to_bus = bus_row_by_bus_id(removed_bus_rows, target_branch["To bus"])
        disabled_from_bus = bus_row_by_bus_id(disabled_bus_rows, target_branch["From bus"])
        disabled_to_bus = bus_row_by_bus_id(disabled_bus_rows, target_branch["To bus"])
        removed_rerouted_branch = branch_row_by_id(removed_branch_rows, "canvas_0_134")
        disabled_rerouted_branch = branch_row_by_id(disabled_branch_rows, "canvas_0_134")
        removed_relieved_branch = branch_row_by_id(removed_branch_rows, "canvas_0_130")
        disabled_relieved_branch = branch_row_by_id(disabled_branch_rows, "canvas_0_130")

        # 对当前已验证的 IEEE39 断线样本，props.enabled=False 与 removeComponent()
        # 在真实云端上的潮流结果一致，可以把它视为“停运而不物理删除”的可靠表达方式。
        assert not any(row[BRANCH_COLUMN] == "canvas_0_126" for row in removed_branch_rows)
        assert not any(row[BRANCH_COLUMN] == "canvas_0_126" for row in disabled_branch_rows)
        assert disabled_rerouted_branch[P_IJ_COLUMN] == pytest.approx(
            removed_rerouted_branch[P_IJ_COLUMN],
            abs=1e-9,
        )
        assert disabled_relieved_branch[P_IJ_COLUMN] == pytest.approx(
            removed_relieved_branch[P_IJ_COLUMN],
            abs=1e-9,
        )
        assert disabled_from_bus[VM_COLUMN] == pytest.approx(removed_from_bus[VM_COLUMN], abs=1e-12)
        assert disabled_to_bus[VM_COLUMN] == pytest.approx(removed_to_bus[VM_COLUMN], abs=1e-12)
        assert disabled_to_bus[VA_COLUMN] == pytest.approx(removed_to_bus[VA_COLUMN], abs=1e-12)

    def test_ieee39_active_line_candidates_exclude_base_absent_line_component(
        self, integration_model, completed_powerflow_job
    ):
        base_branch_rows = table_rows(completed_powerflow_job.result.getBranches()[0])
        base_branch_ids = {row[BRANCH_COLUMN] for row in base_branch_rows}
        all_line_components = sorted(
            integration_model.getComponentsByRid(TRANSMISSION_LINE_RID).values(),
            key=lambda component: (study_branch_name(component), component.id),
        )
        active_line_components = [
            component for component in all_line_components if component.id in base_branch_ids
        ]
        base_absent_components = [
            component for component in all_line_components if component.id not in base_branch_ids
        ]

        # IEEE39 里有 33 个 TransmissionLine 组件，但 line-6-11 这个组件并不出现在
        # 基线潮流支路结果表中，不能把它当成“已进入 N-1 主线候选集”的有效样本。
        assert len(all_line_components) == 33
        assert len(active_line_components) == 32
        assert [component.id for component in base_absent_components] == [IEEE39_BASE_ABSENT_LINE_ID]
        assert base_absent_components[0].args.get("Name") == "line-6-11"

    def test_ieee39_transformer_disable_via_props_enabled_matches_component_removal_for_validated_outage(
        self, integration_model
    ):
        target_transformer_id = "canvas_0_47"

        removed_model = Model(deepcopy(integration_model.toJSON()))
        removed_model.removeComponent(target_transformer_id)
        removed_bus_rows, removed_branch_rows = run_powerflow_tables(removed_model)

        disabled_model = Model(deepcopy(integration_model.toJSON()))
        target_transformer = disabled_model.getComponentByKey(target_transformer_id)
        disabled_model.updateComponent(target_transformer.id, props={"enabled": False})
        disabled_bus_rows, disabled_branch_rows = run_powerflow_tables(disabled_model)

        removed_bus_by_id = {row[BUS_COLUMN]: row for row in removed_bus_rows}
        disabled_bus_by_id = {row[BUS_COLUMN]: row for row in disabled_bus_rows}
        removed_branch_by_id = {row[BRANCH_COLUMN]: row for row in removed_branch_rows}
        disabled_branch_by_id = {row[BRANCH_COLUMN]: row for row in disabled_branch_rows}

        # 对已验证的 IEEE39 变压器样本，props.enabled=False 与 removeComponent()
        # 也会得到完全一致的潮流结果，可作为“停运而不物理删除”的可靠表达方式。
        assert target_transformer_id not in removed_branch_by_id
        assert target_transformer_id not in disabled_branch_by_id
        assert removed_bus_by_id.keys() == disabled_bus_by_id.keys()
        assert removed_branch_by_id.keys() == disabled_branch_by_id.keys()
        assert max(
            abs(disabled_bus_by_id[bus_id][VM_COLUMN] - removed_bus_by_id[bus_id][VM_COLUMN])
            for bus_id in removed_bus_by_id
        ) == pytest.approx(0.0, abs=1e-12)
        assert max(
            abs(disabled_bus_by_id[bus_id][VA_COLUMN] - removed_bus_by_id[bus_id][VA_COLUMN])
            for bus_id in removed_bus_by_id
        ) == pytest.approx(0.0, abs=1e-12)
        assert max(
            abs(disabled_branch_by_id[branch_id][P_IJ_COLUMN] - removed_branch_by_id[branch_id][P_IJ_COLUMN])
            for branch_id in removed_branch_by_id
        ) == pytest.approx(0.0, abs=1e-9)

    def test_ieee39_subset_n1_screening_can_disable_multiple_lines_and_report_nontrivial_shifts(
        self, integration_model
    ):
        base_bus_rows, base_branch_rows = run_powerflow_tables(Model(deepcopy(integration_model.toJSON())))
        screened_line_ids = ["canvas_0_126", "canvas_0_134", "canvas_0_130"]
        screening_results = []

        for line_id in screened_line_ids:
            working_model = Model(deepcopy(integration_model.toJSON()))
            target_line = working_model.getComponentByKey(line_id)
            working_model.updateComponent(target_line.id, props={"enabled": False})

            outage_job = working_model.runPowerFlow()
            wait_for_completion(outage_job)
            outage_bus_rows = table_rows(outage_job.result.getBuses()[0])
            outage_branch_rows = table_rows(outage_job.result.getBranches()[0])
            metrics = ieee39_n1_metrics(
                base_bus_rows=base_bus_rows,
                base_branch_rows=base_branch_rows,
                outage_bus_rows=outage_bus_rows,
                outage_branch_rows=outage_branch_rows,
            )

            screening_results.append(
                {
                    "line_id": line_id,
                    "line_present_after_outage": any(
                        row[BRANCH_COLUMN] == line_id for row in outage_branch_rows
                    ),
                    **metrics,
                    "severity": classify_ieee39_n1_severity(metrics),
                }
            )

        ranked_results = sorted(
            screening_results,
            key=lambda item: (
                item["new_low_voltage_bus_count"] + item["new_high_voltage_bus_count"],
                max(0.0, 0.95 - item["min_vm"]),
                item["max_vm_shift"],
                item["max_branch_shift"],
            ),
            reverse=True,
        )

        # 这条受限 N-1 筛查只验证一个当前可信子集：
        # 三条 IEEE39 线路都能通过 props.enabled=False 形成停运工况，并报告非平凡的系统响应。
        # 同时，严重性排序应把新增越限更多、最差电压更低、潮流改道更剧烈的工况排在前面。
        assert [result["line_id"] for result in screening_results] == screened_line_ids
        assert all(result["line_present_after_outage"] is False for result in screening_results)
        assert all(result["max_vm_shift"] > 0.005 for result in screening_results)
        assert all(result["max_branch_shift"] > 10.0 for result in screening_results)
        assert [result["line_id"] for result in ranked_results] == [
            "canvas_0_130",
            "canvas_0_134",
            "canvas_0_126",
        ]
        assert [result["severity"] for result in ranked_results] == [
            "critical",
            "critical",
            "warning",
        ]

    def test_ieee39_full_active_branch_n1_screening_covers_lines_and_transformers_and_stable_top_rankings(
        self, ieee39_full_active_branch_n1_results
    ):
        ranked_results = ieee39_full_active_branch_n1_results

        # 这条测试把 IEEE39 基线潮流里真正在线的全部支路都扫一遍，确认当前仓库已经具备
        # “全网支路 N-1 潮流筛查”的真实主线证据，而不只是若干示范线路。
        assert len(ranked_results) == 43
        assert sum(1 for result in ranked_results if result["branch_kind"] == "line") == 32
        assert sum(1 for result in ranked_results if result["branch_kind"] == "transformer") == 11
        assert all(result["branch_present_after_outage"] is False for result in ranked_results)
        assert ranked_results[0]["branch_id"] == "canvas_0_258"
        assert ranked_results[1]["branch_id"] == "canvas_0_175"
        assert ranked_results[2]["branch_id"] == "canvas_0_208"
        assert ranked_results[0]["branch_kind"] == "transformer"
        assert sum(1 for result in ranked_results if result["severity"] == "critical") >= 20
        assert ranked_results[-1]["severity"] == "observe"

    def test_ieee39_full_active_branch_n1_screening_digest_identifies_top_line_transformer_and_islanding_cases(
        self, ieee39_full_active_branch_n1_results
    ):
        ranked_results = ieee39_full_active_branch_n1_results
        top_line = next(result for result in ranked_results if result["branch_kind"] == "line")
        top_transformer = next(
            result for result in ranked_results if result["branch_kind"] == "transformer"
        )
        lowest_voltage_case = min(ranked_results, key=lambda item: item["min_vm"])
        largest_missing_bus_case = max(
            ranked_results,
            key=lambda item: (
                item["missing_bus_count"],
                item["new_low_voltage_bus_count"] + item["new_high_voltage_bus_count"],
                item["max_vm_shift"],
                item["max_branch_shift"],
            ),
        )
        largest_branch_shift_case = max(ranked_results, key=lambda item: item["max_branch_shift"])

        assert top_transformer["branch_id"] == "canvas_0_258"
        assert top_transformer["severity"] == "critical"
        assert top_line["branch_id"] == "canvas_0_175"
        assert top_line["severity"] == "critical"
        assert lowest_voltage_case["branch_id"] == "canvas_0_208"
        assert lowest_voltage_case["min_vm"] < 0.87
        assert lowest_voltage_case["min_vm_bus_id"] == "canvas_0_207"
        assert largest_missing_bus_case["branch_id"] == "canvas_0_225"
        assert largest_missing_bus_case["missing_bus_count"] == 2
        assert largest_missing_bus_case["missing_bus_ids"] == ["canvas_0_216", "canvas_0_44"]
        assert largest_branch_shift_case["branch_id"] == "canvas_0_234"
        assert largest_branch_shift_case["max_branch_shift"] > 649.0
        assert largest_branch_shift_case["max_branch_shift_branch_id"] == "canvas_0_237"

    def test_ieee39_line_maintenance_state_can_be_rechecked_with_residual_n1_subset(
        self, integration_model
    ):
        base_model = Model(deepcopy(integration_model.toJSON()))
        base_bus_rows, base_branch_rows = run_powerflow_tables(base_model)

        maintenance_branch_id = "canvas_0_126"
        maintenance_model = Model(deepcopy(integration_model.toJSON()))
        maintenance_branch = maintenance_model.getComponentByKey(maintenance_branch_id)
        maintenance_model.updateComponent(maintenance_branch.id, props={"enabled": False})
        maintenance_bus_rows, maintenance_branch_rows = run_powerflow_tables(maintenance_model)
        maintenance_metrics = ieee39_n1_metrics(
            base_bus_rows=base_bus_rows,
            base_branch_rows=base_branch_rows,
            outage_bus_rows=maintenance_bus_rows,
            outage_branch_rows=maintenance_branch_rows,
        )

        residual_branch_ids = ["canvas_0_134", "canvas_0_130", "canvas_0_47"]
        residual_results = []
        for branch_id in residual_branch_ids:
            residual_model = Model(deepcopy(maintenance_model.toJSON()))
            residual_branch = residual_model.getComponentByKey(branch_id)
            residual_model.updateComponent(residual_branch.id, props={"enabled": False})
            residual_bus_rows, residual_branch_rows = run_powerflow_tables(residual_model)
            metrics = ieee39_n1_metrics(
                base_bus_rows=maintenance_bus_rows,
                base_branch_rows=maintenance_branch_rows,
                outage_bus_rows=residual_bus_rows,
                outage_branch_rows=residual_branch_rows,
            )
            residual_results.append(
                {
                    "branch_id": branch_id,
                    "branch_present_after_outage": any(
                        row[BRANCH_COLUMN] == branch_id for row in residual_branch_rows
                    ),
                    **metrics,
                    "severity": classify_ieee39_n1_severity(metrics),
                }
            )

        ranked_results = sorted(
            residual_results,
            key=lambda item: (
                ieee39_n1_severity_rank(item),
                item["new_low_voltage_bus_count"] + item["new_high_voltage_bus_count"],
                max(0.0, 0.95 - item["min_vm"]),
                item["max_vm_shift"],
                item["max_branch_shift"],
            ),
            reverse=True,
        )

        # 这条受限校核验证“计划检修 + 残余 N-1 复核”在 IEEE39 上是可跑通的：
        # 先停运 line-26-28，再对剩余已验证子集继续停运，仍能得到稳定的潮流结果和非平凡排序。
        assert not any(row[BRANCH_COLUMN] == maintenance_branch_id for row in maintenance_branch_rows)
        assert maintenance_metrics["missing_bus_count"] == 0
        assert maintenance_metrics["max_vm_shift"] > 0.005
        assert maintenance_metrics["max_branch_shift"] > 100.0
        assert [result["branch_id"] for result in residual_results] == residual_branch_ids
        assert all(result["branch_present_after_outage"] is False for result in residual_results)
        assert all(result["max_vm_shift"] > 0.003 for result in residual_results)
        assert all(result["max_branch_shift"] > 10.0 for result in residual_results)
        assert any(
            result["new_low_voltage_bus_count"] > 0 or result["min_vm"] < maintenance_metrics["min_vm"] - 1e-4
            for result in residual_results
        )
        assert ranked_results[0]["severity"] in {"critical", "warning"}

    def test_ieee39_transformer_maintenance_state_can_be_rechecked_with_residual_n1_subset(
        self, integration_model
    ):
        base_model = Model(deepcopy(integration_model.toJSON()))
        base_bus_rows, base_branch_rows = run_powerflow_tables(base_model)

        maintenance_branch_id = "canvas_0_47"
        maintenance_model = Model(deepcopy(integration_model.toJSON()))
        maintenance_branch = maintenance_model.getComponentByKey(maintenance_branch_id)
        maintenance_model.updateComponent(maintenance_branch.id, props={"enabled": False})
        maintenance_bus_rows, maintenance_branch_rows = run_powerflow_tables(maintenance_model)
        maintenance_metrics = ieee39_n1_metrics(
            base_bus_rows=base_bus_rows,
            base_branch_rows=base_branch_rows,
            outage_bus_rows=maintenance_bus_rows,
            outage_branch_rows=maintenance_branch_rows,
        )

        residual_branch_ids = ["canvas_0_126", "canvas_0_134", "canvas_0_130"]
        residual_results = []
        for branch_id in residual_branch_ids:
            residual_model = Model(deepcopy(maintenance_model.toJSON()))
            residual_branch = residual_model.getComponentByKey(branch_id)
            residual_model.updateComponent(residual_branch.id, props={"enabled": False})
            residual_bus_rows, residual_branch_rows = run_powerflow_tables(residual_model)
            metrics = ieee39_n1_metrics(
                base_bus_rows=maintenance_bus_rows,
                base_branch_rows=maintenance_branch_rows,
                outage_bus_rows=residual_bus_rows,
                outage_branch_rows=residual_branch_rows,
            )
            residual_results.append(
                {
                    "branch_id": branch_id,
                    "branch_present_after_outage": any(
                        row[BRANCH_COLUMN] == branch_id for row in residual_branch_rows
                    ),
                    **metrics,
                    "severity": classify_ieee39_n1_severity(metrics),
                }
            )

        ranked_results = sorted(
            residual_results,
            key=lambda item: (
                ieee39_n1_severity_rank(item),
                item["new_low_voltage_bus_count"] + item["new_high_voltage_bus_count"],
                max(0.0, 0.95 - item["min_vm"]),
                item["max_vm_shift"],
                item["max_branch_shift"],
            ),
            reverse=True,
        )

        # 这条受限校核补上了已验证的变压器检修样本：
        # 先停运 canvas_0_47，再对剩余已验证线路子集继续停运，仍能形成稳定的残余 N-1 排序。
        assert not any(row[BRANCH_COLUMN] == maintenance_branch_id for row in maintenance_branch_rows)
        assert maintenance_metrics["missing_bus_count"] == 0
        assert maintenance_metrics["max_vm_shift"] > 0.003
        assert maintenance_metrics["max_branch_shift"] > 10.0
        assert [result["branch_id"] for result in residual_results] == residual_branch_ids
        assert all(result["branch_present_after_outage"] is False for result in residual_results)
        assert all(result["max_vm_shift"] > 0.003 for result in residual_results)
        assert all(result["max_branch_shift"] > 10.0 for result in residual_results)
        assert any(
            result["new_low_voltage_bus_count"] > 0
            or result["min_vm"] < maintenance_metrics["min_vm"] - 1e-4
            or result["max_branch_shift"] > maintenance_metrics["max_branch_shift"] + 1.0
            for result in residual_results
        )
        assert ranked_results[0]["severity"] in {"critical", "warning"}
