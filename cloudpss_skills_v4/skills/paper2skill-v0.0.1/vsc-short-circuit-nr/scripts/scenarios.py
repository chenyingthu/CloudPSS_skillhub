import numpy as np
from numpy.typing import NDArray

TEST_SYSTEM_2_VSC_BUSES = [1, 2, 5, 7, 9, 11, 12, 13]
TEST_SYSTEM_2_SYSTEM_BASE_MVA = 100.0
TEST_SYSTEM_2_FAULT_BUS = 10
TEST_SYSTEM_2_FAULT_BUS_KV_ASSUMPTION = 110.0


LOCAL_VALIDATION_SCENARIOS = {
    "baseline_ieee14_fault": {
        "fault_bus": 12,
        "fault_impedance": 0.01j,
        "converters": [],
    },
    "single_vsc_pss_fault": {
        "fault_bus": 12,
        "fault_impedance": 0.01j,
        "converters": [
            {
                "bus": 5,
                "p_ref": 0.2,
                "q_ref": 0.1,
                "i_max": 0.8,
                "saturation_preference": "PSS",
            }
        ],
    },
}


PAPER_VALIDATION_TARGETS = {
    "test_system_1": {
        "name": "CIGRE European MV based system",
        "fault_bus": 12,
        "fault_impedances_pu": ["j0.2", "j0.05"],
        "reported_state_resolution": {"VSC1": "USS", "VSC2": "FSS", "VSC3": "PSS"},
        "table_10_parameters": {
            "u_ref1_pu": 1.0,
            "i_vsc1_max_pu": 2.5,
            "p_ref2_pu": -0.794,
            "u_ref_pv2_pu": 0.96,
            "i_vsc2_max_pu": 1.0,
            "p_ref3_pu": -0.8,
            "q_ref3_pu": -0.023,
            "i_vsc3_max_pu": 1.0,
            "k_isp3": 2.0,
            "u_ref_gs3_pu": 1.0,
        },
        "moderate_fault_table": {
            "fault_impedance_pu": "j0.2",
            "source": "Table 2",
            "iterations": [
                {
                    "iteration": 1,
                    "vsc_states": {"VSC1": "USS", "VSC2": "USS", "VSC3": "USS"},
                    "i_vsc1_pu": 2.412,
                    "u1": "1∠0°",
                    "i_vsc2_pu": 2.73,
                    "p_vsc2_pu": -0.794,
                    "u6": "0.96∠-10.6°",
                    "i_vsc3_pu": 1.231,
                    "p_vsc3_pu": -0.8,
                    "q_vsc3_pu": 0.385,
                    "u12": "0.722∠-5.7°",
                    "feasible": False,
                },
                {
                    "iteration": 2,
                    "vsc_states": {"VSC1": "USS", "VSC2": "FSS", "VSC3": "PSS"},
                    "i_vsc1_pu": 2.204,
                    "u1": "1∠0°",
                    "i_vsc2_pu": 1.0,
                    "p_vsc2_pu": 0.0,
                    "u6": "0.912∠-2.6°",
                    "i_vsc3_pu": 1.0,
                    "p_vsc3_pu": -0.572,
                    "q_vsc3_pu": 0.403,
                    "u12": "0.700∠-0.1°",
                    "feasible": True,
                },
            ],
        },
        "severe_fault_table": {
            "fault_impedance_pu": "j0.05",
            "source": "Section 4.1 lower-impedance result table (caption OCR-corrupted)",
            "caption_recovery_status": "numeric rows reliable, table label corrupted",
            "iterations": [
                {
                    "iteration": 1,
                    "vsc_states": {"VSC1": "USS", "VSC2": "USS", "VSC3": "USS"},
                    "i_vsc1_pu": 4.507,
                    "u1": "1∠0°",
                    "i_vsc2_pu": 6.254,
                    "p_vsc2_pu": -0.794,
                    "u6": "0.96∠-21.9°",
                    "i_vsc3_pu": 2.294,
                    "p_vsc3_pu": -0.8,
                    "q_vsc3_pu": 0.472,
                    "u12": "0.405∠-8.7°",
                    "feasible": False,
                },
                {
                    "iteration": 2,
                    "vsc_states": {"VSC1": "FSS", "VSC2": "FSS", "VSC3": "FSS"},
                    "i_vsc1_pu": 2.5,
                    "u1": "0.556∠0°",
                    "i_vsc2_pu": 1.0,
                    "p_vsc2_pu": 0.0,
                    "u6": "0.454∠-2.7°",
                    "i_vsc3_pu": 1.0,
                    "p_vsc3_pu": 0.0,
                    "q_vsc3_pu": 0.222,
                    "u12": "0.222∠10.4°",
                    "feasible": True,
                },
            ],
        },
    },
    "test_system_2": {
        "name": "IEEE 14 bus based system",
        "vsc_count": 8,
        "penetration_levels": [0.25, 0.5, 0.75],
        "explicit_fault": {"location": "bus 11", "type": "bolted three-phase-to-ground", "u_ft": 0.0},
        "fault_description": "three-phase bolted fault at bus 11 with u_ft = 0",
        "method_level_acceptance": {
            "max_error_percent": 5.0,
            "scope": "public IEEE14 reconstruction with documented voltage-base and converter-base assumptions",
        },
        "table_10_parameters": {
            "p_ref_pu": 0.75,
            "q_ref_pu": 0.008,
            "i_vsc_max_pu": 1.0,
            "k_isp": 0.0,
            "penetration_capacity_mva": {
                "25%": 11.3,
                "50%": 22.7,
                "75%": 34.0,
            },
        },
        "short_circuit_tables": {
            "25%": {
                "source": "Table 4",
                "this_paper_ka": 1.706,
                "comparators_ka": {"VDE0102": 2.038, "IEC60909": 2.038, "ANSI": 1.827, "Complete": 6.478},
                "error_percent": {"VDE0102": 19.5, "IEC60909": 19.5, "ANSI": 7.1, "Complete": 279.7},
            },
            "50%": {
                "source": "Table 5",
                "this_paper_ka": 1.82,
                "comparators_ka": {"VDE0102": 2.388, "IEC60909": 2.388, "ANSI": 2.136, "Complete": 6.446},
                "error_percent": {"VDE0102": 31.2, "IEC60909": 31.2, "ANSI": 17.4, "Complete": 254.2},
            },
            "75%": {
                "source": "Table 6",
                "this_paper_ka": 1.761,
                "comparators_ka": {"VDE0102": 2.684, "IEC60909": 2.684, "ANSI": 2.396, "Complete": 6.401},
                "error_percent": {"VDE0102": 52.4, "IEC60909": 52.4, "ANSI": 36.1, "Complete": 263.5},
            },
        },
    },
}


MISSING_REPRODUCTION_PARAMETERS = {
    "test_system_1": [
        "Complete Table 10 column mapping for all VSC1/VSC2/VSC3 parameters",
        "Adapted CIGRE MV network impedances, transformers, and load equivalents used in the paper",
        "Explicit base values confirmed from the journal paper rather than inferred benchmark references",
        "Unambiguous fault-type wording for the Section 4.1 study",
    ],
    "test_system_2": [
        "PowerFactory-specific VSC transformer impedances, if any, behind the Figure 4 converter insertions",
        "Exact kA voltage-base convention used by the commercial-model comparison",
        "Pre-fault operating point and non-converter equivalent modeling choices needed for strict commercial-model reproduction",
    ],
}


def build_ieee14_admittance_matrix() -> tuple[NDArray[np.complex128], int]:
    branch_data = [
        (1, 2, 0.01938, 0.05917),
        (1, 5, 0.05403, 0.22304),
        (2, 3, 0.04699, 0.19797),
        (2, 4, 0.05811, 0.17632),
        (2, 5, 0.05695, 0.17388),
        (3, 4, 0.06701, 0.17103),
        (4, 5, 0.01335, 0.04211),
        (4, 7, 0.0, 0.20912),
        (4, 9, 0.0, 0.55618),
        (5, 6, 0.0, 0.25202),
        (6, 11, 0.09498, 0.19890),
        (6, 12, 0.12291, 0.25581),
        (6, 13, 0.06615, 0.13027),
        (7, 8, 0.0, 0.17615),
        (7, 9, 0.0, 0.11001),
        (9, 10, 0.03181, 0.08450),
        (9, 14, 0.12711, 0.27038),
        (10, 11, 0.08205, 0.19207),
        (12, 13, 0.22092, 0.19988),
        (13, 14, 0.17093, 0.34802),
    ]
    bus_count = 14
    admittance_matrix: NDArray[np.complex128] = np.zeros((bus_count, bus_count), dtype=np.complex128)

    for from_bus, to_bus, resistance, reactance in branch_data:
        branch_impedance = complex(resistance, reactance)
        branch_admittance = 1 / branch_impedance
        first_index = from_bus - 1
        second_index = to_bus - 1
        admittance_matrix[first_index, first_index] += branch_admittance
        admittance_matrix[second_index, second_index] += branch_admittance
        admittance_matrix[first_index, second_index] -= branch_admittance
        admittance_matrix[second_index, first_index] -= branch_admittance

    return admittance_matrix, 0


def build_ieee14_full_admittance_matrix() -> tuple[NDArray[np.complex128], int]:
    branch_data = [
        (1, 2, 0.01938, 0.05917, 0.0528, 0.0),
        (1, 5, 0.05403, 0.22304, 0.0492, 0.0),
        (2, 3, 0.04699, 0.19797, 0.0438, 0.0),
        (2, 4, 0.05811, 0.17632, 0.0340, 0.0),
        (2, 5, 0.05695, 0.17388, 0.0346, 0.0),
        (3, 4, 0.06701, 0.17103, 0.0128, 0.0),
        (4, 5, 0.01335, 0.04211, 0.0, 0.0),
        (4, 7, 0.0, 0.20912, 0.0, 0.978),
        (4, 9, 0.0, 0.55618, 0.0, 0.969),
        (5, 6, 0.0, 0.25202, 0.0, 0.932),
        (6, 11, 0.09498, 0.19890, 0.0, 0.0),
        (6, 12, 0.12291, 0.25581, 0.0, 0.0),
        (6, 13, 0.06615, 0.13027, 0.0, 0.0),
        (7, 8, 0.0, 0.17615, 0.0, 0.0),
        (7, 9, 0.0, 0.11001, 0.0, 0.0),
        (9, 10, 0.03181, 0.08450, 0.0, 0.0),
        (9, 14, 0.12711, 0.27038, 0.0, 0.0),
        (10, 11, 0.08205, 0.19207, 0.0, 0.0),
        (12, 13, 0.22092, 0.19988, 0.0, 0.0),
        (13, 14, 0.17093, 0.34802, 0.0, 0.0),
    ]
    bus_count = 14
    admittance_matrix: NDArray[np.complex128] = np.zeros((bus_count, bus_count), dtype=np.complex128)

    for from_bus, to_bus, resistance, reactance, line_charging, tap_ratio in branch_data:
        branch_admittance = 1 / complex(resistance, reactance)
        first_index = from_bus - 1
        second_index = to_bus - 1
        tap = tap_ratio if tap_ratio else 1.0
        admittance_matrix[first_index, first_index] += branch_admittance / (tap * tap) + 0.5j * line_charging
        admittance_matrix[second_index, second_index] += branch_admittance + 0.5j * line_charging
        admittance_matrix[first_index, second_index] -= branch_admittance / tap
        admittance_matrix[second_index, first_index] -= branch_admittance / tap

    return admittance_matrix, 0


def get_test_system_2_converters(
    penetration_capacity_mva: float,
    system_base_mva: float = TEST_SYSTEM_2_SYSTEM_BASE_MVA,
) -> list[dict[str, float | int | str]]:
    scale = penetration_capacity_mva / system_base_mva
    parameters = PAPER_VALIDATION_TARGETS["test_system_2"]["table_10_parameters"]
    return [
        {
            "bus": bus,
            "p_ref": float(parameters["p_ref_pu"]) * scale,
            "q_ref": float(parameters["q_ref_pu"]) * scale,
            "i_max": float(parameters["i_vsc_max_pu"]) * scale,
            "control_mode": "PQ",
            "saturation_preference": "PSS",
            "k_isp": float(parameters["k_isp"]),
            "u_ref_gs": 1.0,
        }
        for bus in TEST_SYSTEM_2_VSC_BUSES
    ]


def per_unit_current_to_ka(current_pu: float, system_base_mva: float, voltage_base_kv: float) -> float:
    return current_pu * system_base_mva / (np.sqrt(3.0) * voltage_base_kv)
