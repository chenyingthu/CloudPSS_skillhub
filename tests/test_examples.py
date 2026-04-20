import importlib.util
from pathlib import Path

import pytest

from cloudpss import Model


REPO_ROOT = Path(__file__).resolve().parents[1]
RUN_EMT_SIMULATION_PATH = REPO_ROOT / "examples" / "simulation" / "run_emt_simulation.py"
RUN_POWERFLOW_PATH = REPO_ROOT / "examples" / "simulation" / "run_powerflow.py"
MODEL_SAVE_DUMP_PATH = REPO_ROOT / "examples" / "basic" / "model_save_dump_example.py"
COMPONENT_EXAMPLE_PATH = REPO_ROOT / "examples" / "basic" / "component_example.py"
MODEL_FETCH_EXAMPLE_PATH = REPO_ROOT / "examples" / "basic" / "model_fetch_example.py"
REVISION_EXAMPLE_PATH = REPO_ROOT / "examples" / "basic" / "revision_example.py"
EMT_VOLTAGE_METER_CHAIN_PATH = (
    REPO_ROOT / "examples" / "basic" / "emt_voltage_meter_chain_example.py"
)
POWERFLOW_ENGINEERING_STUDY_PATH = (
    REPO_ROOT / "examples" / "analysis" / "powerflow_engineering_study_example.py"
)
POWERFLOW_BATCH_STUDY_PATH = (
    REPO_ROOT / "examples" / "analysis" / "powerflow_batch_study_example.py"
)
POWERFLOW_N1_SCREENING_PATH = (
    REPO_ROOT / "examples" / "analysis" / "powerflow_n1_screening_example.py"
)
POWERFLOW_MAINTENANCE_SECURITY_PATH = (
    REPO_ROOT / "examples" / "analysis" / "powerflow_maintenance_security_example.py"
)
EMT_FAULT_STUDY_PATH = (
    REPO_ROOT / "examples" / "analysis" / "emt_fault_study_example.py"
)
EMT_FAULT_SEVERITY_SCAN_PATH = (
    REPO_ROOT / "examples" / "analysis" / "emt_fault_severity_scan_example.py"
)
EMT_FAULT_CLEARING_SCAN_PATH = (
    REPO_ROOT / "examples" / "analysis" / "emt_fault_clearing_scan_example.py"
)
EMT_MEASUREMENT_WORKFLOW_PATH = (
    REPO_ROOT / "examples" / "analysis" / "emt_measurement_workflow_example.py"
)
EMT_N1_SECURITY_SCREENING_PATH = (
    REPO_ROOT / "examples" / "analysis" / "emt_n1_security_screening_example.py"
)
EMT_N1_SECURITY_REPORT_PATH = (
    REPO_ROOT / "examples" / "analysis" / "emt_n1_security_report_example.py"
)
EMT_N1_FULL_REPORT_PATH = (
    REPO_ROOT / "examples" / "analysis" / "emt_n1_full_report_example.py"
)
EMT_RESEARCH_REPORT_PATH = (
    REPO_ROOT / "examples" / "analysis" / "emt_research_report_example.py"
)
RUN_SFEMT_PATH = REPO_ROOT / "examples" / "simulation" / "run_sfemt_simulation.py"
RUN_IES_PATH = REPO_ROOT / "examples" / "simulation" / "run_ies_simulation.py"


def load_module(module_path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def build_local_model():
    return Model(
        {
            "name": "local-example-model",
            "rid": "model/test/local-example-model",
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


def build_local_emt_bus_model(with_template_edge=True):
    cells = {
        "bus_a": {
            "id": "bus_a",
            "shape": "diagram-component",
            "definition": "model/CloudPSS/_newBus_3p",
            "label": "bus-a",
            "args": {
                "Name": "BusA",
                "Freq": {"source": "50", "ɵexp": ""},
                "V": 1.0,
                "VBase": {"source": "230", "ɵexp": ""},
            },
            "pins": {"0": "BusA"},
            "canvas": "canvas_0",
            "position": {"x": 100, "y": 200},
            "size": {"width": 100, "height": 40},
            "props": {"enabled": True},
            "context": {},
            "style": {"--stroke-width": 2},
            "zIndex": -10,
        },
        "channel_template": {
            "id": "channel_template",
            "shape": "diagram-component",
            "definition": "model/CloudPSS/_newChannel",
            "label": "channel-template",
            "args": {
                "Name": "existing",
                "Dim": {"source": "3", "ɵexp": ""},
                "Freq": {"source": "1000", "ɵexp": ""},
            },
            "pins": {"0": "#existing"},
            "canvas": "canvas_0",
            "position": {"x": 260, "y": 60},
            "size": {"width": 110, "height": 20},
            "props": {"enabled": True},
            "context": {},
            "style": {"--stroke-width": 2},
            "zIndex": -11,
        },
    }

    if with_template_edge:
        cells["meter_template"] = {
            "id": "meter_template",
            "shape": "diagram-component",
            "definition": "model/CloudPSS/_NewVoltageMeter",
            "label": "meter-template",
            "args": {"Dim": "3", "V": "#existing_v"},
            "pins": {"0": ""},
            "canvas": "canvas_0",
            "position": {"x": 80, "y": 80},
            "size": {"width": 30, "height": 50},
            "props": {"enabled": True},
            "context": {},
            "style": {"--stroke-width": 2},
            "zIndex": -12,
        }
        cells["edge_template"] = {
            "id": "edge_template",
            "shape": "diagram-edge",
            "canvas": "canvas_0",
            "attrs": {
                "line": {
                    "sourceMarker": {"args": {"cx": 0, "r": 0.5}, "name": "circle"},
                    "stroke": "var(--stroke)",
                    "strokeWidth": "var(--stroke-width)",
                    "targetMarker": {"args": {"cx": 0, "r": 0.5}, "name": "circle"},
                },
                "lines": {"connection": True, "strokeLinejoin": "round"},
                "root": {"style": {"--stroke-width": 2}},
            },
            "source": {"cell": "meter_template", "port": "0"},
            "target": {
                "anchor": {"args": {"dx": "-20%", "dy": "0%", "rotate": True}, "name": "center"},
                "cell": "bus_a",
                "port": "0",
                "selector": "> path:nth-child(2)",
            },
            "vertices": [{"x": 90, "y": 150}],
            "zIndex": -13,
        }

    return Model(
        {
            "name": "local-emt-bus-model",
            "rid": "model/test/local-emt-bus-model",
            "jobs": [
                {
                    "rid": "function/CloudPSS/emtps",
                    "name": "emt",
                    "args": {"output_channels": []},
                }
            ],
            "configs": [{"name": "config-1", "args": {}, "pins": {}}],
            "context": {"currentJob": 0, "currentConfig": 0},
            "revision": {
                "hash": "local-emt-hash",
                "version": 4,
                "implements": {
                    "diagram": {
                        "canvas": [{"key": "canvas_0"}],
                        "cells": cells,
                    }
                },
                "parameters": [],
                "pins": {},
                "documentation": {},
            },
        }
    )


def build_local_n1_model():
    cells = {
        "line_b": {
            "id": "line_b",
            "shape": "diagram-component",
            "definition": "model/CloudPSS/TransmissionLine",
            "label": "line-b",
            "args": {"Name": "line-26-29"},
            "pins": {"0": "", "1": ""},
            "canvas": "canvas_0",
            "position": {"x": 100, "y": 100},
            "size": {"width": 120, "height": 20},
            "props": {"enabled": True},
            "context": {},
            "style": {"--stroke-width": 2},
            "zIndex": -10,
        },
        "line_a": {
            "id": "line_a",
            "shape": "diagram-component",
            "definition": "model/CloudPSS/TransmissionLine",
            "label": "line-a",
            "args": {"Name": "line-26-28"},
            "pins": {"0": "", "1": ""},
            "canvas": "canvas_0",
            "position": {"x": 120, "y": 130},
            "size": {"width": 120, "height": 20},
            "props": {"enabled": True},
            "context": {},
            "style": {"--stroke-width": 2},
            "zIndex": -11,
        },
        "line_c": {
            "id": "line_c",
            "shape": "diagram-component",
            "definition": "model/CloudPSS/TransmissionLine",
            "label": "line-c",
            "args": {"Name": "line-28-29"},
            "pins": {"0": "", "1": ""},
            "canvas": "canvas_0",
            "position": {"x": 140, "y": 160},
            "size": {"width": 120, "height": 20},
            "props": {"enabled": False},
            "context": {},
            "style": {"--stroke-width": 2},
            "zIndex": -12,
        },
        "transformer_a": {
            "id": "transformer_a",
            "shape": "diagram-component",
            "definition": "model/CloudPSS/_newTransformer_3p2w",
            "label": "newTransformer_3p2w-1",
            "args": {"Name": ""},
            "pins": {"0": "", "1": ""},
            "canvas": "canvas_0",
            "position": {"x": 160, "y": 190},
            "size": {"width": 120, "height": 20},
            "props": {"enabled": True},
            "context": {},
            "style": {"--stroke-width": 2},
            "zIndex": -13,
        },
        "load_x": {
            "id": "load_x",
            "shape": "diagram-component",
            "definition": "model/CloudPSS/_newExpLoad_3p",
            "label": "load-x",
            "args": {"Name": "load-x"},
            "pins": {"0": ""},
            "canvas": "canvas_0",
            "position": {"x": 180, "y": 200},
            "size": {"width": 120, "height": 20},
            "props": {"enabled": True},
            "context": {},
            "style": {"--stroke-width": 2},
            "zIndex": -14,
        },
    }

    return Model(
        {
            "name": "local-n1-model",
            "rid": "model/test/local-n1-model",
            "jobs": [],
            "configs": [],
            "context": {"currentJob": 0, "currentConfig": 0},
            "revision": {
                "hash": "local-n1-hash",
                "version": 4,
                "implements": {
                    "diagram": {
                        "canvas": [{"key": "canvas_0"}],
                        "cells": cells,
                    }
                },
                "parameters": [],
                "pins": {},
                "documentation": {},
            },
        }
    )


class TestRunEMTSimulationExample:
    def test_load_model_from_source_reads_local_yaml(self, tmp_path):
        module = load_module(RUN_EMT_SIMULATION_PATH, "run_emt_simulation_example")
        export_path = tmp_path / "local-model.yaml"

        Model.dump(build_local_model(), str(export_path), compress=None)
        loaded_model = module.load_model_from_source(str(export_path))

        assert loaded_model.name == "local-example-model"
        assert loaded_model.rid == "model/test/local-example-model"

    def test_describe_job_falls_back_to_context_when_name_missing(self):
        module = load_module(RUN_EMT_SIMULATION_PATH, "run_emt_simulation_example_job")

        job_like = type(
            "JobLike",
            (),
            {
                "id": "job-1",
                "rid": "model/holdme/IEEE3",
                "context": ["function/CloudPSS/emtps"],
            },
        )()

        description = module.describe_job(job_like)

        assert description["id"] == "job-1"
        assert description["label"] == "function/CloudPSS/emtps"
        assert description["context"] == ["function/CloudPSS/emtps"]

    def test_describe_plot_prefers_key_over_optional_name(self):
        module = load_module(RUN_EMT_SIMULATION_PATH, "run_emt_simulation_example_plot")

        label = module.describe_plot({"key": "plot-0", "name": "Legacy"}, 0)

        assert label == "plot-0"


class TestRunPowerFlowExample:
    def test_load_model_from_source_reads_local_yaml(self, tmp_path):
        module = load_module(RUN_POWERFLOW_PATH, "run_powerflow_example")
        export_path = tmp_path / "local-powerflow-model.yaml"

        Model.dump(build_local_model(), str(export_path), compress=None)
        loaded_model = module.load_model_from_source(str(export_path))

        assert loaded_model.name == "local-example-model"
        assert loaded_model.rid == "model/test/local-example-model"

    def test_describe_table_column_prefers_name_then_title(self):
        module = load_module(RUN_POWERFLOW_PATH, "run_powerflow_column_example")

        assert module.describe_table_column({"name": "Bus"}) == "Bus"
        assert module.describe_table_column({"title": "Legacy"}) == "Legacy"
        assert module.describe_table_column({}) == "Unknown"


class TestModelSaveDumpExample:
    def test_load_model_from_source_reads_local_yaml(self, tmp_path):
        module = load_module(MODEL_SAVE_DUMP_PATH, "model_save_dump_example")
        export_path = tmp_path / "local-study-model.yaml"

        Model.dump(build_local_model(), str(export_path), compress=None)
        loaded_model = module.load_model_from_source(str(export_path))

        assert loaded_model.name == "local-example-model"
        assert loaded_model.rid == "model/test/local-example-model"

    def test_create_local_branch_returns_model_and_export_path(self, tmp_path):
        module = load_module(MODEL_SAVE_DUMP_PATH, "model_save_dump_example_branch")
        export_path = tmp_path / "working-copy.yaml"

        working_model, returned_path = module.create_local_branch(
            build_local_model(),
            str(export_path),
        )

        assert returned_path == str(export_path)
        assert working_model.name == "local-example-model"
        assert export_path.exists()

    def test_suggest_working_copy_path_avoids_overwriting_local_source(self, tmp_path):
        module = load_module(MODEL_SAVE_DUMP_PATH, "model_save_dump_example_path")
        source_path = tmp_path / "study-working-copy.yaml"

        Model.dump(build_local_model(), str(source_path), compress=None)
        suggested = module.suggest_working_copy_path(str(source_path))

        assert suggested.endswith("study-working-copy-branch.yaml")
        assert suggested != str(source_path)

    def test_annotate_local_branch_handles_missing_description(self, monkeypatch):
        module = load_module(MODEL_SAVE_DUMP_PATH, "model_save_dump_example_annotate")
        model = build_local_model()

        monkeypatch.setattr("builtins.input", lambda _prompt: "")
        updated_model = module.annotate_local_branch(model)

        assert updated_model.description == (
            "[study-note] offline study branch for topology and parameter iteration"
        )


class TestComponentExample:
    def test_load_model_from_source_reads_local_yaml(self, tmp_path):
        module = load_module(COMPONENT_EXAMPLE_PATH, "component_example")
        export_path = tmp_path / "local-component-model.yaml"

        Model.dump(build_local_model(), str(export_path), compress=None)
        loaded_model = module.load_model_from_source(str(export_path))

        assert loaded_model.name == "local-example-model"
        assert loaded_model.rid == "model/test/local-example-model"

    def test_suggest_working_copy_path_avoids_overwriting_local_source(self, tmp_path):
        module = load_module(COMPONENT_EXAMPLE_PATH, "component_example_path")
        source_path = tmp_path / "component-working-copy.yaml"

        Model.dump(build_local_model(), str(source_path), compress=None)
        suggested = module.suggest_working_copy_path(str(source_path))

        assert suggested.endswith("component-working-copy-branch.yaml")
        assert suggested != str(source_path)

    def test_suggest_modified_copy_path_appends_modified_suffix(self):
        module = load_module(COMPONENT_EXAMPLE_PATH, "component_example_modified")

        suggested = module.suggest_modified_copy_path(
            "examples/basic/component_working_copy.yaml"
        )

        assert suggested == "examples/basic/component_working_copy-modified.yaml"


class TestModelFetchExample:
    def test_load_model_from_source_reads_local_yaml(self, tmp_path):
        module = load_module(MODEL_FETCH_EXAMPLE_PATH, "model_fetch_example")
        export_path = tmp_path / "local-fetch-model.yaml"

        Model.dump(build_local_model(), str(export_path), compress=None)
        loaded_model = module.load_model_from_source(str(export_path))

        assert loaded_model.name == "local-example-model"
        assert loaded_model.rid == "model/test/local-example-model"

    def test_suggest_working_copy_path_avoids_overwriting_local_source(self, tmp_path):
        module = load_module(MODEL_FETCH_EXAMPLE_PATH, "model_fetch_example_path")
        source_path = tmp_path / "model_fetch_working_copy.yaml"

        Model.dump(build_local_model(), str(source_path), compress=None)
        suggested = module.suggest_working_copy_path(str(source_path))

        assert suggested.endswith("model_fetch_working_copy-branch.yaml")
        assert suggested != str(source_path)


class TestRevisionExample:
    def test_load_model_from_source_reads_local_yaml(self, tmp_path):
        module = load_module(REVISION_EXAMPLE_PATH, "revision_example")
        export_path = tmp_path / "local-revision-model.yaml"

        Model.dump(build_local_model(), str(export_path), compress=None)
        loaded_model = module.load_model_from_source(str(export_path))

        assert loaded_model.name == "local-example-model"
        assert loaded_model.rid == "model/test/local-example-model"


class TestEMTVoltageMeterChainExample:
    def test_load_model_from_source_reads_local_yaml(self, tmp_path):
        module = load_module(EMT_VOLTAGE_METER_CHAIN_PATH, "emt_voltage_meter_chain_example")
        export_path = tmp_path / "local-emt-bus-model.yaml"

        Model.dump(build_local_emt_bus_model(), str(export_path), compress=None)
        loaded_model = module.load_model_from_source(str(export_path))

        assert loaded_model.name == "local-emt-bus-model"
        assert loaded_model.rid == "model/test/local-emt-bus-model"

    def test_suggest_working_copy_path_avoids_overwriting_local_source(self, tmp_path):
        module = load_module(
            EMT_VOLTAGE_METER_CHAIN_PATH,
            "emt_voltage_meter_chain_example_path",
        )
        source_path = tmp_path / "emt-voltage-meter-working-copy.yaml"

        Model.dump(build_local_emt_bus_model(), str(source_path), compress=None)
        suggested = module.suggest_working_copy_path(str(source_path))

        assert suggested.endswith("emt-voltage-meter-working-copy-branch.yaml")
        assert suggested != str(source_path)

    def test_add_voltage_meter_chain_reuses_existing_template_edge(self):
        module = load_module(
            EMT_VOLTAGE_METER_CHAIN_PATH,
            "emt_voltage_meter_chain_example_template",
        )
        model = build_local_emt_bus_model(with_template_edge=True)

        result = module.add_voltage_meter_chain(
            model,
            bus_name="BusA",
            signal_name="#busa_added",
            channel_name="busa_added",
            sampling_freq=2000,
        )

        edge = model.getAllComponents()[result["edge_id"]]
        output_group = model.jobs[0]["args"]["output_channels"][result["output_group_index"]]

        assert result["used_edge_template"] is True
        assert result["channel"].pins["0"] == "#busa_added"
        assert edge.shape == "diagram-edge"
        assert edge.source["cell"] == result["meter"].id
        assert edge.target["cell"] == "bus_a"
        assert output_group["4"] == [result["channel"].id]

    def test_add_voltage_meter_chain_falls_back_to_generic_edge(self):
        module = load_module(
            EMT_VOLTAGE_METER_CHAIN_PATH,
            "emt_voltage_meter_chain_example_generic",
        )
        model = build_local_emt_bus_model(with_template_edge=False)

        result = module.add_voltage_meter_chain(
            model,
            bus_name="BusA",
            signal_name="#busa_added",
            channel_name="busa_added",
            sampling_freq=2000,
        )

        edge = model.getAllComponents()[result["edge_id"]]

        assert result["used_edge_template"] is False
        assert edge.shape == "diagram-edge"
        assert edge.source["cell"] == result["meter"].id
        assert edge.target["cell"] == "bus_a"


class TestPowerFlowEngineeringStudyExample:
    def test_load_model_from_source_reads_local_yaml(self, tmp_path):
        module = load_module(
            POWERFLOW_ENGINEERING_STUDY_PATH,
            "powerflow_engineering_study_example",
        )
        export_path = tmp_path / "local-engineering-model.yaml"

        Model.dump(build_local_model(), str(export_path), compress=None)
        loaded_model = module.load_model_from_source(str(export_path))

        assert loaded_model.name == "local-example-model"
        assert loaded_model.rid == "model/test/local-example-model"

    def test_compute_line_outage_summary_tracks_target_and_neighbor_branches(self):
        module = load_module(
            POWERFLOW_ENGINEERING_STUDY_PATH,
            "powerflow_engineering_study_example_line",
        )
        base_buses = [
            {
                module.BUS_COLUMN: "canvas_0_29",
                module.VM_COLUMN: 1.01,
                module.VA_COLUMN: -1.05,
            },
            {
                module.BUS_COLUMN: "canvas_0_31",
                module.VM_COLUMN: 1.02,
                module.VA_COLUMN: 2.74,
            },
        ]
        outage_buses = [
            {
                module.BUS_COLUMN: "canvas_0_29",
                module.VM_COLUMN: 0.99,
                module.VA_COLUMN: -0.99,
            },
            {
                module.BUS_COLUMN: "canvas_0_31",
                module.VM_COLUMN: 1.01,
                module.VA_COLUMN: 9.31,
            },
        ]
        base_branches = [
            {
                module.BRANCH_COLUMN: "canvas_0_126",
                "From bus": "canvas_0_29",
                "To bus": "canvas_0_31",
                module.P_IJ_COLUMN: -143.5,
                module.P_JI_COLUMN: 144.4,
            },
            {
                module.BRANCH_COLUMN: "canvas_0_123",
                "From bus": "canvas_0_29",
                "To bus": "canvas_0_30",
                module.P_IJ_COLUMN: 141.3,
                module.P_JI_COLUMN: -140.9,
            },
            {
                module.BRANCH_COLUMN: "canvas_0_130",
                "From bus": "canvas_0_31",
                "To bus": "canvas_0_32",
                module.P_IJ_COLUMN: -350.4,
                module.P_JI_COLUMN: 352.0,
            },
            {
                module.BRANCH_COLUMN: "canvas_0_134",
                "From bus": "canvas_0_29",
                "To bus": "canvas_0_32",
                module.P_IJ_COLUMN: -192.4,
                module.P_JI_COLUMN: 194.5,
            },
        ]
        outage_branches = [
            {
                module.BRANCH_COLUMN: "canvas_0_123",
                "From bus": "canvas_0_29",
                "To bus": "canvas_0_30",
                module.P_IJ_COLUMN: 142.0,
                module.P_JI_COLUMN: -141.7,
            },
            {
                module.BRANCH_COLUMN: "canvas_0_130",
                "From bus": "canvas_0_31",
                "To bus": "canvas_0_32",
                module.P_IJ_COLUMN: -206.0,
                module.P_JI_COLUMN: 206.6,
            },
            {
                module.BRANCH_COLUMN: "canvas_0_134",
                "From bus": "canvas_0_29",
                "To bus": "canvas_0_32",
                module.P_IJ_COLUMN: -333.4,
                module.P_JI_COLUMN: 339.9,
            },
        ]

        summary = module.compute_line_outage_summary(
            base_buses=base_buses,
            base_branches=base_branches,
            outage_buses=outage_buses,
            outage_branches=outage_branches,
        )

        assert summary["target_branch"]["name"] == "line-26-28"
        assert summary["from_bus_shift"]["outage_vm"] == 0.99
        assert summary["to_bus_shift"]["outage_va"] == 9.31
        assert summary["monitored_branches"]["canvas_0_134"]["outage_p_ij"] == -333.4

    def test_compute_voltage_control_summary_tracks_generator_bus_and_ranked_changes(self):
        module = load_module(
            POWERFLOW_ENGINEERING_STUDY_PATH,
            "powerflow_engineering_study_example_voltage",
        )
        base_buses = [
            {
                module.BUS_COLUMN: "canvas_0_28",
                module.NODE_COLUMN: "canvas_2_303",
                module.VM_COLUMN: 1.047,
                module.P_GEN_COLUMN: 250.0,
                module.Q_GEN_COLUMN: 157.7,
            },
            {
                module.BUS_COLUMN: "canvas_0_27",
                module.NODE_COLUMN: "",
                module.VM_COLUMN: 1.0207,
                module.P_GEN_COLUMN: 0.0,
                module.Q_GEN_COLUMN: 0.0,
            },
        ]
        adjusted_buses = [
            {
                module.BUS_COLUMN: "canvas_0_28",
                module.NODE_COLUMN: "canvas_2_303",
                module.VM_COLUMN: 1.070,
                module.P_GEN_COLUMN: 250.0,
                module.Q_GEN_COLUMN: 226.2,
            },
            {
                module.BUS_COLUMN: "canvas_0_27",
                module.NODE_COLUMN: "",
                module.VM_COLUMN: 1.0326,
                module.P_GEN_COLUMN: 0.0,
                module.Q_GEN_COLUMN: 0.0,
            },
        ]

        summary = module.compute_voltage_control_summary(
            base_buses=base_buses,
            adjusted_buses=adjusted_buses,
        )

        assert summary["generator"] == "Gen30"
        assert summary["target_bus"]["adjusted_vm"] == 1.070
        assert summary["target_bus"]["adjusted_q_gen"] == 226.2
        assert summary["largest_voltage_changes"][0]["bus_id"] == "canvas_0_28"

    def test_compute_active_redispatch_summary_tracks_generator_slack_and_corridor_shifts(self):
        module = load_module(
            POWERFLOW_ENGINEERING_STUDY_PATH,
            "powerflow_engineering_study_example_redispatch",
        )
        base_buses = [
            {
                module.BUS_COLUMN: "canvas_0_33",
                module.NODE_COLUMN: "canvas_9_384",
                module.VM_COLUMN: 1.026,
                module.P_GEN_COLUMN: 830.0,
                module.Q_GEN_COLUMN: 75.7,
            },
            {
                module.BUS_COLUMN: "canvas_0_35",
                module.NODE_COLUMN: "canvas_10_399",
                module.VM_COLUMN: 1.03,
                module.P_GEN_COLUMN: 1315.472,
                module.Q_GEN_COLUMN: 238.070,
            },
        ]
        adjusted_buses = [
            {
                module.BUS_COLUMN: "canvas_0_33",
                module.NODE_COLUMN: "canvas_9_384",
                module.VM_COLUMN: 1.026,
                module.P_GEN_COLUMN: 900.0,
                module.Q_GEN_COLUMN: 97.7,
            },
            {
                module.BUS_COLUMN: "canvas_0_35",
                module.NODE_COLUMN: "canvas_10_399",
                module.VM_COLUMN: 1.03,
                module.P_GEN_COLUMN: 1246.662,
                module.Q_GEN_COLUMN: 242.203,
            },
        ]
        base_branches = [
            {
                module.BRANCH_COLUMN: "canvas_0_258",
                "From bus": "canvas_0_32",
                "To bus": "canvas_0_33",
                module.P_IJ_COLUMN: -830.0,
            },
            {
                module.BRANCH_COLUMN: "canvas_0_126",
                "From bus": "canvas_0_29",
                "To bus": "canvas_0_31",
                module.P_IJ_COLUMN: -143.505,
            },
            {
                module.BRANCH_COLUMN: "canvas_0_134",
                "From bus": "canvas_0_29",
                "To bus": "canvas_0_32",
                module.P_IJ_COLUMN: -192.398,
            },
            {
                module.BRANCH_COLUMN: "canvas_0_130",
                "From bus": "canvas_0_31",
                "To bus": "canvas_0_32",
                module.P_IJ_COLUMN: -350.371,
            },
            {
                module.BRANCH_COLUMN: "canvas_0_123",
                "From bus": "canvas_0_29",
                "To bus": "canvas_0_30",
                module.P_IJ_COLUMN: 141.279,
            },
        ]
        adjusted_branches = [
            {
                module.BRANCH_COLUMN: "canvas_0_258",
                "From bus": "canvas_0_32",
                "To bus": "canvas_0_33",
                module.P_IJ_COLUMN: -900.0,
            },
            {
                module.BRANCH_COLUMN: "canvas_0_126",
                "From bus": "canvas_0_29",
                "To bus": "canvas_0_31",
                module.P_IJ_COLUMN: -177.745,
            },
            {
                module.BRANCH_COLUMN: "canvas_0_134",
                "From bus": "canvas_0_29",
                "To bus": "canvas_0_32",
                module.P_IJ_COLUMN: -226.512,
            },
            {
                module.BRANCH_COLUMN: "canvas_0_130",
                "From bus": "canvas_0_31",
                "To bus": "canvas_0_32",
                module.P_IJ_COLUMN: -385.082,
            },
            {
                module.BRANCH_COLUMN: "canvas_0_123",
                "From bus": "canvas_0_29",
                "To bus": "canvas_0_30",
                module.P_IJ_COLUMN: 173.642,
            },
        ]

        summary = module.compute_active_redispatch_summary(
            base_buses=base_buses,
            base_branches=base_branches,
            adjusted_buses=adjusted_buses,
            adjusted_branches=adjusted_branches,
        )

        assert summary["generator"] == "Gen38"
        assert summary["target_bus"]["adjusted_p_gen"] == 900.0
        assert summary["slack_bus"]["adjusted_p_gen"] == 1246.662
        assert summary["monitored_branches"]["canvas_0_258"]["delta_abs_p_ij"] == 70.0
        assert summary["monitored_branches"]["canvas_0_126"]["adjusted_abs_p_ij"] == 177.745

    def test_compute_load_transfer_summary_tracks_remote_buses_and_corridor_rebalancing(self):
        module = load_module(
            POWERFLOW_ENGINEERING_STUDY_PATH,
            "powerflow_engineering_study_example_load_transfer",
        )
        base_buses = [
            {
                module.BUS_COLUMN: "canvas_0_35",
                module.VM_COLUMN: 1.03,
                module.VA_COLUMN: 15.44,
                module.P_GEN_COLUMN: 1315.472,
                module.Q_GEN_COLUMN: 238.070,
            },
            {
                module.BUS_COLUMN: "canvas_0_154",
                module.VM_COLUMN: 0.9825,
                module.VA_COLUMN: -2.10,
                module.P_GEN_COLUMN: 0.0,
                module.Q_GEN_COLUMN: 0.0,
            },
            {
                module.BUS_COLUMN: "canvas_0_153",
                module.VM_COLUMN: 0.9760,
                module.VA_COLUMN: -5.40,
                module.P_GEN_COLUMN: 0.0,
                module.Q_GEN_COLUMN: 0.0,
            },
            {
                module.BUS_COLUMN: "canvas_0_181",
                module.VM_COLUMN: 0.9720,
                module.VA_COLUMN: -6.20,
                module.P_GEN_COLUMN: 0.0,
                module.Q_GEN_COLUMN: 0.0,
            },
        ]
        adjusted_buses = [
            {
                module.BUS_COLUMN: "canvas_0_35",
                module.VM_COLUMN: 1.03,
                module.VA_COLUMN: 15.44,
                module.P_GEN_COLUMN: 1316.455,
                module.Q_GEN_COLUMN: 184.921,
            },
            {
                module.BUS_COLUMN: "canvas_0_154",
                module.VM_COLUMN: 0.9740,
                module.VA_COLUMN: -9.71,
                module.P_GEN_COLUMN: 0.0,
                module.Q_GEN_COLUMN: 0.0,
            },
            {
                module.BUS_COLUMN: "canvas_0_153",
                module.VM_COLUMN: 0.9723,
                module.VA_COLUMN: -12.69,
                module.P_GEN_COLUMN: 0.0,
                module.Q_GEN_COLUMN: 0.0,
            },
            {
                module.BUS_COLUMN: "canvas_0_181",
                module.VM_COLUMN: 0.9694,
                module.VA_COLUMN: -13.31,
                module.P_GEN_COLUMN: 0.0,
                module.Q_GEN_COLUMN: 0.0,
            },
        ]
        base_branches = [
            {
                module.BRANCH_COLUMN: "canvas_0_175",
                "From bus": "canvas_0_154",
                "To bus": "canvas_0_153",
                module.P_IJ_COLUMN: -603.930,
            },
            {
                module.BRANCH_COLUMN: "canvas_0_182",
                "From bus": "canvas_0_181",
                "To bus": "canvas_0_153",
                module.P_IJ_COLUMN: -42.961,
            },
            {
                module.BRANCH_COLUMN: "canvas_0_185",
                "From bus": "canvas_0_114",
                "To bus": "canvas_0_181",
                module.P_IJ_COLUMN: -352.677,
            },
        ]
        adjusted_branches = [
            {
                module.BRANCH_COLUMN: "canvas_0_175",
                "From bus": "canvas_0_154",
                "To bus": "canvas_0_153",
                module.P_IJ_COLUMN: -638.251,
            },
            {
                module.BRANCH_COLUMN: "canvas_0_182",
                "From bus": "canvas_0_181",
                "To bus": "canvas_0_153",
                module.P_IJ_COLUMN: -8.179,
            },
            {
                module.BRANCH_COLUMN: "canvas_0_185",
                "From bus": "canvas_0_114",
                "To bus": "canvas_0_181",
                module.P_IJ_COLUMN: -318.383,
            },
        ]

        summary = module.compute_load_transfer_summary(
            base_buses=base_buses,
            base_branches=base_branches,
            adjusted_buses=adjusted_buses,
            adjusted_branches=adjusted_branches,
        )

        assert summary["source_load"]["adjusted_p"] == 904.0
        assert summary["target_load"]["adjusted_q"] == 175.0
        assert summary["slack_bus"]["adjusted_p_gen"] == 1316.455
        assert summary["monitored_buses"]["canvas_0_154"]["delta_vm"] == pytest.approx(-0.0085, abs=1e-4)
        assert summary["monitored_branches"]["canvas_0_175"]["delta_abs_p_ij"] == pytest.approx(
            34.321,
            abs=1e-3,
        )
        assert summary["monitored_branches"]["canvas_0_182"]["delta_abs_p_ij"] == pytest.approx(
            -34.782,
            abs=1e-3,
        )

    def test_compute_reactive_stress_summary_tracks_voltage_drop_and_reactive_support_ranking(self):
        module = load_module(
            POWERFLOW_ENGINEERING_STUDY_PATH,
            "powerflow_engineering_study_example_reactive_stress",
        )
        base_buses = [
            {
                module.BUS_COLUMN: "canvas_0_35",
                module.NODE_COLUMN: "canvas_10_399",
                module.VM_COLUMN: 1.03,
                module.VA_COLUMN: 0.0,
                module.P_GEN_COLUMN: 1315.472,
                module.Q_GEN_COLUMN: 238.070,
            },
            {
                module.BUS_COLUMN: "canvas_0_154",
                module.NODE_COLUMN: "",
                module.VM_COLUMN: 0.9938,
                module.VA_COLUMN: 3.6022,
                module.P_GEN_COLUMN: 0.0,
                module.Q_GEN_COLUMN: 0.0,
            },
            {
                module.BUS_COLUMN: "canvas_0_153",
                module.NODE_COLUMN: "",
                module.VM_COLUMN: 1.0209,
                module.VA_COLUMN: 8.3219,
                module.P_GEN_COLUMN: 0.0,
                module.Q_GEN_COLUMN: 0.0,
            },
            {
                module.BUS_COLUMN: "canvas_0_181",
                module.NODE_COLUMN: "",
                module.VM_COLUMN: 1.0200,
                module.VA_COLUMN: 8.0973,
                module.P_GEN_COLUMN: 0.0,
                module.Q_GEN_COLUMN: 0.0,
            },
            {
                module.BUS_COLUMN: "canvas_0_114",
                module.NODE_COLUMN: "",
                module.VM_COLUMN: 0.9947,
                module.VA_COLUMN: 1.1450,
                module.P_GEN_COLUMN: 0.0,
                module.Q_GEN_COLUMN: 0.0,
            },
            {
                module.BUS_COLUMN: "canvas_0_152",
                module.NODE_COLUMN: "canvas_6_351",
                module.VM_COLUMN: 1.05,
                module.VA_COLUMN: 0.0,
                module.P_GEN_COLUMN: 650.0,
                module.Q_GEN_COLUMN: 120.0,
            },
            {
                module.BUS_COLUMN: "canvas_0_189",
                module.NODE_COLUMN: "canvas_8_373",
                module.VM_COLUMN: 1.02,
                module.VA_COLUMN: 0.0,
                module.P_GEN_COLUMN: 560.0,
                module.Q_GEN_COLUMN: 80.0,
            },
        ]
        adjusted_buses = [
            {
                module.BUS_COLUMN: "canvas_0_35",
                module.NODE_COLUMN: "canvas_10_399",
                module.VM_COLUMN: 1.03,
                module.VA_COLUMN: 0.0,
                module.P_GEN_COLUMN: 1315.912,
                module.Q_GEN_COLUMN: 242.859,
            },
            {
                module.BUS_COLUMN: "canvas_0_154",
                module.NODE_COLUMN: "",
                module.VM_COLUMN: 0.9804,
                module.VA_COLUMN: 3.7080,
                module.P_GEN_COLUMN: 0.0,
                module.Q_GEN_COLUMN: 0.0,
            },
            {
                module.BUS_COLUMN: "canvas_0_153",
                module.NODE_COLUMN: "",
                module.VM_COLUMN: 1.0150,
                module.VA_COLUMN: 8.4844,
                module.P_GEN_COLUMN: 0.0,
                module.Q_GEN_COLUMN: 0.0,
            },
            {
                module.BUS_COLUMN: "canvas_0_181",
                module.NODE_COLUMN: "",
                module.VM_COLUMN: 1.0152,
                module.VA_COLUMN: 8.2456,
                module.P_GEN_COLUMN: 0.0,
                module.Q_GEN_COLUMN: 0.0,
            },
            {
                module.BUS_COLUMN: "canvas_0_114",
                module.NODE_COLUMN: "",
                module.VM_COLUMN: 0.9885,
                module.VA_COLUMN: 1.1928,
                module.P_GEN_COLUMN: 0.0,
                module.Q_GEN_COLUMN: 0.0,
            },
            {
                module.BUS_COLUMN: "canvas_0_152",
                module.NODE_COLUMN: "canvas_6_351",
                module.VM_COLUMN: 1.05,
                module.VA_COLUMN: 0.0,
                module.P_GEN_COLUMN: 650.0,
                module.Q_GEN_COLUMN: 163.831,
            },
            {
                module.BUS_COLUMN: "canvas_0_189",
                module.NODE_COLUMN: "canvas_8_373",
                module.VM_COLUMN: 1.02,
                module.VA_COLUMN: 0.0,
                module.P_GEN_COLUMN: 560.0,
                module.Q_GEN_COLUMN: 98.878,
            },
        ]
        base_branches = [
            {
                module.BRANCH_COLUMN: "canvas_0_175",
                "From bus": "canvas_0_154",
                "To bus": "canvas_0_153",
                module.P_IJ_COLUMN: -603.930,
            },
            {
                module.BRANCH_COLUMN: "canvas_0_182",
                "From bus": "canvas_0_181",
                "To bus": "canvas_0_153",
                module.P_IJ_COLUMN: -42.961,
            },
            {
                module.BRANCH_COLUMN: "canvas_0_185",
                "From bus": "canvas_0_114",
                "To bus": "canvas_0_181",
                module.P_IJ_COLUMN: -352.677,
            },
        ]
        adjusted_branches = [
            {
                module.BRANCH_COLUMN: "canvas_0_175",
                "From bus": "canvas_0_154",
                "To bus": "canvas_0_153",
                module.P_IJ_COLUMN: -602.303,
            },
            {
                module.BRANCH_COLUMN: "canvas_0_182",
                "From bus": "canvas_0_181",
                "To bus": "canvas_0_153",
                module.P_IJ_COLUMN: -44.387,
            },
            {
                module.BRANCH_COLUMN: "canvas_0_185",
                "From bus": "canvas_0_114",
                "To bus": "canvas_0_181",
                module.P_IJ_COLUMN: -354.042,
            },
        ]

        summary = module.compute_reactive_stress_summary(
            base_buses=base_buses,
            base_branches=base_branches,
            adjusted_buses=adjusted_buses,
            adjusted_branches=adjusted_branches,
        )

        assert summary["target_load"]["adjusted_q"] == 215.0
        assert summary["slack_bus"]["adjusted_q_gen"] == 242.859
        assert summary["monitored_buses"]["canvas_0_154"]["delta_vm"] == pytest.approx(-0.0134, abs=1e-4)
        assert summary["monitored_branches"]["canvas_0_175"]["delta_abs_p_ij"] == pytest.approx(
            -1.627,
            abs=1e-3,
        )
        assert summary["top_reactive_support_changes"][0]["bus_id"] == "canvas_0_152"
        assert summary["top_reactive_support_changes"][0]["delta_q_gen"] == pytest.approx(
            43.831,
            abs=1e-3,
        )


class TestPowerFlowBatchStudyExample:
    def test_load_model_from_source_reads_local_yaml(self, tmp_path):
        module = load_module(
            POWERFLOW_BATCH_STUDY_PATH,
            "powerflow_batch_study_example",
        )
        export_path = tmp_path / "local-batch-model.yaml"

        Model.dump(build_local_model(), str(export_path), compress=None)
        loaded_model = module.load_model_from_source(str(export_path))

        assert loaded_model.name == "local-example-model"
        assert loaded_model.rid == "model/test/local-example-model"

    def test_build_scenario_specs_includes_load_transfer_and_reactive_stress(self):
        module = load_module(
            POWERFLOW_BATCH_STUDY_PATH,
            "powerflow_batch_study_example_specs",
        )

        names = [item["name"] for item in module.build_scenario_specs()]

        assert "load_shift_39_to_21" in names
        assert "load21_q_up" in names

    def test_extract_study_metrics_marks_removed_branch_as_none(self):
        module = load_module(
            POWERFLOW_BATCH_STUDY_PATH,
            "powerflow_batch_study_example_metrics",
        )
        bus_rows = [
            {
                module.BUS_COLUMN: "canvas_0_35",
                module.NODE_COLUMN: "canvas_10_399",
                module.P_GEN_COLUMN: 1315.4,
                module.Q_GEN_COLUMN: 238.1,
                module.VM_COLUMN: 1.03,
            },
            {
                module.BUS_COLUMN: "canvas_0_28",
                module.NODE_COLUMN: "canvas_2_303",
                module.P_GEN_COLUMN: 250.0,
                module.Q_GEN_COLUMN: 157.7,
                module.VM_COLUMN: 1.047,
            },
            {
                module.BUS_COLUMN: "canvas_0_33",
                module.NODE_COLUMN: "canvas_9_384",
                module.P_GEN_COLUMN: 830.0,
                module.Q_GEN_COLUMN: 75.7,
                module.VM_COLUMN: 1.026,
            },
            {
                module.BUS_COLUMN: "canvas_0_154",
                module.NODE_COLUMN: "",
                module.P_GEN_COLUMN: 0.0,
                module.Q_GEN_COLUMN: 0.0,
                module.VM_COLUMN: 0.982,
            },
        ]
        branch_rows = [
            {
                module.BRANCH_COLUMN: "canvas_0_134",
                module.P_IJ_COLUMN: -333.4,
            },
            {
                module.BRANCH_COLUMN: "canvas_0_130",
                module.P_IJ_COLUMN: -206.0,
            },
            {
                module.BRANCH_COLUMN: "canvas_0_175",
                module.P_IJ_COLUMN: -603.9,
            },
            {
                module.BRANCH_COLUMN: "canvas_0_182",
                module.P_IJ_COLUMN: -43.0,
            },
            {
                module.BRANCH_COLUMN: "canvas_0_185",
                module.P_IJ_COLUMN: -352.7,
            },
        ]

        metrics = module.extract_study_metrics(bus_rows, branch_rows)

        assert metrics["slack_p_gen"] == 1315.4
        assert metrics["bus30_vm"] == 1.047
        assert metrics["gen38_p_gen"] == 830.0
        assert metrics["bus21_vm"] == 0.982
        assert metrics["line_26_28_abs_pij"] is None
        assert metrics["line_26_29_abs_pij"] == 333.4
        assert metrics["line_21_22_abs_pij"] == 603.9
        assert metrics["line_22_23_abs_pij"] == 43.0
        assert metrics["line_23_24_abs_pij"] == 352.7

    def test_build_summary_rows_formats_numeric_and_removed_metrics(self):
        module = load_module(
            POWERFLOW_BATCH_STUDY_PATH,
            "powerflow_batch_study_example_summary",
        )

        rows = module.build_summary_rows(
            [
                {
                    "name": "baseline",
                    "description": "基线工况",
                    "metrics": {
                        "slack_p_gen": 1315.472094,
                        "slack_q_gen": 238.069675,
                        "bus30_vm": 1.047,
                        "bus30_q_gen": 157.653238,
                        "gen38_p_gen": 830.0,
                        "gen38_q_gen": 75.665832,
                        "bus21_vm": 0.982321,
                        "line_26_28_abs_pij": 143.504584,
                        "line_26_29_abs_pij": 192.398298,
                        "line_28_29_abs_pij": 350.371039,
                        "line_21_22_abs_pij": 603.929564,
                        "line_22_23_abs_pij": 42.960627,
                        "line_23_24_abs_pij": 352.677324,
                    },
                },
                {
                    "name": "line_outage",
                    "description": "切除 line-26-28",
                    "metrics": {
                        "slack_p_gen": 1315.472094,
                        "slack_q_gen": 238.069675,
                        "bus30_vm": 1.047,
                        "bus30_q_gen": 157.653238,
                        "gen38_p_gen": 830.0,
                        "gen38_q_gen": 75.665832,
                        "bus21_vm": 0.971111,
                        "line_26_28_abs_pij": None,
                        "line_26_29_abs_pij": 333.439765,
                        "line_28_29_abs_pij": 206.000000,
                        "line_21_22_abs_pij": 603.929564,
                        "line_22_23_abs_pij": 42.960627,
                        "line_23_24_abs_pij": 352.677324,
                    },
                },
            ]
        )

        assert rows[0]["scenario"] == "baseline"
        assert rows[0]["slack_p_gen"] == "1315.472"
        assert rows[0]["gen38_p_gen"] == "830.000"
        assert rows[0]["bus21_vm"] == "0.982"
        assert rows[1]["line_26_28_abs_pij"] == "removed"
        assert rows[1]["line_26_29_abs_pij"] == "333.440"
        assert rows[1]["line_21_22_abs_pij"] == "603.930"


class TestPowerFlowN1ScreeningExample:
    def test_load_model_from_source_reads_local_yaml(self, tmp_path):
        module = load_module(
            POWERFLOW_N1_SCREENING_PATH,
            "powerflow_n1_screening_example",
        )
        export_path = tmp_path / "local-n1-model.yaml"

        Model.dump(build_local_n1_model(), str(export_path), compress=None)
        loaded_model = module.load_model_from_source(str(export_path))

        assert loaded_model.name == "local-n1-model"
        assert loaded_model.rid == "model/test/local-n1-model"

    def test_choose_candidate_branch_ids_supports_full_set_and_validated_subset(self):
        module = load_module(
            POWERFLOW_N1_SCREENING_PATH,
            "powerflow_n1_screening_example_candidates",
        )
        model = build_local_n1_model()

        original_default_branch_ids = list(module.DEFAULT_VALIDATED_BRANCH_IDS)
        module.DEFAULT_VALIDATED_BRANCH_IDS = ["line_a", "missing_branch", "line_b", "transformer_a"]
        try:
            discovered = module.choose_candidate_branch_ids(model)
            discovered_lines_only = module.choose_candidate_branch_ids(
                model,
                include_transformers=False,
            )
            validated = module.choose_candidate_branch_ids(
                model,
                use_all_discovered=False,
                limit=2,
            )
        finally:
            module.DEFAULT_VALIDATED_BRANCH_IDS = original_default_branch_ids

        assert discovered == ["line_a", "line_b", "line_c", "transformer_a"]
        assert discovered_lines_only == ["line_a", "line_b", "line_c"]
        assert validated == ["line_a", "line_b"]

    def test_filter_candidate_branches_by_base_presence_excludes_base_absent_components(self):
        module = load_module(
            POWERFLOW_N1_SCREENING_PATH,
            "powerflow_n1_screening_example_base_presence",
        )
        candidates = [
            {"branch_id": "line_a", "branch_name": "line-a", "branch_kind": "line", "enabled": True},
            {
                "branch_id": "transformer_a",
                "branch_name": "transformer-a",
                "branch_kind": "transformer",
                "enabled": True,
            },
            {"branch_id": "line_c", "branch_name": "line-c", "branch_kind": "line", "enabled": False},
        ]

        active, skipped = module.filter_candidate_branches_by_base_presence(
            candidates,
            base_branch_ids={"line_a", "transformer_a"},
        )

        assert [item["branch_id"] for item in active] == ["line_a", "transformer_a"]
        assert [item["branch_id"] for item in skipped] == ["line_c"]

    def test_compute_n1_delta_metrics_tracks_bus_and_branch_shifts(self):
        module = load_module(
            POWERFLOW_N1_SCREENING_PATH,
            "powerflow_n1_screening_example_metrics",
        )
        base_buses = [
            {module.BUS_COLUMN: "bus-a", module.VM_COLUMN: 1.01},
            {module.BUS_COLUMN: "bus-b", module.VM_COLUMN: 1.02},
            {module.BUS_COLUMN: "bus-c", module.VM_COLUMN: 0.96},
        ]
        outage_buses = [
            {module.BUS_COLUMN: "bus-a", module.VM_COLUMN: 0.99},
            {module.BUS_COLUMN: "bus-b", module.VM_COLUMN: 0.94},
        ]
        base_branches = [
            {module.BRANCH_COLUMN: "line-1", module.P_IJ_COLUMN: -120.0},
            {module.BRANCH_COLUMN: "line-2", module.P_IJ_COLUMN: 80.0},
            {module.BRANCH_COLUMN: "line-3", module.P_IJ_COLUMN: 40.0},
        ]
        outage_branches = [
            {module.BRANCH_COLUMN: "line-2", module.P_IJ_COLUMN: 130.0},
            {module.BRANCH_COLUMN: "line-3", module.P_IJ_COLUMN: -20.0},
        ]

        metrics = module.compute_n1_delta_metrics(
            base_buses=base_buses,
            base_branches=base_branches,
            outage_buses=outage_buses,
            outage_branches=outage_branches,
        )

        assert metrics["min_vm"] == 0.94
        assert metrics["min_vm_bus_id"] == "bus-b"
        assert metrics["low_voltage_bus_count"] == 1
        assert metrics["new_low_voltage_bus_count"] == 1
        assert metrics["new_low_voltage_buses"] == ["bus-b"]
        assert metrics["missing_bus_count"] == 1
        assert metrics["missing_bus_ids"] == ["bus-c"]
        assert metrics["missing_branch_count"] == 1
        assert metrics["missing_branch_ids"] == ["line-1"]
        assert metrics["max_vm_shift"] == 0.08000000000000007
        assert metrics["max_vm_shift_bus_id"] == "bus-b"
        assert metrics["max_branch_shift"] == 50.0
        assert metrics["max_branch_shift_branch_id"] == "line-2"

    def test_build_summary_rows_formats_screening_output(self):
        module = load_module(
            POWERFLOW_N1_SCREENING_PATH,
            "powerflow_n1_screening_example_summary",
        )

        rows = module.build_summary_rows(
            [
                {
                    "branch_id": "canvas_0_126",
                    "branch_name": "line-26-28",
                    "branch_kind": "line",
                    "severity": "warning",
                    "rank": 2,
                    "branch_present_after_outage": False,
                    "min_vm": 0.9332,
                    "min_vm_bus_id": "canvas_0_39",
                    "new_low_voltage_bus_count": 0,
                    "new_low_voltage_buses": [],
                    "new_high_voltage_bus_count": 0,
                    "new_high_voltage_buses": [],
                    "missing_bus_count": 2,
                    "missing_bus_ids": ["canvas_0_01", "canvas_0_02"],
                    "missing_branch_count": 3,
                    "missing_branch_ids": ["canvas_0_126", "canvas_0_130", "canvas_0_134"],
                    "max_vm_shift": 0.016777,
                    "max_vm_shift_bus_id": "canvas_0_30",
                    "max_branch_shift": 141.041,
                    "max_branch_shift_branch_id": "canvas_0_130",
                }
            ]
        )

        assert rows == [
            {
                "rank": "2",
                "branch_id": "canvas_0_126",
                "branch_name": "line-26-28",
                "branch_kind": "line",
                "severity": "warning",
                "branch_present_after_outage": "no",
                "min_vm": "0.9332",
                "min_vm_bus_id": "canvas_0_39",
                "new_low_voltage_bus_count": "0",
                "new_low_voltage_buses": "-",
                "new_high_voltage_bus_count": "0",
                "new_high_voltage_buses": "-",
                "missing_bus_count": "2",
                "missing_bus_ids": "canvas_0_01,canvas_0_02",
                "missing_branch_count": "3",
                "missing_branch_ids": "canvas_0_126,canvas_0_130,canvas_0_134",
                "max_vm_shift": "0.0168",
                "max_vm_shift_bus_id": "canvas_0_30",
                "max_branch_shift": "141.041",
                "max_branch_shift_branch_id": "canvas_0_130",
            }
        ]

    def test_build_screening_digest_summarizes_top_cases_by_kind_and_failure_mode(self):
        module = load_module(
            POWERFLOW_N1_SCREENING_PATH,
            "powerflow_n1_screening_example_digest",
        )

        digest = module.build_screening_digest(
            [
                {
                    "branch_id": "line-a",
                    "branch_name": "line-a",
                    "branch_kind": "line",
                    "severity": "warning",
                    "min_vm": 0.9300,
                    "min_vm_bus_id": "bus-a",
                    "missing_bus_count": 0,
                    "new_low_voltage_bus_count": 0,
                    "new_high_voltage_bus_count": 0,
                    "max_vm_shift": 0.0200,
                    "max_branch_shift": 150.0,
                },
                {
                    "branch_id": "xf-1",
                    "branch_name": "xf-1",
                    "branch_kind": "transformer",
                    "severity": "critical",
                    "min_vm": 0.9100,
                    "min_vm_bus_id": "bus-b",
                    "missing_bus_count": 2,
                    "new_low_voltage_bus_count": 1,
                    "new_high_voltage_bus_count": 0,
                    "max_vm_shift": 0.0500,
                    "max_branch_shift": 220.0,
                },
                {
                    "branch_id": "line-b",
                    "branch_name": "line-b",
                    "branch_kind": "line",
                    "severity": "critical",
                    "min_vm": 0.9000,
                    "min_vm_bus_id": "bus-c",
                    "missing_bus_count": 1,
                    "new_low_voltage_bus_count": 2,
                    "new_high_voltage_bus_count": 0,
                    "max_vm_shift": 0.0600,
                    "max_branch_shift": 300.0,
                },
            ]
        )

        assert digest["total_cases"] == 3
        assert digest["severity_counts"] == {"critical": 2, "warning": 1, "observe": 0}
        assert digest["branch_kind_counts"] == {"line": 2, "transformer": 1}
        assert digest["top_case"]["branch_id"] == "line-a"
        assert digest["top_line_case"]["branch_id"] == "line-a"
        assert digest["top_transformer_case"]["branch_id"] == "xf-1"
        assert digest["lowest_voltage_case"]["branch_id"] == "line-b"
        assert digest["largest_vm_shift_case"]["branch_id"] == "line-b"
        assert digest["largest_branch_shift_case"]["branch_id"] == "line-b"
        assert digest["largest_missing_bus_case"]["branch_id"] == "xf-1"

    def test_rank_n1_results_prioritizes_new_voltage_violations_then_shift_magnitude(self):
        module = load_module(
            POWERFLOW_N1_SCREENING_PATH,
            "powerflow_n1_screening_example_rank",
        )

        ranked = module.rank_n1_results(
            [
                {
                    "branch_id": "line-a",
                    "new_low_voltage_bus_count": 0,
                    "new_high_voltage_bus_count": 0,
                    "min_vm": 0.9097,
                    "max_vm_shift": 0.0168,
                    "max_branch_shift": 144.3,
                },
                {
                    "branch_id": "line-b",
                    "new_low_voltage_bus_count": 1,
                    "new_high_voltage_bus_count": 0,
                    "min_vm": 0.9093,
                    "max_vm_shift": 0.0211,
                    "max_branch_shift": 192.0,
                },
                {
                    "branch_id": "line-c",
                    "new_low_voltage_bus_count": 1,
                    "new_high_voltage_bus_count": 0,
                    "min_vm": 0.9085,
                    "max_vm_shift": 0.0468,
                    "max_branch_shift": 336.9,
                },
            ]
        )

        assert [item["branch_id"] for item in ranked] == ["line-c", "line-b", "line-a"]
        assert module.classify_n1_severity(ranked[0]) == "critical"
        assert module.classify_n1_severity(ranked[-1]) == "warning"

    def test_export_summary_rows_csv_writes_ranked_screening_table(self, tmp_path):
        module = load_module(
            POWERFLOW_N1_SCREENING_PATH,
            "powerflow_n1_screening_example_csv",
        )
        export_path = tmp_path / "n1-screening.csv"
        rows = [
            {
                "rank": "1",
                "branch_id": "canvas_0_130",
                "branch_name": "line-28-29",
                "branch_kind": "line",
                "severity": "critical",
                "branch_present_after_outage": "no",
                "min_vm": "0.9085",
                "min_vm_bus_id": "canvas_0_29",
                "new_low_voltage_bus_count": "1",
                "new_low_voltage_buses": "canvas_0_29",
                "new_high_voltage_bus_count": "0",
                "new_high_voltage_buses": "-",
                "missing_bus_count": "0",
                "missing_bus_ids": "-",
                "missing_branch_count": "1",
                "missing_branch_ids": "canvas_0_130",
                "max_vm_shift": "0.0468",
                "max_vm_shift_bus_id": "canvas_0_29",
                "max_branch_shift": "336.929",
                "max_branch_shift_branch_id": "canvas_0_134",
            }
        ]

        module.export_summary_rows_csv(rows, export_path)

        content = export_path.read_text(encoding="utf-8")
        assert "severity" in content
        assert "missing_bus_count" in content
        assert "line-28-29" in content
        assert "336.929" in content


class TestPowerFlowMaintenanceSecurityExample:
    def test_load_model_from_source_reads_local_yaml(self, tmp_path):
        module = load_module(
            POWERFLOW_MAINTENANCE_SECURITY_PATH,
            "powerflow_maintenance_security_example",
        )
        export_path = tmp_path / "local-maintenance-model.yaml"

        Model.dump(build_local_n1_model(), str(export_path), compress=None)
        loaded_model = module.load_model_from_source(str(export_path))

        assert loaded_model.name == "local-n1-model"
        assert loaded_model.rid == "model/test/local-n1-model"

    def test_choose_followup_branch_ids_excludes_maintenance_branch_and_disabled_components(self):
        module = load_module(
            POWERFLOW_MAINTENANCE_SECURITY_PATH,
            "powerflow_maintenance_security_example_followup",
        )
        model = build_local_n1_model()

        original_default_ids = list(module.DEFAULT_VALIDATED_FOLLOWUP_BRANCH_IDS)
        module.DEFAULT_VALIDATED_FOLLOWUP_BRANCH_IDS = [
            "line_a",
            "line_b",
            "transformer_a",
            "missing_branch",
        ]
        try:
            validated = module.choose_followup_branch_ids(
                model,
                "line_a",
                use_all_discovered=False,
                base_branch_ids={"line_a", "line_b", "transformer_a"},
            )
            discovered = module.choose_followup_branch_ids(
                model,
                "line_a",
                use_all_discovered=True,
                base_branch_ids={"line_a", "line_b", "transformer_a"},
            )
        finally:
            module.DEFAULT_VALIDATED_FOLLOWUP_BRANCH_IDS = original_default_ids

        assert validated == ["line_b", "transformer_a"]
        assert discovered == ["line_b", "transformer_a"]

    def test_choose_followup_branch_ids_supports_transformer_maintenance_case(self):
        module = load_module(
            POWERFLOW_MAINTENANCE_SECURITY_PATH,
            "powerflow_maintenance_security_example_transformer_followup",
        )
        model = build_local_n1_model()

        original_default_ids = list(module.DEFAULT_VALIDATED_FOLLOWUP_BRANCH_IDS)
        module.DEFAULT_VALIDATED_FOLLOWUP_BRANCH_IDS = [
            "transformer_a",
            "line_a",
            "line_b",
        ]
        try:
            validated = module.choose_followup_branch_ids(
                model,
                "transformer_a",
                use_all_discovered=False,
                base_branch_ids={"line_a", "line_b", "transformer_a"},
            )
        finally:
            module.DEFAULT_VALIDATED_FOLLOWUP_BRANCH_IDS = original_default_ids

        assert validated == ["line_a", "line_b"]

    def test_build_summary_rows_attaches_maintenance_context(self):
        module = load_module(
            POWERFLOW_MAINTENANCE_SECURITY_PATH,
            "powerflow_maintenance_security_example_summary",
        )

        rows = module.build_summary_rows(
            {
                "maintenance_case": {
                    "branch_id": "line_a",
                    "branch_name": "line-26-28",
                    "branch_kind": "line",
                    "severity": "warning",
                    "min_vm": 0.9332,
                },
                "followup_results": [
                    {
                        "branch_id": "line_b",
                        "branch_name": "line-26-29",
                        "branch_kind": "line",
                        "severity": "critical",
                        "rank": 1,
                        "branch_present_after_outage": False,
                        "min_vm": 0.9085,
                        "min_vm_bus_id": "bus-b",
                        "new_low_voltage_bus_count": 1,
                        "new_low_voltage_buses": ["bus-b"],
                        "new_high_voltage_bus_count": 0,
                        "new_high_voltage_buses": [],
                        "missing_bus_count": 0,
                        "missing_bus_ids": [],
                        "missing_branch_count": 1,
                        "missing_branch_ids": ["line_b"],
                        "max_vm_shift": 0.0468,
                        "max_vm_shift_bus_id": "bus-b",
                        "max_branch_shift": 336.929,
                        "max_branch_shift_branch_id": "line_c",
                    }
                ],
            }
        )

        assert rows == [
            {
                "maintenance_branch_id": "line_a",
                "maintenance_branch_name": "line-26-28",
                "maintenance_branch_kind": "line",
                "maintenance_severity": "warning",
                "maintenance_min_vm": "0.9332",
                "rank": "1",
                "branch_id": "line_b",
                "branch_name": "line-26-29",
                "branch_kind": "line",
                "severity": "critical",
                "branch_present_after_outage": "no",
                "min_vm": "0.9085",
                "min_vm_bus_id": "bus-b",
                "new_low_voltage_bus_count": "1",
                "new_low_voltage_buses": "bus-b",
                "new_high_voltage_bus_count": "0",
                "new_high_voltage_buses": "-",
                "missing_bus_count": "0",
                "missing_bus_ids": "-",
                "missing_branch_count": "1",
                "missing_branch_ids": "line_b",
                "max_vm_shift": "0.0468",
                "max_vm_shift_bus_id": "bus-b",
                "max_branch_shift": "336.929",
                "max_branch_shift_branch_id": "line_c",
            }
        ]

    def test_build_conclusion_report_describes_maintenance_and_residual_top_case(self):
        module = load_module(
            POWERFLOW_MAINTENANCE_SECURITY_PATH,
            "powerflow_maintenance_security_example_conclusion",
        )

        report = module.build_conclusion_report(
            {
                "maintenance_case": {
                    "branch_id": "line_a",
                    "branch_name": "line-26-28",
                    "branch_kind": "line",
                    "branch_present_after_outage": False,
                    "severity": "warning",
                    "min_vm": 0.9332,
                    "min_vm_bus_id": "bus-29",
                    "missing_bus_count": 0,
                    "max_vm_shift": 0.0168,
                    "max_vm_shift_bus_id": "bus-30",
                    "max_branch_shift": 141.041,
                    "max_branch_shift_branch_id": "line_b",
                },
                "followup_digest": {
                    "top_case": {
                        "branch_id": "line_b",
                        "branch_name": "line-26-29",
                        "severity": "critical",
                        "min_vm": 0.9085,
                        "min_vm_bus_id": "bus-29",
                        "new_low_voltage_bus_count": 1,
                        "new_high_voltage_bus_count": 0,
                        "max_branch_shift": 336.929,
                        "max_branch_shift_branch_id": "line_c",
                    }
                },
            }
        )

        assert "line-26-28" in report["findings"][0]["title"]
        assert report["findings"][0]["supported"] is True
        assert "line-26-29" in report["findings"][1]["title"]
        assert report["findings"][2]["supported"] is True
        assert "IEEE39" in report["boundary"]

    def test_export_summary_rows_csv_writes_maintenance_context_columns(self, tmp_path):
        module = load_module(
            POWERFLOW_MAINTENANCE_SECURITY_PATH,
            "powerflow_maintenance_security_example_csv",
        )
        export_path = tmp_path / "maintenance-security.csv"
        rows = [
            {
                "maintenance_branch_id": "line_a",
                "maintenance_branch_name": "line-26-28",
                "maintenance_branch_kind": "line",
                "maintenance_severity": "warning",
                "maintenance_min_vm": "0.9332",
                "rank": "1",
                "branch_id": "line_b",
                "branch_name": "line-26-29",
                "branch_kind": "line",
                "severity": "critical",
                "branch_present_after_outage": "no",
                "min_vm": "0.9085",
                "min_vm_bus_id": "bus-b",
                "new_low_voltage_bus_count": "1",
                "new_low_voltage_buses": "bus-b",
                "new_high_voltage_bus_count": "0",
                "new_high_voltage_buses": "-",
                "missing_bus_count": "0",
                "missing_bus_ids": "-",
                "missing_branch_count": "1",
                "missing_branch_ids": "line_b",
                "max_vm_shift": "0.0468",
                "max_vm_shift_bus_id": "bus-b",
                "max_branch_shift": "336.929",
                "max_branch_shift_branch_id": "line_c",
            }
        ]

        module.export_summary_rows_csv(rows, export_path)

        content = export_path.read_text(encoding="utf-8")
        assert "maintenance_branch_id" in content
        assert "maintenance_severity" in content
        assert "line-26-29" in content

    def test_parse_args_supports_maintenance_and_export_options(self):
        module = load_module(
            POWERFLOW_MAINTENANCE_SECURITY_PATH,
            "powerflow_maintenance_security_example_args",
        )

        (
            source,
            maintenance_branch_id,
            use_all_discovered,
            include_transformers,
            limit,
            csv_path,
            conclusion_path,
        ) = module.parse_args(
            [
                "study-case.yaml",
                "--maintenance-branch=line_b",
                "--all-discovered",
                "--lines-only",
                "--limit=4",
                "--csv=maintenance.csv",
                "--conclusion-txt=maintenance.txt",
            ]
        )

        assert source == "study-case.yaml"
        assert maintenance_branch_id == "line_b"
        assert use_all_discovered is True
        assert include_transformers is False
        assert limit == 4
        assert csv_path == "maintenance.csv"
        assert conclusion_path == "maintenance.txt"


class TestEMTFaultStudyExample:
    def test_load_model_from_source_reads_local_yaml(self, tmp_path):
        module = load_module(
            EMT_FAULT_STUDY_PATH,
            "emt_fault_study_example",
        )
        export_path = tmp_path / "local-emt-study-model.yaml"

        Model.dump(build_local_model(), str(export_path), compress=None)
        loaded_model = module.load_model_from_source(str(export_path))

        assert loaded_model.name == "local-example-model"
        assert loaded_model.rid == "model/test/local-example-model"

    def test_extract_voltage_recovery_metrics_uses_declared_windows(self):
        module = load_module(
            EMT_FAULT_STUDY_PATH,
            "emt_fault_study_example_metrics",
        )

        xs = [index / 100 for index in range(301)]
        ys = []
        for time_value in xs:
            if module.FAULT_WINDOW[0] <= time_value <= module.FAULT_WINDOW[1]:
                ys.append(60.0)
            elif module.POSTFAULT_WINDOW[0] <= time_value <= module.POSTFAULT_WINDOW[1]:
                ys.append(280.0)
            elif module.LATE_RECOVERY_WINDOW[0] <= time_value <= module.LATE_RECOVERY_WINDOW[1]:
                ys.append(290.0)
            else:
                ys.append(300.0)

        class FakeResult:
            def getPlots(self):
                return [{"key": "plot-0"}, {"key": "plot-1"}, {"key": "plot-2"}]

            def getPlotChannelNames(self, plot_index):
                if plot_index == 2:
                    return [module.VOLTAGE_TRACE_NAME]
                return [f"other-{plot_index}:0"]

            def getPlotChannelData(self, plot_index, trace_name):
                assert plot_index == 2
                assert trace_name == module.VOLTAGE_TRACE_NAME
                return {"x": xs, "y": ys}

        metrics = module.extract_voltage_recovery_metrics(FakeResult())

        assert metrics["plot_index"] == 2
        assert metrics["point_count"] == len(xs)
        assert metrics["time_step"] == pytest.approx(0.01)
        assert metrics["prefault_rms"] == pytest.approx(300.0)
        assert metrics["fault_rms"] == pytest.approx(60.0)
        assert metrics["postfault_rms"] == pytest.approx(280.0)
        assert metrics["late_recovery_rms"] == pytest.approx(290.0)

    def test_build_summary_rows_formats_deltas_against_baseline(self):
        module = load_module(
            EMT_FAULT_STUDY_PATH,
            "emt_fault_study_example_summary",
        )

        rows = module.build_summary_rows(
            [
                {
                    "name": "baseline",
                    "description": "基线故障",
                    "fault_end_time": "2.7",
                    "fault_chg": "0.01",
                    "metrics": {
                        "point_count": 20001,
                        "prefault_rms": 302.467,
                        "fault_rms": 62.926,
                        "postfault_rms": 292.651,
                        "late_recovery_rms": 295.189,
                    },
                },
                {
                    "name": "delayed_clearing",
                    "description": "延长切除",
                    "fault_end_time": "2.9",
                    "fault_chg": "0.01",
                    "metrics": {
                        "point_count": 20001,
                        "prefault_rms": 302.467,
                        "fault_rms": 62.926,
                        "postfault_rms": 280.139,
                        "late_recovery_rms": 277.356,
                    },
                },
            ]
        )

        assert rows[0]["scenario"] == "baseline"
        assert rows[0]["fault_rms"] == "62.926"
        assert rows[0]["fault_drop_vs_prefault"] == "239.541"
        assert rows[0]["postfault_gap_vs_prefault"] == "9.816"
        assert rows[0]["delta_fault_rms_vs_baseline"] == "0.000"
        assert rows[0]["observation"] == "reference"
        assert rows[1]["scenario"] == "delayed_clearing"
        assert rows[1]["postfault_rms"] == "280.139"
        assert rows[1]["late_recovery_gap_vs_prefault"] == "25.111"
        assert rows[1]["delta_postfault_rms_vs_baseline"] == "-12.512"
        assert rows[1]["observation"] == "same fault depth, weaker post-fault recovery"

    def test_parse_args_supports_source_and_csv_export(self):
        module = load_module(
            EMT_FAULT_STUDY_PATH,
            "emt_fault_study_example_args",
        )

        source, csv_path, waveform_csv_path, waveform_window, conclusion_path = module.parse_args(
            [
                "examples/basic/ieee3-emt-prepared.yaml",
                "--csv=study-summary.csv",
                "--waveform-csv=study-waveforms.csv",
                "--waveform-window=2.4,3.0",
                "--conclusion-txt=study-conclusions.txt",
            ]
        )

        assert source == "examples/basic/ieee3-emt-prepared.yaml"
        assert csv_path == "study-summary.csv"
        assert waveform_csv_path == "study-waveforms.csv"
        assert waveform_window == (2.4, 3.0)
        assert conclusion_path == "study-conclusions.txt"

    def test_export_summary_rows_csv_writes_fault_study_table(self, tmp_path):
        module = load_module(
            EMT_FAULT_STUDY_PATH,
            "emt_fault_study_example_csv",
        )
        export_path = tmp_path / "emt-fault-study.csv"
        rows = [
            {
                "scenario": "baseline",
                "description": "基线故障",
                "fault_end_time": "2.7",
                "fault_chg": "0.01",
                "point_count": "20001",
                "prefault_rms": "302.467",
                "fault_rms": "62.926",
                "postfault_rms": "292.651",
                "late_recovery_rms": "295.189",
                "fault_drop_vs_prefault": "239.541",
                "postfault_gap_vs_prefault": "9.816",
                "late_recovery_gap_vs_prefault": "7.278",
                "delta_fault_rms_vs_baseline": "0.000",
                "delta_postfault_rms_vs_baseline": "0.000",
                "observation": "reference",
            },
            {
                "scenario": "mild_fault",
                "description": "较轻故障",
                "fault_end_time": "2.7",
                "fault_chg": "1e4",
                "point_count": "20001",
                "prefault_rms": "302.467",
                "fault_rms": "294.717",
                "postfault_rms": "301.931",
                "late_recovery_rms": "302.056",
                "fault_drop_vs_prefault": "7.750",
                "postfault_gap_vs_prefault": "0.536",
                "late_recovery_gap_vs_prefault": "0.411",
                "delta_fault_rms_vs_baseline": "231.791",
                "delta_postfault_rms_vs_baseline": "9.280",
                "observation": "shallower sag, stronger post-fault recovery",
            },
        ]

        module.export_summary_rows_csv(rows, export_path)

        content = export_path.read_text(encoding="utf-8")
        assert "scenario,description,fault_end_time,fault_chg" in content
        assert "baseline,基线故障,2.7,0.01" in content
        assert "mild_fault,较轻故障,2.7,1e4" in content
        assert "fault_drop_vs_prefault" in content
        assert "shallower sag, stronger post-fault recovery" in content

    def test_export_waveform_comparison_csv_writes_aligned_trace_table(self, tmp_path):
        module = load_module(
            EMT_FAULT_STUDY_PATH,
            "emt_fault_study_example_waveform_csv",
        )
        export_path = tmp_path / "emt-fault-study-waveforms.csv"
        study_results = [
            {
                "name": "baseline",
                "metrics": {
                    "trace": {
                        "x": [2.40, 2.41, 2.42],
                        "y": [300.0, 280.0, 260.0],
                    }
                },
            },
            {
                "name": "delayed_clearing",
                "metrics": {
                    "trace": {
                        "x": [2.40, 2.41, 2.42],
                        "y": [300.0, 278.0, 250.0],
                    }
                },
            },
            {
                "name": "mild_fault",
                "metrics": {
                    "trace": {
                        "x": [2.40, 2.41, 2.42],
                        "y": [300.0, 295.0, 292.0],
                    }
                },
            },
        ]

        module.export_waveform_comparison_csv(study_results, export_path)

        content = export_path.read_text(encoding="utf-8")
        assert "time,baseline,delayed_clearing,mild_fault" in content
        assert "2.400000,300.000000,300.000000,300.000000" in content
        assert "2.420000,260.000000,250.000000,292.000000" in content

    def test_export_waveform_comparison_window_csv_filters_time_range(self, tmp_path):
        module = load_module(
            EMT_FAULT_STUDY_PATH,
            "emt_fault_study_example_waveform_window_csv",
        )
        export_path = tmp_path / "emt-fault-study-waveforms-window.csv"
        study_results = [
            {
                "name": "baseline",
                "metrics": {"trace": {"x": [2.39, 2.40, 2.41, 2.42], "y": [1.0, 2.0, 3.0, 4.0]}},
            },
            {
                "name": "delayed_clearing",
                "metrics": {"trace": {"x": [2.39, 2.40, 2.41, 2.42], "y": [1.5, 2.5, 3.5, 4.5]}},
            },
        ]

        module.export_waveform_comparison_window_csv(
            study_results,
            export_path,
            time_window=(2.40, 2.41),
        )

        content = export_path.read_text(encoding="utf-8")
        assert "2.390000" not in content
        assert "2.420000" not in content
        assert "2.400000,2.000000,2.500000" in content
        assert "2.410000,3.000000,3.500000" in content

    def test_resolve_export_paths_binds_summary_and_waveform_to_same_prefix(self):
        module = load_module(
            EMT_FAULT_STUDY_PATH,
            "emt_fault_study_example_paths",
        )

        summary_path, waveform_path = module.resolve_export_paths(
            csv_path="reports/study-a-summary.csv",
            waveform_csv_path=None,
        )
        summary_path_2, waveform_path_2 = module.resolve_export_paths(
            csv_path=None,
            waveform_csv_path="reports/study-b-waveforms.csv",
        )
        summary_default, waveform_default = module.resolve_export_paths()

        assert summary_path == "reports/study-a-summary.csv"
        assert waveform_path == "reports/study-a-waveforms.csv"
        assert summary_path_2 == "reports/study-b-summary.csv"
        assert waveform_path_2 == "reports/study-b-waveforms.csv"
        assert summary_default == module.DEFAULT_EXPORT_PATH
        assert waveform_default == module.DEFAULT_WAVEFORM_EXPORT_PATH

    def test_build_conclusion_report_turns_metrics_into_supported_findings(self):
        module = load_module(
            EMT_FAULT_STUDY_PATH,
            "emt_fault_study_example_conclusions",
        )
        rows = [
            {
                "scenario": "baseline",
                "fault_drop_vs_prefault": "239.535",
                "postfault_gap_vs_prefault": "9.778",
                "late_recovery_gap_vs_prefault": "7.225",
                "delta_fault_rms_vs_baseline": "0.000",
            },
            {
                "scenario": "delayed_clearing",
                "fault_drop_vs_prefault": "239.535",
                "postfault_gap_vs_prefault": "21.715",
                "late_recovery_gap_vs_prefault": "24.942",
                "delta_fault_rms_vs_baseline": "0.000",
            },
            {
                "scenario": "mild_fault",
                "fault_drop_vs_prefault": "7.750",
                "postfault_gap_vs_prefault": "0.537",
                "late_recovery_gap_vs_prefault": "0.411",
                "delta_fault_rms_vs_baseline": "231.785",
            },
        ]

        report = module.build_conclusion_report(rows)
        text = module.format_conclusion_report(report)

        assert report["findings"][0]["supported"] is True
        assert report["findings"][1]["supported"] is True
        assert "研究问题:" in text
        assert "研究结论:" in text
        assert "[成立] 延迟切除主要恶化故障后恢复，而不是改变故障深度" in text
        assert "总体结论:" in text

    def test_resolve_conclusion_path_follows_study_prefix(self):
        module = load_module(
            EMT_FAULT_STUDY_PATH,
            "emt_fault_study_example_conclusion_path",
        )

        derived = module.resolve_conclusion_path(
            csv_path="reports/case-a-summary.csv",
            waveform_csv_path=None,
            conclusion_path=None,
        )
        explicit = module.resolve_conclusion_path(
            csv_path="reports/case-a-summary.csv",
            waveform_csv_path=None,
            conclusion_path="reports/custom.txt",
        )

        assert derived == "reports/case-a-conclusions.txt"
        assert explicit == "reports/custom.txt"


class TestEMTFaultSeverityScanExample:
    def test_load_model_from_source_reads_local_yaml(self, tmp_path):
        module = load_module(
            EMT_FAULT_SEVERITY_SCAN_PATH,
            "emt_fault_severity_scan_example",
        )
        export_path = tmp_path / "local-emt-scan-model.yaml"

        Model.dump(build_local_model(), str(export_path), compress=None)
        loaded_model = module.load_model_from_source(str(export_path))

        assert loaded_model.name == "local-example-model"
        assert loaded_model.rid == "model/test/local-example-model"

    def test_build_conclusion_report_detects_monotonic_scan(self):
        module = load_module(
            EMT_FAULT_SEVERITY_SCAN_PATH,
            "emt_fault_severity_scan_example_conclusion",
        )
        rows = [
            {
                "scenario": "severe_fault",
                "fault_drop_vs_prefault": "239.535",
                "postfault_gap_vs_prefault": "9.778",
                "late_recovery_gap_vs_prefault": "7.225",
            },
            {
                "scenario": "intermediate_fault",
                "fault_drop_vs_prefault": "210.131",
                "postfault_gap_vs_prefault": "9.451",
                "late_recovery_gap_vs_prefault": "9.000",
            },
            {
                "scenario": "mild_fault",
                "fault_drop_vs_prefault": "7.750",
                "postfault_gap_vs_prefault": "0.537",
                "late_recovery_gap_vs_prefault": "0.411",
            },
        ]

        report = module.build_conclusion_report(rows)
        text = module.format_conclusion_report(report)

        assert all(item["supported"] for item in report["findings"])
        assert "[成立] 随着 chg 增大，故障期间电压跌落显著减轻" in text
        assert "总体结论:" in text

    def test_export_summary_rows_csv_writes_scan_table(self, tmp_path):
        module = load_module(
            EMT_FAULT_SEVERITY_SCAN_PATH,
            "emt_fault_severity_scan_example_csv",
        )
        export_path = tmp_path / "emt-fault-severity-scan.csv"
        rows = [
            {
                "scenario": "severe_fault",
                "description": "强故障近似: chg=1e-2",
                "fault_chg": "1e-2",
                "prefault_rms": "302.467",
                "fault_rms": "62.932",
                "postfault_rms": "292.689",
                "late_recovery_rms": "295.243",
                "fault_drop_vs_prefault": "239.535",
                "postfault_gap_vs_prefault": "9.778",
                "late_recovery_gap_vs_prefault": "7.225",
            }
        ]

        module.export_summary_rows_csv(rows, export_path)

        content = export_path.read_text(encoding="utf-8")
        assert "scenario,description,fault_chg" in content
        assert "severe_fault,强故障近似: chg=1e-2,1e-2" in content

    def test_parse_args_supports_csv_and_conclusion_paths(self):
        module = load_module(
            EMT_FAULT_SEVERITY_SCAN_PATH,
            "emt_fault_severity_scan_example_args",
        )

        source, csv_path, conclusion_path = module.parse_args(
            [
                "examples/basic/ieee3-emt-prepared.yaml",
                "--csv=scan.csv",
                "--conclusion-txt=scan.txt",
            ]
        )

        assert source == "examples/basic/ieee3-emt-prepared.yaml"
        assert csv_path == "scan.csv"
        assert conclusion_path == "scan.txt"


class TestEMTFaultClearingScanExample:
    def test_load_model_from_source_reads_local_yaml(self, tmp_path):
        module = load_module(
            EMT_FAULT_CLEARING_SCAN_PATH,
            "emt_fault_clearing_scan_example",
        )
        export_path = tmp_path / "local-emt-clearing-scan-model.yaml"

        Model.dump(build_local_model(), str(export_path), compress=None)
        loaded_model = module.load_model_from_source(str(export_path))

        assert loaded_model.name == "local-example-model"
        assert loaded_model.rid == "model/test/local-example-model"

    def test_build_conclusion_report_detects_monotonic_fixed_deadline_gaps(self):
        module = load_module(
            EMT_FAULT_CLEARING_SCAN_PATH,
            "emt_fault_clearing_scan_example_conclusion",
        )
        rows = [
            {"scenario": "fe_270", "fault_end_time": "2.70", "gap_295": "8.418", "gap_300": "5.754"},
            {"scenario": "fe_275", "fault_end_time": "2.75", "gap_295": "12.770", "gap_300": "8.890"},
            {"scenario": "fe_280", "fault_end_time": "2.80", "gap_295": "17.766", "gap_300": "12.987"},
            {"scenario": "fe_285", "fault_end_time": "2.85", "gap_295": "22.674", "gap_300": "17.833"},
            {"scenario": "fe_290", "fault_end_time": "2.90", "gap_295": "25.669", "gap_300": "22.607"},
        ]

        report = module.build_conclusion_report(rows)
        text = module.format_conclusion_report(report)

        assert all(item["supported"] for item in report["findings"])
        assert "[成立] 在固定 2.95s 评估时点，延迟清除会系统性放大恢复缺口" in text
        assert "总体结论:" in text

    def test_export_summary_rows_csv_writes_clearing_scan_table(self, tmp_path):
        module = load_module(
            EMT_FAULT_CLEARING_SCAN_PATH,
            "emt_fault_clearing_scan_example_csv",
        )
        export_path = tmp_path / "emt-fault-clearing-scan.csv"
        rows = [
            {
                "scenario": "fe_270",
                "fault_end_time": "2.70",
                "prefault_rms": "302.467",
                "postfault_rms": "292.689",
                "late_recovery_rms": "295.243",
                "gap_295": "8.418",
                "gap_300": "5.754",
            }
        ]

        module.export_summary_rows_csv(rows, export_path)

        content = export_path.read_text(encoding="utf-8")
        assert "scenario,fault_end_time,prefault_rms,postfault_rms,late_recovery_rms,gap_295,gap_300" in content
        assert "fe_270,2.70,302.467,292.689,295.243,8.418,5.754" in content

    def test_parse_args_supports_csv_and_conclusion_paths(self):
        module = load_module(
            EMT_FAULT_CLEARING_SCAN_PATH,
            "emt_fault_clearing_scan_example_args",
        )

        source, csv_path, conclusion_path = module.parse_args(
            [
                "examples/basic/ieee3-emt-prepared.yaml",
                "--csv=clearing.csv",
                "--conclusion-txt=clearing.txt",
            ]
        )

        assert source == "examples/basic/ieee3-emt-prepared.yaml"
        assert csv_path == "clearing.csv"
        assert conclusion_path == "clearing.txt"


class TestEMTMeasurementWorkflowExample:
    def test_load_model_from_source_reads_local_yaml(self, tmp_path):
        module = load_module(
            EMT_MEASUREMENT_WORKFLOW_PATH,
            "emt_measurement_workflow_example",
        )
        export_path = tmp_path / "local-emt-measurement-model.yaml"

        Model.dump(build_local_model(), str(export_path), compress=None)
        loaded_model = module.load_model_from_source(str(export_path))

        assert loaded_model.name == "local-example-model"
        assert loaded_model.rid == "model/test/local-example-model"

    def test_build_conclusion_report_covers_add_delete_and_use_actions(self):
        module = load_module(
            EMT_MEASUREMENT_WORKFLOW_PATH,
            "emt_measurement_workflow_example_conclusion",
        )
        summary = {
            "bus7_prefault_rms": 302.467,
            "bus7_fault_rms": 62.932,
            "bus7_postfault_rms": 292.689,
            "bus2_prefault_rms": 115.000,
            "bus2_fault_rms": 109.500,
            "bus2_postfault_rms": 114.700,
            "bus2_expected_rms": 114.500,
            "retained_p_channels": ["#P2:0", "#P1:0", "#P3:0"],
            "p1_prefault_value": 123.456,
            "p1_prefault_avg": 79.500,
            "p1_fault_avg": 129.100,
            "p1_postfault_avg": 51.800,
        }

        report = module.build_conclusion_report(summary)
        text = module.format_conclusion_report(report)

        assert all(item["supported"] for item in report["findings"])
        assert "[成立] 新增 Bus2 电压测点成功进入 EMT 输出链" in text
        assert "[成立] 删除不需要的无功输出后，PQ 组只保留有功通道" in text
        assert "[成立] 故障局部母线 Bus7 的电压跌落显著重于远端 Bus2" in text
        assert "[成立] 保留下来的 #P1 通道能够揭示故障期间功率响应和故障后回落" in text
        assert "#P1 avg 79.500 -> 129.100 -> 51.800" in text

    def test_export_summary_rows_csv_writes_measurement_workflow_table(self, tmp_path):
        module = load_module(
            EMT_MEASUREMENT_WORKFLOW_PATH,
            "emt_measurement_workflow_example_csv",
        )
        export_path = tmp_path / "emt-measurement-workflow.csv"
        rows = [
            {
                "action": "add_measurement",
                "target": "Bus2 bus2_added:0",
                "value": "drop 5.500",
                "criterion": "expected prefault RMS 114.500",
            },
            {
                "action": "delete_unneeded_outputs",
                "target": "PQ group keep #P only",
                "value": "#P2:0,#P1:0,#P3:0",
                "criterion": "#Q channels removed",
            },
        ]

        module.export_summary_rows_csv(rows, export_path)

        content = export_path.read_text(encoding="utf-8")
        assert "action,target,value,criterion" in content
        assert "add_measurement,Bus2 bus2_added:0,drop 5.500,expected prefault RMS 114.500" in content
        assert "delete_unneeded_outputs,PQ group keep #P only,\"#P2:0,#P1:0,#P3:0\",#Q channels removed" in content

    def test_parse_args_supports_csv_and_conclusion_paths(self):
        module = load_module(
            EMT_MEASUREMENT_WORKFLOW_PATH,
            "emt_measurement_workflow_example_args",
        )

        source, csv_path, conclusion_path = module.parse_args(
            [
                "examples/basic/ieee3-emt-prepared.yaml",
                "--csv=measurement.csv",
                "--conclusion-txt=measurement.txt",
            ]
        )

        assert source == "examples/basic/ieee3-emt-prepared.yaml"
        assert csv_path == "measurement.csv"
        assert conclusion_path == "measurement.txt"


class TestEMTN1SecurityScreeningExample:
    def test_load_model_from_source_reads_local_yaml(self, tmp_path):
        module = load_module(
            EMT_N1_SECURITY_SCREENING_PATH,
            "emt_n1_security_screening_example",
        )
        export_path = tmp_path / "local-emt-n1-model.yaml"

        Model.dump(build_local_n1_model(), str(export_path), compress=None)
        loaded_model = module.load_model_from_source(str(export_path))

        assert loaded_model.name == "local-n1-model"
        assert loaded_model.rid == "model/test/local-n1-model"

    def test_choose_candidate_branch_ids_supports_subset_lines_only_and_limit(self):
        module = load_module(
            EMT_N1_SECURITY_SCREENING_PATH,
            "emt_n1_security_screening_example_candidates",
        )
        model = build_local_n1_model()

        original_default_branch_ids = list(module.DEFAULT_VALIDATED_BRANCH_IDS)
        module.DEFAULT_VALIDATED_BRANCH_IDS = ["transformer_a", "line_b", "missing_branch", "line_a"]
        try:
            discovered = module.choose_candidate_branch_ids(model)
            lines_only = module.choose_candidate_branch_ids(
                model,
                include_transformers=False,
            )
            validated = module.choose_candidate_branch_ids(
                model,
                use_all_discovered=False,
                limit=2,
            )
        finally:
            module.DEFAULT_VALIDATED_BRANCH_IDS = original_default_branch_ids

        assert discovered == ["line_a", "line_b", "transformer_a"]
        assert lines_only == ["line_a", "line_b"]
        assert validated == ["transformer_a", "line_b"]

    def test_rank_n1_security_results_prioritizes_support_loss_then_recovery_gap(self):
        module = load_module(
            EMT_N1_SECURITY_SCREENING_PATH,
            "emt_n1_security_screening_example_rank",
        )

        ranked = module.rank_n1_security_results(
            [
                {
                    "branch_id": "line-light",
                    "generator_support_lost": False,
                    "worst_postfault_gap": 0.8,
                    "worst_late_gap": 0.1,
                    "monitored_buses": {
                        "Bus7": {"postfault_gap_vs_prefault": 0.8},
                        "Bus2": {"postfault_gap_vs_prefault": 0.0},
                        "Bus8": {"postfault_gap_vs_prefault": 0.8},
                    },
                },
                {
                    "branch_id": "line-heavy",
                    "generator_support_lost": False,
                    "worst_postfault_gap": 10.1,
                    "worst_late_gap": 7.2,
                    "monitored_buses": {
                        "Bus7": {"postfault_gap_vs_prefault": 9.9},
                        "Bus2": {"postfault_gap_vs_prefault": 0.2},
                        "Bus8": {"postfault_gap_vs_prefault": 10.1},
                    },
                },
                {
                    "branch_id": "xf-support-loss",
                    "generator_support_lost": True,
                    "worst_postfault_gap": 11.7,
                    "worst_late_gap": 8.1,
                    "monitored_buses": {
                        "Bus7": {"postfault_gap_vs_prefault": 11.2},
                        "Bus2": {"postfault_gap_vs_prefault": 0.3},
                        "Bus8": {"postfault_gap_vs_prefault": 11.7},
                    },
                },
            ]
        )

        assert [item["branch_id"] for item in ranked] == [
            "xf-support-loss",
            "line-heavy",
            "line-light",
        ]
        assert module.classify_n1_security_severity(ranked[0]) == "critical"
        assert module.classify_n1_security_severity(ranked[1]) == "warning"
        assert module.classify_n1_security_severity(ranked[2]) == "observe"

    def test_build_summary_rows_and_digest_capture_baseline_deltas(self):
        module = load_module(
            EMT_N1_SECURITY_SCREENING_PATH,
            "emt_n1_security_screening_example_summary",
        )
        baseline = {
            "worst_postfault_gap": 10.349,
            "worst_late_gap": 7.622,
        }
        results = [
            {
                "branch_id": "xf-1",
                "branch_name": "Trans1",
                "branch_kind": "transformer",
                "severity": "critical",
                "rank": 1,
                "generator_support_lost": True,
                "monitored_buses": {
                    "Bus7": {
                        "postfault_gap_vs_prefault": 11.213,
                        "late_recovery_gap_vs_prefault": 7.751,
                    },
                    "Bus2": {
                        "postfault_gap_vs_prefault": 0.358,
                    },
                    "Bus8": {
                        "postfault_gap_vs_prefault": 11.739,
                        "late_recovery_gap_vs_prefault": 8.159,
                    },
                },
                "worst_postfault_gap": 11.739,
                "worst_late_gap": 8.159,
                "delta_worst_postfault_gap_vs_baseline": 1.390,
                "delta_worst_late_gap_vs_baseline": 0.537,
                "p1_metrics": {
                    "prefault_avg": 0.0,
                    "fault_avg": 0.0,
                    "postfault_avg": 0.0,
                },
            },
            {
                "branch_id": "line-6",
                "branch_name": "tline6",
                "branch_kind": "line",
                "severity": "observe",
                "rank": 2,
                "generator_support_lost": False,
                "monitored_buses": {
                    "Bus7": {
                        "postfault_gap_vs_prefault": 0.808,
                        "late_recovery_gap_vs_prefault": -0.190,
                    },
                    "Bus2": {
                        "postfault_gap_vs_prefault": -0.053,
                    },
                    "Bus8": {
                        "postfault_gap_vs_prefault": 0.819,
                        "late_recovery_gap_vs_prefault": -2.526,
                    },
                },
                "worst_postfault_gap": 0.819,
                "worst_late_gap": -0.190,
                "delta_worst_postfault_gap_vs_baseline": -9.530,
                "delta_worst_late_gap_vs_baseline": -7.812,
                "p1_metrics": {
                    "prefault_avg": 79.6,
                    "fault_avg": 108.4,
                    "postfault_avg": 63.5,
                },
            },
        ]

        rows = module.build_summary_rows(baseline, results)
        digest = module.build_screening_digest(baseline, results)

        assert rows[0]["generator_support_lost"] == "yes"
        assert rows[0]["delta_worst_postfault_gap_vs_baseline"] == "+1.390"
        assert rows[1]["delta_worst_postfault_gap_vs_baseline"] == "-9.530"
        assert rows[1]["baseline_worst_postfault_gap"] == "10.349"
        assert digest["top_case"]["branch_id"] == "xf-1"
        assert digest["top_line_case"]["branch_id"] == "line-6"
        assert digest["top_transformer_case"]["branch_id"] == "xf-1"
        assert digest["largest_worsening_case"]["branch_id"] == "xf-1"
        assert digest["mildest_case"]["branch_id"] == "line-6"
        assert digest["max_bus2_gap"] == 0.358

    def test_build_conclusion_report_formats_supported_findings(self):
        module = load_module(
            EMT_N1_SECURITY_SCREENING_PATH,
            "emt_n1_security_screening_example_conclusion",
        )
        baseline = {
            "worst_postfault_gap": 10.349,
            "worst_late_gap": 7.622,
        }
        results = [
            {
                "branch_id": "xf-1",
                "branch_name": "Trans1",
                "branch_kind": "transformer",
                "severity": "critical",
                "rank": 1,
                "generator_support_lost": True,
                "worst_postfault_gap": 11.739,
                "worst_late_gap": 8.159,
                "delta_worst_postfault_gap_vs_baseline": 1.390,
                "delta_worst_late_gap_vs_baseline": 0.537,
                "monitored_buses": {
                    "Bus7": {"postfault_gap_vs_prefault": 11.213},
                    "Bus2": {"postfault_gap_vs_prefault": 0.358},
                    "Bus8": {"postfault_gap_vs_prefault": 11.739},
                },
                "p1_metrics": {"prefault_avg": 0.0, "fault_avg": 0.0, "postfault_avg": 0.0},
            },
            {
                "branch_id": "line-4",
                "branch_name": "tline4",
                "branch_kind": "line",
                "severity": "warning",
                "rank": 2,
                "generator_support_lost": False,
                "worst_postfault_gap": 10.081,
                "worst_late_gap": 7.223,
                "delta_worst_postfault_gap_vs_baseline": -0.268,
                "delta_worst_late_gap_vs_baseline": -0.399,
                "monitored_buses": {
                    "Bus7": {"postfault_gap_vs_prefault": 9.927},
                    "Bus2": {"postfault_gap_vs_prefault": 0.264},
                    "Bus8": {"postfault_gap_vs_prefault": 10.081},
                },
                "p1_metrics": {"prefault_avg": 120.6, "fault_avg": 157.9, "postfault_avg": 115.2},
            },
            {
                "branch_id": "line-6",
                "branch_name": "tline6",
                "branch_kind": "line",
                "severity": "observe",
                "rank": 3,
                "generator_support_lost": False,
                "worst_postfault_gap": 0.819,
                "worst_late_gap": -0.190,
                "delta_worst_postfault_gap_vs_baseline": -9.530,
                "delta_worst_late_gap_vs_baseline": -7.812,
                "monitored_buses": {
                    "Bus7": {"postfault_gap_vs_prefault": 0.808},
                    "Bus2": {"postfault_gap_vs_prefault": -0.053},
                    "Bus8": {"postfault_gap_vs_prefault": 0.819},
                },
                "p1_metrics": {"prefault_avg": 79.6, "fault_avg": 108.4, "postfault_avg": 63.5},
            },
        ]
        digest = module.build_screening_digest(baseline, results)

        report = module.build_conclusion_report(baseline, results, digest)
        formatted = module.format_conclusion_report(report)

        assert all(item["supported"] for item in report["findings"])
        assert "Trans1 是当前扫描里最不安全的 N-1 工况" in formatted
        assert "tline6 是当前扫描里最轻的 N-1 工况" in formatted
        assert "Bus2" in formatted

    def test_parse_args_supports_subset_lines_only_and_paths(self):
        module = load_module(
            EMT_N1_SECURITY_SCREENING_PATH,
            "emt_n1_security_screening_example_args",
        )

        (
            source,
            csv_path,
            conclusion_path,
            use_all_discovered,
            include_transformers,
            limit,
        ) = module.parse_args(
            [
                "examples/basic/ieee3-emt-prepared.yaml",
                "--csv=n1.csv",
                "--conclusion-txt=n1.txt",
                "--validated-subset",
                "--lines-only",
                "--limit=3",
            ]
        )

        assert source == "examples/basic/ieee3-emt-prepared.yaml"
        assert csv_path == "n1.csv"
        assert conclusion_path == "n1.txt"
        assert not use_all_discovered
        assert not include_transformers
        assert limit == 3


class TestEMTResearchReportExample:
    def test_parse_args_supports_report_path(self):
        module = load_module(
            EMT_RESEARCH_REPORT_PATH,
            "emt_research_report_example_args",
        )

        source, report_path = module.parse_args(
            [
                "examples/basic/ieee3-emt-prepared.yaml",
                "--report=emt-report.md",
            ]
        )

        assert source == "examples/basic/ieee3-emt-prepared.yaml"
        assert report_path == "emt-report.md"

    def test_markdown_table_formats_rows(self):
        module = load_module(
            EMT_RESEARCH_REPORT_PATH,
            "emt_research_report_example_table",
        )

        table = module.markdown_table(
            [
                {"scenario": "baseline", "fault_rms": "62.932"},
                {"scenario": "mild_fault", "fault_rms": "294.717"},
            ]
        )

        assert "| scenario | fault_rms |" in table
        assert "| baseline | 62.932 |" in table
        assert "| mild_fault | 294.717 |" in table

    def test_build_markdown_report_contains_all_sections(self):
        module = load_module(
            EMT_RESEARCH_REPORT_PATH,
            "emt_research_report_example_report",
        )
        sections = {
            "fault_study": {
                "rows": [{"scenario": "baseline", "fault_rms": "62.932"}],
                "report": {
                    "research_question": "Q1",
                    "criteria": ["C1"],
                    "findings": [{"title": "F1", "supported": True, "evidence": "E1"}],
                    "overall_conclusion": "O1",
                    "boundary": "B1",
                },
            },
            "fault_clearing_scan": {
                "rows": [{"scenario": "fe_270", "gap_295": "8.418"}],
                "report": {
                    "research_question": "Q2",
                    "criteria": ["C2"],
                    "findings": [{"title": "F2", "supported": True, "evidence": "E2"}],
                    "overall_conclusion": "O2",
                    "boundary": "B2",
                },
            },
            "fault_severity_scan": {
                "rows": [{"scenario": "severe_fault", "fault_drop_vs_prefault": "239.535"}],
                "report": {
                    "research_question": "Q3",
                    "criteria": ["C3"],
                    "findings": [{"title": "F3", "supported": True, "evidence": "E3"}],
                    "overall_conclusion": "O3",
                    "boundary": "B3",
                },
            },
            "measurement_workflow": {
                "rows": [{"action": "add_measurement", "target": "Bus2"}],
                "report": {
                    "research_question": "Q4",
                    "criteria": ["C4"],
                    "findings": [{"title": "F4", "supported": True, "evidence": "E4"}],
                    "overall_conclusion": "O4",
                    "boundary": "B4",
                },
            },
        }

        report_text = module.build_markdown_report("model/holdme/IEEE3", sections)

        assert "# CloudPSS EMT Research Report" in report_text
        assert "## Fault Study Comparison" in report_text
        assert "## Fault Clearing Scan" in report_text
        assert "## Fault Severity Scan" in report_text
        assert "## Measurement Workflow" in report_text
        assert "Model: `model/holdme/IEEE3`" in report_text

    def test_export_report_writes_markdown_file(self, tmp_path):
        module = load_module(
            EMT_RESEARCH_REPORT_PATH,
            "emt_research_report_example_export",
        )
        export_path = tmp_path / "emt-report.md"

        module.export_report("# Report", export_path)

        assert export_path.read_text(encoding="utf-8") == "# Report\n"


class TestEMTN1SecurityReportExample:
    def test_parse_args_supports_report_scope_and_limit(self):
        module = load_module(
            EMT_N1_SECURITY_REPORT_PATH,
            "emt_n1_security_report_example_args",
        )

        source, report_path, use_all_discovered, include_transformers, limit = module.parse_args(
            [
                "examples/basic/ieee3-emt-prepared.yaml",
                "--report=n1-report.md",
                "--all-discovered",
                "--lines-only",
                "--limit=4",
            ]
        )

        assert source == "examples/basic/ieee3-emt-prepared.yaml"
        assert report_path == "n1-report.md"
        assert use_all_discovered
        assert not include_transformers
        assert limit == 4

    def test_build_markdown_report_contains_expected_sections(self):
        module = load_module(
            EMT_N1_SECURITY_REPORT_PATH,
            "emt_n1_security_report_example_report",
        )
        sections = {
            "baseline": {
                "worst_postfault_gap": 10.349,
                "worst_late_gap": 7.622,
            },
            "baseline_rows": [
                {"bus": "Bus7", "postfault_gap": "9.778", "late_gap": "7.225"},
            ],
            "digest": {
                "total_cases": 3,
                "severity_counts": {"critical": 1, "warning": 1, "observe": 1},
            },
            "highlight_rows": [
                {
                    "label": "Top Case",
                    "branch_name": "Trans1",
                    "branch_kind": "transformer",
                    "severity": "critical",
                    "worst_postfault_gap": "11.739",
                    "worst_late_gap": "8.159",
                    "p1_postfault_avg": "0.000",
                }
            ],
            "summary_rows": [
                {
                    "rank": "1",
                    "branch_name": "Trans1",
                    "severity": "critical",
                }
            ],
            "conclusion_report": {
                "research_question": "Q",
                "criteria": ["C"],
                "findings": [{"title": "F", "supported": True, "evidence": "E"}],
                "overall_conclusion": "O",
                "boundary": "B",
            },
        }

        report_text = module.build_markdown_report(
            "model/holdme/IEEE3",
            sections,
            use_all_discovered=False,
        )

        assert "# CloudPSS EMT N-1 Security Report" in report_text
        assert "## Baseline Reference" in report_text
        assert "## Representative Cases" in report_text
        assert "## Ranked Screening Table" in report_text
        assert "## Conclusions" in report_text
        assert "validated representative IEEE3 N-1 subset" in report_text

    def test_export_report_writes_markdown_file(self, tmp_path):
        module = load_module(
            EMT_N1_SECURITY_REPORT_PATH,
            "emt_n1_security_report_example_export",
        )
        export_path = tmp_path / "emt-n1-report.md"

        module.export_report("# EMT N-1", export_path)

        assert export_path.read_text(encoding="utf-8") == "# EMT N-1\n"


class TestEMTN1FullReportExample:
    def test_parse_args_supports_lines_only_and_limit(self):
        module = load_module(
            EMT_N1_FULL_REPORT_PATH,
            "emt_n1_full_report_example_args",
        )

        source, report_path, include_transformers, limit = module.parse_args(
            [
                "examples/basic/ieee3-emt-prepared.yaml",
                "--report=n1-full.md",
                "--lines-only",
                "--limit=5",
            ]
        )

        assert source == "examples/basic/ieee3-emt-prepared.yaml"
        assert report_path == "n1-full.md"
        assert not include_transformers
        assert limit == 5

    def test_build_markdown_report_contains_full_scan_sections(self):
        module = load_module(
            EMT_N1_FULL_REPORT_PATH,
            "emt_n1_full_report_example_report",
        )
        sections = {
            "digest": {
                "total_cases": 9,
                "severity_counts": {"critical": 1, "warning": 2, "observe": 6},
            },
            "highlight_rows": [
                {
                    "label": "Top Case",
                    "branch_name": "Trans1",
                    "branch_kind": "transformer",
                    "severity": "critical",
                    "worst_postfault_gap": "11.739",
                    "worst_late_gap": "8.159",
                    "p1_postfault_avg": "0.000",
                }
            ],
            "top_rank_rows": [
                {
                    "rank": "1",
                    "branch_name": "Trans1",
                    "severity": "critical",
                }
            ],
            "summary_rows": [
                {
                    "rank": "1",
                    "branch_name": "Trans1",
                    "severity": "critical",
                },
                {
                    "rank": "2",
                    "branch_name": "tline4",
                    "severity": "warning",
                },
            ],
            "severity_rows": [
                {"severity": "critical", "count": "1"},
                {"severity": "warning", "count": "2"},
                {"severity": "observe", "count": "6"},
            ],
            "conclusion_report": {
                "research_question": "Q",
                "criteria": ["C"],
                "findings": [{"title": "F", "supported": True, "evidence": "E"}],
                "overall_conclusion": "O",
                "boundary": "B",
            },
        }

        report_text = module.build_markdown_report(
            "model/holdme/IEEE3",
            sections,
            include_transformers=True,
        )

        assert "# CloudPSS EMT N-1 Full Screening Report" in report_text
        assert "## Severity Distribution" in report_text
        assert "## Case Highlights" in report_text
        assert "## Top Ranked Cases" in report_text
        assert "## Full Ranked Table" in report_text
        assert "full discovered IEEE3 lines + transformers subset" in report_text

    def test_export_report_writes_markdown_file(self, tmp_path):
        module = load_module(
            EMT_N1_FULL_REPORT_PATH,
            "emt_n1_full_report_example_export",
        )
        export_path = tmp_path / "emt-n1-full-report.md"

        module.export_report("# EMT N-1 Full", export_path)

        assert export_path.read_text(encoding="utf-8") == "# EMT N-1 Full\n"


class TestDelayedExamples:
    def test_sfemt_describe_plot_prefers_key_over_name(self):
        module = load_module(RUN_SFEMT_PATH, "run_sfemt_simulation_example")

        label = module.describe_plot({"key": "plot-2", "name": "Legacy"}, 2)

        assert label == "plot-2"

    def test_ies_describe_plot_prefers_key_over_name(self):
        module = load_module(RUN_IES_PATH, "run_ies_simulation_example")

        label = module.describe_plot({"key": "plot-1", "name": "Legacy"}, 1)

        assert label == "plot-1"

    def test_ies_example_only_treats_sdk_supported_job_definition_rids_as_runnable(self):
        module = load_module(RUN_IES_PATH, "run_ies_simulation_jobs")
        model = build_local_model()
        model.jobs = [
            {"name": "legacy pf", "rid": "function/CloudPSS/ies-power-flow"},
            {"name": "supported pf", "rid": "job-definition/ies/ies-power-flow"},
            {"name": "emt", "rid": "function/CloudPSS/emtps"},
        ]

        supported_jobs = module.example_get_ies_jobs(model)

        assert [job["rid"] for job in supported_jobs] == [
            "job-definition/ies/ies-power-flow"
        ]
