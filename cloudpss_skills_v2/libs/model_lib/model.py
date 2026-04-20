"""
ModelLib - Power System Model Abstraction and Conversion

Provides an engine-agnostic representation of power system models
and converters for cross-engine model translation.

Architecture role:
    CloudPSS Model <-> ModelLib <-> pandapower Net
                        |
                    DataLib (unified format)
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from cloudpss_skills_v2.libs.data_lib import (
    BranchData,
    BusData,
    FaultData,
    GeneratorData,
    LoadData,
    NetworkSummary,
    ShuntData,
    SwitchData,
    SwitchState,
)


class ConversionMode(Enum):
    LOSSLESS = "lossless"
    APPROXIMATE = "approximate"
    SEMANTIC = "semantic"


class ConversionQuality(Enum):
    EXACT = "exact"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    PARTIAL = "partial"


@dataclass
class ConversionReport:
    source_engine: str = ""
    target_engine: str = ""
    mode: ConversionMode = ConversionMode.LOSSLESS
    quality: ConversionQuality = ConversionQuality.MEDIUM
    items_converted: int = 0
    items_skipped: int = 0
    items_approximated: int = 0
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def is_success(self) -> bool:
        return len(self.errors) == 0

    def to_dict(self) -> dict[str, Any]:
        return {
            k: (v.value if isinstance(v, Enum) else v)
            for k, v in (
                (f, getattr(self, f))
                for f in (
                    "source_engine",
                    "target_engine",
                    "mode",
                    "quality",
                    "items_converted",
                    "items_skipped",
                    "items_approximated",
                    "warnings",
                    "errors",
                )
            )
        }


@dataclass
class PowerSystemModel:
    name: str = ""
    base_mva: float = 100.0
    frequency_hz: float = 50.0
    buses: list[BusData] = field(default_factory=list)
    branches: list[BranchData] = field(default_factory=list)
    generators: list[GeneratorData] = field(default_factory=list)
    loads: list[LoadData] = field(default_factory=list)
    switches: list[SwitchData] = field(default_factory=list)
    shunts: list[ShuntData] = field(default_factory=list)
    faults: list[FaultData] = field(default_factory=list)
    source_engine: str | None = None
    source_id: str | None = None

    def get_bus_by_name(self, name: str) -> BusData | None:
        for bus in self.buses:
            if bus.name == name:
                return bus
        return None

    def get_branch_by_name(self, name: str) -> BranchData | None:
        for branch in self.branches:
            if branch.name == name:
                return branch
        return None

    def get_generators_at_bus(self, bus_name: str) -> list[GeneratorData]:
        return [g for g in self.generators if g.bus == bus_name]

    def get_loads_at_bus(self, bus_name: str) -> list[LoadData]:
        return [l for l in self.loads if l.bus == bus_name]

    def get_connected_branches(self, bus_name: str) -> list[BranchData]:
        return [
            b for b in self.branches if b.from_bus == bus_name or b.to_bus == bus_name
        ]

    @property
    def slack_buses(self) -> list[BusData]:
        from cloudpss_skills_v2.libs.data_lib import BusType

        return [b for b in self.buses if b.bus_type == BusType.SLACK]

    @property
    def bus_count(self) -> int:
        return len(self.buses)

    @property
    def branch_count(self) -> int:
        return len(self.branches)

    @property
    def total_generation_mw(self) -> float:
        return sum(g.p_mw for g in self.generators)

    @property
    def total_load_mw(self) -> float:
        return sum(l.p_mw for l in self.loads)

    @property
    def summary(self, converged: bool = True) -> NetworkSummary:
        return NetworkSummary.from_results(
            self.buses, self.branches, self.generators, self.loads, converged
        )

    def validate_topology(self) -> list[str]:
        errors = []
        if not self.buses:
            errors.append("Model has no buses")
            return errors
        if not self.slack_buses:
            errors.append("Model has no slack bus")
        bus_names = {b.name for b in self.buses}
        for branch in self.branches:
            if branch.from_bus not in bus_names:
                errors.append(
                    f"Branch '{branch.name}': from_bus '{branch.from_bus}' not found"
                )
            if branch.to_bus not in bus_names:
                errors.append(
                    f"Branch '{branch.name}': to_bus '{branch.to_bus}' not found"
                )
        for gen in self.generators:
            if gen.bus not in bus_names:
                errors.append(f"Generator '{gen.name}': bus '{gen.bus}' not found")
        for load in self.loads:
            if load.bus not in bus_names:
                errors.append(f"Load '{load.name}': bus '{load.bus}' not found")
        return errors

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "base_mva": self.base_mva,
            "frequency_hz": self.frequency_hz,
            "buses": [b.to_dict() for b in self.buses],
            "branches": [b.to_dict() for b in self.branches],
            "generators": [g.to_dict() for g in self.generators],
            "loads": [l.to_dict() for l in self.loads],
            "source_engine": self.source_engine,
            "source_id": self.source_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PowerSystemModel:
        buses = [BusData.from_dict(b) for b in data.get("buses", [])]
        branches = [BranchData.from_dict(b) for b in data.get("branches", [])]
        generators = [GeneratorData.from_dict(g) for g in data.get("generators", [])]
        loads = [LoadData.from_dict(l) for l in data.get("loads", [])]
        return cls(
            name=data.get("name", ""),
            base_mva=float(data.get("base_mva", data.get("sn_mva", 100.0))),
            frequency_hz=float(data.get("frequency_hz", data.get("f_hz", 50.0))),
            buses=buses,
            branches=branches,
            generators=generators,
            loads=loads,
            source_engine=data.get("source_engine"),
            source_id=data.get("source_id"),
        )


class ModelConverter(ABC):
    @property
    @abstractmethod
    def source_engine(self) -> str: ...

    @property
    @abstractmethod
    def target_engine(self) -> str: ...

    @abstractmethod
    def convert_to_model(
        self, source: Any, mode: ConversionMode = ConversionMode.APPROXIMATE
    ) -> tuple[PowerSystemModel, ConversionReport]: ...

    @abstractmethod
    def convert_from_model(
        self, model: PowerSystemModel, mode: ConversionMode = ConversionMode.APPROXIMATE
    ) -> tuple[Any, ConversionReport]: ...


class DictModelConverter(ModelConverter):
    @property
    def source_engine(self) -> str:
        return "dict"

    @property
    def target_engine(self) -> str:
        return "dict"

    def convert_to_model(
        self, source: dict[str, Any], mode: ConversionMode = ConversionMode.APPROXIMATE
    ) -> tuple[PowerSystemModel, ConversionReport]:
        report = ConversionReport(
            source_engine="dict",
            target_engine="model",
            mode=mode,
            quality=ConversionQuality.EXACT,
        )
        model = PowerSystemModel.from_dict(source)
        report.items_converted = (
            len(model.buses)
            + len(model.branches)
            + len(model.generators)
            + len(model.loads)
        )
        return (model, report)

    def convert_from_model(
        self, model: PowerSystemModel, mode: ConversionMode = ConversionMode.APPROXIMATE
    ) -> tuple[dict[str, Any], ConversionReport]:
        report = ConversionReport(
            source_engine="model",
            target_engine="dict",
            mode=mode,
            quality=ConversionQuality.EXACT,
        )
        result = model.to_dict()
        report.items_converted = (
            len(model.buses)
            + len(model.branches)
            + len(model.generators)
            + len(model.loads)
        )
        return (result, report)


class PandapowerModelConverter(ModelConverter):
    @property
    def source_engine(self) -> str:
        return "pandapower"

    @property
    def target_engine(self) -> str:
        return "pandapower"

    def convert_to_model(
        self, source: Any, mode: ConversionMode = ConversionMode.APPROXIMATE
    ) -> tuple[PowerSystemModel, ConversionReport]:
        import pandapower as pp

        report = ConversionReport(
            source_engine="pandapower", target_engine="model", mode=mode
        )
        net = source
        buses = []
        for idx, row in net.bus.iterrows():
            bus_type_val = "pq"
            vm_pu = None
            if (
                hasattr(net, "res_bus")
                and not net.res_bus.empty
                and idx in net.res_bus.index
            ):
                vm_pu = net.res_bus.at[idx, "vm_pu"]
            buses.append(
                BusData(
                    name=str(row.get("name", f"Bus_{idx}")),
                    voltage_kv=float(row.get("vn_kv", 0)),
                    bus_type=BusType(bus_type_val),
                    voltage_pu=vm_pu,
                    engine_id=idx,
                )
            )
        branches = []
        for idx, row in net.line.iterrows():
            loading = None
            if (
                hasattr(net, "res_line")
                and not net.res_line.empty
                and idx in net.res_line.index
            ):
                loading = net.res_line.at[idx, "loading_percent"]
            branches.append(
                BranchData(
                    name=str(row.get("name", f"Line_{idx}")),
                    from_bus=str(row.get("from_bus", "")),
                    to_bus=str(row.get("to_bus", "")),
                    resistance_pu=float(
                        row.get("r_ohm_per_km", 0) * row.get("length_km", 1)
                    ),
                    reactance_pu=float(
                        row.get("x_ohm_per_km", 0) * row.get("length_km", 1)
                    ),
                    loading_pct=loading,
                    engine_id=idx,
                )
            )
        generators = []
        for idx, row in net.gen.iterrows():
            generators.append(
                GeneratorData(
                    name=str(row.get("name", f"Gen_{idx}")),
                    bus=str(row.get("bus", "")),
                    p_mw=float(row.get("p_mw", 0)),
                    v_set_pu=float(row.get("vm_pu", 1)),
                    engine_id=idx,
                )
            )
        if hasattr(net, "ext_grid") and not net.ext_grid.empty:
            for idx, row in net.ext_grid.iterrows():
                generators.append(
                    GeneratorData(
                        name=str(row.get("name", f"ExtGrid_{idx}")),
                        bus=str(row.get("bus", "")),
                        generator_type=GeneratorType.EXTERNAL_GRID,
                        v_set_pu=float(row.get("vm_pu", 1)),
                        engine_id=idx,
                    )
                )
        loads_list = []
        for idx, row in net.load.iterrows():
            loads_list.append(
                LoadData(
                    name=str(row.get("name", f"Load_{idx}")),
                    bus=str(row.get("bus", "")),
                    p_mw=float(row.get("p_mw", 0)),
                    q_mvar=float(row.get("q_mvar", 0)),
                    engine_id=idx,
                )
            )
        switches = []
        if hasattr(net, "switch") and not net.switch.empty:
            for idx, row in net.switch.iterrows():
                state = "closed" if row.get("closed", True) else "open"
                switches.append(
                    SwitchData(
                        name=str(row.get("name", f"Switch_{idx}")),
                        from_bus=str(row.get("bus", "")),
                        to_bus=str(row.get("element", "")),
                        state=SwitchState(state),
                        rated_current_ka=row.get("rated_current", None),
                        in_service=row.get("in_service", True),
                        engine_id=idx,
                    )
                )
        shunts = []
        if hasattr(net, "shunt") and not net.shunt.empty:
            for idx, row in net.shunt.iterrows():
                shunts.append(
                    ShuntData(
                        name=str(row.get("name", f"Shunt_{idx}")),
                        bus=str(row.get("bus", "")),
                        q_mvar=float(row.get("q_mvar", 0)),
                        step=int(row.get("step", 1)),
                        max_step=int(row.get("max_step", 1)),
                        in_service=row.get("in_service", True),
                        engine_id=idx,
                    )
                )
        model = PowerSystemModel(
            name=net.name if hasattr(net, "name") else "",
            base_mva=float(net.sn_mva if hasattr(net, "sn_mva") else 100),
            frequency_hz=float(net.f_hz if hasattr(net, "f_hz") else 50),
            buses=buses,
            branches=branches,
            generators=generators,
            loads=loads_list,
            switches=switches,
            shunts=shunts,
            source_engine="pandapower",
        )
        report.items_converted = (
            len(buses)
            + len(branches)
            + len(generators)
            + len(loads_list)
            + len(switches)
            + len(shunts)
        )
        report.quality = ConversionQuality.HIGH
        return (model, report)

    def convert_from_model(
        self, model: PowerSystemModel, mode: ConversionMode = ConversionMode.APPROXIMATE
    ) -> tuple[Any, ConversionReport]:
        import pandapower as pp

        report = ConversionReport(
            source_engine="model", target_engine="pandapower", mode=mode
        )
        net = pp.create_empty_network(
            sn_mva=model.base_mva, f_hz=model.frequency_hz, name=model.name
        )
        bus_index_map = {}
        for bus in model.buses:
            bus_idx = pp.create_bus(net, vn_kv=bus.voltage_kv, name=bus.name)
            bus_index_map[bus.name] = bus_idx
        from cloudpss_skills_v2.libs.data_lib import BusType

        for gen in model.generators:
            if gen.bus not in bus_index_map:
                continue
            if gen.generator_type == GeneratorType.EXTERNAL_GRID:
                pp.create_ext_grid(
                    net, bus=bus_index_map[gen.bus], vm_pu=gen.v_set_pu, name=gen.name
                )
                continue
            pp.create_gen(
                net,
                bus=bus_index_map[gen.bus],
                p_mw=gen.p_mw,
                vm_pu=gen.v_set_pu,
                min_p_mw=gen.p_min_mw,
                max_p_mw=gen.p_max_mw,
                min_q_mvar=gen.q_min_mvar,
                max_q_mvar=gen.q_max_mvar,
                name=gen.name,
            )
        for load in model.loads:
            if load.bus not in bus_index_map:
                continue
            pp.create_load(
                net,
                bus=bus_index_map[load.bus],
                p_mw=load.p_mw,
                q_mvar=load.q_mvar,
                name=load.name,
            )
        for branch in model.branches:
            if branch.from_bus not in bus_index_map:
                continue
            if branch.to_bus not in bus_index_map:
                continue
            from_idx = bus_index_map[branch.from_bus]
            to_idx = bus_index_map[branch.to_bus]
            if branch.branch_type == BranchType.TRANSFORMER:
                name = branch.name or "Trafo"
                pp.create_transformer(
                    net, hv_bus=from_idx, lv_bus=to_idx, std_type="Trafo", name=name
                )
                continue
            name = branch.name or f"Line_{branch.from_bus}_{branch.to_bus}"
            pp.create_line_from_parameters(
                net,
                from_bus=from_idx,
                to_bus=to_idx,
                length_km=1,
                r_ohm_per_km=branch.resistance_pu if branch.resistance_pu else 0.1,
                x_ohm_per_km=branch.reactance_pu if branch.reactance_pu else 0.4,
                c_nf_per_km=0,
                max_i_ka=1,
                name=name,
            )
        for switch in model.switches:
            if switch.from_bus not in bus_index_map:
                continue
            if switch.to_bus not in bus_index_map:
                continue
            rated = switch.rated_current_ka or 1
            pp.create_switch(
                net,
                bus=bus_index_map[switch.from_bus],
                element=bus_index_map[switch.to_bus],
                et="b",
                closed=switch.state == SwitchState.CLOSED,
                name=switch.name,
                rated_current=rated,
                in_service=switch.in_service,
            )
        for shunt in model.shunts:
            if shunt.bus not in bus_index_map:
                continue
            pp.create_shunt(
                net,
                bus=bus_index_map[shunt.bus],
                q_mvar=-shunt.q_mvar,
                step=shunt.step,
                max_step=shunt.max_step,
                name=shunt.name,
                in_service=shunt.in_service,
            )
        report.items_converted = (
            len(model.buses)
            + len(model.branches)
            + len(model.generators)
            + len(model.loads)
            + len(model.switches)
            + len(model.shunts)
        )
        report.quality = (
            ConversionQuality.HIGH
            if mode == ConversionMode.LOSSLESS
            else ConversionQuality.MEDIUM
        )
        return (net, report)


def _safe_float(value: Any, default: float | None = None) -> float | None:
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


class CloudPSSModelConverter(ModelConverter):
    @property
    def source_engine(self) -> str:
        return "cloudpss"

    @property
    def target_engine(self) -> str:
        return "cloudpss"

    def _build_node_bus_map(self, components: dict) -> tuple[dict, dict]:
        bus_type_rid = "model/CloudPSS/_newBus_3p"
        node_to_bus = {}
        bus_components = {}
        for key, comp in components.items():
            if not isinstance(comp, dict):
                continue
            rid = comp.get("rid", "")
            if rid != bus_type_rid:
                continue
            args = comp.get("args", {})
            if not isinstance(args, dict):
                continue
            name = str(args.get("Name", f"Bus_{key}"))
            pins = comp.get("pins", {})
            if isinstance(pins, dict) and "0" in pins:
                node_to_bus[pins["0"]] = name
            bus_components[key] = comp
        return (node_to_bus, bus_components)

    def _parse_buses(
        self, bus_components: dict, report: ConversionReport
    ) -> list[BusData]:
        buses = []
        for key, comp in bus_components.items():
            args = comp.get("args", {})
            if not isinstance(args, dict):
                continue
            name = str(args.get("Name", f"Bus_{key}"))
            v_base = _safe_float(args.get("VBase"), 0.0)
            v_pu_raw = _safe_float(args.get("V"))
            angle = _safe_float(args.get("Theta"))
            v_pu = v_pu_raw if v_pu_raw is not None else 1.0
            buses.append(
                BusData(
                    name=name,
                    voltage_kv=v_base,
                    bus_type=BusType.PQ,
                    voltage_pu=v_pu,
                    angle_deg=angle or 0.0,
                    engine_id=key,
                )
            )
        report.items_converted = len(buses)
        return buses

    def _parse_branches(
        self, components: dict, node_to_bus: dict, report: ConversionReport
    ) -> list[BranchData]:
        branches = []
        line_rid = "model/CloudPSS/TransmissionLine"
        trafo_rid = "model/CloudPSS/_newTransformer_3p2w"
        for key, comp in components.items():
            if not isinstance(comp, dict):
                continue
            rid = comp.get("rid", "")
            args = comp.get("args", {})
            pins = comp.get("pins", {})
            if rid == line_rid:
                from_bus = node_to_bus.get(
                    pins.get("0"), f"Unknown_{pins.get('0', '?')}"
                )
                to_bus = node_to_bus.get(pins.get("1"), f"Unknown_{pins.get('1', '?')}")
                r_pu = _safe_float(args.get("R1pu", args.get("R")), 0.0) or 0.001
                x_pu = _safe_float(args.get("X1pu", args.get("X")), 0.0) or 0.01
                b_pu = _safe_float(args.get("B1pu", args.get("B")), 0.0)
                name = str(args.get("Name", f"Line_{key}"))
                rating = _safe_float(args.get("Rating"))
                in_svc = bool(comp.get("status", 1) != 0)
                branches.append(
                    BranchData(
                        name=name,
                        from_bus=from_bus,
                        to_bus=to_bus,
                        branch_type=BranchType.LINE,
                        resistance_pu=r_pu,
                        reactance_pu=x_pu,
                        susceptance_pu=b_pu,
                        rating_mva=rating,
                        in_service=in_svc,
                        engine_id=key,
                    )
                )
            elif rid == trafo_rid:
                from_bus = node_to_bus.get(
                    pins.get("0"), f"Unknown_{pins.get('0', '?')}"
                )
                to_bus = node_to_bus.get(pins.get("1"), f"Unknown_{pins.get('1', '?')}")
                name = str(args.get("Name", f"Trafo_{key}"))
                r_pu = _safe_float(args.get("R1pu", args.get("Rl")), 0.0)
                x_pu = _safe_float(args.get("X1pu", args.get("Xl")), 0.0)
                rating = _safe_float(args.get("Tmva"))
                tap = _safe_float(args.get("Tm"), 1.0)
                v1 = _safe_float(args.get("V1"), 345.0)
                v2 = _safe_float(args.get("V2"), 230.0)
                phase_shift = _safe_float(args.get("Lead"), 0.0)
                no_load_i = _safe_float(args.get("Im1"))
                no_load_loss = _safe_float(args.get("Gm"), 100.0)
                in_svc = bool(comp.get("status", 1) != 0)
                branches.append(
                    BranchData(
                        name=name,
                        from_bus=from_bus,
                        to_bus=to_bus,
                        branch_type=BranchType.TRANSFORMER,
                        resistance_pu=r_pu,
                        reactance_pu=x_pu,
                        rating_mva=rating,
                        tap_ratio=tap,
                        winding1_kv=v1,
                        winding2_kv=v2,
                        phase_shift_deg=phase_shift,
                        no_load_current_pct=no_load_i,
                        no_load_loss_kw=no_load_loss,
                        in_service=in_svc,
                        engine_id=key,
                    )
                )
        report.items_converted += len(branches)
        return branches

    def _parse_generators(
        self, components: dict, node_to_bus: dict, report: ConversionReport
    ) -> list[GeneratorData]:
        generators = []
        gen_rid = "model/CloudPSS/SyncGeneratorRouter"
        for key, comp in components.items():
            if not isinstance(comp, dict):
                continue
            rid = comp.get("rid", "")
            if rid != gen_rid:
                continue
            args = comp.get("args", {})
            pins = comp.get("pins", {})
            name = str(args.get("Name", f"Gen_{key}"))
            bus = node_to_bus.get(pins.get("0"), f"Unknown_{pins.get('0', '?')}")
            p_mw = _safe_float(args.get("pf_P", args.get("P")), 0.0)
            v_pu = _safe_float(args.get("pf_V", args.get("V")))
            gen_type = (
                GeneratorType.EXTERNAL_GRID
                if pins.get("1")
                else GeneratorType.SYNCHRONOUS
            )
            v_set = v_pu if v_pu is not None else 1.0
            generators.append(
                GeneratorData(
                    name=name,
                    bus=bus,
                    generator_type=gen_type,
                    p_mw=p_mw,
                    v_set_pu=v_set,
                    engine_id=key,
                )
            )
        report.items_converted += len(generators)
        return generators

    def _parse_loads(
        self, components: dict, node_to_bus: dict, report: ConversionReport
    ) -> list[LoadData]:
        loads = []
        load_rid = "model/CloudPSS/_newExpLoad_3p"
        for key, comp in components.items():
            if not isinstance(comp, dict):
                continue
            rid = comp.get("rid", "")
            if rid != load_rid:
                continue
            args = comp.get("args", {})
            pins = comp.get("pins", {})
            name = str(args.get("Name", f"Load_{key}"))
            bus = node_to_bus.get(pins.get("0"), f"Unknown_{pins.get('0', '?')}")
            p_mw = _safe_float(args.get("p"), 0.0)
            q_mvar = _safe_float(args.get("q"), 0.0)
            in_svc = bool(comp.get("status", 1) != 0)
            loads.append(
                LoadData(
                    name=name,
                    bus=bus,
                    p_mw=p_mw,
                    q_mvar=q_mvar,
                    in_service=in_svc,
                    engine_id=key,
                )
            )
        report.items_converted += len(loads)
        return loads

    def _parse_switches(
        self, components: dict, node_to_bus: dict, report: ConversionReport
    ) -> list[SwitchData]:
        switches = []
        switch_rid = "model/CloudPSS/_newBreaker_3p"
        for key, comp in components.items():
            if not isinstance(comp, dict):
                continue
            rid = comp.get("rid", "")
            if rid != switch_rid:
                continue
            args = comp.get("args", {})
            pins = comp.get("pins", {})
            name = str(args.get("Name", f"Switch_{key}"))
            from_bus = node_to_bus.get(pins.get("0"), f"Unknown_{pins.get('0', '?')}")
            to_bus = node_to_bus.get(pins.get("1"), f"Unknown_{pins.get('1', '?')}")
            state = "closed" if args.get("Status", "closed") == "closed" else "open"
            in_svc = bool(comp.get("status", 1) != 0)
            switches.append(
                SwitchData(
                    name=name,
                    from_bus=from_bus,
                    to_bus=to_bus,
                    state=SwitchState(state),
                    in_service=in_svc,
                    engine_id=key,
                )
            )
        report.items_converted += len(switches)
        return switches

    def _parse_faults(
        self, components: dict, node_to_bus: dict, report: ConversionReport
    ) -> list[FaultData]:
        from cloudpss_skills_v2.libs.data_lib import FaultType

        faults = []
        fault_rid = "model/CloudPSS/_newFaultResistor_3p"
        for key, comp in components.items():
            if not isinstance(comp, dict):
                continue
            rid = comp.get("rid", "")
            if rid != fault_rid:
                continue
            args = comp.get("args", {})
            pins = comp.get("pins", {})
            bus = node_to_bus.get(pins.get("0"), f"Unknown_{pins.get('0', '?')}")
            r_f = _safe_float(args.get("R"), 0.0) or 0.0
            x_f = _safe_float(args.get("X"), 0.0) or 0.0
            faults.append(FaultData(bus=bus, r_f_ohm=r_f, x_f_ohm=x_f))
        report.items_converted += len(faults)
        return faults

    def _parse_shunts(
        self, components: dict, node_to_bus: dict, report: ConversionReport
    ) -> list[ShuntData]:
        shunts = []
        shunt_rid = "model/CloudPSS/_newShuntLC_3p"
        for key, comp in components.items():
            if not isinstance(comp, dict):
                continue
            rid = comp.get("rid", "")
            if rid != shunt_rid:
                continue
            args = comp.get("args", {})
            pins = comp.get("pins", {})
            name = str(args.get("Name", f"Shunt_{key}"))
            bus = node_to_bus.get(pins.get("0"), f"Unknown_{pins.get('0', '?')}")
            q_mvar = _safe_float(args.get("q"), 0.0)
            in_svc = bool(comp.get("status", 1) != 0)
            shunts.append(
                ShuntData(
                    name=name, bus=bus, q_mvar=q_mvar, in_service=in_svc, engine_id=key
                )
            )
        report.items_converted += len(shunts)
        return shunts

    def convert_to_model(
        self, source: Any, mode: ConversionMode = ConversionMode.APPROXIMATE
    ) -> tuple[PowerSystemModel, ConversionReport]:
        report = ConversionReport(
            source_engine="cloudpss", target_engine="model", mode=mode
        )
        model = source
        if hasattr(model, "fetchTopology"):
            topo = model.fetchTopology(implementType="powerflow")
        elif hasattr(model, "components"):
            topo = model
        else:
            report.errors.append("Source must be a CloudPSS Model or topology dict")
            return (PowerSystemModel(source_engine="cloudpss"), report)
        components = topo.components if hasattr(topo, "components") else topo
        node_to_bus, bus_components = self._build_node_bus_map(components)
        buses = self._parse_buses(bus_components, report)
        branches = self._parse_branches(components, node_to_bus, report)
        generators = self._parse_generators(components, node_to_bus, report)
        loads = self._parse_loads(components, node_to_bus, report)
        switches = self._parse_switches(components, node_to_bus, report)
        faults = self._parse_faults(components, node_to_bus, report)
        shunts = self._parse_shunts(components, node_to_bus, report)
        return (
            PowerSystemModel(
                source_engine="cloudpss",
                buses=buses,
                branches=branches,
                generators=generators,
                loads=loads,
                switches=switches,
                faults=faults,
                shunts=shunts,
            ),
            report,
        )

    def convert_from_model(
        self, model: PowerSystemModel, mode: ConversionMode = ConversionMode.APPROXIMATE
    ) -> tuple[Any, ConversionReport]:
        report = ConversionReport(
            source_engine="model", target_engine="cloudpss", mode=mode
        )
        report.errors.append("CloudPSS model write-back not yet implemented")
        return (None, report)


from cloudpss_skills_v2.libs.data_lib import BusType, GeneratorType, BranchType

__all__ = [
    "ConversionMode",
    "ConversionQuality",
    "ConversionReport",
    "PowerSystemModel",
    "ModelConverter",
    "DictModelConverter",
    "PandapowerModelConverter",
    "CloudPSSModelConverter",
]
