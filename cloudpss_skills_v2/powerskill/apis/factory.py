"""API Factory - Creates engine-agnostic API instances with proper adapters.

Resolves the engine name to a concrete EngineAdapter, then wraps it
in the requested PowerSkill API type.
"""

from __future__ import annotations

from typing import Optional

from cloudpss_skills_v2.powerapi import EngineAdapter, EngineConfig
from cloudpss_skills_v2.powerskill.base import SimulationAPI
from cloudpss_skills_v2.powerskill.apis.powerflow import PowerFlowAPI
from cloudpss_skills_v2.powerskill.apis.short_circuit import ShortCircuitAPI
from cloudpss_skills_v2.powerskill.apis.emt import EMTAPI


def _create_adapter(
    engine: str, sim_type: str = "power_flow", config: EngineConfig | None = None
) -> EngineAdapter:
    """Instantiate the appropriate adapter for the given engine name and simulation type."""
    from cloudpss_skills_v2.powerapi.registry import registry

    if config is None:
        config = EngineConfig(engine_name=engine)
    else:
        config = EngineConfig(
            engine_name=engine, **{k: v for k, v in config.__dict__.items() if v}
        )

    adapter_cls = registry.get(engine, sim_type)
    if adapter_cls is not None:
        return adapter_cls(config=config)

    # Fallback: try power_flow adapter for any engine
    fallback = registry.get(engine, "power_flow")
    if fallback is not None:
        return fallback(config=config)

    # Last resort: CloudPSS power flow
    from cloudpss_skills_v2.powerapi.adapters.cloudpss.powerflow import (
        CloudPSSPowerFlowAdapter,
    )

    return CloudPSSPowerFlowAdapter(config=config)


_API_MAP = {
    "powerflow": PowerFlowAPI,
    "short_circuit": ShortCircuitAPI,
    "emt": EMTAPI,
}


class APIFactory:
    """Factory for creating engine-agnostic API instances backed by adapters."""

    @classmethod
    def create_powerflow_api(
        cls, engine: str = "cloudpss", config: EngineConfig | None = None
    ) -> PowerFlowAPI:
        adapter = _create_adapter(engine, "power_flow", config)
        return PowerFlowAPI(adapter=adapter)

    @classmethod
    def create_short_circuit_api(
        cls, engine: str = "cloudpss", config: EngineConfig | None = None
    ) -> ShortCircuitAPI:
        adapter = _create_adapter(engine, "short_circuit", config)
        return ShortCircuitAPI(adapter=adapter)

    @classmethod
    def create_emt_api(
        cls, engine: str = "cloudpss", config: EngineConfig | None = None
    ) -> EMTAPI:
        adapter = _create_adapter(engine, "emt", config)
        return EMTAPI(adapter=adapter)

    @classmethod
    def create_api(
        cls, api_type: str, engine: str = "cloudpss", config: EngineConfig | None = None
    ) -> SimulationAPI:
        api_cls = _API_MAP.get(api_type)
        if api_cls is None:
            raise ValueError(
                f"Unknown API type: {api_type}. Available: {list(_API_MAP.keys())}"
            )
        adapter = _create_adapter(engine, api_type, config)
        return api_cls(adapter=adapter)


__all__ = ["APIFactory"]
