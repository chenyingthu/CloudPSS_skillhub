"""Deterministic golden cases for trusted-analysis tests.

These cases are intentionally small and hand-calculable. They are not a
replacement for IEEE/IEC benchmark systems; they lock formula behavior before
larger live or literature-backed golden studies are added.
"""

from __future__ import annotations


TWO_BUS_PV_MODEL = {
    "rid": "golden/two_bus_pv",
    "components": [
        {"id": "bus_source", "type": "bus", "parameters": {"vn_kv": 110}},
        {"id": "bus_pcc", "type": "bus", "parameters": {"vn_kv": 110}},
        {
            "id": "line_source_pcc",
            "type": "line",
            "from_bus": "bus_source",
            "to_bus": "bus_pcc",
            "parameters": {"length_km": 10.0, "r_ohm": 1.0, "x_ohm": 5.0},
        },
        {
            "id": "pv_pcc",
            "type": "pv",
            "bus": "bus_pcc",
            "parameters": {"p_mw": 50.0},
        },
    ],
}


THEVENIN_WEAK_GRID = {
    "base_mva": 100.0,
    "z_th_pu": {"real": 0.03, "imag": 0.04},
    "expected_z_mag": 0.05,
    "expected_scc_mva": 2000.0,
    "expected_scr": 20.0,
}


POWER_QUALITY_BALANCED_HARMONIC = {
    "harmonic_voltages": {"5": 0.03, "7": 0.04},
    "phase_voltages_pu": [1.0, 0.99, 1.01],
    "expected_thd": 0.05,
    "expected_unbalance": 0.01,
}


PROTECTION_IEC_STANDARD_INVERSE = {
    "relay": {
        "id": "R1",
        "load_current": 200.0,
        "fault_current": 3000.0,
        "time_dial": 0.1,
        "curve_type": "iec_standard_inverse",
    },
    "analysis": {"load_multiplier": 1.25, "fault_current_safety_factor": 0.5},
    "expected_pickup_current": 250.0,
    "expected_operating_time_s": 0.2748,
}


REACTIVE_COMPENSATION_WEAK_BUS = {
    "bus": {"bus": "bus_pcc", "scr": 2.5, "voltage_pu": 0.92, "x_pu": 0.25},
    "expected_required_q_mvar": 0.29,
}


RENEWABLE_INTEGRATION_PASSING = {
    "renewable": {
        "type": "pv",
        "capacity_mw": 50.0,
        "short_circuit_mva": 200.0,
        "point_of_interconnection": "bus_pcc",
        "capacity_series_mw": [25.0, 30.0, 20.0, 35.0],
    },
    "harmonics": {
        "fundamental_voltage": 1.0,
        "orders": {"5": 0.03, "7": 0.04},
        "limit_thd": 0.06,
    },
    "lvrt": {
        "profile": [
            {"time_s": 0.0, "voltage_pu": 1.0},
            {"time_s": 0.1, "voltage_pu": 0.2},
            {"time_s": 0.8, "voltage_pu": 0.92},
        ],
        "min_voltage_pu": 0.15,
        "max_recovery_time_s": 1.5,
    },
    "analysis": {"min_scr": 3.0, "target_capacity_factor": 0.5},
    "expected_scr": 4.0,
    "expected_thd": 0.05,
    "expected_capacity_factor": 0.55,
}
