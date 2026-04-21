"""ModelHandle - Engine-agnostic model manipulation interface.

This module provides the ModelHandle abstraction that allows skills to
manipulate power system model topology (query, remove, update components)
without depending on any specific simulation engine SDK.

Architecture:
    Skill -> ModelHandle (engine-agnostic) -> EngineAdapter._do_* (engine-specific) -> Engine SDK

This follows the AWT/Swing pattern where ModelHandle is the lightweight
"Swing" component that delegates to heavyweight "AWT" adapter methods.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from cloudpss_skills_v2.powerapi.base import EngineAdapter


@dataclass
class ComponentInfo:
    """Engine-agnostic component descriptor.

    Represents a single component in a power system model, providing
    a normalized view independent of the underlying simulation engine.

    Attributes:
        key: Component identifier in the model (engine-specific).
        name: Human-readable component name or label.
        definition: Component definition string (e.g., "model/CloudPSS/line").
        component_type: Normalized type classification (e.g., "branch",
            "load", "generator", "transformer", "shunt", "other").
        args: Component parameters as a dict. The structure is engine-specific,
            but follows consistent conventions per engine. Skills that need to
            modify args should use update_component_args() rather than editing
            this field directly.
    """

    key: str = ""
    name: str = ""
    definition: str = ""
    component_type: str = "other"
    args: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "key": self.key,
            "name": self.name,
            "definition": self.definition,
            "component_type": self.component_type,
            "args": self.args,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ComponentInfo:
        """Create from dictionary."""
        return cls(
            key=data.get("key", ""),
            name=data.get("name", ""),
            definition=data.get("definition", ""),
            component_type=data.get("component_type", "other"),
            args=data.get("args"),
        )


class ComponentType:
    """Standard component type classifications."""

    BRANCH = "branch"
    TRANSFORMER = "transformer"
    GENERATOR = "generator"
    LOAD = "load"
    SHUNT = "shunt"
    BUS = "bus"
    SOURCE = "source"
    OTHER = "other"


class ModelHandle:
    """Engine-agnostic model handle for topology manipulation.

    ModelHandle provides a lightweight, engine-agnostic interface for
    manipulating power system models. It wraps an EngineAdapter and
    delegates all operations through the adapter's _do_* methods.

    Skills use ModelHandle to:
    - Query model components (get_components, get_components_by_type)
    - Remove components (remove_component) — for N-1 / contingency analysis
    - Update component parameters (update_component_args) — for load scaling
    - Clone the model (clone) — for iterative what-if scenarios

    Usage:
        api = Engine.create_powerflow_api(engine="cloudpss")
        handle = api.get_model_handle(model_rid)

        # Query branches for N-1 analysis
        branches = handle.get_components_by_type("branch")

        # Run N-1: clone, remove, simulate
        for branch in branches:
            working = handle.clone()
            working.remove_component(branch.key)
            result = api.run_power_flow(model_handle=working)
    """

    def __init__(self, adapter: EngineAdapter, model_id: str):
        """Initialize ModelHandle with an adapter and model identifier.

        Args:
            adapter: The EngineAdapter that handles engine-specific operations.
            model_id: The model identifier. For CloudPSS, this is the RID.
                For pandapower, this could be a file path or cache key.

        Raises:
            TypeError: If adapter is not an EngineAdapter instance.
        """
        if not isinstance(adapter, EngineAdapter):
            raise TypeError(f"Expected EngineAdapter, got {type(adapter).__name__}")
        self._adapter = adapter
        self._model_id = model_id

    @property
    def model_id(self) -> str:
        """The model identifier used by the adapter."""
        return self._model_id

    @property
    def adapter(self) -> EngineAdapter:
        """The underlying EngineAdapter."""
        return self._adapter

    def get_components(self) -> list[ComponentInfo]:
        """Get all components in the model.

        Returns:
            List of ComponentInfo descriptors for all components.
            Returns empty list if the adapter does not support model manipulation.

        Raises:
            RuntimeError: If the adapter is not connected.
        """
        try:
            return self._adapter.get_components(self._model_id)
        except NotImplementedError:
            return []

    def get_components_by_type(self, comp_type: str) -> list[ComponentInfo]:
        """Get components of a specific type.

        Args:
            comp_type: Component type filter (e.g., "branch", "load",
                "generator", "transformer"). Use ComponentType constants.

        Returns:
            List of ComponentInfo descriptors matching the type.
        """
        try:
            return self._adapter.get_components_by_type(self._model_id, comp_type)
        except NotImplementedError:
            all_comps = self.get_components()
            return [c for c in all_comps if c.component_type == comp_type]

    def remove_component(self, component_key: str) -> bool:
        """Remove a component from the model.

        The removal is applied to the working copy held by this handle.
        The original model (on the server or in the adapter cache) is
        NOT modified unless this handle refers to the original.

        Args:
            component_key: The component identifier to remove.

        Returns:
            True if removal succeeded, False otherwise.
        """
        try:
            return self._adapter.remove_component(self._model_id, component_key)
        except NotImplementedError:
            return False

    def update_component_args(self, component_key: str, args: dict[str, Any]) -> bool:
        """Update a component's parameters.

        Args:
            component_key: The component identifier to update.
            args: New parameter dict to set on the component.
                The structure is engine-specific but follows consistent
                conventions per engine.

        Returns:
            True if update succeeded, False otherwise.
        """
        try:
            return self._adapter.update_component_args(
                self._model_id, component_key, args
            )
        except NotImplementedError:
            return False

    def clone(self) -> ModelHandle:
        """Create a fresh copy of the model for modification.

        Returns a new ModelHandle pointing to an independent copy of
        the model. Modifications to the clone do NOT affect this handle.

        For N-1 and contingency analysis, call clone() before each
        what-if scenario to start from a clean copy.

        Returns:
            A new ModelHandle for the cloned model.

        Raises:
            NotImplementedError: If the adapter does not support model cloning.
        """
        new_model_id = self._adapter.clone_model(self._model_id)
        return ModelHandle(self._adapter, new_model_id)

    def __repr__(self) -> str:
        return f"ModelHandle(model_id={self._model_id!r}, adapter={self._adapter.engine_name})"


__all__ = ["ModelHandle", "ComponentInfo", "ComponentType"]
