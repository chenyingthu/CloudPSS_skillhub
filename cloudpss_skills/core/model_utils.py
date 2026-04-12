"""
Model Utilities Module - Unified model manipulation utilities.

Provides standardized interfaces for:
- Model cloning (deep copy)
- Model reloading from source
- Component manipulation helpers
- Component discovery
"""

from __future__ import annotations

import logging
from copy import deepcopy
from typing import Any, Callable, Dict, List, Optional, Tuple

from cloudpss import Model

from cloudpss_skills.core.auth_utils import get_cloudpss_kwargs

logger = logging.getLogger(__name__)


def clone_model(model: Model) -> Model:
    """
    Create a deep copy of a model for modification.

    This is the standard way to create a working copy for simulations
    that modify the model topology.

    Args:
        model: Source model to clone

    Returns:
        New Model instance with identical topology
    """
    return Model(deepcopy(model.toJSON()))


def reload_model(
    model_rid: str,
    source: str = "cloud",
    config: Optional[Dict] = None,
) -> Model:
    """
    Reload a model from its source.

    Use this when you need a fresh copy of the original model,
    rather than modifying an existing clone.

    Args:
        model_rid: Model RID (cloud path or local file path)
        source: 'cloud' or 'local'
        config: Optional auth configuration

    Returns:
        Fresh Model instance
    """
    kwargs = get_cloudpss_kwargs(config) if config else {}

    if source == "local":
        return Model.load(model_rid)
    else:
        return Model.fetch(model_rid, **kwargs)


def get_or_clone_model(
    base_model: Optional[Model],
    model_config: Dict[str, Any],
    config: Optional[Dict] = None,
) -> Model:
    """
    Get a model for simulation: clone existing or load from source.

    If base_model is provided, clones it. Otherwise loads from model_config.

    Args:
        base_model: Existing model to clone (optional)
        model_config: Model configuration dict with 'rid' and 'source'
        config: Optional auth configuration

    Returns:
        Model instance ready for simulation
    """
    if base_model is not None:
        return clone_model(base_model)

    model_rid = model_config.get("rid")
    source = model_config.get("source", "cloud")

    if not model_rid:
        raise ValueError("model.rid is required when no base_model provided")

    return reload_model(model_rid, source, config)


def get_all_components(model: Model) -> Dict[str, Any]:
    """
    Get all components from a model.

    Args:
        model: CloudPSS Model object

    Returns:
        Dict mapping component keys to component objects
    """
    try:
        return model.getAllComponents()
    except Exception as e:
        logger.error(f"Failed to get components: {e}")
        return {}


def get_components_by_definition(
    model: Model,
    definition: str,
) -> Dict[str, Dict]:
    """
    Get components by definition type.

    Args:
        model: CloudPSS Model object
        definition: Component definition (e.g., 'model/CloudPSS/_newBus_3p')

    Returns:
        Dict of matching components
    """
    components = get_all_components(model)
    result = {}

    for key, comp in components.items():
        if getattr(comp, "definition", None) == definition:
            result[key] = {
                "key": key,
                "id": key,
                "label": getattr(comp, "label", ""),
                "name": getattr(comp, "name", ""),
                "args": getattr(comp, "args", {}) or {},
                "pins": getattr(comp, "pins", {}) or {},
                "definition": getattr(comp, "definition", ""),
            }

    return result


def get_components_by_type(
    model: Model,
    comp_type: str,
) -> Dict[str, Dict]:
    """
    Get components by type (alternative name for get_components_by_definition).

    Args:
        model: CloudPSS Model object
        comp_type: Component type/definition

    Returns:
        Dict of matching components
    """
    return get_components_by_definition(model, comp_type)


def get_buses(model: Model) -> Dict[str, Dict]:
    """Get all bus components."""
    return get_components_by_definition(model, "model/CloudPSS/_newBus_3p")


def get_lines(model: Model) -> Dict[str, Dict]:
    """Get all transmission line components."""
    return get_components_by_definition(model, "model/CloudPSS/TransmissionLine")


def get_generators(model: Model) -> Dict[str, Dict]:
    """Get all generator components."""
    return get_components_by_definition(model, "model/CloudPSS/_newGenerator")


def find_component_by_label(
    model: Model,
    label: str,
) -> Optional[Dict]:
    """
    Find a component by its label.

    Args:
        model: CloudPSS Model object
        label: Component label to search for

    Returns:
        Component dict if found, None otherwise
    """
    components = get_all_components(model)
    label_lower = label.lower()

    for key, comp in components.items():
        comp_label = getattr(comp, "label", "") or ""
        if comp_label.lower() == label_lower:
            return {
                "key": key,
                "id": key,
                "label": comp_label,
                "name": getattr(comp, "name", ""),
                "args": getattr(comp, "args", {}) or {},
                "pins": getattr(comp, "pins", {}) or {},
                "definition": getattr(comp, "definition", ""),
            }

    return None


def matches_label(candidate: str, target: str) -> bool:
    """
    Check if a label matches a target (case-insensitive, flexible matching).

    Args:
        candidate: Label to check
        target: Target label

    Returns:
        True if labels match
    """
    if not candidate or not target:
        return False

    cand_lower = candidate.lower().strip()
    targ_lower = target.lower().strip()

    if cand_lower == targ_lower:
        return True

    cand_alnum = "".join(c for c in cand_lower if c.isalnum())
    targ_alnum = "".join(c for c in targ_lower if c.isalnum())

    if cand_alnum and cand_alnum == targ_alnum:
        return True

    cand_digits = "".join(c for c in cand_lower if c.isdigit())
    targ_digits = "".join(c for c in targ_lower if c.isdigit())

    if cand_digits and targ_digits and cand_digits == targ_digits:
        return True

    return False


def remove_component_safe(model: Model, component_id: str) -> bool:
    """
    Safely remove a component from model.

    Args:
        model: CloudPSS Model object
        component_id: ID of component to remove

    Returns:
        True if removed successfully, False otherwise
    """
    try:
        model.removeComponent(component_id)
        return True
    except (KeyError, AttributeError, ValueError) as e:
        logger.warning(f"Failed to remove component {component_id}: {e}")
        return False


def update_component_args(
    model: Model,
    component_id: str,
    args: Dict[str, Any],
) -> bool:
    """
    Update component arguments safely.

    Args:
        model: CloudPSS Model object
        component_id: ID of component to update
        args: New arguments dict

    Returns:
        True if updated successfully, False otherwise
    """
    try:
        model.updateComponent(component_id, args=args)
        return True
    except (KeyError, AttributeError, ValueError, TypeError) as e:
        logger.warning(f"Failed to update component {component_id}: {e}")
        return False


def get_component_args(model: Model, component_id: str) -> Dict[str, Any]:
    """
    Get component arguments.

    Args:
        model: CloudPSS Model object
        component_id: ID of component

    Returns:
        Component args dict, empty dict if not found
    """
    components = get_all_components(model)
    comp = components.get(component_id)
    if comp:
        return getattr(comp, "args", {}) or {}
    return {}


def get_revision_components(
    model: Model,
    implement_type: str = "powerflow",
) -> Dict[str, Any]:
    """
    Get components from model revision (alternative to getAllComponents).

    Args:
        model: CloudPSS Model object
        implement_type: 'powerflow' or 'emtp'

    Returns:
        Dict of components from revision
    """
    try:
        revision = model.getRevision()
        implements = revision.get("implements", {})
        diagram = implements.get("diagram", {})
        cells = diagram.get("cells", [])

        components = {}
        for cell in cells:
            if cell.get("type") == "standard.Image":
                key = cell.get("key")
                data = cell.get("data", {})
                components[key] = data

        return components

    except Exception as e:
        logger.error(f"Failed to get revision components: {e}")
        return {}


def iterate_components(
    model: Model,
    filter_func: Optional[Callable[[Any], bool]] = None,
) -> List[Tuple[str, Any]]:
    """
    Iterate over components with optional filtering.

    Args:
        model: CloudPSS Model object
        filter_func: Optional function(component) -> bool

    Returns:
        List of (component_id, component) tuples
    """
    components = get_all_components(model)
    result = []

    for key, comp in components.items():
        if filter_func is None or filter_func(comp):
            result.append((key, comp))

    return result


def count_components_by_definition(model: Model) -> Dict[str, int]:
    """
    Count components grouped by definition type.

    Args:
        model: CloudPSS Model object

    Returns:
        Dict mapping definition -> count
    """
    components = get_all_components(model)
    counts: Dict[str, int] = {}

    for comp in components.values():
        definition = getattr(comp, "definition", "")
        if definition:
            counts[definition] = counts.get(definition, 0) + 1

    return counts
