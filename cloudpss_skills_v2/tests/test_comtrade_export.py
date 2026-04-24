"""Tests for cloudpss_skills_v2.tools.comtrade_export."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, cast

import pytest
from _pytest.tmpdir import TempPathFactory

from cloudpss_skills_v2.core import SkillResult, SkillStatus
from cloudpss_skills_v2.tools.comtrade_export import ComtradeExportTool


def parse_comtrade_ascii(cfg_path: Path, dat_path: Path) -> dict[str, Any]:
    cfg_lines = cfg_path.read_text(encoding="utf-8").strip().splitlines()
    first = cfg_lines[0].split(",")
    counts = cfg_lines[1].split(",")
    analog_count = int(counts[1][:-1])
    digital_count = int(counts[2][:-1])

    analog_channels: list[dict[str, Any]] = []
    digital_channels: list[dict[str, Any]] = []
    line_index = 2
    for _ in range(analog_count):
        parts = cfg_lines[line_index].split(",")
        analog_channels.append(
            {
                "index": int(parts[0]),
                "name": parts[1],
                "a": float(parts[5]),
                "b": float(parts[6]),
            }
        )
        line_index += 1
    for _ in range(digital_count):
        parts = cfg_lines[line_index].split(",")
        digital_channels.append({"index": int(parts[0]), "name": parts[1]})
        line_index += 1

    sample_rate_line = cfg_lines[line_index + 2].split(",")
    sample_rate = float(sample_rate_line[0])
    sample_count = int(sample_rate_line[1])

    rows: list[list[str]] = []
    with dat_path.open(encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        for row in reader:
            rows.append(row)

    decoded: list[dict[str, Any]] = []
    for row in rows:
        analog_values: dict[str, float] = {}
        for offset, channel in enumerate(analog_channels, start=2):
            raw = int(row[offset])
            analog_values[str(channel["name"])] = raw * float(channel["a"]) + float(channel["b"])
        digital_values: dict[str, int] = {}
        for offset, channel in enumerate(digital_channels, start=2 + analog_count):
            digital_values[str(channel["name"])] = int(row[offset])
        decoded.append(
            {
                "sample": int(row[0]),
                "timestamp_us": int(row[1]),
                "analog": analog_values,
                "digital": digital_values,
            }
        )

    return {
        "station_name": first[0],
        "rec_dev_id": first[1],
        "analog_channels": analog_channels,
        "digital_channels": digital_channels,
        "sample_rate": sample_rate,
        "sample_count": sample_count,
        "rows": decoded,
    }


@pytest.fixture
def tool() -> ComtradeExportTool:
    return ComtradeExportTool()


@pytest.fixture
def sample_config(tmp_path: Path) -> dict[str, Any]:
    return {
        "skill": "comtrade_export",
        "source": {
            "data": {
                "time": [0.0, 0.0005, 0.001],
                "channels": [
                    {
                        "name": "Bus1_V",
                        "type": "voltage",
                        "unit": "kV",
                        "phase": "A",
                        "circuit": "BUS1",
                        "a": 0.001,
                        "b": 0.0,
                        "values": [110.001, 110.002, 110.003],
                    },
                    {
                        "name": "Line1_I",
                        "type": "current",
                        "unit": "A",
                        "phase": "A",
                        "circuit": "LINE1",
                        "a": 0.01,
                        "b": 0.0,
                        "values": [10.01, 10.02, 10.03],
                    },
                    {
                        "name": "Trip",
                        "type": "digital",
                        "values": [0, 1, 1],
                    },
                ],
            }
        },
        "comtrade": {
            "station_name": "StationA",
            "rec_dev_id": "Recorder01",
            "frequency": 50.0,
            "start_time": "01/01/2025,12:00:00.000000",
        },
        "output": {
            "path": str(tmp_path),
            "filename": "fault_record",
            "file_type": "ASCII",
            "format": "ASCII",
        },
    }


class TestComtradeExportTool:
    def test_default_config(self, tool: ComtradeExportTool) -> None:
        config = tool.get_default_config()
        assert config["skill"] == "comtrade_export"
        output = cast(dict[str, Any], config["output"])
        assert output["file_type"] == "ASCII"

    def test_generate_cfg_header(self, tool: ComtradeExportTool) -> None:
        header = tool._generate_cfg_header(
            station_name="StationA",
            rec_dev_id="Recorder01",
            num_channels=2,
            sample_rate=2000.0,
            frequency=50.0,
            num_analog=2,
            num_digital=1,
        )
        lines = header.splitlines()
        assert lines[0] == "StationA,Recorder01,1999"
        assert lines[1] == "3,2A,1D"
        assert lines[2] == "50.000000"
        assert lines[4] == "2000.000000,0"

    def test_generate_dat_record_clips_values(self, tool: ComtradeExportTool) -> None:
        assert tool._generate_dat_record([1.2, 40000, -50000, True, False]) == "1,32767,-32767,1,0"

    def test_format_timestamp_microseconds(self, tool: ComtradeExportTool) -> None:
        assert tool._format_timestamp(0.000001) == "1"
        assert tool._format_timestamp(0.123456) == "123456"

    def test_validate_rejects_non_voltage_current_analog(
        self,
        tool: ComtradeExportTool,
        sample_config: dict[str, Any],
    ) -> None:
        sample_config["source"]["data"]["channels"][0]["type"] = "power"
        valid, errors = tool.validate(sample_config)
        assert valid is False
        assert any("voltage or current" in error for error in errors)

    def test_validate_rejects_missing_source_data(self, tool: ComtradeExportTool) -> None:
        valid, errors = tool.validate({"output": {"path": "./tmp", "file_type": "ASCII"}})
        assert valid is False
        assert "source.data with time-series data is required" in errors

    def test_run_writes_cfg_and_dat_files(
        self,
        tool: ComtradeExportTool,
        sample_config: dict[str, Any],
    ) -> None:
        result = tool.run(sample_config)
        assert result.status == SkillStatus.SUCCESS
        cfg_path = Path(result.data["cfg_file"])
        dat_path = Path(result.data["dat_file"])
        assert cfg_path.exists()
        assert dat_path.exists()

        cfg_lines = cfg_path.read_text(encoding="utf-8").splitlines()
        dat_lines = dat_path.read_text(encoding="utf-8").splitlines()
        assert cfg_lines[0] == "StationA,Recorder01,1999"
        assert cfg_lines[1] == "3,2A,1D"
        assert cfg_lines[5] == "50.000000"
        assert cfg_lines[6] == "1"
        assert cfg_lines[7] == "2000.000000,3"
        assert dat_lines[0] == "1,0,32767,1001,0"
        assert dat_lines[1] == "2,500,32767,1002,1"
        assert dat_lines[2] == "3,1000,32767,1003,1"

    def test_round_trip_parser_style_decode(
        self,
        tool: ComtradeExportTool,
        sample_config: dict[str, Any],
    ) -> None:
        result = tool.run(sample_config)
        parsed = parse_comtrade_ascii(
            Path(result.data["cfg_file"]),
            Path(result.data["dat_file"]),
        )
        assert parsed["station_name"] == "StationA"
        assert parsed["rec_dev_id"] == "Recorder01"
        assert parsed["sample_rate"] == pytest.approx(2000.0)
        assert parsed["sample_count"] == 3
        rows = parsed["rows"]
        assert rows[0]["timestamp_us"] == 0
        assert rows[1]["timestamp_us"] == 500
        assert rows[2]["timestamp_us"] == 1000
        assert rows[0]["analog"]["Line1_I"] == pytest.approx(10.01)
        assert rows[1]["digital"]["Trip"] == 1

    def test_run_returns_failure_for_invalid_config(self, tool: ComtradeExportTool) -> None:
        result = tool.run({"source": {"data": {"time": [0.0], "channels": []}}, "output": {"path": "./x"}})
        assert result.status == SkillStatus.FAILED
        assert result.data["stage"] == "validation"
        assert result.data["errors"]

    def test_run_supports_mapping_style_channels(
        self,
        tool: ComtradeExportTool,
        tmp_path: Path,
    ) -> None:
        config = {
            "source": {
                "data": {
                    "time": [0.0, 0.001],
                    "channels": {"Va": [1.0, 1.1], "Ia": [0.1, 0.2]},
                    "metadata": {
                        "Va": {"type": "voltage", "a": 0.001},
                        "Ia": {"type": "current", "a": 0.001},
                    },
                }
            },
            "output": {
                "path": str(tmp_path),
                "filename": "mapping_case",
                "file_type": "ASCII",
                "format": "ASCII",
            },
        }
        typed_config = cast(dict[str, object], config)
        result = tool.run(typed_config)
        assert result.status == SkillStatus.SUCCESS
        assert Path(result.data["cfg_file"]).exists()
        assert Path(result.data["dat_file"]).exists()
