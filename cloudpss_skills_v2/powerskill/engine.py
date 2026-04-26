"""API Factory - Creates engine-agnostic API instances with proper adapters.

Resolves the engine name to a concrete EngineAdapter, then wraps it
in the requested PowerSkill API type.
"""

from __future__ import annotations

from typing import Any, Optional

from cloudpss_skills_v2.powerapi import EngineAdapter, EngineConfig
from cloudpss_skills_v2.powerskill.base import SimulationAPI
from cloudpss_skills_v2.powerskill.powerflow import PowerFlow
from cloudpss_skills_v2.powerskill.short_circuit import ShortCircuit
from cloudpss_skills_v2.powerskill.emt import EMT
from cloudpss_skills_v2.powerskill.transient import TransientStability
from cloudpss_skills_v2.powerskill.harmonic import HarmonicAnalysis
from cloudpss_skills_v2.powerskill.small_signal import SmallSignalStability

_API_MAP = {
    "powerflow": PowerFlow,
    "power_flow": PowerFlow,
    "emt": EMT,
    "emt_simulation": EMT,
    "short_circuit": ShortCircuit,
    "shortcircuit": ShortCircuit,
    "transient": TransientStability,
    "transient_stability": TransientStability,
    "harmonic": HarmonicAnalysis,
    "harmonic_analysis": HarmonicAnalysis,
    "small_signal": SmallSignalStability,
    "small_signal_stability": SmallSignalStability,
}

_SIM_TYPE_ALIASES = {
    "powerflow": "power_flow",
    "power_flow": "power_flow",
    "emt": "emt",
    "emt_simulation": "emt",
    "short_circuit": "short_circuit",
    "shortcircuit": "short_circuit",
    "transient": "transient",
    "transient_stability": "transient",
    "harmonic": "harmonic",
    "harmonic_analysis": "harmonic",
    "small_signal": "small_signal",
    "small_signal_stability": "small_signal",
}


def _create_adapter(
    engine: str, sim_type: str = "power_flow", config: EngineConfig | None = None
) -> EngineAdapter:
    """Instantiate the appropriate adapter for the given engine name and simulation type."""
    from cloudpss_skills_v2.powerapi.registry import registry

    if config is None:
        config = EngineConfig(engine_name=engine)
    else:
        config_dict = {'engine_name': engine}
        if config.base_url:
            config_dict['base_url'] = config.base_url
        if config.extra:
            config_dict['extra'] = config.extra
        config = EngineConfig(**config_dict)

    canonical_sim_type = _SIM_TYPE_ALIASES.get(sim_type, sim_type)
    adapter_cls = registry.get(engine, canonical_sim_type)
    if adapter_cls is not None:
        return adapter_cls(config=config)

    available = registry.list_sim_types(engine)
    if not available:
        raise ValueError(f"Unknown engine: {engine}")
    raise ValueError(
        f"Engine '{engine}' does not support simulation type '{canonical_sim_type}'. "
        f"Available: {available}"
    )


def _build_engine_config(
    engine: str,
    base_url: str | None = None,
    auth: dict[str, Any] | None = None,
) -> EngineConfig:
    """Build EngineConfig from skill-level parameters."""
    extra = dict(auth) if auth else {}
    if auth:
        extra["auth"] = dict(auth)
    if base_url:
        extra["base_url"] = base_url
        if "auth" in extra:
            extra["auth"]["base_url"] = base_url
    return EngineConfig(engine_name=engine, base_url=base_url or "", extra=extra)


class Engine:
    """Factory for creating engine-agnostic API instances backed by adapters."""

    @classmethod
    def create_powerflow(
        cls, engine: str = "cloudpss", config: EngineConfig | None = None
    ) -> PowerFlow:
        adapter = _create_adapter(engine, "power_flow", config)
        adapter.connect()
        return PowerFlow(adapter=adapter)

    @classmethod
    def create_powerflow_for_skill(
        cls,
        engine: str = "cloudpss",
        base_url: str | None = None,
        auth: dict[str, Any] | None = None,
    ) -> PowerFlow:
        cfg = _build_engine_config(engine, base_url, auth)
        adapter = _create_adapter(engine, "power_flow", cfg)
        adapter.connect()
        return PowerFlow(adapter=adapter)

    @classmethod
    def create_short_circuit(
        cls, engine: str = "cloudpss", config: EngineConfig | None = None
    ) -> ShortCircuit:
        adapter = _create_adapter(engine, "short_circuit", config)
        adapter.connect()
        return ShortCircuit(adapter=adapter)

    @classmethod
    def create_short_circuit_for_skill(
        cls,
        engine: str = "cloudpss",
        base_url: str | None = None,
        auth: dict[str, Any] | None = None,
    ) -> ShortCircuit:
        cfg = _build_engine_config(engine, base_url, auth)
        adapter = _create_adapter(engine, "short_circuit", cfg)
        adapter.connect()
        return ShortCircuit(adapter=adapter)

    @classmethod
    def create_emt(
        cls, engine: str = "cloudpss", config: EngineConfig | None = None
    ) -> EMT:
        adapter = _create_adapter(engine, "emt", config)
        adapter.connect()
        return EMT(adapter=adapter)

    @classmethod
    def create_emt_for_skill(
        cls,
        engine: str = "cloudpss",
        base_url: str | None = None,
        auth: dict[str, Any] | None = None,
    ) -> EMT:
        cfg = _build_engine_config(engine, base_url, auth)
        adapter = _create_adapter(engine, "emt", cfg)
        adapter.connect()
        return EMT(adapter=adapter)

    @classmethod
    def create_transient(
        cls, engine: str = "cloudpss", config: EngineConfig | None = None
    ) -> TransientStability:
        adapter = _create_adapter(engine, "transient", config)
        adapter.connect()
        return TransientStability(adapter=adapter)

    @classmethod
    def create_transient_for_skill(
        cls,
        engine: str = "cloudpss",
        base_url: str | None = None,
        auth: dict[str, Any] | None = None,
    ) -> TransientStability:
        cfg = _build_engine_config(engine, base_url, auth)
        adapter = _create_adapter(engine, "transient", cfg)
        adapter.connect()
        return TransientStability(adapter=adapter)

    @classmethod
    def create_harmonic(
        cls, engine: str = "cloudpss", config: EngineConfig | None = None
    ) -> HarmonicAnalysis:
        adapter = _create_adapter(engine, "harmonic", config)
        adapter.connect()
        return HarmonicAnalysis(adapter=adapter)

    @classmethod
    def create_harmonic_for_skill(
        cls,
        engine: str = "cloudpss",
        base_url: str | None = None,
        auth: dict[str, Any] | None = None,
    ) -> HarmonicAnalysis:
        cfg = _build_engine_config(engine, base_url, auth)
        adapter = _create_adapter(engine, "harmonic", cfg)
        adapter.connect()
        return HarmonicAnalysis(adapter=adapter)

    @classmethod
    def create_small_signal(
        cls, engine: str = "cloudpss", config: EngineConfig | None = None
    ) -> SmallSignalStability:
        adapter = _create_adapter(engine, "small_signal", config)
        adapter.connect()
        return SmallSignalStability(adapter=adapter)

    @classmethod
    def create_small_signal_for_skill(
        cls,
        engine: str = "cloudpss",
        base_url: str | None = None,
        auth: dict[str, Any] | None = None,
    ) -> SmallSignalStability:
        cfg = _build_engine_config(engine, base_url, auth)
        adapter = _create_adapter(engine, "small_signal", cfg)
        adapter.connect()
        return SmallSignalStability(adapter=adapter)

    @classmethod
    def create(
        cls, api_type: str, engine: str = "cloudpss", config: EngineConfig | None = None
    ) -> SimulationAPI:
        api_cls = _API_MAP.get(api_type)
        if api_cls is None:
            raise ValueError(
                f"Unknown API type: {api_type}. Available: {list(_API_MAP.keys())}"
            )
        adapter = _create_adapter(engine, api_type, config)
        adapter.connect()
        return api_cls(adapter=adapter)


__all__ = ["Engine"]
