"""Integration tests for converting real engine results into DataLib types."""

from __future__ import annotations

import pytest

from cloudpss_skills_v2.libs.data_lib import BranchData, BusData
from cloudpss_skills_v2.libs.data_lib.types import NetworkSummary
from cloudpss_skills_v2.powerapi import SimulationStatus
from cloudpss_skills_v2.powerskill import Engine


@pytest.fixture(scope="module")
def case14_powerflow():
    powerflow = Engine.create_powerflow(engine="pandapower")
    result = powerflow.run_power_flow("case14")
    assert result.status == SimulationStatus.COMPLETED
    assert result.job_id
    return powerflow, result


def test_real_powerflow_bus_results_convert_to_datalib(case14_powerflow):
    powerflow, raw_result = case14_powerflow

    buses = powerflow.get_bus_results(raw_result.job_id)

    assert len(buses) == 14
    assert all(isinstance(bus, BusData) for bus in buses)
    assert any(bus.is_slack for bus in buses)
    assert any(bus.is_pv for bus in buses)
    assert all(bus.voltage_pu is not None for bus in buses)
    assert all(0.9 <= bus.voltage_pu <= 1.1 for bus in buses if bus.voltage_pu)


def test_real_powerflow_branch_results_convert_to_datalib(case14_powerflow):
    powerflow, raw_result = case14_powerflow

    branches = powerflow.get_branch_results(raw_result.job_id)

    assert len(branches) >= 15
    assert all(isinstance(branch, BranchData) for branch in branches)
    assert any(branch.loading_pct is not None for branch in branches)
    assert all(branch.from_bus != "" for branch in branches)
    assert all(branch.to_bus != "" for branch in branches)


def test_real_powerflow_summary_converts_to_datalib(case14_powerflow):
    powerflow, raw_result = case14_powerflow

    summary = powerflow.get_summary(raw_result.job_id)

    assert isinstance(summary, NetworkSummary)
    assert summary.total_generation_mw > 0
    assert summary.total_load_mw > 0
    assert summary.total_loss_mw >= 0
    assert summary.min_voltage_pu > 0.9
    assert summary.max_voltage_pu < 1.1
