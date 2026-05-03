"""Engine Capabilities - Unified engine capability declaration.

This module provides the mechanism for engines to declare their capabilities,
enabling dynamic discovery and configuration of simulation engines.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Protocol


# =============================================================================
# Simulation Types (Engine Capability Granularity)
# =============================================================================

class SimulationType(Enum):
    """Simulation types that engines may support.

    This is the primary capability identifier - each engine declares
    which simulation types it supports.
    """
    # Power flow
    POWER_FLOW_AC = "power_flow_ac"
    POWER_FLOW_DC = "power_flow_dc"
    OPTIMAL_POWER_FLOW = "optimal_power_flow"
    CONTINUATION_POWER_FLOW = "continuation_power_flow"

    # Short circuit
    SHORT_CIRCUIT_3PH = "short_circuit_3ph"
    SHORT_CIRCUIT_1PH = "short_circuit_1ph"
    SHORT_CIRCUIT_2PH = "short_circuit_2ph"

    # Transient analysis
    EMT_TRANSIENT = "emt_transient"
    TRANSIENT_STABILITY = "transient_stability"
    SMALL_SIGNAL = "small_signal"

    # Other
    HARMONIC_ANALYSIS = "harmonic_analysis"
    MONTE_CARLO = "monte_carlo"
    CONTINGENCY_ANALYSIS = "contingency_analysis"


# =============================================================================
# Parameter Specifications
# =============================================================================

@dataclass(frozen=True)
class ParameterSpec:
    """Specification for a configuration parameter.

    Engines declare which parameters they accept for each simulation type,
    enabling automatic UI generation and validation.

    Attributes:
        name: Parameter name
        param_type: Data type - "float", "int", "string", "enum", "bool"
        description: Human-readable description
        default: Default value
        required: Whether parameter is required
        choices: For enum type, valid choices
        min_value: Minimum value (for numeric types)
        max_value: Maximum value (for numeric types)
        units: Physical units (e.g., "MW", "seconds", "p.u.")
    """

    name: str
    param_type: str  # "float", "int", "string", "enum", "bool", "list"
    description: str = ""
    default: Any = None
    required: bool = False
    choices: list[Any] = field(default_factory=list)
    min_value: float | None = None
    max_value: float | None = None
    units: str = ""

    def __post_init__(self) -> None:
        """Validate parameter specification."""
        valid_types = ("float", "int", "string", "enum", "bool", "list")
        if self.param_type not in valid_types:
            raise ValueError(f"Invalid param_type '{self.param_type}'")

        if self.param_type == "enum" and not self.choices:
            raise ValueError(f"Enum parameter {self.name} must have choices")


# =============================================================================
# Simulation Configuration
# =============================================================================

@dataclass
class SimulationConfig:
    """Standard simulation configuration.

    This is the unified configuration format that all engines accept.
    Engines validate against their ParameterSpecs and map to their native format.
    """

    simulation_type: SimulationType
    model_id: str  # Unified model identifier

    # Engine selection
    engine_type: str = "auto"  # "auto" or specific engine name

    # Core parameters (common across most simulation types)
    tolerance: float = 1e-6
    max_iterations: int = 100
    timeout_seconds: int = 300

    # Engine-specific parameters (validated by engine)
    engine_params: dict[str, Any] = field(default_factory=dict)

    # Additional options
    options: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate basic configuration."""
        if self.tolerance <= 0:
            raise ValueError(f"Tolerance {self.tolerance} must be positive")
        if self.max_iterations <= 0:
            raise ValueError(f"Max iterations {self.max_iterations} must be positive")


# =============================================================================
# Engine Capabilities Declaration
# =============================================================================

@dataclass
class EngineCapabilities:
    """Complete capability declaration for a simulation engine.

    Engines provide this declaration to register themselves with the system.
    It enables:
    - Dynamic discovery of available engines
    - Automatic UI generation for engine selection
    - Configuration validation before execution
    - Capability-based routing of simulation requests

    Attributes:
        engine_name: Unique engine identifier
        engine_version: Version string
        vendor: Engine vendor/organization
        description: Human-readable description

        supported_simulations: Which simulation types are supported
        supported_model_formats: Which model formats can be loaded

        # Scalability
        max_buses: Maximum recommended system size (None = unlimited)
        max_branches: Maximum recommended branches (None = unlimited)
        supports_parallel: Whether parallel execution is supported

        # Features
        supports_reactive_power: Whether reactive power is modeled
        supports_tap_changers: Whether transformer taps are supported
        supports_phase_shifters: Whether phase shifters are supported
        supports_hvdc: Whether HVDC is supported

        # Parameters by simulation type
        simulation_parameters: Parameter specifications for each simulation type
    """

    # Identification
    engine_name: str
    engine_version: str
    vendor: str = ""
    description: str = ""

    # Capabilities
    supported_simulations: list[SimulationType] = field(default_factory=list)
    supported_model_formats: list[str] = field(default_factory=list)

    # Scalability
    max_buses: int | None = None
    max_branches: int | None = None
    supports_parallel: bool = False

    # Features
    supports_reactive_power: bool = True
    supports_tap_changers: bool = True
    supports_phase_shifters: bool = False
    supports_hvdc: bool = False
    supports_distributed_slack: bool = False

    # Detailed parameter specifications
    simulation_parameters: dict[SimulationType, list[ParameterSpec]] = field(
        default_factory=dict
    )

    def supports(self, sim_type: SimulationType) -> bool:
        """Check if engine supports a simulation type."""
        return sim_type in self.supported_simulations

    def get_parameters(self, sim_type: SimulationType) -> list[ParameterSpec]:
        """Get parameter specifications for a simulation type."""
        return self.simulation_parameters.get(sim_type, [])

    def validate_config(self, config: SimulationConfig) -> ValidationResult:
        """Validate a simulation configuration against capabilities."""
        errors = []
        warnings = []

        # Check simulation type support
        if config.simulation_type not in self.supported_simulations:
            errors.append(
                f"Engine {self.engine_name} does not support "
                f"{config.simulation_type.value}"
            )
            return ValidationResult(valid=False, errors=errors, warnings=warnings)

        # Validate engine-specific parameters
        param_specs = {p.name: p for p in self.get_parameters(config.simulation_type)}

        for param_name, param_value in config.engine_params.items():
            if param_name not in param_specs:
                warnings.append(
                    f"Unknown parameter '{param_name}' for {self.engine_name}"
                )
                continue

            spec = param_specs[param_name]

            # Type validation
            if spec.param_type == "float" and not isinstance(param_value, (int, float)):
                errors.append(f"Parameter '{param_name}' must be numeric")
            elif spec.param_type == "int" and not isinstance(param_value, int):
                errors.append(f"Parameter '{param_name}' must be integer")
            elif spec.param_type == "bool" and not isinstance(param_value, bool):
                errors.append(f"Parameter '{param_name}' must be boolean")
            elif spec.param_type == "enum" and param_value not in spec.choices:
                errors.append(
                    f"Parameter '{param_name}' must be one of {spec.choices}"
                )

            # Range validation
            if spec.param_type in ("float", "int"):
                if spec.min_value is not None and param_value < spec.min_value:
                    errors.append(
                        f"Parameter '{param_name}' {param_value} below minimum "
                        f"{spec.min_value}"
                    )
                if spec.max_value is not None and param_value > spec.max_value:
                    errors.append(
                        f"Parameter '{param_name}' {param_value} above maximum "
                        f"{spec.max_value}"
                    )

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )


# =============================================================================
# Engine Interface Protocol
# =============================================================================

class EngineInterface(Protocol):
    """Protocol that all engine adapters must implement.

    This defines the contract between the framework and engines.
    """

    @property
    def capabilities(self) -> EngineCapabilities:
        """Return engine capability declaration."""
        ...

    def connect(self, config: dict[str, Any]) -> None:
        """Connect to the engine."""
        ...

    def disconnect(self) -> None:
        """Disconnect from the engine."""
        ...

    def load_model(self, model_id: str, format_hint: str | None = None) -> bool:
        """Load a model into the engine."""
        ...

    def run_simulation(self, config: SimulationConfig) -> SimulationResult:
        """Execute a simulation."""
        ...

    def get_result(self, job_id: str) -> SimulationResult:
        """Fetch simulation results."""
        ...


# =============================================================================
# Engine Registry
# =============================================================================

@dataclass
class ValidationResult:
    """Validation result."""

    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class SimulationResult:
    """Standard simulation result container."""

    job_id: str
    status: str  # "pending", "running", "completed", "failed"
    success: bool

    # Unified model (the key abstraction)
    system_model: Any = None  # PowerSystemModel

    # Engine-specific raw data (for debugging)
    raw_data: dict[str, Any] = field(default_factory=dict)

    # Metadata
    metadata: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    # Timing
    start_time: str = ""
    end_time: str = ""


class EngineRegistry:
    """Registry of available simulation engines.

    Engines register themselves at import time:

        # In cloudpss_skills_v2/engines/cloudpss/__init__.py
        from cloudpss_skills_v2.core.engine_registry import EngineRegistry
        from .adapter import CloudPSSAdapter

        EngineRegistry.register("cloudpss", CloudPSSAdapter)
    """

    _engines: dict[str, type[EngineInterface]] = {}
    _capabilities: dict[str, EngineCapabilities] = {}

    @classmethod
    def register(
        cls,
        name: str,
        engine_class: type[EngineInterface]
    ) -> None:
        """Register an engine."""
        cls._engines[name] = engine_class

        # Cache capabilities
        try:
            instance = engine_class()
            cls._capabilities[name] = instance.capabilities
        except Exception as e:
            raise RuntimeError(f"Failed to get capabilities for {name}: {e}")

    @classmethod
    def get(cls, name: str) -> type[EngineInterface]:
        """Get engine class by name."""
        if name not in cls._engines:
            available = ", ".join(cls.list_engines())
            raise KeyError(f"Unknown engine '{name}'. Available: {available}")
        return cls._engines[name]

    @classmethod
    def get_capabilities(cls, name: str) -> EngineCapabilities:
        """Get cached capabilities for an engine."""
        if name not in cls._capabilities:
            raise KeyError(f"Unknown engine '{name}'")
        return cls._capabilities[name]

    @classmethod
    def list_engines(
        cls,
        simulation_type: SimulationType | None = None
    ) -> list[str]:
        """List available engines, optionally filtered by simulation type."""
        if simulation_type is None:
            return sorted(cls._engines.keys())

        return [
            name for name, caps in cls._capabilities.items()
            if simulation_type in caps.supported_simulations
        ]

    @classmethod
    def find_best_engine(
        cls,
        simulation_type: SimulationType,
        model_size: int | None = None
    ) -> str | None:
        """Find the best engine for a given simulation.

        Criteria:
        1. Supports the simulation type
        2. Can handle the model size
        3. Prefer local engines for small models (faster)
        4. Prefer cloud engines for very large models
        """
        candidates = []

        for name, caps in cls._capabilities.items():
            if simulation_type not in caps.supported_simulations:
                continue

            if model_size and caps.max_buses and model_size > caps.max_buses:
                continue

            # Score: prefer unlimited capacity, parallel support
            score = 0
            if caps.max_buses is None:
                score += 100
            if caps.supports_parallel:
                score += 50

            candidates.append((name, score))

        if not candidates:
            return None

        # Return highest scored engine
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[0][0]

    @classmethod
    def clear(cls) -> None:
        """Clear all registered engines (mainly for testing)."""
        cls._engines.clear()
        cls._capabilities.clear()


# =============================================================================
# Example Capability Declarations
# =============================================================================

def create_cloudpss_capabilities() -> EngineCapabilities:
    """Example: CloudPSS capability declaration."""
    return EngineCapabilities(
        engine_name="cloudpss",
        engine_version="2.0",
        vendor="CloudPSS",
        description="Cloud-based power system simulation platform",

        supported_simulations=[
            SimulationType.POWER_FLOW_AC,
            SimulationType.SHORT_CIRCUIT_3PH,
            SimulationType.EMT_TRANSIENT,
            SimulationType.TRANSIENT_STABILITY,
            SimulationType.CONTINGENCY_ANALYSIS,
        ],
        supported_model_formats=["cloudpss_rid", "json"],

        max_buses=10000,
        max_branches=20000,
        supports_parallel=True,

        supports_reactive_power=True,
        supports_tap_changers=True,
        supports_phase_shifters=True,
        supports_hvdc=True,

        simulation_parameters={
            SimulationType.POWER_FLOW_AC: [
                ParameterSpec(
                    name="algorithm",
                    param_type="enum",
                    description="Power flow solution algorithm",
                    default="newton_raphson",
                    choices=["newton_raphson", "fast_decoupled", "gauss_seidel"]
                ),
                ParameterSpec(
                    name="flat_start",
                    param_type="bool",
                    description="Use flat start (1.0 p.u., 0°)",
                    default=False
                ),
                ParameterSpec(
                    name="distributed_slack",
                    param_type="bool",
                    description="Distribute slack across generators",
                    default=False
                ),
            ],
            SimulationType.EMT_TRANSIENT: [
                ParameterSpec(
                    name="time_step_us",
                    param_type="float",
                    description="Simulation time step in microseconds",
                    default=50.0,
                    min_value=1.0,
                    max_value=1000.0,
                    units="us"
                ),
                ParameterSpec(
                    name="duration_s",
                    param_type="float",
                    description="Simulation duration in seconds",
                    default=10.0,
                    min_value=0.001,
                    max_value=3600.0,
                    units="s"
                ),
            ],
        }
    )


def create_pandapower_capabilities() -> EngineCapabilities:
    """Example: Pandapower capability declaration."""
    return EngineCapabilities(
        engine_name="pandapower",
        engine_version="2.13",
        vendor="PandaPower Team",
        description="Open source power system analysis framework",

        supported_simulations=[
            SimulationType.POWER_FLOW_AC,
            SimulationType.POWER_FLOW_DC,
            SimulationType.OPTIMAL_POWER_FLOW,
            SimulationType.SHORT_CIRCUIT_3PH,
            SimulationType.SHORT_CIRCUIT_1PH,
        ],
        supported_model_formats=["pandapower_net", "matpower", "excel", "json"],

        max_buses=None,  # Memory limited
        max_branches=None,
        supports_parallel=True,

        supports_reactive_power=True,
        supports_tap_changers=True,
        supports_phase_shifters=False,
        supports_hvdc=False,

        simulation_parameters={
            SimulationType.POWER_FLOW_AC: [
                ParameterSpec(
                    name="algorithm",
                    param_type="enum",
                    description="Power flow algorithm",
                    default="nr",
                    choices=["nr", "iwamoto_nr", "gs", "fdbx", "fdxb"]
                ),
                ParameterSpec(
                    name="calculate_voltage_angles",
                    param_type="bool",
                    description="Calculate voltage angles",
                    default=True
                ),
                ParameterSpec(
                    name="numba",
                    param_type="bool",
                    description="Use Numba JIT acceleration",
                    default=True
                ),
            ],
            SimulationType.OPTIMAL_POWER_FLOW: [
                ParameterSpec(
                    name="objective",
                    param_type="enum",
                    description="Optimization objective",
                    default="min_cost",
                    choices=["min_cost", "min_loss", "max_gen_margin"]
                ),
            ],
        }
    )


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "SimulationType",
    "ParameterSpec",
    "SimulationConfig",
    "EngineCapabilities",
    "EngineInterface",
    "EngineRegistry",
    "ValidationResult",
    "SimulationResult",
    # Examples
    "create_cloudpss_capabilities",
    "create_pandapower_capabilities",
]
