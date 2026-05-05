"""Tests for CloudPSS static model inventory extraction."""

from cloudpss_skills_v2.powerapi.adapters.cloudpss.model_inventory import (
    CloudPSSInventoryExtractor,
    cloudpss_arg_value,
    first_present,
    parse_float,
)
from cloudpss_skills_v2.powerskill.model_handle import ComponentType


class FakeComponent:
    def __init__(self, definition, args, pins=None, name=None):
        self.definition = definition
        self.args = args
        self.pins = pins or {}
        self.name = name


class FakeModel:
    name = "inventory-case"
    rid = "rid-inventory"

    def getAllComponents(self):
        return {
            "bus_a": FakeComponent(
                "model/CloudPSS/_newBus_3p",
                {"VBase": {"source": "500"}, "Freq": {"value": "60"}},
                {"0": "node-a"},
                "Bus A",
            ),
            "line_ab": FakeComponent(
                "model/CloudPSS/TransmissionLine",
                {
                    "R1pu": {"source": "0.001"},
                    "X1pu": {"source": "0.01"},
                    "B1pu": {"source": "0.03"},
                    "Sbase": {"source": "100"},
                    "Vbase": {"source": "500"},
                    "Irated": {"source": "1.2"},
                    "Name": "Line A-B",
                },
            ),
            "xf_1": FakeComponent(
                "model/CloudPSS/_newTransformer_3p2w",
                {
                    "Rl": {"source": "0.002"},
                    "Xl": {"source": "0.08"},
                    "Tmva": {"source": "200"},
                    "V1": {"source": "500"},
                    "InitTap": {"source": "1.02"},
                },
            ),
            "load_1": FakeComponent(
                "model/CloudPSS/_newLoad",
                {"p": {"source": "80"}, "q": {"source": "20"}},
            ),
            "gen_1": FakeComponent(
                "model/CloudPSS/_newGenerator",
                {"pf_P": {"source": "120"}, "pf_Q": {"source": "12"}, "pf_V": {"source": "1.01"}},
            ),
            "shunt_1": FakeComponent(
                "model/CloudPSS/_newShunt",
                {"B": {"source": "-5"}},
            ),
            "other_1": FakeComponent("model/CloudPSS/Unknown", {"foo": "bar"}),
        }


def test_arg_helpers_preserve_cloudpss_wrappers_and_zero_values():
    assert cloudpss_arg_value({"source": "1.2"}) == "1.2"
    assert cloudpss_arg_value({"value": 3}) == 3
    assert cloudpss_arg_value(0) == 0
    assert first_present({"a": None, "b": 0, "c": 1}, "a", "b", "c") == 0
    assert parse_float("2.5") == 2.5
    assert parse_float("", None) is None
    assert parse_float("bad", 7.0) == 7.0


def test_inventory_extracts_component_types_parameters_and_indexes():
    inventory = CloudPSSInventoryExtractor().extract(FakeModel())

    assert inventory.model_name == "inventory-case"
    assert inventory.model_rid == "rid-inventory"
    assert inventory.component_type_counts() == {
        ComponentType.BUS: 1,
        ComponentType.BRANCH: 1,
        ComponentType.TRANSFORMER: 1,
        ComponentType.LOAD: 1,
        ComponentType.GENERATOR: 1,
        ComponentType.SHUNT: 1,
        ComponentType.OTHER: 1,
    }

    index = inventory.parameter_index()
    assert index["bus_by_component_id"]["bus_a"]["voltage_kv"] == 500.0
    assert index["bus_by_node_name"]["node-a"]["frequency_hz"] == 60.0
    assert index["branch_by_component_id"]["line_ab"]["r_pu"] == 0.001
    assert index["branch_by_component_id"]["line_ab"]["x_pu"] == 0.01
    assert index["branch_by_component_id"]["line_ab"]["b_pu"] == 0.03
    assert index["branch_by_component_id"]["line_ab"]["rate_a_mva"] > 1000
    assert index["branch_by_component_id"]["xf_1"]["branch_type"] == "transformer"
    assert index["branch_by_component_id"]["xf_1"]["tap_ratio"] == 1.02

    load = next(
        item for item in inventory.components if item.component_type == ComponentType.LOAD
    )
    generator = next(
        item for item in inventory.components if item.component_type == ComponentType.GENERATOR
    )
    shunt = next(
        item for item in inventory.components if item.component_type == ComponentType.SHUNT
    )
    assert load.extracted_parameters == {"p_mw": 80.0, "q_mvar": 20.0}
    assert generator.extracted_parameters == {
        "p_mw": 120.0,
        "q_mvar": 12.0,
        "v_set_pu": 1.01,
    }
    assert shunt.extracted_parameters == {"q_mvar": -5.0}


def test_inventory_diagnostics_report_static_parameter_gaps():
    class IncompleteModel:
        name = "incomplete"
        rid = "rid-incomplete"

        def getAllComponents(self):
            return {
                "bus_missing": FakeComponent("model/CloudPSS/_newBus_3p", {}),
                "line_missing": FakeComponent(
                    "model/CloudPSS/TransmissionLine",
                    {"R1pu": {"source": "0.01"}},
                ),
                "xf_missing": FakeComponent(
                    "model/CloudPSS/_newTransformer_3p2w",
                    {"Rl": {"source": "0.001"}},
                ),
            }

    diagnostics = CloudPSSInventoryExtractor().extract(IncompleteModel()).diagnostics()

    assert diagnostics["status"] == "warning"
    assert diagnostics["parameter_coverage"] == {
        "line_count": 1,
        "line_with_r_x_count": 0,
        "transformer_count": 1,
        "transformer_with_x_count": 0,
        "bus_count": 1,
        "bus_with_base_voltage_count": 0,
    }
    assert {
        finding["code"] for finding in diagnostics["findings"]
    } == {
        "missing_line_static_impedance",
        "missing_transformer_static_impedance",
        "missing_bus_base_voltage",
    }


def test_inventory_read_failure_is_reported_as_warning():
    class BrokenModel:
        def getAllComponents(self):
            raise RuntimeError("sdk unavailable")

    diagnostics = CloudPSSInventoryExtractor().extract(BrokenModel()).diagnostics()

    assert diagnostics["status"] == "warning"
    assert diagnostics["component_type_counts"] == {}
    assert diagnostics["findings"][0]["code"] == "component_read_failed"
