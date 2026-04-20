"""API Factory - Creates engine-agnostic API instances."""
from __future__ import annotations
from typing import TYPE_CHECKING
from cloudpss_skills_v2.powerapi import EngineAdapter, EngineConfig
from cloudpss_skills_v2.powerskill import SimulationAPI
from cloudpss_skills_v2.powerskill.apis.powerflow import PowerFlowAPI

if TYPE_CHECKING:
    pass

_ADAPTER_MAP = {
    'powerflow': PowerFlowAPI,
}

class APIFactory:
    """Factory for creating engine-agnostic API instances."""

    _initialized = False
    _registry: dict[str, type] = {}

    @classmethod
    def _ensure_initialized(cls):
        if not cls._initialized:
            cls._registry.update(_ADAPTER_MAP)
            cls._initialized = True

    @classmethod
    def create_powerflow_api(cls, engine: str = 'cloudpss', config: EngineConfig | None = None) -> PowerFlowAPI:
        cls._ensure_initialized()
        if config is None:
            config = EngineConfig(engine_name=engine)
        return PowerFlowAPI(engine=engine, config=config)

    @classmethod
    def create_api(cls, api_type: str, engine: str = 'cloudpss', config: EngineConfig | None = None) -> SimulationAPI:
        cls._ensure_initialized()
        api_cls = cls._registry.get(api_type)
        if api_cls is None:
            raise ValueError(f"Unknown API type: {api_type}")
        if config is None:
            config = EngineConfig(engine_name=engine)
        return api_cls(engine=engine, config=config)

__all__ = ['APIFactory']
