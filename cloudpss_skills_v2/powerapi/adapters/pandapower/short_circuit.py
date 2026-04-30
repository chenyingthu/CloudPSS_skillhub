from __future__ import annotations

import copy
import uuid
from datetime import datetime
from pathlib import Path
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
        model_file = config.get("model_file") or model_id
        if (
            isinstance(model_file, str)
            and model_file.endswith(".json")
            and Path(model_file).exists()
        ):
            from cloudpss_skills_v2.powerapi.adapters.pandapower.powerflow import (
                load_net_from_json,
            )

            net = load_net_from_json(model_file)
            self._net_cache[model_id] = net
            return net
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
                        str(net_sc.bus.at[idx, "name"]) if idx in net_sc.bus.index else f"Bus_{idx}"
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
            errors.append(ValidationError(field="model_id", message="model_id is required"))
        return ValidationResult(valid=len(errors) == 0, errors=errors)


__all__ = ["PandapowerShortCircuitAdapter", "VSCConverter", "VSCNrSolver"]


# =============================================================================
# VSC Short-Circuit Solver - Based on Paper doi:10.1016/j.ijepes.2024.109839
# =============================================================================

class VSCConverter:
    """VSC Converter: compute i_p, i_q based on local voltage."""
    
    def __init__(self, bus_index: int, p_ref: float = 0.0, q_ref: float = 0.0, 
                 i_max: float = 1.2, mode: str = "PSS"):
        self.bus_index = bus_index
        self.p_ref = p_ref
        self.q_ref = q_ref
        self.i_max = i_max
        self.mode = mode
        self.is_saturated = False
    
    def compute_current(self, v_mag: float) -> tuple[float, float]:
        """Compute (i_p, i_q) from P/Q refs at given voltage (all in PU)."""
        if v_mag < 1e-6:
            return 0.0, 0.0
        
        i_p = self.p_ref / v_mag
        i_q = self.q_ref / v_mag
        i_mag = np.sqrt(i_p**2 + i_q**2)
        
        if i_mag > self.i_max:
            self.is_saturated = True
            return self._saturate(i_p, i_q, i_mag)
        
        self.is_saturated = False
        return i_p, i_q
    
    def _saturate(self, i_p: float, i_q: float, i_mag: float) -> tuple[float, float]:
        if self.mode == "FSS":
            i_q_sat = min(self.i_max, abs(i_q))
            i_p_sat = np.sqrt(max(0, self.i_max**2 - i_q_sat**2))
            return i_p_sat if i_p >= 0 else -i_p_sat, i_q_sat
        else:
            scale = self.i_max / i_mag
            return i_p * scale, i_q * scale


class VSCNrSolver:
    """Extended NR solver for short-circuit with VSC converters.
    
    Paper algorithm (doi:10.1016/j.ijepes.2024.109839):
    1. Build Y in PU (S_base=100MVA)
    2. Add ext_grid as Norton: I_sc = S_sc/S_base
    3. Add fault impedance
    4. Initialize V = 1 at slack
    5. Iterate: compute VSC currents → solve Y@V=I → check convergence
    """
    
    def __init__(self, tolerance: float = 1e-6, max_iter: int = 50):
        self.tolerance = tolerance
        self.max_iter = max_iter
        self.iterations = 0
        self.converged = False
        self._V_pu = None
        self._I_base = None
    
    def solve(self, net, fault_bus: int, fault_z: float = 0.01, 
              converters: dict[int, VSCConverter] = None) -> tuple[np.ndarray, bool]:
        """Solve using NR iteration (all in PU)."""
        converters = converters or {}
        n = len(net.bus)
        
        # Base values
        S_base = 100.0  # MVA
        slack_bus = 0
        V_base_kV = float(net.bus.at[slack_bus, "vn_kv"])
        self._I_base = S_base / (np.sqrt(3) * V_base_kV)  # kA
        
        # Build Y in PU
        Y = self._build_Y_pu(net, S_base)
        
        # Add fault
        Y[fault_bus, fault_bus] += 1 / complex(fault_z, 0)
        
        # Add ext_grid: Y_th = S_base/S_sc at slack
        S_sc = float(net.ext_grid.at[0, "s_sc_max_mva"])
        Y_th = S_sc / S_base
        Y[slack_bus, slack_bus] += Y_th
        
        # Initial V
        V = np.ones(n, dtype=complex)
        
        # NR Iteration - use current source model
        # Compute I from ext_grid and VSC converters
        S_sc = float(net.ext_grid.at[0, "s_sc_max_mva"])  # MVA
        I_sc_pu = S_sc / S_base  # Norton current: 1/Z_th = S_sc/S_base in pu
        
        for it in range(self.max_iter):
            V_old = V.copy()
            
            # Build current injection vector
            I = np.zeros(n, dtype=complex)
            I[slack_bus] = I_sc_pu  # Ext grid as current source
            
            # Update VSC currents
            for bus_idx, vsc in converters.items():
                v_mag = abs(V[bus_idx])
                i_p, i_q = vsc.compute_current(max(v_mag, 0.01))
                I[bus_idx] = complex(i_p, -i_q)
            
            # Solve
            try:
                V = np.linalg.solve(Y, I)
            except:
                V = np.linalg.pinv(Y) @ I
            
            V[slack_bus] = complex(1.0, 0)
            
            # Check convergence
            if it > 0:
                delta = np.max(np.abs(np.abs(V) - np.abs(V_old)))
                if delta < self.tolerance:
                    self.converged = True
                    break
            
            self.iterations = it
        
        self._V_pu = V
        return V, self.converged
    
    def _build_Y_pu(self, net: Any, S_base: float) -> np.ndarray:
        """Build Y matrix in per-unit (R_pu, X_pu directly from pandapower)."""
        from dataclasses import asdict
        n = len(net.bus)
        Y = np.zeros((n, n), dtype=complex)
        
        # Lines: r, x already in pu if < 1.0, or convert
        if hasattr(net, "line") and not net.line.empty:
            for _, line in net.line.iterrows():
                f = int(line["from_bus"])
                t = int(line["to_bus"])
                # r, x in pu or ohms
                r = line.get("r_ohm_per_km", 0)
                x = line.get("x_ohm_per_km", 0)
                length = line.get("length_km", 1)
                
                # Simple: assume pu if < 1
                z = complex(r * length, x * length)
                if abs(z) > 1e-9:
                    y = 1 / z
                else:
                    y = 1e6
                Y[f, f] += y
                Y[f, t] -= y
                Y[t, f] -= y
                Y[t, t] += y
        
        return Y
    
    def get_fault_current_kA(self, fault_bus: int, fault_z: float) -> float:
        """Convert fault current to kA."""
        V = self._V_pu
        Ik_pu = abs(V[fault_bus] / complex(fault_z, 0))
        return Ik_pu * self._I_base
