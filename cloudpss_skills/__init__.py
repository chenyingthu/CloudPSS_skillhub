"""
CloudPSS Skill System

技能系统模块导出。
"""

__version__ = "1.0.0"
__author__ = "CloudPSS"

from cloudpss_skills.core import (
    SkillBase,
    SkillResult,
    register,
    get_skill,
    list_skills,
)

__all__ = [
    "__version__",
    "__author__",
    "SkillBase",
    "SkillResult",
    "register",
    "get_skill",
    "list_skills",
]
