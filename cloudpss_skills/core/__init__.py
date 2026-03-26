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
    # CLI
    "main",
]
