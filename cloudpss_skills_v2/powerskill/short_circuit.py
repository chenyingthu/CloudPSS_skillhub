"""Short Circuit API - Engine-agnostic short circuit simulation facade.

Provides convenience methods for short circuit analysis on top of the
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
from cloudpss_skills_v2.libs.data_lib.types import (
    BusData,
    BranchData,
    FaultData,
    FaultType,
)
from cloudpss_skills_v2.core.system_model import PowerSystemModel


class ShortCircuit(SimulationAPI):
    """
    Lightweight API facade for short circuit simulations.

    Wraps an EngineAdapter and exposes short-circuit-domain methods:
    run_short_circuit, get_fault_currents, get_bus_voltages, get_summary.
    """

    def run_short_circuit(
        self,
        model_id: str,
        fault_type: str = "three_phase",
        fault_impedance: dict[str, float] | None = None,
        bus_id: str | None = None,
        **kwargs,
    ) -> SimulationResult:
        config = {
            "model_id": model_id,
            "simulation_type": "short_circuit",
            "fault_type": fault_type,
            "fault_impedance": fault_impedance or {},
            "bus_id": bus_id,
            **kwargs,
        }
        return self._adapter.run_simulation(config)

    def get_fault_currents(self, job_id: str) -> list[FaultData]:
        result = self._adapter.get_result(job_id)
        if result.data and "fault_currents" in result.data:
            return [FaultData.from_dict(f) for f in result.data["fault_currents"]]
        return []

    def get_bus_voltages(self, job_id: str) -> list[BusData]:
        result = self._adapter.get_result(job_id)
        if result.data and "bus_voltages" in result.data:
            return [BusData.from_dict(b) for b in result.data["bus_voltages"]]
        return []

    def get_summary(self, job_id: str) -> dict[str, Any]:
        result = self._adapter.get_result(job_id)
        if result.data and "summary" in result.data:
            return result.data["summary"]
        return {}

    def get_typed_fault_data(self, job_id: str) -> list[FaultData]:
        return self.get_fault_currents(job_id)

    def get_typed_bus_voltages(self, job_id: str) -> list[BusData]:
        return self.get_bus_voltages(job_id)

    def get_raw_result(self, job_id: str) -> SimulationResult:
        return self._adapter.get_result(job_id)

    def get_system_model(self, job_id: str) -> PowerSystemModel | None:
        """Get unified PowerSystemModel for a completed short circuit job.

        This is the new architecture method for accessing results
        in an engine-agnostic format using DataClass components.

        Args:
            job_id: The simulation job ID

        Returns:
            Unified PowerSystemModel or None if not available
        """
        # First try to get from result's system_model field (new architecture)
        result = self._adapter.get_result(job_id)
        if result.system_model is not None:
            return result.system_model

        # Fall back to adapter's unified model cache
        if hasattr(self._adapter, 'get_unified_model'):
            return self._adapter.get_unified_model(job_id)

        return None


__all__ = ["ShortCircuit"]
