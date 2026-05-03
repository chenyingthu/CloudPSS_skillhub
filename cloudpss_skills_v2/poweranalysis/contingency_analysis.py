"""Contingency Analysis Skill v2 - Engine-agnostic N-K contingency analysis.

预想事故分析 - 系统性评估电网在多种故障工况下的安全裕度
支持N-1、N-2、N-K故障，故障排序，薄弱环节识别
"""

from __future__ import annotations

import logging
from itertools import combinations
from typing import Any

from cloudpss_skills_v2.core.system_model import (
    PowerSystemModel,
    Bus,
    Branch,
)
from cloudpss_skills_v2.poweranalysis.base import PowerAnalysis

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

    def run(self, model: PowerSystemModel, config: dict) -> dict:
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

    def _identify_weak_points(self, results: list[dict]) -> list[dict]:
        """Identify weak points in the system from contingency results.

        Args:
            results: List of contingency result dictionaries

        Returns:
            List of weak point dictionaries with component name and critical case count
        """
        component_count: dict[str, int] = {}

        for result in results:
            if result.get("severity") in ["critical", "warning"]:
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
            for comp, count in sorted_points[:10]  # Top 10
        ]


__all__ = ["ContingencyAnalysis"]
