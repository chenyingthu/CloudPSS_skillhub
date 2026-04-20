
'''
AlgoLib Power Flow Adapters

Lightweight engine adapters wrapping NewtonRaphsonSolver and FastDecoupledSolver.
No external SDK required — pure Python + numpy.
'''
from __future__ import annotations
from datetime import datetime
from typing import Any
import uuid
from cloudpss_skills_v2.powerapi import EngineAdapter, EngineConfig, SimulationResult, SimulationStatus, SimulationType, ValidationError, ValidationResult
from cloudpss_skills_v2.libs.data_lib import BusData, BranchData, GeneratorData, NetworkSummary

def _to_bus_data(raw = None):
    if isinstance(raw, BusData):
        return raw
    return None.from_dict(raw)


def _to_branch_data(raw = None):
    if isinstance(raw, BranchData):
        return raw
    return None.from_dict(raw)


def _to_gen_data(raw = None):
    if isinstance(raw, GeneratorData):
        return raw
    return None.from_dict(raw)


class AlgoLibPowerFlowAdapter(EngineAdapter):
    pass
class AlgoLibFastDecoupledAdapter(AlgoLibPowerFlowAdapter):
    '''
    Fast Decoupled power flow adapter.

    Engine name: algo_fd
    Same interface as AlgoLibPowerFlowAdapter but uses FastDecoupledSolver.
    '''
    pass  # FIXME: lambda pattern
    
    def _do_run_simulation(self, config = None):
        FastDecoupledSolver = FastDecoupledSolver
        import cloudpss_skills_v2.libs.algo_lib
        job_id = str(uuid.uuid4())[:8]
        started = datetime.now()
