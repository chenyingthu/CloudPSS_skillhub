
'''
AlgoLib Short Circuit Adapter

Lightweight IEC 60909 short circuit calculator.
No external SDK required — pure Python + numpy.
'''
from __future__ import annotations
from datetime import datetime
from typing import Any
import uuid
from cloudpss_skills_v2.powerapi import EngineAdapter, EngineConfig, SimulationResult, SimulationStatus, SimulationType, ValidationError, ValidationResult
from cloudpss_skills_v2.libs.data_lib import BusData, BranchData, FaultData, FaultType, GeneratorData
_FAULT_TYPE_MAP = {
    '3phase': FaultType.THREE_PHASE,
    '3ph': FaultType.THREE_PHASE,
    'slg': FaultType.SINGLE_LINE_TO_GROUND,
    '1phase': FaultType.SINGLE_LINE_TO_GROUND,
    'phase-ground': FaultType.SINGLE_LINE_TO_GROUND,
    'll': FaultType.LINE_TO_LINE,
    '2phase': FaultType.LINE_TO_LINE,
    'llg': FaultType.DOUBLE_LINE_TO_GROUND,
    'dlg': FaultType.DOUBLE_LINE_TO_GROUND,
    '2phase-ground': FaultType.DOUBLE_LINE_TO_GROUND }

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


class AlgoLibShortCircuitAdapter(EngineAdapter):
    pass
