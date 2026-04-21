"""Visualize Tool - Plot simulation results.

可视化工具 - 绘制仿真结果。
"""

from __future__ import annotations

import json
import logging
import os
import tempfile
from datetime import datetime
from typing import Any

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

    def validate(self, config: dict | None) -> tuple[bool, list[str]]:
        errors = []
        if not config:
            errors.append("config is required")
            return (False, errors)
        if not config.get("model", {}).get("rid"):
            errors.append("model.rid is required")
        return (len(errors) == 0, errors)

    def _load_data(self, config: dict) -> dict:
        """Load data from config or result."""
        if config.get("data") is not None:
            return config["data"]

        result = config.get("result")
        if result:
            return result

        source = config.get("source") or {}
        if source.get("data") is not None:
            return source["data"]
        if source.get("data_file") is not None:
            path = source["data_file"]
            with open(path, "r") as f:
                return json.load(f)

        return {}

    def _plot_time_series(self, data: dict, out_dir: str) -> dict[str, str]:
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

    def _plot_bus_voltages(self, data: dict, out_dir: str) -> dict[str, str]:
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

    def _plot_branch_flows(self, data: dict, out_dir: str) -> dict[str, str]:
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

    def run(self, config: dict | None) -> SkillResult:
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
                                    mime=f"image/{ext}",
                                )
                            )

            self._log(
                "INFO", f"Visualization complete with {len(self.artifacts)} plots"
            )

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.COMPLETED,
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


__all__ = ["VisualizeTool"]
