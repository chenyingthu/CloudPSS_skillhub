"""
PowerSkill Layer - Engine-agnostic PowerSkill API Framework

This module provides the PowerSkill layer for cloudpss_skills_v2,
following the Java Swing pattern where APIs are lightweight components
that provide engine-agnostic interfaces on top of PowerAPI adapters.

Architecture:
    Skills -> PowerSkill APIs (Lightweight, engine-agnostic) -> PowerAPI Adapters (Heavyweight) -> Engines
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional
import logging

from cloudpss_skills_v2.powerapi import EngineAdapter, EngineConfig, SimulationResult
from cloudpss_skills_v2.powerskill.model_handle import ModelHandle


class SimulationAPI(ABC):
    """
    Abstract base class for simulation APIs.

    PowerSkill APIs are lightweight, engine-agnostic interfaces that delegate
    to PowerAPI adapters. This follows the Java Swing pattern where the API
    facade hides engine-specific implementation details.

    Each API wraps an EngineAdapter and provides domain-specific convenience
    methods on top of the generic adapter interface.
    """

    def __init__(self, adapter: EngineAdapter):
        """
        Initialize the API with a PowerAPI adapter.

        Args:
            adapter: An EngineAdapter instance that handles engine-specific logic.
        """
        if not isinstance(adapter, EngineAdapter):
            raise TypeError(f"Expected EngineAdapter, got {type(adapter).__name__}")
        self._adapter = adapter
        self._logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    @property
    def adapter(self) -> EngineAdapter:
        return self._adapter

    def connect(self) -> None:
        self._adapter.connect()

    def disconnect(self) -> None:
        self._adapter.disconnect()

    def load_model(self, model_id: str | None = None) -> bool:
        return self._adapter.load_model(model_id)

    def validate_config(self, config: dict[str, Any] | None = None):
        return self._adapter.validate_config(config)

    def run(self, config: dict[str, Any] | None = None) -> SimulationResult:
        return self._adapter.run_simulation(config)

    def get_result(self, job_id: str | None = None) -> SimulationResult:
        return self._adapter.get_result(job_id)

    def get_model_handle(self, model_id: str) -> ModelHandle:
        """Get an engine-agnostic model handle for topology manipulation.

        Skills use ModelHandle to query, remove, update, and clone model
        components without depending on any specific engine SDK.

        Args:
            model_id: The model identifier (e.g., CloudPSS RID).

        Returns:
            A ModelHandle instance for this model.
        """
        return ModelHandle(self._adapter, model_id)

    def __enter__(self) -> SimulationAPI:
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.disconnect()


__all__ = ["SimulationAPI"]
