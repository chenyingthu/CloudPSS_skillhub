
'''
CloudPSS Short Circuit Adapter

CloudPSS has no dedicated short-circuit API. Short circuit analysis is performed
by running an EMT simulation with a fault component, then extracting current
and voltage waveforms from the EMT result.

Uses: Model.fetch(), model.runEMT(), job.status(), job.result → EMTResult → waveform analysis
'''
from __future__ import annotations
import os
import time
import uuid
from datetime import datetime
from typing import Any
from cloudpss_skills_v2.powerapi import EngineAdapter, EngineConfig, SimulationResult, SimulationStatus, SimulationType, ValidationError, ValidationResult
_FAULT_TYPE_MAP = {
    '3phase': '3ph',
    '3ph': '3ph',
    '1phase': 'slg',
    'slg': 'slg',
    'phase-ground': 'slg',
    '2phase': 'll',
    'll': 'll',
    '2phase-ground': 'dlg',
    'dlg': 'dlg' }

class CloudPSSShortCircuitAdapter(EngineAdapter):
    pass
