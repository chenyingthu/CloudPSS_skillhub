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

from cloudpss_skills_v2.core.system_model import Branch, Bus, Generator, Load, PowerSystemModel


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
        bus_number_by_id = {
            bus.bus_id: idx + 1
            for idx, bus in enumerate(model.buses)
        }
        generator_bus_ids = {
            gen.bus_id
            for gen in model.generators
            if gen.in_service and gen.bus_id in bus_number_by_id
        }
        bus_rows = []
        for idx, bus in enumerate(model.buses):
            bus_type = (
                3
                if bus.bus_type == "SLACK"
                else 2
                if bus.bus_type == "PV" or bus.bus_id in generator_bus_ids
                else 1
            )
            p_load = sum(load.p_mw for load in model.loads if load.bus_id == bus.bus_id and load.in_service)
            q_load = sum(load.q_mvar for load in model.loads if load.bus_id == bus.bus_id and load.in_service)
            bus_rows.append([
                idx + 1,
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
            if gen.bus_id not in bus_number_by_id:
                continue
            gen_rows.append([
                bus_number_by_id[gen.bus_id],
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
                    bus_number_by_id[slack.bus_id],
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
            if branch.from_bus not in bus_number_by_id or branch.to_bus not in bus_number_by_id:
                continue
            branch_rows.append([
                bus_number_by_id[branch.from_bus],
                bus_number_by_id[branch.to_bus],
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

    def from_mpc(self, mpc: dict[str, Any], *, name: str = "") -> PowerSystemModel:
        """Convert a MATPOWER case dict to a unified model."""
        bus_matrix = _as_2d_float_array(mpc.get("bus", []))
        gen_matrix = _as_2d_float_array(mpc.get("gen", []))
        branch_matrix = _as_2d_float_array(mpc.get("branch", []))
        base_mva = float(mpc.get("baseMVA", 100.0) or 100.0)

        buses = []
        bus_ids = set()
        for idx, row in enumerate(bus_matrix):
            bus_number = int(row[0])
            bus_ids.add(bus_number)
            base_kv = float(row[9]) if row.size > 9 and row[9] > 0 else 1.0
            vm_max = float(row[11]) if row.size > 11 and row[11] > 0 else 1.1
            vm_min = float(row[12]) if row.size > 12 and row[12] > 0 else 0.9
            if vm_min >= vm_max:
                vm_min, vm_max = 0.9, 1.1
            buses.append(
                Bus(
                    bus_id=bus_number,
                    name=f"Bus {bus_number}",
                    base_kv=base_kv,
                    bus_type=_matpower_bus_type(row[1] if row.size > 1 else 1),
                    v_magnitude_pu=_valid_voltage(row[7] if row.size > 7 else None),
                    v_angle_degree=_valid_angle(row[8] if row.size > 8 else None),
                    vm_max_pu=vm_max,
                    vm_min_pu=vm_min,
                    area=int(row[6]) if row.size > 6 else 1,
                    zone=int(row[10]) if row.size > 10 else 1,
                )
            )

        generators = []
        for idx, row in enumerate(gen_matrix):
            bus_id = int(row[0])
            if bus_id not in bus_ids:
                continue
            status = bool(row[7]) if row.size > 7 else True
            p_gen = float(row[1]) if row.size > 1 else 0.0
            p_max = float(row[8]) if row.size > 8 else max(p_gen, 0.0)
            p_min = float(row[9]) if row.size > 9 else min(p_gen, 0.0)
            p_min = min(p_min, p_gen)
            p_max = max(p_max, p_gen)
            generators.append(
                Generator(
                    bus_id=bus_id,
                    name=f"Gen {idx + 1} @ Bus {bus_id}",
                    p_gen_mw=p_gen,
                    q_gen_mvar=float(row[2]) if row.size > 2 else None,
                    q_max_mvar=float(row[3]) if row.size > 3 else 999999.0,
                    q_min_mvar=float(row[4]) if row.size > 4 else -999999.0,
                    v_set_pu=_valid_voltage(row[5] if row.size > 5 else None) or 1.0,
                    p_max_mw=p_max,
                    p_min_mw=p_min,
                    in_service=status,
                )
            )

        loads = []
        for row in bus_matrix:
            bus_id = int(row[0])
            p_load = float(row[2]) if row.size > 2 else 0.0
            q_load = float(row[3]) if row.size > 3 else 0.0
            if p_load or q_load:
                loads.append(
                    Load(
                        bus_id=bus_id,
                        name=f"Load @ Bus {bus_id}",
                        p_mw=p_load,
                        q_mvar=q_load,
                    )
                )

        branches = []
        for idx, row in enumerate(branch_matrix):
            from_bus = int(row[0])
            to_bus = int(row[1])
            if from_bus not in bus_ids or to_bus not in bus_ids or from_bus == to_bus:
                continue
            tap_ratio = float(row[8]) if row.size > 8 and row[8] else 1.0
            phase_shift = float(row[9]) if row.size > 9 else 0.0
            branches.append(
                Branch(
                    from_bus=from_bus,
                    to_bus=to_bus,
                    name=f"Branch {idx + 1}: {from_bus}-{to_bus}",
                    branch_type=_matpower_branch_type(tap_ratio, phase_shift),
                    r_pu=float(row[2]) if row.size > 2 else 0.0,
                    x_pu=float(row[3]) if row.size > 3 else 0.0,
                    b_pu=float(row[4]) if row.size > 4 else 0.0,
                    rate_a_mva=float(row[5]) if row.size > 5 else 0.0,
                    rate_b_mva=float(row[6]) if row.size > 6 else None,
                    rate_c_mva=float(row[7]) if row.size > 7 else None,
                    tap_ratio=tap_ratio,
                    phase_shift_degree=phase_shift,
                    in_service=bool(row[10]) if row.size > 10 else True,
                )
            )

        return PowerSystemModel(
            buses=buses,
            branches=branches,
            generators=generators,
            loads=loads,
            base_mva=base_mva,
            name=name or str(mpc.get("name", "matpower_case")),
            source_engine="matpower",
            version=str(mpc.get("version", "2")),
        )

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
            "cpf_mpopt = mpoption('verbose', 0, 'out.all', 0, 'exp.use_legacy_core', 1);",
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
    values = values[~np.isnan(values)]
    if values.size == 0:
        return None
    return float(np.nanmax(values))


def _as_2d_float_array(value: Any) -> np.ndarray:
    array = np.asarray(value, dtype=float)
    if array.size == 0:
        return np.empty((0, 0), dtype=float)
    if array.ndim == 1:
        return array.reshape((1, -1))
    return array


def _matpower_bus_type(value: float) -> str:
    bus_type = int(value)
    if bus_type == 3:
        return "SLACK"
    if bus_type == 2:
        return "PV"
    if bus_type == 4:
        return "ISOLATED"
    return "PQ"


def _matpower_branch_type(tap_ratio: float, phase_shift_degree: float) -> str:
    if abs(phase_shift_degree) > 1e-12:
        return "PHASE_SHIFTER"
    if abs(tap_ratio - 1.0) > 1e-12:
        return "TRANSFORMER"
    return "LINE"


def _valid_voltage(value: Any) -> float | None:
    if value is None:
        return None
    value = float(value)
    if 0.5 <= value <= 1.5:
        return value
    return None


def _valid_angle(value: Any) -> float | None:
    if value is None:
        return None
    value = float(value)
    if -90.0 <= value <= 90.0:
        return value
    return None


__all__ = ["MatpowerCPFAdapter", "MatpowerCPFUnavailable"]
