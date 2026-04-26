"""Source-backed deterministic golden cases for trusted-analysis tests.

These cases are intentionally small and hand-calculable. They are not a
replacement for full IEEE/IEC benchmark systems; they lock formula behavior and
record the standard family, public source, or explicit derivation behind each
expected value before larger live or literature-backed studies are added.
"""

from __future__ import annotations


def public_source(title: str, url: str, note: str = "") -> dict[str, str]:
    return {"title": title, "url": url, "note": note}


def derived_source(title: str, derivation: str, note: str = "") -> dict[str, str]:
    return {
        "title": title,
        "source_kind": "derivation",
        "derivation": derivation,
        "note": note,
    }


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
    "reference": {
        "standard_basis": "Local topology contract for model_builder/model_validator.",
        "formula": "Not a numerical benchmark; validates graph connectivity and explicit parameter typing.",
        "sources": [
            derived_source(
                "Two-bus PV topology invariant",
                "One source bus connected to one PCC bus by one line; one PV component attached to the PCC.",
                "Used only to test model construction/validation plumbing.",
            )
        ],
        "limitations": [
            "This is a structural case, not a power-flow or short-circuit benchmark.",
            "No professional numerical correctness is claimed from this topology alone.",
        ],
    },
}


THEVENIN_WEAK_GRID = {
    "base_mva": 100.0,
    "z_th_pu": {"real": 0.03, "imag": 0.04},
    "expected_z_mag": 0.05,
    "expected_scc_mva": 2000.0,
    "expected_scr": 20.0,
    "reference": {
        "standard_basis": "IEC 60909 short-circuit capacity convention; per-unit Thevenin impedance arithmetic.",
        "formula": "|Zth| = sqrt(R^2 + X^2); Ssc = Sbase / |Zth|; SCR = Ssc / Srated",
        "sources": [
            public_source(
                "pandapower Short-Circuit documentation",
                "https://pandapower.readthedocs.io/en/latest/shortcircuit.html",
                "Documents short-circuit calculations according to DIN/IEC EN 60909.",
            ),
            public_source(
                "IEC 60909-0:2016 publication page",
                "https://webstore.iec.ch/en/publication/24100",
                "Official IEC publication metadata for short-circuit current calculation.",
            ),
        ],
        "limitations": [
            "The case verifies arithmetic after Zth is supplied; it does not derive Zth from a network.",
            "Voltage correction factors, X/R effects, and current-source contributions are outside this case.",
        ],
    },
}


POWER_QUALITY_BALANCED_HARMONIC = {
    "harmonic_voltages": {"5": 0.03, "7": 0.04},
    "phase_voltages_pu": [1.0, 0.99, 1.01],
    "expected_thd": 0.05,
    "expected_unbalance": 0.01,
    "reference": {
        "standard_basis": "IEEE 519/IEC power-quality THD convention and NEMA magnitude-unbalance convention.",
        "formula": "THD = sqrt(sum(Vh^2)) / V1; unbalance = max(|Va,b,c - Vavg|) / Vavg",
        "sources": [
            public_source(
                "MathWorks Total Harmonic Distortion block documentation",
                "https://de.mathworks.com/help/sps/ref/totalharmonicdistortion.html",
                "Defines THD as RMS total harmonics divided by RMS fundamental.",
            ),
            public_source(
                "Schneider Electric voltage/current unbalance FAQ",
                "https://www.se.com/us/en/faqs/FA409853/",
                "Documents the NEMA maximum-deviation-from-average method.",
            ),
        ],
        "limitations": [
            "This verifies THD and NEMA-style magnitude unbalance from explicit measurements only.",
            "IEC sequence-component voltage unbalance is a different metric and is not tested here.",
        ],
    },
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
    "reference": {
        "standard_basis": "IEC 60255 / IEC 60255-151 inverse-time overcurrent curve family.",
        "formula": "t = TMS * k / ((If / Ipickup)^alpha - 1), with SI k=0.14 and alpha=0.02",
        "sources": [
            public_source(
                "ABB REX610 technical manual, standard inverse-time characteristics",
                "https://techdoc.relays.protection-control.abb/r/REX610-Technical-Manual/1.1/en-US/Standard-inverse-time-characteristics",
                "Vendor technical manual publishing IEC normal inverse constants.",
            ),
            public_source(
                "Schneider Electric ADVC operations manual, IEC255 inverse time tables",
                "https://www.productinfo.schneider-electric.com/advc-operationsmanual/pkr39809_advc_operations-manual/English/BM_ADVC3%20Operations%20Manual_0000999204.xml/%24/TPC_ADVC3_OM_AppendixDIEC255InverseTimeTablesCPT_0001060607",
                "Vendor manual states IEC255 inverse-time formulas used for table values.",
            ),
        ],
        "limitations": [
            "Only the IEC standard inverse curve is checked in this golden case.",
            "CT saturation, reset behavior, breaker clearing time, and grading margins are outside this formula check.",
        ],
    },
}


REACTIVE_COMPENSATION_WEAK_BUS = {
    "bus": {"bus": "bus_pcc", "scr": 2.5, "voltage_pu": 0.92, "x_pu": 0.25},
    "expected_required_q_mvar": 0.29,
    "reference": {
        "standard_basis": "Small-signal per-unit Q-V sensitivity approximation for a weak bus.",
        "formula": "Qreq ~= Vpu * (Vtarget - Vpu) / Xth_pu, with Vtarget = 1.0 pu",
        "sources": [
            derived_source(
                "Lossless Thevenin reactance voltage-support approximation",
                "Starting from the local Q-V sensitivity dV/dQ ~= Xth / V, rearrange to Q ~= V * dV / Xth.",
                "This is an engineering sizing approximation, not a standards-compliance calculation.",
            )
        ],
        "limitations": [
            "The result is a screening size in per unit/Mvar convention, not an optimal capacitor/SVC/SVG design.",
            "It ignores voltage limits, discrete device steps, losses, controller dynamics, and load-flow iteration.",
        ],
    },
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
    "reference": {
        "standard_basis": "NERC-style SCR definition, IEEE 519/IEC THD convention, and EIA/NREL capacity-factor convention.",
        "formula": "SCR = Ssc / Prated; THD = sqrt(sum(Vh^2)) / V1; capacity_factor = average(P) / Prated",
        "sources": [
            derived_source(
                "Short-circuit ratio arithmetic used for grid-strength screening",
                "SCR is calculated as short-circuit capacity at the point of interconnection divided by rated renewable capacity.",
                "The source server for the NERC low short-circuit-strength guideline is not stable enough for an automated provenance gate.",
            ),
            public_source(
                "EIA glossary: capacity factor",
                "https://www.eia.gov/tools/glossary/index.php?id=Capacity_factor",
                "Defines capacity factor as actual energy over possible full-power energy.",
            ),
            public_source(
                "MathWorks Total Harmonic Distortion block documentation",
                "https://de.mathworks.com/help/sps/ref/totalharmonicdistortion.html",
                "Defines THD as RMS total harmonics divided by RMS fundamental.",
            ),
        ],
        "limitations": [
            "LVRT pass/fail here checks an explicit profile against configured thresholds only.",
            "The case does not validate regional grid-code LVRT envelopes or inverter controls.",
        ],
    },
}


TRUSTED_GOLDEN_CASES = {
    "two_bus_pv_model": TWO_BUS_PV_MODEL,
    "thevenin_weak_grid": THEVENIN_WEAK_GRID,
    "power_quality_balanced_harmonic": POWER_QUALITY_BALANCED_HARMONIC,
    "protection_iec_standard_inverse": PROTECTION_IEC_STANDARD_INVERSE,
    "reactive_compensation_weak_bus": REACTIVE_COMPENSATION_WEAK_BUS,
    "renewable_integration_passing": RENEWABLE_INTEGRATION_PASSING,
}
