"""Tests for cloudpss_skills_v2.tools.hdf5_export."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import h5py
import numpy as np
import pytest

from cloudpss_skills_v2.core.skill_result import SkillStatus
from cloudpss_skills_v2.tools.hdf5_export import HDF5ExportTool


@pytest.fixture
def tool() -> HDF5ExportTool:
    return HDF5ExportTool()


@pytest.fixture
def ieee39_results() -> dict[str, Any]:
    return {
        "power_flow": {
            "attrs": {"case": "IEEE39", "solver": "newton_raphson"},
            "bus": [
                {"bus_id": 1, "vm_pu": 1.0394, "va_deg": -13.54},
                {"bus_id": 2, "vm_pu": 1.0482, "va_deg": -9.21},
            ],
            "branch_flows": np.array(
                [[1.0, 100.5, 20.2], [2.0, 85.1, 14.7]], dtype=float
            ),
            "summary": {"total_load_mw": 6254.23, "loss_mw": 43.51},
        },
        "waveforms": {
            "time": np.array([0.0, 0.1, 0.2], dtype=float),
            "frequency_hz": np.array([50.0, 49.98, 49.97], dtype=float),
        },
    }


def _build_config(
    output_path: Path, data: object, metadata: dict[str, Any] | None = None
) -> dict[str, Any]:
    return {
        "source": {"data": data},
        "output": {"path": str(output_path)},
        "metadata": metadata or {"study": "IEEE39 dispatch", "operator": "pytest"},
    }


class TestValidate:
    def test_rejects_missing_source_data(self, tool: HDF5ExportTool, tmp_path: Path):
        valid, errors = tool.validate({"source": {}, "output": {"path": str(tmp_path / "bad.h5")}})
        assert valid is False
        assert "source.data is required" in errors

    def test_rejects_unsupported_data_type(self, tool: HDF5ExportTool, tmp_path: Path):
        valid, errors = tool.validate(
            {"source": {"data": "not-supported"}, "output": {"path": str(tmp_path / "bad.h5")}}
        )
        assert valid is False
        assert any("must be a dict, list, numpy array, or pandas DataFrame" in error for error in errors)

    def test_rejects_path_outside_allowed_directories(self, tool: HDF5ExportTool):
        valid, errors = tool.validate(
            {
                "source": {"data": {"x": [1, 2, 3]}},
                "output": {"path": "/home/chenying/researches/cloudpss-toolkit/results/outside.h5"},
            }
        )
        assert valid is False
        assert any("outside allowed directories" in error for error in errors)

    def test_accepts_numpy_and_tmp_output(self, tool: HDF5ExportTool, tmp_path: Path):
        config = {
            "source": {"data": np.array([1.0, 2.0, 3.0])},
            "output": {"path": str(tmp_path / "valid.h5")},
        }
        valid, errors = tool.validate(config)
        assert valid is True
        assert errors == []


class TestExportAndRead:
    def test_run_exports_ieee39_results_and_metadata(
        self, tool: HDF5ExportTool, tmp_path: Path, ieee39_results: dict[str, Any]
    ):
        output_path = tmp_path / "ieee39_results.h5"
        config = _build_config(
            output_path,
            ieee39_results,
            metadata={"study": "IEEE39", "scenario": "base_case"},
        )

        result = tool.run(config)

        assert result.status == SkillStatus.SUCCESS
        assert result.data["output_path"] == str(output_path)
        assert set(result.data["datasets"]) == {
            "/power_flow/bus",
            "/power_flow/branch_flows",
            "/power_flow/summary/loss_mw",
            "/power_flow/summary/total_load_mw",
            "/waveforms/frequency_hz",
            "/waveforms/time",
        }
        assert len(result.artifacts) == 2

        with h5py.File(output_path, "r") as handle:
            assert handle.attrs["skill_name"] == "hdf5_export"
            assert handle.attrs["version"] == "2.0"
            assert handle.attrs["study"] == "IEEE39"
            assert "timestamp" in handle.attrs
            assert handle["power_flow"].attrs["case"] == "IEEE39"
            branch_flows = handle["power_flow/branch_flows"]
            assert isinstance(branch_flows, h5py.Dataset)
            assert branch_flows.shape == (2, 3)

    def test_round_trip_reads_structured_table(
        self, tool: HDF5ExportTool, tmp_path: Path, ieee39_results: dict[str, Any]
    ):
        output_path = tmp_path / "round_trip.h5"
        tool.run(_build_config(output_path, ieee39_results))

        bus_data = tool.read_hdf5(output_path, "/power_flow/bus")
        full_data = tool.read_hdf5(output_path)

        assert isinstance(bus_data, list)
        assert isinstance(full_data, dict)
        assert bus_data[0]["bus_id"] == 1
        assert pytest.approx(bus_data[1]["vm_pu"], rel=1e-6) == 1.0482
        power_flow = full_data["power_flow"]
        root_attrs = full_data["attrs"]
        assert isinstance(power_flow, dict)
        assert isinstance(root_attrs, dict)
        assert power_flow["summary"]["loss_mw"] == 43.51
        assert root_attrs["skill_name"] == "hdf5_export"

    def test_list_datasets_and_index_file(
        self, tool: HDF5ExportTool, tmp_path: Path, ieee39_results: dict[str, Any]
    ):
        output_path = tmp_path / "indexable.hdf5"
        result = tool.run(_build_config(output_path, ieee39_results))
        index_path = Path(result.data["index_path"])

        datasets = tool.list_datasets(output_path)
        index_data = json.loads(index_path.read_text(encoding="utf-8"))

        assert "/waveforms/time" in datasets
        assert "/power_flow/branch_flows" in datasets
        assert index_path.exists()
        assert {item["path"] for item in index_data["datasets"]} == set(datasets)
        assert index_data["attrs"]["skill_name"] == "hdf5_export"

    def test_run_returns_failed_result_for_invalid_config(self, tool: HDF5ExportTool):
        result = tool.run({"source": {}, "output": {"path": "/tmp/missing.h5"}})

        assert result.status == SkillStatus.FAILED
        assert result.data["stage"] == "validation"
        assert "source.data is required" in result.data["errors"]
