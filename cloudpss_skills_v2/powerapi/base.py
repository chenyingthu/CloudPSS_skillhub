"""
powerAPI Layer - Engine Adapter Base Classes

This module provides the foundation for the AWT (Abstract Window Toolkit) layer,
following the Java powerAPI pattern for simulation engine adapters.

Architecture:
    powerAPI Layer (Heavyweight) -> Engine-specific implementations
    PowerSkill Layer (Lightweight) -> Engine-agnostic API facade

Example:
    class CloudPSSPowerFlowAdapter(EngineAdapter):
        def _do_connect(self) -> None:
            # CloudPSS-specific connection logic
            pass

    adapter = CloudPSSPowerFlowAdapter()
    adapter.connect()
    result = adapter.run_simulation(config)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class SimulationStatus(Enum):
    """Status of a simulation job."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


class SimulationType(Enum):
    """Types of simulations supported by the adapter."""

    POWER_FLOW = "power_flow"
    EMT = "emt"
    SHORT_CIRCUIT = "short_circuit"
    HARMONIC = "harmonic"
    DYNAMIC = "dynamic"
    MONTE_CARLO = "monte_carlo"
    CONTINGENCY = "contingency"


@dataclass
class ValidationError:
    """Represents a validation error."""

    field: str = ""
    message: str = ""
    code: str = ""


@dataclass
class ValidationResult:
    """
    Result of configuration validation.

    Attributes:
        valid: Whether the configuration is valid
        errors: List of validation errors
        warnings: List of warning messages
    """

    valid: bool = True
    errors: list[ValidationError] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def __post_init__(self):
        if self.errors:
            self.valid = False

    @classmethod
    def success(cls) -> ValidationResult:
        """Create a successful validation result."""
        return cls(valid=True)

    @classmethod
    def failure(cls, errors: list) -> ValidationResult:
        """Create a failed validation result."""
        parsed_errors = []
        for e in errors:
            if isinstance(e, tuple):
                parsed_errors.append(ValidationError(field=e[0], message=e[1]))
            else:
                parsed_errors.append(e)
        return cls(valid=False, errors=parsed_errors)


@dataclass
class SimulationResult:
    """
    Result of a simulation run.

    Attributes:
        job_id: Unique identifier for the simulation job
        status: Current status of the simulation
        data: Simulation result data (engine-specific format)
        metadata: Additional metadata about the simulation
        errors: List of error messages
        warnings: List of warning messages
        started_at: When the simulation started
        completed_at: When the simulation completed
    """

    job_id: str = ""
    status: Optional[SimulationStatus] = None
    data: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    @property
    def is_success(self) -> bool:
        """Check if simulation completed successfully."""
        return self.status == SimulationStatus.COMPLETED and not self.errors

    @property
    def duration_seconds(self) -> Optional[float]:
        """Calculate simulation duration in seconds."""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "job_id": self.job_id,
            "status": self.status.value if self.status else None,
            "data": self.data,
            "metadata": self.metadata,
            "errors": self.errors,
            "warnings": self.warnings,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat()
            if self.completed_at
            else None,
            "duration_seconds": self.duration_seconds,
        }


@dataclass
class EngineConfig:
    """Configuration for an engine adapter."""

    engine_name: str = ""
    endpoint: str = ""
    timeout: int = 300
    max_retries: int = 3
    retry_delay: float = 1.0
    api_key: str = ""
    extra: dict[str, Any] = field(default_factory=dict)


class EngineAdapter(ABC):
    """
    Abstract base class for simulation engine adapters.

    This follows the Java powerAPI pattern where adapters are heavyweight components
    that directly interface with specific simulation engines (CloudPSS, pandapower, PSSE, etc.).

    Subclasses must implement:
        - _do_connect: Engine-specific connection logic
        - _do_disconnect: Engine-specific disconnection logic
        - _do_load_model: Engine-specific model loading
        - _do_run_simulation: Engine-specific simulation execution
        - _do_get_result: Engine-specific result fetching
        - _do_validate_config: Engine-specific config validation

    Example:
        class MyEngineAdapter(EngineAdapter):
            def _do_connect(self) -> None:
                # Connect to MyEngine
                pass

            def _do_disconnect(self) -> None:
                # Disconnect from MyEngine
                pass

            # ... implement other abstract methods
    """

    def __init__(self, config: Optional[EngineConfig] = None):
        """
        Initialize the adapter.

        Args:
            config: Engine configuration. If None, uses default config.
        """
        if config is None:
            config = EngineConfig(engine_name=self.get_engine_name())
        self._config = config
        self._connected = False
        self._current_model_id = None
        self._logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    @property
    @abstractmethod
    def engine_name(self) -> str:
        """Return the engine name identifier."""
        ...

    @abstractmethod
    def _do_connect(self) -> None:
        """
        Engine-specific connection logic.

        Raise:
            ConnectionError: If connection fails
        """
        ...

    @abstractmethod
    def _do_disconnect(self) -> None:
        """Engine-specific disconnection logic."""
        ...

    @abstractmethod
    def _do_load_model(self, model_id: str) -> bool:
        """
        Engine-specific model loading.

        Args:
            model_id: The model identifier to load

        Returns:
            True if model loaded successfully

        Raise:
            ValueError: If model_id is invalid
            RuntimeError: If loading fails
        """
        ...

    @abstractmethod
    def _do_run_simulation(self, config: dict[str, Any]) -> SimulationResult:
        """
        Execute a simulation.

        Args:
            config: Simulation configuration dict

        Returns:
            SimulationResult with job_id and initial status

        Raise:
            RuntimeError: If simulation fails to start
        """
        ...

    @abstractmethod
    def _do_get_result(self, job_id: str) -> SimulationResult:
        """
        Fetch simulation results.

        Args:
            job_id: The job identifier

        Returns:
            SimulationResult with complete data if ready

        Raise:
            ValueError: If job_id is invalid
            RuntimeError: If fetch fails
        """
        ...

    @abstractmethod
    def _do_validate_config(self, config: dict[str, Any]) -> ValidationResult:
        """
        Validate simulation configuration.

        Args:
            config: Configuration to validate

        Returns:
            ValidationResult with any errors/warnings
        """
        ...

    def get_components(self, model_id: str) -> list:
        self._require_connected()
        return self._do_get_components(model_id)

    def get_components_by_type(self, model_id: str, comp_type: str) -> list:
        self._require_connected()
        return self._do_get_components_by_type(model_id, comp_type)

    def remove_component(self, model_id: str, component_key: str) -> bool:
        self._require_connected()
        return self._do_remove_component(model_id, component_key)

    def update_component_args(
        self, model_id: str, component_key: str, args: dict[str, Any]
    ) -> bool:
        self._require_connected()
        return self._do_update_component_args(model_id, component_key, args)

    def clone_model(self, model_id: str) -> str:
        self._require_connected()
        return self._do_clone_model(model_id)

    def _do_get_components(self, model_id: str) -> list:
        raise NotImplementedError(f"{self.engine_name} does not support get_components")

    def _do_get_components_by_type(self, model_id: str, comp_type: str) -> list:
        all_comps = self._do_get_components(model_id)
        return [c for c in all_comps if getattr(c, "component_type", None) == comp_type]

    def _do_remove_component(self, model_id: str, component_key: str) -> bool:
        raise NotImplementedError(
            f"{self.engine_name} does not support remove_component"
        )

    def _do_update_component_args(
        self, model_id: str, component_key: str, args: dict[str, Any]
    ) -> bool:
        raise NotImplementedError(
            f"{self.engine_name} does not support update_component_args"
        )

    def _do_clone_model(self, model_id: str) -> str:
        raise NotImplementedError(f"{self.engine_name} does not support clone_model")

    def connect(self) -> None:
        """
        Establish connection to the engine.

        Raises:
            ConnectionError: If connection fails
        """
        if self._connected:
            self._logger.warning("Already connected to %s", self.engine_name)
            return
        self._logger.info("Connecting to engine: %s", self.engine_name)
        self._do_connect()
        self._connected = True
        self._logger.info("Successfully connected to %s", self.engine_name)

    def disconnect(self) -> None:
        """Close connection to the engine."""
        if not self._connected:
            return
        self._logger.info("Disconnecting from engine: %s", self.engine_name)
        self._do_disconnect()
        self._connected = False
        self._current_model_id = None
        self._logger.info("Disconnected from %s", self.engine_name)

    def load_model(self, model_id: str) -> bool:
        """
        Load a model into the engine.

        Args:
            model_id: The model identifier to load

        Returns:
            True if model loaded successfully

        Raises:
            RuntimeError: If not connected or loading fails
        """
        self._require_connected()
        self._logger.info("Loading model: %s", model_id)
        result = self._do_load_model(model_id)
        if result:
            self._current_model_id = model_id
            self._logger.info("Model loaded successfully: %s", model_id)
        return result

    def run_simulation(self, config: dict[str, Any]) -> SimulationResult:
        """
        Execute a simulation.

        Args:
            config: Simulation configuration

        Returns:
            SimulationResult with job_id and initial status

        Raises:
            RuntimeError: If not connected or simulation fails
        """
        self._require_connected()
        validation = self.validate_config(config)
        if not validation.valid:
            error_msg = "; ".join(f"{e.field}: {e.message}" for e in validation.errors)
            return SimulationResult(
                job_id="",
                status=SimulationStatus.FAILED,
                errors=[f"Configuration validation failed: {error_msg}"],
            )
        if validation.warnings:
            self._logger.warning("Config validation warnings: %s", validation.warnings)
        self._logger.info("Starting simulation with config: %s", config)
        result = self._do_run_simulation(config)
        if result.status in (SimulationStatus.PENDING, SimulationStatus.RUNNING):
            self._logger.info("Simulation started, job_id: %s", result.job_id)
        return result

    def get_result(self, job_id: str) -> SimulationResult:
        """
        Fetch simulation results.

        Args:
            job_id: The job identifier

        Returns:
            SimulationResult with complete data if ready

        Raises:
            RuntimeError: If not connected or fetch fails
        """
        self._require_connected()
        return self._do_get_result(job_id)

    def validate_config(self, config: dict[str, Any]) -> ValidationResult:
        """
        Validate simulation configuration.

        Args:
            config: Configuration to validate

        Returns:
            ValidationResult with any errors/warnings
        """
        return self._do_validate_config(config)

    def is_connected(self) -> bool:
        """Check if adapter is connected to the engine."""
        return self._connected

    def get_engine_name(self) -> str:
        """Get the engine name."""
        return self.engine_name

    def get_current_model_id(self) -> Optional[str]:
        """Get the currently loaded model ID, if any."""
        return self._current_model_id

    def get_supported_simulations(self) -> list[SimulationType]:
        """
        Get list of simulation types supported by this engine.

        Override in subclass to specify supported types.
        """
        return []

    def _require_connected(self) -> None:
        """Raise if not connected."""
        if not self._connected:
            raise RuntimeError(
                f"Not connected to {self.engine_name}. Call connect() first."
            )

    def __enter__(self) -> EngineAdapter:
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.disconnect()

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(engine={self.engine_name}, connected={self._connected}, model={self._current_model_id})"
        )


class AsyncEngineAdapter(EngineAdapter):
    """
    Asynchronous version of EngineAdapter for non-blocking operations.

    Use this when the underlying engine supports async operations.
    """

    @abstractmethod
    async def _do_connect_async(self) -> None:
        """Async engine-specific connection logic."""
        ...

    @abstractmethod
    async def _do_disconnect_async(self) -> None:
        """Async engine-specific disconnection logic."""
        ...

    @abstractmethod
    async def _do_load_model_async(self, model_id: str) -> bool:
        """Async model loading."""
        ...

    @abstractmethod
    async def _do_run_simulation_async(
        self, config: dict[str, Any]
    ) -> SimulationResult:
        """Async simulation execution."""
        ...

    @abstractmethod
    async def _do_get_result_async(self, job_id: str) -> SimulationResult:
        """Async result fetching."""
        ...

    async def connect_async(self) -> None:
        """Async connection."""
        await self._do_connect_async()
        self._connected = True

    async def disconnect_async(self) -> None:
        """Async disconnection."""
        await self._do_disconnect_async()
        self._connected = False

    async def load_model_async(self, model_id: str) -> bool:
        """Async model loading."""
        self._require_connected()
        result = await self._do_load_model_async(model_id)
        if result:
            self._current_model_id = model_id
        return result

    async def run_simulation_async(self, config: dict[str, Any]) -> SimulationResult:
        """Async simulation execution."""
        self._require_connected()
        validation = self.validate_config(config)
        if not validation.valid:
            error_msg = "; ".join(f"{e.field}: {e.message}" for e in validation.errors)
            return SimulationResult(
                job_id="",
                status=SimulationStatus.FAILED,
                errors=[f"Configuration validation failed: {error_msg}"],
            )
        return await self._do_run_simulation_async(config)

    async def get_result_async(self, job_id: str) -> SimulationResult:
        """Async result fetching."""
        self._require_connected()
        return await self._do_get_result_async(job_id)


__all__ = [
    "SimulationStatus",
    "SimulationType",
    "ValidationError",
    "ValidationResult",
    "SimulationResult",
    "EngineConfig",
    "EngineAdapter",
    "AsyncEngineAdapter",
]
