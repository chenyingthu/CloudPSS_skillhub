"""
Network equivalent utilities.

Reusable helpers for extracting a minimum positive-sequence network model
from CloudPSS topology data and computing PCC Thevenin equivalents and SCR.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

import numpy as np


def normalize_bus_name(name: Any) -> str:
    return "".join(ch for ch in str(name or "").lower() if ch.isalnum())


@dataclass
class ZthResult:
    verified: bool
    z_th_pu: complex | None = None
    bus_node: Optional[str] = None
    bus_nominal_voltage_kv: Optional[float] = None
    system_base_mva: float = 100.0
    error: Optional[str] = None


@dataclass
class SCRResult:
    scr: float
    short_circuit_capacity_mva: float
    grid_strength: str
    threshold: float = 3.0
    verified: bool = True
    error: Optional[str] = None
    renewable_capacity_mw: Optional[float] = None
    z_th_pu: Optional[complex] = None
    bus_node: Optional[str] = None
    bus_nominal_voltage_kv: Optional[float] = None
    system_base_mva: float = 100.0


def compute_positive_sequence_zth(
    model, renewable_bus: str, system_base_mva: float = 100.0
) -> ZthResult:
    """
    Compute a minimum positive-sequence Thevenin impedance seen from a PCC.

    Data sources:
    - powerflow topology: bus-node mapping and transmission line positive-sequence data
    - EMT topology: generator subtransient and transformer leakage data
    """
    pf_components = (
        model.fetchTopology(implementType="powerflow").toJSON().get("components", {})
    )
    emt_components = (
        model.fetchTopology(implementType="emtp").toJSON().get("components", {})
    )

    node_to_index: Dict[str, int] = {}
    target_node = None
    target_vbase = None
    bus_name_target = normalize_bus_name(renewable_bus)

    for comp in pf_components.values():
        if (
            not isinstance(comp, dict)
            or comp.get("definition") != "model/CloudPSS/_newBus_3p"
        ):
            continue
        node = str((comp.get("pins") or {}).get("0", ""))
        if not node:
            continue
        if node not in node_to_index:
            node_to_index[node] = len(node_to_index)
        bus_args = comp.get("args", {}) or {}
        if (
            bus_name_target
            and normalize_bus_name(bus_args.get("Name")) == bus_name_target
        ):
            target_node = node
            target_vbase = float(bus_args.get("VBase", 0) or 0)

    if target_node is None:
        return ZthResult(verified=False, error=f"未找到接入母线 {renewable_bus}")
    if not node_to_index:
        return ZthResult(verified=False, error="拓扑中未识别到母线节点")

    size = len(node_to_index)
    ybus = np.zeros((size, size), dtype=complex)

    def add_series(node_a: str, node_b: str, z_pu: complex):
        if abs(z_pu) == 0:
            return
        ia = node_to_index.get(str(node_a))
        ib = node_to_index.get(str(node_b))
        if ia is None or ib is None:
            return
        y = 1 / z_pu
        ybus[ia, ia] += y
        ybus[ib, ib] += y
        ybus[ia, ib] -= y
        ybus[ib, ia] -= y

    def add_shunt(node: str, z_pu: complex):
        if abs(z_pu) == 0:
            return
        idx = node_to_index.get(str(node))
        if idx is None:
            return
        ybus[idx, idx] += 1 / z_pu

    for comp in pf_components.values():
        if (
            not isinstance(comp, dict)
            or comp.get("definition") != "model/CloudPSS/TransmissionLine"
        ):
            continue
        pins = comp.get("pins") or {}
        node_a = str(pins.get("0", ""))
        node_b = str(pins.get("1", ""))
        args = comp.get("args", {}) or {}
        r_pu = args.get("R1pu")
        x_pu = args.get("X1pu")
        if r_pu is None:
            r_pu = args.get("R1pu", args.get("R1", 0))
        if x_pu is None:
            x_pu = args.get("X1pu", args.get("Xl1", 0))
        if r_pu is None or x_pu is None:
            continue
        add_series(node_a, node_b, complex(float(r_pu), float(x_pu)))

    for comp in emt_components.values():
        if not isinstance(comp, dict):
            continue
        definition = comp.get("definition")
        pins = comp.get("pins") or {}
        args = comp.get("args", {}) or {}

        if definition == "model/CloudPSS/_newTransformer_3p2w":
            node_a = str(pins.get("0", ""))
            node_b = str(pins.get("1", ""))
            tmva = float(args.get("Tmva", system_base_mva) or system_base_mva)
            r_pu = float(args.get("Rn1", 0) or 0) + float(args.get("Rn2", 0) or 0)
            x_pu = float(args.get("Xl", 0) or 0)
            z_pu = complex(r_pu, x_pu) * (system_base_mva / tmva)
            add_series(node_a, node_b, z_pu)

        elif definition == "model/CloudPSS/SyncGeneratorRouter":
            node = str(pins.get("0", ""))
            smva = float(args.get("Smva", system_base_mva) or system_base_mva)
            r_pu = float(args.get("Rs_2", args.get("Rs", 0)) or 0)
            x_pu = float(args.get("Xdpp_2", args.get("Xdp_2", args.get("Xd", 0))) or 0)
            z_pu = complex(r_pu, x_pu) * (system_base_mva / smva)
            add_shunt(node, z_pu)

    try:
        zbus = np.linalg.inv(ybus)
    except np.linalg.LinAlgError:
        return ZthResult(verified=False, error="Ybus奇异，无法求逆得到Zbus")

    idx = node_to_index[target_node]
    return ZthResult(
        verified=True,
        z_th_pu=zbus[idx, idx],
        bus_node=target_node,
        bus_nominal_voltage_kv=float(target_vbase or 0.0),
        system_base_mva=float(system_base_mva),
    )


def compute_scr(
    zth_result: ZthResult,
    capacity_mw: float,
    threshold: float = 3.0,
) -> SCRResult:
    """
    计算短路比 SCR = Ssc / Pn

    SCR >= 3: 强电网 (strong)
    2 <= SCR < 3: 中等强度 (medium)
    SCR < 2: 弱电网 (weak)

    Args:
        zth_result: 戴维南等值计算结果
        capacity_mw: 新能源额定容量(MW)
        threshold: SCR判定阈值，默认3.0

    Returns:
        SCRResult: 包含SCR计算结果的dataclass
    """
    if not zth_result.verified or zth_result.z_th_pu is None:
        return SCRResult(
            scr=float("inf"),
            short_circuit_capacity_mva=0,
            grid_strength="unknown",
            verified=False,
            error=zth_result.error or "戴维南等值计算失败",
        )

    zth_pu = zth_result.z_th_pu
    zth_mag = abs(zth_pu)

    if zth_mag == 0:
        return SCRResult(
            scr=float("inf"),
            short_circuit_capacity_mva=float("inf"),
            grid_strength="strong",
            verified=True,
            capacity_mw=capacity_mw,
            threshold=threshold,
        )

    ssc = zth_result.system_base_mva / zth_mag
    scr = ssc / capacity_mw if capacity_mw > 0 else float("inf")

    if scr >= 3:
        strength = "strong"
    elif scr >= 2:
        strength = "medium"
    else:
        strength = "weak"

    return SCRResult(
        scr=round(scr, 2),
        short_circuit_capacity_mva=round(ssc, 2),
        grid_strength=strength,
        verified=True,
        threshold=threshold,
        renewable_capacity_mw=capacity_mw,
        z_th_pu=zth_pu,
        bus_node=zth_result.bus_node,
        bus_nominal_voltage_kv=zth_result.bus_nominal_voltage_kv,
        system_base_mva=zth_result.system_base_mva,
    )
