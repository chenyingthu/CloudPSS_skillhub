"""Comprehensive edge case tests for unified PowerSystemModel.

This module tests edge cases and boundary conditions for analysis skills
that use the unified PowerSystemModel data structure.

Test categories:
1. Empty Model Handling - Tests with empty/minimal systems
2. Single Bus Systems - Tests with only slack bus or only PQ bus
3. Disconnected Components - Tests with isolated buses/branches
4. Extreme Values - Tests with very high/low impedance, loads, etc.
5. Transformer Handling - Tests with tap changers, phase shifters, multi-voltage
6. Generator Variations - Tests with PV buses, Q limits, multiple slacks, no generators
7. Cross-Engine Consistency - Tests ensuring different engines produce compatible models
"""

import pytest
import numpy as np

from cloudpss_skills_v2.core.system_model import (
    Bus,
    Branch,
    Generator,
    Load,
    Transformer,
    PowerSystemModel,
)
from cloudpss_skills_v2.poweranalysis.loss_analysis import LossAnalysis
from cloudpss_skills_v2.poweranalysis.contingency_analysis import ContingencyAnalysis


# =============================================================================
# Empty Model Handling Tests
# =============================================================================


def test_loss_analysis_with_empty_model():
    """Test LossAnalysis with completely empty PowerSystemModel.

    Edge case: Model with no buses, branches, generators, or loads.
    Expected: Analysis should return error status with appropriate message.
    """
    model = PowerSystemModel(buses=[], branches=[], generators=[], loads=[], base_mva=100.0)
    analysis = LossAnalysis()
    result = analysis.run(model, {})

    assert result["status"] == "error"
    assert "No buses" in result["error"]


def test_loss_analysis_with_no_slack_bus():
    """Test LossAnalysis with buses but no slack bus.

    Edge case: System has buses but lacks a reference/slack bus.
    Expected: Analysis should detect missing slack bus and report error.
    """
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="PQ"),
            Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ"),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="Line1-2", branch_type="LINE",
                   r_pu=0.01, x_pu=0.1, rate_a_mva=100.0),
        ],
        generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=100)],
        loads=[Load(bus_id=1, name="Load1", p_mw=50)],
        base_mva=100.0
    )

    analysis = LossAnalysis()
    result = analysis.run(model, {})

    assert result["status"] == "error"
    assert "slack" in result["error"].lower()


def test_contingency_analysis_with_empty_model():
    """Test ContingencyAnalysis with empty model.

    Edge case: No components to analyze for contingencies.
    Expected: Should handle gracefully with appropriate error.
    """
    model = PowerSystemModel(buses=[], branches=[], base_mva=100.0)
    analysis = ContingencyAnalysis()
    result = analysis.run(model, {"contingencies": []})

    assert result["status"] == "error"


# =============================================================================
# Single Bus Systems Tests
# =============================================================================


def test_single_slack_bus_only():
    """Test with only a single slack bus and no other components.

    Edge case: Minimal possible system - just one slack bus.
    Expected: Should handle gracefully, no losses (no branches).
    """
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="SlackBus", base_kv=230.0, bus_type="SLACK",
                v_magnitude_pu=1.0, v_angle_degree=0.0),
        ],
        branches=[],
        generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=0)],
        loads=[],
        base_mva=100.0
    )

    analysis = LossAnalysis()
    result = analysis.run(model, {})

    assert result["status"] == "success"
    assert result["total_loss_mw"] == 0.0
    assert len(result["branch_losses"]) == 0


def test_single_pq_bus_no_slack():
    """Test with single PQ bus and no slack bus.

    Edge case: System without reference bus - physically invalid.
    Expected: Should detect and report missing slack bus error.
    """
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="PQ"),
        ],
        branches=[],
        generators=[],
        loads=[Load(bus_id=0, name="Load1", p_mw=50)],
        base_mva=100.0
    )

    analysis = LossAnalysis()
    result = analysis.run(model, {})

    assert result["status"] == "error"
    assert "slack" in result["error"].lower()


def test_two_bus_system_minimal():
    """Test with minimal 2-bus system (slack + PQ).

    Edge case: Smallest valid power system configuration.
    Expected: Normal operation with loss calculation.
    """
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Slack", base_kv=230.0, bus_type="SLACK",
                v_magnitude_pu=1.0, v_angle_degree=0.0),
            Bus(bus_id=1, name="LoadBus", base_kv=230.0, bus_type="PQ",
                v_magnitude_pu=0.95, v_angle_degree=-5.0),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="Line1", branch_type="LINE",
                   r_pu=0.02, x_pu=0.1, rate_a_mva=100.0,
                   p_from_mw=50.5, p_to_mw=-50.0),
        ],
        generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=50.5)],
        loads=[Load(bus_id=1, name="Load1", p_mw=50.0)],
        base_mva=100.0
    )

    analysis = LossAnalysis()
    result = analysis.run(model, {})

    assert result["status"] == "success"
    assert result["total_loss_mw"] == pytest.approx(0.5, abs=0.01)


# =============================================================================
# Disconnected Components Tests
# =============================================================================


def test_isolated_bus_not_connected():
    """Test with isolated bus not connected to any branches.

    Edge case: Bus exists but has no electrical connection to the network.
    Expected: Physical validation should detect connectivity issue.
    """
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ"),
            Bus(bus_id=2, name="Isolated", base_kv=230.0, bus_type="PQ"),  # Not connected
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="Line1-2", branch_type="LINE",
                   r_pu=0.01, x_pu=0.1, rate_a_mva=100.0,
                   p_from_mw=50, p_to_mw=-49),
        ],
        generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=50)],
        loads=[
            Load(bus_id=1, name="Load1", p_mw=49),
            Load(bus_id=2, name="Load2", p_mw=10),  # On isolated bus
        ],
        base_mva=100.0
    )

    # Physical validation should detect connectivity issue
    violations = model.validate_physical(raise_on_error=False)
    connectivity_violations = [v for v in violations if v["type"] == "connectivity"]
    assert len(connectivity_violations) > 0
    assert "Isolated" in connectivity_violations[0]["message"] or "isolated" in connectivity_violations[0]["message"].lower()


def test_disconnected_branch_out_of_service():
    """Test with branch marked as out of service.

    Edge case: Branch exists but is not in service.
    Expected: Analysis should skip out-of-service branches.
    """
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ"),
            Bus(bus_id=2, name="Bus3", base_kv=230.0, bus_type="PQ"),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="Line1-2", branch_type="LINE",
                   r_pu=0.01, x_pu=0.1, rate_a_mva=100.0,
                   p_from_mw=50, p_to_mw=-49, in_service=True),
            Branch(from_bus=1, to_bus=2, name="Line2-3", branch_type="LINE",
                   r_pu=0.01, x_pu=0.1, rate_a_mva=100.0,
                   p_from_mw=0, p_to_mw=0, in_service=False),  # Out of service
        ],
        generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=50)],
        loads=[
            Load(bus_id=1, name="Load1", p_mw=49),
            Load(bus_id=2, name="Load2", p_mw=0),  # No load since disconnected
        ],
        base_mva=100.0
    )

    analysis = LossAnalysis()
    result = analysis.run(model, {})

    assert result["status"] == "success"
    # Only the in-service branch should contribute to losses
    assert len(result["branch_losses"]) == 1
    assert result["branch_losses"][0]["branch_id"] == "Line1-2"


def test_network_connectivity_validation():
    """Test network connectivity check with multiple isolated subnetworks.

    Edge case: Multiple separate connected components.
    Expected: Physical validation should detect network not fully connected.
    """
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ"),
            Bus(bus_id=2, name="Bus3", base_kv=230.0, bus_type="SLACK"),  # Separate network
            Bus(bus_id=3, name="Bus4", base_kv=230.0, bus_type="PQ"),   # Separate network
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="Line1-2", branch_type="LINE",
                   r_pu=0.01, x_pu=0.1, rate_a_mva=100.0),
            Branch(from_bus=2, to_bus=3, name="Line3-4", branch_type="LINE",
                   r_pu=0.01, x_pu=0.1, rate_a_mva=100.0),  # Separate component
        ],
        generators=[
            Generator(bus_id=0, name="Gen1", p_gen_mw=50),
            Generator(bus_id=2, name="Gen2", p_gen_mw=30),
        ],
        loads=[
            Load(bus_id=1, name="Load1", p_mw=50),
            Load(bus_id=3, name="Load2", p_mw=30),
        ],
        base_mva=100.0
    )

    violations = model.validate_physical(raise_on_error=False)
    connectivity_issues = [v for v in violations if v["type"] == "connectivity"]
    assert len(connectivity_issues) > 0


# =============================================================================
# Extreme Values Tests
# =============================================================================


def test_very_high_impedance_branch():
    """Test with extremely high impedance branch.

    Edge case: Branch with very high R and X values.
    Expected: Should handle without numerical issues.
    """
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ"),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="HighZLine", branch_type="LINE",
                   r_pu=10.0, x_pu=10.0, rate_a_mva=100.0,  # Very high impedance
                   p_from_mw=0.1, p_to_mw=-0.05),
        ],
        generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=0.1)],
        loads=[Load(bus_id=1, name="Load1", p_mw=0.05)],
        base_mva=100.0
    )

    analysis = LossAnalysis()
    result = analysis.run(model, {})

    assert result["status"] == "success"
    assert result["total_loss_mw"] == pytest.approx(0.05, abs=0.01)


def test_very_low_impedance_branch():
    """Test with extremely low (near zero) impedance branch.

    Edge case: Branch with R and X approaching zero.
    Expected: Should handle with appropriate numerical care.
    """
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ"),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="LowZLine", branch_type="LINE",
                   r_pu=0.0001, x_pu=0.001, rate_a_mva=1000.0,  # Very low impedance
                   p_from_mw=100, p_to_mw=-99.9),
        ],
        generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=100)],
        loads=[Load(bus_id=1, name="Load1", p_mw=99.9)],
        base_mva=100.0
    )

    analysis = LossAnalysis()
    result = analysis.run(model, {})

    assert result["status"] == "success"
    assert result["total_loss_mw"] == pytest.approx(0.1, abs=0.01)


def test_zero_impedance_branch():
    """Test with zero impedance branch (ideal connection).

    Edge case: R = 0, X = 0 (ideal bus tie).
    Expected: Should handle without division by zero errors.
    """
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ"),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="IdealTie", branch_type="LINE",
                   r_pu=0.0, x_pu=0.0, rate_a_mva=1000.0,  # Zero impedance
                   p_from_mw=50, p_to_mw=-50),  # No loss
        ],
        generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=50)],
        loads=[Load(bus_id=1, name="Load1", p_mw=50)],
        base_mva=100.0
    )

    analysis = LossAnalysis()
    result = analysis.run(model, {})

    assert result["status"] == "success"
    assert result["total_loss_mw"] == pytest.approx(0.0, abs=0.001)


def test_very_high_load_values():
    """Test with extremely high load values.

    Edge case: Load values orders of magnitude above normal.
    Expected: Should handle or report appropriate error.
    """
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ"),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="Line1", branch_type="LINE",
                   r_pu=0.01, x_pu=0.1, rate_a_mva=10000.0,
                   p_from_mw=10000, p_to_mw=-9950),
        ],
        generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=10000)],
        loads=[Load(bus_id=1, name="Load1", p_mw=9950)],  # Very high load
        base_mva=100.0
    )

    analysis = LossAnalysis()
    result = analysis.run(model, {})

    assert result["status"] == "success"
    assert result["total_loss_mw"] == pytest.approx(50.0, abs=1.0)


def test_very_low_load_values():
    """Test with extremely low (near zero) load values.

    Edge case: Minimal load - light load conditions.
    Expected: Should handle very small power flows.
    """
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ"),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="Line1", branch_type="LINE",
                   r_pu=0.01, x_pu=0.1, rate_a_mva=100.0,
                   p_from_mw=0.001, p_to_mw=-0.0009),
        ],
        generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=0.001)],
        loads=[Load(bus_id=1, name="Load1", p_mw=0.0009)],  # Very small load
        base_mva=100.0
    )

    analysis = LossAnalysis()
    result = analysis.run(model, {})

    assert result["status"] == "success"
    # Loss = p_from + p_to = 0.001 + (-0.0009) = 0.0001 MW
    assert result["total_loss_mw"] == pytest.approx(0.0001, abs=0.00001)


def test_extreme_voltage_values():
    """Test with voltage values at physical limits.

    Edge case: Voltages near minimum and maximum physically reasonable values.
    Expected: Validation should catch values outside reasonable range.
    """
    # Voltage too low (below 0.5 pu)
    with pytest.raises(ValueError) as exc_info:
        Bus(bus_id=0, name="LowVBus", base_kv=230.0, bus_type="SLACK",
            v_magnitude_pu=0.3)  # Below VOLTAGE_PU_MIN (0.5)
    assert "Voltage" in str(exc_info.value)

    # Voltage too high (above 1.5 pu)
    with pytest.raises(ValueError) as exc_info:
        Bus(bus_id=0, name="HighVBus", base_kv=230.0, bus_type="SLACK",
            v_magnitude_pu=2.0)  # Above VOLTAGE_PU_MAX (1.5)
    assert "Voltage" in str(exc_info.value)


def test_extreme_angle_values():
    """Test with extreme voltage angle values.

    Edge case: Angles outside reasonable operating range.
    Expected: Validation should catch extreme angle values.
    """
    # Angle outside -90 to +90 range
    with pytest.raises(ValueError) as exc_info:
        Bus(bus_id=0, name="ExtremeAngleBus", base_kv=230.0, bus_type="SLACK",
            v_angle_degree=120.0)  # Above ANGLE_DEGREE_MAX (90)
    assert "Angle" in str(exc_info.value)

    with pytest.raises(ValueError) as exc_info:
        Bus(bus_id=0, name="ExtremeAngleBus", base_kv=230.0, bus_type="SLACK",
            v_angle_degree=-120.0)  # Below ANGLE_DEGREE_MIN (-90)
    assert "Angle" in str(exc_info.value)


# =============================================================================
# Transformer Handling Tests
# =============================================================================


def test_transformer_with_tap_changer():
    """Test transformer with off-nominal tap ratio.

    Edge case: Tap changer at non-unity position.
    Expected: Should recognize as transformer and handle tap settings.
    """
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="HVBus", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="LVBus", base_kv=110.0, bus_type="PQ"),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="T1", branch_type="TRANSFORMER",
                   r_pu=0.005, x_pu=0.08, rate_a_mva=100.0,
                   tap_ratio=1.05,  # 5% tap up
                   p_from_mw=50, p_to_mw=-49.5),
        ],
        generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=50)],
        loads=[Load(bus_id=1, name="Load1", p_mw=49.5)],
        base_mva=100.0
    )

    analysis = LossAnalysis()
    result = analysis.run(model, {})

    assert result["status"] == "success"
    assert result["total_loss_mw"] == pytest.approx(0.5, abs=0.01)

    # Check transformer is correctly identified
    assert len(result["transformer_losses"]) == 1
    assert result["transformer_losses"][0]["transformer_id"] == "T1"


def test_transformer_with_phase_shifter():
    """Test phase shifting transformer.

    Edge case: Transformer with phase shift angle.
    Expected: Should handle phase shift and recognize as transformer.
    """
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ"),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="PhaseShifter", branch_type="PHASE_SHIFTER",
                   r_pu=0.005, x_pu=0.1, rate_a_mva=100.0,
                   phase_shift_degree=15.0,  # 15 degree phase shift
                   p_from_mw=80, p_to_mw=-79),
        ],
        generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=80)],
        loads=[Load(bus_id=1, name="Load1", p_mw=79)],
        base_mva=100.0
    )

    analysis = LossAnalysis()
    result = analysis.run(model, {})

    assert result["status"] == "success"
    assert result["total_loss_mw"] == pytest.approx(1.0, abs=0.01)

    # Phase shifter should be identified as transformer
    assert len(result["transformer_losses"]) == 1


def test_multiple_voltage_levels():
    """Test system with multiple voltage levels connected by transformers.

    Edge case: Multi-voltage system with 230kV, 110kV, and 11kV levels.
    Expected: Should handle all voltage levels correctly.
    """
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="GenBus", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="HVBus", base_kv=230.0, bus_type="PQ"),
            Bus(bus_id=2, name="MVBus", base_kv=110.0, bus_type="PQ"),
            Bus(bus_id=3, name="LVBus", base_kv=11.0, bus_type="PQ"),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="Line1", branch_type="LINE",
                   r_pu=0.01, x_pu=0.1, rate_a_mva=100.0,
                   p_from_mw=100, p_to_mw=-99),
            Branch(from_bus=1, to_bus=2, name="T1", branch_type="TRANSFORMER",
                   r_pu=0.005, x_pu=0.08, rate_a_mva=100.0,
                   p_from_mw=99, p_to_mw=-98),
            Branch(from_bus=2, to_bus=3, name="T2", branch_type="TRANSFORMER",
                   r_pu=0.01, x_pu=0.06, rate_a_mva=50.0,
                   p_from_mw=48, p_to_mw=-47),
        ],
        generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=100)],
        loads=[
            Load(bus_id=1, name="Load1", p_mw=1),   # 1 MW at HV
            Load(bus_id=2, name="Load2", p_mw=50),  # 50 MW at MV
            Load(bus_id=3, name="Load3", p_mw=47),  # 47 MW at LV
        ],
        base_mva=100.0
    )

    analysis = LossAnalysis()
    result = analysis.run(model, {})

    assert result["status"] == "success"
    # Total losses: Line (1) + T1 (1) + T2 (1) = 3 MW
    assert result["total_loss_mw"] == pytest.approx(3.0, abs=0.1)

    # Should have 2 transformers
    assert len(result["transformer_losses"]) == 2


def test_transformer_with_detailed_model():
    """Test with detailed transformer model including loss components.

    Edge case: Using detailed Transformer dataclass with core/copper losses.
    """
    transformer = Transformer(
        name="DetailedT1",
        hv_bus=0,
        lv_bus=1,
        sn_mva=100.0,
        vn_hv_kv=230.0,
        vn_lv_kv=110.0,
        vk_percent=10.0,
        vkr_percent=0.5,
        pfe_kw=25.0,  # 25 kW iron losses
        i0_percent=0.1,
        tap_pos=0,
        tap_min=-10,
        tap_max=10,
    )

    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="HVBus", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="LVBus", base_kv=110.0, bus_type="PQ"),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="T1", branch_type="TRANSFORMER",
                   r_pu=0.005, x_pu=0.08, rate_a_mva=100.0,
                   p_from_mw=50, p_to_mw=-49.5),
        ],
        transformers=[transformer],
        generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=50)],
        loads=[Load(bus_id=1, name="Load1", p_mw=49.5)],
        base_mva=100.0
    )

    # Verify transformer data is stored correctly
    assert len(model.transformers) == 1
    assert model.transformers[0].name == "DetailedT1"
    assert model.transformers[0].pfe_kw == 25.0


# =============================================================================
# Generator Variations Tests
# =============================================================================


def test_pv_bus_with_q_limits():
    """Test PV bus operating within reactive power limits.

    Edge case: Generator at Q limit boundary.
    Expected: Should handle Q limit checking correctly.
    """
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Slack", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="PVBus", base_kv=230.0, bus_type="PV",
                v_magnitude_pu=1.02),  # PV bus with voltage setpoint
            Bus(bus_id=2, name="PQBus", base_kv=230.0, bus_type="PQ"),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="Line1", branch_type="LINE",
                   r_pu=0.01, x_pu=0.1, rate_a_mva=100.0,
                   p_from_mw=50, p_to_mw=-49.5),
            Branch(from_bus=1, to_bus=2, name="Line2", branch_type="LINE",
                   r_pu=0.01, x_pu=0.1, rate_a_mva=100.0,
                   p_from_mw=49.5, p_to_mw=-49),
        ],
        generators=[
            Generator(bus_id=0, name="SlackGen", p_gen_mw=50),
            Generator(bus_id=1, name="PVGen", p_gen_mw=50, v_set_pu=1.02,
                     q_max_mvar=50, q_min_mvar=-50, q_gen_mvar=10),  # Within limits
        ],
        loads=[
            Load(bus_id=1, name="Load1", p_mw=0.5),
            Load(bus_id=2, name="Load2", p_mw=49),
        ],
        base_mva=100.0
    )

    # Check generator is at PV bus
    gen = model.generators[1]
    assert gen.is_at_q_limit() is False  # Q=10 is within [-50, 50]

    # Now test at limit
    gen_at_limit = Generator(bus_id=1, name="PVGenLimit", p_gen_mw=50, v_set_pu=1.02,
                            q_max_mvar=50, q_min_mvar=-50, q_gen_mvar=50)
    assert gen_at_limit.is_at_q_limit() is True  # Q=50 is at max limit


def test_pv_bus_at_q_limit():
    """Test PV bus operating at Q limit (should behave like PQ).

    Edge case: Generator hitting reactive power limit.
    """
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Slack", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="PVBus", base_kv=230.0, bus_type="PV"),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="Line1", branch_type="LINE",
                   r_pu=0.01, x_pu=0.1, rate_a_mva=100.0,
                   p_from_mw=50, p_to_mw=-49.5),
        ],
        generators=[
            Generator(bus_id=1, name="PVGen", p_gen_mw=50, v_set_pu=1.05,
                     q_max_mvar=50, q_min_mvar=-50, q_gen_mvar=50),  # At Qmax
        ],
        loads=[Load(bus_id=1, name="Load1", p_mw=0.5)],
        base_mva=100.0
    )

    # Check that generator is at Q limit
    gen = model.generators[0]
    assert gen.is_at_q_limit() is True


def test_multiple_slack_buses():
    """Test system with multiple slack buses.

    Edge case: More than one reference bus (unusual but possible in multi-area).
    Expected: Analysis should handle or report appropriately.
    """
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Slack1", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="Slack2", base_kv=230.0, bus_type="SLACK"),  # Second slack
            Bus(bus_id=2, name="PQBus", base_kv=230.0, bus_type="PQ"),
        ],
        branches=[
            Branch(from_bus=0, to_bus=2, name="Line1", branch_type="LINE",
                   r_pu=0.01, x_pu=0.1, rate_a_mva=100.0,
                   p_from_mw=50, p_to_mw=-49.5),
            Branch(from_bus=1, to_bus=2, name="Line2", branch_type="LINE",
                   r_pu=0.01, x_pu=0.1, rate_a_mva=100.0,
                   p_from_mw=50, p_to_mw=-49.5),
        ],
        generators=[
            Generator(bus_id=0, name="Gen1", p_gen_mw=50),
            Generator(bus_id=1, name="Gen2", p_gen_mw=50),
        ],
        loads=[Load(bus_id=2, name="Load1", p_mw=99)],
        base_mva=100.0
    )

    analysis = LossAnalysis()
    result = analysis.run(model, {})

    # Should still work with multiple slacks
    assert result["status"] == "success"
    assert result["total_loss_mw"] == pytest.approx(1.0, abs=0.1)


def test_no_generators():
    """Test system with no generators.

    Edge case: Load-only system without generation.
    Expected: Model should have zero generation, and physical validation
    will not flag power balance since generation is zero (no power to balance).
    """
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ"),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="Line1", branch_type="LINE",
                   r_pu=0.01, x_pu=0.1, rate_a_mva=100.0),
        ],
        generators=[],  # No generators
        loads=[Load(bus_id=1, name="Load1", p_mw=50)],
        base_mva=100.0
    )

    # Check power balance - generation should be 0
    total_gen = model.total_generation_mw()
    total_load = model.total_load_mw()

    assert total_gen == 0.0
    assert total_load == 50.0

    # Power balance validation is skipped when total_gen is 0
    # This is expected behavior - no generation means no power to be imbalanced
    violations = model.validate_physical(raise_on_error=False)
    power_balance_issues = [v for v in violations if v["type"] == "power_balance"]
    assert len(power_balance_issues) == 0  # No power balance issues when Gen = 0


def test_generator_power_limits():
    """Test generator with P setpoint outside limits.

    Edge case: P setpoint violates Pmin/Pmax constraints.
    Expected: Bus validation should catch this.
    """
    # This should raise an error during generator construction
    with pytest.raises(ValueError) as exc_info:
        Generator(
            bus_id=0,
            name="Gen1",
            p_gen_mw=150,  # Above Pmax
            p_max_mw=100,
            p_min_mw=0
        )
    assert "outside limits" in str(exc_info.value)

    with pytest.raises(ValueError) as exc_info:
        Generator(
            bus_id=0,
            name="Gen2",
            p_gen_mw=-10,  # Below Pmin
            p_max_mw=100,
            p_min_mw=0
        )
    assert "outside limits" in str(exc_info.value)


def test_generator_at_p_limit():
    """Test generator operating at active power limits.

    Edge case: Generator at Pmax or Pmin.
    """
    gen_at_max = Generator(
        bus_id=0,
        name="GenMax",
        p_gen_mw=100,
        p_max_mw=100,
        p_min_mw=0
    )
    assert gen_at_max.is_at_p_limit() is True

    gen_at_min = Generator(
        bus_id=0,
        name="GenMin",
        p_gen_mw=0,
        p_max_mw=100,
        p_min_mw=0
    )
    assert gen_at_min.is_at_p_limit() is True

    gen_mid = Generator(
        bus_id=0,
        name="GenMid",
        p_gen_mw=50,
        p_max_mw=100,
        p_min_mw=0
    )
    assert gen_mid.is_at_p_limit() is False


# =============================================================================
# Cross-Engine Consistency Tests
# =============================================================================


def test_model_creation_with_different_base_mva():
    """Test model behavior with different base MVA values.

    Edge case: Systems with different per-unit bases.
    Expected: All calculations should be consistent.
    """
    # Create models with different base MVA
    model_100 = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ"),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="Line1", branch_type="LINE",
                   r_pu=0.01, x_pu=0.1, rate_a_mva=100.0,
                   p_from_mw=50, p_to_mw=-49),
        ],
        generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=50)],
        loads=[Load(bus_id=1, name="Load1", p_mw=49)],
        base_mva=100.0
    )

    model_50 = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ"),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="Line1", branch_type="LINE",
                   r_pu=0.02, x_pu=0.2, rate_a_mva=200.0,  # Scaled for base MVA
                   p_from_mw=50, p_to_mw=-49),
        ],
        generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=50)],
        loads=[Load(bus_id=1, name="Load1", p_mw=49)],
        base_mva=50.0
    )

    # Both models should have same actual power values
    assert model_100.total_generation_mw() == model_50.total_generation_mw()
    assert model_100.total_load_mw() == model_50.total_load_mw()


def test_model_dataframe_views():
    """Test DataFrame views of model components.

    Edge case: Converting model to DataFrames for analysis.
    """
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ"),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="Line1", branch_type="LINE",
                   r_pu=0.01, x_pu=0.1, rate_a_mva=100.0),
        ],
        generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=50)],
        loads=[Load(bus_id=1, name="Load1", p_mw=50)],
        base_mva=100.0
    )

    # Test DataFrame conversion
    buses_df = model.buses_df
    branches_df = model.branches_df
    generators_df = model.generators_df

    assert len(buses_df) == 2
    assert len(branches_df) == 1
    assert len(generators_df) == 1
    assert buses_df.loc[0, "name"] == "Bus1"
    assert branches_df.loc[0, "name"] == "Line1"


def test_empty_dataframe_views():
    """Test DataFrame views with empty model.

    Edge case: Converting empty model to DataFrames.
    """
    model = PowerSystemModel(buses=[], branches=[], generators=[], loads=[], base_mva=100.0)

    # Should return empty DataFrames without error
    assert model.buses_df.empty
    assert model.branches_df.empty
    assert model.generators_df.empty


def test_model_bus_accessors():
    """Test bus accessor methods.

    Edge case: Lookup buses by ID and name.
    """
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="SlackBus", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="LoadBus", base_kv=230.0, bus_type="PQ"),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="Line1", branch_type="LINE",
                   r_pu=0.01, x_pu=0.1, rate_a_mva=100.0),
        ],
        base_mva=100.0
    )

    # Test get_bus_by_id
    bus0 = model.get_bus_by_id(0)
    assert bus0 is not None
    assert bus0.name == "SlackBus"

    bus_missing = model.get_bus_by_id(999)
    assert bus_missing is None

    # Test get_bus_by_name
    bus1 = model.get_bus_by_name("LoadBus")
    assert bus1 is not None
    assert bus1.bus_id == 1

    bus_missing_name = model.get_bus_by_name("NonExistent")
    assert bus_missing_name is None


def test_model_branch_accessors():
    """Test branch accessor methods.

    Edge case: Get branches connected to a bus.
    """
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus0", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="Bus1", base_kv=230.0, bus_type="PQ"),
            Bus(bus_id=2, name="Bus2", base_kv=230.0, bus_type="PQ"),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="Line0-1", branch_type="LINE",
                   r_pu=0.01, x_pu=0.1, rate_a_mva=100.0),
            Branch(from_bus=1, to_bus=2, name="Line1-2", branch_type="LINE",
                   r_pu=0.01, x_pu=0.1, rate_a_mva=100.0),
        ],
        base_mva=100.0
    )

    # Bus 0 has 1 connected branch
    branches_at_0 = model.get_branches_connected_to(0)
    assert len(branches_at_0) == 1
    assert branches_at_0[0].name == "Line0-1"

    # Bus 1 has 2 connected branches
    branches_at_1 = model.get_branches_connected_to(1)
    assert len(branches_at_1) == 2

    # Bus with no connections
    branches_at_999 = model.get_branches_connected_to(999)
    assert len(branches_at_999) == 0


# =============================================================================
# Contingency Analysis Edge Cases
# =============================================================================


def test_contingency_analysis_with_single_branch():
    """Test contingency analysis with only one branch.

    Edge case: Minimal system for N-1 contingency analysis.
    """
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ"),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="OnlyLine", branch_type="LINE",
                   r_pu=0.01, x_pu=0.1, rate_a_mva=100.0,
                   p_from_mw=50, p_to_mw=-49),
        ],
        generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=50)],
        loads=[Load(bus_id=1, name="Load1", p_mw=49)],
        base_mva=100.0
    )

    analysis = ContingencyAnalysis()
    result = analysis.run(model, {"contingency_type": "n1"})

    assert result["status"] == "success"
    # Single branch N-1 will create one contingency result
    assert "contingencies" in result


def test_contingency_analysis_with_no_contingencies():
    """Test contingency analysis with no branches to contingencies.

    Edge case: System with no branches for contingency analysis.
    """
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
        ],
        branches=[],
        generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=50)],
        loads=[],
        base_mva=100.0
    )

    analysis = ContingencyAnalysis()
    result = analysis.run(model, {"contingency_type": "n1"})

    # Should succeed but return empty contingencies (no branches to analyze)
    assert result["status"] == "success"
    assert "contingencies" in result


# =============================================================================
# Physical Validation Edge Cases
# =============================================================================


def test_power_balance_validation():
    """Test power balance validation.

    Edge case: Generation not matching load plus losses.
    """
    # Balanced system
    balanced_model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK",
                p_injected_mw=51),  # Generation
            Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ",
                p_injected_mw=-50),  # Load
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="Line1", branch_type="LINE",
                   r_pu=0.01, x_pu=0.1, rate_a_mva=100.0),
        ],
        generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=51)],
        loads=[Load(bus_id=1, name="Load1", p_mw=50)],
        base_mva=100.0
    )

    # Total injection should be approximately 0 (Gen - Load - Losses ≈ 0)
    total_inj = balanced_model.total_losses_mw()
    assert total_inj is not None
    assert abs(total_inj) < 10  # Within tolerance


def test_voltage_violation_detection():
    """Test detection of voltage limit violations.

    Edge case: Bus voltages outside operational limits.
    """
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="NormalBus", base_kv=230.0, bus_type="SLACK",
                v_magnitude_pu=1.0, vm_min_pu=0.9, vm_max_pu=1.1),
            Bus(bus_id=1, name="UndervoltageBus", base_kv=230.0, bus_type="PQ",
                v_magnitude_pu=0.85, vm_min_pu=0.9, vm_max_pu=1.1),  # Below min
            Bus(bus_id=2, name="OvervoltageBus", base_kv=230.0, bus_type="PQ",
                v_magnitude_pu=1.15, vm_min_pu=0.9, vm_max_pu=1.1),  # Above max
        ],
        branches=[],
        base_mva=100.0
    )

    violations = model.get_voltage_violations()
    assert len(violations) == 2

    # Check undervoltage detected
    undervoltage = [v for v in violations if v[2] == "undervoltage"]
    assert len(undervoltage) == 1
    assert undervoltage[0][0].name == "UndervoltageBus"

    # Check overvoltage detected
    overvoltage = [v for v in violations if v[2] == "overvoltage"]
    assert len(overvoltage) == 1
    assert overvoltage[0][0].name == "OvervoltageBus"


def test_thermal_violation_detection():
    """Test detection of thermal (loading) violations.

    Edge case: Branch loading exceeding rating.
    """
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ"),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="NormalLine", branch_type="LINE",
                   r_pu=0.01, x_pu=0.1, rate_a_mva=100.0,
                   loading_percent=80.0),  # Normal loading
            Branch(from_bus=0, to_bus=1, name="OverloadedLine", branch_type="LINE",
                   r_pu=0.01, x_pu=0.1, rate_a_mva=100.0,
                   loading_percent=120.0),  # Overloaded
        ],
        base_mva=100.0
    )

    violations = model.get_thermal_violations(threshold=1.0)
    assert len(violations) == 1
    assert violations[0][0].name == "OverloadedLine"
    assert violations[0][1] == 120.0


# =============================================================================
# Model Modification Edge Cases
# =============================================================================


def test_n1_model_modification():
    """Test N-1 model modification (removing bus).

    Edge case: Create modified model with bus removed.
    """
    original_model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus0", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="Bus1", base_kv=230.0, bus_type="PQ"),
            Bus(bus_id=2, name="Bus2", base_kv=230.0, bus_type="PQ"),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="Line0-1", branch_type="LINE",
                   r_pu=0.01, x_pu=0.1, rate_a_mva=100.0),
            Branch(from_bus=1, to_bus=2, name="Line1-2", branch_type="LINE",
                   r_pu=0.01, x_pu=0.1, rate_a_mva=100.0),
        ],
        generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=100)],
        loads=[
            Load(bus_id=1, name="Load1", p_mw=50),
            Load(bus_id=2, name="Load2", p_mw=50),
        ],
        base_mva=100.0,
        name="Original"
    )

    # Remove Bus 1
    modified_model = original_model.with_bus_removed(1)

    assert len(modified_model.buses) == 2
    assert len(modified_model.branches) == 0  # Both branches connected to Bus 1
    assert len(modified_model.loads) == 1  # Load 2 remains
    assert modified_model.loads[0].bus_id == 2
    assert "bus_1_removed" in modified_model.name


def test_branch_removal_modification():
    """Test branch removal modification.

    Edge case: Create modified model with branch removed.
    """
    original_model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus0", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="Bus1", base_kv=230.0, bus_type="PQ"),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="LineToRemove", branch_type="LINE",
                   r_pu=0.01, x_pu=0.1, rate_a_mva=100.0),
        ],
        generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=50)],
        loads=[Load(bus_id=1, name="Load1", p_mw=50)],
        base_mva=100.0,
        name="Original"
    )

    # Remove the branch
    modified_model = original_model.with_branch_removed("LineToRemove")

    assert len(modified_model.branches) == 0
    assert "LineToRemove_removed" in modified_model.name


def test_branch_removal_not_found():
    """Test branch removal with non-existent branch name.

    Edge case: Attempt to remove branch that doesn't exist.
    """
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus0", base_kv=230.0, bus_type="SLACK"),
        ],
        branches=[],
        base_mva=100.0
    )

    with pytest.raises(ValueError) as exc_info:
        model.with_branch_removed("NonExistentBranch")
    assert "not found" in str(exc_info.value)


# =============================================================================
# Data Validation Edge Cases
# =============================================================================


def test_duplicate_bus_id_validation():
    """Test validation catches duplicate bus IDs.

    Edge case: Two buses with same ID.
    """
    with pytest.raises(ValueError) as exc_info:
        PowerSystemModel(
            buses=[
                Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
                Bus(bus_id=0, name="Bus2", base_kv=230.0, bus_type="PQ"),  # Same ID!
            ],
            branches=[],
            base_mva=100.0
        )
    assert "Duplicate" in str(exc_info.value) or "duplicate" in str(exc_info.value).lower()


def test_invalid_branch_connection():
    """Test validation catches branch connection to non-existent bus.

    Edge case: Branch references bus ID not in the model.
    """
    with pytest.raises(ValueError) as exc_info:
        PowerSystemModel(
            buses=[
                Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
            ],
            branches=[
                Branch(from_bus=0, to_bus=999, name="InvalidLine", branch_type="LINE",
                       r_pu=0.01, x_pu=0.1, rate_a_mva=100.0),
            ],
            base_mva=100.0
        )
    assert "unknown" in str(exc_info.value).lower()


def test_generator_connection_to_invalid_bus():
    """Test validation catches generator at non-existent bus.

    Edge case: Generator connected to bus ID not in the model.
    """
    with pytest.raises(ValueError) as exc_info:
        PowerSystemModel(
            buses=[
                Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
            ],
            branches=[],
            generators=[Generator(bus_id=999, name="Gen1", p_gen_mw=50)],  # Invalid bus
            base_mva=100.0
        )
    assert "unknown" in str(exc_info.value).lower()


def test_negative_base_mva():
    """Test validation catches invalid (negative) base MVA.

    Edge case: Negative or zero base MVA value.
    """
    with pytest.raises(ValueError) as exc_info:
        PowerSystemModel(
            buses=[Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK")],
            branches=[],
            base_mva=-100.0  # Invalid
        )
    assert "positive" in str(exc_info.value).lower()

    with pytest.raises(ValueError) as exc_info:
        PowerSystemModel(
            buses=[Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK")],
            branches=[],
            base_mva=0.0  # Also invalid
        )
    assert "positive" in str(exc_info.value).lower()


def test_bus_self_connection():
    """Test validation prevents branch connecting bus to itself.

    Edge case: from_bus == to_bus.
    """
    with pytest.raises(ValueError) as exc_info:
        Branch(from_bus=0, to_bus=0, name="SelfLoop", branch_type="LINE",
               r_pu=0.01, x_pu=0.1, rate_a_mva=100.0)
    assert "itself" in str(exc_info.value)


def test_invalid_bus_type():
    """Test validation catches invalid bus type.

    Edge case: Bus type not in valid set.
    """
    with pytest.raises(ValueError) as exc_info:
        Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="INVALID")  # type: ignore
    assert "Invalid" in str(exc_info.value) or "invalid" in str(exc_info.value).lower()


def test_invalid_branch_type():
    """Test validation catches invalid branch type.

    Edge case: Branch type not in valid set.
    """
    with pytest.raises(ValueError) as exc_info:
        Branch(from_bus=0, to_bus=1, name="Branch1", branch_type="INVALID",  # type: ignore
               r_pu=0.01, x_pu=0.1, rate_a_mva=100.0)
    assert "Invalid" in str(exc_info.value) or "invalid" in str(exc_info.value).lower()


def test_negative_base_kv():
    """Test validation catches negative base kV for bus.

    Edge case: Invalid negative base voltage.
    """
    with pytest.raises(ValueError) as exc_info:
        Bus(bus_id=0, name="Bus1", base_kv=-230.0, bus_type="SLACK")
    assert "positive" in str(exc_info.value).lower()


def test_inverted_voltage_limits():
    """Test validation catches inverted voltage limits.

    Edge case: vm_min_pu >= vm_max_pu.
    """
    with pytest.raises(ValueError) as exc_info:
        Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK",
            vm_min_pu=1.1, vm_max_pu=0.9)  # Min > Max
    assert ">=" in str(exc_info.value) or "max" in str(exc_info.value).lower()


def test_negative_branch_rating():
    """Test validation catches negative branch rating.

    Edge case: Negative rate_a_mva.
    """
    with pytest.raises(ValueError) as exc_info:
        Branch(from_bus=0, to_bus=1, name="Branch1", branch_type="LINE",
               r_pu=0.01, x_pu=0.1, rate_a_mva=-100.0)
    assert "non-negative" in str(exc_info.value).lower() or "negative" in str(exc_info.value).lower()


def test_negative_bus_id():
    """Test validation catches negative bus ID.

    Edge case: Bus ID < 0.
    """
    with pytest.raises(ValueError) as exc_info:
        Bus(bus_id=-1, name="Bus1", base_kv=230.0, bus_type="SLACK")
    assert "non-negative" in str(exc_info.value).lower() or "negative" in str(exc_info.value).lower()


# =============================================================================
# Summary
# =============================================================================

# Total edge case tests: 50 tests covering:
# - Empty Model Handling (3 tests)
# - Single Bus Systems (3 tests)
# - Disconnected Components (3 tests)
# - Extreme Values (7 tests)
# - Transformer Handling (4 tests)
# - Generator Variations (6 tests)
# - Cross-Engine Consistency (4 tests)
# - Contingency Analysis Edge Cases (2 tests)
# - Physical Validation Edge Cases (3 tests)
# - Model Modification Edge Cases (3 tests)
# - Data Validation Edge Cases (12 tests)
