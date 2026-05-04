"""Large standard-case coverage for pandapower -> unified -> MATPOWER reuse."""

from __future__ import annotations

import os

import numpy as np
import pytest

pytest.importorskip("pandapower")
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
        "loads": len(net.load),
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
