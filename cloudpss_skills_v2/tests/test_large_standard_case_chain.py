"""Large standard-case coverage for pandapower -> unified -> MATPOWER reuse."""

from __future__ import annotations

import os

import numpy as np
import pytest

pytest.importorskip("pandapower")
import pandapower as pp
import pandapower.networks as pn

from cloudpss_skills_v2.powerapi import SimulationStatus
from cloudpss_skills_v2.powerapi.adapters.matpower_cpf import MatpowerCPFAdapter
from cloudpss_skills_v2.powerapi.adapters.pandapower import PandapowerPowerFlowAdapter
from cloudpss_skills_v2.powerapi.model_quality import diagnose_unified_model


DEFAULT_STANDARD_CASES = [
    "case57",
    "case118",
    "case300",
    "case1354pegase",
]

PRESSURE_STANDARD_CASES = [
    "case2869pegase",
]


def _run_pandapower_standard_case(case_name: str):
    result = PandapowerPowerFlowAdapter()._do_run_simulation({"model_id": case_name})
    assert result.status == SimulationStatus.COMPLETED
    assert result.system_model is not None
    return result.system_model


def _native_case_counts(case_name: str) -> dict[str, int]:
    net = getattr(pn, case_name)()
    return {
        "buses": len(net.bus),
        "branches": len(net.line) + len(net.trafo),
        "generators": len(net.gen) + len(net.ext_grid) + len(net.sgen),
        "loads": len(net.load) + len(net.shunt),
    }


@pytest.mark.integration
@pytest.mark.pandapower
@pytest.mark.parametrize("case_name", DEFAULT_STANDARD_CASES)
def test_large_pandapower_cases_convert_to_matpower_ready_unified_models(case_name):
    """Medium and large standard cases should remain reusable across adapters."""
    expected = _native_case_counts(case_name)
    model = _run_pandapower_standard_case(case_name)

    assert len(model.buses) == expected["buses"]
    assert len(model.branches) == expected["branches"]
    assert len(model.generators) == expected["generators"]
    assert len(model.loads) == expected["loads"]

    quality = diagnose_unified_model(model, include_matpower=True)
    matpower_quality = quality["engine_readiness"]["matpower"]

    assert quality["status"] in {"pass", "warning"}
    assert quality["engine_readiness"]["pandapower"]["convertible"] is True
    assert matpower_quality["convertible"] is True
    assert matpower_quality["bus_shape"] == [expected["buses"], 13]
    assert matpower_quality["branch_shape"] == [expected["branches"], 13]
    assert matpower_quality["slack_bus_count"] >= 1
    assert matpower_quality["total_pd_mw"] > 0


@pytest.mark.integration
@pytest.mark.pandapower
@pytest.mark.parametrize("case_name", ["case57", "case118", "case300"])
def test_large_pandapower_cases_build_finite_matpower_cases(case_name):
    """MATPOWER matrix construction should stay finite beyond tiny examples."""
    model = _run_pandapower_standard_case(case_name)
    mpc = MatpowerCPFAdapter().to_mpc(model)

    assert mpc["bus"].shape[0] == len(model.buses)
    assert mpc["gen"].shape[0] == sum(1 for gen in model.generators if gen.in_service)
    assert mpc["branch"].shape[0] == sum(1 for branch in model.branches if branch.in_service)
    assert np.all(np.isfinite(mpc["bus"]))
    assert np.all(np.isfinite(mpc["gen"]))
    assert np.all(np.isfinite(mpc["branch"]))
    assert np.any(mpc["bus"][:, 1] == 3)


@pytest.mark.integration
@pytest.mark.pandapower
@pytest.mark.parametrize("case_name", ["case57", "case118", "case300"])
def test_large_pandapower_cases_roundtrip_back_to_pandapower(case_name):
    """Verify the reverse unified -> pandapower path on larger standard cases."""
    original_model = _run_pandapower_standard_case(case_name)
    pp_net = PandapowerPowerFlowAdapter().from_unified_model(original_model)

    pp.runpp(pp_net)
    roundtrip_model = PandapowerPowerFlowAdapter()._to_unified_model(pp_net)
    quality = diagnose_unified_model(roundtrip_model, include_matpower=True)

    assert len(roundtrip_model.buses) == len(original_model.buses)
    assert len(roundtrip_model.branches) == len(original_model.branches)
    assert len(roundtrip_model.generators) == len(original_model.generators)
    assert len(roundtrip_model.loads) == len(original_model.loads)
    assert quality["status"] in {"pass", "warning"}
    assert quality["engine_readiness"]["matpower"]["convertible"] is True

    original_voltage = np.array([bus.v_magnitude_pu for bus in original_model.buses], dtype=float)
    roundtrip_voltage = np.array([bus.v_magnitude_pu for bus in roundtrip_model.buses], dtype=float)
    voltage_diff = np.abs(original_voltage - roundtrip_voltage)
    assert float(np.nanmax(voltage_diff)) < 0.10


@pytest.mark.integration
@pytest.mark.pandapower
@pytest.mark.parametrize("case_name", ["case57", "case118", "case300"])
def test_large_pandapower_cases_roundtrip_through_matpower_case(case_name):
    """Verify MATPOWER case -> unified after pandapower-origin conversion."""
    source_model = _run_pandapower_standard_case(case_name)
    adapter = MatpowerCPFAdapter()
    mpc = adapter.to_mpc(source_model)
    matpower_model = adapter.from_mpc(mpc, name=f"{case_name}_from_matpower")
    quality = diagnose_unified_model(matpower_model, include_matpower=True)
    rebuilt = adapter.to_mpc(matpower_model)

    assert matpower_model.source_engine == "matpower"
    assert len(matpower_model.buses) == len(source_model.buses)
    assert len(matpower_model.branches) == sum(1 for branch in source_model.branches if branch.in_service)
    assert len(matpower_model.loads) == sum(
        1
        for bus in source_model.buses
        if any(load.bus_id == bus.bus_id and load.in_service and (load.p_mw or load.q_mvar) for load in source_model.loads)
    )
    assert quality["status"] in {"pass", "warning"}
    assert quality["engine_readiness"]["matpower"]["convertible"] is True
    assert rebuilt["bus"].shape == mpc["bus"].shape
    assert rebuilt["gen"].shape == mpc["gen"].shape
    assert rebuilt["branch"].shape == mpc["branch"].shape
    assert np.allclose(rebuilt["bus"][:, 1:4], mpc["bus"][:, 1:4])
    assert np.allclose(rebuilt["branch"][:, :10], mpc["branch"][:, :10])


@pytest.mark.integration
@pytest.mark.pandapower
@pytest.mark.slow
@pytest.mark.skipif(
    os.getenv("CLOUDPSS_V2_RUN_LARGE_CASES") != "1",
    reason="set CLOUDPSS_V2_RUN_LARGE_CASES=1 to run multi-thousand-bus pressure cases",
)
@pytest.mark.parametrize("case_name", PRESSURE_STANDARD_CASES)
def test_pressure_pandapower_cases_are_matpower_ready_when_enabled(case_name):
    """Optional pressure tests cover multi-thousand-bus standard systems."""
    expected = _native_case_counts(case_name)
    model = _run_pandapower_standard_case(case_name)
    quality = diagnose_unified_model(model, include_matpower=True)

    assert len(model.buses) == expected["buses"]
    assert len(model.branches) == expected["branches"]
    assert quality["status"] in {"pass", "warning"}
    assert quality["engine_readiness"]["matpower"]["convertible"] is True
    assert quality["engine_readiness"]["matpower"]["bus_shape"] == [expected["buses"], 13]
