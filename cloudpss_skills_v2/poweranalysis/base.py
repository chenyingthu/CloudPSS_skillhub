from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from cloudpss_skills_v2.core.skill_result import (
    Artifact,
    LogEntry,
    SkillResult,
    SkillStatus,
)
from cloudpss_skills_v2.base import AnalysisBase
from cloudpss_skills_v2.powerskill import Engine, ModelHandle, ComponentType

logger = logging.getLogger(__name__)


def _as_float(value, default=0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


class PowerAnalysisBase(ABC):
    """Power analysis skill base class using PowerSkill APIs.

    This is the recommended base class for all power analysis skills
    that use the PowerSkill API layer (Engine, PowerFlow, etc.).

    For backward compatibility, AnalysisBase is aliased to this class.
    """

    name: str = ""
    description: str = ""

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string"},
                "engine": {
                    "type": "string",
                    "enum": ["cloudpss", "pandapower"],
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
                        "rid": {"type": "string"},
                        "source": {"enum": ["cloud", "local"], "default": "cloud"},
                    },
                },
            },
        }

    def get_default_config(self) -> dict[str, Any]:
        return {
            "skill": self.name,
            "engine": "cloudpss",
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "", "source": "cloud"},
        }

    def __init__(self):
        self.logs: list[LogEntry] = []
        self.artifacts: list[Artifact] = []

    def _log(self, level: str, message: str) -> None:
        self.logs.append(
            LogEntry(timestamp=datetime.now(), level=level, message=message)
        )
        getattr(logger, level.lower(), logger.info)(message)

    def validate(self, config: dict[str, Any]) -> tuple[bool, list[str]]:
        errors = []
        if not config.get("model", {}).get("rid"):
            errors.append("必须提供 model.rid")
        auth = config.get("auth", {})
        if not auth.get("token") and not auth.get("token_file"):
            errors.append("必须提供 auth.token 或 auth.token_file")
        return len(errors) == 0, errors

    def _get_api(self, config: dict[str, Any]):
        engine = config.get("engine", "cloudpss")
        auth = config.get("auth", {})
        return Engine.create_powerflow_for_skill(
            engine=engine,
            base_url=auth.get("base_url"),
            auth=auth,
        )

    def _get_handle(self, config: dict[str, Any], api=None):
        model_rid = config.get("model", {}).get("rid", "")
        if api is None:
            api = self._get_api(config)
        return api.get_model_handle(model_rid)

    def _reset_state(self) -> None:
        self.logs = []
        self.artifacts = []

    def _failed_result(self, error: str, start_time: datetime) -> SkillResult:
        return SkillResult(
            skill_name=self.name,
            status=SkillStatus.FAILED,
            error=error,
            logs=self.logs,
            start_time=start_time,
            end_time=datetime.now(),
        )

    @abstractmethod
    def run(self, config: dict[str, Any]) -> SkillResult:
        """执行分析

        Args:
            config: 配置字典

        Returns:
            SkillResult 结果对象

        Raises:
            NotImplementedError: 子类必须实现此方法
        """
        raise NotImplementedError("子类必须实现 run() 方法")


# Backward compatibility alias
# TODO: Deprecated, use PowerAnalysisBase instead
AnalysisBase = PowerAnalysisBase


# =============================================================================
# Unified Model Power Analysis Base Class
# =============================================================================

from cloudpss_skills_v2.core.system_model import PowerSystemModel


class PowerAnalysis(ABC):
    """Base class for power system analyses using unified PowerSystemModel.

    This class provides a simplified interface for analyses that work directly
    with the unified PowerSystemModel data structure, rather than going through
    the PowerSkill API layer.

    Example:
        class MyAnalysis(PowerAnalysis):
            def run(self, model: PowerSystemModel, config: dict) -> dict:
                return {"bus_count": len(model.buses)}
    """

    @abstractmethod
    def run(self, model: PowerSystemModel, config: dict) -> dict:
        """Run analysis on unified model.

        Args:
            model: Unified PowerSystemModel containing buses, branches, generators, etc.
            config: Analysis configuration dictionary

        Returns:
            Analysis results as a dictionary

        Raises:
            NotImplementedError: Subclasses must implement this method
        """
        raise NotImplementedError("子类必须实现 run() 方法")

    def validate_model(self, model: PowerSystemModel) -> list[str]:
        """Validate model before analysis.

        Performs basic validation checks:
        - Model has at least one bus
        - Model has a slack bus for reference

        Args:
            model: PowerSystemModel to validate

        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []

        if not model.buses:
            errors.append("No buses in model")

        if model.get_slack_bus() is None:
            errors.append("No slack bus found")

        return errors
