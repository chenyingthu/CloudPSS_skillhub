"""Adapter Registry

Central registry for engine adapters, following the Java AWT ComponentRegistry pattern.
"""

from typing import Type

from cloudpss_skills_v2.awt import EngineAdapter, SimulationType


class AdapterRegistry:
    """Registry for engine adapters.

    Allows registration and retrieval of adapters by engine name and simulation type.
    """

    engine_name: str
    supported_simulations: dict

    def register_adapter(engine_name, supported_simulations):
        """Decorator to register an adapter class."""
        pass  # TODO: restore from disassembly


registry = AdapterRegistry()
