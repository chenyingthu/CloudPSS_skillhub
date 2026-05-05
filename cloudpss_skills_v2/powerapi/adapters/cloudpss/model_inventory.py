"""CloudPSS static model inventory and parameter diagnostics."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from cloudpss_skills_v2.powerskill.model_handle import ComponentType


@dataclass
class CloudPSSComponentRecord:
    """Auditable static CloudPSS component snapshot."""

    component_id: str
    name: str
    definition: str
    component_type: str
    args: dict[str, Any] = field(default_factory=dict)
    pins: dict[str, Any] = field(default_factory=dict)
    extracted_parameters: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "component_id": self.component_id,
            "name": self.name,
            "definition": self.definition,
            "component_type": self.component_type,
            "args": self.args,
            "pins": self.pins,
            "extracted_parameters": self.extracted_parameters,
        }


@dataclass
class CloudPSSModelInventory:
    """Static component inventory for a CloudPSS model."""

    model_name: str = ""
    model_rid: str = ""
    components: list[CloudPSSComponentRecord] = field(default_factory=list)
    warnings: list[dict[str, str]] = field(default_factory=list)

    def component_type_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for record in self.components:
            counts[record.component_type] = counts.get(record.component_type, 0) + 1
        return counts

    def parameter_index(self) -> dict[str, dict[str, dict[str, Any]]]:
        """Return indexes used to enrich CloudPSS power-flow result rows."""
        bus_by_component_id: dict[str, dict[str, Any]] = {}
        bus_by_node_name: dict[str, dict[str, Any]] = {}
        branch_by_component_id: dict[str, dict[str, Any]] = {}

        for record in self.components:
            params = record.extracted_parameters
            if not params:
                continue
            if record.component_type == ComponentType.BUS:
                bus_by_component_id[record.component_id] = params
                node_name = params.get("node_name")
                if node_name:
                    bus_by_node_name[str(node_name)] = params
            elif record.component_type in (ComponentType.BRANCH, ComponentType.TRANSFORMER):
                branch_by_component_id[record.component_id] = params

        return {
            "bus_by_component_id": bus_by_component_id,
            "bus_by_node_name": bus_by_node_name,
            "branch_by_component_id": branch_by_component_id,
        }

    def diagnostics(self) -> dict[str, Any]:
        """Return CloudPSS-aligned static parameter diagnostics."""
        findings = list(self.warnings)
        line_records = [
            item for item in self.components if item.component_type == ComponentType.BRANCH
        ]
        transformer_records = [
            item for item in self.components if item.component_type == ComponentType.TRANSFORMER
        ]
        bus_records = [
            item for item in self.components if item.component_type == ComponentType.BUS
        ]

        missing_line_impedance = [
            item.component_id
            for item in line_records
            if item.extracted_parameters.get("r_pu") is None
            or item.extracted_parameters.get("x_pu") is None
        ]
        missing_transformer_impedance = [
            item.component_id
            for item in transformer_records
            if item.extracted_parameters.get("x_pu") is None
        ]
        missing_bus_base = [
            item.component_id
            for item in bus_records
            if item.extracted_parameters.get("voltage_kv") is None
        ]

        if missing_line_impedance:
            findings.append({
                "severity": "warning",
                "code": "missing_line_static_impedance",
                "message": f"{len(missing_line_impedance)} CloudPSS line components lack R/X static parameters",
            })
        if missing_transformer_impedance:
            findings.append({
                "severity": "warning",
                "code": "missing_transformer_static_impedance",
                "message": f"{len(missing_transformer_impedance)} CloudPSS transformer components lack X static parameters",
            })
        if missing_bus_base:
            findings.append({
                "severity": "warning",
                "code": "missing_bus_base_voltage",
                "message": f"{len(missing_bus_base)} CloudPSS bus components lack base voltage",
            })

        return {
            "status": "warning" if findings else "pass",
            "model": {
                "name": self.model_name,
                "rid": self.model_rid,
            },
            "component_type_counts": self.component_type_counts(),
            "parameter_coverage": {
                "line_count": len(line_records),
                "line_with_r_x_count": len(line_records) - len(missing_line_impedance),
                "transformer_count": len(transformer_records),
                "transformer_with_x_count": len(transformer_records) - len(missing_transformer_impedance),
                "bus_count": len(bus_records),
                "bus_with_base_voltage_count": len(bus_records) - len(missing_bus_base),
            },
            "findings": findings,
        }


class CloudPSSInventoryExtractor:
    """Extract a static, auditable CloudPSS component inventory."""

    _BRANCH_DEFINITIONS = [
        "model/CloudPSS/line",
        "model/CloudPSS/3pline",
        "model/CloudPSS/transformer",
        "model/CloudPSS/3ptransformer",
        "model/CloudPSS/TransmissionLine",
        "model/CloudPSS/_newTransformer_3p2w",
        "model/CloudPSS/_newTransformer_3p",
    ]

    _LOAD_DEFINITIONS = ["Load", "_newExpLoad", "_newLoad"]
    _GENERATOR_DEFINITIONS = ["Generator", "Gen", "SyncGenerator", "_newGenerator"]
    _TRANSFORMER_DEFINITIONS = [
        "transformer",
        "3ptransformer",
        "_newTransformer_3p2w",
        "_newTransformer_3p",
    ]
    _BUS_DEFINITIONS = [
        "model/CloudPSS/_newBus_3p",
        "model/CloudPSS/Bus",
    ]
    _SHUNT_DEFINITIONS = ["Shunt", "_newShunt"]

    def extract(self, model: Any) -> CloudPSSModelInventory:
        inventory = CloudPSSModelInventory(
            model_name=str(getattr(model, "name", "")),
            model_rid=str(getattr(model, "rid", "")),
        )
        try:
            components = model.getAllComponents()
        except Exception as exc:
            inventory.warnings.append({
                "severity": "warning",
                "code": "component_read_failed",
                "message": f"Could not read CloudPSS components: {exc}",
            })
            return inventory

        for component_id, component in components.items():
            definition = str(getattr(component, "definition", ""))
            args = self.component_args(component)
            pins = getattr(component, "pins", {})
            if not isinstance(pins, dict):
                pins = {}
            component_type = self.classify_component(definition)
            inventory.components.append(
                CloudPSSComponentRecord(
                    component_id=str(component_id),
                    name=str(getattr(component, "name", getattr(component, "label", component_id))),
                    definition=definition,
                    component_type=component_type,
                    args=args,
                    pins=dict(pins),
                    extracted_parameters=self.extract_parameters(
                        str(component_id),
                        component,
                        args,
                        component_type,
                    ),
                )
            )
        return inventory

    @classmethod
    def classify_component(cls, definition: str) -> str:
        d = str(definition)
        d_lower = d.lower()
        if cls.is_bus_definition(d):
            return ComponentType.BUS
        for branch_def in cls._BRANCH_DEFINITIONS:
            if branch_def in d:
                if any(t in d_lower for t in cls._TRANSFORMER_DEFINITIONS):
                    return ComponentType.TRANSFORMER
                return ComponentType.BRANCH
        for shunt_def in cls._SHUNT_DEFINITIONS:
            if shunt_def.lower() in d_lower:
                return ComponentType.SHUNT
        for load_def in cls._LOAD_DEFINITIONS:
            if load_def in d:
                return ComponentType.LOAD
        for gen_def in cls._GENERATOR_DEFINITIONS:
            if gen_def in d:
                return ComponentType.GENERATOR
        return ComponentType.OTHER

    @classmethod
    def is_bus_definition(cls, definition: str) -> bool:
        d = str(definition)
        return any(bus_def in d for bus_def in cls._BUS_DEFINITIONS)

    @classmethod
    def component_args(cls, component: Any) -> dict[str, Any]:
        args = getattr(component, "args", None)
        if not isinstance(args, dict):
            return {}
        return {key: cloudpss_arg_value(value) for key, value in args.items()}

    def extract_parameters(
        self,
        component_id: str,
        component: Any,
        args: dict[str, Any],
        component_type: str,
    ) -> dict[str, Any]:
        if component_type == ComponentType.BUS:
            return self.extract_bus_parameters(component, args)
        if component_type == ComponentType.BRANCH:
            return self.extract_line_parameters(component_id, component, args)
        if component_type == ComponentType.TRANSFORMER:
            return self.extract_transformer_parameters(component_id, component, args)
        if component_type == ComponentType.LOAD:
            return {
                "p_mw": parse_float(first_present(args, "P", "p", "p_mw", "Pl"), None),
                "q_mvar": parse_float(first_present(args, "Q", "q", "q_mvar", "Ql"), None),
            }
        if component_type == ComponentType.GENERATOR:
            return {
                "p_mw": parse_float(first_present(args, "P", "pf_P", "p_mw", "Pg"), None),
                "q_mvar": parse_float(first_present(args, "Q", "pf_Q", "q_mvar", "Qg"), None),
                "v_set_pu": parse_float(first_present(args, "Vset", "pf_V", "v_set_pu"), None),
            }
        if component_type == ComponentType.SHUNT:
            return {
                "q_mvar": parse_float(first_present(args, "Q", "q_mvar", "B"), None),
            }
        return {}

    def extract_bus_parameters(self, component: Any, args: dict[str, Any]) -> dict[str, Any]:
        pins = getattr(component, "pins", {})
        node_name = first_present(pins, "0") if isinstance(pins, dict) else None
        return {
            "node_name": node_name,
            "voltage_kv": parse_float(
                first_present(args, "VBase", "Vbase", "base_kv", "voltage_kv"),
                None,
            ),
            "frequency_hz": parse_float(first_present(args, "Freq", "freq"), None),
        }

    def extract_line_parameters(
        self,
        component_id: str,
        component: Any,
        args: dict[str, Any],
    ) -> dict[str, Any]:
        r_pu = parse_float(first_present(args, "R1pu", "r_pu", "Rpu"), None)
        x_pu = parse_float(first_present(args, "X1pu", "x_pu", "Xpu"), None)
        b_pu = parse_float(first_present(args, "B1pu", "b_pu", "Bpu"), None)
        sbase = parse_float(first_present(args, "Sbase", "base_mva"), None)
        vbase = parse_float(first_present(args, "Vbase", "VBase", "base_kv"), None)
        rate = parse_float(first_present(args, "Rate", "rate_a_mva", "Smva"), None)
        irated = parse_float(first_present(args, "Irated", "Ir"), None)
        if rate is None and irated is not None and irated > 0 and vbase:
            rate = (3**0.5) * vbase * irated
        return {
            "branch_type": "line",
            "r_pu": r_pu,
            "x_pu": x_pu,
            "b_pu": b_pu,
            "rate_a_mva": rate,
            "parameter_source": "cloudpss_model_component",
            "parameter_component_id": component_id,
            "parameter_component_definition": getattr(component, "definition", ""),
            "parameter_base_mva": sbase,
            "parameter_base_kv": vbase,
            "static_name": first_present(args, "Name"),
        }

    def extract_transformer_parameters(
        self,
        component_id: str,
        component: Any,
        args: dict[str, Any],
    ) -> dict[str, Any]:
        rate = parse_float(first_present(args, "Tmva", "Smva", "rate_a_mva"), None)
        return {
            "branch_type": "transformer",
            "r_pu": parse_float(first_present(args, "Rl", "r_pu", "Rpu"), 0.0),
            "x_pu": parse_float(first_present(args, "Xl", "Xac", "x_pu", "Xpu"), None),
            "rate_a_mva": rate,
            "tap_ratio": parse_float(first_present(args, "InitTap", "Tap", "tap_ratio"), None),
            "parameter_source": "cloudpss_model_component",
            "parameter_component_id": component_id,
            "parameter_component_definition": getattr(component, "definition", ""),
            "parameter_base_mva": rate,
            "parameter_base_kv": parse_float(first_present(args, "V1", "Vbase", "VBase"), None),
            "static_name": first_present(args, "Name"),
        }


def cloudpss_arg_value(value: Any) -> Any:
    """Extract scalar payloads from CloudPSS expression wrappers."""
    if isinstance(value, dict):
        if "source" in value:
            return value.get("source")
        if "value" in value:
            return value.get("value")
    return value


def first_present(data: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in data and data[key] not in (None, ""):
            return data[key]
    return None


def parse_float(value: Any, default: float | None = 0.0) -> float | None:
    try:
        if value in (None, ""):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


__all__ = [
    "CloudPSSComponentRecord",
    "CloudPSSInventoryExtractor",
    "CloudPSSModelInventory",
    "cloudpss_arg_value",
    "first_present",
    "parse_float",
]
