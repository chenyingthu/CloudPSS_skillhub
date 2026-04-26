"""Engine-runnable golden benchmark cases.

These tests are intentionally separate from skill-level golden configs. Cases
in this lane must provide a repository model artifact and must be executed by
the declared engine adapter before comparing expected outputs.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from cloudpss_skills_v2.powerapi import SimulationStatus
from cloudpss_skills_v2.powerapi.adapters.pandapower import (
    PandapowerPowerFlowAdapter,
    PandapowerShortCircuitAdapter,
)


GOLDEN_ENGINE_CASE_DIR = Path(__file__).parent / "golden_engine_cases"


def _load_case(case_name: str) -> dict[str, Any]:
    return json.loads(
        (GOLDEN_ENGINE_CASE_DIR / f"{case_name}.json").read_text(encoding="utf-8")
    )


def _build_pandapower_net(model: dict[str, Any]):
    import pandapower as pp

    if model.get("format") != "pandapower_network_spec_v1":
        raise ValueError(f"unsupported model format: {model.get('format')}")

    net = pp.create_empty_network(sn_mva=float(model["sn_mva"]))
    bus_index: dict[str, int] = {}

    for bus in model["buses"]:
        bus_index[bus["id"]] = pp.create_bus(
            net,
            vn_kv=float(bus["vn_kv"]),
            name=bus.get("name", bus["id"]),
        )

    for grid in model.get("external_grids", []):
        pp.create_ext_grid(
            net,
            bus=bus_index[grid["bus"]],
            vm_pu=float(grid["vm_pu"]),
            va_degree=float(grid.get("va_degree", 0.0)),
            name=grid.get("name", "Grid"),
            s_sc_max_mva=float(grid["s_sc_max_mva"]),
            s_sc_min_mva=float(grid["s_sc_min_mva"]),
            rx_max=float(grid["rx_max"]),
            rx_min=float(grid["rx_min"]),
        )

    for line in model.get("lines", []):
        pp.create_line_from_parameters(
            net,
            from_bus=bus_index[line["from_bus"]],
            to_bus=bus_index[line["to_bus"]],
            length_km=float(line["length_km"]),
            r_ohm_per_km=float(line["r_ohm_per_km"]),
            x_ohm_per_km=float(line["x_ohm_per_km"]),
            c_nf_per_km=float(line["c_nf_per_km"]),
            max_i_ka=float(line["max_i_ka"]),
            name=line.get("name", "Line"),
        )

    for load in model.get("loads", []):
        pp.create_load(
            net,
            bus=bus_index[load["bus"]],
            p_mw=float(load["p_mw"]),
            q_mvar=float(load["q_mvar"]),
            name=load.get("name", "Load"),
        )

    return net


def _run_power_flow(case: dict[str, Any]):
    adapter = PandapowerPowerFlowAdapter()
    adapter.connect()
    try:
        config = dict(case["power_flow_config"])
        config["network"] = _build_pandapower_net(case["model"])
        return adapter.run_simulation(config)
    finally:
        adapter.disconnect()


def _run_short_circuit(case: dict[str, Any]):
    adapter = PandapowerShortCircuitAdapter()
    adapter.connect()
    try:
        config = dict(case["short_circuit_config"])
        config["network"] = _build_pandapower_net(case["model"])
        return adapter.run_simulation(config)
    finally:
        adapter.disconnect()


def test_engine_golden_case_artifacts_declare_verified_engine_capability():
    paths = sorted(GOLDEN_ENGINE_CASE_DIR.glob("*.json"))
    assert [path.name for path in paths] == ["pandapower_two_bus_radial.json"]

    for path in paths:
        case = json.loads(path.read_text(encoding="utf-8"))
        capability = case["capability"]
        assert capability["skill_runnable"] is False
        assert capability["engine_runnable"] is True
        assert capability["engine"] == "pandapower"
        assert capability["engine_claim"] == "pandapower_powerflow_and_short_circuit"
        assert case["model"]["format"] == "pandapower_network_spec_v1"
        assert case["expected"]["power_flow"]["converged"] is True
        assert case["expected"]["short_circuit"]["standard"] == "IEC 60909"


@pytest.mark.integration
@pytest.mark.pandapower
def test_pandapower_two_bus_radial_power_flow_engine_golden_case():
    case = _load_case("pandapower_two_bus_radial")
    expected = case["expected"]["power_flow"]
    tolerances = case["tolerances"]

    result = _run_power_flow(case)

    assert result.status == SimulationStatus.COMPLETED, result.errors
    assert result.data["converged"] is True
    assert result.data["bus_count"] == expected["bus_count"]
    assert result.data["branch_count"] == expected["branch_count"]

    buses = {bus["name"]: bus for bus in result.data["buses"]}
    line = result.data["branches"][0]
    summary = result.data["summary"]

    assert buses["Source"]["voltage_pu"] == pytest.approx(
        expected["source_bus_voltage_pu"], abs=tolerances["voltage_pu"]
    )
    assert buses["Load"]["voltage_pu"] == pytest.approx(
        expected["load_bus_voltage_pu"], abs=tolerances["voltage_pu"]
    )
    assert buses["Load"]["angle_deg"] == pytest.approx(
        expected["load_bus_angle_degree"], abs=tolerances["angle_degree"]
    )
    assert line["loading_pct"] == pytest.approx(
        expected["line_loading_percent"], abs=tolerances["percent"]
    )
    assert line["pl_mw"] == pytest.approx(
        expected["line_loss_mw"], abs=tolerances["power_mw"]
    )
    assert summary["total_generation"]["p_mw"] == pytest.approx(
        expected["grid_p_mw"], abs=1e-4
    )
    assert summary["total_generation"]["q_mvar"] == pytest.approx(
        expected["grid_q_mvar"], abs=1e-4
    )


@pytest.mark.integration
@pytest.mark.pandapower
def test_pandapower_two_bus_radial_short_circuit_engine_golden_case():
    case = _load_case("pandapower_two_bus_radial")
    expected = case["expected"]["short_circuit"]
    tolerances = case["tolerances"]

    result = _run_short_circuit(case)

    assert result.status == SimulationStatus.COMPLETED, result.errors
    assert result.data["standard"] == expected["standard"]
    assert result.data["summary"]["fault_type"] == expected["fault_type"]
    assert result.data["summary"]["bus_count"] == expected["bus_count"]
    assert result.data["summary"]["max_ikss_ka"] == pytest.approx(
        expected["max_ikss_ka"], abs=1e-4
    )

    buses = {bus["bus"]: bus for bus in result.data["bus_results"]}
    assert buses["Source"]["ikss_ka"] == pytest.approx(
        expected["source_bus_ikss_ka"], abs=tolerances["current_ka"]
    )
    assert buses["Load"]["ikss_ka"] == pytest.approx(
        expected["load_bus_ikss_ka"], abs=tolerances["current_ka"]
    )
