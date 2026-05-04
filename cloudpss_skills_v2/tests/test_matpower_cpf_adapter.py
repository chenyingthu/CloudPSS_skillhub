"""Tests for optional MATPOWER CPF integration."""

from __future__ import annotations

import numpy as np

from cloudpss_skills_v2.core.system_model import Branch, Bus, Generator, Load, PowerSystemModel
from cloudpss_skills_v2.powerapi.adapters.matpower_cpf import MatpowerCPFAdapter
from cloudpss_skills_v2.poweranalysis.voltage_stability import VoltageStabilityAnalysis


def _sample_model() -> PowerSystemModel:
    return PowerSystemModel(
        buses=[
            Bus(bus_id=1, name="Slack", base_kv=230.0, bus_type="SLACK", v_magnitude_pu=1.0),
            Bus(bus_id=2, name="Load", base_kv=230.0, bus_type="PQ", v_magnitude_pu=0.98),
        ],
        branches=[
            Branch(from_bus=1, to_bus=2, name="Line1", r_pu=0.01, x_pu=0.1, rate_a_mva=100),
        ],
        generators=[
            Generator(bus_id=1, name="G1", p_gen_mw=80, p_max_mw=200, p_min_mw=0),
        ],
        loads=[
            Load(bus_id=2, name="L1", p_mw=50, q_mvar=10),
        ],
        base_mva=100.0,
    )


def test_matpower_cpf_adapter_builds_base_and_target_cases():
    adapter = MatpowerCPFAdapter()

    base, target = adapter.build_cases(_sample_model(), target_scale=2.0)

    assert base["baseMVA"] == 100.0
    assert base["bus"].shape == (2, 13)
    assert base["gen"].shape == (1, 10)
    assert base["branch"].shape == (1, 13)
    assert base["bus"][1, 2] == 50
    assert target["bus"][1, 2] == 100
    assert target["bus"][1, 3] == 20


def test_matpower_cpf_runtime_status_is_structured():
    status = MatpowerCPFAdapter.runtime_status()

    assert set(status) == {
        "matpower_python",
        "oct2py",
        "matlab_engine",
        "octave",
        "matlab",
        "available_octave",
        "available_matlab",
        "available",
    }
    assert isinstance(status["available"], bool)
    assert isinstance(status["available_octave"], bool)
    assert isinstance(status["available_matlab"], bool)


def test_matpower_cpf_normalizes_tuple_result():
    result = MatpowerCPFAdapter._normalize_result({
        "cpf": {"lam": np.array([0.0, 0.5, 1.2])},
    })

    assert result["success"] is True
    assert result["max_lambda"] == 1.2


def test_matpower_cpf_extracts_monitored_pv_curve_from_arrays():
    model = _sample_model()
    cpf = {
        "V": np.array([
            [1.0 + 0j, 0.99 + 0j, 0.97 + 0j],
            [0.98 + 0j, 0.90 + 0j, 0.82 + 0j],
        ]),
        "lam": np.array([0.0, 0.5, 1.0]),
    }

    points = VoltageStabilityAnalysis._extract_matpower_pv_curve(
        model=model,
        cpf=cpf,
        monitor_buses=["Load"],
    )

    assert points == [
        {"bus": "Load", "scale": 0.0, "voltage": 0.98, "source": "matpower_runcpf"},
        {"bus": "Load", "scale": 0.5, "voltage": 0.9, "source": "matpower_runcpf"},
        {"bus": "Load", "scale": 1.0, "voltage": 0.82, "source": "matpower_runcpf"},
    ]
