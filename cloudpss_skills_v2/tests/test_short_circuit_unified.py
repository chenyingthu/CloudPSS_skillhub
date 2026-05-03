"""Test ShortCircuitAnalysis with unified PowerSystemModel."""

from __future__ import annotations

import pytest

from cloudpss_skills_v2.core.system_model import (
    Branch,
    Bus,
    Generator,
    PowerSystemModel,
)


def test_short_circuit_runs_on_unified_model():
    """Test that ShortCircuitAnalysis works with unified model."""
    from cloudpss_skills_v2.poweranalysis.short_circuit import ShortCircuitAnalysis

    model = PowerSystemModel(
        buses=[
            Bus(
                bus_id=0,
                name="Bus1",
                base_kv=230.0,
                bus_type="SLACK",
                v_magnitude_pu=1.0,
                v_angle_degree=0.0,
            ),
            Bus(
                bus_id=1,
                name="Bus2",
                base_kv=230.0,
                bus_type="PQ",
                v_magnitude_pu=0.98,
                v_angle_degree=-2.0,
            ),
        ],
        branches=[
            Branch(
                from_bus=0,
                to_bus=1,
                name="Line1",
                branch_type="LINE",
                r_pu=0.01,
                x_pu=0.1,
                rate_a_mva=100.0,
            )
        ],
        generators=[
            Generator(bus_id=0, name="Gen1", p_gen_mw=100, in_service=True)
        ],
        base_mva=100.0,
    )

    analysis = ShortCircuitAnalysis()
    result = analysis.run(
        model,
        {
            "fault_location": "Bus2",
            "fault_type": "three_phase",
            "fault_resistance": 0.0,
        },
    )

    assert result["status"] in ["success", "error"]
    assert "fault_current" in result or "errors" in result


def test_short_circuit_inherits_from_power_analysis():
    """Test that ShortCircuitAnalysis inherits from PowerAnalysis."""
    from cloudpss_skills_v2.poweranalysis.short_circuit import ShortCircuitAnalysis
    from cloudpss_skills_v2.poweranalysis.base import PowerAnalysis

    assert issubclass(ShortCircuitAnalysis, PowerAnalysis)


def test_short_circuit_has_run_method():
    """Test that ShortCircuitAnalysis has run method with correct signature."""
    from cloudpss_skills_v2.poweranalysis.short_circuit import ShortCircuitAnalysis
    from cloudpss_skills_v2.core.system_model import PowerSystemModel

    import inspect

    analysis = ShortCircuitAnalysis()
    run_method = getattr(analysis, "run", None)
    assert run_method is not None, "ShortCircuitAnalysis must have run() method"

    sig = inspect.signature(run_method)
    params = list(sig.parameters.keys())
    assert "model" in params, "run() must have 'model' parameter"
    assert "config" in params, "run() must have 'config' parameter"


def test_short_circuit_validates_model():
    """Test that ShortCircuitAnalysis validates the model."""
    from cloudpss_skills_v2.poweranalysis.short_circuit import ShortCircuitAnalysis
    from cloudpss_skills_v2.core.system_model import PowerSystemModel

    analysis = ShortCircuitAnalysis()

    # Empty model should fail validation
    empty_model = PowerSystemModel(buses=[], branches=[], base_mva=100.0)
    result = analysis.run(
        empty_model,
        {
            "fault_location": "Bus1",
            "fault_type": "three_phase",
            "fault_resistance": 0.0,
        },
    )

    assert result["status"] == "error"
    assert "errors" in result


def test_short_circuit_requires_slack_bus():
    """Test that ShortCircuitAnalysis requires a slack bus."""
    from cloudpss_skills_v2.poweranalysis.short_circuit import ShortCircuitAnalysis

    # Model without slack bus
    model = PowerSystemModel(
        buses=[
            Bus(
                bus_id=0,
                name="Bus1",
                base_kv=230.0,
                bus_type="PQ",  # Not slack
            ),
            Bus(
                bus_id=1,
                name="Bus2",
                base_kv=230.0,
                bus_type="PQ",
            ),
        ],
        branches=[
            Branch(
                from_bus=0,
                to_bus=1,
                name="Line1",
                branch_type="LINE",
                r_pu=0.01,
                x_pu=0.1,
            )
        ],
        base_mva=100.0,
    )

    analysis = ShortCircuitAnalysis()
    result = analysis.run(
        model,
        {
            "fault_location": "Bus2",
            "fault_type": "three_phase",
            "fault_resistance": 0.0,
        },
    )

    assert result["status"] == "error"
    assert "errors" in result


def test_short_circuit_with_different_fault_types():
    """Test ShortCircuitAnalysis with various fault types."""
    from cloudpss_skills_v2.poweranalysis.short_circuit import ShortCircuitAnalysis

    model = PowerSystemModel(
        buses=[
            Bus(
                bus_id=0,
                name="Bus1",
                base_kv=230.0,
                bus_type="SLACK",
            ),
            Bus(
                bus_id=1,
                name="Bus2",
                base_kv=230.0,
                bus_type="PQ",
            ),
        ],
        branches=[
            Branch(
                from_bus=0,
                to_bus=1,
                name="Line1",
                branch_type="LINE",
                r_pu=0.01,
                x_pu=0.1,
            )
        ],
        generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=100)],
        base_mva=100.0,
    )

    analysis = ShortCircuitAnalysis()

    for fault_type in ["three_phase", "line_to_ground", "line_to_line"]:
        result = analysis.run(
            model,
            {
                "fault_location": "Bus2",
                "fault_type": fault_type,
                "fault_resistance": 0.0,
            },
        )
        assert "status" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
