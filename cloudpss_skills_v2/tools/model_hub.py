"""Model Hub Skill v2 - local multi-server model index management."""

from __future__ import annotations

import base64
import copy
import json
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any

from cloudpss_skills_v2.core import LogEntry, SkillResult, SkillStatus


def normalize_model_name(name: str) -> str:
    """Normalize a model name into a stable lookup key."""
    return re.sub(r"[^a-zA-Z0-9_]", "_", str(name)).strip("_").lower()


def parse_token_username(token: str) -> str | None:
    """Best-effort JWT payload parsing for per-server token ownership."""
    if not token:
        return None
    try:
        parts = token.split(".")
        if len(parts) >= 2:
            payload = parts[1]
            payload += "=" * (-len(payload) % 4)
            data = json.loads(base64.urlsafe_b64decode(payload.encode("utf-8")))
            return data.get("username") or data.get("sub") or data.get("user")
    except Exception:
        return None
    return None


parse_token_userid = parse_token_username


@dataclass
class ModelEntry:
    name: str = ""
    rids: dict[str, str] = field(default_factory=dict)
    metadata: Any = None
    owner: str | None = None


@dataclass
class ServerInfo:
    name: str = ""
    url: str = ""
    token: str | None = None
    is_public: bool = False


class ModelHubTool:
    """Search and manage model metadata across multiple configured servers."""

    name = "model_hub"

    _cache: dict[str, Any] = {}

    def __init__(self):
        self.logs = []
        self.artifacts = []

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill"],
            "properties": {
                "skill": {"type": "string", "const": "model_hub", "default": "model_hub"},
                "action": {"type": "string", "enum": ["search", "list", "get", "cache_status", "clear_cache"], "default": "search"},
                "query": {"type": "string", "default": ""},
                "servers": {"type": "array", "items": {"type": "object"}, "default": []},
                "cache": {"type": "object", "properties": {"enabled": {"type": "boolean", "default": True}, "clear": {"type": "boolean", "default": False}}},
            },
        }

    def get_default_config(self) -> dict[str, object]:
        return {
            "skill": self.name,
            "action": "search",
            "query": "",
            "servers": [],
            "cache": {"enabled": True, "clear": False},
        }

    def validate(self, config: dict[str, object] | None = None) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if config is None:
            return False, ["config is required"]
        if not isinstance(config, dict):
            return False, ["config must be a dictionary"]

        action = config.get("action", "search")
        if action not in {"search", "list", "get", "cache_status", "clear_cache"}:
            errors.append("action must be one of search, list, get, cache_status, clear_cache")

        servers = config.get("servers", [])
        if action not in {"cache_status", "clear_cache"}:
            if not isinstance(servers, list) or not servers:
                errors.append("servers must contain at least one server")
        if isinstance(servers, list):
            for index, server in enumerate(servers):
                if not isinstance(server, dict):
                    errors.append(f"servers[{index}] must be an object")
                    continue
                if not server.get("name"):
                    errors.append(f"servers[{index}].name is required")
                if not server.get("url"):
                    errors.append(f"servers[{index}].url is required")
                if not server.get("is_public", False) and not server.get("token"):
                    errors.append(f"servers[{index}].token is required for private servers")
        return len(errors) == 0, errors

    def _normalize_server(self, server: dict[str, object]) -> ServerInfo:
        return ServerInfo(
            name=str(server.get("name")),
            url=str(server.get("url")),
            token=server.get("token"),
            is_public=bool(server.get("is_public", False)),
        )

    def _server_models(self, server: dict[str, object]) -> list[ModelEntry]:
        server_name = str(server.get("name"))
        owner = server.get("owner") or parse_token_username(server.get("token", ""))
        entries: list[ModelEntry] = []
        for raw in server.get("models", []) or []:
            if isinstance(raw, str):
                entries.append(ModelEntry(name=raw, rids={server_name: raw}, owner=owner))
                continue
            name = raw.get("name") or raw.get("rid") or "unnamed"
            rid = raw.get("rid") or raw.get("rids", {}).get(server_name) or str(name)
            rids = dict(raw.get("rids", {}))
            rids.setdefault(server_name, rid)
            entries.append(
                ModelEntry(
                    name=str(name),
                    rids=rids,
                    metadata=copy.deepcopy(raw.get("metadata", {})),
                    owner=raw.get("owner", owner),
                )
            )
        return entries

    def _build_index(self, servers: list[dict[str, object]]) -> dict[str, ModelEntry]:
        index: dict[str, ModelEntry] = {}
        for server in servers:
            for entry in self._server_models(server):
                key = normalize_model_name(entry.name)
                if key not in index:
                    index[key] = entry
                else:
                    index[key].rids.update(entry.rids)
                    if isinstance(index[key].metadata, dict) and isinstance(entry.metadata, dict):
                        index[key].metadata.update(entry.metadata)
        return index

    def _search(self, index: dict[str, ModelEntry], query: str) -> list[dict[str, object]]:
        normalized = normalize_model_name(query)
        matches = []
        for key, entry in index.items():
            text = " ".join([key, entry.name, json.dumps(entry.metadata or {}, ensure_ascii=False)]).lower()
            if not normalized or normalized in text:
                matches.append(asdict(entry))
        return sorted(matches, key=lambda item: item["name"])

    def run(self, config: dict[str, object] | None = None) -> SkillResult:
        start_time = datetime.now()
        if config is None:
            config = {}
        self.logs = []
        valid, errors = self.validate(config)
        if not valid:
            return SkillResult.failure(self.name, "; ".join(errors), {"errors": errors}, "validation")

        action = config.get("action", "search")
        cache_key = config.get("cache", {}).get("key", "default")
        if action == "clear_cache" or config.get("cache", {}).get("clear"):
            self._cache.pop(cache_key, None)
            return SkillResult.success(self.name, {"cache_key": cache_key, "cleared": True})
        if action == "cache_status":
            return SkillResult.success(self.name, {"keys": sorted(self._cache), "size": len(self._cache)})

        index = self._build_index(config.get("servers", []))
        if config.get("cache", {}).get("enabled", True):
            self._cache[cache_key] = {key: asdict(value) for key, value in index.items()}

        if action == "get":
            key = normalize_model_name(config.get("name") or config.get("rid") or config.get("query", ""))
            data: dict[str, object] = {"model": asdict(index[key]) if key in index else None}
        elif action == "list":
            data = {"models": [asdict(entry) for entry in index.values()]}
        else:
            data = {"query": config.get("query", ""), "models": self._search(index, config.get("query", ""))}

        data["servers"] = [asdict(self._normalize_server(server)) for server in config.get("servers", [])]
        self.logs.append(LogEntry(level="info", message=f"Model hub action completed: {action}"))
        return SkillResult(
            skill_name=self.name,
            status=SkillStatus.SUCCESS,
            data=data,
            logs=self.logs,
            metrics={"model_count": len(index), "server_count": len(config.get("servers", []))},
            start_time=start_time,
            end_time=datetime.now(),
        )


__all__ = ["ModelHubTool", "ModelEntry", "ServerInfo", "normalize_model_name", "parse_token_userid", "parse_token_username"]
