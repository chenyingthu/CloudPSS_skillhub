"""MATPOWER continuation power-flow adapter.

This adapter is optional: it requires Octave/MATLAB plus the Python
``matpower`` bridge. It keeps all MATPOWER-specific conversion and runtime
checks outside the analysis skill so missing external tools fail explicitly.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.util import find_spec
from shutil import which
from typing import Any

import numpy as np

from cloudpss_skills_v2.core.system_model import PowerSystemModel


class MatpowerCPFUnavailable(RuntimeError):
    """Raised when the optional MATPOWER CPF runtime is not available."""


@dataclass
class MatpowerCPFAdapter:
    """Thin wrapper around MATPOWER ``runcpf``."""

    backend: str = "auto"

    @staticmethod
    def runtime_status() -> dict[str, Any]:
        octave_path = which("octave")
        matlab_path = which("matlab")
        matpower_python = _module_available("matpower")
        oct2py = _module_available("oct2py")
        matlab_engine = _module_available("matlab.engine")
        available_octave = bool(oct2py and octave_path)
        available_matlab = bool(matlab_engine)
        return {
            "matpower_python": matpower_python,
            "oct2py": oct2py,
            "matlab_engine": matlab_engine,
            "octave": octave_path,
            "matlab": matlab_path,
            "available_octave": available_octave,
            "available_matlab": available_matlab,
            "available": bool(matpower_python and (available_octave or available_matlab)),
        }

    def ensure_available(self) -> None:
        status = self.runtime_status()
        if not status["matpower_python"]:
            raise MatpowerCPFUnavailable("Python package 'matpower' is not installed")
        if self.backend == "auto":
            if not (status["available_octave"] or status["available_matlab"]):
                raise MatpowerCPFUnavailable(
                    "No MATPOWER runtime is available: install Octave plus 'oct2py' "
                    "or install MATLAB Engine for Python"
                )
            return
        if self.backend == "matlab":
            if not status["matlab_engine"]:
                raise MatpowerCPFUnavailable("Python package 'matlab.engine' is not installed")
            return
        if self.backend != "octave":
            raise MatpowerCPFUnavailable(
                f"Unsupported MATPOWER backend '{self.backend}'; use 'auto', 'octave', or 'matlab'"
            )
        if not status["oct2py"]:
            raise MatpowerCPFUnavailable("Python package 'oct2py' is not installed")
        if not status["octave"]:
            raise MatpowerCPFUnavailable("Octave is not available on PATH")

    def build_cases(
        self,
        model: PowerSystemModel,
        *,
        target_scale: float = 2.0,
        load_bus_ids: list[int] | None = None,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        base = self.to_mpc(model)
        target = {
            "version": base["version"],
            "baseMVA": base["baseMVA"],
            "bus": np.array(base["bus"], dtype=float, copy=True),
            "gen": np.array(base["gen"], dtype=float, copy=True),
            "branch": np.array(base["branch"], dtype=float, copy=True),
        }

        selected = set(load_bus_ids or [])
        for idx, bus_row in enumerate(target["bus"]):
            bus_id = int(bus_row[0])
            if selected and bus_id not in selected:
                continue
            target["bus"][idx, 2] *= target_scale
            target["bus"][idx, 3] *= target_scale

        return base, target

    def to_mpc(self, model: PowerSystemModel) -> dict[str, Any]:
        """Convert a unified model to a MATPOWER case dict."""
        bus_rows = []
        for bus in model.buses:
            bus_type = 3 if bus.bus_type == "SLACK" else 2 if bus.bus_type == "PV" else 1
            p_load = sum(load.p_mw for load in model.loads if load.bus_id == bus.bus_id and load.in_service)
            q_load = sum(load.q_mvar for load in model.loads if load.bus_id == bus.bus_id and load.in_service)
            bus_rows.append([
                bus.bus_id,
                bus_type,
                p_load,
                q_load,
                0.0,
                0.0,
                bus.area,
                bus.v_magnitude_pu or 1.0,
                bus.v_angle_degree or 0.0,
                bus.base_kv,
                bus.zone,
                bus.vm_max_pu,
                bus.vm_min_pu,
            ])

        gen_rows = []
        for gen in model.generators:
            if not gen.in_service:
                continue
            gen_rows.append([
                gen.bus_id,
                gen.p_gen_mw,
                gen.q_gen_mvar or 0.0,
                gen.q_max_mvar,
                gen.q_min_mvar,
                gen.v_set_pu or 1.0,
                model.base_mva,
                1,
                gen.p_max_mw,
                gen.p_min_mw,
            ])

        if not gen_rows:
            slack = model.get_slack_bus()
            if slack is not None:
                gen_rows.append([
                    slack.bus_id,
                    model.total_load_mw(),
                    0.0,
                    999999.0,
                    -999999.0,
                    slack.v_magnitude_pu or 1.0,
                    model.base_mva,
                    1,
                    999999.0,
                    -999999.0,
                ])

        branch_rows = []
        for branch in model.branches:
            if not branch.in_service:
                continue
            branch_rows.append([
                branch.from_bus,
                branch.to_bus,
                branch.r_pu,
                branch.x_pu,
                branch.b_pu,
                branch.rate_a_mva or 0.0,
                branch.rate_b_mva or 0.0,
                branch.rate_c_mva or 0.0,
                branch.tap_ratio,
                branch.phase_shift_degree,
                1,
                -360.0,
                360.0,
            ])

        return {
            "version": "2",
            "baseMVA": model.base_mva,
            "bus": np.array(bus_rows, dtype=float),
            "gen": np.array(gen_rows, dtype=float),
            "branch": np.array(branch_rows, dtype=float),
        }

    def run_cpf(
        self,
        model: PowerSystemModel,
        *,
        target_scale: float = 2.0,
        load_bus_ids: list[int] | None = None,
    ) -> dict[str, Any]:
        """Run MATPOWER runcpf and normalize the result."""
        self.ensure_available()

        import matpower

        base, target = self.build_cases(
            model,
            target_scale=target_scale,
            load_bus_ids=load_bus_ids,
        )
        engine = self._select_engine()
        mp = matpower.start_instance(engine=engine)
        try:
            if engine == "matlab":
                result = mp.runcpf(base, target, nargout=2)
            elif engine == "octave":
                result = self._run_octave_cpf(mp, base, target)
            else:
                result = mp.runcpf(base, target)
        finally:
            self._stop_session(mp)

        return self._normalize_result(result)

    @staticmethod
    def _run_octave_cpf(mp: Any, base: dict[str, Any], target: dict[str, Any]) -> dict[str, Any]:
        """Run CPF in Octave without returning MATPOWER's full object graph."""
        mp.push("cpf_base_case", base, verbose=False)
        mp.push("cpf_target_case", target, verbose=False)
        mp.eval(
            "cpf_mpopt = mpoption('verbose', 0, 'out.all', 0);",
            verbose=False,
        )
        mp.eval(
            "[cpf_results, cpf_success] = runcpf(cpf_base_case, cpf_target_case, cpf_mpopt);",
            verbose=False,
        )
        mp.eval(
            "cpf_lam = []; cpf_v = []; cpf_max_lam = NaN;"
            "if isfield(cpf_results, 'cpf'); "
            "  if isfield(cpf_results.cpf, 'lam_c'); cpf_lam = cpf_results.cpf.lam_c; "
            "  elseif isfield(cpf_results.cpf, 'lam'); cpf_lam = cpf_results.cpf.lam; endif; "
            "  if isfield(cpf_results.cpf, 'V_c'); cpf_v = cpf_results.cpf.V_c; "
            "  elseif isfield(cpf_results.cpf, 'V'); cpf_v = cpf_results.cpf.V; endif; "
            "  if isfield(cpf_results.cpf, 'max_lam'); cpf_max_lam = cpf_results.cpf.max_lam; endif; "
            "endif;",
            verbose=False,
        )
        cpf = {
            "lam": mp.pull("cpf_lam", verbose=False),
            "V": mp.pull("cpf_v", verbose=False),
            "max_lam": mp.pull("cpf_max_lam", verbose=False),
        }
        success = mp.pull("cpf_success", verbose=False)
        return {
            "cpf": cpf,
            "success": bool(np.asarray(success).reshape(-1)[0]),
        }

    @staticmethod
    def _normalize_result(result: Any) -> dict[str, Any]:
        success = None
        if isinstance(result, (list, tuple)) and result:
            data = result[0] if isinstance(result[0], dict) else {}
            if len(result) > 1:
                success = result[1]
        else:
            data = result if isinstance(result, dict) else {}
        cpf = data.get("cpf", {}) if isinstance(data, dict) else {}
        if success is None and isinstance(data, dict):
            success = data.get("success", True)
        return {
            "raw_result": data,
            "cpf": cpf,
            "max_lambda": _extract_max_lambda(cpf),
            "success": bool(success),
        }

    def _select_engine(self) -> str:
        if self.backend in {"octave", "matlab"}:
            return self.backend

        status = self.runtime_status()
        if status["available_octave"]:
            return "octave"
        if status["available_matlab"]:
            return "matlab"
        raise MatpowerCPFUnavailable(
            "No MATPOWER runtime is available: install Octave plus 'oct2py' "
            "or install MATLAB Engine for Python"
        )

    @staticmethod
    def _stop_session(mp: Any) -> None:
        exit_method = getattr(type(mp), "exit", None)
        if callable(exit_method):
            exit_method(mp)


def _module_available(name: str) -> bool:
    try:
        return find_spec(name) is not None
    except (ImportError, ValueError):
        return False


def _extract_max_lambda(cpf: dict[str, Any]) -> float | None:
    value = cpf.get("max_lam")
    if value is None:
        value = cpf.get("lam_c")
    if value is None:
        value = cpf.get("lam")
    if value is None:
        return None

    values = np.asarray(value).reshape(-1)
    if values.size == 0:
        return None
    return float(np.nanmax(values))


__all__ = ["MatpowerCPFAdapter", "MatpowerCPFUnavailable"]
