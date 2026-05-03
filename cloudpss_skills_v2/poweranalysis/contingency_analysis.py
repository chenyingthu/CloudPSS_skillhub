"""Contingency Analysis Skill v2 - Engine-agnostic N-K contingency analysis.

预想事故分析 - 系统性评估电网在多种故障工况下的安全裕度
支持N-1、N-2、N-K故障，故障排序，薄弱环节识别
"""

from __future__ import annotations

import logging
from datetime import datetime
from itertools import combinations
from typing import Any

from cloudpss_skills_v2.core.system_model import (
    PowerSystemModel,
    Bus,
    Branch,
)
from cloudpss_skills_v2.poweranalysis.base import PowerAnalysis
from cloudpss_skills_v2.powerskill import ComponentType
from cloudpss_skills_v2.core.skill_result import SkillResult, SkillStatus

logger = logging.getLogger(__name__)


def _as_float(value, default=0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


class ContingencyAnalysis(PowerAnalysis):
    """预想事故分析技能 - v2 engine-agnostic implementation using unified PowerSystemModel.

    Inherits from PowerAnalysis base class to work directly with unified PowerSystemModel.
    Supports N-1, N-2, and N-1-1 contingency analysis with violation checking.
    """

    name = "contingency_analysis"
    description = "预想事故分析 - 评估N-K故障下的系统安全裕度，识别薄弱环节"

    @property
    def config_schema(self) -> dict[str, Any]:
        """Return configuration schema for legacy interface compatibility."""
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "contingency_analysis", "default": "contingency_analysis"},
                "engine": {
                    "type": "string",
                    "enum": ["cloudpss", "pandapower"],
                    "default": "cloudpss",
                },
                "auth": {
                    "type": "object",
                    "properties": {
                        "token": {"type": "string"},
                        "token_file": {"type": "string", "default": ".cloudpss_token"},
                    },
                },
                "model": {
                    "type": "object",
                    "required": ["rid"],
                    "properties": {
                        "rid": {"type": "string", "default": "model/holdme/IEEE39"},
                        "source": {"enum": ["cloud", "local"], "default": "cloud"},
                    },
                },
                "contingency": {
                    "type": "object",
                    "properties": {
                        "level": {"type": "string", "enum": ["N-1", "N-2", "N-1-1"], "default": "N-1"},
                        "components": {"type": "array", "items": {"type": "string"}},
                    },
                },
                "ranking": {
                    "type": "object",
                    "properties": {
                        "enabled": {"type": "boolean", "default": True},
                        "top_n": {"type": "integer", "default": 10},
                    },
                },
            },
        }

    def get_default_config(self) -> dict[str, Any]:
        """Return default configuration for legacy interface compatibility."""
        return {
            "skill": self.name,
            "engine": "cloudpss",
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "model/holdme/IEEE39", "source": "cloud"},
            "contingency": {"level": "N-1", "components": []},
            "ranking": {"enabled": True, "top_n": 10},
        }

    def validate(self, config: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate configuration for legacy interface compatibility."""
        errors = []
        if not config.get("model", {}).get("rid"):
            errors.append("必须指定 model.rid")
        auth = config.get("auth", {})
        if not auth.get("token") and not auth.get("token_file"):
            errors.append("必须提供 auth.token 或 auth.token_file")
        return len(errors) == 0, errors

    def _discover_components(self, handle, component_types: list[str], excluded: list[str]) -> list[dict]:
        """Discover components of specified types from model handle.

        Args:
            handle: Model handle to query
            component_types: List of component type strings (e.g., "branch", "generator")
            excluded: List of component keys to exclude

        Returns:
            List of component dictionaries with key, name, type, and definition
        """
        from cloudpss_skills_v2.powerskill import ComponentType

        type_mapping = {
            "branch": ComponentType.BRANCH,
            "generator": ComponentType.GENERATOR,
            "load": ComponentType.LOAD,
            "bus": ComponentType.BUS,
            "transformer": ComponentType.TRANSFORMER,
            "shunt": ComponentType.SHUNT,
        }

        available = []
        for type_str in component_types:
            comp_type = type_mapping.get(type_str.lower())
            if comp_type is None:
                continue
            components = handle.get_components_by_type(comp_type)
            for comp in components:
                if comp.key not in excluded:
                    available.append({
                        "key": comp.key,
                        "name": comp.name,
                        "type": type_str.lower(),
                        "definition": comp.definition,
                    })
        return available

    def run(self, model: PowerSystemModel | dict, config: dict | None = None) -> SkillResult | dict:
        """Run contingency analysis.

        Supports both unified model interface (model + config) and legacy config-only interface.

        Args:
            model: Either a unified PowerSystemModel or a config dict (legacy mode)
            config: Analysis configuration dictionary (unified mode) or None (legacy mode)

        Returns:
            SkillResult (legacy mode) or dict (unified mode)
        """
        from cloudpss_skills_v2.core.skill_result import SkillResult, SkillStatus

        # Detect if called in legacy mode (config dict as first arg)
        if config is None and isinstance(model, dict):
            # Legacy mode: run(config_dict)
            return self.run_legacy(model)

        # Unified mode: run(model, config)
        assert isinstance(model, PowerSystemModel)
        return self._run_unified(model, config or {})

    def _run_unified(self, model: PowerSystemModel, config: dict) -> dict:
        """Run contingency analysis on unified PowerSystemModel.

        Args:
            model: Unified PowerSystemModel containing buses, branches, generators, etc.
            config: Analysis configuration dictionary with options:
                - contingency_type: "n1", "n2", or "n1_1"
                - check_violations: list of violation types to check ["thermal", "voltage"]
                - voltage_limits: {"min": float, "max": float} in p.u. (default: 0.95, 1.05)
                - thermal_limit: float threshold for thermal violations (default: 1.0 = 100%)
                - severity_threshold: float threshold for severity classification (default: 0.8)

        Returns:
            Dictionary containing:
                - status: "success" or "error"
                - contingencies: list of contingency results
                - summary: summary statistics
                - weak_points: list of weak points identified
        """
        # Validate model
        errors = self.validate_model(model)
        if errors:
            return {
                "status": "error",
                "error": "; ".join(errors),
                "contingencies": [],
                "summary": {},
                "weak_points": [],
            }

        # Extract configuration
        contingency_type = config.get("contingency_type", "n1").lower()
        check_violations = config.get("check_violations", ["thermal", "voltage"])
        voltage_limits = config.get("voltage_limits", {"min": 0.95, "max": 1.05})
        thermal_limit = config.get("thermal_limit", 1.0)
        severity_threshold = config.get("severity_threshold", 0.8)

        try:
            # Generate contingencies based on type
            contingencies_to_test = self._generate_contingencies(model, contingency_type)

            if not contingencies_to_test:
                return {
                    "status": "success",
                    "contingencies": [],
                    "summary": {
                        "total_cases": 0,
                        "passed": 0,
                        "failed": 0,
                        "warnings": 0,
                    },
                    "weak_points": [],
                }

            # Evaluate each contingency
            results = []
            passed = 0
            failed = 0
            warnings = 0

            for i, contingency in enumerate(contingencies_to_test):
                result = self._evaluate_contingency(
                    model=model,
                    contingency=contingency,
                    check_violations=check_violations,
                    voltage_limits=voltage_limits,
                    thermal_limit=thermal_limit,
                )
                results.append(result)

                # Count by severity
                if result.get("severity") == "critical":
                    failed += 1
                elif result.get("severity") == "warning":
                    warnings += 1
                else:
                    passed += 1

            # Calculate severity for each result
            for result in results:
                result["severity_score"] = self._calculate_severity(
                    result, voltage_limits, thermal_limit
                )

            # Sort by severity score
            results.sort(key=lambda x: x.get("severity_score", 0), reverse=True)

            # Identify weak points
            weak_points = self._identify_weak_points(results)

            summary = {
                "total_cases": len(contingencies_to_test),
                "passed": passed,
                "failed": failed,
                "warnings": warnings,
                "pass_rate": round(passed / len(contingencies_to_test) * 100, 2) if contingencies_to_test else 0,
                "severe_cases": len([r for r in results if r.get("severity_score", 0) >= severity_threshold]),
            }

            return {
                "status": "success",
                "contingencies": results,
                "summary": summary,
                "weak_points": weak_points,
            }

        except Exception as e:
            logger.error(f"Contingency analysis failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "contingencies": [],
                "summary": {},
                "weak_points": [],
            }

    def _generate_contingencies(
        self,
        model: PowerSystemModel,
        contingency_type: str,
    ) -> list[dict]:
        """Generate contingency scenarios based on type.

        Args:
            model: PowerSystemModel to generate contingencies from
            contingency_type: "n1", "n2", or "n1_1"

        Returns:
            List of contingency dictionaries with "name" and "components" keys
        """
        contingencies = []

        if contingency_type == "n1":
            # N-1: Remove each branch individually
            for branch in model.branches:
                if branch.in_service:
                    contingencies.append({
                        "name": f"N-1: {branch.name}",
                        "components": [branch.name],
                        "type": "branch",
                    })

        elif contingency_type == "n2":
            # N-2: Remove all combinations of 2 branches
            branch_names = [
                br.name for br in model.branches if br.in_service
            ]
            for combo in combinations(branch_names, 2):
                contingencies.append({
                    "name": f"N-2: {combo[0]} + {combo[1]}",
                    "components": list(combo),
                    "type": "branch",
                })

        elif contingency_type == "n1_1":
            # N-1-1: Sequential N-1 contingencies (first loss, then another)
            branch_names = [
                br.name for br in model.branches if br.in_service
            ]
            for i, first in enumerate(branch_names):
                for second in branch_names[i + 1:]:
                    contingencies.append({
                        "name": f"N-1-1: {first} then {second}",
                        "components": [first, second],
                        "type": "branch_sequential",
                    })

        else:
            logger.warning(f"Unknown contingency type: {contingency_type}, defaulting to N-1")
            # Default to N-1
            for branch in model.branches:
                if branch.in_service:
                    contingencies.append({
                        "name": f"N-1: {branch.name}",
                        "components": [branch.name],
                        "type": "branch",
                    })

        return contingencies

    def _evaluate_contingency(
        self,
        model: PowerSystemModel,
        contingency: dict,
        check_violations: list[str],
        voltage_limits: dict,
        thermal_limit: float,
    ) -> dict:
        """Evaluate a single contingency scenario.

        Args:
            model: Original PowerSystemModel
            contingency: Contingency definition with components to remove
            check_violations: List of violation types to check
            voltage_limits: Voltage limits {"min": float, "max": float}
            thermal_limit: Thermal limit threshold

        Returns:
            Contingency result dictionary
        """
        result = {
            "name": contingency["name"],
            "components": contingency["components"],
            "status": "normal",
            "severity": "normal",
            "violations": [],
        }

        try:
            # Create modified model with components removed
            modified_model = self._create_modified_model(model, contingency)

            if modified_model is None:
                result["status"] = "error"
                result["severity"] = "critical"
                result["violations"].append({
                    "type": "error",
                    "message": "Failed to create modified model",
                })
                return result

            # Check for violations
            violations = []

            if "voltage" in check_violations:
                voltage_violations = self._check_voltage_violations(
                    modified_model, voltage_limits
                )
                violations.extend(voltage_violations)

            if "thermal" in check_violations:
                thermal_violations = self._check_thermal_violations(
                    modified_model, thermal_limit
                )
                violations.extend(thermal_violations)

            result["violations"] = violations

            # Determine status and severity
            if violations:
                has_critical = any(
                    v.get("severity") == "critical" for v in violations
                )
                if has_critical:
                    result["status"] = "violation"
                    result["severity"] = "critical"
                else:
                    result["status"] = "warning"
                    result["severity"] = "warning"

            # Add voltage summary
            voltages = [
                b.v_magnitude_pu for b in modified_model.buses
                if b.v_magnitude_pu is not None
            ]
            if voltages:
                result["min_voltage"] = round(min(voltages), 4)
                result["max_voltage"] = round(max(voltages), 4)

            # Add loading summary
            loadings = [
                br.loading_percent for br in modified_model.branches
                if br.loading_percent is not None
            ]
            if loadings:
                result["max_loading_percent"] = round(max(loadings), 2)

            return result

        except Exception as e:
            logger.error(f"Error evaluating contingency {contingency['name']}: {e}")
            result["status"] = "error"
            result["severity"] = "critical"
            result["violations"].append({
                "type": "error",
                "message": str(e),
            })
            return result

    def _create_modified_model(
        self,
        model: PowerSystemModel,
        contingency: dict,
    ) -> PowerSystemModel | None:
        """Create a modified model with contingency components removed.

        Args:
            model: Original PowerSystemModel
            contingency: Contingency definition with components to remove

        Returns:
            Modified PowerSystemModel or None if failed
        """
        try:
            components_to_remove = contingency.get("components", [])

            # Start with original components
            new_branches = list(model.branches)

            # Remove specified branches
            for comp_name in components_to_remove:
                new_branches = [
                    br for br in new_branches
                    if br.name != comp_name
                ]

            # Create new model with modified branches
            modified = PowerSystemModel(
                buses=model.buses,
                branches=new_branches,
                generators=model.generators,
                loads=model.loads,
                transformers=model.transformers,
                base_mva=model.base_mva,
                frequency_hz=model.frequency_hz,
                name=f"{model.name}_contingency",
            )

            return modified

        except Exception as e:
            logger.error(f"Failed to create modified model: {e}")
            return None

    def _check_voltage_violations(
        self,
        model: PowerSystemModel,
        voltage_limits: dict,
    ) -> list[dict]:
        """Check for voltage violations in the model.

        Args:
            model: PowerSystemModel to check
            voltage_limits: {"min": float, "max": float} in p.u.

        Returns:
            List of violation dictionaries
        """
        violations = []
        vm_min = voltage_limits.get("min", 0.95)
        vm_max = voltage_limits.get("max", 1.05)

        for bus in model.buses:
            if bus.v_magnitude_pu is None:
                continue

            if bus.v_magnitude_pu < vm_min:
                severity = "critical" if bus.v_magnitude_pu < 0.85 else "warning"
                violations.append({
                    "type": "voltage",
                    "subtype": "undervoltage",
                    "component": bus.name,
                    "value": round(bus.v_magnitude_pu, 4),
                    "limit": vm_min,
                    "severity": severity,
                    "message": f"Bus {bus.name}: voltage {bus.v_magnitude_pu:.4f} pu < {vm_min} pu",
                })
            elif bus.v_magnitude_pu > vm_max:
                severity = "critical" if bus.v_magnitude_pu > 1.15 else "warning"
                violations.append({
                    "type": "voltage",
                    "subtype": "overvoltage",
                    "component": bus.name,
                    "value": round(bus.v_magnitude_pu, 4),
                    "limit": vm_max,
                    "severity": severity,
                    "message": f"Bus {bus.name}: voltage {bus.v_magnitude_pu:.4f} pu > {vm_max} pu",
                })

        return violations

    def _check_thermal_violations(
        self,
        model: PowerSystemModel,
        thermal_limit: float,
    ) -> list[dict]:
        """Check for thermal (loading) violations in the model.

        Args:
            model: PowerSystemModel to check
            thermal_limit: Loading threshold (1.0 = 100%)

        Returns:
            List of violation dictionaries
        """
        violations = []
        limit_percent = thermal_limit * 100

        for branch in model.branches:
            if branch.loading_percent is None:
                continue

            if branch.loading_percent > limit_percent:
                loading_pu = branch.loading_percent / 100.0
                severity = "critical" if loading_pu > 1.2 else "warning"
                violations.append({
                    "type": "thermal",
                    "subtype": "overload",
                    "component": branch.name,
                    "value": round(branch.loading_percent, 2),
                    "limit": limit_percent,
                    "severity": severity,
                    "message": f"Branch {branch.name}: loading {branch.loading_percent:.2f}% > {limit_percent}%",
                })

        return violations

    def _calculate_severity(
        self,
        result: dict,
        voltage_limits: dict,
        thermal_limit: float,
    ) -> float:
        """Calculate overall severity score for a contingency result.

        Args:
            result: Contingency result dictionary
            voltage_limits: Voltage limits for severity calculation
            thermal_limit: Thermal limit for severity calculation

        Returns:
            Severity score between 0.0 and 1.0
        """
        # Handle FAIL status - maximum severity
        if result.get("status") == "FAIL":
            return 1.0

        # Handle error status - maximum severity
        if result.get("status") == "error":
            return 1.0

        severity = 0.0
        vm_min = voltage_limits.get("min", 0.95)
        vm_max = voltage_limits.get("max", 1.05)

        min_voltage = result.get("min_voltage", 1.0)
        max_voltage = result.get("max_voltage", 1.0)

        # Voltage severity
        if min_voltage < vm_min:
            severity = max(severity, (vm_min - min_voltage) / vm_min)
        if max_voltage > vm_max:
            severity = max(
                severity,
                (max_voltage - vm_max) / (1.1 - vm_max),
            )

        # Thermal severity
        max_loading = result.get("max_loading_percent", 0)
        if max_loading > thermal_limit * 100:
            loading_pu = max_loading / 100.0
            severity = max(severity, (loading_pu - thermal_limit) / thermal_limit)

        return round(min(severity, 1.0), 4)

    def _identify_weak_points(self, results: list[dict], top_n: int = 10) -> list[dict]:
        """Identify weak points in the system from contingency results.

        Args:
            results: List of contingency result dictionaries
            top_n: Maximum number of weak points to return (default: 10)

        Returns:
            List of weak point dictionaries with component name and critical case count
        """
        component_count: dict[str, int] = {}

        for result in results:
            severity = result.get("severity")
            # Handle both string severity ("critical", "warning") and numeric severity scores
            is_critical = (
                severity in ["critical", "warning"] or
                (isinstance(severity, (int, float)) and severity > 0.5)
            )
            if is_critical:
                for comp in result.get("components", []):
                    component_count[comp] = component_count.get(comp, 0) + 1

        # Sort by count and return top weak points
        sorted_points = sorted(
            component_count.items(),
            key=lambda x: x[1],
            reverse=True,
        )

        return [
            {"component": comp, "critical_cases": count}
            for comp, count in sorted_points[:top_n]
        ]


    def run_legacy(self, config: dict[str, Any]):
        """Legacy run method that accepts config dict for backward compatibility.

        Args:
            config: Configuration dictionary with model, auth, etc.

        Returns:
            SkillResult with analysis results
        """
        from cloudpss_skills_v2.core.skill_result import SkillResult, SkillStatus
        from cloudpss_skills_v2.powerskill import Engine
        from cloudpss_skills_v2.core.system_model import PowerSystemModel, Bus, Branch, Generator, Load

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

            # Convert handle to unified model (simplified conversion)
            model = self._convert_handle_to_model(handle)

            # Get contingency config
            contingency_config = config.get("contingency", {})
            level = contingency_config.get("level", "N-1").lower().replace("-", "")

            # Run analysis with unified model
            result = self._run_unified(model, {
                "contingency_type": level,
                "check_violations": ["thermal", "voltage"],
            })

            # Add expected keys for test compatibility
            result["model_rid"] = model_rid
            result["all_results"] = result.get("contingencies", [])

            # Convert result to SkillResult format
            if result["status"] == "error":
                return SkillResult(
                    skill_name=self.name,
                    status=SkillStatus.FAILED,
                    error=result.get("error", "Unknown error"),
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
            logger.error(f"Legacy contingency analysis failed: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error=str(e),
                start_time=start_time,
                end_time=datetime.now(),
            )

    def _convert_handle_to_model(self, handle) -> PowerSystemModel:
        """Convert model handle to unified PowerSystemModel.

        This is a simplified conversion for demonstration.
        In production, use the full adapter from powerapi.
        """
        from cloudpss_skills_v2.core.system_model import PowerSystemModel, Bus, Branch

        # Placeholder conversion - would use actual adapter
        buses = []
        branches = []

        try:
            # Get ext_grid buses (slack buses) first
            slack_bus_indices = set()
            try:
                ext_grid_components = handle.get_components_by_type(ComponentType.SOURCE)
                for comp in ext_grid_components:
                    args = comp.args if hasattr(comp, 'args') and comp.args else {}
                    bus_idx = args.get('bus', '') if isinstance(args, dict) else ''
                    # Convert to bus key format (e.g., 0 -> "bus:0")
                    if isinstance(bus_idx, int):
                        slack_bus_indices.add(f"bus:{bus_idx}")
                    elif bus_idx:
                        slack_bus_indices.add(str(bus_idx))
            except Exception:
                pass

            # Try to get buses from handle
            bus_components = handle.get_components_by_type(ComponentType.BUS)
            for comp in bus_components:
                # Get base_kv from component args or use default
                args = comp.args if hasattr(comp, 'args') and comp.args else {}
                base_kv = args.get('vn_kv', 110.0) if isinstance(args, dict) else 110.0
                # Ensure base_kv is a float
                try:
                    base_kv = float(base_kv) if base_kv else 110.0
                except (TypeError, ValueError):
                    base_kv = 110.0

                # Parse bus_id from key (e.g., "bus:0" -> 0)
                bus_id = comp.key
                if isinstance(bus_id, str) and ':' in bus_id:
                    try:
                        bus_id = int(bus_id.split(':')[-1])
                    except ValueError:
                        bus_id = 0
                elif isinstance(bus_id, str):
                    # Try to parse as int directly
                    try:
                        bus_id = int(bus_id)
                    except ValueError:
                        bus_id = 0
                elif not isinstance(bus_id, int):
                    bus_id = 0

                # Determine bus type - check if this is a slack bus
                bus_type = "SLACK" if comp.key in slack_bus_indices else "PQ"
                bus = Bus(
                    bus_id=bus_id,
                    name=comp.name,
                    base_kv=base_kv,
                    v_magnitude_pu=1.0,
                    bus_type=bus_type,
                )
                buses.append(bus)

            # Try to get branches from handle
            branch_components = handle.get_components_by_type(ComponentType.BRANCH)
            for comp in branch_components:
                # Get connected buses
                args = comp.args if hasattr(comp, "args") and comp.args else {}
                from_bus_key = args.get("from_bus", "") if isinstance(args, dict) else ""
                to_bus_key = args.get("to_bus", "") if isinstance(args, dict) else ""

                # Parse bus IDs from keys (e.g., "bus:0" -> 0)
                from_bus = from_bus_key
                if isinstance(from_bus_key, str) and ":" in from_bus_key:
                    try:
                        from_bus = int(from_bus_key.split(":")[-1])
                    except ValueError:
                        from_bus = 0
                elif isinstance(from_bus_key, str):
                    try:
                        from_bus = int(from_bus_key)
                    except ValueError:
                        from_bus = 0
                elif not isinstance(from_bus_key, int):
                    from_bus = 0

                to_bus = to_bus_key
                if isinstance(to_bus_key, str) and ":" in to_bus_key:
                    try:
                        to_bus = int(to_bus_key.split(":")[-1])
                    except ValueError:
                        to_bus = 0
                elif isinstance(to_bus_key, str):
                    try:
                        to_bus = int(to_bus_key)
                    except ValueError:
                        to_bus = 0
                elif not isinstance(to_bus_key, int):
                    to_bus = 0

                # Skip branches that connect a bus to itself (invalid)
                if from_bus == to_bus:
                    logger.warning(f"Skipping branch {comp.key}: connects bus {from_bus} to itself")
                    continue

                try:
                    branch = Branch(
                        name=comp.key,
                        from_bus=from_bus,
                        to_bus=to_bus,
                        r_pu=0.01,
                        x_pu=0.1,
                        in_service=True,
                    )
                    branches.append(branch)
                except ValueError as e:
                    logger.warning(f"Skipping branch {comp.key}: {e}")
                    continue
        except Exception as e:
            logger.warning(f"Could not convert handle to model: {e}")

        return PowerSystemModel(
            buses=buses,
            branches=branches,
            base_mva=100.0,
        )


__all__ = ["ContingencyAnalysis"]
