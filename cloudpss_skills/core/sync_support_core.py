"""
Shared helpers for synchronous-compensator style EMT construction.
"""

import ast
import copy
import math
import operator
from typing import Any, Dict, List, Optional, Set, Tuple

from cloudpss import Model

from cloudpss_skills.core.utils import clean_component_key, get_bus_components

_SAFE_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}
_SAFE_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}
_SAFE_CALLS = {
    "sqrt": math.sqrt,
    "abs": abs,
}


def matches_bus_identifier(candidate: str, target: str) -> bool:
    candidate_norm = (candidate or "").strip().lower()
    target_norm = (target or "").strip().lower()
    if not candidate_norm or not target_norm:
        return False
    if candidate_norm == target_norm:
        return True
    compact_candidate = "".join(ch for ch in candidate_norm if ch.isalnum())
    compact_target = "".join(ch for ch in target_norm if ch.isalnum())
    if compact_candidate and compact_candidate == compact_target:
        return True
    candidate_digits = "".join(ch for ch in candidate_norm if ch.isdigit())
    target_digits = "".join(ch for ch in target_norm if ch.isdigit())
    return bool(candidate_digits and target_digits and candidate_digits == target_digits)


def as_numeric(value: Any, default: float = 0.0) -> float:
    if isinstance(value, dict):
        value = value.get("source")
    if value in (None, ""):
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def get_model_variable_map(model: Model) -> Dict[str, float]:
    variables: Dict[str, float] = {}
    try:
        entries = model.toJSON()["revision"]["implements"]["diagram"].get("variables", [])
    except (KeyError, TypeError, AttributeError):
        return variables

    for entry in entries:
        key = entry.get("key")
        if not key:
            continue
        raw_value = entry.get("value")
        parsed = as_numeric(raw_value, default=math.nan)
        if not math.isnan(parsed):
            variables[key] = parsed
    return variables


def evaluate_numeric_expression(expression: str, variables: Dict[str, float]) -> float:
    tree = ast.parse(expression, mode="eval")

    def _eval(node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)
        if isinstance(node, ast.Name) and node.id in _SAFE_CALLS:
            return _SAFE_CALLS[node.id]
        if isinstance(node, ast.BinOp) and type(node.op) in _SAFE_BINARY_OPERATORS:
            return _SAFE_BINARY_OPERATORS[type(node.op)](_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in _SAFE_UNARY_OPERATORS:
            return _SAFE_UNARY_OPERATORS[type(node.op)](_eval(node.operand))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in _SAFE_CALLS:
            return _SAFE_CALLS[node.func.id](*[_eval(arg) for arg in node.args])
        raise ValueError(f"不支持的数值表达式: {expression}")

    return float(_eval(tree))


def resolve_model_numeric(model: Model, value: Any, default: float = 0.0) -> float:
    if isinstance(value, dict):
        value = value.get("source")
    if value in (None, ""):
        return default
    if isinstance(value, (int, float)):
        return float(value)
    if not isinstance(value, str):
        return default

    expression = value.strip()
    if not expression:
        return default

    variables = get_model_variable_map(model)
    for key, numeric_value in variables.items():
        expression = expression.replace(f"${key}", str(numeric_value))

    try:
        return evaluate_numeric_expression(expression, variables)
    except (ValueError, SyntaxError, TypeError, ZeroDivisionError):
        return as_numeric(value, default=default)


def as_signal_token(value: Any) -> str:
    if isinstance(value, dict):
        value = value.get("source")
    return "" if value is None else str(value)


def find_diagram_edges_for_component(model: Model, component_id: str) -> List[Any]:
    edges = []
    for component in model.getAllComponents().values():
        if getattr(component, "shape", None) != "diagram-edge":
            continue
        source = getattr(component, "source", {}) or {}
        target = getattr(component, "target", {}) or {}
        if source.get("cell") == component_id or target.get("cell") == component_id:
            edges.append(component)
    return edges


def select_sync_template(model: Model, target_bus: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    sync_templates = list(model.getComponentsByRid("model/CloudPSS/SyncGeneratorRouter").values())
    exciters = list(model.getComponentsByRid("model/CloudPSS/_EXST1_PTI").values())
    governors = list(model.getComponentsByRid("model/CloudPSS/_STEAM_GOV_1").values())
    turbines = list(model.getComponentsByRid("model/CloudPSS/_STEAM_TUR_1").values())
    candidates = []

    for sync in sync_templates:
        vt_token = as_signal_token(sync.args.get("VT_o"))
        it_token = as_signal_token(sync.args.get("IT_o"))
        ef0_token = as_signal_token(sync.args.get("Ef0_o"))
        wr_token = as_signal_token(sync.args.get("wr_o"))
        tm0_token = as_signal_token(sync.args.get("Tm0_o"))
        tm_token = str((sync.pins or {}).get("2", ""))

        exciter = next(
            (
                comp
                for comp in exciters
                if str((comp.pins or {}).get("2", "")) == vt_token
                and str((comp.pins or {}).get("3", "")) == it_token
                and str((comp.pins or {}).get("4", "")) == ef0_token
            ),
            None,
        )
        governor = next(
            (
                comp
                for comp in governors
                if str((comp.pins or {}).get("2", "")) == wr_token
            ),
            None,
        )
        turbine = next(
            (
                comp
                for comp in turbines
                if str((comp.pins or {}).get("1", "")) == wr_token
                and str((comp.pins or {}).get("3", "")) == tm0_token
                and str((comp.pins or {}).get("8", "")) == tm_token
            ),
            None,
        )
        if exciter is None or governor is None or turbine is None:
            continue

        local_bus = None
        transformer = None
        network_bus = None
        for edge in find_diagram_edges_for_component(model, sync.id):
            source = getattr(edge, "source", {}) or {}
            target = getattr(edge, "target", {}) or {}
            other_id = target.get("cell") if source.get("cell") == sync.id else source.get("cell")
            if not other_id:
                continue
            other = model.getComponentByKey(other_id)
            if getattr(other, "definition", None) == "model/CloudPSS/_newBus_3p":
                local_bus = other
                break
        if local_bus is None:
            continue

        for edge in find_diagram_edges_for_component(model, local_bus.id):
            source = getattr(edge, "source", {}) or {}
            target = getattr(edge, "target", {}) or {}
            other_id = target.get("cell") if source.get("cell") == local_bus.id else source.get("cell")
            if not other_id or other_id == sync.id:
                continue
            other = model.getComponentByKey(other_id)
            if getattr(other, "definition", None) == "model/CloudPSS/_newTransformer_3p2w":
                transformer = other
                break
        if transformer is None:
            continue

        for edge in find_diagram_edges_for_component(model, transformer.id):
            source = getattr(edge, "source", {}) or {}
            target = getattr(edge, "target", {}) or {}
            other_id = target.get("cell") if source.get("cell") == transformer.id else source.get("cell")
            if not other_id or other_id == local_bus.id:
                continue
            other = model.getComponentByKey(other_id)
            if getattr(other, "definition", None) == "model/CloudPSS/_newBus_3p":
                network_bus = other
                break
        if network_bus is None:
            continue

        template_components = {
            sync.id,
            local_bus.id,
            transformer.id,
            exciter.id,
            governor.id,
            turbine.id,
        }
        whitelist = {
            "model/CloudPSS/_newGain",
            "model/CloudPSS/_newLoopNode",
            "model/CloudPSS/_PSS1A",
            "model/CloudPSS/_newSum",
            "model/CloudPSS/_newConstant",
            "model/CloudPSS/ElectricalLable",
        }
        queue = [exciter.id, governor.id, turbine.id]
        seen: Set[str] = set(queue)
        while queue:
            current = queue.pop()
            for edge in find_diagram_edges_for_component(model, current):
                source = getattr(edge, "source", {}) or {}
                target = getattr(edge, "target", {}) or {}
                other_id = target.get("cell") if source.get("cell") == current else source.get("cell")
                if not other_id or other_id in seen:
                    continue
                other = model.getComponentByKey(other_id)
                if getattr(other, "definition", None) in whitelist:
                    seen.add(other_id)
                    queue.append(other_id)
                    template_components.add(other_id)

        template_edges = set()
        transformer_to_network_edge_id = None
        for component_id in template_components:
            for edge in find_diagram_edges_for_component(model, component_id):
                source = getattr(edge, "source", {}) or {}
                target = getattr(edge, "target", {}) or {}
                src_id = source.get("cell")
                tgt_id = target.get("cell")
                if src_id in template_components and tgt_id in template_components:
                    template_edges.add(edge.id)
                elif edge.id not in template_edges and component_id == transformer.id:
                    other_id = tgt_id if src_id == transformer.id else src_id
                    if other_id == network_bus.id:
                        template_edges.add(edge.id)
                        transformer_to_network_edge_id = edge.id

        candidates.append(
            {
                "sync": sync,
                "local_bus": local_bus,
                "transformer": transformer,
                "network_bus": network_bus,
                "exciter": exciter,
                "governor": governor,
                "turbine": turbine,
                "component_ids": template_components,
                "edge_ids": template_edges,
                "transformer_to_network_edge_id": transformer_to_network_edge_id,
            }
        )

    if not candidates:
        return None
    if target_bus is None:
        return candidates[0]

    target_name = str(target_bus.get("name", "")).strip().lower()
    target_label = str(target_bus.get("label", "")).strip().lower()
    for candidate in candidates:
        network_bus = candidate["network_bus"]
        network_name = str(network_bus.args.get("Name", "")).strip().lower()
        network_label = str(getattr(network_bus, "label", "")).strip().lower()
        if (
            (target_name and network_name == target_name)
            or (target_name and network_label == target_name)
            or (target_label and network_name == target_label)
            or (target_label and network_label == target_label)
        ):
            return candidate
    return candidates[0]


def clone_sync_template_chain(
    model: Model,
    target_bus: Dict[str, Any],
    initial_capacity: float,
) -> Optional[Tuple[str, str]]:
    template = select_sync_template(model, target_bus=target_bus)
    if template is None:
        return None

    from cloudpss.model.implements.component import Component

    target_component = model.getComponentByKey(target_bus["key"])
    target_vm = resolve_model_numeric(model, target_component.args.get("V"), 1.0)
    target_va = float(target_component.args.get("Theta", 0.0))
    target_vbase = resolve_model_numeric(model, target_component.args.get("VBase"), 1.0)

    local_bus_template = template["local_bus"]
    low_side_vbase = resolve_model_numeric(model, local_bus_template.args.get("VBase"), 1.0)
    low_side_phase = low_side_vbase / math.sqrt(3)

    sync_template = template["sync"]
    suffix = clean_component_key(target_bus["name"] or target_bus["label"] or target_bus["key"])
    unique_suffix = suffix or str(len(template["component_ids"]))

    signal_map = {
        as_signal_token(sync_template.args.get("VT_o")): f"#VT_{unique_suffix}",
        as_signal_token(sync_template.args.get("IT_o")): f"#IT_{unique_suffix}",
        as_signal_token(sync_template.args.get("Ef0_o")): f"#Ef0_{unique_suffix}",
        as_signal_token(sync_template.args.get("Tm0_o")): f"#Tm0_{unique_suffix}",
        as_signal_token(sync_template.args.get("wr_o")): f"#wr_{unique_suffix}",
        as_signal_token(sync_template.args.get("PT_o")): f"#P_{unique_suffix}",
        as_signal_token(sync_template.args.get("QT_o")): f"#Q_{unique_suffix}",
        as_signal_token(sync_template.args.get("s2m_o")): f"#initEx_{unique_suffix}",
        as_signal_token(sync_template.args.get("l2n_o")): f"#initGv_{unique_suffix}",
        str((sync_template.pins or {}).get("2", "")): f"Tm_{unique_suffix}",
        str((local_bus_template.pins or {}).get("0", "")): f"CompBus_{unique_suffix}",
    }
    signal_map = {old: new for old, new in signal_map.items() if old}

    component_ids = sorted(template["component_ids"])
    edge_ids = sorted(template["edge_ids"])
    component_id_map = {
        old_id: f"comp_sync_clone_{unique_suffix}_{index}"
        for index, old_id in enumerate(component_ids, 1)
    }
    edge_id_map = {
        old_id: f"edge_sync_clone_{unique_suffix}_{index}"
        for index, old_id in enumerate(edge_ids, 1)
    }

    base_position = local_bus_template.position
    shift_x = target_component.position["x"] + 260 - base_position["x"]
    shift_y = target_component.position["y"] - base_position["y"]
    cells = model.revision.getImplements().getDiagram().cells

    def replace_value(value: Any) -> Any:
        if isinstance(value, dict):
            updated = copy.deepcopy(value)
            if "source" in updated and isinstance(updated["source"], str):
                source_value = updated["source"]
                for old, new in signal_map.items():
                    source_value = source_value.replace(old, new)
                updated["source"] = source_value
            return updated
        if isinstance(value, str):
            updated = value
            for old, new in signal_map.items():
                updated = updated.replace(old, new)
            return updated
        return copy.deepcopy(value)

    cloned_sync_id = None
    cloned_transformer_id = None
    for old_id in component_ids:
        component = model.getComponentByKey(old_id)
        component_json = copy.deepcopy(component.toJSON())
        new_id = component_id_map[old_id]
        component_json["id"] = new_id
        if "position" in component_json and isinstance(component_json["position"], dict):
            component_json["position"]["x"] += shift_x
            component_json["position"]["y"] += shift_y
        if "pins" in component_json:
            component_json["pins"] = {
                pin_key: replace_value(pin_value)
                for pin_key, pin_value in component_json["pins"].items()
            }
        if "args" in component_json:
            component_json["args"] = {
                arg_key: replace_value(arg_value)
                for arg_key, arg_value in component_json["args"].items()
            }

        definition = component_json.get("definition")
        if definition == "model/CloudPSS/SyncGeneratorRouter":
            cloned_sync_id = new_id
            component_json["label"] = f"SyncComp-{unique_suffix}"
            component_json["args"]["Name"] = f"调相机_{target_bus['label']}"
            component_json["args"]["AP"] = 0
            component_json["args"]["RP"] = 0
            component_json["args"]["BusType"] = "0"
            component_json["args"]["pf_P"] = {"source": "0", "ɵexp": ""}
            component_json["args"]["pf_Q"] = {"source": "0", "ɵexp": ""}
            component_json["args"]["pf_Qmax"] = {"source": str(max(initial_capacity * 3, 300)), "ɵexp": ""}
            component_json["args"]["pf_Qmin"] = {"source": str(-max(initial_capacity * 3, 300)), "ɵexp": ""}
            component_json["args"]["Smva"] = {"source": str(initial_capacity), "ɵexp": ""}
            component_json["args"]["V"] = {"source": str(low_side_phase), "ɵexp": ""}
            component_json["args"]["V_mag"] = target_vm
            component_json["args"]["V_ph"] = target_va
            component_json["pins"]["2"] = signal_map[str((sync_template.pins or {}).get("2", ""))]
        elif definition == "model/CloudPSS/_newBus_3p":
            component_json["label"] = f"CompBus-{unique_suffix}"
            component_json["args"]["Name"] = f"CompBus_{unique_suffix}"
            component_json["args"]["VBase"] = {"source": str(low_side_vbase), "ɵexp": ""}
            component_json["args"]["V"] = target_vm
            component_json["args"]["Theta"] = target_va
            component_json["pins"]["0"] = signal_map[str((local_bus_template.pins or {}).get("0", ""))]
        elif definition == "model/CloudPSS/_newTransformer_3p2w":
            cloned_transformer_id = new_id
            component_json["label"] = f"Transformer-{unique_suffix}"
            component_json["args"]["Name"] = f"Trans_{unique_suffix}"
            component_json["args"]["V1"] = {"source": str(low_side_vbase), "ɵexp": ""}
            component_json["args"]["V2"] = {"source": str(target_vbase), "ɵexp": ""}
            component_json["args"]["Tmva"] = {"source": str(initial_capacity), "ɵexp": ""}

        cells[new_id] = Component(component_json)

    for old_id in edge_ids:
        edge = model.getComponentByKey(old_id)
        edge_json = copy.deepcopy(edge.toJSON())
        edge_json["id"] = edge_id_map[old_id]
        if "source" in edge_json and edge_json["source"].get("cell") in component_id_map:
            edge_json["source"]["cell"] = component_id_map[edge_json["source"]["cell"]]
        if "target" in edge_json and edge_json["target"].get("cell") in component_id_map:
            edge_json["target"]["cell"] = component_id_map[edge_json["target"]["cell"]]
        if old_id == template["transformer_to_network_edge_id"]:
            edge_json["target"]["cell"] = target_bus["key"]
        if "vertices" in edge_json:
            for vertex in edge_json["vertices"]:
                if isinstance(vertex, dict):
                    vertex["x"] += shift_x
                    vertex["y"] += shift_y
        cells[edge_json["id"]] = Component(edge_json)

    if not cloned_sync_id or not cloned_transformer_id:
        return None
    return cloned_sync_id, cloned_transformer_id


def configure_fault_scenario(
    model: Model,
    *,
    fault_bus_label: Optional[str],
    fault_time: float,
    fault_duration: float,
    chg: float = 0.01,
) -> Optional[str]:
    fault_components = list(model.getComponentsByRid("model/CloudPSS/_newFaultResistor_3p").values())
    if not fault_components:
        return None

    fault = fault_components[0]
    fault.args["fs"] = {"source": str(fault_time), "ɵexp": ""}
    fault.args["fe"] = {"source": str(fault_time + fault_duration), "ɵexp": ""}
    fault.args["chg"] = {"source": str(chg), "ɵexp": ""}

    if not fault_bus_label:
        return None

    buses = get_bus_components(model)
    target_bus_key = None
    for key, data in buses.items():
        label = data.get("label", "")
        name = str(data.get("args", {}).get("Name", ""))
        if matches_bus_identifier(label, fault_bus_label) or matches_bus_identifier(name, fault_bus_label):
            target_bus_key = key
            break
    if not target_bus_key:
        return None

    for edge in find_diagram_edges_for_component(model, fault.id):
        source = getattr(edge, "source", {}) or {}
        target = getattr(edge, "target", {}) or {}
        if source.get("cell") == fault.id and source.get("port") == "1":
            edge.target["cell"] = target_bus_key
            return target_bus_key
        if target.get("cell") == fault.id and target.get("port") == "1":
            edge.source["cell"] = target_bus_key
            return target_bus_key
    return target_bus_key
