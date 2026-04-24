"""CloudPSS PowerFlow Adapter - Heavyweight adapter for CloudPSS power flow simulations.

Implements the EngineAdapter ABC for the CloudPSS platform, handling:
- Authentication via token
- Model loading via Model.fetch / Model.load
- Power flow execution via model.runPowerFlow
- Result extraction via result.getBuses / result.getBranches
"""

from __future__ import annotations

import re
import time
import uuid
from datetime import datetime
from typing import Any, Optional

from cloudpss_skills_v2.core.token_manager import (
    CloudPSSAdapter,
    build_cloudpss_adapter,
)
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


def _strip_html(name: str) -> str:
    return re.sub(r"<[^>]+>", "", name).strip()


_BUS_KEY_MAP = {
    "<i>V</i><sub>m</sub> / pu": "voltage_pu",
    "<i>V</i><sub>a</sub> / deg": "angle_deg",
    "<i>P</i><sub>g</sub> / MW": "generation_mw",
    "<i>Q</i><sub>g</sub> / MVar": "generation_mvar",
    "<i>P</i><sub>l</sub> / MW": "load_mw",
    "<i>Q</i><sub>l</sub> / MVar": "load_mvar",
    "Bus": "name",
    "Vm / pu": "voltage_pu",
    "Va / deg": "angle_deg",
    "Pgen / MW": "generation_mw",
    "Qgen / MVar": "generation_mvar",
    "Pload / MW": "load_mw",
    "Qload / MVar": "load_mvar",
}

_BRANCH_KEY_MAP = {
    "Branch": "name",
    "From bus": "from_bus",
    "To bus": "to_bus",
    "<i>P</i><sub>ij</sub> / MW": "p_from_mw",
    "<i>Q</i><sub>ij</sub> / MVar": "q_from_mvar",
    "<i>P</i><sub>ji</sub> / MW": "p_to_mw",
    "<i>Q</i><sub>ji</sub> / MVar": "q_to_mvar",
    "<i>P</i><sub>loss</sub> / MW": "power_loss_mw",
    "<i>Q</i><sub>loss</sub> / MVar": "reactive_loss_mvar",
    "Pij / MW": "p_from_mw",
    "Qij / MVar": "q_from_mvar",
    "Pji / MW": "p_to_mw",
    "Qji / MVar": "q_to_mvar",
    "Ploss / MW": "power_loss_mw",
    "Qloss / MVar": "reactive_loss_mvar",
}


def _normalize_bus_row(raw: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for k, v in raw.items():
        mapped = _BUS_KEY_MAP.get(k)
        if mapped:
            result[mapped] = v
            continue
        result[k] = v
    if "name" not in result and "Bus" in raw:
        result["name"] = raw["Bus"]
    result.setdefault("voltage_kv", 230)
    result.setdefault("bus_type", "pq")
    return result


def _normalize_branch_row(raw: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for k, v in raw.items():
        mapped = _BRANCH_KEY_MAP.get(k)
        if mapped:
            result[mapped] = v
            continue
        result[k] = v
    if "name" not in result and "Branch" in raw:
        result["name"] = raw["Branch"]
    result.setdefault("from_bus", raw.get("From bus", ""))
    result.setdefault("to_bus", raw.get("To bus", ""))
    result.setdefault("branch_type", "line")
    return result


def _parse_cloudpss_table(table: Any) -> list[dict[str, Any]]:
    """Parse CloudPSS SDK table format (columnar) into row dicts."""
    if table is None:
        return []
    try:
        raw_data = table
        if hasattr(table, "toJSON"):
            raw_data = table.toJSON()
        if isinstance(raw_data, dict) and "data" in raw_data:
            columns = raw_data["data"].get("columns", [])
            if not columns:
                return []
            n_rows = len(columns[0].get("data", []))
            rows = []
            for i in range(n_rows):
                row: dict[str, Any] = {}
                for col in columns:
                    clean_name = _strip_html(col["name"])
                    row[clean_name] = col["data"][i]
                rows.append(row)
            return rows
        if isinstance(raw_data, list):
            return raw_data
    except (KeyError, TypeError, AttributeError):
        pass
    return []


def _setup_auth(config: dict[str, Any]) -> CloudPSSAdapter:
    """Set up CloudPSS authentication without modifying global environment."""

    return build_cloudpss_adapter(config)


class CloudPSSPowerFlowAdapter(EngineAdapter):
    """
    CloudPSS engine adapter for power flow simulations.

    Implements the EngineAdapter ABC by delegating to the CloudPSS SDK:
    - connect: authenticate via token
    - load_model: Model.fetch(rid) or Model.load(rid)
    - run_simulation: model.runPowerFlow()
    - get_result: extract buses/branches from result
    - model manipulation: get/remove/update components, clone model
    """

    _model_cache: dict[str, Any]
    _original_rid_map: dict[str, str]

    def __init__(self, config: Optional[EngineConfig] = None):
        super().__init__(config)
        self._model_cache = {}
        self._result_cache: dict[str, SimulationResult] = {}
        self._original_rid_map = {}
        self._cloudpss = CloudPSSAdapter(
            api_url=CloudPSSAdapter.resolve_api_url(self._config.extra.get("auth", {}))
        )

    @property
    def engine_name(self) -> str:
        return "cloudpss"

    def get_supported_simulations(self) -> list[SimulationType]:
        return [SimulationType.POWER_FLOW]

    def _do_connect(self) -> None:
        auth = self._config.extra.get("auth", {})
        try:
            self._cloudpss = CloudPSSAdapter.from_config(auth)
        except ValueError as exc:
            self._logger.warning("CloudPSS token setup skipped: %s", exc)
            return

        if not self._cloudpss.connect():
            self._logger.warning("cloudpss SDK not installed; skipping token setup")

    def _do_disconnect(self) -> None:
        self._model_cache.clear()
        self._result_cache.clear()
        self._original_rid_map.clear()

    def _do_load_model(self, model_id: str) -> bool:
        from cloudpss import Model

        source = self._config.extra.get("model", {}).get("source", "cloud")
        kwargs = self._cloudpss.sdk_kwargs()

        if source == "local":
            model = Model.load(model_id)
        else:
            model = Model.fetch(model_id, **kwargs)

        self._model_cache[model_id] = model
        self._original_rid_map[model_id] = model_id
        self._logger.info(
            "Model loaded: %s (%s)",
            getattr(model, "name", model_id),
            getattr(model, "rid", model_id),
        )
        return True

    def _do_run_simulation(self, config: dict[str, Any]) -> SimulationResult:
        model_id = config.get("model_id") or self._current_model_id
        if not model_id:
            return SimulationResult(
                status=SimulationStatus.FAILED,
                errors=["No model_id provided"],
            )

        try:
            cloudpss = _setup_auth(config)
        except ValueError as e:
            return SimulationResult(
                status=SimulationStatus.FAILED,
                errors=[f"CloudPSS authentication failed: {e}"],
            )

        model = self._model_cache.get(model_id)
        if model is None:
            source = config.get("source", "cloud")
            kwargs = cloudpss.sdk_kwargs()
            try:
                from cloudpss import Model

                if source == "local":
                    model = Model.load(model_id)
                else:
                    model = Model.fetch(model_id, **kwargs)
                self._model_cache[model_id] = model
            except Exception as e:
                return SimulationResult(
                    status=SimulationStatus.FAILED,
                    errors=[f"Failed to load model {model_id}: {e}"],
                )

        job_id = str(uuid.uuid4())[:8]
        started = datetime.now()

        try:
            kwargs = cloudpss.sdk_kwargs()

            job = model.runPowerFlow(**kwargs)

            max_wait = config.get("timeout", 120)
            poll_interval = 2
            waited = 0

            sdk_status = 0
            while waited < max_wait:
                sdk_status = job.status()
                if sdk_status == 1:  # DONE
                    break
                if sdk_status == 2:  # FAILED
                    return SimulationResult(
                        job_id=job_id,
                        status=SimulationStatus.FAILED,
                        errors=["Power flow simulation failed"],
                        started_at=started,
                        completed_at=datetime.now(),
                    )
                time.sleep(poll_interval)
                waited += poll_interval

            if sdk_status != 1:
                return SimulationResult(
                    job_id=job_id,
                    status=SimulationStatus.TIMEOUT,
                    errors=[f"Simulation timed out after {waited}s"],
                    started_at=started,
                    completed_at=datetime.now(),
                )

            pf_result = job.result
            if pf_result is None:
                return SimulationResult(
                    job_id=job_id,
                    status=SimulationStatus.FAILED,
                    errors=["Power flow result is empty"],
                    started_at=started,
                    completed_at=datetime.now(),
                )

            bus_rows = _parse_cloudpss_table(pf_result.getBuses())
            branch_rows = _parse_cloudpss_table(pf_result.getBranches())

            normalized_buses = [_normalize_bus_row(b) for b in bus_rows]
            normalized_branches = [_normalize_branch_row(b) for b in branch_rows]

            summary = _generate_pf_summary(normalized_buses, normalized_branches)

            result_data = {
                "model": getattr(model, "name", model_id),
                "model_rid": model.rid if hasattr(model, "rid") else model_id,
                "job_id": getattr(job, "id", job_id),
                "converged": True,
                "bus_count": len(normalized_buses),
                "branch_count": len(normalized_branches),
                "buses": normalized_buses,
                "branches": normalized_branches,
                "summary": summary,
            }

            sim_result = SimulationResult(
                job_id=getattr(job, "id", job_id),
                status=SimulationStatus.COMPLETED,
                data=result_data,
                started_at=started,
                completed_at=datetime.now(),
            )

            self._result_cache[getattr(job, "id", job_id)] = sim_result
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

    # --- Model manipulation _do_* implementations ---

    _BRANCH_DEFINITIONS = [
        "model/CloudPSS/line",
        "model/CloudPSS/3pline",
        "model/CloudPSS/transformer",
        "model/CloudPSS/3ptransformer",
        "model/CloudPSS/TransmissionLine",
        "model/CloudPSS/_newTransformer_3p2w",
        "model/CloudPSS/_newTransformer_3p",
    ]

    _LOAD_DEFINITIONS = ["Load", "_newExpLoad", "_newLoad"]

    _GENERATOR_DEFINITIONS = ["Generator", "Gen", "SyncGenerator", "_newGenerator"]

    _TRANSFORMER_DEFINITIONS = [
        "transformer",
        "3ptransformer",
        "_newTransformer_3p2w",
        "_newTransformer_3p",
    ]

    @staticmethod
    def _classify_component(definition: str) -> str:
        d = str(definition)
        d_lower = d.lower()

        for branch_def in CloudPSSPowerFlowAdapter._BRANCH_DEFINITIONS:
            if branch_def in d:
                if any(
                    t in d_lower
                    for t in CloudPSSPowerFlowAdapter._TRANSFORMER_DEFINITIONS
                ):
                    return ComponentType.TRANSFORMER
                return ComponentType.BRANCH

        for load_def in CloudPSSPowerFlowAdapter._LOAD_DEFINITIONS:
            if load_def in d:
                return ComponentType.LOAD

        for gen_def in CloudPSSPowerFlowAdapter._GENERATOR_DEFINITIONS:
            if gen_def in d:
                return ComponentType.GENERATOR

        return ComponentType.OTHER

    def _ensure_model_loaded(self, model_id: str) -> Any:
        model = self._model_cache.get(model_id)
        if model is not None:
            return model
        from cloudpss import Model

        source = self._config.extra.get("model", {}).get("source", "cloud")
        kwargs = self._cloudpss.sdk_kwargs()
        if source == "local":
            model = Model.load(model_id)
        else:
            model = Model.fetch(model_id, **kwargs)
        self._model_cache[model_id] = model
        return model

    def _do_get_components(self, model_id: str) -> list[ComponentInfo]:
        model = self._ensure_model_loaded(model_id)
        components = model.getAllComponents()
        result = []
        for comp_id, comp in components.items():
            definition = getattr(comp, "definition", "")
            result.append(
                ComponentInfo(
                    key=comp_id,
                    name=getattr(comp, "name", getattr(comp, "label", comp_id)),
                    definition=definition,
                    component_type=self._classify_component(definition),
                    args=dict(getattr(comp, "args", {}))
                    if hasattr(comp, "args") and comp.args
                    else None,
                )
            )
        return result

    def _do_get_components_by_type(
        self, model_id: str, comp_type: str
    ) -> list[ComponentInfo]:
        model = self._ensure_model_loaded(model_id)
        components = model.getAllComponents()
        result = []
        for comp_id, comp in components.items():
            definition = getattr(comp, "definition", "")
            classified = self._classify_component(definition)
            if classified == comp_type:
                result.append(
                    ComponentInfo(
                        key=comp_id,
                        name=getattr(comp, "name", getattr(comp, "label", comp_id)),
                        definition=definition,
                        component_type=classified,
                        args=dict(getattr(comp, "args", {}))
                        if hasattr(comp, "args") and comp.args
                        else None,
                    )
                )
        return result

    def _do_remove_component(self, model_id: str, component_key: str) -> bool:
        model = self._ensure_model_loaded(model_id)
        try:
            if hasattr(model, "removeComponent"):
                model.removeComponent(component_key)
                return True
            components = model.getAllComponents()
            if component_key in components:
                del components[component_key]
                return True
        except Exception:
            pass
        return False

    def _do_update_component_args(
        self, model_id: str, component_key: str, args: dict[str, Any]
    ) -> bool:
        model = self._ensure_model_loaded(model_id)
        try:
            if hasattr(model, "updateComponent"):
                model.updateComponent(component_key, args=args)
                return True
            comp = model.getComponent(component_key)
            if hasattr(comp, "update_args"):
                comp.update_args(args)
                return True
            if hasattr(comp, "args"):
                comp.args = args
                return True
        except Exception:
            pass
        return False

    def _do_clone_model(self, model_id: str) -> str:
        original_rid = self._original_rid_map.get(model_id, model_id)
        from cloudpss import Model

        source = self._config.extra.get("model", {}).get("source", "cloud")
        kwargs = self._cloudpss.sdk_kwargs()

        if source == "local":
            new_model = Model.load(original_rid)
        else:
            new_model = Model.fetch(original_rid, **kwargs)

        clone_id = f"{original_rid}__clone_{uuid.uuid4().hex[:8]}"
        self._model_cache[clone_id] = new_model
        self._original_rid_map[clone_id] = original_rid
        return clone_id

    def _do_validate_config(self, config: dict[str, Any]) -> ValidationResult:
        errors = []
        model_id = config.get("model_id")
        if not model_id:
            errors.append(
                ValidationError(field="model_id", message="model_id is required")
            )
        algorithm = config.get("algorithm")
        if algorithm and algorithm not in ("newton_raphson", "fast_decoupled", "acpf"):
            errors.append(
                ValidationError(
                    field="algorithm", message=f"Unknown algorithm: {algorithm}"
                )
            )
        return ValidationResult(valid=len(errors) == 0, errors=errors)


def _generate_pf_summary(
    bus_rows: list[dict[str, Any]], branch_rows: list[dict[str, Any]]
) -> dict[str, Any]:
    """Generate power flow summary statistics from normalized result rows."""
    total_p_gen = 0.0
    total_q_gen = 0.0
    total_p_load = 0.0
    total_q_load = 0.0
    total_loss = 0.0
    min_voltage = 999.0
    max_voltage = 0.0

    for bus in bus_rows:
        p_gen = _as_float(bus.get("generation_mw") or bus.get("Pg"))
        q_gen = _as_float(bus.get("generation_mvar") or bus.get("Qg"))
        p_load = _as_float(bus.get("load_mw") or bus.get("Pl"))
        q_load = _as_float(bus.get("load_mvar") or bus.get("Ql"))
        vm = _as_float(bus.get("voltage_pu") or bus.get("Vm"), 1.0)

        total_p_gen += p_gen
        total_q_gen += q_gen
        total_p_load += p_load
        total_q_load += q_load
        if 0 < vm < min_voltage:
            min_voltage = vm
        if vm > max_voltage:
            max_voltage = vm

    for branch in branch_rows:
        p_loss = _as_float(
            branch.get("power_loss_mw") or branch.get("Ploss") or branch.get("P_loss")
        )
        total_loss += p_loss

    return {
        "total_generation": {
            "p_mw": round(total_p_gen, 2),
            "q_mvar": round(total_q_gen, 2),
        },
        "total_load": {
            "p_mw": round(total_p_load, 2),
            "q_mvar": round(total_q_load, 2),
        },
        "total_loss_mw": round(total_loss, 4),
        "voltage_range": {
            "min_pu": round(min_voltage, 4),
            "max_pu": round(max_voltage, 4),
        },
    }


def _as_float(value, default=0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


__all__ = ["CloudPSSPowerFlowAdapter"]
