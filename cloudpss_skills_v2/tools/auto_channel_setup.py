"""Auto Channel Setup Skill v2.

Build measurement channel definitions for simulation output configurations.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from cloudpss_skills_v2.core import LogEntry, SkillResult, SkillStatus


class AutoChannelSetupTool:
    """Automatically generate voltage, current, power and frequency channels."""

    name = "auto_channel_setup"

    def __init__(self):
        self.logs = []
        self.artifacts = []

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill"],
            "properties": {
                "skill": {"type": "string", "const": "auto_channel_setup", "default": "auto_channel_setup"},
                "model": {"type": "object", "properties": {"rid": {"type": "string", "default": ""}}},
                "channels": {
                    "type": "object",
                    "properties": {
                        "voltage": {"type": "object", "properties": {"buses": {"type": "array", "items": {"type": "string"}, "default": []}}},
                        "current": {"type": "object", "properties": {"components": {"type": "array", "items": {"type": "string"}, "default": []}}},
                        "power": {"type": "object", "properties": {"components": {"type": "array", "items": {"type": "string"}, "default": []}}},
                        "frequency": {"type": "object", "properties": {"buses": {"type": "array", "items": {"type": "string"}, "default": []}}},
                    },
                },
                "sampling": {"type": "object", "properties": {"frequency": {"type": "number", "default": 50.0}}},
                "output": {"type": "object", "properties": {"format": {"type": "string", "default": "json"}, "group_by_type": {"type": "boolean", "default": True}}},
            },
        }

    def get_default_config(self) -> dict[str, Any]:
        return {
            "skill": self.name,
            "model": {"rid": ""},
            "channels": {
                "voltage": {"buses": []},
                "current": {"components": []},
                "power": {"components": []},
                "frequency": {"buses": []},
            },
            "sampling": {"frequency": 50.0},
            "output": {"format": "json", "group_by_type": True},
        }

    def validate(self, config):
        errors = []
        if config is None:
            return False, ["config is required"]
        if not isinstance(config, dict):
            return False, ["config must be a dictionary"]

        channel_config = config.get("channels", {})
        if not isinstance(channel_config, dict):
            errors.append("channels must be an object")
            return False, errors

        has_request = False
        for key in ("voltage", "current", "power", "frequency"):
            value = channel_config.get(key)
            if value:
                has_request = True
                if not isinstance(value, (dict, list, tuple)):
                    errors.append(f"channels.{key} must be an object or list")

        if not has_request:
            errors.append("at least one channel type must be requested")

        frequency = config.get("sampling", {}).get("frequency", config.get("frequency", 50.0))
        try:
            if float(frequency) <= 0:
                errors.append("sampling.frequency must be positive")
        except (TypeError, ValueError):
            errors.append("sampling.frequency must be numeric")

        return len(errors) == 0, errors

    def _build_voltage_channel(self, bus_name, v_base=None, freq=50.0):
        if not bus_name:
            raise ValueError("bus_name is required")
        channel = {
            "id": f"V_{bus_name}",
            "name": f"Voltage {bus_name}",
            "type": "voltage",
            "target": {"bus": str(bus_name)},
            "unit": "pu" if v_base in (None, "") else "kV",
            "sampling_frequency": float(freq),
        }
        if v_base not in (None, ""):
            channel["base"] = float(v_base)
        return channel

    def _build_current_channel(self, comp_name, pin_suffix="", freq=50.0):
        if not comp_name:
            raise ValueError("comp_name is required")
        suffix = str(pin_suffix or "").strip()
        suffix_part = f"_{suffix}" if suffix else ""
        return {
            "id": f"I_{comp_name}{suffix_part}",
            "name": f"Current {comp_name}{suffix_part}",
            "type": "current",
            "target": {"component": str(comp_name), "pin": suffix or None},
            "unit": "A",
            "sampling_frequency": float(freq),
        }

    def _build_power_channel(self, comp_name, power_type="P", freq=50.0):
        if not comp_name:
            raise ValueError("comp_name is required")
        normalized = str(power_type or "P").upper()
        if normalized not in {"P", "Q", "S", "PQ"}:
            raise ValueError("power_type must be one of P, Q, S, PQ")
        return {
            "id": f"{normalized}_{comp_name}",
            "name": f"{normalized} Power {comp_name}",
            "type": "power",
            "power_type": normalized,
            "target": {"component": str(comp_name)},
            "unit": "MVA" if normalized == "S" else "MW" if normalized == "P" else "Mvar",
            "sampling_frequency": float(freq),
        }

    def _build_frequency_channel(self, bus_name, freq=50.0):
        if not bus_name:
            raise ValueError("bus_name is required")
        return {
            "id": f"F_{bus_name}",
            "name": f"Frequency {bus_name}",
            "type": "frequency",
            "target": {"bus": str(bus_name)},
            "unit": "Hz",
            "nominal_frequency": float(freq),
            "sampling_frequency": float(freq),
        }

    def _generate_output_config(self, channels):
        grouped = self._group_channels_by_type(channels)
        return {
            "channels": channels,
            "groups": grouped,
            "channel_count": len(channels),
            "enabled": [channel["id"] for channel in channels],
        }

    def _group_channels_by_type(self, channels):
        grouped: dict[str, list[dict[str, Any]]] = {}
        for channel in channels or []:
            grouped.setdefault(channel.get("type", "unknown"), []).append(channel)
        return grouped

    def _iter_items(self, value, default_key):
        if isinstance(value, dict):
            if default_key in value:
                items = value.get(default_key) or []
            else:
                items = value.get("items") or []
        else:
            items = value or []
        if isinstance(items, (str, dict)):
            items = [items]
        return items

    def run(self, config):
        start_time = datetime.now()
        if config is None:
            config = {}
        self.logs = []
        self.artifacts = []

        valid, errors = self.validate(config)
        if not valid:
            return SkillResult.failure(self.name, "; ".join(errors), {"errors": errors}, "validation")

        try:
            freq = float(config.get("sampling", {}).get("frequency", config.get("frequency", 50.0)))
            channels_config = config.get("channels", {})
            channels = []

            for item in self._iter_items(channels_config.get("voltage"), "buses"):
                if isinstance(item, dict):
                    channels.append(self._build_voltage_channel(item.get("name") or item.get("bus"), item.get("v_base"), freq))
                else:
                    channels.append(self._build_voltage_channel(item, None, freq))

            for item in self._iter_items(channels_config.get("current"), "components"):
                if isinstance(item, dict):
                    pins = item.get("pins") or [item.get("pin") or item.get("pin_suffix") or ""]
                    for pin in pins:
                        channels.append(self._build_current_channel(item.get("name") or item.get("component"), pin, freq))
                else:
                    channels.append(self._build_current_channel(item, "", freq))

            for item in self._iter_items(channels_config.get("power"), "components"):
                if isinstance(item, dict):
                    power_types = item.get("power_types") or [item.get("power_type", "P")]
                    for power_type in power_types:
                        channels.append(self._build_power_channel(item.get("name") or item.get("component"), power_type, freq))
                else:
                    channels.append(self._build_power_channel(item, "P", freq))

            for item in self._iter_items(channels_config.get("frequency"), "buses"):
                bus = item.get("name") or item.get("bus") if isinstance(item, dict) else item
                channels.append(self._build_frequency_channel(bus, freq))

            output_config = self._generate_output_config(channels)
            self.logs.append(LogEntry(level="info", message="Auto channel setup completed"))
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                data={"channels": channels, "output_config": output_config},
                logs=self.logs,
                metrics={"channel_count": len(channels)},
                start_time=start_time,
                end_time=datetime.now(),
            )
        except (TypeError, ValueError) as exc:
            return SkillResult.failure(self.name, str(exc), stage="auto_channel_setup")


__all__ = ["AutoChannelSetupTool"]
