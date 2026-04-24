
'''
Core module for cloudpss_skills_v2.

This module provides core abstractions following the output standard:
- SkillResult: Standard result container
- SkillOutputValidator: Result validation
'''
from cloudpss_skills_v2.core.skill_result import SkillStatus, SkillResult, Artifact, LogEntry
from cloudpss_skills_v2.core.token_manager import TokenManager
from cloudpss_skills_v2.core.validator import SkillOutputValidator, ValidationResult
__all__ = [
    'SkillStatus',
    'SkillResult',
    'Artifact',
    'LogEntry',
    'TokenManager',
    'SkillOutputValidator',
    'ValidationResult']
