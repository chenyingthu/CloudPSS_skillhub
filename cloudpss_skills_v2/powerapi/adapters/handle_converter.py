"""Shared ModelHandle to PowerSystemModel conversion utilities."""

from __future__ import annotations

import logging
from typing import Any

from cloudpss_skills_v2.core.system_model import (
    Branch,
    Bus,
    Generator,
    Load,
    PowerSystemModel,
)
from cloudpss_skills_v2.powerskill import ComponentType

logger = logging.getLogger(__name__)


def _component_data(component: Any) -> dict[str, Any]:
    args = getattr(component, "args", None)
    if isinstance(args, dict) and args:
        return args
    properties = getattr(component, "properties", None)
    if isinstance(properties, dict):
        return properties
    return {}


def _float_value(value: Any, default: float) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _bool_value(value: Any, default: bool = True) -> bool:
    if value is None or value == "":
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() not in {"false", "0", "no", "off"}
    return bool(value)


def _parse_bus_id(value: Any) -> int | None:
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        raw = value.split(":")[-1] if ":" in value else value
        try:
            return int(raw)
        except ValueError:
            return None
    return None


def _bus_aliases(original_key: Any, bus_id: int) -> set[Any]:
    return {original_key, bus_id, str(bus_id), f"bus:{bus_id}"}


def _resolve_bus(value: Any, bus_id_map: dict[Any, int]) -> int | None:
    if value in bus_id_map:
        return bus_id_map[value]
    bus_id = _parse_bus_id(value)
    if bus_id is None:
        return None
    return bus_id if bus_id in bus_id_map.values() else None


def _components(handle: Any, component_type: str) -> list[Any]:
    try:
        return list(handle.get_components_by_type(component_type))
    except Exception as exc:
        logger.debug("Could not get %s components: %s", component_type, exc)
        return []


def convert_handle_to_power_system_model(handle: Any, *, base_mva: float = 100.0) -> PowerSystemModel:
    """Convert a powerskill ModelHandle-like object to a unified model.

    The converter is intentionally conservative: it resolves branch and
    transformer endpoints only from explicit component data and skips invalid
    topology instead of fabricating bus connections.
    """
    slack_bus_refs: set[Any] = set()
    for component in _components(handle, ComponentType.SOURCE):
        data = _component_data(component)
        bus_ref = data.get("bus")
        if bus_ref is None or bus_ref == "":
            continue
        slack_bus_refs.add(bus_ref)
        parsed = _parse_bus_id(bus_ref)
        if parsed is not None:
            slack_bus_refs.update({parsed, str(parsed), f"bus:{parsed}"})

    buses: list[Bus] = []
    bus_id_map: dict[Any, int] = {}
    for index, component in enumerate(_components(handle, ComponentType.BUS)):
        data = _component_data(component)
        original_key = getattr(component, "key", index)
        bus_id = _parse_bus_id(original_key)
        if bus_id is None:
            bus_id = index

        for alias in _bus_aliases(original_key, bus_id):
            bus_id_map[alias] = bus_id

        base_kv = _float_value(data.get("vn_kv", data.get("base_kv", 110.0)), 110.0)
        voltage_pu = _float_value(data.get("vm_pu", data.get("v_magnitude_pu", 1.0)), 1.0)
        is_slack = bool(slack_bus_refs.intersection(_bus_aliases(original_key, bus_id)))
        buses.append(
            Bus(
                bus_id=bus_id,
                name=getattr(component, "name", None) or str(original_key),
                base_kv=base_kv,
                v_magnitude_pu=voltage_pu,
                bus_type="SLACK" if is_slack else "PQ",
            )
        )

    branches: list[Branch] = []
    for component in _components(handle, ComponentType.BRANCH):
        branch = _branch_from_component(component, bus_id_map, branch_type="LINE")
        if branch is not None:
            branches.append(branch)

    for component in _components(handle, ComponentType.TRANSFORMER):
        branch = _branch_from_component(component, bus_id_map, branch_type="TRANSFORMER")
        if branch is not None:
            branches.append(branch)

    loads: list[Load] = []
    for component in _components(handle, ComponentType.LOAD):
        data = _component_data(component)
        bus_id = _resolve_bus(data.get("bus"), bus_id_map)
        if bus_id is None:
            logger.debug("Skipping load %s: cannot resolve bus ID", getattr(component, "key", ""))
            continue
        loads.append(
            Load(
                bus_id=bus_id,
                name=getattr(component, "name", None) or str(getattr(component, "key", "")),
                p_mw=_float_value(data.get("p_mw"), 0.0),
                q_mvar=_float_value(data.get("q_mvar"), 0.0),
                in_service=_bool_value(data.get("in_service"), True),
            )
        )

    generators: list[Generator] = []
    for component in _components(handle, ComponentType.GENERATOR):
        data = _component_data(component)
        bus_id = _resolve_bus(data.get("bus"), bus_id_map)
        if bus_id is None:
            logger.debug("Skipping generator %s: cannot resolve bus ID", getattr(component, "key", ""))
            continue
        generators.append(
            Generator(
                bus_id=bus_id,
                name=getattr(component, "name", None) or str(getattr(component, "key", "")),
                p_gen_mw=_float_value(data.get("p_gen_mw", data.get("p_mw")), 0.0),
                v_set_pu=_float_value(data.get("v_set_pu"), 1.0),
                in_service=_bool_value(data.get("in_service"), True),
            )
        )

    return PowerSystemModel(
        buses=buses,
        branches=branches,
        loads=loads,
        generators=generators,
        base_mva=base_mva,
    )


def _branch_from_component(
    component: Any,
    bus_id_map: dict[Any, int],
    *,
    branch_type: str,
) -> Branch | None:
    data = _component_data(component)
    from_bus = _resolve_bus(data.get("from_bus"), bus_id_map)
    to_bus = _resolve_bus(data.get("to_bus"), bus_id_map)
    key = getattr(component, "key", "")

    if from_bus is None or to_bus is None:
        logger.debug("Skipping %s %s: cannot resolve bus IDs", branch_type.lower(), key)
        return None
    if from_bus == to_bus:
        logger.debug("Skipping %s %s: connects bus %s to itself", branch_type.lower(), key, from_bus)
        return None

    if branch_type == "TRANSFORMER":
        r_default = 0.001
        x_default = 0.05
        r_value = data.get("r_pu", data.get("r_ohm"))
        x_value = data.get("x_pu", data.get("x_ohm"))
        rate_value = data.get("rate_a_mva", data.get("sn_mva"))
    else:
        r_default = 0.001
        x_default = 0.01
        r_value = data.get("r_pu")
        x_value = data.get("x_pu")
        rate_value = data.get("rate_a_mva")

    try:
        return Branch(
            name=key or f"{branch_type.title()}{from_bus}-{to_bus}",
            from_bus=from_bus,
            to_bus=to_bus,
            branch_type=branch_type,
            r_pu=_float_value(r_value, r_default),
            x_pu=_float_value(x_value, x_default),
            rate_a_mva=_float_value(rate_value, 0.0),
            in_service=_bool_value(data.get("in_service"), True),
            tap_ratio=_float_value(data.get("tap_ratio", data.get("tap_pos")), 1.0),
            phase_shift_degree=_float_value(
                data.get(
                    "phase_shift_degree",
                    data.get("shift_degree", data.get("phase_shift")),
                ),
                0.0,
            ),
        )
    except ValueError as exc:
        logger.debug("Skipping %s %s: %s", branch_type.lower(), key, exc)
        return None


__all__ = ["convert_handle_to_power_system_model"]
