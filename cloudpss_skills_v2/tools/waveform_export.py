"""Waveform Export Skill v2 - Export waveform data from simulation results."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from cloudpss_skills_v2.core import Artifact, LogEntry, SkillResult, SkillStatus


class WaveformExportTool:
    """Export waveform data from in-memory traces to CSV or JSON."""

    name = "waveform_export"

    def __init__(self):
        self.logs: list[LogEntry] = []
        self.artifacts: list[Artifact] = []

    def get_default_config(self):
        return {
            "skill": self.name,
            "source": {"job_id": ""},
            "data": {"time": [], "channels": {}},
            "export": {"channels": [], "time_range": {}},
            "output": {"format": "csv", "path": "./results/", "filename": ""},
        }

    def validate(self, config=None):
        errors = []
        if config is None:
            return False, ["config is required"]
        source = config.get("source", {})
        data = config.get("data", {})
        job_id = source.get("job_id", "") if source else ""
        has_inline_data = bool(data.get("time")) and bool(data.get("channels"))
        if (not job_id or job_id == "your_job_id_here") and not has_inline_data:
            errors.append("source.job_id or data.time/data.channels is required")
        output_format = config.get("output", {}).get("format", "csv")
        if output_format not in {"csv", "json"}:
            errors.append("output.format must be csv or json")
        return len(errors) == 0, errors

    def _log(self, level: str, message: str) -> None:
        self.logs.append(LogEntry(timestamp=datetime.now(), level=level, message=message))

    def _format_csv(self, time=None, data=None):
        if not time or not data:
            return ""
        lines = []
        channels = list(data.keys())
        lines.append("time," + ",".join(channels))
        for i, t in enumerate(time):
            row = [str(t)]
            for ch in channels:
                values = data.get(ch, [])
                row.append(str(values[i]) if i < len(values) else "")
            lines.append(",".join(row))
        return "\n".join(lines)

    def _format_json(self, time=None, data=None):
        return json.dumps({"time": time or [], "channels": data or {}}, indent=2)

    def _filter_channels(self, data=None, channels=None):
        data = data or {}
        if not channels or "*" in channels:
            return data
        return {name: values for name, values in data.items() if name in channels}

    def _filter_time_range(self, time=None, data=None, start=None, end=None):
        time = list(time or [])
        data = data or {}
        if start is None and end is None:
            return time, data
        indices = [
            idx
            for idx, value in enumerate(time)
            if (start is None or value >= start) and (end is None or value <= end)
        ]
        filtered_time = [time[idx] for idx in indices]
        filtered_data = {
            name: [values[idx] for idx in indices if idx < len(values)]
            for name, values in data.items()
        }
        return filtered_time, filtered_data

    def run(self, config=None):
        start_time = datetime.now()
        self.logs = []
        self.artifacts = []
        config = config or {}
        valid, errors = self.validate(config)
        if not valid:
            return SkillResult.failure(
                skill_name=self.name,
                error="; ".join(errors),
                data={"stage": "validation", "errors": errors},
            )

        try:
            source_data = config.get("data", {})
            time = source_data.get("time", [])
            data = source_data.get("channels", {})
            export_config = config.get("export", {})
            output_config = config.get("output", {})

            data = self._filter_channels(data, export_config.get("channels", []))
            time_range = export_config.get("time_range", {})
            time, data = self._filter_time_range(
                time,
                data,
                start=time_range.get("start"),
                end=time_range.get("end"),
            )

            output_format = output_config.get("format", "csv")
            content = (
                self._format_json(time, data)
                if output_format == "json"
                else self._format_csv(time, data)
            )

            output_path = Path(output_config.get("path", "./results/"))
            output_path.mkdir(parents=True, exist_ok=True)
            filename = output_config.get("filename") or (
                f"{self.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{output_format}"
            )
            filepath = output_path / filename
            filepath.write_text(content, encoding="utf-8")
            self.artifacts.append(
                Artifact(
                    name=filepath.name,
                    path=str(filepath),
                    type=output_format,
                    size_bytes=filepath.stat().st_size,
                    description="Exported waveform data",
                )
            )
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                data={
                    "channel_count": len(data),
                    "sample_count": len(time),
                    "output_file": str(filepath),
                },
                artifacts=self.artifacts,
                logs=self.logs,
                start_time=start_time,
                end_time=datetime.now(),
            )
        except Exception as exc:
            self._log("error", str(exc))
            return SkillResult.failure(self.name, str(exc), {"stage": "waveform_export"})


__all__ = ["WaveformExportTool"]
