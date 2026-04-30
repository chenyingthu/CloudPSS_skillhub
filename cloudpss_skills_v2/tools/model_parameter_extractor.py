"""Model parameter extraction tool.

The implementation supports deterministic extraction from inline model data and
a built-in component catalog. Inline extraction is the integration-testable path;
CloudPSS live extraction belongs in service-specific tests.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from cloudpss_skills_v2.core import SkillResult, SkillStatus


COMPONENT_DEFINITIONS: dict[str, dict[str, Any]] = {
    "bus_3p": {"type": "bus", "defaults": {"voltage": 110}},
    "line_3p": {"type": "line", "defaults": {"rating": 100}},
    "transformer_3p": {"type": "transformer", "defaults": {}},
    "generator_3p": {"type": "generator", "defaults": {}},
    "load_3p": {"type": "load", "defaults": {}},
}


@dataclass
class ComponentParameter:
    comp_key: str = ""
    comp_type: str = ""
    comp_rid: str = ""
    label: str = ""
    args: dict[str, Any] = field(default_factory=dict)
    pins: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "comp_key": self.comp_key,
            "comp_type": self.comp_type,
            "comp_rid": self.comp_rid,
            "label": self.label,
            "args": self.args,
            "pins": self.pins,
        }


@dataclass
class ParameterGroup:
    group_name: str = ""
    component_type: str = ""
    parameters: list[ComponentParameter] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "group_name": self.group_name,
            "component_type": self.component_type,
            "parameters": [parameter.to_dict() for parameter in self.parameters],
        }


class ModelParameterExtractorTool:
    """Extract component parameters from an inline model description."""

    name = "model_parameter_extractor"

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill"],
            "properties": {
                "skill": {"type": "string", "const": "model_parameter_extractor", "default": "model_parameter_extractor"},
                "model": {
                    "type": "object",
                    "properties": {
                        "rid": {"type": "string", "default": ""},
                        "source": {"type": "string", "default": "inline"},
                        "components": {"type": "array", "items": {"type": "object"}, "default": []},
                    },
                },
                "component_types": {"type": "array", "items": {"type": "string"}, "default": []},
                "extraction": {
                    "type": "object",
                    "properties": {
                        "include_args": {"type": "boolean", "default": True},
                        "include_pins": {"type": "boolean", "default": True},
                    },
                },
                "output": {"type": "object", "properties": {"format": {"type": "string", "default": "json"}}},
            },
        }

    def get_default_config(self) -> dict[str, Any]:
        return {
            "skill": self.name,
            "model": {"rid": "", "source": "inline", "components": []},
            "component_types": [],
            "extraction": {"include_args": True, "include_pins": True},
            "output": {"format": "json"},
        }

    def validate(self, config: dict[str, Any] | None = None) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if not isinstance(config, dict):
            return False, ["config is required"]

        model = config.get("model")
        if not isinstance(model, dict) or not model.get("rid"):
            errors.append("model.rid is required")

        component_types = config.get("component_types")
        if component_types is not None and not isinstance(component_types, list):
            errors.append("component_types must be a list")

        components = model.get("components", []) if isinstance(model, dict) else []
        if components is not None and not isinstance(components, list):
            errors.append("model.components must be a list")

        return len(errors) == 0, errors

    def _component_type(self, component: dict[str, Any]) -> str:
        return str(
            component.get("type")
            or component.get("component_type")
            or component.get("definition")
            or "unknown"
        )

    def _group_name(self, component_type: str) -> str:
        normalized = component_type.replace("_3p", "").replace("_", " ").strip()
        return f"{normalized.title()}s" if normalized else "Unknown"

    def _fallback_components(self, component_types: list[str]) -> list[dict[str, Any]]:
        selected = component_types or list(COMPONENT_DEFINITIONS)
        components = []
        for index, component_type in enumerate(selected, start=1):
            definition = COMPONENT_DEFINITIONS.get(component_type, {})
            components.append(
                {
                    "key": f"{component_type}_{index}",
                    "type": component_type,
                    "rid": f"model/{component_type}/{index}",
                    "name": f"{component_type.upper()} {index}",
                    "args": dict(definition.get("defaults", {})),
                    "pins": {},
                }
            )
        return components

    def run(self, config: dict[str, Any] | None = None) -> SkillResult:
        start_time = datetime.now()
        config = config or {}
        valid, errors = self.validate(config)
        if not valid:
            return SkillResult.failure(
                skill_name=self.name,
                error="; ".join(errors),
                data={"stage": "validation", "errors": errors},
            )

        model = config["model"]
        requested_types = list(config.get("component_types") or [])
        extraction = config.get("extraction", {})
        include_args = extraction.get("include_args", True)
        include_pins = extraction.get("include_pins", True)

        components = list(model.get("components") or [])
        if not components:
            components = self._fallback_components(requested_types)

        groups: dict[str, ParameterGroup] = {}
        for component in components:
            component_type = self._component_type(component)
            if requested_types and component_type not in requested_types:
                continue

            parameter = ComponentParameter(
                comp_key=str(component.get("key") or component.get("id") or ""),
                comp_type=component_type,
                comp_rid=str(component.get("rid") or component.get("definition") or ""),
                label=str(component.get("name") or component.get("label") or ""),
                args=dict(component.get("args") or component.get("parameters") or {})
                if include_args
                else {},
                pins=dict(component.get("pins") or {}) if include_pins else {},
            )
            groups.setdefault(
                component_type,
                ParameterGroup(
                    group_name=self._group_name(component_type),
                    component_type=component_type,
                ),
            ).parameters.append(parameter)

        result_groups = [group.to_dict() for group in groups.values()]
        return SkillResult(
            skill_name=self.name,
            status=SkillStatus.SUCCESS,
            data={
                "model_rid": model["rid"],
                "groups": result_groups,
                "component_count": sum(
                    len(group["parameters"]) for group in result_groups
                ),
            },
            metrics={"group_count": len(result_groups)},
            start_time=start_time,
            end_time=datetime.now(),
        )


__all__ = [
    "ModelParameterExtractorTool",
    "ComponentParameter",
    "ParameterGroup",
]
