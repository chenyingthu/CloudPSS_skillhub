"""
CloudPSS Skill System - Core Module

核心模块导出。
"""

from .base import (
    SkillBase,
    SkillResult,
    SkillStatus,
    Artifact,
    LogEntry,
    ValidationResult,
)

from .registry import (
    register,
    get_skill,
    list_skills,
    has_skill,
    auto_discover,
)

from .config import (
    ConfigLoader,
    ConfigValidator,
    ConfigGenerator,
    InteractiveConfigBuilder,
)

from . import utils

from .auth_utils import (
    setup_auth,
    get_token_from_config,
    DEFAULT_TOKEN_FILE,
    DEFAULT_TIMEOUT,
    DEFAULT_POWERFLOW_TOLERANCE,
    DEFAULT_VOLTAGE_MIN,
    DEFAULT_VOLTAGE_MAX,
)

from .cli import main

__all__ = [
    # Base classes
    "SkillBase",
    "SkillResult",
    "SkillStatus",
    "Artifact",
    "LogEntry",
    "ValidationResult",
    # Registry
    "register",
    "get_skill",
    "list_skills",
    "has_skill",
    "auto_discover",
    # Config
    "ConfigLoader",
    "ConfigValidator",
    "ConfigGenerator",
    "InteractiveConfigBuilder",
    # Utils
    "utils",
    # Auth
    "setup_auth",
    "get_token_from_config",
    "DEFAULT_TOKEN_FILE",
    "DEFAULT_TIMEOUT",
    "DEFAULT_POWERFLOW_TOLERANCE",
    "DEFAULT_VOLTAGE_MIN",
    "DEFAULT_VOLTAGE_MAX",
    # CLI
    "main",
]
