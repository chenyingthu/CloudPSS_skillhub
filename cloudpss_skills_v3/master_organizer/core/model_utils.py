"""Model utility functions for CloudPSS model operations."""

from __future__ import annotations

from typing import Any


def fetch_model_summary(rid: str) -> dict[str, Any] | None:
    """Fetch model summary from CloudPSS.

    Args:
        rid: Resource ID of the model (e.g., "model/user/modelname")

    Returns:
        Model summary dict or None if not found
    """
    # TODO: Implement actual CloudPSS API call
    # For now, return a mock response for testing
    if rid.startswith("model/"):
        return {
            "rid": rid,
            "name": rid.split("/")[-1],
            "description": f"Model {rid}",
            "components": 15,
            "topology": {"buses": 5, "branches": 4},
        }
    return None


def fetch_model_parameters(rid: str, component: str = "") -> dict[str, Any]:
    """Fetch model parameters from CloudPSS.

    Args:
        rid: Resource ID of the model
        component: Optional component type filter (e.g., "bus", "line")

    Returns:
        Model parameters dict
    """
    # TODO: Implement actual CloudPSS API call
    # For now, return mock response for testing
    result: dict[str, Any] = {
        "rid": rid,
        "parameters": [
            {"name": "baseMVA", "value": 100.0, "unit": "MVA"},
            {"name": "frequency", "value": 50.0, "unit": "Hz"},
        ],
        "component_parameters": {
            "bus": [{"id": 1, "type": "slack", "v": 1.0}],
            "line": [{"from": 1, "to": 2, "r": 0.01, "x": 0.1}],
        },
    }

    if component:
        # Filter by component type
        filtered = result["component_parameters"].get(component, [])
        result["component_parameters"] = {component: filtered}

    return result


def list_available_models() -> list[dict[str, Any]]:
    """List available models from CloudPSS.

    Returns:
        List of model info dicts
    """
    # TODO: Implement actual CloudPSS API call
    # For now, return mock data for testing
    return [
        {"rid": "model/user1/ieee14", "name": "IEEE 14 Bus"},
        {"rid": "model/user1/ieee39", "name": "IEEE 39 Bus"},
        {"rid": "model/user2/test", "name": "Test Model"},
    ]


def validate_rid(rid: str) -> dict[str, Any]:
    """Validate RID format.

    Args:
        rid: Resource ID to validate

    Returns:
        Validation result dict with 'valid' boolean and optional 'message'
    """
    if not rid:
        return {
            "valid": False,
            "rid": rid,
            "message": "RID cannot be empty",
        }

    if not rid.startswith("model/"):
        return {
            "valid": False,
            "rid": rid,
            "message": "RID must start with 'model/'",
        }

    parts = rid.split("/")
    if len(parts) < 3:
        return {
            "valid": False,
            "rid": rid,
            "message": "RID must have format 'model/{user}/{name}'",
        }

    return {
        "valid": True,
        "rid": rid,
        "message": "RID format is valid",
    }


def load_model_from_cloud(rid: str, output_path: str | None = None) -> dict[str, Any]:
    """Load a model from CloudPSS cloud.

    Args:
        rid: Resource ID of the model
        output_path: Optional local path to save the model

    Returns:
        Model data dict
    """
    # TODO: Implement actual CloudPSS API call
    raise NotImplementedError("Cloud model loading not yet implemented")


def load_model_from_local(path: str) -> dict[str, Any]:
    """Load a model from local file.

    Args:
        path: Path to local model file

    Returns:
        Model data dict
    """
    import json
    from pathlib import Path

    model_path = Path(path)
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {path}")

    with open(model_path, encoding="utf-8") as f:
        return json.load(f)
