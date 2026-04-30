"""Model validator skill v2 - local model-dict validation.

This validator intentionally does not pretend to run CloudPSS power-flow or EMT
studies. It validates in-memory model dictionaries and explicit study results
so model-building workflows have a trustworthy local gate before live tests.
"""

from __future__ import annotations

from collections import defaultdict, deque
from datetime import datetime
from typing import Any

from cloudpss_skills_v2.core import LogEntry, SkillResult, SkillStatus


RENEWABLE_TYPE_HINTS = ("pv", "pvs", "wind", "wtg", "pmsg", "dfig", "renewable")
BRANCH_TYPE_HINTS = ("line", "branch", "transformer", "trafo")
BUS_TYPE_HINTS = ("bus",)
GENERATOR_TYPE_HINTS = ("gen", "generator", "source", "pv", "wind", "wtg", "pmsg")


class ModelValidatorTool:
    name = "model_validator"

    def __init__(self):
        self.logs: list[LogEntry] = []

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill"],
            "properties": {
                "skill": {"type": "string", "const": "model_validator", "default": "model_validator"},
                "model": {"type": "object", "properties": {"components": {"type": "array", "items": {"type": "object"}, "default": []}}},
                "validation": {"type": "object", "properties": {"phases": {"type": "array", "items": {"type": "string"}, "default": ["structure", "topology", "parameters"]}}},
            },
        }

    def get_default_config(self) -> dict[str, Any]:
        return {
            "skill": self.name,
            "model": {"components": []},
            "validation": {"phases": ["structure", "topology", "parameters"]},
        }

    def validate(self, config: dict[str, Any] | None) -> tuple[bool, list[str]]:
        if not isinstance(config, dict):
            return False, ["config is required"]
        errors: list[str] = []
        model = self._resolve_model(config)
        if not isinstance(model, dict):
            errors.append("model or models[0].model must be an object")
        phases = self._phases(config)
        allowed = {"structure", "topology", "parameters", "powerflow", "emt"}
        invalid = [phase for phase in phases if phase not in allowed]
        if invalid:
            errors.append(f"validation.phases contains unsupported phases: {invalid}")
        return len(errors) == 0, errors

    def _resolve_model(self, config: dict[str, Any]) -> dict[str, Any] | None:
        if isinstance(config.get("model"), dict):
            return config["model"]
        models = config.get("models")
        if isinstance(models, list) and models and isinstance(models[0], dict):
            if isinstance(models[0].get("model"), dict):
                return models[0]["model"]
        return None

    def _phases(self, config: dict[str, Any]) -> list[str]:
        validation = config.get("validation", {}) or {}
        phases = validation.get("phases", ["structure", "topology", "parameters"])
        return list(phases or [])

    def _components(self, model: dict[str, Any]) -> list[dict[str, Any]]:
        components = model.get("components", [])
        if isinstance(components, dict):
            return [
                {**component, "id": component.get("id", comp_id)}
                for comp_id, component in components.items()
                if isinstance(component, dict)
            ]
        if isinstance(components, list):
            return [component for component in components if isinstance(component, dict)]
        return []

    def _component_id(self, component: dict[str, Any]) -> str:
        return str(component.get("id") or component.get("key") or component.get("name") or "")

    def _component_type(self, component: dict[str, Any]) -> str:
        return str(component.get("type") or component.get("component_type") or component.get("rid") or "").lower()

    def _is_type(self, component: dict[str, Any], hints: tuple[str, ...]) -> bool:
        text = " ".join(
            [
                self._component_id(component),
                str(component.get("name", "")),
                self._component_type(component),
            ]
        ).lower()
        return any(hint in text for hint in hints)

    def _type_has_hint(self, component: dict[str, Any], hints: tuple[str, ...]) -> bool:
        comp_type = self._component_type(component)
        return any(hint in comp_type for hint in hints)

    def _pins(self, component: dict[str, Any]) -> dict[str, Any]:
        pins = component.get("pins") or component.get("connections") or {}
        return pins if isinstance(pins, dict) else {}

    def _connection_targets(self, component: dict[str, Any]) -> list[str]:
        targets: list[str] = []
        for value in self._pins(component).values():
            if isinstance(value, str):
                targets.append(value)
            elif isinstance(value, dict):
                target = value.get("target") or value.get("target_bus") or value.get("bus")
                if target:
                    targets.append(str(target))
            elif isinstance(value, list):
                targets.extend(str(item) for item in value if item)
        for key in ("bus", "from_bus", "to_bus"):
            if component.get(key):
                targets.append(str(component[key]))
        return targets

    def _validate_structure(self, components: list[dict[str, Any]]) -> dict[str, Any]:
        issues: list[dict[str, Any]] = []
        ids = [self._component_id(component) for component in components]
        if not components:
            issues.append({"type": "empty_model", "message": "model has no components"})
        missing_ids = [index for index, comp_id in enumerate(ids) if not comp_id]
        for index in missing_ids:
            issues.append({"type": "missing_component_id", "component_index": index})
        duplicates = sorted({comp_id for comp_id in ids if comp_id and ids.count(comp_id) > 1})
        for comp_id in duplicates:
            issues.append({"type": "duplicate_component_id", "component": comp_id})
        return {"phase": "structure", "passed": not issues, "issues": issues}

    def _validate_topology(self, components: list[dict[str, Any]]) -> dict[str, Any]:
        issues: list[dict[str, Any]] = []
        bus_ids = {
            self._component_id(component)
            for component in components
            if self._type_has_hint(component, BUS_TYPE_HINTS)
        }
        adjacency: dict[str, set[str]] = defaultdict(set)

        for component in components:
            if not self._type_has_hint(component, BRANCH_TYPE_HINTS):
                continue
            targets = [target for target in self._connection_targets(component) if target in bus_ids]
            if len(targets) < 2:
                issues.append(
                    {
                        "type": "branch_unconnected",
                        "component": self._component_id(component),
                        "targets": targets,
                    }
                )
                continue
            a, b = targets[0], targets[1]
            adjacency[a].add(b)
            adjacency[b].add(a)

        for bus_id in bus_ids:
            adjacency.setdefault(bus_id, set())

        islands = self._find_islands(adjacency)
        if len(islands) > 1:
            issues.append({"type": "islands", "islands": islands})

        for component in components:
            if not self._type_has_hint(component, GENERATOR_TYPE_HINTS):
                continue
            targets = self._connection_targets(component)
            if not any(target in bus_ids for target in targets):
                issues.append(
                    {
                        "type": "source_unconnected",
                        "component": self._component_id(component),
                        "targets": targets,
                    }
                )

        return {
            "phase": "topology",
            "passed": not issues,
            "issues": issues,
            "bus_count": len(bus_ids),
            "island_count": len(islands),
        }

    def _find_islands(self, adjacency: dict[str, set[str]]) -> list[list[str]]:
        visited: set[str] = set()
        islands: list[list[str]] = []
        for start in sorted(adjacency):
            if start in visited:
                continue
            island: list[str] = []
            queue = deque([start])
            visited.add(start)
            while queue:
                node = queue.popleft()
                island.append(node)
                for neighbor in sorted(adjacency[node]):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            islands.append(island)
        return islands

    def _validate_parameters(self, components: list[dict[str, Any]], config: dict[str, Any]) -> dict[str, Any]:
        issues: list[dict[str, Any]] = []
        requirements = config.get("component_requirements", {}) or {}

        for component in components:
            params = component.get("parameters", {}) or component.get("args", {}) or {}
            comp_id = self._component_id(component)
            comp_type = self._component_type(component)
            required = list(requirements.get(comp_id, [])) + list(requirements.get(comp_type, []))

            if self._type_has_hint(component, RENEWABLE_TYPE_HINTS):
                required.extend(["p_mw"])
                if not self._pins(component) and not component.get("bus"):
                    issues.append({"type": "renewable_missing_connection", "component": comp_id})

            for key in sorted(set(required)):
                if key not in params or params[key] in (None, ""):
                    issues.append(
                        {
                            "type": "missing_required_parameter",
                            "component": comp_id,
                            "parameter": key,
                        }
                    )
                    continue
                try:
                    if key.endswith("_mw") and float(params[key]) <= 0:
                        issues.append(
                            {
                                "type": "non_positive_power_parameter",
                                "component": comp_id,
                                "parameter": key,
                                "value": params[key],
                            }
                        )
                except (TypeError, ValueError):
                    issues.append(
                        {
                            "type": "non_numeric_power_parameter",
                            "component": comp_id,
                            "parameter": key,
                            "value": params[key],
                        }
                    )

        return {"phase": "parameters", "passed": not issues, "issues": issues}

    def _validate_study_result(self, config: dict[str, Any], phase: str) -> dict[str, Any]:
        result = (config.get("study_results", {}) or {}).get(phase)
        if not isinstance(result, dict):
            return {
                "phase": phase,
                "passed": False,
                "issues": [
                    {
                        "type": "missing_explicit_study_result",
                        "message": f"{phase} validation requires study_results.{phase}",
                    }
                ],
            }
        passed = bool(result.get("success") or result.get("converged"))
        issues = [] if passed else [{"type": f"{phase}_failed", "result": result}]
        return {"phase": phase, "passed": passed, "issues": issues, "data_source": f"study_results.{phase}"}

    def _validate_expectations(self, components: list[dict[str, Any]], config: dict[str, Any]) -> list[dict[str, Any]]:
        issues: list[dict[str, Any]] = []
        expected = config.get("expectations", {}) or {}
        ids = {self._component_id(component) for component in components}
        for comp_id in expected.get("components_present", []) or []:
            if comp_id not in ids:
                issues.append({"type": "expected_component_missing", "component": comp_id})
        for comp_id in expected.get("components_absent", []) or []:
            if comp_id in ids:
                issues.append({"type": "unexpected_component_present", "component": comp_id})
        if "component_count" in expected and len(components) != int(expected["component_count"]):
            issues.append(
                {
                    "type": "component_count_mismatch",
                    "expected": int(expected["component_count"]),
                    "actual": len(components),
                }
            )
        return issues

    def run(self, config: dict[str, Any] | None = None) -> SkillResult:
        start_time = datetime.now()
        config = config or {}
        self.logs = []
        valid, errors = self.validate(config)
        if not valid:
            return SkillResult.failure(self.name, "; ".join(errors), {"errors": errors}, "validation")

        model = self._resolve_model(config) or {}
        components = self._components(model)
        phase_results: list[dict[str, Any]] = []
        for phase in self._phases(config):
            if phase == "structure":
                phase_results.append(self._validate_structure(components))
            elif phase == "topology":
                phase_results.append(self._validate_topology(components))
            elif phase == "parameters":
                phase_results.append(self._validate_parameters(components, config))
            else:
                phase_results.append(self._validate_study_result(config, phase))

        expectation_issues = self._validate_expectations(components, config)
        if expectation_issues:
            phase_results.append(
                {"phase": "expectations", "passed": False, "issues": expectation_issues}
            )

        passed = all(result["passed"] for result in phase_results)
        self.logs.append(LogEntry(level="info", message="Model validation completed"))
        data = {
            "model_rid": model.get("rid", ""),
            "component_count": len(components),
            "phases": phase_results,
            "issues": [
                issue
                for result in phase_results
                for issue in result.get("issues", [])
            ],
            "status": "pass" if passed else "fail",
            "data_source": "model",
            "confidence_level": "structure_validation",
        }
        return SkillResult(
            skill_name=self.name,
            status=SkillStatus.SUCCESS if passed else SkillStatus.FAILED,
            data=data,
            logs=self.logs,
            metrics={
                "component_count": len(components),
                "issue_count": len(data["issues"]),
                "phase_count": len(phase_results),
            },
            error=None if passed else "model validation failed",
            start_time=start_time,
            end_time=datetime.now(),
        )


__all__ = ["ModelValidatorTool"]
