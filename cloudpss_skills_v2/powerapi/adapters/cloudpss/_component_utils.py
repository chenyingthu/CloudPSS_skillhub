"""Component utilities for CloudPSS model manipulation."""

from __future__ import annotations

from typing import Any, Optional


def get_components_by_definition(model, definition: str, sdk_kwargs: Optional[dict] = None) -> list[Any]:
    """Find all components matching a definition string."""
    kwargs = sdk_kwargs or {}
    components = model.getAllComponents(**kwargs)
    matches = []
    for comp_id, comp in components.items():
        comp_def = getattr(comp, "definition", "")
        if definition in comp_def:
            matches.append(comp)
    return matches


def update_component_args(model, comp_id: str, args: dict, sdk_kwargs: Optional[dict] = None) -> None:
    """Update a component's arguments on the model."""
    kwargs = sdk_kwargs or {}
    try:
        comp = model.getComponent(comp_id, **kwargs)
        if hasattr(comp, "update_args"):
            comp.update_args(args)
        elif hasattr(comp, "args"):
            comp.args = args
        else:
            model.update_component(comp_id, args, **kwargs)
    except (AttributeError, KeyError):
        try:
            model.update_component(comp_id, args, **kwargs)
        except Exception:
            pass


def remove_component_safe(model, comp_id: str, sdk_kwargs: Optional[dict] = None) -> bool:
    """Remove a component from the model, returning True on success."""
    kwargs = sdk_kwargs or {}
    try:
        if hasattr(model, "removeComponent"):
            model.removeComponent(comp_id, **kwargs)
            return True
        components = model.getAllComponents(**kwargs)
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
