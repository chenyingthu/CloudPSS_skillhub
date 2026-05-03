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
from cloudpss_skills_v2.core.system_model import PowerSystemModel


class PowerFlow(SimulationAPI):
    """
    Lightweight API facade for power flow simulations.

    Wraps an EngineAdapter and exposes domain-specific methods:
    run_power_flow, get_bus_results, get_branch_results, get_summary.

    The unified model (PowerSystemModel) is automatically included in results
    when available, providing engine-agnostic access to power system data.
    """

    def __init__(self, adapter):
        """Initialize PowerFlow with adapter and set up result caching."""
        super().__init__(adapter)
        self._last_result: SimulationResult | None = None

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
        result = self._adapter.run_simulation(config)
        self._last_result = result
        return result

    def run_power_flow_with_unified(
        self,
        model_id: str | None = None,
        model_handle: ModelHandle | None = None,
        algorithm: str = "newton_raphson",
        tolerance: float = 1e-6,
        max_iterations: int = 100,
        **kwargs,
    ) -> dict[str, Any]:
        """Run power flow and return result with unified model included.

        This method runs a power flow simulation and returns a dictionary
        that includes both the standard result data and the unified model
        (PowerSystemModel) for engine-agnostic result access.

        Args:
            model_id: The model identifier to run power flow on
            model_handle: Alternative to model_id, a ModelHandle instance
            algorithm: Power flow algorithm (default: "newton_raphson")
            tolerance: Convergence tolerance (default: 1e-6)
            max_iterations: Maximum iterations (default: 100)
            **kwargs: Additional simulation parameters

        Returns:
            Dictionary containing:
            - 'status': Simulation status (completed, failed, etc.)
            - 'job_id': Job identifier
            - 'data': Raw result data from the engine
            - 'unified_model': PowerSystemModel instance (if available)
            - 'buses': List of bus dictionaries (if unified_model available)
            - 'branches': List of branch dictionaries (if unified_model available)
            - 'errors': List of error messages (if any)
            - 'warnings': List of warning messages (if any)

        Example:
            result = powerflow.run_power_flow_with_unified(model_id="model/123")
            if result['status'] == 'completed':
                model = result['unified_model']
                print(f"System has {len(model.buses)} buses")
        """
        # Run the power flow simulation
        result = self.run_power_flow(
            model_id=model_id,
            model_handle=model_handle,
            algorithm=algorithm,
            tolerance=tolerance,
            max_iterations=max_iterations,
            **kwargs,
        )

        # Build the response dictionary
        response: dict[str, Any] = {
            "status": result.status.value if result.status else None,
            "job_id": result.job_id,
            "data": result.data,
            "errors": result.errors,
            "warnings": result.warnings,
        }

        # Include unified model if available
        if result.system_model is not None:
            response["unified_model"] = result.system_model
            response["buses"] = [self._bus_to_dict(b) for b in result.system_model.buses]
            response["branches"] = [self._branch_to_dict(b) for b in result.system_model.branches]
        else:
            response["unified_model"] = None
            response["buses"] = []
            response["branches"] = []

        return response

    def _bus_to_dict(self, bus: Any) -> dict[str, Any]:
        """Convert a Bus to dictionary."""
        return {
            "bus_id": bus.bus_id,
            "name": bus.name,
            "base_kv": bus.base_kv,
            "bus_type": bus.bus_type,
            "v_magnitude_pu": bus.v_magnitude_pu,
            "v_angle_degree": bus.v_angle_degree,
            "p_injected_mw": bus.p_injected_mw,
            "q_injected_mvar": bus.q_injected_mvar,
            "vm_max_pu": bus.vm_max_pu,
            "vm_min_pu": bus.vm_min_pu,
            "area": bus.area,
            "zone": bus.zone,
        }

    def _branch_to_dict(self, branch: Any) -> dict[str, Any]:
        """Convert a Branch to dictionary."""
        return {
            "from_bus": branch.from_bus,
            "to_bus": branch.to_bus,
            "name": branch.name,
            "branch_type": branch.branch_type,
            "r_pu": branch.r_pu,
            "x_pu": branch.x_pu,
            "b_pu": branch.b_pu,
            "g_pu": branch.g_pu,
            "rate_a_mva": branch.rate_a_mva,
            "tap_ratio": branch.tap_ratio,
            "phase_shift_degree": branch.phase_shift_degree,
            "p_from_mw": branch.p_from_mw,
            "q_from_mvar": branch.q_from_mvar,
            "p_to_mw": branch.p_to_mw,
            "q_to_mvar": branch.q_to_mvar,
            "loading_percent": branch.loading_percent,
            "p_loss_mw": branch.p_loss_mw,
            "q_loss_mvar": branch.q_loss_mvar,
            "in_service": branch.in_service,
        }

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

    def get_system_model(self, job_id: str) -> PowerSystemModel | None:
        """Get unified PowerSystemModel for a completed job.

        This is the new architecture method for accessing results
        in an engine-agnostic format using DataClass components.

        Args:
            job_id: The simulation job ID

        Returns:
            Unified PowerSystemModel or None if not available
        """
        # First check if we have the result cached from a recent run
        if self._last_result is not None and self._last_result.job_id == job_id:
            if self._last_result.system_model is not None:
                return self._last_result.system_model

        # Try to get from result's system_model field (new architecture)
        result = self._adapter.get_result(job_id)
        if result.system_model is not None:
            return result.system_model

        # Fall back to adapter's unified model cache
        if hasattr(self._adapter, 'get_unified_model'):
            return self._adapter.get_unified_model(job_id)

        return None

    def get_cached_result(self) -> SimulationResult | None:
        """Get the last cached simulation result.

        Returns:
            The most recent SimulationResult from run_power_flow,
            or None if no simulation has been run yet.
        """
        return self._last_result


__all__ = ["PowerFlow"]
