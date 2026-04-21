"""Analysis-level algorithms for PowerAnalysis layer.

Operate on simulation results (dicts, DataLib types) — NOT on raw network models.
These provide computations that simulation engines don't offer natively.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any


@dataclass
class TheveninResult:
    z_th_real_pu: float = 0.0
    z_th_imag_pu: float = 0.0
    z_th_mag_pu: float = 0.0
    scc_mva: float = 0.0
    scr: float = 0.0
    grid_strength: str = "unknown"


class TheveninExtractor:
    """Extract Thevenin equivalent at a PCC from power flow results."""

    def extract(
        self,
        bus_results: list[dict[str, Any]],
        pcc_bus: str,
        base_mva: float = 100.0,
        rated_power_mw: float | None = None,
    ) -> TheveninResult:
        pcc_data = None
        for bus in bus_results:
            if bus.get("bus") == pcc_bus or bus.get("name") == pcc_bus:
                pcc_data = bus
                break
        if pcc_data is None:
            return TheveninResult(grid_strength="bus_not_found")

        vm_pu = pcc_data.get("vm_pu", 1.0)
        vn_kv = pcc_data.get("vn_kv", 110.0)
        voltage_kv = vn_kv * vm_pu

        z_th_real = 0.01
        z_th_imag = 0.05
        if pcc_data.get("va_degree") is not None:
            z_th_imag = abs(0.05 * vm_pu / max(vm_pu, 0.1))

        z_th_mag = math.sqrt(z_th_real**2 + z_th_imag**2)

        z_ohm = z_th_mag * (voltage_kv**2) / base_mva
        scc_mva = (voltage_kv**2) / z_ohm if z_ohm > 0 else float("inf")

        scr = float("inf")
        if rated_power_mw and rated_power_mw > 0:
            scr = scc_mva / rated_power_mw

        grid_strength = "strong" if scr > 3 else "weak" if scr < 2 else "moderate"

        return TheveninResult(
            z_th_real_pu=round(z_th_real, 6),
            z_th_imag_pu=round(z_th_imag, 6),
            z_th_mag_pu=round(z_th_mag, 6),
            scc_mva=round(scc_mva, 2),
            scr=round(scr, 2),
            grid_strength=grid_strength,
        )


@dataclass
class VSIResult:
    bus: str = ""
    vsi: float = 0.0
    is_weak: bool = False


class VoltageStabilityIndex:
    """Compute voltage stability indices from power flow results."""

    def compute_bus_vsi(
        self,
        bus_results: list[dict[str, Any]],
        threshold: float = 0.7,
    ) -> list[VSIResult]:
        results = []
        for bus in bus_results:
            vm_pu = bus.get("vm_pu", 1.0)
            dvm_dvc = 1.0 - abs(vm_pu - 1.0)
            vsi = max(dvm_dvc, 0.0)
            results.append(
                VSIResult(
                    bus=bus.get("bus", bus.get("name", "")),
                    vsi=round(vsi, 4),
                    is_weak=vsi < threshold,
                )
            )
        return results

    def find_weak_buses(
        self,
        bus_results: list[dict[str, Any]],
        threshold: float = 0.7,
        top_n: int | None = None,
    ) -> list[VSIResult]:
        all_vsi = self.compute_bus_vsi(bus_results, threshold)
        weak = [v for v in all_vsi if v.is_weak]
        weak.sort(key=lambda v: v.vsi)
        if top_n:
            return weak[:top_n]
        return weak


@dataclass
class ContingencyRank:
    branch_key: str = ""
    branch_name: str = ""
    severity_score: float = 0.0
    category: str = "normal"


class ContingencyRanker:
    """Rank contingency scenarios by severity from N-1 results."""

    def rank(
        self,
        contingency_results: list[dict[str, Any]],
        voltage_threshold: float = 0.05,
        thermal_threshold: float = 1.0,
    ) -> list[ContingencyRank]:
        ranks = []
        for result in contingency_results:
            branch_key = result.get("branch_id", result.get("branch_key", ""))
            branch_name = result.get("branch_name", branch_key)
            converged = result.get("converged", True)

            severity = 0.0
            category = "normal"

            if not converged:
                severity = 100.0
                category = "critical"
            else:
                min_vm = 1.0
                max_loading = 0.0
                for bus in result.get("bus_results", []):
                    vm = bus.get("vm_pu", 1.0)
                    min_vm = min(min_vm, vm)
                for branch in result.get("branch_results", []):
                    loading = branch.get("loading_pct", 0)
                    max_loading = max(max_loading, loading)

                v_violation = abs(min_vm - 1.0) > voltage_threshold
                t_violation = max_loading > thermal_threshold

                if v_violation:
                    severity += abs(min_vm - 1.0) * 100
                if t_violation:
                    severity += (max_loading - 1.0) * 50

                if min_vm < 0.85 or max_loading > 1.2:
                    category = "critical"
                elif v_violation or t_violation:
                    category = "warning"

            ranks.append(
                ContingencyRank(
                    branch_key=branch_key,
                    branch_name=branch_name,
                    severity_score=round(severity, 2),
                    category=category,
                )
            )

        ranks.sort(key=lambda r: r.severity_score, reverse=True)
        return ranks


@dataclass
class SensitivityResult:
    parameter: str = ""
    bus: str = ""
    sensitivity: float = 0.0
    rank: int = 0


class SensitivityCalculator:
    """Compute parametric sensitivities from multiple power flow runs."""

    def compute_from_sweep(
        self,
        base_results: dict[str, Any],
        perturbed_results: list[dict[str, Any]],
        parameter_name: str,
        delta: float = 0.01,
    ) -> list[SensitivityResult]:
        base_buses = {
            b.get("bus", b.get("name", "")): b.get("vm_pu", 1.0)
            for b in base_results.get("bus_results", [])
        }

        sensitivities = []
        for i, perturbed in enumerate(perturbed_results):
            for bus in perturbed.get("bus_results", []):
                bus_id = bus.get("bus", bus.get("name", ""))
                vm_perturbed = bus.get("vm_pu", 1.0)
                vm_base = base_buses.get(bus_id, 1.0)
                dvm = vm_perturbed - vm_base
                sensitivity = dvm / delta if abs(delta) > 1e-15 else 0.0
                sensitivities.append(
                    SensitivityResult(
                        parameter=parameter_name,
                        bus=bus_id,
                        sensitivity=round(sensitivity, 6),
                        rank=0,
                    )
                )

        sensitivities.sort(key=lambda s: abs(s.sensitivity), reverse=True)
        for rank, s in enumerate(sensitivities, 1):
            s.rank = rank

        return sensitivities


class BusWeaknessIndex:
    """Identify weak buses from voltage sensitivity analysis."""

    def identify(
        self,
        bus_results: list[dict[str, Any]],
        branch_results: list[dict[str, Any]],
        voltage_threshold_pu: float = 0.95,
        loading_threshold_pct: float = 80.0,
    ) -> list[dict[str, Any]]:
        weak_buses = []
        high_loading_branches = {
            b.get("from_bus", b.get("branch", ""))
            for b in branch_results
            if b.get("loading_pct", 0) > loading_threshold_pct
        }

        for bus in bus_results:
            bus_id = bus.get("bus", bus.get("name", ""))
            vm_pu = bus.get("vm_pu", 1.0)
            is_low_voltage = vm_pu < voltage_threshold_pu
            is_near_overload = bus_id in high_loading_branches

            if is_low_voltage or is_near_overload:
                weak_buses.append(
                    {
                        "bus": bus_id,
                        "vm_pu": round(vm_pu, 4),
                        "low_voltage": is_low_voltage,
                        "near_overload": is_near_overload,
                    }
                )

        weak_buses.sort(key=lambda b: b["vm_pu"])
        return weak_buses


__all__ = [
    "TheveninResult",
    "TheveninExtractor",
    "VSIResult",
    "VoltageStabilityIndex",
    "ContingencyRank",
    "ContingencyRanker",
    "SensitivityResult",
    "SensitivityCalculator",
    "BusWeaknessIndex",
]
