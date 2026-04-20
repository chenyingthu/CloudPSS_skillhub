"""Model Hub Skill v2."""

from __future__ import annotations
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from cloudpss_skills_v2.core import Artifact, LogEntry, SkillResult, SkillStatus


def normalize_model_name(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_]", "_", name).strip("_")


def parse_token_username(token: str) -> Optional[str]:
    if not token:
        return None
    try:
        import base64, json

        parts = token.split(".")
        if len(parts) >= 2:
            payload = parts[1]
            padding = 4 - len(payload) % 4
            if padding != 4:
                payload += "=" * padding
            data = json.loads(base64.b64decode(payload))
            return data.get("username") or data.get("sub")
    except Exception:
        pass
    return None


parse_token_userid = parse_token_username


@dataclass
class ModelEntry:
    name: str = ""
    rids: Dict[str, str] = field(default_factory=dict)
    metadata: Any = None
    owner: Optional[str] = None


@dataclass
class ServerInfo:
    name: str = ""
    url: str = ""
    token: Optional[str] = None
    is_public: bool = False


class ModelHubSkill:
    name = "model_hub"

    def __init__(self):
        self.logs = []
        self.artifacts = []

    def validate(self, config: Optional[Dict] = None) -> tuple:
        errors = []
        if not config:
            errors.append("config is required")
        return (len(errors) == 0, errors)

    def run(self, config: Optional[Dict] = None) -> SkillResult:
        if config is None:
            config = {}
        valid, errors = self.validate(config)
        if not valid:
            return SkillResult(
                skill_name=self.name, status=SkillStatus.FAILED, errors=errors
            )
        # TODO: Implement model_hub logic
        return SkillResult(skill_name=self.name, status=SkillStatus.SUCCESS)


__all__ = [
    "ModelHubSkill",
    "ModelEntry",
    "ServerInfo",
    "normalize_model_name",
    "parse_token_userid",
    "parse_token_username",
]
