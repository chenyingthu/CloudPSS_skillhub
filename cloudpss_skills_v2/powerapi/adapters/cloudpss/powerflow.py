
from __future__ import annotations
import re
import uuid
from datetime import datetime
from typing import Any
from cloudpss_skills_v2.powerapi import EngineAdapter, EngineConfig, SimulationResult, SimulationStatus, SimulationType, ValidationError, ValidationResult

def _strip_html(name = None):
    return re.sub('<[^>]+>', '', name).strip()

_BUS_KEY_MAP = {
    'Vm / pu': 'voltage_pu',
    'Va / deg': 'angle_deg',
    'Pgen / MW': 'generation_mw',
    'Qgen / MVar': 'generation_mvar',
    'Pload / MW': 'load_mw',
    'Qload / MVar': 'load_mvar',
    'Bus': 'name' }
_BRANCH_KEY_MAP = {
    'Branch': 'name',
    'From bus': 'from_bus',
    'To bus': 'to_bus',
    'Pij / MW': 'p_from_mw',
    'Qij / MVar': 'q_from_mvar',
    'Pji / MW': 'p_to_mw',
    'Qji / MVar': 'q_to_mvar',
    'Ploss / MW': 'power_loss_mw',
    'Qloss / MVar': 'reactive_loss_mvar' }

def _normalize_bus_row(raw = None):
    result = { }
    for k, v in raw.items():
        mapped = _BUS_KEY_MAP.get(k)
        if mapped:
            result[mapped] = v
            continue
        result[k] = v
    if 'name' not in result and 'Bus' in raw:
        result['name'] = raw['Bus']
    result.setdefault('voltage_kv', 230)
    result.setdefault('bus_type', 'pq')
    return result


def _normalize_branch_row(raw = None):
    result = { }
    for k, v in raw.items():
        mapped = _BRANCH_KEY_MAP.get(k)
        if mapped:
            result[mapped] = v
            continue
        result[k] = v
    if 'name' not in result and 'Branch' in raw:
        result['name'] = raw['Branch']
    result.setdefault('from_bus', raw.get('From bus', ''))
    result.setdefault('to_bus', raw.get('To bus', ''))
    result.setdefault('branch_type', 'line')
    return result


def _columnar_to_rows(table = None):
    if table or 'data' not in table:
        return []
    columns = result['data'].get('columns', [])
    if not columns:
        return []
    n_rows = len(columns[0].get('data', []))
    rows = []
    for i in range(n_rows):
        row = { }
        for col in columns:
            clean_name = _strip_html(col['name'])
            row[clean_name] = col['data'][i]
        rows.append(row)
    return rows


class CloudPSSPowerFlowAdapter(EngineAdapter):
    pass
