"""CloudPSS Short Circuit Adapter - Uses EMT with fault component for SC analysis.

CloudPSS has no dedicated short-circuit API. Short circuit analysis is performed
by running an EMT simulation with a fault component, then extracting current
and voltage waveforms from the EMT result.
"""

from __future__ import annotations

import time
import uuid
from datetime import datetime
from typing import Any, Optional

from cloudpss_skills_v2.core.token_manager import (
    CloudPSSAdapter,
    TokenManager,
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
from cloudpss_skills_v2.powerapi.adapters.cloudpss._component_utils import (
    get_components_by_definition,
    update_component_args,
)

_FAULT_TYPE_MAP = {
    "3phase": "3ph",
    "3ph": "3ph",
    "three_phase": "3ph",
    "1phase": "slg",
    "slg": "slg",
    "single_line_ground": "slg",
    "phase-ground": "slg",
    "2phase": "ll",
    "ll": "ll",
    "line_line": "ll",
    "2phase-ground": "dlg",
    "dlg": "dlg",
    "double_line_ground": "dlg",
}


class CloudPSSShortCircuitAdapter(EngineAdapter):
    """
    CloudPSS engine adapter for short circuit analysis via EMT.

    Since CloudPSS has no dedicated SC solver, this adapter:
    1. Configures a fault component on the model
    2. Runs an EMT simulation
    3. Extracts fault currents and bus voltages from the EMT result
    """

    _model_cache: dict[str, Any]
    _result_cache: dict[str, SimulationResult]
    _cloud_pss_adapter: CloudPSSAdapter

    def __init__(self, config: Optional[EngineConfig] = None):
        super().__init__(config)
        self._model_cache = {}
        self._result_cache = {}
        
        # Build SDK with proper base_url
        auth = self._config.extra or {}
        base_url = self._config.base_url
        token = TokenManager.get_token(auth)
        
        self._cloud_pss_adapter = CloudPSSAdapter(token=token, api_url=base_url)

    @property
    def engine_name(self) -> str:
        return "cloudpss_sc"

    def get_supported_simulations(self) -> list[SimulationType]:
        return [SimulationType.SHORT_CIRCUIT]

    def _do_connect(self) -> None:
        auth = self._config.extra or {}
        base_url = self._config.base_url
        token = TokenManager.get_token(auth)
        
        self._cloud_pss_adapter = CloudPSSAdapter(token=token, api_url=base_url)

        if not self._cloud_pss_adapter.connect():
            pass

    def _do_disconnect(self) -> None:
        self._model_cache.clear()
        self._result_cache.clear()

    def _do_load_model(self, model_id: str) -> bool:
        from cloudpss import Model

        source = self._config.extra.get("model", {}).get("source", "cloud")
        kwargs = self._cloud_pss_adapter.sdk_kwargs()
        if source == "local":
            model = Model.load(model_id)
        else:
            model = Model.fetch(model_id, **kwargs)
        self._model_cache[model_id] = model
        return True

    def _do_run_simulation(self, config: dict[str, Any]) -> SimulationResult:
        model_id = config.get("model_id") or self._current_model_id
        if not model_id:
            return SimulationResult(
                status=SimulationStatus.FAILED, errors=["No model_id provided"]
            )

        cloudpss = self._cloud_pss_adapter

        model = self._model_cache.get(model_id)
        if model is None:
            try:
                from cloudpss import Model

                kwargs = cloudpss.sdk_kwargs()
                source = config.get("source", "cloud")
                if source == "local":
                    model = Model.load(model_id)
                else:
                    model = Model.fetch(model_id, **kwargs)
                self._model_cache[model_id] = model
            except Exception as e:
                return SimulationResult(
                    status=SimulationStatus.FAILED,
                    errors=[f"Failed to load model: {e}"],
                )

        # Configure fault component
        fault_type = config.get("fault_type", "three_phase")
        fault_impedance = config.get("fault_impedance", {})
        bus_id = config.get("bus_id")

        FAULT_DEFINITION = "model/CloudPSS/_newFaultResistor_3p"
        fault_comps = get_components_by_definition(model, FAULT_DEFINITION)
        if fault_comps:
            fault_comp = fault_comps[0]
            args = dict(fault_comp.args) if hasattr(fault_comp, "args") else {}
            # Set fault type and impedance
            ft_mapped = _FAULT_TYPE_MAP.get(fault_type, "3ph")
            args["faultType"] = {"source": ft_mapped, "ɵexp": ""}
            if fault_impedance:
                r = fault_impedance.get("r", 0)
                args["R"] = {"source": str(r), "ɵexp": ""}
            if bus_id:
                args["bus"] = {"source": bus_id, "ɵexp": ""}
            update_component_args(model, fault_comp.id, args)

        # Run EMT simulation
        job_id = str(uuid.uuid4())[:8]
        started = datetime.now()
        timeout = config.get("timeout", 300)

        try:
            kwargs = cloudpss.sdk_kwargs()

            job = model.runEMT(**kwargs)

            max_wait = timeout
            poll_interval = 2
            waited = 0
            sdk_status = 0

            while waited < max_wait:
                sdk_status = job.status()
                if sdk_status == 1:
                    break
                if sdk_status == 2:
                    return SimulationResult(
                        job_id=job_id,
                        status=SimulationStatus.FAILED,
                        errors=["Short circuit EMT simulation failed"],
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

            emt_result = job.result
            if emt_result is None:
                return SimulationResult(
                    job_id=job_id,
                    status=SimulationStatus.FAILED,
                    errors=["EMT result is empty"],
                    started_at=started,
                    completed_at=datetime.now(),
                )

            # Extract fault currents and bus voltages from EMT result
            fault_currents = self._extract_fault_currents(emt_result)
            bus_voltages = self._extract_bus_voltages(emt_result)

            result_data = {
                "model_name": getattr(model, "name", model_id),
                "model_rid": model.rid if hasattr(model, "rid") else model_id,
                "job_id": getattr(job, "id", job_id),
                "fault_type": fault_type,
                "fault_currents": fault_currents,
                "bus_voltages": bus_voltages,
                "summary": {
                    "fault_type": fault_type,
                    "max_fault_current_ka": max(
                        (fc.get("current_ka", 0) for fc in fault_currents), default=0
                    ),
                    "min_voltage_pu": min(
                        (bv.get("voltage_pu", 1.0) for bv in bus_voltages), default=1.0
                    ),
                },
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

    def _do_validate_config(self, config: dict[str, Any]) -> ValidationResult:
        errors = []
        if not config.get("model_id"):
            errors.append(
                ValidationError(field="model_id", message="model_id is required")
            )
        return ValidationResult(valid=len(errors) == 0, errors=errors)

    def _setup_auth(self, config: dict[str, Any]) -> CloudPSSAdapter:
        return build_cloudpss_adapter(config)

    def _extract_fault_currents(self, emt_result: Any) -> list[dict[str, Any]]:
        """Extract fault current magnitudes from EMT waveform data."""
        currents: list[dict[str, Any]] = []
        try:
            plots = list(emt_result.getPlots())
            for i, plot in enumerate(plots):
                channel_names = emt_result.getPlotChannelNames(i)
                for ch_name in channel_names:
                    if any(kw in ch_name.lower() for kw in ["fault", "current", "i_"]):
                        ch_data = emt_result.getPlotChannelData(i, ch_name)
                        if ch_data and ch_data.get("y"):
                            max_current = max(abs(v) for v in ch_data["y"])
                            currents.append(
                                {
                                    "channel": ch_name,
                                    "current_ka": round(max_current, 4),
                                    "peak_value": max(ch_data["y"]),
                                }
                            )
        except (AttributeError, TypeError):
            pass
        return currents

    def _extract_bus_voltages(self, emt_result: Any) -> list[dict[str, Any]]:
        """Extract bus voltage magnitudes from EMT waveform data."""
        voltages: list[dict[str, Any]] = []
        try:
            plots = list(emt_result.getPlots())
            for i, plot in enumerate(plots):
                channel_names = emt_result.getPlotChannelNames(i)
                for ch_name in channel_names:
                    if any(kw in ch_name.lower() for kw in ["voltage", "v_", "bus"]):
                        ch_data = emt_result.getPlotChannelData(i, ch_name)
                        if ch_data and ch_data.get("y"):
                            min_voltage = min(abs(v) for v in ch_data["y"])
                            voltages.append(
                                {
                                    "channel": ch_name,
                                    "voltage_pu": round(min_voltage, 4),
                                }
                            )
        except (AttributeError, TypeError):
            pass
        return voltages


__all__ = ["CloudPSSShortCircuitAdapter"]
