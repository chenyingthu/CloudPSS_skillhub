"""Model Builder Skill v2 - programmatic in-memory model construction."""

from __future__ import annotations

import copy
import re
from datetime import datetime
from typing import Any

from cloudpss_skills_v2.core import LogEntry, SkillResult, SkillStatus


class ModelBuilderTool:
    name = "model_builder"

    def __init__(self):
        self.logs = []
        self.artifacts = []

    def get_default_config(self):
        return {"skill": self.name, "base_model": {"components": []}, "operations": []}

    def _coerce_scalar_value(self, value, target_type):
        if target_type in (None, "any"):
            return value
        normalized = str(target_type).lower()
        if normalized in {"str", "string"}:
            return str(value)
        if normalized in {"int", "integer"}:
            return int(value)
        if normalized in {"float", "number"}:
            return float(value)
        if normalized in {"bool", "boolean"}:
            if isinstance(value, bool):
                return value
            if isinstance(value, str):
                lowered = value.strip().lower()
                if lowered in {"true", "1", "yes", "y", "on"}:
                    return True
                if lowered in {"false", "0", "no", "n", "off"}:
                    return False
            return bool(value)
        raise ValueError(f"unsupported target type: {target_type}")

    def _normalize_lookup_value(self, value):
        return re.sub(r"[^a-z0-9]+", "_", str(value).strip().lower()).strip("_")

    def _first_present(self, params, keys):
        for key in keys:
            if key in params and params[key] is not None:
                return params[key]
        return None

    def validate(self, config):
        errors = []
        if config is None:
            return False, ["config is required"]
        if not isinstance(config, dict):
            return False, ["config must be a dictionary"]
        if not isinstance(config.get("base_model", {}), dict):
            errors.append("base_model must be an object")
        operations = config.get("operations", [])
        if not isinstance(operations, list):
            errors.append("operations must be a list")
            return False, errors
        for index, operation in enumerate(operations):
            if not isinstance(operation, dict):
                errors.append(f"operations[{index}] must be an object")
                continue
            action = operation.get("action") or operation.get("op")
            if action not in {"add", "modify", "update", "delete", "remove"}:
                errors.append(f"operations[{index}].action is invalid")
            if action == "add" and not operation.get("component"):
                errors.append(f"operations[{index}].component is required for add")
            if action in {"modify", "update", "delete", "remove"} and not (operation.get("id") or operation.get("name")):
                errors.append(f"operations[{index}] requires id or name")
        return len(errors) == 0, errors

    def _components(self, model):
        components = model.setdefault("components", [])
        if isinstance(components, dict):
            converted = []
            for comp_id, component in components.items():
                current = copy.deepcopy(component)
                current.setdefault("id", comp_id)
                converted.append(current)
            model["components"] = converted
        return model["components"]

    def _find_component(self, components, identifier):
        wanted = self._normalize_lookup_value(identifier)
        for component in components:
            if wanted in {self._normalize_lookup_value(component.get("id", "")), self._normalize_lookup_value(component.get("name", ""))}:
                return component
        return None

    def _coerce_parameters(self, parameters, schema):
        result = copy.deepcopy(parameters or {})
        for key, target_type in (schema or {}).items():
            if key in result:
                result[key] = self._coerce_scalar_value(result[key], target_type)
        return result

    def _add_component(self, components, operation):
        component = copy.deepcopy(operation["component"])
        component_id = component.get("id") or component.get("name")
        if not component_id:
            raise ValueError("component.id or component.name is required")
        if self._find_component(components, component_id):
            raise ValueError(f"component already exists: {component_id}")
        component.setdefault("id", str(component_id))
        component.setdefault("parameters", {})
        component["parameters"] = self._coerce_parameters(component.get("parameters", {}), operation.get("schema", {}))
        components.append(component)
        return component

    def _modify_component(self, components, operation):
        component = self._find_component(components, operation.get("id") or operation.get("name"))
        if component is None:
            raise ValueError("component not found")
        updates = copy.deepcopy(operation.get("updates") or operation.get("component") or {})
        params = updates.pop("parameters", None)
        component.update(updates)
        if params is not None:
            component.setdefault("parameters", {})
            component["parameters"].update(self._coerce_parameters(params, operation.get("schema", {})))
        return component

    def _delete_component(self, components, operation):
        component = self._find_component(components, operation.get("id") or operation.get("name"))
        if component is None:
            raise ValueError("component not found")
        components.remove(component)
        return component

    def run(self, config):
        start_time = datetime.now()
        if config is None:
            config = {}
        self.logs = []
        valid, errors = self.validate(config)
        if not valid:
            return SkillResult.failure(self.name, "; ".join(errors), {"errors": errors}, "validation")
        try:
            model = copy.deepcopy(config.get("base_model", {}))
            components = self._components(model)
            applied = []
            for operation in config.get("operations", []):
                action = operation.get("action") or operation.get("op")
                if action == "add":
                    changed = self._add_component(components, operation)
                elif action in {"modify", "update"}:
                    changed = self._modify_component(components, operation)
                else:
                    changed = self._delete_component(components, operation)
                applied.append({"action": action, "id": changed.get("id")})
            self.logs.append(LogEntry(level="info", message="Model builder operations applied"))
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                data={"model": model, "operations_applied": applied},
                logs=self.logs,
                metrics={"component_count": len(components), "operation_count": len(applied)},
                start_time=start_time,
                end_time=datetime.now(),
            )
        except (TypeError, ValueError) as exc:
            return SkillResult.failure(self.name, str(exc), stage="model_builder")


__all__ = ["ModelBuilderTool"]
