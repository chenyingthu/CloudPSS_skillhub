"""Component utilities for CloudPSS model manipulation."""

from __future__ import annotations

from typing import Any


def get_components_by_definition(model, definition: str) -> list[Any]:
    """Find all components matching a definition string."""
    components = model.getAllComponents()
    matches = []
    for comp_id, comp in components.items():
        comp_def = getattr(comp, "definition", "")
        if definition in comp_def:
            matches.append(comp)
    return matches


def update_component_args(model, comp_id: str, args: dict) -> None:
    """Update a component's arguments on the model."""
    try:
        comp = model.getComponent(comp_id)
        if hasattr(comp, "update_args"):
            comp.update_args(args)
        elif hasattr(comp, "args"):
            comp.args = args
        else:
            model.update_component(comp_id, args)
    except (AttributeError, KeyError):
        try:
            model.update_component(comp_id, args)
        except Exception:
            pass


def remove_component_safe(model, comp_id: str) -> bool:
    """Remove a component from the model, returning True on success."""
    try:
        if hasattr(model, "removeComponent"):
            model.removeComponent(comp_id)
            return True
        components = model.getAllComponents()
        if comp_id in components:
            del components[comp_id]
            return True
    except Exception:
        pass
    return False


__all__ = [
    "get_components_by_definition",
    "update_component_args",
    "remove_component_safe",
]
