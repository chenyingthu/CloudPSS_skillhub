"""
DataLib - Standardized Power System Data Types

Provides engine-agnostic data types for power system modeling and analysis.
All types use dataclasses with full type annotations and conversion helpers.

These types serve as the canonical data exchange format between:
- Engine adapters (powerAPI layer)
- Simulation APIs (PowerSkill layer)
- Skills (user-level)
- Algorithms (AlgoLib)
- Workflows (WorkflowLib)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class BusType(Enum):
    """Bus classification type."""

    PQ = "pq"
    PV = "pv"
    SLACK = "slack"
    ISOLATED = "isolated"


class BranchType(Enum):
    """Branch element type."""

    LINE = "line"
    TRANSFORMER = "transformer"
    THREE_WINDING_TRANSFORMER = "three_winding_transformer"


class GeneratorType(Enum):
    """Generator classification."""

    SYNCHRONOUS = "synchronous"
    WIND = "wind"
    PV = "pv"
    HYDRO = "hydro"
    NUCLEAR = "nuclear"
    THERMAL = "thermal"
    EXTERNAL_GRID = "external_grid"


class FaultType(Enum):
    """Short circuit fault type."""

    THREE_PHASE = "3ph"
    SINGLE_LINE_TO_GROUND = "slg"
    LINE_TO_LINE = "ll"
    DOUBLE_LINE_TO_GROUND = "dlg"


class LoadType(Enum):
    """Load classification."""

    CONSTANT_POWER = "constant_power"
    CONSTANT_CURRENT = "constant_current"
    CONSTANT_IMPEDANCE = "constant_impedance"
    ZIP = "zip"


class SwitchState(Enum):
    """Switch operational state."""

    OPEN = "open"
    CLOSED = "closed"


class RenewableType(Enum):
    """Renewable energy source type."""

    PV_STATION = "pv_station"
    WIND_FARM = "wind_farm"
    BATTERY = "battery"
    HYBRID = "hybrid"


class InverterType(Enum):
    """Power electronics inverter type."""

    PV_INVERTER = "pv_inverter"
    WIND_CONVERTER = "wind_converter"
    MMC = "mmc"
    SVG = "svg"
    VSC_HVDC = "vsc_hvdc"


class DynamicModelType(Enum):
    """Dynamic model type for generator controls."""

    EXCITER = "exciter"
    GOVERNOR = "governor"
    TURBINE = "turbine"
    PSS = "pss"


class HVDCType(Enum):
    """HVDC transmission type."""

    LCC = "lcc"
    VSC = "vsc"
    MMC = "mmc"


def _optional_float(value: Any) -> float | None:
    """Convert a value to float, returning None on failure."""
    if value is None:
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


@dataclass
class PowerElectronicsData:
    """Base class for power electronics devices (SVG, SVC, MMC, etc.)."""

    name: str = ""
    bus: str = field(default_factory=lambda: "")
    inverter_type: InverterType = InverterType.PV_INVERTER
    p_mw: float = 0.0
    q_mvar: float = 0.0
    v_set_pu: float = 1.0
    rated_mva: float = 0.0
    in_service: bool = True
    engine_id: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            k: (v.value if isinstance(v, Enum) else v)
            for k, v in (
                (f, getattr(self, f))
                for f in (
                    "name",
                    "bus",
                    "inverter_type",
                    "p_mw",
                    "q_mvar",
                    "v_set_pu",
                    "rated_mva",
                    "in_service",
                )
            )
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PowerElectronicsData:
        itype = data.get("inverter_type", "pv_inverter")
        if isinstance(itype, str):
            itype = InverterType(itype)
        return cls(
            name=data.get("name", ""),
            bus=data.get("bus", ""),
            inverter_type=itype,
            p_mw=float(data.get("p_mw", 0.0)),
            q_mvar=float(data.get("q_mvar", 0.0)),
            v_set_pu=float(data.get("v_set_pu", 1.0)),
            rated_mva=float(data.get("rated_mva", 0.0)),
            in_service=bool(data.get("in_service", True)),
        )


@dataclass
class SVGData(PowerElectronicsData):
    """Static Var Generator (SVG) data."""

    q_max_mvar: float = 0.0
    q_min_mvar: float = 0.0

    def __init__(self, bus: str = "", name: str = "", **kwargs):
        parent_kwargs = {
            k: kwargs.pop(k, v)
            for k, v in (
                ("p_mw", 0.0),
                ("q_mvar", 0.0),
                ("v_set_pu", 1.0),
                ("rated_mva", 0.0),
                ("in_service", True),
            )
        }
        super().__init__(
            name=name, bus=bus, inverter_type=InverterType.SVG, **parent_kwargs
        )
        self.q_max_mvar = kwargs.get("q_max_mvar", 0.0)
        self.q_min_mvar = kwargs.get("q_min_mvar", 0.0)

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d.update({k: getattr(self, k) for k in ("q_max_mvar", "q_min_mvar")})
        return d

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SVGData:
        return cls(
            bus=data.get("bus", ""),
            name=data.get("name", ""),
            p_mw=float(data.get("p_mw", 0.0)),
            q_mvar=float(data.get("q_mvar", 0.0)),
            v_set_pu=float(data.get("v_set_pu", 1.0)),
            rated_mva=float(data.get("rated_mva", 0.0)),
            q_max_mvar=float(data.get("q_max_mvar", 0.0)),
            q_min_mvar=float(data.get("q_min_mvar", 0.0)),
            in_service=bool(data.get("in_service", True)),
        )


@dataclass
class SVCData(PowerElectronicsData):
    """Static Var Compensator (SVC) data."""

    q_max_mvar: float = 0.0
    q_min_mvar: float = 0.0
    slope_pct: float = 0.05

    def __init__(self, bus: str = "", name: str = "", **kwargs):
        parent_kwargs = {
            k: kwargs.pop(k, v)
            for k, v in (
                ("p_mw", 0.0),
                ("q_mvar", 0.0),
                ("v_set_pu", 1.0),
                ("rated_mva", 0.0),
                ("in_service", True),
            )
        }
        super().__init__(
            name=name, bus=bus, inverter_type=InverterType.PV_INVERTER, **parent_kwargs
        )
        self.q_max_mvar = kwargs.get("q_max_mvar", 0.0)
        self.q_min_mvar = kwargs.get("q_min_mvar", 0.0)
        self.slope_pct = kwargs.get("slope_pct", 0.05)

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d.update(
            {k: getattr(self, k) for k in ("q_max_mvar", "q_min_mvar", "slope_pct")}
        )
        return d

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SVCData:
        return cls(
            bus=data.get("bus", ""),
            name=data.get("name", ""),
            p_mw=float(data.get("p_mw", 0.0)),
            q_mvar=float(data.get("q_mvar", 0.0)),
            v_set_pu=float(data.get("v_set_pu", 1.0)),
            rated_mva=float(data.get("rated_mva", 0.0)),
            q_max_mvar=float(data.get("q_max_mvar", 0.0)),
            q_min_mvar=float(data.get("q_min_mvar", 0.0)),
            slope_pct=float(data.get("slope_pct", 0.05)),
            in_service=bool(data.get("in_service", True)),
        )


@dataclass
class MMCData(PowerElectronicsData):
    """Modular Multilevel Converter (MMC) data."""

    arm_count: int = 10
    sub_module_count: int = 200
    dc_voltage_kv: float = 0.0

    def __init__(self, bus: str = "", name: str = "", **kwargs):
        parent_kwargs = {
            k: kwargs.pop(k, v)
            for k, v in (
                ("p_mw", 0.0),
                ("q_mvar", 0.0),
                ("v_set_pu", 1.0),
                ("rated_mva", 0.0),
                ("in_service", True),
            )
        }
        super().__init__(
            name=name, bus=bus, inverter_type=InverterType.MMC, **parent_kwargs
        )
        self.arm_count = kwargs.get("arm_count", 10)
        self.sub_module_count = kwargs.get("sub_module_count", 200)
        self.dc_voltage_kv = kwargs.get("dc_voltage_kv", 0.0)

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d.update(
            {
                k: getattr(self, k)
                for k in ("arm_count", "sub_module_count", "dc_voltage_kv")
            }
        )
        return d

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MMCData:
        return cls(
            bus=data.get("bus", ""),
            name=data.get("name", ""),
            p_mw=float(data.get("p_mw", 0.0)),
            q_mvar=float(data.get("q_mvar", 0.0)),
            v_set_pu=float(data.get("v_set_pu", 1.0)),
            rated_mva=float(data.get("rated_mva", 0.0)),
            arm_count=int(data.get("arm_count", 10)),
            sub_module_count=int(data.get("sub_module_count", 200)),
            dc_voltage_kv=float(data.get("dc_voltage_kv", 0.0)),
            in_service=bool(data.get("in_service", True)),
        )


@dataclass
class BusData:
    """
    Standardized bus (node) data.

    Covers the essential electrical and topological attributes
    of a power system bus, independent of any specific engine format.
    """

    name: str = ""
    voltage_kv: float = 0.0
    bus_type: BusType = BusType.PQ
    voltage_pu: Optional[float] = None
    angle_deg: float = 0.0
    load_mw: float = 0.0
    load_mvar: float = 0.0
    generation_mw: float = 0.0
    generation_mvar: float = 0.0
    v_min_pu: float = 0.95
    v_max_pu: float = 1.05
    zone: Optional[int] = None
    area: Optional[int] = None
    engine_id: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            k: (v.value if isinstance(v, Enum) else v)
            for k, v in (
                (f, getattr(self, f))
                for f in (
                    "name",
                    "voltage_kv",
                    "bus_type",
                    "voltage_pu",
                    "angle_deg",
                    "load_mw",
                    "load_mvar",
                    "generation_mw",
                    "generation_mvar",
                    "v_min_pu",
                    "v_max_pu",
                    "zone",
                    "area",
                    "engine_id",
                )
            )
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> BusData:
        """Create from dictionary, normalizing field names."""
        bus_type = data.get("bus_type", "pq")
        if isinstance(bus_type, str):
            bus_type = BusType(bus_type)
        return cls(
            name=data.get("name", ""),
            voltage_kv=float(data.get("voltage_kv", data.get("vn_kv", 0.0))),
            bus_type=bus_type,
            voltage_pu=_optional_float(data.get("voltage_pu", data.get("vm_pu"))),
            angle_deg=float(data.get("angle_deg", data.get("va_degree", 0.0))),
            load_mw=float(data.get("load_mw", data.get("p_mw", 0.0))),
            load_mvar=float(data.get("load_mvar", data.get("q_mvar", 0.0))),
            generation_mw=float(data.get("generation_mw", 0.0)),
            generation_mvar=float(data.get("generation_mvar", 0.0)),
            v_min_pu=float(data.get("v_min_pu", data.get("min_vm_pu", 0.95))),
            v_max_pu=float(data.get("v_max_pu", data.get("max_vm_pu", 1.05))),
            zone=data.get("zone"),
            area=data.get("area"),
            engine_id=data.get("engine_id", data.get("bus_id")),
        )

    @property
    def is_slack(self) -> bool:
        """Check if this is a slack bus."""
        return self.bus_type == BusType.SLACK

    @property
    def is_pv(self) -> bool:
        """Check if this is a PV bus."""
        return self.bus_type == BusType.PV

    @property
    def voltage_within_limits(self) -> bool:
        """Check if voltage is within acceptable limits."""
        if self.voltage_pu is None:
            return True
        return self.v_min_pu <= self.voltage_pu <= self.v_max_pu


@dataclass
class BranchData:
    """
    Standardized branch (line/transformer) data.

    Covers the essential electrical parameters of a branch element
    connecting two buses in the network.
    """

    name: str = ""
    from_bus: str = ""
    to_bus: str = ""
    branch_type: BranchType = BranchType.LINE
    resistance_pu: float = 0.0
    reactance_pu: float = 0.0
    susceptance_pu: float = 0.0
    rating_mva: Optional[float] = None
    loading_pct: Optional[float] = None
    p_from_mw: Optional[float] = None
    q_from_mvar: Optional[float] = None
    p_to_mw: Optional[float] = None
    q_to_mvar: Optional[float] = None
    power_loss_mw: Optional[float] = None
    reactive_loss_mvar: Optional[float] = None
    tap_ratio: float = 1.0
    phase_shift_deg: float = 0.0
    vector_group: Optional[str] = None
    winding1_kv: Optional[float] = None
    winding2_kv: Optional[float] = None
    no_load_current_pct: Optional[float] = None
    no_load_loss_kw: Optional[float] = None
    load_loss_kw: Optional[float] = None
    impedance_voltage_pct: Optional[float] = None
    r0_pu: Optional[float] = None
    x0_pu: Optional[float] = None
    r1_pu: Optional[float] = None
    x1_pu: Optional[float] = None
    in_service: bool = True
    engine_id: Optional[int] = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            k: (v.value if isinstance(v, Enum) else v)
            for k, v in (
                (f, getattr(self, f))
                for f in (
                    "name",
                    "from_bus",
                    "to_bus",
                    "branch_type",
                    "resistance_pu",
                    "reactance_pu",
                    "susceptance_pu",
                    "rating_mva",
                    "loading_pct",
                    "p_from_mw",
                    "q_from_mvar",
                    "p_to_mw",
                    "q_to_mvar",
                    "power_loss_mw",
                    "reactive_loss_mvar",
                    "tap_ratio",
                    "phase_shift_deg",
                    "vector_group",
                    "winding1_kv",
                    "winding2_kv",
                    "no_load_current_pct",
                    "no_load_loss_kw",
                    "load_loss_kw",
                    "impedance_voltage_pct",
                    "r0_pu",
                    "x0_pu",
                    "r1_pu",
                    "x1_pu",
                    "in_service",
                    "engine_id",
                )
            )
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> BranchData:
        """Create from dictionary, normalizing field names."""
        branch_type = data.get("branch_type", "line")
        if isinstance(branch_type, str):
            branch_type = BranchType(branch_type)
        return cls(
            name=data.get("name", ""),
            from_bus=data.get("from_bus", ""),
            to_bus=data.get("to_bus", ""),
            branch_type=branch_type,
            resistance_pu=float(
                data.get(
                    "resistance_pu", data.get("r_pu", data.get("r_ohm_per_km", 0.0))
                )
            ),
            reactance_pu=float(
                data.get(
                    "reactance_pu", data.get("x_pu", data.get("x_ohm_per_km", 0.0))
                )
            ),
            susceptance_pu=float(
                data.get(
                    "susceptance_pu", data.get("b_pu", data.get("c_nf_per_km", 0.0))
                )
            ),
            rating_mva=_optional_float(data.get("rating_mva", data.get("max_i_ka"))),
            loading_pct=_optional_float(
                data.get("loading_pct", data.get("loading_percent"))
            ),
            p_from_mw=_optional_float(data.get("p_from_mw")),
            q_from_mvar=_optional_float(data.get("q_from_mvar")),
            p_to_mw=_optional_float(data.get("p_to_mw")),
            q_to_mvar=_optional_float(data.get("q_to_mvar")),
            power_loss_mw=_optional_float(data.get("power_loss_mw", data.get("pl_mw"))),
            reactive_loss_mvar=_optional_float(
                data.get("reactive_loss_mvar", data.get("ql_mvar"))
            ),
            tap_ratio=float(data.get("tap_ratio", data.get("tap_pos", 1.0))),
            phase_shift_deg=float(
                data.get("phase_shift_deg", data.get("shift_degree", 0.0))
            ),
            vector_group=data.get("vector_group"),
            winding1_kv=_optional_float(data.get("winding1_kv", data.get("v1"))),
            winding2_kv=_optional_float(data.get("winding2_kv", data.get("v2"))),
            no_load_current_pct=_optional_float(data.get("no_load_current_pct")),
            no_load_loss_kw=_optional_float(data.get("no_load_loss_kw")),
            load_loss_kw=_optional_float(data.get("load_loss_kw")),
            impedance_voltage_pct=_optional_float(data.get("impedance_voltage_pct")),
            r0_pu=_optional_float(data.get("r0_pu")),
            x0_pu=_optional_float(data.get("x0_pu")),
            r1_pu=_optional_float(data.get("r1_pu")),
            x1_pu=_optional_float(data.get("x1_pu")),
            in_service=bool(data.get("in_service", True)),
            engine_id=data.get("engine_id"),
        )

    @property
    def impedance_magnitude_pu(self) -> float:
        """Calculate impedance magnitude in per-unit."""
        return (self.resistance_pu**2 + self.reactance_pu**2) ** 0.5

    @property
    def is_overloaded(self) -> bool:
        """Check if branch loading exceeds rating."""
        if self.loading_pct is None:
            return False
        return self.loading_pct > 100.0

    @property
    def computed_loss_mw(self) -> float | None:
        """Compute loss from power flow results."""
        if self.p_from_mw is not None and self.p_to_mw is not None:
            return abs(self.p_from_mw - self.p_to_mw)
        return None


@dataclass
class GeneratorData:
    """
    Standardized generator data.

    Covers the essential electrical parameters of a generator
    connected to a specific bus in the network.
    """

    name: str = ""
    bus: str = ""
    generator_type: GeneratorType = GeneratorType.SYNCHRONOUS
    p_mw: float = 0.0
    v_set_pu: float = 1.0
    p_min_mw: Optional[float] = None
    p_max_mw: Optional[float] = None
    q_min_mvar: Optional[float] = None
    q_max_mvar: Optional[float] = None
    q_mvar: Optional[float] = None
    voltage_pu: Optional[float] = None
    in_service: bool = True
    h_seconds: Optional[float] = None
    d_percent: Optional[float] = None
    xd_pu: Optional[float] = None
    xq_pu: Optional[float] = None
    xd_tr_pu: Optional[float] = None
    xq_tr_pu: Optional[float] = None
    xd_ss_pu: Optional[float] = None
    xq_ss_pu: Optional[float] = None
    ra_pu: Optional[float] = None
    td0_seconds: Optional[float] = None
    tq0_seconds: Optional[float] = None
    exciter_type: Optional[str] = None
    exciter_params: Optional[dict] = None
    governor_type: Optional[str] = None
    governor_params: Optional[dict] = None
    pss_type: Optional[str] = None
    pss_params: Optional[dict] = None
    engine_id: Optional[int] = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            k: (v.value if isinstance(v, Enum) else v)
            for k, v in (
                (f, getattr(self, f))
                for f in (
                    "name",
                    "bus",
                    "generator_type",
                    "p_mw",
                    "v_set_pu",
                    "p_min_mw",
                    "p_max_mw",
                    "q_min_mvar",
                    "q_max_mvar",
                    "q_mvar",
                    "voltage_pu",
                    "in_service",
                    "h_seconds",
                    "d_percent",
                    "xd_pu",
                    "xq_pu",
                    "xd_tr_pu",
                    "xq_tr_pu",
                    "xd_ss_pu",
                    "xq_ss_pu",
                    "ra_pu",
                    "td0_seconds",
                    "tq0_seconds",
                    "exciter_type",
                    "exciter_params",
                    "governor_type",
                    "governor_params",
                    "pss_type",
                    "pss_params",
                    "engine_id",
                )
            )
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GeneratorData:
        """Create from dictionary, normalizing field names."""
        gen_type = data.get("generator_type", "synchronous")
        if isinstance(gen_type, str):
            gen_type = GeneratorType(gen_type)
        return cls(
            name=data.get("name", ""),
            bus=data.get("bus", ""),
            generator_type=gen_type,
            p_mw=float(data.get("p_mw", 0.0)),
            v_set_pu=float(data.get("v_set_pu", data.get("vm_pu", 1.0))),
            p_min_mw=_optional_float(data.get("p_min_mw", data.get("min_p_mw"))),
            p_max_mw=_optional_float(data.get("p_max_mw", data.get("max_p_mw"))),
            q_min_mvar=_optional_float(data.get("q_min_mvar", data.get("min_q_mvar"))),
            q_max_mvar=_optional_float(data.get("q_max_mvar", data.get("max_q_mvar"))),
            q_mvar=_optional_float(data.get("q_mvar")),
            voltage_pu=_optional_float(data.get("voltage_pu")),
            in_service=bool(data.get("in_service", True)),
            h_seconds=_optional_float(data.get("h_seconds", data.get("sn_mva"))),
            d_percent=_optional_float(data.get("d_percent")),
            xd_pu=_optional_float(data.get("xd_pu")),
            xq_pu=_optional_float(data.get("xq_pu")),
            xd_tr_pu=_optional_float(data.get("xd_tr_pu", data.get("xdash_pu"))),
            xq_tr_pu=_optional_float(data.get("xq_tr_pu")),
            xd_ss_pu=_optional_float(data.get("xd_ss_pu")),
            xq_ss_pu=_optional_float(data.get("xq_ss_pu")),
            ra_pu=_optional_float(data.get("ra_pu")),
            td0_seconds=_optional_float(data.get("td0_seconds")),
            tq0_seconds=_optional_float(data.get("tq0_seconds")),
            exciter_type=data.get("exciter_type"),
            exciter_params=data.get("exciter_params"),
            governor_type=data.get("governor_type"),
            governor_params=data.get("governor_params"),
            pss_type=data.get("pss_type"),
            pss_params=data.get("pss_params"),
            engine_id=data.get("engine_id"),
        )

    @property
    def capacity_factor(self) -> float | None:
        """Calculate capacity factor (actual/max)."""
        if self.p_max_mw and self.p_max_mw > 0:
            return self.p_mw / self.p_max_mw
        return None

    @property
    def is_within_limits(self) -> bool:
        """Check if generator output is within limits."""
        if (
            self.q_mvar is not None
            and self.q_min_mvar is not None
            and self.q_max_mvar is not None
        ):
            return self.q_min_mvar <= self.q_mvar <= self.q_max_mvar
        return True


@dataclass
class LoadData:
    """
    Standardized load data.

    Covers the essential parameters of a load connected to a bus.
    """

    name: str = ""
    bus: str = ""
    load_type: LoadType = LoadType.CONSTANT_POWER
    p_mw: float = 0.0
    q_mvar: float = 0.0
    p_z_percent: Optional[float] = None
    p_i_percent: Optional[float] = None
    p_p_percent: Optional[float] = 100.0
    q_z_percent: Optional[float] = None
    q_i_percent: Optional[float] = None
    q_p_percent: Optional[float] = None
    frequency_factor: Optional[float] = None
    voltage_factor: Optional[float] = None
    in_service: bool = True
    scaling: float = 1.0
    engine_id: Optional[int] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            k: (v.value if isinstance(v, Enum) else v)
            for k, v in (
                (f, getattr(self, f))
                for f in (
                    "name",
                    "bus",
                    "load_type",
                    "p_mw",
                    "q_mvar",
                    "p_z_percent",
                    "p_i_percent",
                    "p_p_percent",
                    "q_z_percent",
                    "q_i_percent",
                    "q_p_percent",
                    "frequency_factor",
                    "voltage_factor",
                    "in_service",
                    "scaling",
                    "engine_id",
                )
            )
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> LoadData:
        lt = data.get("load_type", "constant_power")
        if isinstance(lt, str):
            lt = LoadType(lt)
        return cls(
            name=data.get("name", ""),
            bus=data.get("bus", ""),
            load_type=lt,
            p_mw=float(data.get("p_mw", 0.0)),
            q_mvar=float(data.get("q_mvar", 0.0)),
            p_z_percent=_optional_float(data.get("p_z_percent")),
            p_i_percent=_optional_float(data.get("p_i_percent")),
            p_p_percent=_optional_float(data.get("p_p_percent", 100.0)),
            q_z_percent=_optional_float(data.get("q_z_percent")),
            q_i_percent=_optional_float(data.get("q_i_percent")),
            q_p_percent=_optional_float(data.get("q_p_percent")),
            frequency_factor=_optional_float(data.get("frequency_factor")),
            voltage_factor=_optional_float(data.get("voltage_factor")),
            in_service=bool(data.get("in_service", True)),
            scaling=float(data.get("scaling", 1.0)),
            engine_id=data.get("engine_id"),
        )


@dataclass
class SwitchData:
    """Standardized switch data."""

    name: str = ""
    from_bus: str = ""
    to_bus: str = ""
    state: SwitchState = SwitchState.CLOSED
    rated_current_ka: Optional[float] = None
    in_service: bool = True
    engine_id: Optional[int] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            k: (v.value if isinstance(v, Enum) else v)
            for k, v in (
                (f, getattr(self, f))
                for f in (
                    "name",
                    "from_bus",
                    "to_bus",
                    "state",
                    "rated_current_ka",
                    "in_service",
                    "engine_id",
                )
            )
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SwitchData:
        state = data.get("state", "closed")
        if isinstance(state, str):
            state = SwitchState(state)
        return cls(
            name=data.get("name", ""),
            from_bus=data.get("from_bus", ""),
            to_bus=data.get("to_bus", ""),
            state=state,
            rated_current_ka=_optional_float(data.get("rated_current_ka")),
            in_service=bool(data.get("in_service", True)),
            engine_id=data.get("engine_id"),
        )


@dataclass
class ShuntData:
    """Standardized shunt compensator data."""

    name: str = ""
    bus: str = ""
    q_mvar: float = 0.0
    step: int = 1
    max_step: int = 1
    in_service: bool = True
    engine_id: Optional[int] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            k: v
            for k, v in (
                (f, getattr(self, f))
                for f in (
                    "name",
                    "bus",
                    "q_mvar",
                    "step",
                    "max_step",
                    "in_service",
                    "engine_id",
                )
            )
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ShuntData:
        return cls(
            name=data.get("name", ""),
            bus=data.get("bus", ""),
            q_mvar=float(data.get("q_mvar", 0.0)),
            step=int(data.get("step", 1)),
            max_step=int(data.get("max_step", 1)),
            in_service=bool(data.get("in_service", True)),
            engine_id=data.get("engine_id"),
        )


@dataclass
class FaultData:
    """Standardized fault data."""

    bus: str = ""
    fault_type: FaultType = FaultType.THREE_PHASE
    r_f_ohm: float = 0.0
    x_f_ohm: float = 0.0
    engine_id: Optional[int] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            k: (v.value if isinstance(v, Enum) else v)
            for k, v in (
                (f, getattr(self, f))
                for f in ("bus", "fault_type", "r_f_ohm", "x_f_ohm", "engine_id")
            )
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> FaultData:
        ft = data.get("fault_type", "3ph")
        if isinstance(ft, str):
            ft = FaultType(ft)
        return cls(
            bus=data.get("bus", ""),
            fault_type=ft,
            r_f_ohm=float(data.get("r_f_ohm", 0.0)),
            x_f_ohm=float(data.get("x_f_ohm", 0.0)),
            engine_id=data.get("engine_id"),
        )


@dataclass
class NetworkSummary:
    """Summary statistics for a power system network."""

    bus_count: int = 0
    branch_count: int = 0
    generator_count: int = 0
    load_count: int = 0
    total_generation_mw: float = 0.0
    total_load_mw: float = 0.0
    total_loss_mw: float = 0.0
    min_voltage_pu: Optional[float] = None
    max_voltage_pu: Optional[float] = None
    max_loading_pct: Optional[float] = None
    converged: Optional[bool] = None

    @classmethod
    def from_results(
        cls,
        buses: list[BusData],
        branches: list[BranchData],
        generators: list[GeneratorData],
        loads: list[LoadData],
        converged: bool = True,
    ) -> NetworkSummary:
        total_gen = sum(g.p_mw for g in generators)
        total_load = sum(l.p_mw for l in loads)
        total_loss = sum(
            b.computed_loss_mw for b in branches if b.computed_loss_mw is not None
        )
        voltages = [b.voltage_pu for b in buses if b.voltage_pu is not None]
        loadings = [b.loading_pct for b in branches if b.loading_pct is not None]
        return cls(
            bus_count=len(buses),
            branch_count=len(branches),
            generator_count=len(generators),
            load_count=len(loads),
            total_generation_mw=total_gen,
            total_load_mw=total_load,
            total_loss_mw=total_loss,
            min_voltage_pu=min(voltages) if voltages else None,
            max_voltage_pu=max(voltages) if voltages else None,
            max_loading_pct=max(loadings) if loadings else None,
            converged=converged,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            k: v
            for k, v in (
                (f, getattr(self, f))
                for f in (
                    "bus_count",
                    "branch_count",
                    "generator_count",
                    "load_count",
                    "total_generation_mw",
                    "total_load_mw",
                    "total_loss_mw",
                    "min_voltage_pu",
                    "max_voltage_pu",
                    "max_loading_pct",
                    "converged",
                )
            )
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> NetworkSummary:
        total_gen_data = data.get("total_generation", {})
        total_load_data = data.get("total_load", {})
        voltage_range = data.get("voltage_range", {})
        if isinstance(total_gen_data, dict):
            total_gen = total_gen_data.get("p_mw", 0.0)
            total_gen_mvar = total_gen_data.get("q_mvar", 0.0)
        else:
            total_gen = float(total_gen_data) if total_gen_data else 0.0
            total_gen_mvar = 0.0
        if isinstance(total_load_data, dict):
            total_load = total_load_data.get("p_mw", 0.0)
            total_load_mvar = total_load_data.get("q_mvar", 0.0)
        else:
            total_load = float(total_load_data) if total_load_data else 0.0
            total_load_mvar = 0.0
        return cls(
            bus_count=int(data.get("bus_count", 0)),
            branch_count=int(data.get("branch_count", 0)),
            generator_count=int(data.get("generator_count", 0)),
            load_count=int(data.get("load_count", 0)),
            total_generation_mw=float(total_gen),
            total_load_mw=float(total_load),
            total_loss_mw=float(data.get("total_loss_mw", 0.0)),
            min_voltage_pu=_optional_float(voltage_range.get("min_pu") if isinstance(voltage_range, dict) else data.get("min_voltage_pu")),
            max_voltage_pu=_optional_float(voltage_range.get("max_pu") if isinstance(voltage_range, dict) else data.get("max_voltage_pu")),
            max_loading_pct=_optional_float(data.get("max_loading_pct")),
            converged=data.get("converged"),
        )


@dataclass
class RenewableData:
    """Base class for renewable energy source data."""

    name: str = ""
    bus: str = ""
    renewable_type: RenewableType = RenewableType.PV_STATION
    p_mw: float = 0.0
    q_mvar: float = 0.0
    v_set_pu: float = 1.0
    in_service: bool = True
    engine_id: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            k: (v.value if isinstance(v, Enum) else v)
            for k, v in (
                (f, getattr(self, f))
                for f in (
                    "name",
                    "bus",
                    "renewable_type",
                    "p_mw",
                    "q_mvar",
                    "v_set_pu",
                    "in_service",
                    "engine_id",
                )
            )
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> RenewableData:
        rt = data.get("renewable_type", "pv_station")
        if isinstance(rt, str):
            rt = RenewableType(rt)
        return cls(
            name=data.get("name", ""),
            bus=data.get("bus", ""),
            renewable_type=rt,
            p_mw=float(data.get("p_mw", 0.0)),
            q_mvar=float(data.get("q_mvar", 0.0)),
            v_set_pu=float(data.get("v_set_pu", 1.0)),
            in_service=bool(data.get("in_service", True)),
            engine_id=data.get("engine_id"),
        )


@dataclass
class PVStationData(RenewableData):
    """Photovoltaic station data."""

    capacity_mwp: float = 0.0
    irradiance_kw_m2: float = 0.0
    efficiency_pct: float = 100.0

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d.update(
            {
                k: getattr(self, k)
                for k in ("capacity_mwp", "irradiance_kw_m2", "efficiency_pct")
            }
        )
        return d

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PVStationData:
        rt = data.get("renewable_type", "pv_station")
        if isinstance(rt, str):
            rt = RenewableType(rt)
        return cls(
            name=data.get("name", ""),
            bus=data.get("bus", ""),
            renewable_type=rt,
            p_mw=float(data.get("p_mw", 0.0)),
            q_mvar=float(data.get("q_mvar", 0.0)),
            v_set_pu=float(data.get("v_set_pu", 1.0)),
            capacity_mwp=float(data.get("capacity_mwp", 0.0)),
            irradiance_kw_m2=float(data.get("irradiance_kw_m2", 0.0)),
            efficiency_pct=float(data.get("efficiency_pct", 100.0)),
            in_service=bool(data.get("in_service", True)),
            engine_id=data.get("engine_id"),
        )


@dataclass
class WGSourceData(RenewableData):
    """Wind generator source data."""

    rated_power_mw: float = 0.0
    wind_speed_m_s: float = 0.0
    cut_in_speed: float = 3.0
    cut_out_speed: float = 25.0
    rated_speed: float = 12.0

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d.update(
            {
                k: getattr(self, k)
                for k in (
                    "rated_power_mw",
                    "wind_speed_m_s",
                    "cut_in_speed",
                    "cut_out_speed",
                    "rated_speed",
                )
            }
        )
        return d

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> WGSourceData:
        rt = data.get("renewable_type", "wind_farm")
        if isinstance(rt, str):
            rt = RenewableType(rt)
        return cls(
            name=data.get("name", ""),
            bus=data.get("bus", ""),
            renewable_type=rt,
            p_mw=float(data.get("p_mw", 0.0)),
            q_mvar=float(data.get("q_mvar", 0.0)),
            v_set_pu=float(data.get("v_set_pu", 1.0)),
            rated_power_mw=float(data.get("rated_power_mw", 0.0)),
            wind_speed_m_s=float(data.get("wind_speed_m_s", 0.0)),
            cut_in_speed=float(data.get("cut_in_speed", 3.0)),
            cut_out_speed=float(data.get("cut_out_speed", 25.0)),
            rated_speed=float(data.get("rated_speed", 12.0)),
            in_service=bool(data.get("in_service", True)),
            engine_id=data.get("engine_id"),
        )


@dataclass
class BatteryData(RenewableData):
    """Battery energy storage data."""

    capacity_mwh: float = 0.0
    soc_pct: float = 50.0
    max_charge_mw: float = 0.0
    max_discharge_mw: float = 0.0
    efficiency_pct: float = 90.0

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d.update(
            {
                k: getattr(self, k)
                for k in (
                    "capacity_mwh",
                    "soc_pct",
                    "max_charge_mw",
                    "max_discharge_mw",
                    "efficiency_pct",
                )
            }
        )
        return d

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> BatteryData:
        rt = data.get("renewable_type", "battery")
        if isinstance(rt, str):
            rt = RenewableType(rt)
        return cls(
            name=data.get("name", ""),
            bus=data.get("bus", ""),
            renewable_type=rt,
            p_mw=float(data.get("p_mw", 0.0)),
            q_mvar=float(data.get("q_mvar", 0.0)),
            v_set_pu=float(data.get("v_set_pu", 1.0)),
            capacity_mwh=float(data.get("capacity_mwh", 0.0)),
            soc_pct=float(data.get("soc_pct", 50.0)),
            max_charge_mw=float(data.get("max_charge_mw", 0.0)),
            max_discharge_mw=float(data.get("max_discharge_mw", 0.0)),
            efficiency_pct=float(data.get("efficiency_pct", 90.0)),
            in_service=bool(data.get("in_service", True)),
            engine_id=data.get("engine_id"),
        )


@dataclass
class DynamicModelData:
    """Base class for dynamic model data (exciter, governor, etc.)."""

    name: str = ""
    generator_name: str = ""
    model_type: DynamicModelType = DynamicModelType.EXCITER
    parameters: dict[str, Any] = field(default_factory=dict)
    engine_id: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            k: (v.value if isinstance(v, Enum) else v)
            for k, v in (
                (f, getattr(self, f))
                for f in (
                    "name",
                    "generator_name",
                    "model_type",
                    "parameters",
                    "engine_id",
                )
            )
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DynamicModelData:
        mt = data.get("model_type", "exciter")
        if isinstance(mt, str):
            mt = DynamicModelType(mt)
        return cls(
            name=data.get("name", ""),
            generator_name=data.get("generator_name", ""),
            model_type=mt,
            parameters=data.get("parameters", {}),
            engine_id=data.get("engine_id"),
        )


@dataclass
class ExciterData(DynamicModelData):
    """Exciter dynamic model data."""

    ka: float = 0.0
    ta: float = 0.0
    vr_max: float = 0.0
    vr_min: float = 0.0

    def __post_init__(self):
        self.model_type = DynamicModelType.EXCITER

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d.update({k: getattr(self, k) for k in ("ka", "ta", "vr_max", "vr_min")})
        return d

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ExciterData:
        return cls(
            name=data.get("name", ""),
            generator_name=data.get("generator_name", ""),
            ka=float(data.get("ka", 0.0)),
            ta=float(data.get("ta", 0.0)),
            vr_max=float(data.get("vr_max", 0.0)),
            vr_min=float(data.get("vr_min", 0.0)),
            parameters=data.get("parameters", {}),
            engine_id=data.get("engine_id"),
        )


@dataclass
class GovernorData(DynamicModelData):
    """Governor dynamic model data."""

    droop: float = 0.05
    tg: float = 0.0
    p_max: float = 0.0
    p_min: float = 0.0

    def __post_init__(self):
        self.model_type = DynamicModelType.GOVERNOR

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d.update({k: getattr(self, k) for k in ("droop", "tg", "p_max", "p_min")})
        return d

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GovernorData:
        return cls(
            name=data.get("name", ""),
            generator_name=data.get("generator_name", ""),
            droop=float(data.get("droop", 0.05)),
            tg=float(data.get("tg", 0.0)),
            p_max=float(data.get("p_max", 0.0)),
            p_min=float(data.get("p_min", 0.0)),
            parameters=data.get("parameters", {}),
            engine_id=data.get("engine_id"),
        )


@dataclass
class TurbineData(DynamicModelData):
    """Turbine dynamic model data."""

    t1: float = 0.0
    t2: float = 0.0
    t3: float = 0.0

    def __post_init__(self):
        self.model_type = DynamicModelType.TURBINE

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d.update({k: getattr(self, k) for k in ("t1", "t2", "t3")})
        return d

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TurbineData:
        return cls(
            name=data.get("name", ""),
            generator_name=data.get("generator_name", ""),
            t1=float(data.get("t1", 0.0)),
            t2=float(data.get("t2", 0.0)),
            t3=float(data.get("t3", 0.0)),
            parameters=data.get("parameters", {}),
            engine_id=data.get("engine_id"),
        )


@dataclass
class PSSData(DynamicModelData):
    """Power System Stabilizer data."""

    kstab: float = 0.0
    tw: float = 0.0
    t1: float = 0.0
    t2: float = 0.0
    t3: float = 0.0
    t4: float = 0.0

    def __post_init__(self):
        self.model_type = DynamicModelType.PSS

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d.update({k: getattr(self, k) for k in ("kstab", "tw", "t1", "t2", "t3", "t4")})
        return d

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PSSData:
        return cls(
            name=data.get("name", ""),
            generator_name=data.get("generator_name", ""),
            kstab=float(data.get("kstab", 0.0)),
            tw=float(data.get("tw", 0.0)),
            t1=float(data.get("t1", 0.0)),
            t2=float(data.get("t2", 0.0)),
            t3=float(data.get("t3", 0.0)),
            t4=float(data.get("t4", 0.0)),
            parameters=data.get("parameters", {}),
            engine_id=data.get("engine_id"),
        )


@dataclass
class HVDCData:
    """Base class for HVDC transmission data."""

    name: str = ""
    from_bus: str = ""
    to_bus: str = ""
    hvdc_type: HVDCType = HVDCType.VSC
    p_mw: float = 0.0
    q_mvar: float = 0.0
    rated_mw: float = 0.0
    in_service: bool = True
    engine_id: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            k: (v.value if isinstance(v, Enum) else v)
            for k, v in (
                (f, getattr(self, f))
                for f in (
                    "name",
                    "from_bus",
                    "to_bus",
                    "hvdc_type",
                    "p_mw",
                    "q_mvar",
                    "rated_mw",
                    "in_service",
                    "engine_id",
                )
            )
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> HVDCData:
        ht = data.get("hvdc_type", "vsc")
        if isinstance(ht, str):
            ht = HVDCType(ht)
        return cls(
            name=data.get("name", ""),
            from_bus=data.get("from_bus", ""),
            to_bus=data.get("to_bus", ""),
            hvdc_type=ht,
            p_mw=float(data.get("p_mw", 0.0)),
            q_mvar=float(data.get("q_mvar", 0.0)),
            rated_mw=float(data.get("rated_mw", 0.0)),
            in_service=bool(data.get("in_service", True)),
            engine_id=data.get("engine_id"),
        )


@dataclass
class VSC_HVDCData(HVDCData):
    """VSC-HVDC transmission data."""

    dc_voltage_kv: float = 0.0
    converter_mva: float = 0.0
    control_mode: str = ""
    droop_pct: float = 0.0

    def __post_init__(self):
        self.hvdc_type = HVDCType.VSC

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d.update(
            {
                k: getattr(self, k)
                for k in ("dc_voltage_kv", "converter_mva", "control_mode", "droop_pct")
            }
        )
        return d

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> VSC_HVDCData:
        ht = data.get("hvdc_type", "vsc")
        if isinstance(ht, str):
            ht = HVDCType(ht)
        return cls(
            name=data.get("name", ""),
            from_bus=data.get("from_bus", ""),
            to_bus=data.get("to_bus", ""),
            hvdc_type=ht,
            p_mw=float(data.get("p_mw", 0.0)),
            q_mvar=float(data.get("q_mvar", 0.0)),
            rated_mw=float(data.get("rated_mw", 0.0)),
            dc_voltage_kv=float(data.get("dc_voltage_kv", 0.0)),
            converter_mva=float(data.get("converter_mva", 0.0)),
            control_mode=data.get("control_mode", ""),
            droop_pct=float(data.get("droop_pct", 0.0)),
            in_service=bool(data.get("in_service", True)),
            engine_id=data.get("engine_id"),
        )


__all__ = (
    "BusType",
    "BranchType",
    "GeneratorType",
    "FaultType",
    "LoadType",
    "SwitchState",
    "RenewableType",
    "InverterType",
    "DynamicModelType",
    "HVDCType",
    "BusData",
    "BranchData",
    "GeneratorData",
    "LoadData",
    "FaultData",
    "NetworkSummary",
    "PowerElectronicsData",
    "SVGData",
    "SVCData",
    "MMCData",
    "RenewableData",
    "PVStationData",
    "WGSourceData",
    "BatteryData",
    "DynamicModelData",
    "ExciterData",
    "GovernorData",
    "TurbineData",
    "PSSData",
    "HVDCData",
    "VSC_HVDCData",
    "SwitchData",
    "ShuntData",
    "_optional_float",
)
