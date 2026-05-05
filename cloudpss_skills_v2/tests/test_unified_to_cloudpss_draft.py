"""Tests for unified PowerSystemModel to CloudPSS draft generation."""

from cloudpss_skills_v2.core.system_model import (
    Branch,
    Bus,
    Generator,
    Load,
    PowerSystemModel,
)
from cloudpss_skills_v2.powerapi.adapters.cloudpss.model_draft import (
    BUS_DEFINITION,
    GENERATOR_DEFINITION,
    LINE_DEFINITION,
    LOAD_DEFINITION,
    TRANSFORMER_DEFINITION,
    CloudPSSModelWriter,
    UnifiedToCloudPSSDraftConverter,
)
from cloudpss_skills_v2.powerapi.adapters.cloudpss.model_inventory import (
    CloudPSSInventoryExtractor,
)


def build_three_bus_model() -> PowerSystemModel:
    return PowerSystemModel(
        name="three-bus-cloudpss-draft",
        base_mva=100.0,
        frequency_hz=60.0,
        buses=[
            Bus(bus_id=1, name="Bus 1", base_kv=500.0, bus_type="SLACK"),
            Bus(bus_id=2, name="Bus 2", base_kv=500.0, bus_type="PQ"),
            Bus(bus_id=3, name="Bus 3", base_kv=230.0, bus_type="PV"),
        ],
        branches=[
            Branch(
                from_bus=1,
                to_bus=2,
                name="Line 1-2",
                branch_type="LINE",
                r_pu=0.001,
                x_pu=0.01,
                b_pu=0.03,
                rate_a_mva=300.0,
            ),
            Branch(
                from_bus=2,
                to_bus=3,
                name="Transformer 2-3",
                branch_type="TRANSFORMER",
                r_pu=0.002,
                x_pu=0.08,
                rate_a_mva=200.0,
                tap_ratio=1.02,
            ),
        ],
        loads=[
            Load(bus_id=2, name="Load @ Bus 2", p_mw=90.0, q_mvar=30.0),
        ],
        generators=[
            Generator(
                bus_id=1,
                name="Slack Gen",
                p_gen_mw=120.0,
                v_set_pu=1.0,
                p_min_mw=0.0,
                p_max_mw=200.0,
            ),
            Generator(
                bus_id=3,
                name="PV Gen",
                p_gen_mw=60.0,
                v_set_pu=1.01,
                p_min_mw=0.0,
                p_max_mw=100.0,
            ),
        ],
    )


class FakeCloudPSSComponent:
    def __init__(self, definition, label, args, pins, position):
        self.definition = definition
        self.label = label
        self.name = label
        self.args = args
        self.pins = pins
        self.position = position


class FakeCloudPSSModel:
    name = "fake-cloudpss-model"
    rid = "rid-fake-cloudpss-model"

    def __init__(self):
        self.components = {}

    def addComponent(self, definition, label, args, pins, position=None):
        key = f"component_{len(self.components) + 1}"
        self.components[key] = FakeCloudPSSComponent(
            definition,
            label,
            args,
            pins,
            position,
        )
        return key

    def getAllComponents(self):
        return self.components

    def removeComponent(self, component_key):
        if component_key not in self.components:
            return False
        del self.components[component_key]
        return True


def test_unified_model_converts_to_cloudpss_static_draft():
    draft = UnifiedToCloudPSSDraftConverter().convert(build_three_bus_model())

    assert draft.name == "three-bus-cloudpss-draft"
    assert draft.frequency_hz == 60.0
    assert draft.component_type_counts() == {
        BUS_DEFINITION: 3,
        LINE_DEFINITION: 1,
        TRANSFORMER_DEFINITION: 1,
        LOAD_DEFINITION: 1,
        GENERATOR_DEFINITION: 2,
    }

    bus = next(component for component in draft.components if component.label == "Bus 1")
    line = next(component for component in draft.components if component.label == "Line 1-2")
    transformer = next(
        component for component in draft.components if component.label == "Transformer 2-3"
    )
    load = next(component for component in draft.components if component.label == "Load @ Bus 2")
    generator = next(component for component in draft.components if component.label == "PV Gen")

    assert bus.args["VBase"]["source"] == "500.0"
    assert bus.args["Freq"] == "60.0"
    assert bus.pins["0"] == "node_1_bus_1"
    assert line.pins == {"0": "node_1_bus_1", "1": "node_2_bus_2"}
    assert line.args["R1pu"]["source"] == "0.001"
    assert line.args["X1pu"]["source"] == "0.01"
    assert line.args["B1pu"]["source"] == "0.03"
    assert line.args["Rate"]["source"] == "300.0"
    assert transformer.definition == TRANSFORMER_DEFINITION
    assert transformer.args["Xl"]["source"] == "0.08"
    assert transformer.args["InitTap"]["source"] == "1.02"
    assert load.pins == {"0": "node_2_bus_2"}
    assert load.args["p"]["source"] == "90.0"
    assert load.args["q"]["source"] == "30.0"
    assert load.args["v"]["source"] == "500.0"
    assert generator.pins == {"0": "node_3_bus_3"}
    assert generator.args["pf_P"]["source"] == "60.0"
    assert generator.args["pf_V"]["source"] == "1.01"
    assert generator.args["BusType"] == "1"


def test_writer_output_can_be_read_by_cloudpss_inventory_extractor():
    draft = UnifiedToCloudPSSDraftConverter().convert(build_three_bus_model())
    fake_model = FakeCloudPSSModel()

    created = CloudPSSModelWriter().write(fake_model, draft)
    inventory = CloudPSSInventoryExtractor().extract(fake_model)
    index = inventory.parameter_index()
    diagnostics = inventory.diagnostics()

    assert len(created) == len(draft.components)
    assert created[0]["sdk_component_key"] == "component_1"
    assert diagnostics["status"] == "pass"
    assert diagnostics["component_type_counts"] == {
        "bus": 3,
        "branch": 1,
        "transformer": 1,
        "load": 1,
        "generator": 2,
    }
    assert diagnostics["parameter_coverage"]["bus_with_base_voltage_count"] == 3
    assert diagnostics["parameter_coverage"]["line_with_r_x_count"] == 1
    assert diagnostics["parameter_coverage"]["transformer_with_x_count"] == 1
    assert index["bus_by_node_name"]["node_1_bus_1"]["frequency_hz"] == 60.0
    assert index["branch_by_component_id"]["component_4"]["x_pu"] == 0.01
    assert index["branch_by_component_id"]["component_5"]["branch_type"] == "transformer"
    assert index["branch_by_component_id"]["component_5"]["tap_ratio"] == 1.02
    load = next(item for item in inventory.components if item.component_type == "load")
    generator = next(
        item for item in inventory.components
        if item.component_type == "generator" and item.name == "PV Gen"
    )
    assert load.extracted_parameters["p_mw"] == 90.0
    assert generator.extracted_parameters["p_mw"] == 60.0
    assert generator.extracted_parameters["v_set_pu"] == 1.01


def test_writer_can_clear_existing_components_before_write():
    draft = UnifiedToCloudPSSDraftConverter().convert(build_three_bus_model())
    fake_model = FakeCloudPSSModel()
    fake_model.addComponent(
        BUS_DEFINITION,
        "Old Bus",
        {"Name": "old", "VBase": "10"},
        {"0": "old"},
    )

    created = CloudPSSModelWriter().write(fake_model, draft, clear_existing=True)
    inventory = CloudPSSInventoryExtractor().extract(fake_model)

    assert len(created) == len(draft.components)
    assert all(component.name != "Old Bus" for component in inventory.components)
    assert inventory.diagnostics()["component_type_counts"]["bus"] == 3


def test_inactive_components_are_reported_and_not_emitted():
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=1, name="Bus 1", base_kv=110.0, bus_type="SLACK"),
            Bus(bus_id=2, name="Bus 2", base_kv=110.0, bus_type="PQ"),
        ],
        branches=[
            Branch(
                from_bus=1,
                to_bus=2,
                name="Inactive Line",
                branch_type="LINE",
                x_pu=0.01,
                in_service=False,
            )
        ],
        loads=[Load(bus_id=2, name="Inactive Load", p_mw=1.0, in_service=False)],
        generators=[
            Generator(
                bus_id=1,
                name="Inactive Gen",
                p_gen_mw=0.0,
                p_min_mw=0.0,
                p_max_mw=1.0,
                in_service=False,
            )
        ],
    )

    draft = UnifiedToCloudPSSDraftConverter().convert(model)

    assert len(draft.components) == 2
    assert {warning["code"] for warning in draft.warnings} == {
        "skipped_inactive_branch",
        "skipped_inactive_load",
        "skipped_inactive_generator",
    }
