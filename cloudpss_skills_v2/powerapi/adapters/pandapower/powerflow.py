from __future__ import annotations

import copy
import uuid
from datetime import datetime
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


def _load_case(case_name: str):
    import pandapower.networks as nw

    if not hasattr(nw, case_name):
        available = [a for a in dir(nw) if a.startswith("case")]
        raise ValueError(
            f"Unknown pandapower case: {case_name}. Available: {available}"
        )
    return getattr(nw, case_name)()


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
    if hasattr(net, "res_bus") and not net.res_bus.empty and idx in net.res_bus.index:
        vm_pu = _safe_float(net.res_bus.at[idx, "vm_pu"])
        va_degree = _safe_float(net.res_bus.at[idx, "va_degree"])
    return {
        "name": str(row.get("name", f"Bus_{idx}")),
        "voltage_kv": _safe_float(row.get("vn_kv", 0)),
        "voltage_pu": vm_pu,
        "angle_deg": va_degree,
        "bus_type": _determine_bus_type(idx, net),
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
                    "p_from_mw": _safe_float(net.res_line.at[idx, "p_from_mw"])
                    if idx in net.res_line.index
                    else None,
                    "q_from_mvar": _safe_float(net.res_line.at[idx, "q_from_mvar"])
                    if idx in net.res_line.index
                    else None,
                    "p_to_mw": _safe_float(net.res_line.at[idx, "p_to_mw"])
                    if idx in net.res_line.index
                    else None,
                    "q_to_mvar": _safe_float(net.res_line.at[idx, "q_to_mvar"])
                    if idx in net.res_line.index
                    else None,
                    "pl_mw": _safe_float(net.res_line.at[idx, "pl_mw"])
                    if idx in net.res_line.index
                    else None,
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
                    "pl_mw": _safe_float(net.res_trafo.at[idx, "pl_mw"])
                    if idx in net.res_trafo.index
                    else None,
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
        if 0 < vm < min_vm:
            min_vm = vm
        if vm > max_vm:
            max_vm = vm
    for br in branch_rows:
        total_loss += _safe_float(br.get("pl_mw"))
    return {
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
            return SimulationResult(
                status=SimulationStatus.FAILED, errors=["No model_id provided"]
            )

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

            sim_result = SimulationResult(
                job_id=job_id,
                status=SimulationStatus.COMPLETED,
                data=result_data,
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
            errors.append(
                ValidationError(field="model_id", message="model_id is required")
            )
        algorithm = config.get("algorithm")
        if algorithm and algorithm not in (
            "newton_raphson",
            "fast_decoupled",
            "dc",
            "acpf",
        ):
            errors.append(
                ValidationError(
                    field="algorithm", message=f"Unknown algorithm: {algorithm}"
                )
            )
        return ValidationResult(valid=len(errors) == 0, errors=errors)


__all__ = ["PandapowerPowerFlowAdapter"]
