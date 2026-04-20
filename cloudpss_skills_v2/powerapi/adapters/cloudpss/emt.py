"""CloudPSS EMT Adapter - Heavyweight adapter for CloudPSS EMT simulations.

Implements the EngineAdapter ABC for the CloudPSS platform, handling:
- Authentication via token
- Model loading via Model.fetch / Model.load
- EMT execution via model.runEMT
- Result extraction via result.getPlots / getPlotChannelNames / getPlotChannelData
"""

from __future__ import annotations

import csv
import json
import time
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


class CloudPSSEMTAdapter(EngineAdapter):
    """
    CloudPSS engine adapter for EMT simulations.

    Implements the EngineAdapter ABC by delegating to the CloudPSS SDK:
    - connect: authenticate via token
    - load_model: Model.fetch(rid) or Model.load(rid)
    - run_simulation: model.runEMT()
    - get_result: extract plots/channels from EMT result
    """

    _model_cache: dict[str, Any]
    _result_cache: dict[str, SimulationResult]

    def __init__(self, config: Optional[EngineConfig] = None):
        super().__init__(config)
        self._model_cache = {}
        self._result_cache = {}

    @property
    def engine_name(self) -> str:
        return "cloudpss_emt"

    def get_supported_simulations(self) -> list[SimulationType]:
        return [SimulationType.EMT]

    def _do_connect(self) -> None:
        auth_token = self._config.extra.get("auth", {}).get("token")
        if auth_token:
            try:
                from cloudpss import setToken

                setToken(auth_token)
            except ImportError:
                self._logger.warning("cloudpss SDK not installed; skipping token setup")

    def _do_disconnect(self) -> None:
        self._model_cache.clear()
        self._result_cache.clear()

    def _do_load_model(self, model_id: str) -> bool:
        from cloudpss import Model

        source = self._config.extra.get("model", {}).get("source", "cloud")
        kwargs = {}
        base_url = self._config.extra.get("auth", {}).get(
            "base_url"
        ) or self._config.extra.get("auth", {}).get("baseUrl")
        if base_url:
            kwargs["baseUrl"] = base_url

        if source == "local":
            model = Model.load(model_id)
        else:
            model = Model.fetch(model_id, **kwargs)

        self._model_cache[model_id] = model
        self._logger.info("Model loaded: %s (%s)", model.name, model.rid)
        return True

    def _do_run_simulation(self, config: dict[str, Any]) -> SimulationResult:
        model_id = config.get("model_id") or self._current_model_id
        if not model_id:
            return SimulationResult(
                status=SimulationStatus.FAILED,
                errors=["No model_id provided"],
            )

        self._setup_auth(config)

        model = self._model_cache.get(model_id)
        if model is None:
            source = config.get("source", "cloud")
            kwargs = {}
            base_url = config.get("auth", {}).get("base_url") or config.get(
                "auth", {}
            ).get("baseUrl")
            if base_url:
                kwargs["baseUrl"] = base_url
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

        # Optional: apply fault parameters before simulation
        fault_config = config.get("fault")
        if fault_config:
            model = self._apply_fault_parameters(model, fault_config)

        # Optional: set sampling frequency
        sampling_freq = config.get("sampling_freq")
        if sampling_freq:
            model = self._set_sampling_freq(model, sampling_freq)

        job_id = str(uuid.uuid4())[:8]
        started = datetime.now()
        timeout = config.get("timeout", 300)

        try:
            kwargs = {}
            base_url = config.get("auth", {}).get("base_url") or config.get(
                "auth", {}
            ).get("baseUrl")
            if base_url:
                kwargs["baseUrl"] = base_url

            # Check EMT topology first
            try:
                topology = model.fetchTopology(implementType="emtp")
                topology_data = topology.toJSON()
                component_count = len(topology_data.get("components", {}))
                self._logger.info(
                    "EMT topology check passed, component count: %d", component_count
                )
            except (KeyError, AttributeError) as e:
                return SimulationResult(
                    job_id=job_id,
                    status=SimulationStatus.FAILED,
                    errors=[f"EMT topology check failed: {e}"],
                    started_at=started,
                    completed_at=datetime.now(),
                )

            job = model.runEMT(**kwargs)

            max_wait = timeout
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
                        errors=["EMT simulation failed"],
                        started_at=started,
                        completed_at=datetime.now(),
                    )
                time.sleep(poll_interval)
                waited += poll_interval

            if sdk_status != 1:
                return SimulationResult(
                    job_id=job_id,
                    status=SimulationStatus.TIMEOUT,
                    errors=[f"EMT simulation timed out after {waited}s"],
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

            plots_data = self._extract_plot_data(emt_result)

            result_data = {
                "model_name": model.name if hasattr(model, "name") else model_id,
                "model_rid": model.rid if hasattr(model, "rid") else model_id,
                "job_id": getattr(job, "id", job_id),
                "plot_count": len(plots_data),
                "plots": plots_data,
                "metadata": {
                    "duration": config.get("duration"),
                    "step_size": config.get("step_size"),
                    "sampling_freq": config.get("sampling_freq", 2000),
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
        model_id = config.get("model_id")
        if not model_id:
            errors.append(
                ValidationError(field="model_id", message="model_id is required")
            )
        duration = config.get("duration")
        if duration is not None and duration < 0:
            errors.append(
                ValidationError(field="duration", message="duration must be >= 0")
            )
        return ValidationResult(valid=len(errors) == 0, errors=errors)

    def _setup_auth(self, config: dict) -> None:
        """Set up CloudPSS authentication from config dict."""
        import os
        from pathlib import Path

        auth = config.get("auth", {})
        token = auth.get("token")

        base_url = auth.get("base_url") or auth.get("baseUrl")
        if base_url:
            os.environ["CLOUDPSS_API_URL"] = base_url
        elif auth.get("server") == "internal":
            os.environ.setdefault("CLOUDPSS_API_URL", "https://internal.cloudpss.com")

        if not token:
            token_file = auth.get("token_file", ".cloudpss_token")
            token_path = Path(token_file)
            if token_path.exists():
                token = token_path.read_text().strip()
            else:
                for fallback in [".cloudpss_token", ".cloudpss_token_internal"]:
                    p = Path(fallback)
                    if p.exists():
                        token = p.read_text().strip()
                        break

        if token:
            try:
                from cloudpss import setToken

                setToken(token)
            except ImportError:
                pass

    def _apply_fault_parameters(self, model, fault_config: dict) -> Any:
        """Adjust fault component parameters (fs/fe) on the model."""
        FAULT_DEFINITION = "model/CloudPSS/_newFaultResistor_3p"
        try:
            components = model.getAllComponents()
            fault_comp = None
            for comp_id, comp in components.items():
                definition = getattr(comp, "definition", "")
                if FAULT_DEFINITION in definition:
                    fault_comp = comp
                    break

            if fault_comp is None:
                self._logger.warning(
                    "No fault component found, skipping fault parameter adjustment"
                )
                return model

            args = dict(fault_comp.args) if hasattr(fault_comp, "args") else {}
            new_start = fault_config.get("start_time")
            new_end = fault_config.get("end_time")

            if new_start is not None:
                args["fs"] = {"source": str(new_start), "ɵexp": ""}
            if new_end is not None:
                args["fe"] = {"source": str(new_end), "ɵexp": ""}

            from cloudpss_skills_v2.powerapi.adapters.cloudpss._component_utils import (
                update_component_args,
            )

            update_component_args(model, fault_comp.id, args)
        except Exception as e:
            self._logger.warning("Failed to apply fault parameters: %s", e)

        return model

    def _set_sampling_freq(self, model, sampling_freq: int) -> Any:
        """Adjust measurement channel sampling frequency on the model."""
        CHANNEL_DEFINITION = "model/CloudPSS/_newChannel"
        try:
            components = model.getAllComponents()
            channels = []
            for comp_id, comp in components.items():
                definition = getattr(comp, "definition", "")
                if CHANNEL_DEFINITION in definition:
                    channels.append(comp)

            if not channels:
                self._logger.warning(
                    "No measurement channels found, skipping sampling frequency adjustment"
                )
                return model

            for channel in channels:
                args = dict(channel.args) if hasattr(channel, "args") else {}
                args["Freq"] = {"source": str(sampling_freq), "ɵexp": ""}
                from cloudpss_skills_v2.powerapi.adapters.cloudpss._component_utils import (
                    update_component_args,
                )

                update_component_args(model, channel.id, args)

            self._logger.info(
                "Set sampling freq %dHz on %d channels", sampling_freq, len(channels)
            )
        except Exception as e:
            self._logger.warning("Failed to set sampling frequency: %s", e)

        return model

    def _extract_plot_data(self, emt_result) -> list[dict]:
        """Extract plot metadata and channel data from EMT result."""
        plots = []
        try:
            raw_plots = list(emt_result.getPlots())
            for i, plot in enumerate(raw_plots):
                plot_key = plot.get("key") or plot.get("name") or f"plot_{i}"
                channel_names = emt_result.getPlotChannelNames(i)

                channels_data = {}
                for ch_name in channel_names:
                    ch_data = emt_result.getPlotChannelData(i, ch_name)
                    if ch_data:
                        channels_data[ch_name] = {
                            "x": ch_data.get("x", []),
                            "y": ch_data.get("y", []),
                        }

                plots.append(
                    {
                        "index": i,
                        "key": plot_key,
                        "name": plot.get("name"),
                        "channel_count": len(channel_names),
                        "channels": channel_names[:20],
                        "channel_data": channels_data,
                    }
                )
        except (AttributeError, TypeError) as e:
            self._logger.warning("Failed to extract plot data: %s", e)

        return plots


__all__ = ["CloudPSSEMTAdapter"]
