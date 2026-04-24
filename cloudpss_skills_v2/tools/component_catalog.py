"""Component Catalog Skill v2 - component discovery across multiple servers."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any

from cloudpss_skills_v2.core import LogEntry, SkillResult, SkillStatus


@dataclass
class ComponentInfo:
    rid: str = ""
    name: str = ""
    category: str = ""
    data_class: str | None = None
    description: str = ""


class ComponentCatalogTool:
    name = "component_catalog"

    def __init__(self):
        self.logs = []
        self.artifacts = []

    def get_default_config(self) -> dict[str, object]:
        return {
            "skill": self.name,
            "action": "search",
            "servers": [],
            "query": "",
            "rid": "",
        }

    def validate(self, config: dict[str, object] | None = None) -> tuple[bool, list[str]]:
        errors = []
        if config is None:
            return False, ["config is required"]
        if not isinstance(config, dict):
            return False, ["config must be a dictionary"]
        action = config.get("action", "search")
        if action not in {"search", "list", "resolve_rid"}:
            errors.append("action must be one of search, list, resolve_rid")
        servers = config.get("servers", [])
        if not isinstance(servers, list) or not servers:
            errors.append("servers must contain at least one server")
        if action == "resolve_rid" and not config.get("rid"):
            errors.append("rid is required for resolve_rid")
        return len(errors) == 0, errors

    def _iter_components(self, servers):
        items = []
        for server in servers:
            server_name = server.get("name", "server")
            for raw in server.get("components", []) or []:
                info = ComponentInfo(
                    rid=raw.get("rid", ""),
                    name=raw.get("name", ""),
                    category=raw.get("category", ""),
                    data_class=raw.get("data_class"),
                    description=raw.get("description", ""),
                )
                item = asdict(info)
                item["server"] = server_name
                item["metadata"] = raw.get("metadata", {})
                items.append(item)
        return items

    def _search(self, components, query):
        if not query:
            return components
        normalized = str(query).lower()
        matches = []
        for component in components:
            haystack = " ".join(
                [
                    component.get("rid", ""),
                    component.get("name", ""),
                    component.get("category", ""),
                    component.get("data_class") or "",
                    component.get("description", ""),
                ]
            ).lower()
            if normalized in haystack:
                matches.append(component)
        return matches

    def run(self, config: dict[str, object] | None = None) -> SkillResult:
        start_time = datetime.now()
        if config is None:
            config = {}
        self.logs = []
        valid, errors = self.validate(config)
        if not valid:
            return SkillResult.failure(self.name, "; ".join(errors), {"errors": errors}, "validation")
        action = config.get("action", "search")
        components = self._iter_components(config.get("servers", []))
        if action == "resolve_rid":
            resolved = next((component for component in components if component.get("rid") == config.get("rid")), None)
            data = {"component": resolved, "rid": config.get("rid")}
        elif action == "list":
            data = {"components": components}
        else:
            data = {"query": config.get("query", ""), "components": self._search(components, config.get("query", ""))}
        self.logs.append(LogEntry(level="info", message=f"Component catalog action completed: {action}"))
        return SkillResult(
            skill_name=self.name,
            status=SkillStatus.SUCCESS,
            data=data,
            logs=self.logs,
            metrics={"component_count": len(components), "server_count": len(config.get("servers", []))},
            start_time=start_time,
            end_time=datetime.now(),
        )


__all__ = ["ComponentCatalogTool", "ComponentInfo"]
