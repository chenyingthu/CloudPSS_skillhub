from __future__ import annotations

import copy
import uuid
from datetime import datetime
from typing import Any, Optional

import numpy as np

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

_FAULT_TYPE_MAP = {
    "3phase": "3ph",
    "3ph": "3ph",
    "three_phase": "3ph",
    "1phase": "1ph",
    "slg": "1ph",
    "single_line_ground": "1ph",
    "phase-ground": "1ph",
    "2phase": "2ph",
    "ll": "2ph",
    "line_line": "2ph",
    "2phase-ground": "2phg",
    "dlg": "2phg",
    "double_line_ground": "2phg",
}


def _ensure_sc_parameters(net) -> None:
    """Ensure IEC 60909 short circuit parameters are populated."""
    # ext_grid parameters (required for slack bus)
    # Use reasonable defaults: 100 MVA is typical for smaller systems
    # This affects fault current calculation: IkSS = s_sc_max_mva / (Vn_kv * sqrt(3))
    if "s_sc_max_mva" not in net.ext_grid.columns:
        net.ext_grid["s_sc_max_mva"] = 100
    if "s_sc_min_mva" not in net.ext_grid.columns:
        net.ext_grid["s_sc_min_mva"] = 80
    if "rx_max" not in net.ext_grid.columns:
        net.ext_grid["rx_max"] = 0.1
    if "rx_min" not in net.ext_grid.columns:
        net.ext_grid["rx_min"] = 0.1
    # gen parameters - use bus voltage mapping for vn_kv
    if not net.gen.empty:
        # Map vn_kv from connected bus if not present
        if "vn_kv" not in net.gen.columns:
            net.gen["vn_kv"] = net.gen["bus"].map(net.bus["vn_kv"])
        # Fill other SC parameters
        for col in ["rdss_ohm", "xdss_pu", "xos_pu", "ros_ohm", "cos_phi", "kg"]:
            if col not in net.gen.columns:
                if col == "xdss_pu":
                    net.gen[col] = 0.2
                elif col == "xos_pu":
                    net.gen[col] = 0.1
                else:
                    net.gen[col] = 0
        net.gen = net.gen.fillna({"cos_phi": 0.8, "kg": 1, "sn_mva": 100})
    # sgen parameters
    if not net.sgen.empty:
        if "vn_kv" not in net.sgen.columns:
            net.sgen["vn_kv"] = net.sgen["bus"].map(net.bus["vn_kv"])
        net.sgen = net.sgen.fillna({"sn_mva": 1})


def _safe_float(value, default=0.0) -> float:
    try:
        if value is None or (isinstance(value, float) and value != value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


class PandapowerShortCircuitAdapter(EngineAdapter):
    _net_cache: dict[str, Any]
    _result_cache: dict[str, SimulationResult]

    def __init__(self, config: Optional[EngineConfig] = None):
        super().__init__(config)
        self._net_cache = {}
        self._result_cache = {}

    @property
    def engine_name(self) -> str:
        return "pandapower_sc"

    def get_supported_simulations(self) -> list[SimulationType]:
        return [SimulationType.SHORT_CIRCUIT]

    def _do_connect(self) -> None:
        import pandapower as pp

        self._logger.info("pandapower SC adapter ready (pandapower %s)", pp.__version__)

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
        if model_id.startswith("case"):
            from cloudpss_skills_v2.powerapi.adapters.pandapower.powerflow import (
                _load_case,
            )

            net = _load_case(model_id)
            self._net_cache[model_id] = net
            return net
        raise ValueError(f"Cannot resolve pandapower model: {model_id}")

    def _do_load_model(self, model_id: str) -> bool:
        try:
            self._resolve_net(model_id)
            return True
        except Exception:
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
            import pandapower.shortcircuit as sc

            fault_type_raw = config.get("fault_type", "3ph")
            fault_type = _FAULT_TYPE_MAP.get(fault_type_raw, "3ph")

            net_sc = copy.deepcopy(net)
            _ensure_sc_parameters(net_sc)

            sc.calc_sc(net_sc, case="max", fault=fault_type)

            bus_results = []
            if hasattr(net_sc, "res_bus_sc") and not net_sc.res_bus_sc.empty:
                for idx, row in net_sc.res_bus_sc.iterrows():
                    bus_name = (
                        str(net_sc.bus.at[idx, "name"])
                        if idx in net_sc.bus.index
                        else f"Bus_{idx}"
                    )
                    ikss = _safe_float(row.get("ikss_ka", 0))
                    ip = _safe_float(row.get("ip_ka", 0))
                    ith = _safe_float(row.get("ith_ka", 0))
                    bus_results.append(
                        {
                            "bus": bus_name,
                            "bus_index": int(idx),
                            "ikss_ka": ikss,
                            "ip_ka": ip,
                            "ith_ka": ith,
                            "v_pu": _safe_float(row.get("v_pu", 0)),
                        }
                    )

            line_results = []
            if hasattr(net_sc, "res_line_sc") and not net_sc.res_line_sc.empty:
                for idx, row in net_sc.res_line_sc.iterrows():
                    line_results.append(
                        {
                            "line_index": int(idx),
                            "ikss_ka": _safe_float(row.get("ikss_ka", 0)),
                            "ikrm_ka": _safe_float(row.get("ikrm_ka", 0)),
                        }
                    )

            max_ikss = max((b["ikss_ka"] for b in bus_results), default=0)

            result_data = {
                "model": model_id,
                "model_rid": model_id,
                "job_id": job_id,
                "fault_type": fault_type_raw,
                "standard": "IEC 60909",
                "bus_results": bus_results,
                "line_results": line_results,
                "summary": {
                    "fault_type": fault_type_raw,
                    "max_ikss_ka": round(max_ikss, 4),
                    "bus_count": len(bus_results),
                },
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

    def _do_validate_config(self, config: dict[str, Any]) -> ValidationResult:
        errors = []
        if not config.get("model_id"):
            errors.append(
                ValidationError(field="model_id", message="model_id is required")
            )
        return ValidationResult(valid=len(errors) == 0, errors=errors)


__all__ = ["PandapowerShortCircuitAdapter"]
