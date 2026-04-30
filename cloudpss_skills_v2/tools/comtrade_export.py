"""COMTRADE Export Skill v2 - Export time-series data in IEEE COMTRADE ASCII format."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

from cloudpss_skills_v2.core import Artifact, LogEntry, SkillResult, SkillStatus


_ALLOWED_ANALOG_TYPES = {"voltage", "current"}
_DIGITAL_TYPES = {"digital", "status", "binary", "logic"}


@dataclass(frozen=True)
class NormalizedChannel:
    name: str
    channel_type: str
    kind: str
    values: list[float | int | bool]
    unit: str = ""
    phase: str = ""
    circuit: str = ""
    a: float = 1.0
    b: float = 0.0
    skew: float = 0.0
    primary: float = 1.0
    secondary: float = 1.0
    ps: str = "p"
    normal_state: int = 0


class ComtradeExportTool:
    """Export voltage/current time-series data as COMTRADE CFG + ASCII DAT files."""

    name: str = "comtrade_export"

    def __init__(self) -> None:
        self.logs: list[LogEntry] = []
        self.artifacts: list[Artifact] = []

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill"],
            "properties": {
                "skill": {"type": "string", "const": "comtrade_export", "default": "comtrade_export"},
                "source": {
                    "type": "object",
                    "properties": {
                        "data": {"type": "object", "default": {}},
                    },
                },
                "comtrade": {
                    "type": "object",
                    "properties": {
                        "station_name": {"type": "string", "default": "CloudPSS"},
                        "rec_dev_id": {"type": "string", "default": "CloudPSS_EMT"},
                        "rev_year": {"type": "integer", "default": 1999},
                        "frequency": {"type": "number", "default": 50.0},
                        "start_time": {"type": ["string", "null"], "default": None},
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "default": "./results/"},
                        "filename": {"type": "string", "default": "comtrade_export"},
                        "file_type": {"type": "string", "default": "ASCII"},
                        "format": {"type": "string", "default": "ASCII"},
                    },
                },
            },
        }

    def get_default_config(self) -> dict[str, object]:
        return {
            "skill": self.name,
            "source": {"data": {"time": [], "channels": []}},
            "comtrade": {
                "station_name": "CloudPSS",
                "rec_dev_id": "CloudPSS_EMT",
                "rev_year": 1999,
                "frequency": 50.0,
                "start_time": None,
            },
            "output": {
                "path": "./results/",
                "filename": "comtrade_export",
                "file_type": "ASCII",
                "format": "ASCII",
            },
        }

    def validate(self, config: dict[str, object] | None) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if config is None:
            return False, ["config is required"]
        if not isinstance(config, dict):
            return False, ["config must be a dictionary"]

        source = self._as_dict(config.get("source"))
        source_data = self._as_dict(source.get("data")) if source else None
        if source_data is None:
            return False, ["source.data with time-series data is required"]

        time_values = self._extract_time_values(source_data)
        if not time_values:
            errors.append("source.data.time must be a non-empty list of seconds")

        try:
            normalized = self._normalize_channels(source_data)
        except (TypeError, ValueError) as exc:
            errors.append(str(exc))
            normalized = []

        if not normalized:
            errors.append("source.data.channels must contain at least one channel")
        else:
            analog_count = 0
            time_len = len(time_values)
            for channel in normalized:
                if len(channel.values) != time_len:
                    errors.append(
                        f"channel '{channel.name}' has {len(channel.values)} samples; expected {time_len}"
                    )
                if channel.kind == "analog":
                    analog_count += 1
                    if channel.channel_type not in _ALLOWED_ANALOG_TYPES:
                        errors.append(
                            f"channel '{channel.name}' type must be voltage or current, got '{channel.channel_type}'"
                        )
            if analog_count == 0:
                errors.append("at least one voltage or current analog channel is required")

        output = self._as_dict(config.get("output")) or {}
        output_path = output.get("path")
        if not isinstance(output_path, str) or not output_path:
            errors.append("output.path is required")
        file_type = str(output.get("file_type", "ASCII")).upper()
        output_format = str(output.get("format", "ASCII")).upper()
        if file_type != "ASCII" or output_format not in {"ASCII", "COMTRADE"}:
            errors.append("only ASCII COMTRADE export is supported in this MVP")

        return (len(errors) == 0, errors)

    def _generate_cfg_header(
        self,
        station_name: str,
        rec_dev_id: str,
        num_channels: int,
        sample_rate: float,
        frequency: float,
        num_analog: int | None = None,
        num_digital: int = 0,
        rev_year: int = 1999,
    ) -> str:
        analog = num_channels if num_analog is None else num_analog
        total = analog + num_digital
        return "\n".join(
            [
                f"{station_name},{rec_dev_id},{rev_year}",
                f"{total},{analog}A,{num_digital}D",
                f"{frequency:.6f}",
                "1",
                f"{sample_rate:.6f},0",
            ]
        )

    def _generate_dat_record(self, values: list[int | float | bool], bit_width: int = 16) -> str:
        min_value = -(2 ** (bit_width - 1)) + 1
        max_value = (2 ** (bit_width - 1)) - 1
        clipped: list[str] = []
        for value in values:
            if isinstance(value, bool):
                clipped.append("1" if value else "0")
            else:
                numeric = int(round(float(value)))
                clipped.append(str(max(min_value, min(max_value, numeric))))
        return ",".join(clipped)

    def _format_timestamp(self, seconds: float) -> str:
        return str(int(round(seconds * 1_000_000)))

    def run(self, config: dict[str, object] | None) -> SkillResult:
        if config is None:
            config = {}
        self.logs = []
        self.artifacts = []
        start_time = datetime.now()

        valid, errors = self.validate(config)
        if not valid:
            return SkillResult.failure(
                skill_name=self.name,
                error="; ".join(errors),
                data={"stage": "validation", "errors": errors},
            )

        try:
            source = self._as_dict(config.get("source")) or {}
            source_data = self._as_dict(source.get("data"))
            if source_data is None:
                raise ValueError("source.data with time-series data is required")

            times = self._extract_time_values(source_data)
            channels = self._normalize_channels(source_data)
            analog_channels = [channel for channel in channels if channel.kind == "analog"]
            digital_channels = [channel for channel in channels if channel.kind == "digital"]

            comtrade_config = self._as_dict(config.get("comtrade")) or {}
            output_config = self._as_dict(config.get("output")) or {}
            sample_rate = self._sample_rate(times, comtrade_config.get("sample_rate"))
            station_name = str(comtrade_config.get("station_name", "CloudPSS"))
            rec_dev_id = str(comtrade_config.get("rec_dev_id", "CloudPSS_EMT"))
            rev_year = self._to_int(comtrade_config.get("rev_year"), 1999)
            frequency = self._to_float(comtrade_config.get("frequency"), 50.0)
            start_dt = self._parse_start_time(comtrade_config.get("start_time"))
            end_dt = start_dt + timedelta(seconds=times[-1] - times[0])

            output_dir = Path(str(output_config.get("path", "./results/")))
            output_dir.mkdir(parents=True, exist_ok=True)
            filename = str(output_config.get("filename", "comtrade_export")) or "comtrade_export"
            cfg_path = output_dir / f"{filename}.cfg"
            dat_path = output_dir / f"{filename}.dat"

            cfg_content = self._generate_cfg(
                station_name=station_name,
                rec_dev_id=rec_dev_id,
                rev_year=rev_year,
                frequency=frequency,
                sample_rate=sample_rate,
                times=times,
                analog_channels=analog_channels,
                digital_channels=digital_channels,
                start_time=start_dt,
                end_time=end_dt,
            )
            dat_content = self._generate_dat(times, analog_channels, digital_channels)

            cfg_path.write_text(cfg_content, encoding="utf-8")
            dat_path.write_text(dat_content, encoding="utf-8")

            artifacts = [
                Artifact(
                    name=cfg_path.name,
                    path=str(cfg_path),
                    type="cfg",
                    size_bytes=cfg_path.stat().st_size,
                    description="COMTRADE configuration file",
                ),
                Artifact(
                    name=dat_path.name,
                    path=str(dat_path),
                    type="dat",
                    size_bytes=dat_path.stat().st_size,
                    description="COMTRADE ASCII data file",
                ),
            ]
            logs = [
                LogEntry(
                    timestamp=datetime.now(),
                    level="info",
                    message="COMTRADE ASCII export completed",
                    context={"cfg_file": str(cfg_path), "dat_file": str(dat_path)},
                )
            ]
            self.artifacts = artifacts
            self.logs = logs

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                start_time=start_time,
                end_time=datetime.now(),
                data={
                    "cfg_file": str(cfg_path),
                    "dat_file": str(dat_path),
                    "file_type": "ASCII",
                    "analog_channels": len(analog_channels),
                    "digital_channels": len(digital_channels),
                    "samples": len(times),
                    "sample_rate_hz": sample_rate,
                },
                artifacts=artifacts,
                logs=logs,
                metrics={"channels": len(channels), "samples": len(times)},
            )
        except (OSError, TypeError, ValueError) as exc:
            return SkillResult.failure(
                skill_name=self.name,
                error=str(exc),
                data={"stage": "comtrade_export"},
            )

    def _generate_cfg(
        self,
        station_name: str,
        rec_dev_id: str,
        rev_year: int,
        frequency: float,
        sample_rate: float,
        times: list[float],
        analog_channels: list[NormalizedChannel],
        digital_channels: list[NormalizedChannel],
        start_time: datetime,
        end_time: datetime,
    ) -> str:
        lines = [
            f"{station_name},{rec_dev_id},{rev_year}",
            f"{len(analog_channels) + len(digital_channels)},{len(analog_channels)}A,{len(digital_channels)}D",
        ]
        for index, channel in enumerate(analog_channels, start=1):
            lines.append(self._format_analog_cfg_line(index, channel))
        for index, channel in enumerate(digital_channels, start=1):
            lines.append(self._format_digital_cfg_line(index, channel))
        lines.extend(
            [
                f"{frequency:.6f}",
                "1",
                f"{sample_rate:.6f},{len(times)}",
                self._format_cfg_datetime(start_time),
                self._format_cfg_datetime(end_time),
                "ASCII",
                "1.000000",
            ]
        )
        return "\n".join(lines) + "\n"

    def _generate_dat(
        self,
        times: list[float],
        analog_channels: list[NormalizedChannel],
        digital_channels: list[NormalizedChannel],
    ) -> str:
        base_time = times[0]
        lines: list[str] = []
        for sample_index, timestamp in enumerate(times, start=1):
            elapsed = timestamp - base_time
            values: list[int | float | bool] = []
            for channel in analog_channels:
                values.append(self._scale_analog_value(channel, sample_index - 1))
            for channel in digital_channels:
                values.append(1 if bool(channel.values[sample_index - 1]) else 0)
            payload = self._generate_dat_record(values, bit_width=16)
            lines.append(f"{sample_index},{self._format_timestamp(elapsed)},{payload}")
        return "\n".join(lines) + "\n"

    def _format_analog_cfg_line(self, index: int, channel: NormalizedChannel) -> str:
        numeric_values = [float(value) for value in channel.values]
        min_index = min(range(len(numeric_values)), key=numeric_values.__getitem__)
        max_index = max(range(len(numeric_values)), key=numeric_values.__getitem__)
        min_raw = self._scale_analog_value(channel, min_index)
        max_raw = self._scale_analog_value(channel, max_index)
        return ",".join(
            [
                str(index),
                channel.name,
                channel.phase,
                channel.circuit or channel.name,
                channel.unit or self._default_unit(channel.channel_type),
                self._float_text(channel.a),
                self._float_text(channel.b),
                self._float_text(channel.skew),
                str(min_raw),
                str(max_raw),
                self._float_text(channel.primary),
                self._float_text(channel.secondary),
                channel.ps,
            ]
        )

    def _format_digital_cfg_line(self, index: int, channel: NormalizedChannel) -> str:
        return ",".join(
            [
                str(index),
                channel.name,
                channel.phase,
                channel.circuit or channel.name,
                str(channel.normal_state),
            ]
        )

    def _normalize_channels(self, source_data: dict[str, object]) -> list[NormalizedChannel]:
        raw_channels = source_data.get("channels")
        raw_values = source_data.get("values")
        metadata = self._as_dict(source_data.get("metadata")) or {}

        channel_dicts: list[dict[str, object]] = []
        if isinstance(raw_channels, dict):
            for name, values in raw_channels.items():
                meta = self._as_dict(metadata.get(name)) or {}
                channel_dicts.append({**meta, "name": name, "values": values})
        elif raw_channels is None and isinstance(raw_values, dict):
            for name, values in raw_values.items():
                meta = self._as_dict(metadata.get(name)) or {}
                channel_dicts.append({**meta, "name": name, "values": values})
        elif isinstance(raw_channels, list):
            for item in raw_channels:
                channel_dict = self._as_dict(item)
                if channel_dict is None:
                    raise TypeError("source.data.channels entries must be dictionaries")
                channel_dicts.append(channel_dict)
        else:
            raise TypeError("source.data.channels must be a list or mapping")

        normalized_channels: list[NormalizedChannel] = []
        for channel in channel_dicts:
            name = str(channel.get("name") or channel.get("id") or "").strip()
            if not name:
                raise ValueError("each channel must have a name")
            values_obj = channel.get("values", channel.get("data"))
            if not isinstance(values_obj, list):
                raise ValueError(f"channel '{name}' values must be a list")
            channel_type = str(channel.get("type") or self._infer_type(name)).lower()
            kind = "digital" if channel_type in _DIGITAL_TYPES else "analog"
            normalized_type = "digital" if kind == "digital" else channel_type
            normalized_channels.append(
                NormalizedChannel(
                    name=name,
                    channel_type=normalized_type,
                    kind=kind,
                    values=list(values_obj),
                    unit=str(channel.get("unit", "")),
                    phase=str(channel.get("phase", "")),
                    circuit=str(channel.get("circuit", "")),
                    a=self._to_float(channel.get("a"), 1.0),
                    b=self._to_float(channel.get("b"), 0.0),
                    skew=self._to_float(channel.get("skew"), 0.0),
                    primary=self._to_float(channel.get("primary"), 1.0),
                    secondary=self._to_float(channel.get("secondary"), 1.0),
                    ps=str(channel.get("ps", "p")),
                    normal_state=self._to_int(channel.get("normal_state"), 0),
                )
            )
        return normalized_channels

    def _extract_time_values(self, source_data: dict[str, object]) -> list[float]:
        raw_time = source_data.get("time")
        if isinstance(raw_time, list):
            return [float(value) for value in raw_time]
        raw_timestamps = source_data.get("timestamps")
        if isinstance(raw_timestamps, list):
            return [float(value) for value in raw_timestamps]
        return []

    def _sample_rate(self, times: list[float], configured_rate: object) -> float:
        if configured_rate is not None:
            return self._to_float(configured_rate, 1.0)
        if len(times) < 2:
            return 1.0
        first_delta = times[1] - times[0]
        if first_delta <= 0:
            raise ValueError("source.data.time must be strictly increasing")
        for previous, current in zip(times, times[1:]):
            if current <= previous:
                raise ValueError("source.data.time must be strictly increasing")
        return 1.0 / first_delta

    def _scale_analog_value(self, channel: NormalizedChannel, sample_index: int) -> int:
        if channel.a == 0:
            raise ValueError(f"channel '{channel.name}' scale factor a must not be zero")
        raw = int(round((float(channel.values[sample_index]) - channel.b) / channel.a))
        return max(-32767, min(32767, raw))

    def _parse_start_time(self, value: object) -> datetime:
        if value is None:
            return datetime.now()
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            for fmt in (
                "%d/%m/%Y,%H:%M:%S.%f",
                "%Y-%m-%dT%H:%M:%S.%f",
                "%Y-%m-%dT%H:%M:%S",
            ):
                try:
                    return datetime.strptime(value, fmt)
                except ValueError:
                    continue
        raise ValueError("comtrade.start_time must be a datetime or supported timestamp string")

    def _format_cfg_datetime(self, value: datetime) -> str:
        return value.strftime("%d/%m/%Y,%H:%M:%S.%f")

    def _infer_type(self, channel_name: str) -> str:
        lower = channel_name.lower()
        if any(token in lower for token in ("current", "curr", "_i", "ia", "ib", "ic")):
            return "current"
        return "voltage"

    def _default_unit(self, channel_type: str) -> str:
        return "A" if channel_type == "current" else "V"

    def _float_text(self, value: float) -> str:
        return f"{value:.6f}"

    def _as_dict(self, value: object) -> dict[str, object] | None:
        return value if isinstance(value, dict) else None

    def _to_float(self, value: object, default: float) -> float:
        if value is None:
            return default
        if not isinstance(value, (int, float, str)):
            raise TypeError("numeric value must be int, float, or str")
        return float(value)

    def _to_int(self, value: object, default: int) -> int:
        if value is None:
            return default
        if not isinstance(value, (int, float, str)):
            raise TypeError("integer value must be int, float, or str")
        return int(value)


__all__ = ["ComtradeExportTool"]
