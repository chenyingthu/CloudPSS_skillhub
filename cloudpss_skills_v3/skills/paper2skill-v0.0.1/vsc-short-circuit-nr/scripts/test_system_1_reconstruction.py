from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray


def _line_series_admittance(line: dict[str, Any], from_kv: float, system_base_mva: float) -> complex:
    base_impedance = (from_kv ** 2) / system_base_mva
    series_impedance_ohm = complex(line["r_ohm_per_km"], line["x_ohm_per_km"]) * line["length_km"]
    series_impedance_pu = series_impedance_ohm / base_impedance
    return 1 / series_impedance_pu


def load_test_system_1_artifact() -> dict[str, Any]:
    artifact_path = Path(__file__).resolve().with_name("test_system_1_network.json")
    return json.loads(artifact_path.read_text(encoding="utf-8"))


def build_test_system_1_admittance_matrix(islanded: bool = True) -> tuple[NDArray[np.complex128], int, dict[str, int]]:
    artifact = load_test_system_1_artifact()
    model = artifact["model"]
    system_base_mva = float(model["sn_mva"])
    closed_lines = list(model["lines"])
    active_bus_ids = {
        bus_id
        for line in closed_lines
        for bus_id in (line["from_bus"], line["to_bus"])
    }
    if not islanded:
        for trafo in model.get("trafos", []):
            active_bus_ids.add(trafo["hv_bus"])
            active_bus_ids.add(trafo["lv_bus"])

    buses = [bus for bus in model["buses"] if bus["id"] in active_bus_ids]
    bus_index = {bus["id"]: index for index, bus in enumerate(buses)}
    bus_count = len(buses)
    ybus = np.zeros((bus_count, bus_count), dtype=np.complex128)

    grounding_g = 1e-6
    for i in range(bus_count):
        ybus[i, i] += grounding_g

    bus_voltage_lookup = {bus["id"]: float(bus["vn_kv"]) for bus in model["buses"]}

    for line in closed_lines:
        from_bus = bus_index[line["from_bus"]]
        to_bus = bus_index[line["to_bus"]]
        base_kv = bus_voltage_lookup[line["from_bus"]]
        series_admittance = _line_series_admittance(line, base_kv, system_base_mva)
        ybus[from_bus, from_bus] += series_admittance
        ybus[to_bus, to_bus] += series_admittance
        ybus[from_bus, to_bus] -= series_admittance
        ybus[to_bus, from_bus] -= series_admittance

    if not islanded:
        for trafo in model.get("trafos", []):
            hv_bus = bus_index[trafo["hv_bus"]]
            lv_bus = bus_index[trafo["lv_bus"]]
            z_pu = complex(trafo["vkr_percent"], np.sqrt(max(0.0, trafo["vk_percent"] ** 2 - trafo["vkr_percent"] ** 2))) / 100.0
            series_admittance = 1 / z_pu
            ybus[hv_bus, hv_bus] += series_admittance
            ybus[lv_bus, lv_bus] += series_admittance
            ybus[hv_bus, lv_bus] -= series_admittance
            ybus[lv_bus, hv_bus] -= series_admittance
        slack_bus = bus_index[model["external_grids"][0]["bus"]]
    else:
        slack_bus = bus_index["bus1"]

    return ybus, slack_bus, bus_index


def get_paper_vsc_converters(bus_index: dict[str, int] | None = None) -> list[dict[str, Any]]:
    if bus_index is None:
        _, _, bus_index = build_test_system_1_admittance_matrix(islanded=True)

    artifact = load_test_system_1_artifact()
    converters = []
    for converter in artifact["test_system_1"]["converters"]:
        if converter["id"] == "VSC1":
            p_ref = 0.0
            q_ref = 0.0
            saturation_preference = "FSS"
        elif converter["id"] == "VSC2":
            p_ref = float(converter["p_ref_pu"])
            q_ref = 0.0
            saturation_preference = "FSS"
        else:
            p_ref = float(converter["p_ref_pu"])
            q_ref = float(converter["q_ref_pu"])
            saturation_preference = "PSS"

        control_mode = "PQ"
        u_ref = 1.0
        k_isp = 0.0
        u_ref_gs = 1.0
        if converter["id"] == "VSC1":
            control_mode = "GFM"
            u_ref = float(converter["u_ref_pu"])
        elif converter["id"] == "VSC2":
            control_mode = "PV"
            u_ref = float(converter["u_ref_pu"])
        elif converter["id"] == "VSC3":
            control_mode = "GS"
            k_isp = float(converter["k_isp"])
            u_ref_gs = float(converter["u_ref_gs_pu"])

        converters.append(
            {
                "bus": bus_index[converter["bus"]],
                "p_ref": p_ref,
                "q_ref": q_ref,
                "i_max": float(converter["i_max_pu"]),
                "saturation_preference": saturation_preference,
                "control_mode": control_mode,
                "u_ref": u_ref,
                "k_isp": k_isp,
                "u_ref_gs": u_ref_gs,
            }
        )
    return converters


def summarize_test_system_1_artifact() -> dict[str, Any]:
    artifact = load_test_system_1_artifact()
    model = artifact["model"]
    return {
        "case_id": artifact["case_id"],
        "bus_count": len(model["buses"]),
        "line_count": len(model["lines"]),
        "trafo_count": len(model.get("trafos", [])),
        "load_count": len(model.get("loads", [])),
        "converter_count": len(artifact["test_system_1"]["converters"]),
        "fault_bus": artifact["test_system_1"]["fault_bus"],
        "fault_scenarios": artifact["test_system_1"]["fault_scenarios"],
        "benchmark_carryover_notes": artifact["test_system_1"]["benchmark_carryover_notes"],
    }
