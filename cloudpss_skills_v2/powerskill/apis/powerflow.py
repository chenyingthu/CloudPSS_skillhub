"""PowerFlow API - Lightweight facade for power flow simulation."""
from __future__ import annotations
from typing import Any, Optional
from cloudpss_skills_v2.powerapi import SimulationResult, SimulationStatus
from cloudpss_skills_v2.powerskill import SimulationAPI
from cloudpss_skills_v2.libs.data_lib import BusData, BranchData, GeneratorData, NetworkSummary

class PowerFlowAPI(SimulationAPI):
    """Lightweight API facade for power flow simulations."""

    def run_power_flow(self, model_id: str, algorithm: str = 'acpf',
                       tolerance: float = 1e-6, max_iterations: int = 100,
                       **kwargs) -> SimulationResult:
        config = {
            'model_id': model_id,
            'algorithm': algorithm,
            'tolerance': tolerance,
            'max_iterations': max_iterations,
            **kwargs,
        }
        return self.adapter.run_simulation(config)

    def get_bus_results(self, job_id: str) -> list[BusData]:
        result = self.adapter.get_result(job_id)
        if result.data and 'buses' in result.data:
            return [BusData.from_dict(b) for b in result.data['buses']]
        return []

    def get_branch_results(self, job_id: str) -> list[BranchData]:
        result = self.adapter.get_result(job_id)
        if result.data and 'branches' in result.data:
            return [BranchData.from_dict(b) for b in result.data['branches']]
        return []

    def get_summary(self, job_id: str) -> Optional[NetworkSummary]:
        result = self.adapter.get_result(job_id)
        if result.data and 'summary' in result.data:
            return NetworkSummary.from_dict(result.data['summary'])
        return None

__all__ = ['PowerFlowAPI']
