"""Configuration Store - Hierarchical configuration management.

Supports three-level inheritance: base → project → study
Enables configuration reuse and environment-specific overrides.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

import yaml


# =============================================================================
# Configuration Classes
# =============================================================================

@dataclass
class BaseConfig:
    """Base configuration - global defaults.

    This is the foundation layer that defines system-wide defaults.
    All projects inherit from a base config.
    """

    name: str = "default_base"
    description: str = "Default base configuration"

    # Engine defaults
    default_engine: str = "cloudpss"
    engine_profiles: dict[str, dict] = field(default_factory=dict)

    # Default simulation parameters
    default_tolerance: float = 1e-6
    default_max_iterations: int = 100
    default_timeout_seconds: int = 300

    # Default output settings
    default_output_format: str = "hdf5"
    default_output_path: str = "./results"

    # Analysis defaults
    default_voltage_limits: tuple[float, float] = (0.9, 1.1)
    default_thermal_limit: float = 1.0

    # Environment settings
    log_level: str = "INFO"
    save_intermediate_results: bool = False
    parallel_jobs: int = 1

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "BaseConfig":
        return cls(**data)


@dataclass
class ProjectConfig:
    """Project configuration - project-specific settings.

    Inherits from BaseConfig and can override any base settings.
    Defines common settings for all studies within a project.
    """

    name: str = "default_project"
    description: str = "Default project configuration"

    # Inheritance reference
    inherits_from: str = "default_base"

    # Project-specific settings
    project_id: str = ""
    project_path: str = "./"

    # Engine selection for this project
    engine: str | None = None  # None = use base default

    # Common models used in this project
    model_library: dict[str, str] = field(default_factory=dict)

    # Project-specific simulation overrides
    tolerance: float | None = None
    max_iterations: int | None = None

    # Project-specific analysis settings
    voltage_limits: tuple[float, float] | None = None
    thermal_limit: float | None = None

    # Output organization
    output_organization: str = "flat"  # "flat", "by_date", "by_study"
    output_naming_pattern: str = "{study_name}_{timestamp}"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "ProjectConfig":
        return cls(**data)


@dataclass
class StudyConfig:
    """Study configuration - specific analysis definition.

    Inherits from ProjectConfig (which inherits from BaseConfig).
    This is the most specific configuration layer.
    """

    name: str = "default_study"
    description: str = "Default study configuration"

    # Inheritance reference
    inherits_from: str = "default_project"

    # Study identification
    study_id: str = ""
    study_type: str = "power_flow"  # "power_flow", "n1_security", etc.

    # Model specification
    model_id: str = ""
    model_source: str = "cloud"  # "cloud", "local", "project_library"

    # Engine override
    engine: str | None = None  # None = inherit from project

    # Simulation parameters (override inherited values)
    tolerance: float | None = None
    max_iterations: int | None = None
    timeout_seconds: int | None = None

    # Study-specific parameters
    parameters: dict[str, Any] = field(default_factory=dict)

    # Analysis configuration
    analysis_type: str = ""
    analysis_config: dict[str, Any] = field(default_factory=dict)

    # Output configuration
    output_path: str | None = None
    output_format: str | None = None

    # Tags for organization and retrieval
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "StudyConfig":
        return cls(**data)


@dataclass
class EffectiveConfig:
    """Effective configuration after inheritance resolution.

    This is the result of merging base → project → study.
    Contains all final values ready for execution.
    """

    # Identification
    name: str
    study_type: str
    study_id: str

    # Engine
    engine: str
    engine_config: dict[str, Any]

    # Model
    model_id: str
    model_source: str

    # Simulation parameters (resolved values)
    tolerance: float
    max_iterations: int
    timeout_seconds: int

    # Analysis
    analysis_type: str
    analysis_config: dict[str, Any]
    parameters: dict[str, Any]

    # Output
    output_path: str
    output_format: str

    # Environment
    log_level: str
    parallel_jobs: int
    save_intermediate_results: bool

    # Source tracking
    source_config_ids: dict[str, str] = field(default_factory=dict)

    def to_simulation_config(self) -> dict[str, Any]:
        """Convert to simulation configuration format."""
        return {
            "study_type": self.study_type,
            "analysis_type": self.analysis_type,
            "model_id": self.model_id,
            "model_source": self.model_source,
            "engine": self.engine,
            "engine_config": self.engine_config,
            "tolerance": self.tolerance,
            "max_iterations": self.max_iterations,
            "timeout_seconds": self.timeout_seconds,
            "parameters": self.parameters,
            "analysis_config": self.analysis_config,
            "output": {
                "path": self.output_path,
                "format": self.output_format,
            },
            "log_level": self.log_level,
            "parallel_jobs": self.parallel_jobs,
        }


# =============================================================================
# Configuration Store
# =============================================================================

class ConfigStore:
    """Hierarchical configuration store.

    Manages three-level configuration inheritance:
    Base (global defaults) → Project (project-specific) → Study (analysis-specific)

    Storage structure:
        config_store/
        ├── base/
        │   ├── default_base.yaml
        │   └── high_precision.yaml
        ├── projects/
        │   ├── my_project/
        │   │   ├── config.yaml
        │   │   └── studies/
        │   │       ├── n1_analysis.yaml
        │   │       └── voltage_stability.yaml
        │   └── another_project/
        └── environments/
            ├── development.yaml
            ├── testing.yaml
            └── production.yaml
    """

    def __init__(self, storage_path: str | Path = "./config_store"):
        self.storage_path = Path(storage_path)
        self._ensure_directories()

        # Cache
        self._base_cache: dict[str, BaseConfig] = {}
        self._project_cache: dict[str, ProjectConfig] = {}
        self._study_cache: dict[str, StudyConfig] = {}

    def _ensure_directories(self) -> None:
        """Create storage directory structure."""
        (self.storage_path / "base").mkdir(parents=True, exist_ok=True)
        (self.storage_path / "environments").mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------------------------------
    # Base Configuration
    # -------------------------------------------------------------------------

    def save_base_config(self, config: BaseConfig) -> str:
        """Save a base configuration."""
        config_id = config.name
        file_path = self.storage_path / "base" / f"{config_id}.yaml"

        with open(file_path, "w", encoding="utf-8") as f:
            yaml.dump(config.to_dict(), f, default_flow_style=False, allow_unicode=True)

        # Update cache
        self._base_cache[config_id] = config

        return config_id

    def load_base_config(self, config_id: str) -> BaseConfig:
        """Load a base configuration."""
        if config_id in self._base_cache:
            return self._base_cache[config_id]

        file_path = self.storage_path / "base" / f"{config_id}.yaml"

        if not file_path.exists():
            # Return default if not found
            if config_id == "default_base":
                return BaseConfig()
            raise FileNotFoundError(f"Base config '{config_id}' not found")

        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        config = BaseConfig.from_dict(data)
        self._base_cache[config_id] = config
        return config

    def list_base_configs(self) -> list[str]:
        """List available base configurations."""
        base_dir = self.storage_path / "base"
        if not base_dir.exists():
            return []
        return [f.stem for f in base_dir.glob("*.yaml")]

    # -------------------------------------------------------------------------
    # Project Configuration
    # -------------------------------------------------------------------------

    def save_project_config(self, config: ProjectConfig) -> str:
        """Save a project configuration."""
        config_id = config.name
        project_dir = self.storage_path / "projects" / config_id
        project_dir.mkdir(parents=True, exist_ok=True)

        file_path = project_dir / "config.yaml"
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.dump(config.to_dict(), f, default_flow_style=False, allow_unicode=True)

        # Create studies directory
        (project_dir / "studies").mkdir(exist_ok=True)

        # Update cache
        self._project_cache[config_id] = config

        return config_id

    def load_project_config(self, config_id: str) -> ProjectConfig:
        """Load a project configuration."""
        if config_id in self._project_cache:
            return self._project_cache[config_id]

        file_path = self.storage_path / "projects" / config_id / "config.yaml"

        if not file_path.exists():
            raise FileNotFoundError(f"Project config '{config_id}' not found")

        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        config = ProjectConfig.from_dict(data)
        self._project_cache[config_id] = config
        return config

    def list_projects(self) -> list[str]:
        """List available projects."""
        projects_dir = self.storage_path / "projects"
        if not projects_dir.exists():
            return []
        return [d.name for d in projects_dir.iterdir() if d.is_dir()]

    # -------------------------------------------------------------------------
    # Study Configuration
    # -------------------------------------------------------------------------

    def save_study_config(self, project_id: str, config: StudyConfig) -> str:
        """Save a study configuration within a project."""
        study_id = f"{project_id}/{config.name}"
        study_dir = self.storage_path / "projects" / project_id / "studies"
        study_dir.mkdir(parents=True, exist_ok=True)

        file_path = study_dir / f"{config.name}.yaml"
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.dump(config.to_dict(), f, default_flow_style=False, allow_unicode=True)

        # Update cache
        self._study_cache[study_id] = config

        return study_id

    def load_study_config(self, project_id: str, study_name: str) -> StudyConfig:
        """Load a study configuration."""
        study_id = f"{project_id}/{study_name}"

        if study_id in self._study_cache:
            return self._study_cache[study_id]

        file_path = (
            self.storage_path / "projects" / project_id / "studies" / f"{study_name}.yaml"
        )

        if not file_path.exists():
            raise FileNotFoundError(f"Study config '{study_id}' not found")

        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        config = StudyConfig.from_dict(data)
        self._study_cache[study_id] = config
        return config

    def list_studies(self, project_id: str) -> list[str]:
        """List studies in a project."""
        studies_dir = self.storage_path / "projects" / project_id / "studies"
        if not studies_dir.exists():
            return []
        return [f.stem for f in studies_dir.glob("*.yaml")]

    # -------------------------------------------------------------------------
    # Inheritance Resolution
    # -------------------------------------------------------------------------

    def get_effective_config(
        self,
        study_id: str,
        project_id: str | None = None,
        environment: str | None = None,
        runtime_overrides: dict[str, Any] | None = None,
    ) -> EffectiveConfig:
        """Resolve effective configuration with full inheritance.

        Resolution order (later overrides earlier):
        1. Default values
        2. Base config
        3. Project config
        4. Study config
        5. Environment overrides
        6. Runtime overrides
        """
        # Parse study_id if it contains project
        if "/" in study_id and project_id is None:
            project_id, study_name = study_id.split("/", 1)
        else:
            study_name = study_id

        if project_id is None:
            raise ValueError("project_id must be provided")

        # Load configurations
        study_config = self.load_study_config(project_id, study_name)
        project_config = self.load_project_config(project_id)
        base_config = self.load_base_config(project_config.inherits_from)

        # Environment overrides
        env_overrides = {}
        if environment:
            env_overrides = self._load_environment_overrides(environment)

        # Runtime overrides
        runtime_overrides = runtime_overrides or {}

        # Merge configurations (later values override earlier)
        # Engine
        engine = self._resolve_value(
            runtime_overrides.get("engine"),
            env_overrides.get("engine"),
            study_config.engine,
            project_config.engine,
            base_config.default_engine,
        )

        engine_config = self._resolve_engine_config(
            engine, base_config, runtime_overrides, env_overrides
        )

        # Simulation parameters
        tolerance = self._resolve_value(
            runtime_overrides.get("tolerance"),
            study_config.tolerance,
            project_config.tolerance,
            base_config.default_tolerance,
        )

        max_iterations = self._resolve_value(
            runtime_overrides.get("max_iterations"),
            study_config.max_iterations,
            project_config.max_iterations,
            base_config.default_max_iterations,
        )

        timeout_seconds = self._resolve_value(
            runtime_overrides.get("timeout_seconds"),
            study_config.timeout_seconds,
            base_config.default_timeout_seconds,
        )

        # Output settings
        output_format = self._resolve_value(
            runtime_overrides.get("output_format"),
            study_config.output_format,
            base_config.default_output_format,
        )

        output_path = self._resolve_value(
            runtime_overrides.get("output_path"),
            study_config.output_path,
            project_config.project_path,
            base_config.default_output_path,
        )

        # Create effective config
        return EffectiveConfig(
            name=study_config.name,
            study_type=study_config.study_type,
            study_id=study_config.study_id or f"{project_id}/{study_name}",
            engine=engine,
            engine_config=engine_config,
            model_id=study_config.model_id,
            model_source=study_config.model_source,
            tolerance=tolerance,
            max_iterations=max_iterations,
            timeout_seconds=timeout_seconds,
            analysis_type=study_config.analysis_type or study_config.study_type,
            analysis_config=study_config.analysis_config,
            parameters=study_config.parameters,
            output_path=output_path,
            output_format=output_format,
            log_level=env_overrides.get("log_level", base_config.log_level),
            parallel_jobs=runtime_overrides.get(
                "parallel_jobs", base_config.parallel_jobs
            ),
            save_intermediate_results=runtime_overrides.get(
                "save_intermediate_results", base_config.save_intermediate_results
            ),
            source_config_ids={
                "base": project_config.inherits_from,
                "project": project_id,
                "study": study_name,
                "environment": environment,
            },
        )

    def _resolve_value(self, *values: Any) -> Any:
        """Resolve a value from multiple sources.

        Returns the first non-None value.
        """
        for value in values:
            if value is not None:
                return value
        return None

    def _resolve_engine_config(
        self,
        engine: str,
        base_config: BaseConfig,
        runtime_overrides: dict,
        env_overrides: dict,
    ) -> dict[str, Any]:
        """Resolve engine-specific configuration."""
        # Start with base engine profile
        config = base_config.engine_profiles.get(engine, {}).copy()

        # Apply environment overrides
        if "engine_config" in env_overrides:
            config.update(env_overrides["engine_config"])

        # Apply runtime overrides
        if "engine_config" in runtime_overrides:
            config.update(runtime_overrides["engine_config"])

        return config

    def _load_environment_overrides(self, environment: str) -> dict[str, Any]:
        """Load environment-specific overrides."""
        file_path = self.storage_path / "environments" / f"{environment}.yaml"

        if not file_path.exists():
            return {}

        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    # -------------------------------------------------------------------------
    # Environment Management
    # -------------------------------------------------------------------------

    def save_environment_config(self, name: str, config: dict[str, Any]) -> None:
        """Save environment-specific configuration."""
        file_path = self.storage_path / "environments" / f"{name}.yaml"
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as f:
            yaml.dump(config, f, default_flow_style=False)

    def list_environments(self) -> list[str]:
        """List available environments."""
        env_dir = self.storage_path / "environments"
        if not env_dir.exists():
            return []
        return [f.stem for f in env_dir.glob("*.yaml")]


# =============================================================================
# Convenience Functions
# =============================================================================


def create_default_configs(store: ConfigStore) -> None:
    """Create default configuration templates."""

    # Base configuration
    base = BaseConfig(
        name="default_base",
        description="Default base configuration for power system analysis",
        default_engine="cloudpss",
        engine_profiles={
            "cloudpss": {
                "base_url": "https://www.cloudpss.net/",
                "timeout": 300,
            },
            "pandapower": {
                "numba": True,
                "tolerance": 1e-6,
            },
        },
        default_tolerance=1e-6,
        default_max_iterations=100,
        default_output_format="hdf5",
        default_output_path="./results",
        parallel_jobs=1,
    )
    store.save_base_config(base)

    # High precision base
    high_precision = BaseConfig(
        name="high_precision",
        description="High precision configuration for detailed analysis",
        inherits_from="default_base",
        default_tolerance=1e-10,
        default_max_iterations=200,
    )
    store.save_base_config(high_precision)

    # Example project
    project = ProjectConfig(
        name="example_project",
        description="Example project demonstrating configuration inheritance",
        inherits_from="default_base",
        project_id="example_001",
        model_library={
            "IEEE39": "model/holdme/IEEE39",
            "IEEE118": "model/holdme/IEEE118",
        },
        output_organization="by_date",
    )
    store.save_project_config(project)

    # Example studies
    study1 = StudyConfig(
        name="base_case_power_flow",
        description="Base case power flow analysis",
        inherits_from="example_project",
        study_type="power_flow",
        model_id="model/holdme/IEEE39",
        analysis_type="power_flow",
        tags=["base_case", "IEEE39"],
    )
    store.save_study_config("example_project", study1)

    study2 = StudyConfig(
        name="n1_security_analysis",
        description="N-1 security analysis",
        inherits_from="example_project",
        study_type="n1_security",
        model_id="model/holdme/IEEE39",
        analysis_type="n1_security",
        analysis_config={
            "check_voltage": True,
            "check_thermal": True,
            "voltage_threshold": 0.05,
            "thermal_threshold": 1.0,
        },
        tags=["n1", "security", "IEEE39"],
    )
    store.save_study_config("example_project", study2)

    # Environment configurations
    store.save_environment_config(
        "development",
        {
            "log_level": "DEBUG",
            "save_intermediate_results": True,
            "engine_config": {"cloudpss": {"base_url": "http://localhost:50001"}},
        },
    )

    store.save_environment_config(
        "production",
        {
            "log_level": "WARNING",
            "save_intermediate_results": False,
            "parallel_jobs": 4,
        },
    )


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "BaseConfig",
    "ProjectConfig",
    "StudyConfig",
    "EffectiveConfig",
    "ConfigStore",
    "create_default_configs",
]
