"""Tests for LossAnalysis using unified PowerSystemModel."""

import pytest


def test_loss_analysis_runs_on_unified_model():
    from cloudpss_skills_v2.poweranalysis.loss_analysis import LossAnalysis
    from cloudpss_skills_v2.core.system_model import PowerSystemModel, Bus, Branch, Generator, Load

    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK",
                v_magnitude_pu=1.0, v_angle_degree=0.0),
            Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ",
                v_magnitude_pu=0.98, v_angle_degree=-2.0),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="Line1-2", branch_type="LINE",
                   r_pu=0.01, x_pu=0.1, rate_a_mva=100.0,
                   p_from_mw=50, p_to_mw=-49),
        ],
        generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=100)],
        loads=[Load(bus_id=1, name="Load1", p_mw=50)],
        base_mva=100.0
    )

    analysis = LossAnalysis()
    result = analysis.run(model, {"detail_level": "branch"})

    assert result["status"] == "success"
    assert "total_loss_mw" in result
    assert "branch_losses" in result


def test_loss_analysis_calculates_branch_losses():
    """Test that branch losses are calculated correctly from p_from_mw - p_to_mw."""
    from cloudpss_skills_v2.poweranalysis.loss_analysis import LossAnalysis
    from cloudpss_skills_v2.core.system_model import PowerSystemModel, Bus, Branch, Generator, Load

    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK",
                v_magnitude_pu=1.0, v_angle_degree=0.0),
            Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ",
                v_magnitude_pu=0.98, v_angle_degree=-2.0),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="Line1-2", branch_type="LINE",
                   r_pu=0.01, x_pu=0.1, rate_a_mva=100.0,
                   p_from_mw=50, p_to_mw=-49),
        ],
        generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=100)],
        loads=[Load(bus_id=1, name="Load1", p_mw=50)],
        base_mva=100.0
    )

    analysis = LossAnalysis()
    result = analysis.run(model, {"detail_level": "branch"})

    # Expected loss: p_from - (-p_to) = 50 - 49 = 1 MW
    # (p_to is negative because power flows into the branch at to_bus)
    assert result["status"] == "success"
    assert result["total_loss_mw"] == pytest.approx(1.0, abs=0.01)
    assert len(result["branch_losses"]) == 1
    assert result["branch_losses"][0]["p_loss_mw"] == pytest.approx(1.0, abs=0.01)


def test_loss_analysis_with_transformer():
    """Test transformer loss calculation."""
    from cloudpss_skills_v2.poweranalysis.loss_analysis import LossAnalysis
    from cloudpss_skills_v2.core.system_model import PowerSystemModel, Bus, Branch, Generator, Load

    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="Bus2", base_kv=110.0, bus_type="PQ"),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="T1", branch_type="TRANSFORMER",
                   r_pu=0.005, x_pu=0.08, rate_a_mva=100.0,
                   p_from_mw=100, p_to_mw=-98),
        ],
        generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=100)],
        loads=[Load(bus_id=1, name="Load1", p_mw=98)],
        base_mva=100.0
    )

    analysis = LossAnalysis()
    result = analysis.run(model, {"detail_level": "branch"})

    assert result["status"] == "success"
    # Transformer loss: 100 - 98 = 2 MW
    assert result["total_loss_mw"] == pytest.approx(2.0, abs=0.01)


def test_loss_analysis_multiple_branches():
    """Test loss calculation with multiple branches."""
    from cloudpss_skills_v2.poweranalysis.loss_analysis import LossAnalysis
    from cloudpss_skills_v2.core.system_model import PowerSystemModel, Bus, Branch, Generator, Load

    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ"),
            Bus(bus_id=2, name="Bus3", base_kv=230.0, bus_type="PQ"),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="Line1-2", branch_type="LINE",
                   r_pu=0.01, x_pu=0.1, rate_a_mva=100.0,
                   p_from_mw=30, p_to_mw=-29.5),
            Branch(from_bus=1, to_bus=2, name="Line2-3", branch_type="LINE",
                   r_pu=0.01, x_pu=0.1, rate_a_mva=100.0,
                   p_from_mw=20, p_to_mw=-19.7),
        ],
        generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=50)],
        loads=[
            Load(bus_id=1, name="Load1", p_mw=10),
            Load(bus_id=2, name="Load2", p_mw=20),
        ],
        base_mva=100.0
    )

    analysis = LossAnalysis()
    result = analysis.run(model, {"detail_level": "branch"})

    assert result["status"] == "success"
    # Loss 1: 30 - 29.5 = 0.5 MW
    # Loss 2: 20 - 19.7 = 0.3 MW
    # Total: 0.8 MW
    assert result["total_loss_mw"] == pytest.approx(0.8, abs=0.01)
    assert len(result["branch_losses"]) == 2


def test_loss_analysis_empty_model():
    """Test behavior with empty model."""
    from cloudpss_skills_v2.poweranalysis.loss_analysis import LossAnalysis
    from cloudpss_skills_v2.core.system_model import PowerSystemModel

    model = PowerSystemModel(buses=[], branches=[], generators=[], loads=[], base_mva=100.0)
    analysis = LossAnalysis()
    result = analysis.run(model, {"detail_level": "branch"})

    assert result["status"] == "error"
    assert "No buses" in result["error"]


def test_loss_analysis_inherits_from_power_analysis():
    """Test that LossAnalysis inherits from PowerAnalysis base class."""
    from cloudpss_skills_v2.poweranalysis.loss_analysis import LossAnalysis
    from cloudpss_skills_v2.poweranalysis.base import PowerAnalysis

    analysis = LossAnalysis()
    assert isinstance(analysis, PowerAnalysis)
