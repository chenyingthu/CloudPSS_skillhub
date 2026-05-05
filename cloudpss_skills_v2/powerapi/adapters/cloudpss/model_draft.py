"""Generate CloudPSS static power-flow model drafts from unified models."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from cloudpss_skills_v2.core.system_model import (
    Branch,
    Bus,
    Generator,
    Load,
    PowerSystemModel,
)


BUS_DEFINITION = "model/CloudPSS/_newBus_3p"
LINE_DEFINITION = "model/CloudPSS/TransmissionLine"
TRANSFORMER_DEFINITION = "model/CloudPSS/_newTransformer_3p2w"
LOAD_DEFINITION = "model/CloudPSS/_newExpLoad_3p"
GENERATOR_DEFINITION = "model/CloudPSS/SyncGeneratorRouter"


@dataclass
class CloudPSSComponentDraft:
    """One CloudPSS component to be created."""

    component_id: str
    definition: str
    label: str
    args: dict[str, Any] = field(default_factory=dict)
    pins: dict[str, str] = field(default_factory=dict)
    position: dict[str, float] = field(default_factory=dict)
    source: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "component_id": self.component_id,
            "definition": self.definition,
            "label": self.label,
            "args": self.args,
            "pins": self.pins,
            "position": self.position,
            "source": self.source,
        }


@dataclass
class CloudPSSModelDraft:
    """Auditable CloudPSS component draft before SDK writes."""

    name: str = ""
    base_mva: float = 100.0
    frequency_hz: float = 50.0
    components: list[CloudPSSComponentDraft] = field(default_factory=list)
    bus_node_names: dict[int, str] = field(default_factory=dict)
    warnings: list[dict[str, str]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "base_mva": self.base_mva,
            "frequency_hz": self.frequency_hz,
            "bus_node_names": self.bus_node_names,
            "component_count": len(self.components),
            "components": [component.to_dict() for component in self.components],
            "warnings": self.warnings,
        }

    def component_type_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for component in self.components:
            counts[component.definition] = counts.get(component.definition, 0) + 1
        return counts


class UnifiedToCloudPSSDraftConverter:
    """Convert the static PowerSystemModel subset into CloudPSS components."""

    def convert(self, model: PowerSystemModel) -> CloudPSSModelDraft:
        draft = CloudPSSModelDraft(
            name=model.name or "PowerSystemModel",
            base_mva=float(model.base_mva),
            frequency_hz=float(model.frequency_hz),
        )
        bus_by_id = {bus.bus_id: bus for bus in model.buses}
        draft.bus_node_names = {
            bus.bus_id: self._node_name(bus)
            for bus in model.buses
        }

        for index, bus in enumerate(model.buses):
            draft.components.append(
                self._bus_component(
                    bus,
                    draft.bus_node_names[bus.bus_id],
                    index,
                    draft.frequency_hz,
                )
            )

        for index, branch in enumerate(model.branches):
            if not branch.in_service:
                draft.warnings.append(self._warning("skipped_inactive_branch", branch.name))
                continue
            draft.components.append(
                self._branch_component(
                    branch,
                    bus_by_id,
                    draft.bus_node_names,
                    index,
                    draft.base_mva,
                )
            )

        for index, load in enumerate(model.loads):
            if not load.in_service:
                draft.warnings.append(self._warning("skipped_inactive_load", load.name))
                continue
            draft.components.append(
                self._load_component(
                    load,
                    bus_by_id,
                    draft.bus_node_names,
                    index,
                    draft.frequency_hz,
                )
            )

        for index, generator in enumerate(model.generators):
            if not generator.in_service:
                draft.warnings.append(self._warning("skipped_inactive_generator", generator.name))
                continue
            draft.components.append(
                self._generator_component(
                    generator,
                    bus_by_id,
                    draft.bus_node_names,
                    index,
                    draft.frequency_hz,
                )
            )

        if model.transformers:
            draft.warnings.append({
                "severity": "info",
                "code": "detailed_transformers_not_emitted",
                "message": "PowerSystemModel.transformers is not emitted separately; branch transformers are used for CloudPSS generation",
            })

        return draft

    def _bus_component(
        self,
        bus: Bus,
        node_name: str,
        index: int,
        frequency_hz: float,
    ) -> CloudPSSComponentDraft:
        return CloudPSSComponentDraft(
            component_id=f"bus_{bus.bus_id}_{self._slug(bus.name)}",
            definition=BUS_DEFINITION,
            label=bus.name,
            args={
                "Name": bus.name,
                "VBase": self._expr(bus.base_kv),
                "Freq": str(frequency_hz),
                "V": str(bus.v_magnitude_pu if bus.v_magnitude_pu is not None else 1.0),
                "Theta": str(bus.v_angle_degree if bus.v_angle_degree is not None else 0.0),
            },
            pins={"0": node_name},
            position=self._position(index, row=0),
            source={"kind": "bus", "bus_id": bus.bus_id},
        )

    def _branch_component(
        self,
        branch: Branch,
        bus_by_id: dict[int, Bus],
        node_names: dict[int, str],
        index: int,
        base_mva: float,
    ) -> CloudPSSComponentDraft:
        if branch.branch_type in ("TRANSFORMER", "PHASE_SHIFTER"):
            return self._transformer_component(branch, bus_by_id, node_names, index)
        return self._line_component(branch, bus_by_id, node_names, index, base_mva)

    def _line_component(
        self,
        branch: Branch,
        bus_by_id: dict[int, Bus],
        node_names: dict[int, str],
        index: int,
        base_mva: float,
    ) -> CloudPSSComponentDraft:
        from_bus = bus_by_id[branch.from_bus]
        return CloudPSSComponentDraft(
            component_id=f"line_{index}_{self._slug(branch.name)}",
            definition=LINE_DEFINITION,
            label=branch.name,
            args={
                "Name": branch.name,
                "R1pu": self._expr(branch.r_pu),
                "X1pu": self._expr(branch.x_pu),
                "B1pu": self._expr(branch.b_pu),
                "Sbase": self._expr(base_mva),
                "Vbase": self._expr(from_bus.base_kv),
                "Rate": self._expr(branch.rate_a_mva),
            },
            pins={
                "0": node_names[branch.from_bus],
                "1": node_names[branch.to_bus],
            },
            position=self._position(index, row=1),
            source={"kind": "branch", "branch_type": branch.branch_type},
        )

    def _transformer_component(
        self,
        branch: Branch,
        bus_by_id: dict[int, Bus],
        node_names: dict[int, str],
        index: int,
    ) -> CloudPSSComponentDraft:
        from_bus = bus_by_id[branch.from_bus]
        return CloudPSSComponentDraft(
            component_id=f"transformer_{index}_{self._slug(branch.name)}",
            definition=TRANSFORMER_DEFINITION,
            label=branch.name,
            args={
                "Name": branch.name,
                "Rl": self._expr(branch.r_pu),
                "Xl": self._expr(branch.x_pu),
                "Tmva": self._expr(branch.rate_a_mva),
                "V1": self._expr(from_bus.base_kv),
                "InitTap": self._expr(branch.tap_ratio),
            },
            pins={
                "0": node_names[branch.from_bus],
                "1": node_names[branch.to_bus],
            },
            position=self._position(index, row=2),
            source={
                "kind": "branch",
                "branch_type": branch.branch_type,
                "phase_shift_degree": branch.phase_shift_degree,
            },
        )

    def _load_component(
        self,
        load: Load,
        bus_by_id: dict[int, Bus],
        node_names: dict[int, str],
        index: int,
        frequency_hz: float,
    ) -> CloudPSSComponentDraft:
        bus = bus_by_id[load.bus_id]
        return CloudPSSComponentDraft(
            component_id=f"load_{index}_{self._slug(load.name)}",
            definition=LOAD_DEFINITION,
            label=load.name,
            args={
                "Name": load.name,
                "p": self._expr(load.p_mw),
                "q": self._expr(load.q_mvar),
                "f": self._expr(frequency_hz),
                "v": self._expr(bus.base_kv),
                "Vi": self._expr(1.0),
                "NP": self._expr(2),
                "NQ": self._expr(2),
                "KPF": self._expr(0),
                "KQF": self._expr(0),
                "NIM": "1",
            },
            pins={"0": node_names[load.bus_id]},
            position=self._position(index, row=3),
            source={"kind": "load", "bus_id": load.bus_id},
        )

    def _generator_component(
        self,
        generator: Generator,
        bus_by_id: dict[int, Bus],
        node_names: dict[int, str],
        index: int,
        frequency_hz: float,
    ) -> CloudPSSComponentDraft:
        bus = bus_by_id[generator.bus_id]
        bus_type = "2" if bus.bus_type == "SLACK" else "1"
        args = {
            "Name": generator.name,
            "pf_P": self._expr(generator.p_gen_mw),
            "pf_Q": self._expr(generator.q_gen_mvar or 0.0),
            "pf_Qmax": self._expr(generator.q_max_mvar),
            "pf_Qmin": self._expr(generator.q_min_mvar),
            "pf_V": self._expr(generator.v_set_pu if generator.v_set_pu is not None else 1.0),
            "pf_Theta": self._expr(0.0),
            "BusType": bus_type,
            "Control": "1",
            "ModelType": "1",
            "NIM": "1",
            "freq": self._expr(frequency_hz),
            "V": self._expr(f"{bus.base_kv}*sqrt(1/3)"),
        }
        return CloudPSSComponentDraft(
            component_id=f"generator_{index}_{self._slug(generator.name)}",
            definition=GENERATOR_DEFINITION,
            label=generator.name,
            args=args,
            pins={"0": node_names[generator.bus_id]},
            position=self._position(index, row=4),
            source={"kind": "generator", "bus_id": generator.bus_id},
        )

    @staticmethod
    def _expr(value: Any) -> dict[str, str]:
        return {"source": str(value), "ɵexp": ""}

    @staticmethod
    def _slug(value: Any) -> str:
        text = re.sub(r"[^a-zA-Z0-9]+", "_", str(value)).strip("_").lower()
        return text or "component"

    @staticmethod
    def _node_name(bus: Bus) -> str:
        return f"node_{bus.bus_id}_{UnifiedToCloudPSSDraftConverter._slug(bus.name)}"

    @staticmethod
    def _position(index: int, *, row: int) -> dict[str, float]:
        return {"x": float(160 + index * 180), "y": float(120 + row * 120)}

    @staticmethod
    def _warning(code: str, name: str) -> dict[str, str]:
        return {
            "severity": "warning",
            "code": code,
            "message": f"Skipped inactive component: {name}",
        }


class CloudPSSModelWriter:
    """Write a CloudPSSModelDraft into a CloudPSS SDK model object."""

    def write(
        self,
        model: Any,
        draft: CloudPSSModelDraft,
        *,
        clear_existing: bool = False,
    ) -> list[dict[str, Any]]:
        if not hasattr(model, "addComponent"):
            raise TypeError("CloudPSS model object must provide addComponent()")

        if clear_existing:
            self.clear_components(model)

        created: list[dict[str, Any]] = []
        for component in draft.components:
            result = model.addComponent(
                definition=component.definition,
                label=component.label,
                args=component.args,
                pins=component.pins,
                position=component.position or None,
            )
            created.append({
                "component_id": component.component_id,
                "definition": component.definition,
                "label": component.label,
                "sdk_component_key": self._component_key(result),
                "sdk_result": result,
            })
        return created

    @staticmethod
    def clear_components(model: Any) -> int:
        if not hasattr(model, "getAllComponents") or not hasattr(model, "removeComponent"):
            raise TypeError(
                "CloudPSS model object must provide getAllComponents() and removeComponent()"
            )
        component_keys = list(model.getAllComponents().keys())
        removed = 0
        for component_key in component_keys:
            if model.removeComponent(component_key):
                removed += 1
        return removed

    @staticmethod
    def _component_key(result: Any) -> str | None:
        if isinstance(result, str):
            return result
        key = getattr(result, "id", None) or getattr(result, "key", None)
        return str(key) if key else None


__all__ = [
    "BUS_DEFINITION",
    "GENERATOR_DEFINITION",
    "LINE_DEFINITION",
    "LOAD_DEFINITION",
    "TRANSFORMER_DEFINITION",
    "CloudPSSComponentDraft",
    "CloudPSSModelDraft",
    "CloudPSSModelWriter",
    "UnifiedToCloudPSSDraftConverter",
]
