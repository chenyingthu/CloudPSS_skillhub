"""Adapter Registry - Central registry for engine adapters."""

from __future__ import annotations

from typing import Type

from cloudpss_skills_v2.powerapi.base import EngineAdapter, SimulationType


class AdapterRegistry:
    """Registry for engine adapters keyed by engine name and simulation type."""

    _adapters: dict[str, dict[str, Type[EngineAdapter]]]

    def __init__(self):
        self._adapters = {}

    def register(
        self, engine_name: str, sim_type: str, adapter_cls: Type[EngineAdapter]
    ) -> None:
        if engine_name not in self._adapters:
            self._adapters[engine_name] = {}
        self._adapters[engine_name][sim_type] = adapter_cls

    def get(self, engine_name: str, sim_type: str) -> Type[EngineAdapter] | None:
        engine_map = self._adapters.get(engine_name, {})
        return engine_map.get(sim_type)

    def list_engines(self) -> list[str]:
        return list(self._adapters.keys())

    def list_sim_types(self, engine_name: str) -> list[str]:
        return list(self._adapters.get(engine_name, {}).keys())


def _register_defaults(registry: AdapterRegistry) -> None:
    from cloudpss_skills_v2.powerapi.adapters.cloudpss.powerflow import (
        CloudPSSPowerFlowAdapter,
    )
    from cloudpss_skills_v2.powerapi.adapters.cloudpss.emt import CloudPSSEMTAdapter
    from cloudpss_skills_v2.powerapi.adapters.cloudpss.short_circuit import (
        CloudPSSShortCircuitAdapter,
    )

    registry.register("cloudpss", "power_flow", CloudPSSPowerFlowAdapter)
    registry.register("cloudpss", "emt", CloudPSSEMTAdapter)
    registry.register("cloudpss", "short_circuit", CloudPSSShortCircuitAdapter)

    try:
        from cloudpss_skills_v2.powerapi.adapters.pandapower.powerflow import (
            PandapowerPowerFlowAdapter,
        )
        from cloudpss_skills_v2.powerapi.adapters.pandapower.short_circuit import (
            PandapowerShortCircuitAdapter,
        )

        registry.register("pandapower", "power_flow", PandapowerPowerFlowAdapter)
        registry.register("pandapower", "short_circuit", PandapowerShortCircuitAdapter)
    except ImportError:
        pass

    try:
        from cloudpss_skills_v2.powerapi.adapters.algolib.powerflow import (
            AlgoLibPowerFlowAdapter,
        )
        from cloudpss_skills_v2.powerapi.adapters.algolib.short_circuit import (
            AlgoLibShortCircuitAdapter,
        )

        registry.register("algolib", "power_flow", AlgoLibPowerFlowAdapter)
        registry.register("algolib", "short_circuit", AlgoLibShortCircuitAdapter)
    except ImportError:
        pass


registry = AdapterRegistry()
_register_defaults(registry)


__all__ = ["AdapterRegistry", "registry"]
