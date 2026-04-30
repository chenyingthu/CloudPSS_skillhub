"""EMT Simulation Skill v2 - Engine-agnostic electromagnetic transient simulation.

Runs EMT simulation using the PowerSkill API layer,
which delegates to the configured engine adapter.
"""

from __future__ import annotations

import csv
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from cloudpss_skills_v2.core.skill_result import (
    Artifact,
    LogEntry,
    SkillResult,
    SkillStatus,
)
from cloudpss_skills_v2.powerapi import EngineConfig
from cloudpss_skills_v2.powerskill import Engine, EMT

logger = logging.getLogger(__name__)


class EMTPreset:
    """EMT暂态仿真预设入口 - v2 engine-agnostic implementation."""

    name = "emt_simulation"
    description = "运行EMT暂态仿真并导出波形数据"

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "emt_simulation", "default": "emt_simulation"},
                "engine": {
                    "type": "string",
                    "enum": ["cloudpss"],
                    "default": "cloudpss",
                },
                "auth": {
                    "type": "object",
                    "properties": {
                        "token": {"type": "string"},
                        "token_file": {"type": "string", "default": ".cloudpss_token"},
                    },
                },
                "model": {
                    "type": "object",
                    "required": ["rid"],
                    "properties": {
                        "rid": {"type": "string", "default": "model/holdme/IEEE3"},
                        "source": {"enum": ["cloud", "local"], "default": "cloud"},
                    },
                },
                "simulation": {
                    "type": "object",
                    "properties": {
                        "duration": {"type": "number", "minimum": 0},
                        "step_size": {"type": "number", "minimum": 0},
                        "timeout": {"type": "integer", "minimum": 0, "default": 300},
                        "sampling_freq": {
                            "type": "integer",
                            "minimum": 1,
                            "default": 2000,
                        },
                    },
                },
                "fault": {
                    "type": "object",
                    "properties": {
                        "start_time": {"type": "number"},
                        "end_time": {"type": "number"},
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"enum": ["csv", "json"], "default": "csv"},
                        "path": {"type": "string", "default": "./results/"},
                        "prefix": {"type": "string", "default": "emt_output"},
                        "timestamp": {"type": "boolean", "default": True},
                        "channels": {
                            "type": "array",
                            "items": {"type": "string"},
                            "default": ["*"],
                        },
                    },
                },
            },
        }

    def get_default_config(self) -> dict[str, Any]:
        return {
            "skill": self.name,
            "engine": "cloudpss",
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "model/holdme/IEEE3", "source": "cloud"},
            "simulation": {"timeout": 300, "sampling_freq": 2000},
            "output": {
                "format": "csv",
                "path": "./results/",
                "prefix": "emt_output",
                "timestamp": True,
                "channels": ["*"],
            },
        }

    def __init__(self):
        self.logs: list[LogEntry] = []
        self.artifacts: list[Artifact] = []

    def _log(self, level: str, message: str) -> None:
        self.logs.append(
            LogEntry(timestamp=datetime.now(), level=level, message=message)
        )
        getattr(logger, level.lower(), logger.info)(message)

    def _get_api(self, config: dict[str, Any]) -> EMT:
        engine = config.get("engine", "cloudpss")
        auth = config.get("auth", {})
        engine_config = EngineConfig(
            engine_name=engine,
            base_url=auth.get("base_url", ""),
            extra={"auth": auth},
        )
        return Engine.create_emt(engine=engine, config=engine_config)

    def validate(self, config: dict[str, Any]) -> tuple[bool, list[str]]:
        errors = []
        if not config.get("model", {}).get("rid"):
            errors.append("必须提供 model.rid")
        auth = config.get("auth", {})
        if not auth.get("token") and not auth.get("token_file"):
            errors.append("必须提供 auth.token 或 auth.token_file")
        simulation = config.get("simulation", {})
        if simulation.get("duration", 0) < 0:
            errors.append("仿真时长应该大于0")
        return len(errors) == 0, errors

    def run(self, config: dict[str, Any]) -> SkillResult:
        start_time = datetime.now()
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
            api = self._get_api(config)
            self._log("INFO", f"使用引擎: {api.adapter.engine_name}")

            model_config = config["model"]
            model_rid = model_config["rid"]
            sim_config = config.get("simulation", {})
            fault_config = config.get("fault")

            self._log("INFO", f"运行EMT仿真: {model_rid}")

            sim_result = api.run_emt(
                model_id=model_rid,
                duration=sim_config.get("duration"),
                step_size=sim_config.get("step_size"),
                timeout=sim_config.get("timeout", 300),
                sampling_freq=sim_config.get("sampling_freq", 2000),
                fault_config=fault_config,
                source=model_config.get("source", "cloud"),
                auth=config.get("auth", {}),
            )

            if not sim_result.is_success:
                raise RuntimeError(
                    sim_result.errors[0] if sim_result.errors else "EMT仿真失败"
                )

            result_data = sim_result.data
            plots = result_data.get("plots", [])
            self._log("INFO", f"波形分组数: {len(plots)}")

            output_config = config.get("output", {})
            self._export_waveforms(plots, output_config)

            plot_summary = []
            for plot in plots:
                plot_summary.append(
                    {
                        "index": plot.get("index", 0),
                        "key": plot.get("key"),
                        "name": plot.get("name"),
                        "channel_count": plot.get("channel_count", 0),
                        "channels": plot.get("channels", [])[:10],
                    }
                )

            result_data["plots"] = plot_summary

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                data=result_data,
                artifacts=self.artifacts,
                logs=self.logs,
                metrics={
                    "plot_count": len(plots),
                    "exported_files": len(self.artifacts),
                },
                start_time=start_time,
                end_time=datetime.now(),
            )

        except Exception as e:
            self._log("ERROR", f"执行失败: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                data={"success": False, "error": str(e), "stage": "emt_simulation"},
                artifacts=self.artifacts,
                logs=self.logs,
                error=str(e),
                start_time=start_time,
                end_time=datetime.now(),
            )

    def _export_waveforms(self, plots: list[dict], output_config: dict) -> None:
        output_format = output_config.get("format", "csv")
        output_path = Path(output_config.get("path", "./results/"))
        prefix = output_config.get("prefix", "emt_output")
        use_timestamp = output_config.get("timestamp", True)
        requested_channels = output_config.get("channels", ["*"])
        export_all = "*" in requested_channels

        output_path.mkdir(parents=True, exist_ok=True)
        ts_suffix = (
            f"_{datetime.now().strftime('%Y%m%d_%H%M%S')}" if use_timestamp else ""
        )

        for plot in plots:
            plot_key = plot.get("key") or f"plot_{plot.get('index', 0)}"
            channel_data = plot.get("channel_data", {})
            if not channel_data:
                continue

            channels_to_export = (
                list(channel_data.keys())
                if export_all
                else [ch for ch in requested_channels if ch in channel_data]
            )
            if not channels_to_export:
                continue

            filename = f"{prefix}_{plot_key}{ts_suffix}.{output_format}"
            filepath = output_path / filename

            if output_format == "csv":
                self._export_csv(channel_data, channels_to_export, filepath)
            else:
                self._export_json(channel_data, channels_to_export, filepath)

            self.artifacts.append(
                Artifact(
                    name=filename,
                    path=str(filepath),
                    type=output_format,
                    size_bytes=filepath.stat().st_size,
                    description=f"波形数据 ({output_format.upper()})",
                )
            )
            self._log("INFO", f"导出: {filepath}")

    def _export_csv(
        self, channel_data: dict, channels: list[str], filepath: Path
    ) -> None:
        x_data = list(channel_data.values())[0].get("x", []) if channel_data else []
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["time"] + channels)
            for i in range(len(x_data)):
                row = [x_data[i]]
                for ch in channels:
                    y_data = channel_data.get(ch, {}).get("y", [])
                    row.append(y_data[i] if i < len(y_data) else "")
                writer.writerow(row)

    def _export_json(
        self, channel_data: dict, channels: list[str], filepath: Path
    ) -> None:
        export_data = {"channels": {}}
        for ch in channels:
            export_data["channels"][ch] = channel_data.get(ch, {})
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=2, default=str)


__all__ = ["EMTPreset"]
