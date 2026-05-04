"""Regression tests for shared ModelHandle conversion."""

from __future__ import annotations

from cloudpss_skills_v2.poweranalysis.contingency_analysis import ContingencyAnalysis
from cloudpss_skills_v2.poweranalysis.n2_security import N2SecurityAnalysis
from cloudpss_skills_v2.poweranalysis.parameter_sensitivity import ParameterSensitivityAnalysis
from cloudpss_skills_v2.poweranalysis.voltage_stability import (
    VoltageStabilityAnalysis,
    VoltageStabilityAnalysisLegacy,
)
from cloudpss_skills_v2.powerapi.adapters.handle_converter import (
    convert_handle_to_power_system_model,
)
from cloudpss_skills_v2.powerskill import ComponentType


class FakeComponent:
    def __init__(self, key, name=None, args=None, properties=None):
        self.key = key
        self.name = name or key
        self.args = args
        self.properties = properties or {}


class FakeHandle:
    def __init__(self, by_type):
        self.by_type = by_type

    def get_components_by_type(self, component_type):
        return self.by_type.get(component_type, [])


def _handle_with_transformer():
    return FakeHandle(
        {
            ComponentType.BUS: [
                FakeComponent("bus:0", "Slack", args={"vn_kv": "230", "vm_pu": "1.02"}),
                FakeComponent("bus:1", "Load", args={"vn_kv": "115"}),
            ],
            ComponentType.SOURCE: [FakeComponent("source:0", args={"bus": "bus:0"})],
            ComponentType.BRANCH: [
                FakeComponent(
                    "line:0",
                    args={"from_bus": "bus:0", "to_bus": "bus:1", "r_pu": "0.02", "x_pu": "0.2"},
                )
            ],
            ComponentType.TRANSFORMER: [
                FakeComponent(
                    "trafo:0",
                    args={
                        "from_bus": "bus:0",
                        "to_bus": "bus:1",
                        "r_pu": "0.003",
                        "x_pu": "0.06",
                        "sn_mva": "50",
                        "tap_ratio": "1.05",
                        "shift_degree": "10",
                    },
                )
            ],
            ComponentType.LOAD: [FakeComponent("load:0", args={"bus": "bus:1", "p_mw": "40", "q_mvar": "8"})],
            ComponentType.GENERATOR: [FakeComponent("gen:0", args={"bus": "bus:0", "p_mw": "45"})],
            ComponentType.SHUNT: [FakeComponent("shunt:0", args={"bus": "bus:1", "q_mvar": "5"})],
        }
    )


def test_shared_converter_keeps_transformers_and_resolves_real_endpoints():
    model = convert_handle_to_power_system_model(_handle_with_transformer())

    assert [bus.bus_type for bus in model.buses] == ["SLACK", "PQ"]
    assert len(model.branches) == 2
    transformer = next(branch for branch in model.branches if branch.name == "trafo:0")
    assert transformer.branch_type == "TRANSFORMER"
    assert transformer.from_bus == 0
    assert transformer.to_bus == 1
    assert transformer.rate_a_mva == 50
    assert transformer.tap_ratio == 1.05
    assert transformer.phase_shift_degree == 10
    assert model.loads[0].bus_id == 1
    assert model.loads[1].name == "shunt:0"
    assert model.loads[1].q_mvar == -5
    assert model.generators[0].bus_id == 0


def test_shared_converter_prefers_args_and_falls_back_to_properties():
    handle = FakeHandle(
        {
            ComponentType.BUS: [
                FakeComponent("bus:0", args={"vn_kv": 220}),
                FakeComponent("bus:1", args={"vn_kv": 110}),
            ],
            ComponentType.SOURCE: [FakeComponent("source:0", args={"bus": 0})],
            ComponentType.BRANCH: [
                FakeComponent(
                    "line:args",
                    args={"from_bus": "bus:0", "to_bus": "bus:1", "r_pu": 0.02},
                    properties={"from_bus": "bus:1", "to_bus": "bus:0", "r_pu": 0.9},
                ),
                FakeComponent(
                    "line:props",
                    args={},
                    properties={"from_bus": "bus:1", "to_bus": "bus:0", "x_pu": 0.3},
                ),
            ],
        }
    )

    model = convert_handle_to_power_system_model(handle)

    by_name = {branch.name: branch for branch in model.branches}
    assert by_name["line:args"].from_bus == 0
    assert by_name["line:args"].to_bus == 1
    assert by_name["line:args"].r_pu == 0.02
    assert by_name["line:props"].from_bus == 1
    assert by_name["line:props"].to_bus == 0
    assert by_name["line:props"].x_pu == 0.3


def test_shared_converter_skips_invalid_topology_without_fabricating_endpoints():
    handle = FakeHandle(
        {
            ComponentType.BUS: [FakeComponent("bus:0"), FakeComponent("bus:1")],
            ComponentType.SOURCE: [FakeComponent("source:0", args={"bus": "bus:0"})],
            ComponentType.BRANCH: [
                FakeComponent("line:self", args={"from_bus": "bus:0", "to_bus": "bus:0"}),
                FakeComponent("line:missing", args={"from_bus": "bus:0", "to_bus": "bus:99"}),
            ],
            ComponentType.TRANSFORMER: [
                FakeComponent("trafo:missing", args={"from_bus": "", "to_bus": ""}),
            ],
        }
    )

    model = convert_handle_to_power_system_model(handle)

    assert len(model.buses) == 2
    assert model.branches == []


def test_all_poweranalysis_wrappers_delegate_to_shared_converter():
    handle = _handle_with_transformer()

    analyses = [
        ContingencyAnalysis(),
        N2SecurityAnalysis(),
        ParameterSensitivityAnalysis(),
        VoltageStabilityAnalysis(),
        VoltageStabilityAnalysisLegacy(),
    ]

    for analysis in analyses:
        model = analysis._convert_handle_to_model(handle)
        assert any(branch.branch_type == "TRANSFORMER" for branch in model.branches)
