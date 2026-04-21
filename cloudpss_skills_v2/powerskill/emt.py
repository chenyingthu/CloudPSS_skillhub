"""EMT API - Engine-agnostic electromagnetic transient simulation facade.

Provides convenience methods for EMT simulations on top of the
generic EngineAdapter interface, with DataLib-typed result extraction.
"""

from __future__ import annotations

from typing import Any, Optional

from cloudpss_skills_v2.powerapi import (
    EngineAdapter,
    SimulationResult,
    SimulationStatus,
)
from cloudpss_skills_v2.powerskill.base import SimulationAPI
from cloudpss_skills_v2.libs.data_lib.types import BusData, BranchData


class EMT(SimulationAPI):
    """
    Lightweight API facade for electromagnetic transient simulations.

    Wraps an EngineAdapter and exposes EMT-domain methods:
    run_emt, get_waveforms, get_signals, get_metadata, etc.
    """

    def run_emt(
        self,
        model_id: str,
        duration: float | None = None,
        step_size: float | None = None,
        timeout: int = 300,
        sampling_freq: int = 2000,
        fault_config: dict[str, Any] | None = None,
        **kwargs,
    ) -> SimulationResult:
        config = {
            "model_id": model_id,
            "simulation_type": "emt",
            "duration": duration,
            "step_size": step_size,
            "timeout": timeout,
            "sampling_freq": sampling_freq,
            **kwargs,
        }
        if fault_config:
            config["fault"] = fault_config
        return self._adapter.run_simulation(config)

    def get_waveforms(self, job_id: str) -> list[dict[str, Any]]:
        result = self._adapter.get_result(job_id)
        if result.data and "plots" in result.data:
            return result.data["plots"]
        return []

    def get_signals(self, job_id: str, plot_index: int = 0) -> list[str]:
        result = self._adapter.get_result(job_id)
        if result.data and "plots" in result.data:
            plots = result.data["plots"]
            if plot_index < len(plots):
                return plots[plot_index].get("channels", [])
        return []

    def get_metadata(self, job_id: str) -> dict[str, Any]:
        result = self._adapter.get_result(job_id)
        if result.data and "metadata" in result.data:
            return result.data["metadata"]
        return {}

    def get_typed_bus_voltages(
        self, job_id: str, time_index: int = -1
    ) -> list[BusData]:
        result = self._adapter.get_result(job_id)
        if result.data and "bus_voltages" in result.data:
            voltages = result.data["bus_voltages"]
            if isinstance(voltages, list) and time_index >= 0:
                if time_index < len(voltages):
                    return [BusData.from_dict(b) for b in voltages[time_index]]
            elif isinstance(voltages, list):
                return [BusData.from_dict(b) for b in voltages]
        return []

    def get_typed_branch_currents(
        self, job_id: str, time_index: int = -1
    ) -> list[BranchData]:
        result = self._adapter.get_result(job_id)
        if result.data and "branch_currents" in result.data:
            currents = result.data["branch_currents"]
            if isinstance(currents, list) and time_index >= 0:
                if time_index < len(currents):
                    return [BranchData.from_dict(b) for b in currents[time_index]]
            elif isinstance(currents, list):
                return [BranchData.from_dict(b) for b in currents]
        return []

    def get_raw_result(self, job_id: str) -> SimulationResult:
        return self._adapter.get_result(job_id)


__all__ = ["EMT"]
