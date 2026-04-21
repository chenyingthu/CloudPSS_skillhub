"""PowerFlow API - Engine-agnostic power flow simulation facade.

Provides convenience methods for power flow analysis on top of the
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
from cloudpss_skills_v2.powerskill.model_handle import ModelHandle
from cloudpss_skills_v2.libs.data_lib.types import (
    BusData,
    BranchData,
    GeneratorData,
    NetworkSummary,
)


class PowerFlow(SimulationAPI):
    """
    Lightweight API facade for power flow simulations.

    Wraps an EngineAdapter and exposes domain-specific methods:
    run_power_flow, get_bus_results, get_branch_results, get_summary.
    """

    def run_power_flow(
        self,
        model_id: str | None = None,
        model_handle: ModelHandle | None = None,
        algorithm: str = "newton_raphson",
        tolerance: float = 1e-6,
        max_iterations: int = 100,
        **kwargs,
    ) -> SimulationResult:
        effective_model_id = model_id or (
            model_handle.model_id if model_handle else None
        )
        if effective_model_id is None:
            return SimulationResult(
                status=SimulationStatus.FAILED,
                errors=["Either model_id or model_handle must be provided"],
            )
        config = {
            "model_id": effective_model_id,
            "simulation_type": "power_flow",
            "algorithm": algorithm,
            "tolerance": tolerance,
            "max_iterations": max_iterations,
            **kwargs,
        }
        return self._adapter.run_simulation(config)

    def get_bus_results(self, job_id: str) -> list[BusData]:
        result = self._adapter.get_result(job_id)
        if result.data and "buses" in result.data:
            return [BusData.from_dict(b) for b in result.data["buses"]]
        return []

    def get_branch_results(self, job_id: str) -> list[BranchData]:
        result = self._adapter.get_result(job_id)
        if result.data and "branches" in result.data:
            return [BranchData.from_dict(b) for b in result.data["branches"]]
        return []

    def get_summary(self, job_id: str) -> Optional[NetworkSummary]:
        result = self._adapter.get_result(job_id)
        if result.data and "summary" in result.data:
            return NetworkSummary.from_dict(result.data["summary"])
        return None

    def get_raw_result(self, job_id: str) -> SimulationResult:
        return self._adapter.get_result(job_id)


__all__ = ["PowerFlow"]
