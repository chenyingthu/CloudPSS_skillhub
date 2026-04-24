"""Visualize Tool - Plot simulation results.

可视化工具 - 绘制仿真结果。
"""

from __future__ import annotations

import csv
import json
import logging
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping

import h5py

# Use non-interactive backend for headless environments
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from cloudpss_skills_v2.core.skill_result import (
    Artifact,
    SkillResult,
    SkillStatus,
)
from cloudpss_skills_v2.powerskill import Engine

logger = logging.getLogger(__name__)

ALLOWED_DATA_EXTENSIONS = {".csv", ".json", ".h5", ".hdf5"}


def _allowed_data_roots() -> list[Path]:
    return [
        Path("/data").resolve(),
        Path("/results").resolve(),
        (Path.home() / "cloudpss_data").resolve(),
    ]


def validate_data_path(user_input: str) -> Path:
    """
    验证并规范化用户输入的数据文件路径。

    安全要求：
    1. 必须是绝对路径
    2. 必须在允许的目录内
    3. 必须是文件（不是目录）
    4. 必须是 .csv, .json, .h5, .hdf5 格式
    5. 文件必须存在
    """
    if not user_input.strip():
        raise ValueError("Data file path must be a non-empty string")

    raw_path = Path(user_input.strip())
    if not raw_path.is_absolute():
        raise ValueError("Data file path must be an absolute path")

    path = raw_path.resolve(strict=False)
    allowed_roots = _allowed_data_roots()

    if not any(path.is_relative_to(root) for root in allowed_roots):
        allowed_root_text = ", ".join(str(root) for root in allowed_roots)
        raise ValueError(
            f"Data file path '{path}' is outside allowed directories: {allowed_root_text}"
        )

    if not path.exists():
        raise ValueError(f"Data file path does not exist: {raw_path}")

    if not path.is_file():
        raise ValueError(f"Data file path must point to a file: {path}")

    if path.suffix.lower() not in ALLOWED_DATA_EXTENSIONS:
        allowed = ", ".join(sorted(ALLOWED_DATA_EXTENSIONS))
        raise ValueError(
            f"Unsupported data file extension '{path.suffix}'. Allowed: {allowed}"
        )

    return path


class VisualizeTool:
    """Visualize tool for plotting simulation results."""

    name = "visualize"
    description = "可视化工具 - 绘制仿真结果"

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill"],
            "properties": {
                "skill": {"type": "string", "const": "visualize"},
                "engine": {
                    "type": "string",
                    "enum": ["cloudpss", "pandapower"],
                    "default": "pandapower",
                },
                "model": {"type": "object", "required": ["rid"]},
                "result": {"type": "object"},
                "plot": {
                    "type": "object",
                    "properties": {
                        "type": {
                            "type": "array",
                            "items": {"type": "string"},
                            "default": ["time_series", "bus_voltages"],
                        },
                        "channels": {"type": "array", "items": {"type": "string"}},
                    },
                },
            },
        }

    def __init__(self):
        self.logs = []
        self.artifacts = []

    def _log(self, level: str, message: str) -> None:
        self.logs.append(
            {
                "timestamp": datetime.now().isoformat(),
                "level": level,
                "message": message,
            }
        )
        getattr(logger, level.lower(), logger.info)(message)

    def validate(self, config: dict[str, Any] | None) -> tuple[bool, list[str]]:
        errors = []
        if not config:
            errors.append("config is required")
            return (False, errors)
        if not config.get("model", {}).get("rid"):
            errors.append("model.rid is required")
        return (len(errors) == 0, errors)

    def _load_data(self, config: dict[str, Any]) -> dict[str, Any]:
        """Load data from config or result."""
        if config.get("data") is not None:
            return config["data"]

        result = config.get("result")
        if result:
            return result

        source = config.get("source") or {}
        if not isinstance(source, Mapping):
            raise ValueError("source must be an object")
        if source.get("data") is not None:
            return source["data"]
        if source.get("data_file") is not None:
            data_file = source["data_file"]
            if not isinstance(data_file, str):
                raise ValueError("source.data_file must be a string")
            return self._load_data_file(data_file)

        return {}

    def _load_data_file(self, user_input: str) -> dict[str, Any]:
        """Load structured data from an approved local file."""
        path = validate_data_path(user_input)
        suffix = path.suffix.lower()

        try:
            if suffix == ".json":
                with path.open("r", encoding="utf-8") as handle:
                    data = json.load(handle)
            elif suffix == ".csv":
                with path.open("r", encoding="utf-8", newline="") as handle:
                    data = {"rows": list(csv.DictReader(handle))}
            elif suffix in {".h5", ".hdf5"}:
                data = self._read_hdf5_file(path)
            else:
                raise ValueError(f"Unsupported data file extension '{suffix}'")
        except (ValueError, OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"Failed to load data file '{path}': {exc}") from exc

        if not isinstance(data, dict):
            raise ValueError(
                f"Data file '{path}' must contain a top-level object or mapping"
            )

        return data

    def _read_hdf5_file(self, path: Path) -> dict[str, Any]:
        """Convert a simple HDF5 file into a nested dictionary."""

        def _convert_hdf5_node(node: h5py.Group | h5py.Dataset) -> Any:
            if isinstance(node, h5py.Dataset):
                value = node[()]
                if hasattr(value, "tolist"):
                    value = value.tolist()
                if isinstance(value, bytes):
                    return value.decode("utf-8")
                return value

            return {name: _convert_hdf5_node(child) for name, child in node.items()}

        with h5py.File(path, "r") as handle:
            return {name: _convert_hdf5_node(child) for name, child in handle.items()}

    def _plot_time_series(self, data: dict[str, Any], out_dir: str) -> dict[str, str]:
        """Plot time series data."""
        times = data.get("time") or data.get("timestamps") or []
        values = data.get("series") or data.get("values") or []
        if not times or not values:
            return {}
        if len(times) != len(values):
            times = list(range(len(values)))

        plt.figure(figsize=(10, 6))
        plt.plot(times, values, marker="o", linewidth=1.5, markersize=4)
        plt.title("Time Series")
        plt.xlabel("Time")
        plt.ylabel("Value")
        plt.grid(True, alpha=0.3)

        os.makedirs(out_dir, exist_ok=True)
        base = os.path.join(out_dir, "time_series")
        paths = {}
        for ext in ("png",):
            path = f"{base}.{ext}"
            plt.savefig(path, dpi=150, bbox_inches="tight")
            paths[ext] = path
        plt.close()
        self._log("INFO", f"Time series plot saved to {paths}")
        return paths

    def _plot_bus_voltages(self, data: dict[str, Any], out_dir: str) -> dict[str, str]:
        """Plot bus voltages as bar chart."""
        voltages = data.get("bus_voltages") or data.get("voltages")
        if not isinstance(voltages, dict) or not voltages:
            return {}

        labels = list(voltages.keys())
        vals = list(voltages.values())

        plt.figure(figsize=(12, 6))
        plt.bar(labels, vals, color="steelblue", alpha=0.8)
        plt.axhline(y=1.0, color="r", linestyle="--", linewidth=1, label="1.0 pu")
        plt.axhline(y=1.1, color="orange", linestyle="--", linewidth=1, label="1.1 pu")
        plt.axhline(y=0.9, color="orange", linestyle="--", linewidth=1, label="0.9 pu")
        plt.ylabel("Voltage (pu)")
        plt.title("Bus Voltages")
        plt.xticks(rotation=45, ha="right")
        plt.legend()
        plt.grid(True, alpha=0.3, axis="y")

        os.makedirs(out_dir, exist_ok=True)
        base = os.path.join(out_dir, "bus_voltages")
        paths = {}
        for ext in ("png",):
            path = f"{base}.{ext}"
            plt.savefig(path, dpi=150, bbox_inches="tight")
            paths[ext] = path
        plt.close()
        self._log("INFO", f"Bus voltages plot saved to {paths}")
        return paths

    def _plot_branch_flows(self, data: dict[str, Any], out_dir: str) -> dict[str, str]:
        """Plot branch power flows."""
        flows = data.get("branch_flows") or data.get("flows")
        if not isinstance(flows, dict) or not flows:
            return {}

        labels = list(flows.keys())
        vals = list(flows.values())

        plt.figure(figsize=(12, 6))
        plt.bar(labels, vals, color="forestgreen", alpha=0.8)
        plt.ylabel("Power Flow (MW)")
        plt.title("Branch Power Flows")
        plt.xticks(rotation=45, ha="right")
        plt.grid(True, alpha=0.3, axis="y")

        os.makedirs(out_dir, exist_ok=True)
        base = os.path.join(out_dir, "branch_flows")
        paths = {}
        for ext in ("png",):
            path = f"{base}.{ext}"
            plt.savefig(path, dpi=150, bbox_inches="tight")
            paths[ext] = path
        plt.close()
        self._log("INFO", f"Branch flows plot saved to {paths}")
        return paths

    def run(self, config: dict[str, Any] | None) -> SkillResult:
        start_time = datetime.now()
        if config is None:
            config = {}
        self.logs = []
        self.artifacts = []

        valid, errors = self.validate(config)
        if not valid:
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error="; ".join(errors),
                logs=self.logs,
                start_time=start_time,
                end_time=datetime.now(),
            )

        try:
            data = self._load_data(config)
            out_dir = tempfile.mkdtemp(prefix="cloudpss_visualize_")

            plot_types = config.get("plot", {}).get(
                "type", ["time_series", "bus_voltages"]
            )

            plot_funcs = {
                "time_series": self._plot_time_series,
                "bus_voltages": self._plot_bus_voltages,
                "branch_flows": self._plot_branch_flows,
            }

            result_data = {"plots": {}}

            for plot_type in plot_types:
                if plot_type in plot_funcs:
                    paths = plot_funcs[plot_type](data, out_dir)
                    if paths:
                        result_data["plots"][plot_type] = paths
                        for ext, path in paths.items():
                            self.artifacts.append(
                                Artifact(
                                    name=f"{plot_type}.{ext}",
                                    path=path,
                                    type=f"image/{ext}",
                                )
                            )

            self._log(
                "INFO", f"Visualization complete with {len(self.artifacts)} plots"
            )

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                data=result_data,
                logs=self.logs,
                artifacts=self.artifacts,
                start_time=start_time,
                end_time=datetime.now(),
            )

        except Exception as e:
            self._log("ERROR", f"Visualization failed: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error=str(e),
                logs=self.logs,
                start_time=start_time,
                end_time=datetime.now(),
            )


__all__ = ["VisualizeTool", "validate_data_path"]
