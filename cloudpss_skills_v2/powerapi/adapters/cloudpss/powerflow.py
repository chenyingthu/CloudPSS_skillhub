"""CloudPSS PowerFlow Adapter - Heavyweight adapter for CloudPSS power flow simulations.

Implements the EngineAdapter ABC for the CloudPSS platform, handling:
- Authentication via token
- Model loading via Model.fetch / Model.load
- Power flow execution via model.runPowerFlow
- Result extraction via result.getBuses / result.getBranches
- Conversion to unified PowerSystemModel (new architecture)
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

# New architecture: Unified model conversion
from cloudpss_skills_v2.core.system_model import (
    Bus,
    Branch,
    Generator,
    Load,
    PowerSystemModel,
)


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


def _cloudpss_arg_value(value: Any) -> Any:
    """Extract the scalar payload from CloudPSS expression wrappers."""
    if isinstance(value, dict):
        if "source" in value:
            return value.get("source")
        if "value" in value:
            return value.get("value")
    return value


def _first_present(data: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in data and data[key] not in (None, ""):
            return data[key]
    return None


def _parse_cloudpss_table(table: Any) -> list[dict[str, Any]]:
    """Parse CloudPSS SDK table format (columnar) into row dicts."""
    if table is None:
        return []
    try:
        raw_data = table
        if hasattr(table, "toJSON"):
            raw_data = table.toJSON()
        if isinstance(raw_data, list) and len(raw_data) > 0:
            first = raw_data[0]
            if isinstance(first, dict):
                is_component = (
                    first.get("type") == "table"
                    or (
                        "data" in first
                        and isinstance(first.get("data"), dict)
                        and "columns" in first.get("data")
                    )
                    or (
                        "key" in first
                        and "version" in first
                    )
                )
                if not is_component:
                    return raw_data
            raw_data = first
        if isinstance(raw_data, dict):
            if "data" in raw_data and isinstance(raw_data["data"], dict):
                columns = raw_data["data"].get("columns", [])
            elif raw_data.get("type") == "table":
                columns = raw_data.get("data", {}).get("columns", [])
            else:
                columns = []
            if columns:
                n_rows = len(columns[0].get("data", []))
                rows = []
                for i in range(n_rows):
                    row = {}
                    for col in columns:
                        clean_name = _strip_html(str(col.get("name", "")))
                        row[clean_name] = col.get("data", [None])[i] if i < len(col.get("data", [])) else None
                    rows.append(row)
                return rows
    except (KeyError, TypeError, AttributeError):
        pass
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
        if isinstance(raw_data, list) and len(raw_data) > 0:
            if all(isinstance(item, dict) for item in raw_data):
                return raw_data
            raw_data = raw_data[0]
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
        self._unified_model_cache: dict[str, PowerSystemModel] = {}
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
        base_url = self._config.base_url or auth.get("base_url") or auth.get("baseUrl")
        if base_url:
            auth = {**auth, "base_url": base_url}
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
        self._unified_model_cache.clear()

    def get_unified_model(self, job_id: str) -> PowerSystemModel | None:
        """Get unified PowerSystemModel for a completed job.

        This is the new architecture method for accessing results
        in a engine-agnostic format.

        Args:
            job_id: The simulation job ID

        Returns:
            Unified PowerSystemModel or None if not found
        """
        return self._unified_model_cache.get(job_id)

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

        cloudpss = self._cloudpss
        per_call_auth = config.get("auth") or {}
        per_call_base_url = per_call_auth.get("base_url") or per_call_auth.get("baseUrl")
        if per_call_base_url:
            cloudpss = CloudPSSAdapter(
                token=self._cloudpss.token,
                api_url=per_call_base_url,
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
            self._enrich_rows_from_model_components(
                model,
                normalized_buses,
                normalized_branches,
            )

            summary = _generate_pf_summary(normalized_buses, normalized_branches)

            # Build unified PowerSystemModel (new architecture)
            system_model = self._to_unified_model(
                normalized_buses, normalized_branches, base_mva=100.0
            )

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
                system_model=system_model,  # New architecture: unified model
            )

            # Cache the unified model separately for retrieval via get_unified_model()
            job_id_key = getattr(job, "id", job_id)
            self._unified_model_cache[job_id_key] = system_model

            self._result_cache[job_id_key] = sim_result
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

    _BUS_DEFINITIONS = [
        "model/CloudPSS/_newBus_3p",
        "model/CloudPSS/Bus",
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

    @staticmethod
    def _is_bus_definition(definition: str) -> bool:
        d = str(definition)
        return any(bus_def in d for bus_def in CloudPSSPowerFlowAdapter._BUS_DEFINITIONS)

    @classmethod
    def _component_args(cls, component: Any) -> dict[str, Any]:
        args = getattr(component, "args", None)
        if not isinstance(args, dict):
            return {}
        return {
            key: _cloudpss_arg_value(value)
            for key, value in args.items()
        }

    def _enrich_rows_from_model_components(
        self,
        model: Any,
        bus_rows: list[dict[str, Any]],
        branch_rows: list[dict[str, Any]],
    ) -> None:
        """Merge static CloudPSS model parameters into power-flow result rows."""
        try:
            components = model.getAllComponents()
        except Exception as exc:
            self._logger.debug("Could not read CloudPSS components for unified enrichment: %s", exc)
            return

        bus_params_by_component_id: dict[str, dict[str, Any]] = {}
        bus_params_by_node_name: dict[str, dict[str, Any]] = {}
        branch_params_by_component_id: dict[str, dict[str, Any]] = {}

        for component_id, component in components.items():
            definition = getattr(component, "definition", "")
            args = self._component_args(component)

            if self._is_bus_definition(definition):
                params = self._extract_bus_component_parameters(component, args)
                if params:
                    bus_params_by_component_id[str(component_id)] = params
                    node_name = params.get("node_name")
                    if node_name:
                        bus_params_by_node_name[str(node_name)] = params
                continue

            component_type = self._classify_component(definition)
            if component_type in (ComponentType.BRANCH, ComponentType.TRANSFORMER):
                params = self._extract_branch_component_parameters(
                    str(component_id),
                    component,
                    args,
                    component_type,
                )
                if params:
                    branch_params_by_component_id[str(component_id)] = params

        for row in bus_rows:
            params = bus_params_by_component_id.get(str(row.get("name")))
            if params is None:
                params = bus_params_by_node_name.get(str(row.get("Node", "")))
            if params:
                self._merge_missing_values(row, params, override_keys={"voltage_kv"})

        for row in branch_rows:
            params = branch_params_by_component_id.get(str(row.get("name")))
            if params:
                self._merge_missing_values(
                    row,
                    params,
                    override_keys={"branch_type"},
                )

    @staticmethod
    def _merge_missing_values(
        row: dict[str, Any],
        params: dict[str, Any],
        *,
        override_keys: set[str] | None = None,
    ) -> None:
        override_keys = override_keys or set()
        for key, value in params.items():
            if value in (None, ""):
                continue
            if key in override_keys or key not in row or row[key] in (None, ""):
                row[key] = value

    def _extract_bus_component_parameters(
        self,
        component: Any,
        args: dict[str, Any],
    ) -> dict[str, Any]:
        pins = getattr(component, "pins", {})
        node_name = None
        if isinstance(pins, dict):
            node_name = _first_present(pins, "0")

        return {
            "node_name": node_name,
            "voltage_kv": self._parse_float(
                _first_present(args, "VBase", "Vbase", "base_kv", "voltage_kv"),
                None,
            ),
            "frequency_hz": self._parse_float(_first_present(args, "Freq", "freq"), None),
        }

    def _extract_branch_component_parameters(
        self,
        component_id: str,
        component: Any,
        args: dict[str, Any],
        component_type: str,
    ) -> dict[str, Any]:
        if component_type == ComponentType.TRANSFORMER:
            return self._extract_transformer_component_parameters(component_id, component, args)
        return self._extract_line_component_parameters(component_id, component, args)

    def _extract_line_component_parameters(
        self,
        component_id: str,
        component: Any,
        args: dict[str, Any],
    ) -> dict[str, Any]:
        r_pu = self._parse_float(_first_present(args, "R1pu", "r_pu", "Rpu"), None)
        x_pu = self._parse_float(_first_present(args, "X1pu", "x_pu", "Xpu"), None)
        b_pu = self._parse_float(_first_present(args, "B1pu", "b_pu", "Bpu"), None)
        sbase = self._parse_float(_first_present(args, "Sbase", "base_mva"), None)
        vbase = self._parse_float(_first_present(args, "Vbase", "VBase", "base_kv"), None)
        rate = self._parse_float(_first_present(args, "Rate", "rate_a_mva", "Smva"), None)
        irated = self._parse_float(_first_present(args, "Irated", "Ir"), None)
        if rate is None and irated is not None and irated > 0 and vbase:
            rate = (3**0.5) * vbase * irated

        return {
            "branch_type": "line",
            "r_pu": r_pu,
            "x_pu": x_pu,
            "b_pu": b_pu,
            "rate_a_mva": rate,
            "parameter_source": "cloudpss_model_component",
            "parameter_component_id": component_id,
            "parameter_component_definition": getattr(component, "definition", ""),
            "parameter_base_mva": sbase,
            "parameter_base_kv": vbase,
            "static_name": _first_present(args, "Name"),
        }

    def _extract_transformer_component_parameters(
        self,
        component_id: str,
        component: Any,
        args: dict[str, Any],
    ) -> dict[str, Any]:
        r_pu = self._parse_float(_first_present(args, "Rl", "r_pu", "Rpu"), 0.0)
        x_pu = self._parse_float(_first_present(args, "Xl", "Xac", "x_pu", "Xpu"), None)
        rate = self._parse_float(_first_present(args, "Tmva", "Smva", "rate_a_mva"), None)
        vbase = self._parse_float(_first_present(args, "V1", "Vbase", "VBase"), None)
        tap_ratio = self._parse_float(_first_present(args, "InitTap", "Tap", "tap_ratio"), None)

        return {
            "branch_type": "transformer",
            "r_pu": r_pu,
            "x_pu": x_pu,
            "rate_a_mva": rate,
            "tap_ratio": tap_ratio,
            "parameter_source": "cloudpss_model_component",
            "parameter_component_id": component_id,
            "parameter_component_definition": getattr(component, "definition", ""),
            "parameter_base_mva": rate,
            "parameter_base_kv": vbase,
            "static_name": _first_present(args, "Name"),
        }

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

    # -------------------------------------------------------------------------
    # Unified Model Conversion (New Architecture)
    # -------------------------------------------------------------------------

    def _to_unified_model(
        self,
        bus_rows: list[dict[str, Any]],
        branch_rows: list[dict[str, Any]],
        base_mva: float = 100.0,
    ) -> PowerSystemModel:
        """Convert CloudPSS result to unified PowerSystemModel.

        Args:
            bus_rows: Normalized bus data from CloudPSS
            branch_rows: Normalized branch data from CloudPSS
            base_mva: System base MVA

        Returns:
            Unified PowerSystemModel with DataClass components
        """
        buses = self._convert_buses_to_unified(bus_rows)
        # Build name to index mapping for branch connection lookup
        bus_name_to_idx = {b.name: i for i, b in enumerate(buses)}
        branches = self._convert_branches_to_unified(branch_rows, bus_name_to_idx)
        generators = self._extract_generators_from_buses(bus_rows)
        loads = self._extract_loads_from_buses(bus_rows)

        return PowerSystemModel(
            buses=buses,
            branches=branches,
            generators=generators,
            loads=loads,
            base_mva=base_mva,
            source_engine="cloudpss",
        )

    def _convert_buses_to_unified(
        self, bus_rows: list[dict[str, Any]]
    ) -> list[Bus]:
        """Convert CloudPSS bus rows to unified Bus DataClass."""
        buses = []

        for idx, row in enumerate(bus_rows):
            # Determine bus type from data or infer
            bus_type = self._infer_bus_type(row)

            # Get voltage (may be from results or default)
            v_mag = self._parse_float(row.get("voltage_pu"))
            v_ang = self._parse_float(row.get("angle_deg"))

            # Get net injection (generation - load)
            p_gen = self._parse_float(row.get("generation_mw"), 0.0)
            q_gen = self._parse_float(row.get("generation_mvar"), 0.0)
            p_load = self._parse_float(row.get("load_mw"), 0.0)
            q_load = self._parse_float(row.get("load_mvar"), 0.0)

            p_inj = p_gen - p_load if p_gen or p_load else None
            q_inj = q_gen - q_load if q_gen or q_load else None

            bus = Bus(
                bus_id=idx,  # Use index as ID if not provided
                name=row.get("name", f"Bus_{idx}"),
                base_kv=self._parse_float(row.get("voltage_kv"), 230.0),
                bus_type=bus_type,
                v_magnitude_pu=v_mag,
                v_angle_degree=v_ang,
                p_injected_mw=p_inj,
                q_injected_mvar=q_inj,
                vm_max_pu=1.1,  # Default limits
                vm_min_pu=0.9,
            )
            buses.append(bus)

        # Post-process: Identify slack bus by angle (smallest angle = reference)
        # CloudPSS uses the bus with minimum angle as slack bus reference
        if buses:
            # Find bus with minimum absolute angle
            slack_idx = min(range(len(buses)), key=lambda i: abs(buses[i].v_angle_degree or 999))
            # Mark as SLACK (CloudPSS reference bus)
            buses[slack_idx] = Bus(
                bus_id=buses[slack_idx].bus_id,
                name=buses[slack_idx].name,
                base_kv=buses[slack_idx].base_kv,
                bus_type="SLACK",  # Override to SLACK
                v_magnitude_pu=buses[slack_idx].v_magnitude_pu,
                v_angle_degree=buses[slack_idx].v_angle_degree,
                p_injected_mw=buses[slack_idx].p_injected_mw,
                q_injected_mvar=buses[slack_idx].q_injected_mvar,
                vm_max_pu=buses[slack_idx].vm_max_pu,
                vm_min_pu=buses[slack_idx].vm_min_pu,
            )

        return buses

    def _convert_branches_to_unified(
        self, branch_rows: list[dict[str, Any]], bus_name_to_idx: dict[str, int]
    ) -> list[Branch]:
        """Convert CloudPSS branch rows to unified Branch DataClass."""
        branches = []

        for idx, row in enumerate(branch_rows):
            # Determine branch type
            branch_type = self._infer_branch_type(row)

            # Get from/to buses using name mapping
            from_bus_name = row.get("from_bus", "")
            to_bus_name = row.get("to_bus", "")
            from_bus = self._find_bus_index(from_bus_name, bus_name_to_idx)
            to_bus = self._find_bus_index(to_bus_name, bus_name_to_idx)

            # Get power flows
            p_from = self._parse_float(row.get("p_from_mw"))
            q_from = self._parse_float(row.get("q_from_mvar"))
            p_to = self._parse_float(row.get("p_to_mw"))
            q_to = self._parse_float(row.get("q_to_mvar"))

            # Calculate loading
            s_from = (
                (p_from**2 + q_from**2) ** 0.5
                if p_from is not None and q_from is not None
                else None
            )
            rate_a = self._parse_float(row.get("rate_a_mva"), 100.0)
            loading = (s_from / rate_a * 100) if s_from and rate_a else None

            branch = Branch(
                from_bus=from_bus if from_bus is not None else idx,
                to_bus=to_bus if to_bus is not None else idx + 1,
                name=row.get("name", f"Branch_{idx}"),
                branch_type=branch_type,
                r_pu=self._parse_float(row.get("r_pu"), 0.0),
                x_pu=self._parse_float(row.get("x_pu"), 0.01),
                b_pu=self._parse_float(row.get("b_pu"), 0.0),
                rate_a_mva=rate_a,
                tap_ratio=self._parse_float(row.get("tap_ratio"), 1.0) or 1.0,
                p_from_mw=p_from,
                q_from_mvar=q_from,
                p_to_mw=p_to,
                q_to_mvar=q_to,
                loading_percent=loading,
            )
            branches.append(branch)

        return branches

    def _extract_generators_from_buses(
        self, bus_rows: list[dict[str, Any]]
    ) -> list[Generator]:
        """Extract generator information from bus rows."""
        generators = []

        for idx, row in enumerate(bus_rows):
            p_gen = self._parse_float(row.get("generation_mw"), 0.0)
            q_gen = self._parse_float(row.get("generation_mvar"), 0.0)

            # Only create generator if there's generation
            if p_gen > 0 or q_gen != 0:
                bus_type = self._infer_bus_type(row)
                v_set = (
                    self._parse_float(row.get("voltage_pu"), 1.0)
                    if bus_type in ("PV", "SLACK")
                    else None
                )

                gen = Generator(
                    bus_id=idx,
                    name=f"Gen_{row.get('name', f'Bus_{idx}' )}",
                    p_gen_mw=p_gen,
                    q_gen_mvar=q_gen if q_gen != 0 else None,
                    p_max_mw=max(p_gen * 2, 100.0),  # Estimate limits
                    p_min_mw=0.0,
                    v_set_pu=v_set,
                )
                generators.append(gen)

        return generators

    def _extract_loads_from_buses(
        self, bus_rows: list[dict[str, Any]]
    ) -> list[Load]:
        """Extract load information from bus rows."""
        loads = []

        for idx, row in enumerate(bus_rows):
            p_load = self._parse_float(row.get("load_mw"), 0.0)
            q_load = self._parse_float(row.get("load_mvar"), 0.0)

            # Only create load if there's demand
            if p_load > 0 or q_load != 0:
                load = Load(
                    bus_id=idx,
                    name=f"Load_{row.get('name', f'Bus_{idx}')}",
                    p_mw=p_load,
                    q_mvar=q_load,
                )
                loads.append(load)

        return loads

    def _infer_bus_type(self, row: dict[str, Any]) -> str:
        """Infer bus type from CloudPSS data."""
        # Check if explicitly specified
        if "bus_type" in row:
            bt = str(row["bus_type"]).upper()
            if bt in ("SLACK", "SWING", "REF"):
                return "SLACK"
            if bt in ("PV", "GEN"):
                return "PV"
            if bt in ("PQ", "LOAD"):
                return "PQ"

        # Infer from generation/load
        p_gen = self._parse_float(row.get("generation_mw"), 0.0)
        v_mag = self._parse_float(row.get("voltage_pu"))

        # If voltage is specified and generation exists -> PV or SLACK
        if v_mag is not None and p_gen > 0:
            # First generator is typically slack
            return "PV"  # Default to PV, caller can adjust

        return "PQ"

    def _infer_branch_type(self, row: dict[str, Any]) -> str:
        """Infer branch type from CloudPSS data."""
        explicit = str(row.get("branch_type", "")).upper()
        if explicit in ("LINE", "TRANSFORMER", "PHASE_SHIFTER"):
            return explicit

        name = str(row.get("name", "")).lower()

        if "transformer" in name or "trans" in name:
            return "TRANSFORMER"
        if "phase" in name or "ps" in name:
            return "PHASE_SHIFTER"

        return "LINE"

    def _find_bus_index(self, bus_name: str, bus_name_to_idx: dict[str, int]) -> int | None:
        """Find bus index from name using the provided mapping."""
        if not bus_name:
            return None
        # First try direct name lookup
        if bus_name in bus_name_to_idx:
            return bus_name_to_idx[bus_name]
        # Try converting to int (for numeric bus names)
        try:
            idx = int(bus_name)
            # Check if this numeric index exists in the mapping
            if idx in bus_name_to_idx.values():
                return idx
            # If buses are 1-indexed in source but 0-indexed in our model,
            # try adjusting (but only if the adjusted value exists)
            if idx - 1 in bus_name_to_idx.values():
                return idx - 1
        except (ValueError, TypeError):
            pass
        return None

    def _parse_float(
        self, value: Any, default: float | None = None
    ) -> float | None:
        """Safely parse float value."""
        if value is None:
            return default
        try:
            f = float(value)
            return f
        except (ValueError, TypeError):
            return default


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
        "bus_count": len(bus_rows),
        "branch_count": len(branch_rows),
        "total_generation": {"p_mw": round(total_p_gen, 2), "q_mvar": round(total_q_gen, 2)},
        "total_load": {"p_mw": round(total_p_load, 2), "q_mvar": round(total_q_load, 2)},
        "total_loss_mw": round(total_loss, 4),
        "voltage_range": {"min_pu": round(min_voltage, 4), "max_pu": round(max_voltage, 4)},
    }


def _as_float(value, default=0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


__all__ = ["CloudPSSPowerFlowAdapter"]
