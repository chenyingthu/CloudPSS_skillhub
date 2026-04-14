"""
CloudPSS SkillHub

CloudPSS 电力系统仿真技能中心 - 48 个专业仿真技能
"""

__version__ = "1.0.0"
__author__ = "CloudPSS SkillHub"

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
