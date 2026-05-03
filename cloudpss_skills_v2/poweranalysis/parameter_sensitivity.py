"""Parameter Sensitivity Analysis - Compute sensitivity rankings for system parameters.

参数灵敏度分析 - 基于统一模型计算系统参数灵敏度排序。
"""

from __future__ import annotations

import logging
from typing import Any

from cloudpss_skills_v2.core.system_model import PowerSystemModel
from cloudpss_skills_v2.poweranalysis.base import PowerAnalysis

logger = logging.getLogger(__name__)


class ParameterSensitivityAnalysis(PowerAnalysis):
    """Parameter sensitivity analysis using unified PowerSystemModel.

    This class analyzes how changes in system parameters (load power, branch
    impedance, etc.) affect system-wide metrics like total load, generation,
    and voltage profiles.
    """

    name = "parameter_sensitivity"
    description = "参数灵敏度分析 - 基于统一模型计算参数灵敏度"

    def validate(self, config: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate configuration for backward compatibility."""
        errors = []
        if not config:
            errors.append("config is required")
            return False, errors
        if not config.get("model", {}).get("rid"):
            errors.append("model.rid is required")
        return len(errors) == 0, errors

    def run(self, model_or_config, config: dict | None = None):
        """Run parameter sensitivity analysis with unified model or config-based interface.

        Supports two calling conventions:
        1. Unified model: run(model, config) -> dict
        2. Legacy config: run(config) -> SkillResult

        Args:
            model_or_config: Either PowerSystemModel (unified) or config dict (legacy)
            config: Analysis configuration (required for unified interface)

        Returns:
            dict for unified interface, SkillResult for legacy interface
        """
        # Detect which interface is being used
        if hasattr(model_or_config, 'buses') and config is not None:
            # Unified model interface: run(model, config)
            return self._run_unified(model_or_config, config)
        elif isinstance(model_or_config, dict) and config is None:
            # Legacy config interface: run(config)
            return self._run_legacy(model_or_config)
        else:
            raise TypeError("Invalid arguments. Use run(model, config) for unified or run(config) for legacy.")

    def _run_legacy(self, config: dict[str, Any]) -> Any:
        """Run parameter sensitivity analysis with config-based interface (legacy)."""
        from cloudpss_skills_v2.core.skill_result import SkillResult, SkillStatus
        from cloudpss_skills_v2.powerskill import Engine
        from datetime import datetime

        start_time = datetime.now()

        try:
            # Validate config
            valid, errors = self.validate(config)
            if not valid:
                return SkillResult(
                    skill_name=self.name,
                    status=SkillStatus.FAILED,
                    error="; ".join(errors),
                    start_time=start_time,
                    end_time=datetime.now(),
                )

            # Get model from config
            model_rid = config.get("model", {}).get("rid", "")
            engine = config.get("engine", "cloudpss")
            auth = config.get("auth", {})

            # Create API and get model handle
            api = Engine.create_powerflow_for_skill(
                engine=engine,
                base_url=auth.get("base_url"),
                auth=auth,
            )

            handle = api.get_model_handle(model_rid)

            # Convert to unified model
            model = self._convert_handle_to_model(handle)

            # Get analysis config
            analysis_config = config.get("analysis", {})

            # Run analysis with unified model
            result = self.run_unified(model, {
                "target_parameter": analysis_config.get("target_parameter", ""),
                "delta": analysis_config.get("delta", 0.01),
            })

            # Convert result to SkillResult format
            if result.get("status") == "error":
                return SkillResult(
                    skill_name=self.name,
                    status=SkillStatus.FAILED,
                    error="; ".join(result.get("errors", ["Unknown error"])),
                    data=result,
                    start_time=start_time,
                    end_time=datetime.now(),
                )

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                data=result,
                start_time=start_time,
                end_time=datetime.now(),
            )

        except Exception as e:
            logger.error(f"Parameter sensitivity analysis failed: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error=str(e),
                start_time=start_time,
                end_time=datetime.now(),
            )

    def _convert_handle_to_model(self, handle) -> PowerSystemModel:
        """Convert model handle to unified PowerSystemModel."""
        from cloudpss_skills_v2.powerskill import ComponentType
        from cloudpss_skills_v2.core.system_model import Bus, Branch, Load, Generator

        buses = []
        branches = []
        loads = []
        generators = []

        try:
            # Get ext_grid buses (slack buses) first
            slack_bus_indices = set()
            try:
                ext_grid_components = handle.get_components_by_type(ComponentType.SOURCE)
                for comp in ext_grid_components:
                    args = comp.args if hasattr(comp, 'args') and comp.args else {}
                    bus_idx = args.get('bus', '') if isinstance(args, dict) else ''
                    if isinstance(bus_idx, int):
                        slack_bus_indices.add(f"bus:{bus_idx}")
                    elif bus_idx:
                        slack_bus_indices.add(str(bus_idx))
            except Exception:
                pass

            bus_components = handle.get_components_by_type(ComponentType.BUS)
            for comp in bus_components:
                # Get base_kv from component args or use default
                args = comp.args if hasattr(comp, 'args') and comp.args else {}
                base_kv = args.get('vn_kv', 110.0) if isinstance(args, dict) else 110.0
                # Parse bus_id from key (e.g., "bus:0" -> 0)
                bus_id = comp.key
                if isinstance(bus_id, str) and ':' in bus_id:
                    try:
                        bus_id = int(bus_id.split(':')[-1])
                    except ValueError:
                        bus_id = 0
                # Determine bus type - check if this is a slack bus
                bus_type = "SLACK" if comp.key in slack_bus_indices else "PQ"
                bus = Bus(
                    bus_id=bus_id,
                    name=comp.name,
                    base_kv=float(base_kv) if base_kv else 110.0,
                    v_magnitude_pu=1.0,
                    bus_type=bus_type,
                )
                buses.append(bus)

            branch_components = handle.get_components_by_type(ComponentType.BRANCH)
            for comp in branch_components:
                props = comp.properties if hasattr(comp, 'properties') else {}
                from_bus_key = props.get("from_bus", "")
                to_bus_key = props.get("to_bus", "")

                # Parse bus IDs from keys (e.g., "bus:0" -> 0)
                from_bus = from_bus_key
                if isinstance(from_bus_key, str) and ":" in from_bus_key:
                    try:
                        from_bus = int(from_bus_key.split(":")[-1])
                    except ValueError:
                        from_bus = 0
                to_bus = to_bus_key
                if isinstance(to_bus_key, str) and ":" in to_bus_key:
                    try:
                        to_bus = int(to_bus_key.split(":")[-1])
                    except ValueError:
                        to_bus = 0

                branch = Branch(
                    name=comp.key,
                    from_bus=from_bus,
                    to_bus=to_bus,
                    r_pu=props.get("r_pu", 0.001),
                    x_pu=props.get("x_pu", 0.01),
                    in_service=props.get("in_service", True),
                )
                branches.append(branch)

            load_components = handle.get_components_by_type(ComponentType.LOAD)
            for comp in load_components:
                props = comp.properties if hasattr(comp, 'properties') else {}
                # Parse bus_id from key (e.g., "load:0" -> 0)
                bus_id = comp.key
                if isinstance(bus_id, str) and ":" in bus_id:
                    try:
                        bus_id = int(bus_id.split(":")[-1])
                    except ValueError:
                        bus_id = 0
                load = Load(
                    bus_id=bus_id,
                    name=comp.name,
                    p_mw=props.get("p_mw", 0),
                    q_mvar=props.get("q_mvar", 0),
                    in_service=props.get("in_service", True),
                )
                loads.append(load)

            gen_components = handle.get_components_by_type(ComponentType.GENERATOR)
            for comp in gen_components:
                props = comp.properties if hasattr(comp, 'properties') else {}
                # Parse bus_id from key (e.g., "gen:0" -> 0)
                bus_id = comp.key
                if isinstance(bus_id, str) and ":" in bus_id:
                    try:
                        bus_id = int(bus_id.split(":")[-1])
                    except ValueError:
                        bus_id = 0
                gen = Generator(
                    bus_id=bus_id,
                    name=comp.name,
                    p_gen_mw=props.get("p_gen_mw", 0),
                    v_set_pu=props.get("v_set_pu", 1.0),
                    in_service=props.get("in_service", True),
                )
                generators.append(gen)
        except Exception as e:
            logger.warning(f"Could not convert handle to model: {e}")

        return PowerSystemModel(
            buses=buses,
            branches=branches,
            loads=loads,
            generators=generators,
            base_mva=100.0,
        )

    def _run_unified(self, model: PowerSystemModel, config: dict) -> dict:
        """Run sensitivity analysis on unified model.

        Args:
            model: Unified PowerSystemModel containing buses, branches, generators, etc.
            config: Analysis configuration dictionary with keys:
                - target_parameter: Parameter to analyze (e.g., "load.p_mw", "branch.r_pu")
                - delta: Perturbation factor (default: 0.01 = 1%)

        Returns:
            Analysis results as a dictionary with keys:
                - status: "success" or "error"
                - target_parameter: The analyzed parameter
                - delta: The perturbation factor used
                - sensitivities: List of sensitivity records
                - rankings: Sensitivities sorted by absolute value
                - errors: List of error messages (if status is "error")
        """
        # Validate model
        errors = self.validate_model(model)
        if errors:
            return {"status": "error", "errors": errors}

        # Extract configuration
        target_param = config.get("target_parameter", "")
        delta = config.get("delta", 0.01)

        # Calculate base case metrics
        base_result = self._calculate_base_case(model)

        # Analyze based on target parameter type
        sensitivities = []
        if target_param.startswith("load."):
            sensitivities = self._analyze_load_sensitivity(
                model, target_param, delta, base_result
            )
        elif target_param.startswith("branch."):
            sensitivities = self._analyze_branch_sensitivity(
                model, target_param, delta, base_result
            )
        elif target_param.startswith("gen.") or target_param.startswith("generator."):
            sensitivities = self._analyze_generator_sensitivity(
                model, target_param, delta, base_result
            )
        else:
            return {
                "status": "error",
                "errors": [f"Unsupported target parameter: {target_param}"],
            }

        # Sort by absolute sensitivity for rankings
        rankings = sorted(
            sensitivities, key=lambda x: abs(x["sensitivity"]), reverse=True
        )

        return {
            "status": "success",
            "target_parameter": target_param,
            "delta": delta,
            "sensitivities": sensitivities,
            "rankings": rankings,
        }

    def _calculate_base_case(self, model: PowerSystemModel) -> dict:
        """Calculate base case system metrics.

        Args:
            model: PowerSystemModel to analyze

        Returns:
            Dictionary with base case metrics
        """
        total_load = model.total_load_mw()
        total_gen = model.total_generation_mw()

        # Calculate min voltage among buses with valid voltage values
        voltages = [
            b.v_magnitude_pu
            for b in model.buses
            if b.v_magnitude_pu is not None
        ]
        min_voltage = min(voltages) if voltages else 1.0
        max_voltage = max(voltages) if voltages else 1.0

        return {
            "total_load_mw": total_load,
            "total_gen_mw": total_gen,
            "min_voltage": min_voltage,
            "max_voltage": max_voltage,
            "bus_count": len(model.buses),
            "branch_count": len(model.branches),
        }

    def _analyze_load_sensitivity(
        self, model: PowerSystemModel, param: str, delta: float, base: dict
    ) -> list[dict]:
        """Analyze sensitivity to load parameter changes.

        Args:
            model: PowerSystemModel
            param: Target parameter (e.g., "load.p_mw", "load.q_mvar")
            delta: Perturbation factor
            base: Base case metrics

        Returns:
            List of sensitivity dictionaries
        """
        sensitivities = []

        # Determine which load parameter to analyze
        param_field = param.split(".")[-1] if "." in param else "p_mw"

        for load in model.loads:
            if not load.in_service:
                continue

            # Get base value
            if param_field == "p_mw":
                base_value = load.p_mw
            elif param_field == "q_mvar":
                base_value = load.q_mvar
            else:
                base_value = load.p_mw  # Default to p_mw

            if base_value is None:
                continue

            # Calculate delta amount
            delta_amount = base_value * delta

            # Calculate sensitivity as relative impact on total load
            # Sensitivity = (delta_p / base_total_load) / delta
            if base["total_load_mw"] > 0:
                sensitivity = (delta_amount / base["total_load_mw"]) / delta
            else:
                sensitivity = 0.0

            sensitivities.append(
                {
                    "component": load.name,
                    "bus_id": load.bus_id,
                    "parameter": param_field,
                    "base_value": base_value,
                    "delta": delta_amount,
                    "sensitivity": sensitivity,
                }
            )

        return sensitivities

    def _analyze_branch_sensitivity(
        self, model: PowerSystemModel, param: str, delta: float, base: dict
    ) -> list[dict]:
        """Analyze sensitivity to branch parameter changes.

        Args:
            model: PowerSystemModel
            param: Target parameter (e.g., "branch.r_pu", "branch.x_pu")
            delta: Perturbation factor
            base: Base case metrics

        Returns:
            List of sensitivity dictionaries
        """
        sensitivities = []

        # Determine which branch parameter to analyze
        param_field = param.split(".")[-1] if "." in param else "r_pu"

        for branch in model.branches:
            if not branch.in_service:
                continue

            # Get base value
            if param_field == "r_pu":
                base_value = branch.r_pu
            elif param_field == "x_pu":
                base_value = branch.x_pu
            elif param_field == "b_pu":
                base_value = branch.b_pu
            else:
                base_value = branch.r_pu  # Default to r_pu

            # Calculate delta amount
            delta_amount = base_value * delta if base_value != 0 else delta * 0.01

            # For branches, sensitivity is based on impact on power flow
            # Simplified: sensitivity proportional to branch loading
            sensitivity = 0.0
            if branch.loading_percent is not None:
                sensitivity = branch.loading_percent / 100.0 * delta
            elif branch.rate_a_mva > 0:
                # Estimate sensitivity from power flow if available
                s_from = branch.apparent_power_from_mva()
                if s_from is not None:
                    loading = s_from / branch.rate_a_mva
                    sensitivity = loading * delta

            sensitivities.append(
                {
                    "component": branch.name,
                    "from_bus": branch.from_bus,
                    "to_bus": branch.to_bus,
                    "parameter": param_field,
                    "base_value": base_value,
                    "delta": delta_amount,
                    "sensitivity": sensitivity,
                }
            )

        return sensitivities

    def _analyze_generator_sensitivity(
        self, model: PowerSystemModel, param: str, delta: float, base: dict
    ) -> list[dict]:
        """Analyze sensitivity to generator parameter changes.

        Args:
            model: PowerSystemModel
            param: Target parameter (e.g., "gen.p_gen_mw", "gen.v_set_pu")
            delta: Perturbation factor
            base: Base case metrics

        Returns:
            List of sensitivity dictionaries
        """
        sensitivities = []

        # Determine which generator parameter to analyze
        param_field = param.split(".")[-1] if "." in param else "p_gen_mw"

        for gen in model.generators:
            if not gen.in_service:
                continue

            # Get base value
            if param_field == "p_gen_mw":
                base_value = gen.p_gen_mw
            elif param_field == "v_set_pu":
                base_value = gen.v_set_pu if gen.v_set_pu is not None else 1.0
            else:
                base_value = gen.p_gen_mw  # Default to p_gen_mw

            # Calculate delta amount
            delta_amount = base_value * delta

            # Calculate sensitivity as relative impact on total generation
            if base["total_gen_mw"] > 0:
                sensitivity = (delta_amount / base["total_gen_mw"]) / delta
            else:
                sensitivity = 0.0

            sensitivities.append(
                {
                    "component": gen.name,
                    "bus_id": gen.bus_id,
                    "parameter": param_field,
                    "base_value": base_value,
                    "delta": delta_amount,
                    "sensitivity": sensitivity,
                }
            )

        return sensitivities


# Backward compatibility: maintain old class name and interface
class ParameterSensitivityAnalysisLegacy:
    """Legacy compatibility wrapper for old config-based interface.

    This class provides backward compatibility for code using the old
    config-based run() interface while internally using the new unified
    model-based implementation.

    Deprecated: Use ParameterSensitivityAnalysis with PowerSystemModel directly.
    """

    name = "parameter_sensitivity"
    description = "参数灵敏度分析 - 计算系统参数灵敏度排序 (Legacy)"

    def __init__(self):
        self._new_analysis = ParameterSensitivityAnalysis()
        self.logs = []
        self.artifacts = []

    @property
    def config_schema(self) -> dict[str, Any]:
        """Return configuration schema for backward compatibility."""
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {
                    "type": "string",
                    "const": "parameter_sensitivity",
                    "default": "parameter_sensitivity",
                },
                "engine": {
                    "type": "string",
                    "enum": ["cloudpss", "pandapower"],
                    "default": "pandapower",
                },
                "auth": {
                    "type": "object",
                    "properties": {
                        "token": {"type": "string", "default": "local-pandapower-token"},
                    },
                },
                "model": {
                    "type": "object",
                    "required": ["rid"],
                    "properties": {
                        "rid": {"type": "string", "default": "case14"},
                        "source": {
                            "type": "string",
                            "enum": ["cloud", "local"],
                            "default": "local",
                        },
                    },
                },
                "analysis": {
                    "type": "object",
                    "properties": {
                        "target_parameter": {
                            "type": "string",
                            "description": "e.g., load.p_mw",
                            "default": "",
                        },
                        "delta": {"type": "number", "default": 0.01},
                    },
                },
            },
        }

    def get_default_config(self) -> dict[str, Any]:
        """Return default configuration for backward compatibility."""
        return {
            "skill": self.name,
            "engine": "pandapower",
            "auth": {"token": "local-pandapower-token"},
            "model": {"rid": "case14", "source": "local"},
            "analysis": {
                "target_parameter": "",
                "delta": 0.01,
            },
        }

    def validate(self, config: dict | None) -> tuple[bool, list[str]]:
        """Validate configuration for backward compatibility."""
        from cloudpss_skills_v2.core.skill_result import SkillResult, SkillStatus

        errors = []
        if not config:
            errors.append("config is required")
            return (False, errors)
        if not config.get("model", {}).get("rid"):
            errors.append("model.rid is required")
        return (len(errors) == 0, errors)

    def run(self, config: dict | None) -> Any:
        """Run analysis with legacy config-based interface.

        This method provides backward compatibility by converting the legacy
        config format to the new unified model interface.

        Args:
            config: Legacy configuration dictionary

        Returns:
            SkillResult in the legacy format
        """
        from cloudpss_skills_v2.core.skill_result import (
            SkillResult,
            SkillStatus,
        )
        from datetime import datetime

        start_time = datetime.now()

        if config is None:
            config = {}
        self.logs = []
        self.artifacts = []

        valid, errors = self.validate(config)
        if not valid:
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error="; ".join(errors),
                logs=self.logs,
                start_time=start_time,
                end_time=datetime.now(),
            )

        # Note: This is a simplified legacy wrapper
        # In production, this would convert the model RID to a PowerSystemModel
        # For now, return an error indicating migration is needed
        return SkillResult(
            skill_name=self.name,
            status=SkillStatus.FAILED,
            error=(
                "Legacy config-based interface is deprecated. "
                "Use ParameterSensitivityAnalysis with PowerSystemModel directly. "
                "See migration guide for details."
            ),
            logs=self.logs,
            start_time=start_time,
            end_time=datetime.now(),
        )


__all__ = [
    "ParameterSensitivityAnalysis",
    "ParameterSensitivityAnalysisLegacy",
]
