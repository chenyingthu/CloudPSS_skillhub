
'''
Core module for cloudpss_skills_v2.

This module provides core abstractions following the output standard:
- SkillResult: Standard result container
- SkillOutputValidator: Result validation
- SystemModel: Unified power system data model
- EngineCapabilities: Engine capability declaration
- ConfigStore: Hierarchical configuration management
- ResultArchive: HDF5-based result storage
'''
from cloudpss_skills_v2.core.skill_result import SkillStatus, SkillResult, Artifact, LogEntry
from cloudpss_skills_v2.core.token_manager import TokenManager
from cloudpss_skills_v2.core.validator import SkillOutputValidator, ValidationResult

# New architecture components
from cloudpss_skills_v2.core.system_model import (
    Bus,
    Branch,
    Generator,
    Load,
    Transformer,
    PowerSystemModel,
    ValidationResult as ModelValidationResult,
)
from cloudpss_skills_v2.core.engine_capabilities import (
    SimulationType,
    ParameterSpec,
    SimulationConfig,
    EngineCapabilities,
    EngineRegistry,
    ValidationResult as EngineValidationResult,
    SimulationResult,
)
from cloudpss_skills_v2.core.config_store import (
    BaseConfig,
    ProjectConfig,
    StudyConfig,
    EffectiveConfig,
    ConfigStore,
)
from cloudpss_skills_v2.core.result_archive import (
    ArchiveMetadata,
    ArchiveRecord,
    ComparisonResult,
    ResultArchive,
)

__all__ = [
    # Original exports
    'SkillStatus',
    'SkillResult',
    'Artifact',
    'LogEntry',
    'TokenManager',
    'SkillOutputValidator',
    'ValidationResult',
    # System model
    'Bus',
    'Branch',
    'Generator',
    'Load',
    'Transformer',
    'PowerSystemModel',
    'ModelValidationResult',
    # Engine capabilities
    'SimulationType',
    'ParameterSpec',
    'SimulationConfig',
    'EngineCapabilities',
    'EngineRegistry',
    'EngineValidationResult',
    'SimulationResult',
    # Config store
    'BaseConfig',
    'ProjectConfig',
    'StudyConfig',
    'EffectiveConfig',
    'ConfigStore',
    # Result archive
    'ArchiveMetadata',
    'ArchiveRecord',
    'ComparisonResult',
    'ResultArchive',
]
