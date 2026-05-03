"""Power System Model - Unified DataClass representation.

This module provides engine-agnostic data structures for power system models,
ensuring type safety and physical correctness across all simulation engines.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from functools import cached_property
from typing import Literal

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


# =============================================================================
# Enumerations and Constants
# =============================================================================

BusType = Literal["PQ", "PV", "SLACK", "ISOLATED"]
BranchType = Literal["LINE", "TRANSFORMER", "PHASE_SHIFTER"]
SeverityLevel = Literal["NORMAL", "WARNING", "CRITICAL"]

# Physical constants and valid ranges
VOLTAGE_PU_MIN = 0.5  # Minimum physically reasonable voltage (p.u.)
VOLTAGE_PU_MAX = 1.5  # Maximum physically reasonable voltage (p.u.)
ANGLE_DEGREE_MIN = -90.0
ANGLE_DEGREE_MAX = 90.0
LOADING_PERCENT_MAX = 500.0  # Maximum physically reasonable loading


# =============================================================================
# Validation Functions
# =============================================================================

def validate_voltage_pu(value: float | None, context: str = "") -> None:
    """Validate voltage magnitude is in physically reasonable range."""
    if value is None:
        return
    if not VOLTAGE_PU_MIN <= value <= VOLTAGE_PU_MAX:
        raise ValueError(
            f"{context} Voltage {value} p.u. out of valid range "
            f"[{VOLTAGE_PU_MIN}, {VOLTAGE_PU_MAX}]"
        )


def validate_angle_degree(value: float | None, context: str = "") -> None:
    """Validate voltage angle is in physically reasonable range."""
    if value is None:
        return
    if not ANGLE_DEGREE_MIN <= value <= ANGLE_DEGREE_MAX:
        raise ValueError(
            f"{context} Angle {value}° out of valid range "
            f"[{ANGLE_DEGREE_MIN}, {ANGLE_DEGREE_MAX}]"
        )


def validate_bus_id(bus_id: int, context: str = "") -> None:
    """Validate bus ID is non-negative."""
    if bus_id < 0:
        raise ValueError(f"{context} Bus ID {bus_id} must be non-negative")


# =============================================================================
# Core Data Classes
# =============================================================================

@dataclass(frozen=True)
class Bus:
    """Unified bus (node) data class - engine independent.

    Attributes:
        bus_id: Unique identifier for the bus (non-negative integer)
        name: Human-readable name for the bus
        base_kv: Base voltage in kV (positive)
        bus_type: Bus type - "PQ", "PV", "SLACK", or "ISOLATED"

        # Power flow results (optional, None if not computed)
        v_magnitude_pu: Voltage magnitude in per unit
        v_angle_degree: Voltage angle in degrees
        p_injected_mw: Net active power injection in MW (generation - load)
        q_injected_mvar: Net reactive power injection in Mvar

        # Operational limits
        vm_max_pu: Maximum voltage magnitude limit (p.u.)
        vm_min_pu: Minimum voltage magnitude limit (p.u.)

        # Additional metadata
        area: Control area number
        zone: Control zone number
    """

    # Required fields
    bus_id: int
    name: str
    base_kv: float
    bus_type: BusType = "PQ"

    # Power flow results (optional)
    v_magnitude_pu: float | None = None
    v_angle_degree: float | None = None
    p_injected_mw: float | None = None
    q_injected_mvar: float | None = None

    # Operational limits
    vm_max_pu: float = 1.1
    vm_min_pu: float = 0.9

    # Metadata
    area: int = 1
    zone: int = 1

    def __post_init__(self) -> None:
        """Validate physical correctness after construction."""
        # Bus ID validation
        validate_bus_id(self.bus_id, f"Bus {self.name}:")

        # Base voltage must be positive
        if self.base_kv <= 0:
            raise ValueError(f"Bus {self.name}: Base voltage {self.base_kv} kV must be positive")

        # Bus type validation
        valid_types = ("PQ", "PV", "SLACK", "ISOLATED")
        if self.bus_type not in valid_types:
            raise ValueError(f"Bus {self.name}: Invalid bus type '{self.bus_type}'")

        # Voltage limits validation
        if self.vm_min_pu >= self.vm_max_pu:
            raise ValueError(
                f"Bus {self.name}: Min voltage {self.vm_min_pu} >= max voltage {self.vm_max_pu}"
            )

        # Power flow results validation
        validate_voltage_pu(self.v_magnitude_pu, f"Bus {self.name}:")
        validate_angle_degree(self.v_angle_degree, f"Bus {self.name}:")

    def is_slack(self) -> bool:
        """Check if this is the slack/reference bus."""
        return self.bus_type == "SLACK"

    def is_pv(self) -> bool:
        """Check if this is a PV (voltage-controlled) bus."""
        return self.bus_type == "PV"

    def has_voltage_violation(self) -> bool:
        """Check if voltage is outside operational limits."""
        if self.v_magnitude_pu is None:
            return False
        return self.v_magnitude_pu < self.vm_min_pu or self.v_magnitude_pu > self.vm_max_pu

    def voltage_deviation(self) -> float | None:
        """Calculate voltage deviation from nominal (1.0 p.u.)."""
        if self.v_magnitude_pu is None:
            return None
        return abs(self.v_magnitude_pu - 1.0)


@dataclass(frozen=True)
class Branch:
    """Unified branch (line/transformer) data class - engine independent.

    Attributes:
        from_bus: ID of the from bus
        to_bus: ID of the to bus
        name: Human-readable name for the branch
        branch_type: Type of branch - "LINE", "TRANSFORMER", or "PHASE_SHIFTER"

        # Series parameters (per unit)
        r_pu: Resistance
        x_pu: Reactance

        # Shunt parameters (per unit, total)
        b_pu: Susceptitance (charging for lines, magnetizing for transformers)
        g_pu: Conductance (usually zero)

        # Rating
        rate_a_mva: Normal rating in MVA
        rate_b_mva: Short-term rating in MVA (optional)
        rate_c_mva: Emergency rating in MVA (optional)

        # Transformer-specific parameters (optional, for transformers)
        tap_ratio: Tap changer ratio (1.0 for lines)
        phase_shift_degree: Phase shift angle in degrees

        # Power flow results (optional)
        p_from_mw: Active power flow at from end (MW)
        q_from_mvar: Reactive power flow at from end (Mvar)
        p_to_mw: Active power flow at to end (MW)
        q_to_mvar: Reactive power flow at to end (Mvar)

        # Derived results
        loading_percent: Apparent power loading as percentage of rate_a
        p_loss_mw: Active power loss (computed)
        q_loss_mvar: Reactive power loss (computed)

        # Status
        in_service: Whether the branch is in service
    """

    # Required fields
    from_bus: int
    to_bus: int
    name: str
    branch_type: BranchType = "LINE"

    # Series parameters
    r_pu: float = 0.0
    x_pu: float = 0.0

    # Shunt parameters
    b_pu: float = 0.0
    g_pu: float = 0.0

    # Ratings
    rate_a_mva: float = 0.0
    rate_b_mva: float | None = None
    rate_c_mva: float | None = None

    # Transformer parameters
    tap_ratio: float = 1.0
    phase_shift_degree: float = 0.0

    # Power flow results
    p_from_mw: float | None = None
    q_from_mvar: float | None = None
    p_to_mw: float | None = None
    q_to_mvar: float | None = None

    # Derived (set by post-processing)
    loading_percent: float | None = None
    p_loss_mw: float | None = None
    q_loss_mvar: float | None = None

    # Status
    in_service: bool = True

    def __post_init__(self) -> None:
        """Validate physical correctness after construction."""
        # Bus ID validation
        validate_bus_id(self.from_bus, f"Branch {self.name} from_bus:")
        validate_bus_id(self.to_bus, f"Branch {self.name} to_bus:")

        # Cannot connect bus to itself
        if self.from_bus == self.to_bus:
            raise ValueError(f"Branch {self.name}: Cannot connect bus to itself")

        # Branch type validation
        valid_types = ("LINE", "TRANSFORMER", "PHASE_SHIFTER")
        if self.branch_type not in valid_types:
            raise ValueError(f"Branch {self.name}: Invalid branch type '{self.branch_type}'")

        # Rating must be positive if specified
        if self.rate_a_mva < 0:
            raise ValueError(f"Branch {self.name}: Rating {self.rate_a_mva} must be non-negative")

        # Loading validation - warn on extreme values but don't raise
        if self.loading_percent is not None:
            if self.loading_percent < 0:
                raise ValueError(
                    f"Branch {self.name}: Loading {self.loading_percent}% cannot be negative"
                )
            if self.loading_percent > LOADING_PERCENT_MAX:
                logger.warning(
                    f"Branch {self.name}: Loading {self.loading_percent}% exceeds reasonable range (>500%%). "
                    f"This may indicate a data issue but will be accepted."
                )

    def is_transformer(self) -> bool:
        """Check if this is a transformer."""
        return self.branch_type in ("TRANSFORMER", "PHASE_SHIFTER")

    def apparent_power_from_mva(self) -> float | None:
        """Calculate apparent power at from end."""
        if self.p_from_mw is None or self.q_from_mvar is None:
            return None
        return np.sqrt(self.p_from_mw**2 + self.q_from_mvar**2)

    def has_thermal_violation(self, threshold: float = 1.0) -> bool:
        """Check if loading exceeds threshold (default 100%)."""
        if self.loading_percent is None:
            return False
        return self.loading_percent > threshold * 100

    def calculate_loading(self) -> float | None:
        """Calculate loading percentage from power flow results."""
        s_from = self.apparent_power_from_mva()
        if s_from is None or self.rate_a_mva == 0:
            return None
        return (s_from / self.rate_a_mva) * 100


@dataclass(frozen=True)
class Generator:
    """Unified generator data class - engine independent.

    Attributes:
        bus_id: Bus where generator is connected
        name: Human-readable name

        # Operational setpoints
        p_gen_mw: Active power generation setpoint (MW)
        v_set_pu: Voltage setpoint (p.u.) for PV buses

        # Reactive power limits (Mvar)
        q_max_mvar: Maximum reactive power output
        q_min_mvar: Minimum reactive power output

        # Active power limits (MW)
        p_max_mw: Maximum active power output
        p_min_mw: Minimum active power output

        # Power flow results (optional)
        q_gen_mvar: Actual reactive power output

        # Status
        in_service: Whether the generator is in service
    """

    bus_id: int
    name: str

    # Setpoints
    p_gen_mw: float = 0.0
    v_set_pu: float | None = None

    # Limits
    q_max_mvar: float = 999999.0
    q_min_mvar: float = -999999.0
    p_max_mw: float = 999999.0
    p_min_mw: float = -999999.0

    # Results
    q_gen_mvar: float | None = None

    # Status
    in_service: bool = True

    def __post_init__(self) -> None:
        """Validate physical correctness."""
        validate_bus_id(self.bus_id, f"Generator {self.name}:")

        # Power limits consistency
        if self.p_min_mw > self.p_max_mw:
            raise ValueError(
                f"Generator {self.name}: Pmin {self.p_min_mw} > Pmax {self.p_max_mw}"
            )
        if self.q_min_mvar > self.q_max_mvar:
            raise ValueError(
                f"Generator {self.name}: Qmin {self.q_min_mvar} > Qmax {self.q_max_mvar}"
            )

        # Setpoint within limits
        if not (self.p_min_mw <= self.p_gen_mw <= self.p_max_mw):
            raise ValueError(
                f"Generator {self.name}: P setpoint {self.p_gen_mw} outside limits "
                f"[{self.p_min_mw}, {self.p_max_mw}]"
            )

    def is_at_p_limit(self) -> bool:
        """Check if operating at active power limit."""
        return self.p_gen_mw <= self.p_min_mw or self.p_gen_mw >= self.p_max_mw

    def is_at_q_limit(self) -> bool | None:
        """Check if operating at reactive power limit."""
        if self.q_gen_mvar is None:
            return None
        return self.q_gen_mvar <= self.q_min_mvar or self.q_gen_mvar >= self.q_max_mvar


@dataclass(frozen=True)
class Load:
    """Unified load data class - engine independent."""

    bus_id: int
    name: str

    # Load demand
    p_mw: float = 0.0
    q_mvar: float = 0.0

    # Load characteristics
    is_constant_power: bool = True
    is_constant_current: bool = False
    is_constant_impedance: bool = False

    # Status
    in_service: bool = True

    def __post_init__(self) -> None:
        """Validate load data."""
        validate_bus_id(self.bus_id, f"Load {self.name}:")


@dataclass(frozen=True)
class Transformer:
    """Detailed transformer data (when more info than Branch is needed)."""

    name: str
    hv_bus: int  # High voltage side
    lv_bus: int  # Low voltage side

    # Rated parameters
    sn_mva: float  # Rated apparent power
    vn_hv_kv: float  # Rated HV voltage
    vn_lv_kv: float  # Rated LV voltage

    # Impedance
    vk_percent: float  # Short circuit voltage
    vkr_percent: float  # Real part of short circuit voltage
    pfe_kw: float = 0.0  # Iron losses
    i0_percent: float = 0.0  # No-load current

    # Tap changer
    tap_pos: int = 0
    tap_min: int = -10
    tap_max: int = 10
    tap_step_percent: float = 1.25

    def __post_init__(self) -> None:
        """Validate transformer data."""
        validate_bus_id(self.hv_bus, f"Transformer {self.name} HV:")
        validate_bus_id(self.lv_bus, f"Transformer {self.name} LV:")


# =============================================================================
# Power System Model Container
# =============================================================================

@dataclass
class PowerSystemModel:
    """Complete power system model - unified representation.

    This is the central data structure that all engine adapters convert to.
    It provides both direct DataClass access and DataFrame views for analysis.
    """

    # Core components
    buses: list[Bus] = field(default_factory=list)
    branches: list[Branch] = field(default_factory=list)
    generators: list[Generator] = field(default_factory=list)
    loads: list[Load] = field(default_factory=list)
    transformers: list[Transformer] = field(default_factory=list)

    # System parameters
    base_mva: float = 100.0
    frequency_hz: float = 50.0

    # Metadata
    name: str = ""
    description: str = ""
    source_engine: str = ""  # Which engine created this model
    version: str = "1.0"

    def __post_init__(self) -> None:
        """Validate model consistency."""
        # Validate base MVA
        if self.base_mva <= 0:
            raise ValueError(f"Base MVA {self.base_mva} must be positive")

        # Check for duplicate bus IDs
        bus_ids = [b.bus_id for b in self.buses]
        if len(bus_ids) != len(set(bus_ids)):
            duplicates = [bid for bid in bus_ids if bus_ids.count(bid) > 1]
            raise ValueError(f"Duplicate bus IDs found: {set(duplicates)}")

        # Validate branch connections
        bus_id_set = set(bus_ids)
        for branch in self.branches:
            if branch.from_bus not in bus_id_set:
                raise ValueError(
                    f"Branch {branch.name} references unknown from_bus {branch.from_bus}"
                )
            if branch.to_bus not in bus_id_set:
                raise ValueError(
                    f"Branch {branch.name} references unknown to_bus {branch.to_bus}"
                )

        # Validate generator connections
        for gen in self.generators:
            if gen.bus_id not in bus_id_set:
                raise ValueError(
                    f"Generator {gen.name} references unknown bus {gen.bus_id}"
                )

    # -------------------------------------------------------------------------
    # DataFrame Views (for vectorized analysis)
    # -------------------------------------------------------------------------

    @cached_property
    def buses_df(self) -> pd.DataFrame:
        """Bus data as DataFrame (cached)."""
        if not self.buses:
            return pd.DataFrame()
        return pd.DataFrame([vars(b) for b in self.buses])

    @cached_property
    def branches_df(self) -> pd.DataFrame:
        """Branch data as DataFrame (cached)."""
        if not self.branches:
            return pd.DataFrame()
        return pd.DataFrame([vars(b) for b in self.branches])

    @cached_property
    def generators_df(self) -> pd.DataFrame:
        """Generator data as DataFrame (cached)."""
        if not self.generators:
            return pd.DataFrame()
        return pd.DataFrame([vars(g) for g in self.generators])

    # -------------------------------------------------------------------------
    # Convenience Accessors
    # -------------------------------------------------------------------------

    def get_bus_by_id(self, bus_id: int) -> Bus | None:
        """Get bus by ID."""
        for bus in self.buses:
            if bus.bus_id == bus_id:
                return bus
        return None

    def get_bus_by_name(self, name: str) -> Bus | None:
        """Get bus by name."""
        for bus in self.buses:
            if bus.name == name:
                return bus
        return None

    def get_branches_connected_to(self, bus_id: int) -> list[Branch]:
        """Get all branches connected to a bus."""
        return [
            br for br in self.branches
            if br.from_bus == bus_id or br.to_bus == bus_id
        ]

    def get_generators_at_bus(self, bus_id: int) -> list[Generator]:
        """Get all generators at a bus."""
        return [g for g in self.generators if g.bus_id == bus_id]

    # -------------------------------------------------------------------------
    # System-Wide Calculations
    # -------------------------------------------------------------------------

    def total_generation_mw(self) -> float:
        """Total active power generation."""
        return sum(g.p_gen_mw for g in self.generators if g.in_service)

    def total_load_mw(self) -> float:
        """Total active power load."""
        return sum(ld.p_mw for ld in self.loads if ld.in_service)

    def total_losses_mw(self) -> float | None:
        """Total active power losses (None if power flow not run)."""
        if not self.buses:
            return None
        # Losses = Generation - Load (if we have injection results)
        total_inj = sum(
            (b.p_injected_mw or 0) for b in self.buses
        )
        return total_inj if total_inj != 0 else None

    def get_slack_bus(self) -> Bus | None:
        """Get the slack bus."""
        for bus in self.buses:
            if bus.is_slack():
                return bus
        return None

    def validate_physical(self, raise_on_error: bool = True) -> list[dict[str, Any]]:
        """Validate physical correctness of the model.

        Performs comprehensive checks including:
        - Power balance (Generation ≈ Load + Losses)
        - Network connectivity (graph is connected)
        - Slack bus existence
        - Voltage angle bounds
        - Power flow sign consistency

        Args:
            raise_on_error: If True, raise ValueError on first violation.
                           If False, return all violations.

        Returns:
            List of violation dictionaries with keys: type, message, severity

        Raises:
            ValueError: If raise_on_error=True and violations found
        """
        violations = []

        # 1. Check slack bus exists
        slack_bus = self.get_slack_bus()
        if slack_bus is None:
            violations.append({
                "type": "slack_bus",
                "message": "No slack bus found - system lacks reference",
                "severity": "CRITICAL"
            })

        # 2. Check power balance (if we have results)
        total_gen = self.total_generation_mw()
        total_load = self.total_load_mw()
        total_losses = self.total_losses_mw()

        if total_gen > 0 and total_load > 0:
            if total_losses is not None:
                # Check: Gen ≈ Load + Losses
                expected_gen = total_load + total_losses
                imbalance = abs(total_gen - expected_gen)
                imbalance_pct = imbalance / total_gen * 100 if total_gen > 0 else 0

                if imbalance_pct > 5:  # 5% tolerance
                    violations.append({
                        "type": "power_balance",
                        "message": f"Power imbalance: Gen={total_gen:.2f}MW, "
                                  f"Load+Losses={expected_gen:.2f}MW, "
                                  f"Imbalance={imbalance_pct:.2f}%",
                        "severity": "WARNING"
                    })
            else:
                # No power flow results - just check Gen ≈ Load (rough check)
                if abs(total_gen - total_load) / total_gen > 0.5:  # 50% tolerance
                    violations.append({
                        "type": "power_balance",
                        "message": f"Large generation-load mismatch: "
                                  f"Gen={total_gen:.2f}MW, Load={total_load:.2f}MW",
                        "severity": "WARNING"
                    })

        # 3. Check network connectivity
        connectivity_issues = self._check_connectivity()
        violations.extend(connectivity_issues)

        # 4. Check voltage angles are reasonable
        for bus in self.buses:
            if bus.v_angle_degree is not None:
                if abs(bus.v_angle_degree) > 90:
                    violations.append({
                        "type": "voltage_angle",
                        "message": f"Bus {bus.name}: Angle {bus.v_angle_degree:.2f}° "
                                  f"exceeds ±90° (unstable system)",
                        "severity": "WARNING"
                    })

        # 5. Check branch power flow consistency
        for branch in self.branches:
            if branch.p_from_mw is not None and branch.p_to_mw is not None:
                # Power entering branch ≈ -power leaving branch (with losses)
                if abs(branch.p_from_mw + branch.p_to_mw) > 100:  # 100MW tolerance
                    violations.append({
                        "type": "branch_power",
                        "message": f"Branch {branch.name}: P_from={branch.p_from_mw:.2f}MW, "
                                  f"P_to={branch.p_to_mw:.2f}MW, "
                                  f"Sum={branch.p_from_mw + branch.p_to_mw:.2f}MW "
                                  f"(should be ≈ 0 with losses)",
                        "severity": "INFO"
                    })

        if raise_on_error and violations:
            critical = [v for v in violations if v["severity"] == "CRITICAL"]
            if critical:
                raise ValueError(f"Critical violations: {critical[0]['message']}")

        return violations

    def _check_connectivity(self) -> list[dict[str, Any]]:
        """Check network connectivity using graph traversal."""
        violations = []

        if not self.buses or not self.branches:
            return violations

        # Build adjacency list
        adjacency = {bus.bus_id: set() for bus in self.buses}
        for branch in self.branches:
            if branch.in_service:
                adjacency[branch.from_bus].add(branch.to_bus)
                adjacency[branch.to_bus].add(branch.from_bus)

        # BFS from first bus
        visited = set()
        queue = [self.buses[0].bus_id]
        visited.add(self.buses[0].bus_id)

        while queue:
            current = queue.pop(0)
            for neighbor in adjacency.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        # Check if all buses are visited
        all_bus_ids = {b.bus_id for b in self.buses}
        isolated = all_bus_ids - visited

        if isolated:
            violations.append({
                "type": "connectivity",
                "message": f"Network is not fully connected. "
                          f"Isolated buses: {len(isolated)}",
                "severity": "CRITICAL"
            })

        return violations

    def get_voltage_violations(self) -> list[tuple[Bus, float, str]]:
        """Get all buses with voltage violations.

        Returns:
            List of (bus, actual_voltage, violation_type) tuples
        """
        violations = []
        for bus in self.buses:
            if bus.v_magnitude_pu is None:
                continue
            if bus.v_magnitude_pu < bus.vm_min_pu:
                violations.append((bus, bus.v_magnitude_pu, "undervoltage"))
            elif bus.v_magnitude_pu > bus.vm_max_pu:
                violations.append((bus, bus.v_magnitude_pu, "overvoltage"))
        return violations

    def get_thermal_violations(self, threshold: float = 1.0) -> list[tuple[Branch, float]]:
        """Get all branches with thermal violations.

        Args:
            threshold: Loading threshold (1.0 = 100%)

        Returns:
            List of (branch, loading_percent) tuples
        """
        violations = []
        for branch in self.branches:
            if branch.loading_percent and branch.loading_percent > threshold * 100:
                violations.append((branch, branch.loading_percent))
        return violations

    # -------------------------------------------------------------------------
    # Model Modification (returns new model - immutable)
    # -------------------------------------------------------------------------

    def with_bus_removed(self, bus_id: int) -> "PowerSystemModel":
        """Create new model with a bus removed (N-1 style)."""
        new_buses = [b for b in self.buses if b.bus_id != bus_id]
        new_branches = [
            br for br in self.branches
            if br.from_bus != bus_id and br.to_bus != bus_id
        ]
        new_gens = [g for g in self.generators if g.bus_id != bus_id]
        new_loads = [ld for ld in self.loads if ld.bus_id != bus_id]

        return PowerSystemModel(
            buses=new_buses,
            branches=new_branches,
            generators=new_gens,
            loads=new_loads,
            base_mva=self.base_mva,
            name=f"{self.name}_bus_{bus_id}_removed"
        )

    def with_branch_removed(self, branch_name: str) -> "PowerSystemModel":
        """Create new model with a branch removed (N-1 style)."""
        target_branch = None
        for br in self.branches:
            if br.name == branch_name:
                target_branch = br
                break

        if target_branch is None:
            raise ValueError(f"Branch {branch_name} not found")

        new_branches = [br for br in self.branches if br.name != branch_name]

        return PowerSystemModel(
            buses=self.buses,
            branches=new_branches,
            generators=self.generators,
            loads=self.loads,
            base_mva=self.base_mva,
            name=f"{self.name}_branch_{branch_name}_removed"
        )


# =============================================================================
# Validation Result
# =============================================================================

@dataclass
class ValidationResult:
    """Result of model validation."""

    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def __bool__(self) -> bool:
        return self.valid


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    # Enums and constants
    "BusType",
    "BranchType",
    "SeverityLevel",
    "VOLTAGE_PU_MIN",
    "VOLTAGE_PU_MAX",
    # Data classes
    "Bus",
    "Branch",
    "Generator",
    "Load",
    "Transformer",
    "PowerSystemModel",
    "ValidationResult",
    # Validation functions
    "validate_voltage_pu",
    "validate_angle_degree",
]
