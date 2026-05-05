"""Tests for optional MATPOWER CPF integration."""

from __future__ import annotations

import numpy as np
import pytest

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


def _three_bus_model() -> PowerSystemModel:
    return PowerSystemModel(
        buses=[
            Bus(bus_id=1, name="Slack", base_kv=230.0, bus_type="SLACK", v_magnitude_pu=1.0),
            Bus(bus_id=2, name="PV", base_kv=230.0, bus_type="PV", v_magnitude_pu=1.01),
            Bus(bus_id=3, name="Load", base_kv=230.0, bus_type="PQ", v_magnitude_pu=0.98),
        ],
        branches=[
            Branch(from_bus=1, to_bus=2, name="L12", r_pu=0.02, x_pu=0.06, b_pu=0.03, rate_a_mva=120),
            Branch(from_bus=2, to_bus=3, name="L23", r_pu=0.08, x_pu=0.24, b_pu=0.025, rate_a_mva=90),
            Branch(
                from_bus=1,
                to_bus=3,
                name="Outaged",
                r_pu=0.01,
                x_pu=0.03,
                rate_a_mva=50,
                in_service=False,
            ),
        ],
        generators=[
            Generator(
                bus_id=1,
                name="SlackGen",
                p_gen_mw=100,
                q_gen_mvar=20,
                p_max_mw=250,
                p_min_mw=0,
                q_max_mvar=120,
                q_min_mvar=-80,
                v_set_pu=1.0,
            ),
            Generator(
                bus_id=2,
                name="PVGen",
                p_gen_mw=40,
                q_gen_mvar=5,
                p_max_mw=100,
                p_min_mw=0,
                q_max_mvar=60,
                q_min_mvar=-40,
                v_set_pu=1.01,
            ),
            Generator(bus_id=3, name="OfflineGen", p_gen_mw=10, p_max_mw=20, p_min_mw=0, in_service=False),
        ],
        loads=[
            Load(bus_id=2, name="L2", p_mw=20, q_mvar=5),
            Load(bus_id=3, name="L3", p_mw=80, q_mvar=25),
            Load(bus_id=3, name="OfflineLoad", p_mw=10, q_mvar=3, in_service=False),
        ],
        base_mva=100.0,
        name="three_bus_cpf",
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


def test_matpower_cpf_adapter_maps_unified_model_details():
    adapter = MatpowerCPFAdapter()

    base, target = adapter.build_cases(
        _three_bus_model(),
        target_scale=1.5,
        load_bus_ids=[3],
    )

    assert base["bus"][:, 0].tolist() == [1, 2, 3]
    assert base["bus"][:, 1].tolist() == [3, 2, 1]
    assert base["bus"][1, 2] == 20
    assert base["bus"][1, 3] == 5
    assert base["bus"][2, 2] == 80
    assert base["bus"][2, 3] == 25
    assert base["gen"].shape == (2, 10)
    assert base["branch"].shape == (2, 13)
    assert target["bus"][1, 2] == 20
    assert target["bus"][1, 3] == 5
    assert target["bus"][2, 2] == 120
    assert target["bus"][2, 3] == 37.5


def test_matpower_cpf_adapter_renumbers_zero_based_unified_buses_and_marks_generator_buses():
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Slack", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="GeneratorBus", base_kv=230.0, bus_type="PQ"),
            Bus(bus_id=2, name="Load", base_kv=230.0, bus_type="PQ"),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="L01", r_pu=0.01, x_pu=0.05),
            Branch(from_bus=1, to_bus=2, name="L12", r_pu=0.02, x_pu=0.08),
        ],
        generators=[
            Generator(bus_id=1, name="G1", p_gen_mw=40, p_max_mw=100, p_min_mw=0),
        ],
        loads=[
            Load(bus_id=2, name="L2", p_mw=60, q_mvar=20),
        ],
    )

    case = MatpowerCPFAdapter().to_mpc(model)

    assert case["bus"][:, 0].tolist() == [1, 2, 3]
    assert case["bus"][:, 1].tolist() == [3, 2, 1]
    assert case["branch"][:, :2].tolist() == [[1, 2], [2, 3]]
    assert case["gen"][0, 0] == 2


def test_matpower_cpf_adapter_converts_mpc_to_unified_model():
    mpc = {
        "version": "2",
        "baseMVA": 100.0,
        "bus": np.array([
            [10, 3, 0, 0, 0, 0, 1, 1.02, 0.0, 230.0, 1, 1.1, 0.9],
            [20, 1, 50, 15, 0, 0, 1, 0.98, -4.0, 230.0, 1, 1.1, 0.9],
        ]),
        "gen": np.array([
            [10, 80, 5, 100, -50, 1.02, 100, 1, 200, 0],
        ]),
        "branch": np.array([
            [10, 20, 0.01, 0.08, 0.02, 120, 130, 150, 1, 0, 1, -360, 360],
        ]),
    }

    model = MatpowerCPFAdapter().from_mpc(mpc, name="mpc_two_bus")

    assert model.name == "mpc_two_bus"
    assert model.source_engine == "matpower"
    assert model.base_mva == 100.0
    assert [bus.bus_id for bus in model.buses] == [10, 20]
    assert [bus.bus_type for bus in model.buses] == ["SLACK", "PQ"]
    assert len(model.loads) == 1
    assert model.loads[0].bus_id == 20
    assert model.loads[0].p_mw == 50
    assert len(model.generators) == 1
    assert model.generators[0].bus_id == 10
    assert len(model.branches) == 1
    assert model.branches[0].from_bus == 10
    assert model.branches[0].to_bus == 20
    assert model.branches[0].branch_type == "LINE"


def test_matpower_cpf_adapter_roundtrips_mpc_through_unified_case():
    original = {
        "version": "2",
        "baseMVA": 100.0,
        "bus": np.array([
            [1, 3, 0, 0, 0, 0, 1, 1.0, 0.0, 230.0, 1, 1.1, 0.9],
            [2, 2, 30, 10, 0, 0, 1, 1.01, -2.0, 230.0, 1, 1.1, 0.9],
            [3, 1, 70, 25, 0, 0, 1, 0.97, -6.0, 230.0, 1, 1.1, 0.9],
        ]),
        "gen": np.array([
            [1, 100, 20, 120, -80, 1.0, 100, 1, 250, 0],
            [2, 40, 5, 60, -40, 1.01, 100, 1, 100, 0],
        ]),
        "branch": np.array([
            [1, 2, 0.02, 0.06, 0.03, 120, 120, 120, 1, 0, 1, -360, 360],
            [2, 3, 0.08, 0.24, 0.025, 90, 90, 90, 1, 0, 1, -360, 360],
        ]),
    }

    adapter = MatpowerCPFAdapter()
    model = adapter.from_mpc(original, name="roundtrip")
    converted = adapter.to_mpc(model)

    assert converted["baseMVA"] == original["baseMVA"]
    assert converted["bus"].shape == original["bus"].shape
    assert converted["gen"].shape == original["gen"].shape
    assert converted["branch"].shape == original["branch"].shape
    assert np.allclose(converted["bus"][:, 1:4], original["bus"][:, 1:4])
    assert np.allclose(converted["gen"][:, :10], original["gen"][:, :10])
    assert np.allclose(converted["branch"][:, :10], original["branch"][:, :10])


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


def test_matpower_cpf_normalizes_octave_extracted_result():
    result = MatpowerCPFAdapter._normalize_result({
        "cpf": {
            "lam": np.array([[0.0, 0.5, 1.2]]),
            "V": np.array([[1.0, 0.99, 0.97], [0.98, 0.9, 0.82]]),
            "max_lam": 1.2,
        },
        "success": False,
    })

    assert result["success"] is False
    assert result["max_lambda"] == 1.2
    assert result["cpf"]["V"].shape == (2, 3)


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


@pytest.mark.integration
def test_matpower_cpf_runs_real_runtime_when_available():
    status = MatpowerCPFAdapter.runtime_status()
    if not status["available"]:
        pytest.skip(f"MATPOWER CPF runtime is not available: {status}")

    result = VoltageStabilityAnalysis().run(
        _sample_model(),
        {"method": "matpower_cpf", "target_scale": 1.2, "monitor_buses": ["Load"]},
    )

    assert result["analysis_mode"] == "matpower_continuation_power_flow"
    assert result["status"] in {"success", "warning"}
    assert result["max_loadability"] > 1.0
    assert len(result["pv_curve"]) > 2
    assert result["pv_curve"][0]["bus"] == "Load"
    assert result["matpower_runtime"]["available"] is True
    assert result["model_quality"]["status"] in {"pass", "warning"}
    assert result["cpf_output_quality"]["status"] in {"pass", "warning"}
    assert result["cpf_output_quality"]["has_finite_max_loadability"] is True


@pytest.mark.integration
def test_matpower_cpf_runs_real_runtime_on_three_bus_model():
    status = MatpowerCPFAdapter.runtime_status()
    if not status["available"]:
        pytest.skip(f"MATPOWER CPF runtime is not available: {status}")

    result = VoltageStabilityAnalysis().run(
        _three_bus_model(),
        {"method": "matpower_cpf", "target_scale": 1.5, "monitor_buses": ["PV", "Load"]},
    )

    assert result["analysis_mode"] == "matpower_continuation_power_flow"
    assert result["status"] in {"success", "warning"}
    assert result["max_loadability"] > 0.0
    assert len(result["pv_curve"]) > 4
    assert {point["bus"] for point in result["pv_curve"]} == {"PV", "Load"}
    assert all(point["source"] == "matpower_runcpf" for point in result["pv_curve"])
    assert result["model_quality"]["engine_readiness"]["matpower"]["convertible"] is True
    assert result["cpf_output_quality"]["pv_curve_points"] == len(result["pv_curve"])


@pytest.mark.integration
def test_matpower_cpf_runs_on_cloudpss_ieee39_unified_model():
    status = MatpowerCPFAdapter.runtime_status()
    if not status["available"]:
        pytest.skip(f"MATPOWER CPF runtime is not available: {status}")

    from pathlib import Path

    from cloudpss_skills_v2.powerapi import EngineConfig, SimulationStatus
    from cloudpss_skills_v2.powerapi.adapters.cloudpss import (
        CloudPSSPowerFlowAdapter,
    )

    token_file = Path(".cloudpss_token_internal")
    if not token_file.exists():
        pytest.skip("CloudPSS internal token is not available")

    base_url = "http://166.111.60.76:50001"
    token = token_file.read_text().strip()
    adapter = CloudPSSPowerFlowAdapter(
        EngineConfig(
            engine_name="cloudpss",
            base_url=base_url,
            extra={"auth": {"token": token, "base_url": base_url}},
        )
    )
    adapter.connect()
    powerflow = adapter.run_simulation(
        {
            "model_id": "model/chenying/IEEE39",
            "auth": {"token": token, "base_url": base_url},
        }
    )

    assert powerflow.status == SimulationStatus.COMPLETED
    assert powerflow.system_model is not None
    assert powerflow.system_model.source_engine == "cloudpss"
    assert {branch.branch_type for branch in powerflow.system_model.branches} == {
        "LINE",
        "TRANSFORMER",
    }
    assert all(branch.x_pu != 0.01 for branch in powerflow.system_model.branches)

    monitor_buses = [
        bus.name
        for bus in powerflow.system_model.buses
        if bus.bus_type == "PQ"
    ][:3]
    result = VoltageStabilityAnalysis().run(
        powerflow.system_model,
        {"method": "matpower_cpf", "target_scale": 1.02, "monitor_buses": monitor_buses},
    )

    assert result["analysis_mode"] == "matpower_continuation_power_flow"
    assert result["status"] == "success"
    assert result["solver_success"] is True
    assert result["max_loadability"] > 1.0
    assert len(result["pv_curve"]) > len(monitor_buses)
    assert result["model_quality"]["summary"]["source_engine"] == "cloudpss"
    assert result["model_quality"]["parameter_quality"]["default_like_x_pu_branch_count"] == 0
    assert result["model_quality"]["engine_readiness"]["matpower"]["convertible"] is True
    assert result["cpf_output_quality"]["status"] in {"pass", "warning"}


@pytest.mark.integration
@pytest.mark.parametrize("case_name", ["case9", "case30"])
def test_matpower_cpf_runs_on_pandapower_standard_cases(case_name):
    status = MatpowerCPFAdapter.runtime_status()
    if not status["available"]:
        pytest.skip(f"MATPOWER CPF runtime is not available: {status}")

    from cloudpss_skills_v2.powerapi import SimulationStatus
    from cloudpss_skills_v2.powerapi.adapters.pandapower import (
        PandapowerPowerFlowAdapter,
    )

    powerflow = PandapowerPowerFlowAdapter()._do_run_simulation({"model_id": case_name})
    assert powerflow.status == SimulationStatus.COMPLETED
    assert powerflow.system_model is not None
    assert powerflow.system_model.source_engine == "pandapower"

    monitor_buses = [
        bus.name
        for bus in powerflow.system_model.buses
        if bus.bus_type == "PQ"
    ][:3]
    result = VoltageStabilityAnalysis().run(
        powerflow.system_model,
        {"method": "matpower_cpf", "target_scale": 1.1, "monitor_buses": monitor_buses},
    )

    assert result["analysis_mode"] == "matpower_continuation_power_flow"
    assert result["status"] == "success"
    assert result["solver_success"] is True
    assert result["max_loadability"] > 1.0
    assert len(result["pv_curve"]) > len(monitor_buses)
    assert {point["bus"] for point in result["pv_curve"]} == set(monitor_buses)
    assert result["model_quality"]["summary"]["source_engine"] == "pandapower"
    assert result["model_quality"]["engine_readiness"]["matpower"]["convertible"] is True
    assert result["cpf_output_quality"]["has_finite_max_loadability"] is True
