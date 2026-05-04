"""Tests for unified model quality diagnostics."""

from __future__ import annotations

import numpy as np

from cloudpss_skills_v2.core.system_model import Branch, Bus, Generator, Load, PowerSystemModel
from cloudpss_skills_v2.powerapi.model_quality import (
    diagnose_unified_model,
    evaluate_matpower_cpf_output,
)


def _base_model() -> PowerSystemModel:
    return PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Slack", base_kv=230.0, bus_type="SLACK", v_magnitude_pu=1.0),
            Bus(bus_id=1, name="Load", base_kv=230.0, bus_type="PQ", v_magnitude_pu=0.98),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="Line", r_pu=0.02, x_pu=0.08, rate_a_mva=100.0),
        ],
        generators=[
            Generator(
                bus_id=0,
                name="G",
                p_gen_mw=60.0,
                p_max_mw=200.0,
                p_min_mw=0.0,
                q_max_mvar=100.0,
                q_min_mvar=-100.0,
                v_set_pu=1.0,
            )
        ],
        loads=[
            Load(bus_id=1, name="L", p_mw=50.0, q_mvar=10.0),
        ],
        base_mva=100.0,
        source_engine="unit_test",
    )


def test_model_quality_passes_for_complete_two_bus_model():
    report = diagnose_unified_model(_base_model(), include_matpower=True)

    assert report["status"] == "pass"
    assert report["summary"]["bus_count"] == 2
    assert report["summary"]["branch_type_counts"] == {"LINE": 1}
    assert report["parameter_quality"]["zero_impedance_branch_count"] == 0
    assert report["engine_readiness"]["pandapower"]["convertible"] is True
    assert report["engine_readiness"]["matpower"]["convertible"] is True
    assert report["engine_readiness"]["matpower"]["bus_shape"] == [2, 13]


def test_model_quality_warns_on_cloudpss_default_like_branch_reactance():
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Slack", base_kv=500.0, bus_type="SLACK"),
            Bus(bus_id=1, name="Load", base_kv=500.0, bus_type="PQ"),
            Bus(bus_id=2, name="Load2", base_kv=500.0, bus_type="PQ"),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="StaticLine", r_pu=0.001, x_pu=0.03),
            Branch(from_bus=1, to_bus=2, name="DefaultLike", r_pu=0.0, x_pu=0.01),
        ],
        generators=[Generator(bus_id=0, name="G", p_gen_mw=80.0, p_max_mw=200.0, p_min_mw=0.0)],
        loads=[Load(bus_id=1, name="L", p_mw=70.0, q_mvar=20.0)],
    )

    report = diagnose_unified_model(model)

    assert report["status"] == "warning"
    assert report["parameter_quality"]["default_like_x_pu_branch_count"] == 1
    assert any(item["code"] == "default_like_branch_reactance" for item in report["findings"])


def test_model_quality_fails_on_all_zero_impedance_path():
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Slack", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="Load", base_kv=230.0, bus_type="PQ"),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="BadLine", r_pu=0.0, x_pu=0.0),
        ],
        generators=[Generator(bus_id=0, name="G", p_gen_mw=50.0, p_max_mw=100.0, p_min_mw=0.0)],
        loads=[Load(bus_id=1, name="L", p_mw=40.0, q_mvar=10.0)],
    )

    report = diagnose_unified_model(model, include_matpower=True)

    assert report["status"] == "fail"
    assert report["parameter_quality"]["zero_impedance_branch_count"] == 1
    assert any(item["code"] == "zero_branch_impedance" for item in report["findings"])


def test_model_quality_fails_structurally_without_active_branches():
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Slack", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="Load", base_kv=230.0, bus_type="PQ"),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="OffLine", r_pu=0.02, x_pu=0.08, in_service=False),
        ],
        generators=[Generator(bus_id=0, name="G", p_gen_mw=50.0, p_max_mw=100.0, p_min_mw=0.0)],
        loads=[Load(bus_id=1, name="L", p_mw=40.0, q_mvar=10.0)],
    )

    report = diagnose_unified_model(model)

    assert report["status"] == "fail"
    assert report["structural_quality"]["critical_physical_violation_count"] >= 1
    assert any(item["code"] == "no_active_branches" for item in report["findings"])


def test_cpf_output_quality_requires_finite_loadability_and_trace():
    model_quality = diagnose_unified_model(_base_model(), include_matpower=True)
    cpf_result = {
        "success": True,
        "max_lambda": 1.25,
        "cpf": {
            "lam": np.array([0.0, 0.5, 1.25]),
            "V": np.array([[1.0, 0.99, 0.97], [0.98, 0.9, 0.82]]),
        },
    }
    pv_curve = [{"bus": "Load", "scale": 1.25, "voltage": 0.82}]

    quality = evaluate_matpower_cpf_output(model_quality, cpf_result, pv_curve)

    assert quality["status"] == "pass"
    assert quality["has_finite_max_loadability"] is True
    assert quality["pv_curve_points"] == 1


def test_cpf_output_quality_fails_nonfinite_lambda():
    model_quality = diagnose_unified_model(_base_model(), include_matpower=True)
    quality = evaluate_matpower_cpf_output(
        model_quality,
        {"success": True, "max_lambda": float("nan"), "cpf": {"lam": np.array([0.0, np.nan])}},
        [],
    )

    assert quality["status"] == "fail"
    assert any(item["code"] == "missing_max_lambda" for item in quality["findings"])
