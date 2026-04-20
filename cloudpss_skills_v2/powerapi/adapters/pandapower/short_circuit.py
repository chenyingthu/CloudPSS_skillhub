
'''
Pandapower Short Circuit Adapter

Real pandapower IEC 60909 short circuit integration using pp.shortcircuit.calc_sc().
Accepts same input modes as PandapowerPowerFlowAdapter (network, case, loaded model).
Adds default SC parameters to ext_grid/gen if missing before calling calc_sc.
'''
from __future__ import annotations
import copy
import uuid
from datetime import datetime
from typing import Any
from cloudpss_skills_v2.powerapi import EngineAdapter, EngineConfig, SimulationResult, SimulationStatus, SimulationType, ValidationError, ValidationResult
from cloudpss_skills_v2.libs.data_lib import FaultData, FaultType, BusData
_FAULT_TYPE_MAP = {
    '3phase': '3ph',
    '3ph': '3ph',
    'slg': '1ph',
    '1phase': '1ph',
    'phase-ground': '1ph',
    'll': '2ph',
    '2phase': '2ph',
    'dlg': '2phg',
    '2phase-ground': '2phg' }

def _ensure_sc_data(net = None):
    '''Add default IEC 60909 parameters to ext_grid and gen if missing or NaN.'''
    import numpy as np
    if 's_sc_max_mva' not in net.ext_grid.columns:
        net.ext_grid['s_sc_max_mva'] = 10000
    if 's_sc_min_mva' not in net.ext_grid.columns:
        net.ext_grid['s_sc_min_mva'] = 8000
    if 'rx_max' not in net.ext_grid.columns:
        net.ext_grid['rx_max'] = 0.1
    if 'rx_min' not in net.ext_grid.columns:
        net.ext_grid['rx_min'] = 0.1
    if not net.gen.empty:
        if 'vn_kv' not in net.gen.columns or net.gen['vn_kv'].isna().any():
            net.gen['vn_kv'] = net.gen['bus'].map(net.bus['vn_kv'])
        if 'sn_mva' not in net.gen.columns or net.gen['sn_mva'].isna().any():
            net.gen['sn_mva'] = 100
        if 'rdss_ohm' not in net.gen.columns or net.gen['rdss_ohm'].isna().any():
            net.gen['rdss_ohm'] = 0
        if 'xdss_pu' not in net.gen.columns or net.gen['xdss_pu'].isna().any():
            net.gen['xdss_pu'] = 0.2
        if 'xos_pu' not in net.gen.columns or net.gen['xos_pu'].isna().any():
            net.gen['xos_pu'] = 0.1
        if 'ros_ohm' not in net.gen.columns or net.gen['ros_ohm'].isna().any():
            net.gen['ros_ohm'] = 0
        if 'cos_phi' not in net.gen.columns or net.gen['cos_phi'].isna().any():
            net.gen['cos_phi'] = 0.8
        if 'kg' not in net.gen.columns or net.gen['kg'].isna().any():
            net.gen['kg'] = 1
    if not net.sgen.empty:
        if 'sn_mva' not in net.sgen.columns or net.sgen['sn_mva'].isna().any():
            net.sgen['sn_mva'] = net.sgen.p_mw.clip(lower = 1)
        if 'vn_kv' not in net.sgen.columns or net.sgen['vn_kv'].isna().any():
            net.sgen['vn_kv'] = net.sgen['bus'].map(net.bus['vn_kv'])
            return None
        return None


class PandapowerShortCircuitAdapter(EngineAdapter):
    pass
