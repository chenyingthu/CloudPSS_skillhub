
"""
Pandapower Power Flow Adapter

Real pandapower integration using pp.runpp().
Supports three input modes:
  - 'network' key: a pandapowerNet object (highest priority)
  - 'case' key: a case name like 'case14', 'case39' (uses pandapower.networks)
  - model_id: loaded via load_model() with a case name

Result conversion maps pandapower DataFrames to DataLib BusData/BranchData.
"""
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any
from cloudpss_skills_v2.powerapi import EngineAdapter, EngineConfig, SimulationResult, SimulationStatus, SimulationType, ValidationError, ValidationResult
from cloudpss_skills_v2.libs.data_lib import BusData, BusType, BranchData, BranchType, GeneratorData, GeneratorType, NetworkSummary
_CASE_NAMES = {
    'case5',
    'case9',
    'case14',
    'case30',
    'case39',
    'case57',
    'case118',
    'case145',
    'case300',
    'case4gs',
    'case6ww',
    'case33bw',
    'case3120sp',
    'case1888rte',
    'case2848rte',
    'case6470rte',
    'case6495rte',
    'case6515rte',
    'case9241pegase',
    'case24_ieee_rts'}

def _load_case(case_name = None):
    '''Load a pandapower case network by name.'''
    nw = networks
    import pandapower.networks
    if not hasattr(nw, case_name):
        available = [attr for attr in dir(nw) if not attr.startswith('_')]
        raise ValueError(f"Unknown pandapower case: {case_name}. Available: {available}")
    return getattr(nw, case_name)()


class PandapowerPowerFlowAdapter(EngineAdapter):
    pass
