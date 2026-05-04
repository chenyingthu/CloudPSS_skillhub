from __future__ import annotations

import copy
import json
import math
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from cloudpss_skills_v2.powerapi.base import (
    EngineAdapter,
    EngineConfig,
    SimulationResult,
    SimulationStatus,
    SimulationType,
    ValidationError,
    ValidationResult,
)
from cloudpss_skills_v2.powerskill.model_handle import ComponentInfo, ComponentType

_CASE_NAMES = {
    "case3",
    "case4gs",
    "case5",
    "case6ww",
    "case9",
    "case14",
    "case24_ieee_rts",
    "case30",
    "case33bw",
    "case39",
    "case57",
    "case118",
    "case145",
    "case300",
    "case3120sp",
    "case1888rte",
    "case2848rte",
    "case6470rte",
    "case6495rte",
    "case6515rte",
    "case9241pegase",
}

_DF_BUS_FIELDS = {
    "name": "name",
    "vn_kv": "voltage_kv",
}

_DF_LINE_FIELDS = {
    "name": "name",
    "from_bus": "from_bus",
    "to_bus": "to_bus",
    "length_km": "length_km",
    "r_ohm_per_km": "r_ohm_per_km",
    "x_ohm_per_km": "x_ohm_per_km",
    "c_nf_per_km": "c_nf_per_km",
    "max_i_ka": "max_i_ka",
}

_DF_TRAFO_FIELDS = {
    "name": "name",
    "hv_bus": "hv_bus",
    "lv_bus": "lv_bus",
    "sn_mva": "sn_mva",
    "vn_hv_kv": "vn_hv_kv",
    "vn_lv_kv": "vn_lv_kv",
    "vkr_percent": "vkr_percent",
    "vk_percent": "vk_percent",
    "pfe_kw": "pfe_kw",
    "max_loading_percent": "max_loading_percent",
}

_DF_GEN_FIELDS = {
    "name": "name",
    "bus": "bus",
    "p_mw": "p_mw",
    "q_mvar": "q_mvar",
    "vm_pu": "vm_pu",
    "sn_mva": "sn_mva",
    "min_q_mvar": "min_q_mvar",
    "max_q_mvar": "max_q_mvar",
}

_DF_LOAD_FIELDS = {
    "name": "name",
    "bus": "bus",
    "p_mw": "p_mw",
    "q_mvar": "q_mvar",
    "const_z_percent": "const_z_percent",
    "const_i_percent": "const_i_percent",
    "sn_mva": "sn_mva",
}


def _safe_float(value, default=0.0) -> float:
    try:
        if value is None or (isinstance(value, float) and value != value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _component_name(value, fallback: str) -> str:
    if value is None:
        return fallback
    try:
        if value != value:
            return fallback
    except TypeError:
        pass
    text = str(value)
    return fallback if text in {"", "None", "nan", "NaN"} else text


def _load_case(case_name: str):
    import pandapower.networks as nw

    if not hasattr(nw, case_name):
        available = [a for a in dir(nw) if a.startswith("case")]
        raise ValueError(f"Unknown pandapower case: {case_name}. Available: {available}")
    return getattr(nw, case_name)()


def build_net_from_spec(model: dict[str, Any]):
    """Build a pandapower network from a repository JSON model artifact."""
    import pandapower as pp

    if model.get("format") != "pandapower_network_spec_v1":
        raise ValueError(f"unsupported model format: {model.get('format')}")

    net = pp.create_empty_network(sn_mva=float(model["sn_mva"]))
    bus_index: dict[str, int] = {}

    for bus in model.get("buses", []):
        bus_index[bus["id"]] = pp.create_bus(
            net,
            vn_kv=float(bus["vn_kv"]),
            name=bus.get("name", bus["id"]),
        )

    for grid in model.get("external_grids", []):
        pp.create_ext_grid(
            net,
            bus=bus_index[grid["bus"]],
            vm_pu=float(grid["vm_pu"]),
            va_degree=float(grid.get("va_degree", 0.0)),
            name=grid.get("name", "Grid"),
            s_sc_max_mva=float(grid["s_sc_max_mva"]),
            s_sc_min_mva=float(grid["s_sc_min_mva"]),
            rx_max=float(grid["rx_max"]),
            rx_min=float(grid["rx_min"]),
        )

    for line in model.get("lines", []):
        pp.create_line_from_parameters(
            net,
            from_bus=bus_index[line["from_bus"]],
            to_bus=bus_index[line["to_bus"]],
            length_km=float(line["length_km"]),
            r_ohm_per_km=float(line["r_ohm_per_km"]),
            x_ohm_per_km=float(line["x_ohm_per_km"]),
            c_nf_per_km=float(line["c_nf_per_km"]),
            max_i_ka=float(line["max_i_ka"]),
            name=line.get("name", "Line"),
        )

    for load in model.get("loads", []):
        pp.create_load(
            net,
            bus=bus_index[load["bus"]],
            p_mw=float(load["p_mw"]),
            q_mvar=float(load["q_mvar"]),
            name=load.get("name", "Load"),
        )

    return net


def load_net_from_json(path: str | Path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    model = data.get("model", data)
    return build_net_from_spec(model)


def _determine_bus_type(idx, net) -> str:
    """Determine bus type based on pandapower network structure.

    - Slack (ext_grid): Buses connected to external grid
    - PV: Buses with generators but no external grid
    - PQ: Load buses without generation
    """
    # Check if bus is connected to ext_grid (slack bus)
    if hasattr(net, "ext_grid") and not net.ext_grid.empty:
        ext_grid_buses = net.ext_grid["bus"].unique()
        if idx in ext_grid_buses:
            return "slack"

    # Check if bus has generators (PV bus)
    if hasattr(net, "gen") and not net.gen.empty:
        gen_buses = net.gen["bus"].unique()
        if idx in gen_buses:
            return "pv"

    # Check static generators
    if hasattr(net, "sgen") and not net.sgen.empty:
        sgen_buses = net.sgen["bus"].unique()
        if idx in sgen_buses:
            return "pv"

    # Default: PQ (load bus)
    return "pq"


def _bus_row(idx, row, net) -> dict:
    vm_pu = va_degree = None
    generation_mw = generation_mvar = load_mw = load_mvar = 0.0
    if hasattr(net, "res_bus") and not net.res_bus.empty and idx in net.res_bus.index:
        vm_pu = _safe_float(net.res_bus.at[idx, "vm_pu"])
        va_degree = _safe_float(net.res_bus.at[idx, "va_degree"])
    if hasattr(net, "res_gen") and not net.res_gen.empty and hasattr(net, "gen"):
        for gen_idx, gen in net.gen[net.gen["bus"] == idx].iterrows():
            if gen_idx in net.res_gen.index:
                generation_mw += _safe_float(net.res_gen.at[gen_idx, "p_mw"])
                generation_mvar += _safe_float(net.res_gen.at[gen_idx, "q_mvar"])
    if hasattr(net, "res_ext_grid") and not net.res_ext_grid.empty and hasattr(net, "ext_grid"):
        for ext_idx, ext_grid in net.ext_grid[net.ext_grid["bus"] == idx].iterrows():
            if ext_idx in net.res_ext_grid.index:
                generation_mw += _safe_float(net.res_ext_grid.at[ext_idx, "p_mw"])
                generation_mvar += _safe_float(net.res_ext_grid.at[ext_idx, "q_mvar"])
    if hasattr(net, "res_load") and not net.res_load.empty and hasattr(net, "load"):
        for load_idx, load in net.load[net.load["bus"] == idx].iterrows():
            if load_idx in net.res_load.index:
                load_mw += _safe_float(net.res_load.at[load_idx, "p_mw"])
                load_mvar += _safe_float(net.res_load.at[load_idx, "q_mvar"])
    return {
        "name": str(row.get("name", f"Bus_{idx}")),
        "voltage_kv": _safe_float(row.get("vn_kv", 0)),
        "voltage_pu": vm_pu,
        "angle_deg": va_degree,
        "bus_type": _determine_bus_type(idx, net),
        "generation_mw": round(generation_mw, 6),
        "generation_mvar": round(generation_mvar, 6),
        "load_mw": round(load_mw, 6),
        "load_mvar": round(load_mvar, 6),
        "engine_id": idx,
    }


def _branch_rows(net) -> list[dict]:
    rows = []
    if hasattr(net, "res_line") and not net.res_line.empty:
        for idx, row in net.line.iterrows():
            loading = (
                _safe_float(net.res_line.at[idx, "loading_percent"])
                if idx in net.res_line.index
                else None
            )
            rows.append(
                {
                    "name": str(row.get("name", f"Line_{idx}")),
                    "from_bus": int(row.get("from_bus", -1)),
                    "to_bus": int(row.get("to_bus", -1)),
                    "branch_type": "line",
                    "loading_pct": loading,
                    "p_from_mw": (
                        _safe_float(net.res_line.at[idx, "p_from_mw"])
                        if idx in net.res_line.index
                        else None
                    ),
                    "q_from_mvar": (
                        _safe_float(net.res_line.at[idx, "q_from_mvar"])
                        if idx in net.res_line.index
                        else None
                    ),
                    "p_to_mw": (
                        _safe_float(net.res_line.at[idx, "p_to_mw"])
                        if idx in net.res_line.index
                        else None
                    ),
                    "q_to_mvar": (
                        _safe_float(net.res_line.at[idx, "q_to_mvar"])
                        if idx in net.res_line.index
                        else None
                    ),
                    "pl_mw": (
                        _safe_float(net.res_line.at[idx, "pl_mw"])
                        if idx in net.res_line.index
                        else None
                    ),
                    "engine_id": idx,
                }
            )
    if hasattr(net, "res_trafo") and not net.res_trafo.empty:
        for idx, row in net.trafo.iterrows():
            loading = (
                _safe_float(net.res_trafo.at[idx, "loading_percent"])
                if idx in net.res_trafo.index
                else None
            )
            rows.append(
                {
                    "name": str(row.get("name", f"Trafo_{idx}")),
                    "from_bus": int(row.get("hv_bus", -1)),
                    "to_bus": int(row.get("lv_bus", -1)),
                    "branch_type": "transformer",
                    "loading_pct": loading,
                    "pl_mw": (
                        _safe_float(net.res_trafo.at[idx, "pl_mw"])
                        if idx in net.res_trafo.index
                        else None
                    ),
                    "engine_id": idx,
                }
            )
    return rows


def _generate_pf_summary(bus_rows, branch_rows) -> dict:
    total_p_gen = total_q_gen = total_p_load = total_q_load = total_loss = 0.0
    min_vm = 999.0
    max_vm = 0.0
    for b in bus_rows:
        vm = _safe_float(b.get("voltage_pu"), 1.0)
        total_p_gen += _safe_float(b.get("generation_mw"))
        total_q_gen += _safe_float(b.get("generation_mvar"))
        total_p_load += _safe_float(b.get("load_mw"))
        total_q_load += _safe_float(b.get("load_mvar"))
        if 0 < vm < min_vm:
            min_vm = vm
        if vm > max_vm:
            max_vm = vm
    for br in branch_rows:
        total_loss += _safe_float(br.get("pl_mw"))
    return {
        "total_generation": {
            "p_mw": round(total_p_gen, 4),
            "q_mvar": round(total_q_gen, 4),
        },
        "total_load": {
            "p_mw": round(total_p_load, 4),
            "q_mvar": round(total_q_load, 4),
        },
        "total_loss_mw": round(total_loss, 4),
        "voltage_range": {"min_pu": round(min_vm, 4), "max_pu": round(max_vm, 4)},
        "bus_count": len(bus_rows),
        "branch_count": len(branch_rows),
    }


class PandapowerPowerFlowAdapter(EngineAdapter):
    _net_cache: dict[str, Any]
    _result_cache: dict[str, SimulationResult]

    def __init__(self, config: Optional[EngineConfig] = None):
        super().__init__(config)
        self._net_cache = {}
        self._result_cache = {}

    @property
    def engine_name(self) -> str:
        return "pandapower"

    def get_supported_simulations(self) -> list[SimulationType]:
        return [SimulationType.POWER_FLOW]

    def _do_connect(self) -> None:
        import pandapower as pp

        self._logger.info("pandapower %s ready", pp.__version__)

    def _do_disconnect(self) -> None:
        self._net_cache.clear()
        self._result_cache.clear()

    def _resolve_net(self, model_id: str, config: dict[str, Any] | None = None):
        if model_id in self._net_cache:
            return self._net_cache[model_id]
        config = config or {}
        network = config.get("network")
        if network is not None:
            self._net_cache[model_id] = network
            return network
        model_file = config.get("model_file") or model_id
        if (
            isinstance(model_file, str)
            and model_file.endswith(".json")
            and Path(model_file).exists()
        ):
            net = load_net_from_json(model_file)
            self._net_cache[model_id] = net
            return net
        if model_id in _CASE_NAMES or model_id.startswith("case"):
            net = _load_case(model_id)
            self._net_cache[model_id] = net
            return net
        raise ValueError(f"Cannot resolve pandapower model: {model_id}")

    def _do_load_model(self, model_id: str) -> bool:
        try:
            net = self._resolve_net(model_id)
            self._logger.info(
                "Loaded pandapower net: %d buses, %d lines", len(net.bus), len(net.line)
            )
            return True
        except Exception as e:
            self._logger.error("Failed to load model %s: %s", model_id, e)
            return False

    def _do_run_simulation(self, config: dict[str, Any]) -> SimulationResult:
        model_id = config.get("model_id") or self._current_model_id
        if not model_id:
            return SimulationResult(status=SimulationStatus.FAILED, errors=["No model_id provided"])

        started = datetime.now()
        job_id = str(uuid.uuid4())[:8]

        try:
            net = self._resolve_net(model_id, config)
        except Exception as e:
            return SimulationResult(
                job_id=job_id,
                status=SimulationStatus.FAILED,
                errors=[f"Failed to load model {model_id}: {e}"],
                started_at=started,
                completed_at=datetime.now(),
            )

        try:
            import pandapower as pp

            algorithm = config.get("algorithm", "newton_raphson")
            if algorithm == "dc":
                pp.rundcpp(net)
            else:
                pp.runpp(net)

            if not net.converged:
                return SimulationResult(
                    job_id=job_id,
                    status=SimulationStatus.FAILED,
                    errors=["Power flow did not converge"],
                    data={"converged": False},
                    started_at=started,
                    completed_at=datetime.now(),
                )

            bus_rows = [_bus_row(idx, row, net) for idx, row in net.bus.iterrows()]
            branch_rows = _branch_rows(net)
            summary = _generate_pf_summary(bus_rows, branch_rows)

            result_data = {
                "model": model_id,
                "model_rid": model_id,
                "job_id": job_id,
                "converged": True,
                "bus_count": len(bus_rows),
                "branch_count": len(branch_rows),
                "buses": bus_rows,
                "branches": branch_rows,
                "summary": summary,
            }
            system_model = self._to_unified_model(net)

            sim_result = SimulationResult(
                job_id=job_id,
                status=SimulationStatus.COMPLETED,
                data=result_data,
                system_model=system_model,
                started_at=started,
                completed_at=datetime.now(),
            )
            self._result_cache[job_id] = sim_result
            return sim_result

        except Exception as e:
            return SimulationResult(
                job_id=job_id,
                status=SimulationStatus.FAILED,
                errors=[str(e)],
                started_at=started,
                completed_at=datetime.now(),
            )

    def _do_get_result(self, job_id: str) -> SimulationResult:
        cached = self._result_cache.get(job_id)
        if cached:
            return cached
        return SimulationResult(
            job_id=job_id,
            status=SimulationStatus.FAILED,
            errors=[f"Result not found for job_id: {job_id}"],
        )

    # --- Model manipulation ---

    @staticmethod
    def _classify_component(table_name: str) -> str:
        mapping = {
            "line": ComponentType.BRANCH,
            "trafo": ComponentType.TRANSFORMER,
            "trafo3w": ComponentType.TRANSFORMER,
            "gen": ComponentType.GENERATOR,
            "sgen": ComponentType.GENERATOR,
            "ext_grid": ComponentType.SOURCE,
            "load": ComponentType.LOAD,
            "bus": ComponentType.BUS,
            "shunt": ComponentType.SHUNT,
            "switch": ComponentType.OTHER,
            "ward": ComponentType.LOAD,
        }
        return mapping.get(table_name, ComponentType.OTHER)

    def _do_get_components(self, model_id: str) -> list[ComponentInfo]:
        net = self._resolve_net(model_id)
        components = []
        component_tables = [
            ("line", "line"),
            ("trafo", "trafo"),
            ("trafo3w", "trafo3w"),
            ("gen", "gen"),
            ("sgen", "sgen"),
            ("ext_grid", "ext_grid"),
            ("load", "load"),
            ("bus", "bus"),
            ("shunt", "shunt"),
        ]
        for table_attr, table_name in component_tables:
            df = getattr(net, table_attr, None)
            if df is None or df.empty:
                continue
            comp_type = self._classify_component(table_name)
            for idx, row in df.iterrows():
                name = str(row.get("name", f"{table_name}_{idx}"))
                args = {col: row[col] for col in row.index if col != "name"}
                components.append(
                    ComponentInfo(
                        key=f"{table_name}:{idx}",
                        name=name,
                        definition=f"pandapower/{table_name}",
                        component_type=comp_type,
                        args=args,
                    )
                )
        return components

    def _do_remove_component(self, model_id: str, component_key: str) -> bool:
        net = self._resolve_net(model_id)
        try:
            table_name, idx_str = component_key.split(":", 1)
            idx = int(idx_str)
            df = getattr(net, table_name, None)
            if df is None:
                return False
            if idx not in df.index:
                return False
            df.drop(idx, inplace=True)
            return True
        except (ValueError, AttributeError):
            return False

    def _do_update_component_args(
        self, model_id: str, component_key: str, args: dict[str, Any]
    ) -> bool:
        net = self._resolve_net(model_id)
        try:
            table_name, idx_str = component_key.split(":", 1)
            idx = int(idx_str)
            df = getattr(net, table_name, None)
            if df is None or idx not in df.index:
                return False
            for col, val in args.items():
                if col in df.columns:
                    df.at[idx, col] = val
            return True
        except (ValueError, AttributeError):
            return False

    def _do_clone_model(self, model_id: str) -> str:
        net = self._resolve_net(model_id)
        clone_id = f"{model_id}__clone_{uuid.uuid4().hex[:8]}"
        self._net_cache[clone_id] = copy.deepcopy(net)
        return clone_id

    def _do_validate_config(self, config: dict[str, Any]) -> ValidationResult:
        errors = []
        model_id = config.get("model_id")
        if not model_id:
            errors.append(ValidationError(field="model_id", message="model_id is required"))
        algorithm = config.get("algorithm")
        if algorithm and algorithm not in (
            "newton_raphson",
            "fast_decoupled",
            "dc",
            "acpf",
        ):
            errors.append(
                ValidationError(field="algorithm", message=f"Unknown algorithm: {algorithm}")
            )
        return ValidationResult(valid=len(errors) == 0, errors=errors)

    # -------------------------------------------------------------------------
    # Unified Model Conversion (New Architecture)
    # -------------------------------------------------------------------------

    def _to_unified_model(self, net: Any) -> Any:
        """Convert pandapower network to unified PowerSystemModel.

        Args:
            net: pandapower network object

        Returns:
            Unified PowerSystemModel
        """
        # Import here to avoid circular imports
        from cloudpss_skills_v2.core.system_model import (
            Bus, Branch, Generator, Load, PowerSystemModel
        )

        # Convert buses
        buses = []
        for idx, row in net.bus.iterrows():
            bus_type = _determine_bus_type(idx, net)
            vm_pu = va_deg = None

            # Get power flow results if available
            if hasattr(net, 'res_bus') and not net.res_bus.empty and idx in net.res_bus.index:
                vm_pu = _safe_float(net.res_bus.at[idx, "vm_pu"])
                va_deg = _safe_float(net.res_bus.at[idx, "va_degree"])

            # Calculate generation and load at this bus
            p_gen = q_gen = p_load = q_load = 0.0

            # Generation from gen
            if hasattr(net, 'gen') and not net.gen.empty:
                for gen_idx, gen in net.gen[net.gen["bus"] == idx].iterrows():
                    if hasattr(net, 'res_gen') and gen_idx in net.res_gen.index:
                        p_gen += _safe_float(net.res_gen.at[gen_idx, "p_mw"])
                        q_gen += _safe_float(net.res_gen.at[gen_idx, "q_mvar"])

            # Generation from ext_grid
            if hasattr(net, 'ext_grid') and not net.ext_grid.empty:
                for ext_idx, ext in net.ext_grid[net.ext_grid["bus"] == idx].iterrows():
                    if hasattr(net, 'res_ext_grid') and ext_idx in net.res_ext_grid.index:
                        p_gen += _safe_float(net.res_ext_grid.at[ext_idx, "p_mw"])
                        q_gen += _safe_float(net.res_ext_grid.at[ext_idx, "q_mvar"])

            # Static generators
            if hasattr(net, 'sgen') and not net.sgen.empty:
                for sgen_idx, sgen in net.sgen[net.sgen["bus"] == idx].iterrows():
                    if hasattr(net, 'res_sgen') and sgen_idx in net.res_sgen.index:
                        p_gen += _safe_float(net.res_sgen.at[sgen_idx, "p_mw"])
                        q_gen += _safe_float(net.res_sgen.at[sgen_idx, "q_mvar"])

            # Load
            if hasattr(net, 'load') and not net.load.empty:
                for load_idx, load in net.load[net.load["bus"] == idx].iterrows():
                    if hasattr(net, 'res_load') and load_idx in net.res_load.index:
                        p_load += _safe_float(net.res_load.at[load_idx, "p_mw"])
                        q_load += _safe_float(net.res_load.at[load_idx, "q_mvar"])

            bus = Bus(
                bus_id=idx,
                name=str(row.get("name", f"Bus_{idx}")),
                base_kv=_safe_float(row.get("vn_kv"), 230.0),
                bus_type=bus_type.upper(),
                v_magnitude_pu=vm_pu,
                v_angle_degree=va_deg,
                p_injected_mw=(p_gen - p_load) if (p_gen > 0 or p_load > 0) else None,
                q_injected_mvar=(q_gen - q_load) if (q_gen != 0 or q_load != 0) else None,
                vm_min_pu=0.9,
                vm_max_pu=1.1,
            )
            buses.append(bus)

        # Convert branches (lines and transformers)
        branches = []

        # Lines
        if hasattr(net, 'line') and not net.line.empty:
            for idx, row in net.line.iterrows():
                loading = None
                p_from = q_from = p_to = q_to = None

                if hasattr(net, 'res_line') and not net.res_line.empty and idx in net.res_line.index:
                    loading = _safe_float(net.res_line.at[idx, "loading_percent"])
                    p_from = _safe_float(net.res_line.at[idx, "p_from_mw"])
                    q_from = _safe_float(net.res_line.at[idx, "q_from_mvar"])
                    p_to = _safe_float(net.res_line.at[idx, "p_to_mw"])
                    q_to = _safe_float(net.res_line.at[idx, "q_to_mvar"])

                length_km = _safe_float(row.get("length_km", 1.0), 1.0)
                from_bus = int(row.get("from_bus", 0))
                base_kv = _safe_float(net.bus.at[from_bus, "vn_kv"], 230.0) if from_bus in net.bus.index else 230.0
                base_mva = float(net.sn_mva) if hasattr(net, "sn_mva") else 100.0
                z_base = (base_kv ** 2) / base_mva
                r_pu = _safe_float(row.get("r_ohm_per_km", 0.0)) * length_km / z_base if z_base else 0.0
                x_pu = _safe_float(row.get("x_ohm_per_km", 0.01)) * length_km / z_base if z_base else 0.01
                c_nf = _safe_float(row.get("c_nf_per_km", 0.0)) * length_km
                preserved_b_pu = _safe_float(row.get("_unified_b_pu"), None)
                if preserved_b_pu is not None and math.isfinite(preserved_b_pu):
                    b_pu = preserved_b_pu
                else:
                    frequency_hz = float(getattr(net, "f_hz", 50.0) or 50.0)
                    b_pu = (
                        2
                        * 3.141592653589793
                        * frequency_hz
                        * c_nf
                        * 1e-9
                        * (base_kv ** 2)
                        / base_mva
                    )
                rate_a_mva = (
                    _safe_float(row.get("max_i_ka", 1.0))
                    * base_kv
                    * 1.732
                )

                branch = Branch(
                    from_bus=from_bus,
                    to_bus=int(row.get("to_bus", 0)),
                    name=_component_name(row.get("name"), f"line:{idx}"),
                    branch_type="LINE",
                    r_pu=r_pu,
                    x_pu=x_pu,
                    b_pu=b_pu,
                    rate_a_mva=rate_a_mva,
                    p_from_mw=p_from,
                    q_from_mvar=q_from,
                    p_to_mw=p_to,
                    q_to_mvar=q_to,
                    loading_percent=loading,
                )
                branches.append(branch)

        # Transformers
        if hasattr(net, 'trafo') and not net.trafo.empty:
            for idx, row in net.trafo.iterrows():
                loading = None
                p_from = q_from = p_to = q_to = None

                if hasattr(net, 'res_trafo') and not net.res_trafo.empty and idx in net.res_trafo.index:
                    loading = _safe_float(net.res_trafo.at[idx, "loading_percent"])
                    p_from = _safe_float(net.res_trafo.at[idx, "p_hv_mw"])
                    q_from = _safe_float(net.res_trafo.at[idx, "q_hv_mvar"])
                    p_to = _safe_float(net.res_trafo.at[idx, "p_lv_mw"])
                    q_to = _safe_float(net.res_trafo.at[idx, "q_lv_mvar"])

                branch = Branch(
                    from_bus=int(row.get("hv_bus", 0)),
                    to_bus=int(row.get("lv_bus", 0)),
                    name=_component_name(row.get("name"), f"trafo:{idx}"),
                    branch_type="TRANSFORMER",
                    r_pu=_safe_float(row.get("vkr_percent", 0.0)) / 100.0,
                    x_pu=_safe_float(row.get("vk_percent", 0.0)) / 100.0,
                    rate_a_mva=_safe_float(row.get("sn_mva", 100.0)),
                    p_from_mw=p_from,
                    q_from_mvar=q_from,
                    p_to_mw=p_to,
                    q_to_mvar=q_to,
                    loading_percent=loading,
                )
                branches.append(branch)

        # Convert generators
        generators = []

        # 1. Convert synchronous generators (net.gen)
        if hasattr(net, 'gen') and not net.gen.empty:
            for idx, row in net.gen.iterrows():
                p_gen = q_gen = v_set = None
                if hasattr(net, 'res_gen') and not net.res_gen.empty and idx in net.res_gen.index:
                    p_gen = _safe_float(net.res_gen.at[idx, "p_mw"])
                    q_gen = _safe_float(net.res_gen.at[idx, "q_mvar"])

                gen = Generator(
                    bus_id=int(row.get("bus", 0)),
                    name=str(row.get("name", f"Gen_{idx}")),
                    p_gen_mw=p_gen if p_gen else _safe_float(row.get("p_mw", 0)),
                    q_gen_mvar=q_gen,
                    p_max_mw=_safe_float(row.get("max_p_mw", 9999.0)),
                    p_min_mw=_safe_float(row.get("min_p_mw", 0.0)),
                    v_set_pu=_safe_float(row.get("vm_pu", 1.0)),
                )
                generators.append(gen)

        # 2. Convert external grid / slack bus (net.ext_grid)
        if hasattr(net, 'ext_grid') and not net.ext_grid.empty:
            for idx, row in net.ext_grid.iterrows():
                p_gen = q_gen = None
                if hasattr(net, 'res_ext_grid') and not net.res_ext_grid.empty and idx in net.res_ext_grid.index:
                    p_gen = _safe_float(net.res_ext_grid.at[idx, "p_mw"])
                    q_gen = _safe_float(net.res_ext_grid.at[idx, "q_mvar"])

                gen = Generator(
                    bus_id=int(row.get("bus", 0)),
                    name=str(row.get("name", f"ExtGrid_{idx}")),
                    p_gen_mw=p_gen if p_gen else 0.0,
                    q_gen_mvar=q_gen,
                    p_max_mw=999999.0,  # Slack bus has no limits
                    p_min_mw=-999999.0,
                    v_set_pu=_safe_float(row.get("vm_pu", 1.0)),
                )
                generators.append(gen)

        # 3. Convert static generators (net.sgen) - treated as negative load or generation
        if hasattr(net, 'sgen') and not net.sgen.empty:
            for idx, row in net.sgen.iterrows():
                p_sgen = q_sgen = None
                if hasattr(net, 'res_sgen') and not net.res_sgen.empty and idx in net.res_sgen.index:
                    p_sgen = _safe_float(net.res_sgen.at[idx, "p_mw"])
                    q_sgen = _safe_float(net.res_sgen.at[idx, "q_mvar"])

                # Static generators are typically DG/PV - add as generators
                if p_sgen and p_sgen > 0:
                    gen = Generator(
                        bus_id=int(row.get("bus", 0)),
                        name=str(row.get("name", f"SGen_{idx}")),
                        p_gen_mw=p_sgen,
                        q_gen_mvar=q_sgen,
                        p_max_mw=_safe_float(row.get("max_p_mw", p_sgen * 2)),
                        p_min_mw=0.0,
                    )
                    generators.append(gen)

        # Convert loads
        loads = []
        if hasattr(net, 'load') and not net.load.empty:
            for idx, row in net.load.iterrows():
                p_load = q_load = None
                if hasattr(net, 'res_load') and not net.res_load.empty and idx in net.res_load.index:
                    p_load = _safe_float(net.res_load.at[idx, "p_mw"])
                    q_load = _safe_float(net.res_load.at[idx, "q_mvar"])

                load = Load(
                    bus_id=int(row.get("bus", 0)),
                    name=str(row.get("name", f"Load_{idx}")),
                    p_mw=p_load if p_load else _safe_float(row.get("p_mw", 0)),
                    q_mvar=q_load if q_load else _safe_float(row.get("q_mvar", 0)),
                )
                loads.append(load)

        return PowerSystemModel(
            buses=buses,
            branches=branches,
            generators=generators,
            loads=loads,
            base_mva=float(net.sn_mva) if hasattr(net, 'sn_mva') else 100.0,
            frequency_hz=float(getattr(net, "f_hz", 50.0) or 50.0),
            source_engine="pandapower",
            name=getattr(net, 'name', 'pandapower_net'),
        )

    def from_unified_model(self, model: PowerSystemModel) -> Any:
        """Convert unified PowerSystemModel to pandapower network.

        This enables cross-engine comparison by creating an equivalent
        pandapower network from the unified model representation.

        Args:
            model: Unified PowerSystemModel

        Returns:
            pandapower network object
        """
        import pandapower as pp

        # Create empty network
        net = pp.create_empty_network(
            name=model.name or "unified_model",
            f_hz=model.frequency_hz,
        )
        net.sn_mva = model.base_mva

        # Create buses
        bus_idx_map = {}  # Map unified bus_id to pandapower bus index
        for bus in model.buses:
            pp_bus_idx = pp.create_bus(
                net,
                vn_kv=bus.base_kv,
                name=bus.name,
                type=bus.bus_type.lower() if bus.bus_type else "b",
                max_vm_pu=bus.vm_max_pu or 1.1,
                min_vm_pu=bus.vm_min_pu or 0.9,
            )
            bus_idx_map[bus.bus_id] = pp_bus_idx

        # Create external grid (slack bus)
        slack_bus = model.get_slack_bus()

        # If no explicit slack bus in unified model, try to find one by angle=0
        if slack_bus is None:
            # Find bus with angle closest to 0
            slack_candidate = min(model.buses, key=lambda b: abs(b.v_angle_degree or 999))
            if abs(slack_candidate.v_angle_degree or 999) < 0.1:
                slack_bus = slack_candidate
                print(f"Auto-selected slack bus: {slack_bus.name} (angle=0 reference)")

        if slack_bus:
            slack_pp_idx = bus_idx_map.get(slack_bus.bus_id)
            if slack_pp_idx is not None:
                # Use voltage magnitude as setpoint (Bus doesn't have v_set_pu)
                vm_pu = slack_bus.v_magnitude_pu if slack_bus.v_magnitude_pu else 1.0
                pp.create_ext_grid(
                    net,
                    bus=slack_pp_idx,
                    vm_pu=vm_pu,
                    name=f"{slack_bus.name}_slack",
                )

        # Track which buses have generators (for PV bus detection)
        buses_with_gens = {gen.bus_id for gen in model.generators}

        # Create generators (PV buses)
        for gen in model.generators:
            pp_bus = bus_idx_map.get(gen.bus_id)
            if pp_bus is not None:
                # Find the bus to get voltage setpoint
                bus = next((b for b in model.buses if b.bus_id == gen.bus_id), None)
                # Check if this is the slack bus generator
                if slack_bus and gen.bus_id == slack_bus.bus_id:
                    # Slack bus generator is already handled by ext_grid
                    continue
                # Create generator (treat as PV bus if not slack)
                pp.create_gen(
                    net,
                    bus=pp_bus,
                    p_mw=gen.p_gen_mw or 0,
                    vm_pu=gen.v_set_pu or (bus.v_magnitude_pu if bus else 1.0) or 1.0,
                    name=gen.name,
                    max_p_mw=gen.p_max_mw or 9999,
                    min_p_mw=gen.p_min_mw or 0,
                )

        # Create loads
        for load in model.loads:
            pp_bus = bus_idx_map.get(load.bus_id)
            if pp_bus is not None and (load.p_mw or load.q_mvar):
                pp.create_load(
                    net,
                    bus=pp_bus,
                    p_mw=load.p_mw or 0,
                    q_mvar=load.q_mvar or 0,
                    name=load.name,
                )

        # Create branches (lines)
        for branch in model.branches:
            if branch.branch_type == "LINE":
                from_bus = bus_idx_map.get(branch.from_bus)
                to_bus = bus_idx_map.get(branch.to_bus)
                if from_bus is not None and to_bus is not None:
                    # Get base voltage for impedance calculation
                    from_vn = net.bus.at[from_bus, "vn_kv"] if from_bus in net.bus.index else 230.0
                    # Z_base = V_base^2 / S_base (ohm)
                    z_base = (from_vn ** 2) / model.base_mva
                    # Convert pu to ohm: Z_ohm = Z_pu * Z_base
                    # For line parameters (ohm/km), assume 1 km length
                    length_km = 1.0
                    r_ohm = (branch.r_pu or 0) * z_base
                    x_ohm = (branch.x_pu or 0) * z_base
                    # For per-unit admittance, Y_base = S_base / V_base^2, so
                    # C = B_pu / (2*pi*f*V_base^2) when V is in kV and C in nF.
                    frequency_hz = getattr(net, "f_hz", model.frequency_hz)
                    c_nf = (
                        (branch.b_pu or 0)
                        / (2 * 3.14159 * frequency_hz * (from_vn ** 2))
                        * 1e9
                    ) if branch.b_pu and branch.b_pu > 0 else 0

                    pp.create_line_from_parameters(
                        net,
                        from_bus=from_bus,
                        to_bus=to_bus,
                        length_km=length_km,
                        r_ohm_per_km=r_ohm / length_km,
                        x_ohm_per_km=x_ohm / length_km,
                        c_nf_per_km=c_nf / length_km,
                        max_i_ka=(branch.rate_a_mva or 100) / (from_vn * 1.732),
                        name=branch.name,
                    )
                    net.line.at[net.line.index[-1], "_unified_b_pu"] = branch.b_pu or 0.0
            elif branch.branch_type == "TRANSFORMER":
                from_bus = bus_idx_map.get(branch.from_bus)
                to_bus = bus_idx_map.get(branch.to_bus)
                if from_bus is not None and to_bus is not None:
                    # Get bus voltages for tap calculation
                    from_vn = net.bus.at[from_bus, "vn_kv"] if from_bus in net.bus.index else 230.0
                    to_vn = net.bus.at[to_bus, "vn_kv"] if to_bus in net.bus.index else 230.0
                    hv_bus = from_bus if from_vn >= to_vn else to_bus
                    lv_bus = to_bus if from_vn >= to_vn else from_bus
                    hv_vn = max(from_vn, to_vn)
                    lv_vn = min(from_vn, to_vn)

                    pp.create_transformer_from_parameters(
                        net,
                        hv_bus=hv_bus,
                        lv_bus=lv_bus,
                        sn_mva=branch.rate_a_mva or 100.0,
                        vn_hv_kv=hv_vn,
                        vn_lv_kv=lv_vn,
                        vkr_percent=(branch.r_pu or 0) * 100,
                        vk_percent=(branch.x_pu or 0.01) * 100,
                        pfe_kw=0,
                        i0_percent=0,
                        name=branch.name,
                    )

        return net


__all__ = [
    "PandapowerPowerFlowAdapter",
    "build_net_from_spec",
    "load_net_from_json",
]
