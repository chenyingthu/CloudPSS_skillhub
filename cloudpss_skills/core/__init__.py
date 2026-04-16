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

from . import job_runner
from .job_runner import (
    JobStatus,
    JobResult,
    BatchJobResult,
    PollConfig,
    run_powerflow_and_wait,
    run_emt_and_wait,
    batch_simulation,
    wait_for_job,
    check_job_status,
    get_default_poll_config,
)

from . import exporter
from .exporter import (
    OutputFormat,
    OutputConfig,
    ExportResult,
    BatchExportResult,
    save_json,
    save_csv,
    generate_report,
    export_multiple,
    build_artifact,
    table_to_csv,
)

from . import model_utils
from .model_utils import (
    clone_model,
    reload_model,
    get_or_clone_model,
    get_all_components,
    get_components_by_definition,
    get_components_by_type,
    get_buses,
    get_lines,
    get_generators,
    find_component_by_label,
    matches_label,
    remove_component_safe,
    update_component_args,
    get_component_args,
    get_revision_components,
    iterate_components,
    count_components_by_definition,
)

from .cli import main

from .output_validator import (
    SkillOutputValidator,
    validate_skill_output,
)

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
    # Job Runner
    "job_runner",
    "JobStatus",
    "JobResult",
    "BatchJobResult",
    "PollConfig",
    "run_powerflow_and_wait",
    "run_emt_and_wait",
    "batch_simulation",
    "wait_for_job",
    "check_job_status",
    "get_default_poll_config",
    # Exporter
    "exporter",
    "OutputFormat",
    "OutputConfig",
    "ExportResult",
    "BatchExportResult",
    "save_json",
    "save_csv",
    "generate_report",
    "export_multiple",
    "build_artifact",
    "table_to_csv",
    # Model Utils
    "model_utils",
    "clone_model",
    "reload_model",
    "get_or_clone_model",
    "get_all_components",
    "get_components_by_definition",
    "get_components_by_type",
    "get_buses",
    "get_lines",
    "get_generators",
    "find_component_by_label",
    "matches_label",
    "remove_component_safe",
    "update_component_args",
    "get_component_args",
    "get_revision_components",
    "iterate_components",
    "count_components_by_definition",
    # CLI
    "main",
    # Output Validator
    "SkillOutputValidator",
    "validate_skill_output",
]
