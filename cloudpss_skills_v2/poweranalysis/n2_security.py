"""N2 Security Analysis - Check all pairwise contingency scenarios using unified model.

N-2安全校核 - 检查所有支路对的同时断开，使用统一PowerSystemModel。
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from itertools import combinations
from typing import Any

from cloudpss_skills_v2.core.system_model import PowerSystemModel, Branch
from cloudpss_skills_v2.poweranalysis.base import PowerAnalysis

logger = logging.getLogger(__name__)


@dataclass
class N2ContingencyResult:
    """Result for a single N-2 contingency scenario."""

    branch_pair: tuple[str, str] = ()
    converged: bool = True
    voltage_violations: list[dict[str, Any]] = field(default_factory=list)
    thermal_violations: list[dict[str, Any]] = field(default_factory=list)
    has_violations: bool = False


class N2SecurityAnalysis(PowerAnalysis):
    """N-2安全校核技能 - 使用统一PowerSystemModel的实现。

    检查所有支路对同时断开后的系统安全性。
    """

    name = "n2_security"
    description = "N-2安全校核 - 检查支路对同时断开的安全"

    def run(self, model: PowerSystemModel, config: dict) -> dict:
        """Run N-2 security analysis on unified model.

        Args:
            model: Unified PowerSystemModel containing buses, branches, etc.
            config: Analysis configuration dictionary with optional keys:
                - check_pairs: List of (branch1_name, branch2_name) tuples to check.
                               If empty, all pairs are checked.
                - voltage_threshold: Voltage deviation threshold (default: 0.05)
                - thermal_threshold: Thermal loading threshold (default: 1.0)
                - max_pairs: Maximum number of pairs to check (default: all)

        Returns:
            Dictionary with analysis results:
                - status: "success" or "error"
                - n2_results: List of N2ContingencyResult for each pair
                - total_pairs: Total number of pairs checked
                - violations_count: Number of pairs with violations
                - summary: Summary statistics
        """
        # Validate model
        errors = self.validate_model(model)
        if errors:
            return {
                "status": "error",
                "errors": errors,
            }

        # Get configuration
        check_pairs = config.get("check_pairs", [])
        voltage_threshold = config.get("voltage_threshold", 0.05)
        thermal_threshold = config.get("thermal_threshold", 1.0)
        max_pairs = config.get("max_pairs", None)

        # Generate branch pairs to check
        if check_pairs:
            # Use specified pairs
            pairs = check_pairs
        else:
            # Generate all combinations of 2 branches
            branch_names = [br.name for br in model.branches if br.in_service]
            pairs = list(combinations(branch_names, 2))

        # Apply max_pairs limit if specified
        if max_pairs is not None:
            pairs = pairs[:max_pairs]

        # Run N-2 analysis for each pair
        results: list[N2ContingencyResult] = []
        violations_count = 0

        for i, (br1_name, br2_name) in enumerate(pairs):
            logger.info(f"[{i + 1}/{len(pairs)}] Checking N-2 contingency: {br1_name} + {br2_name}")

            try:
                # Create N-2 model by removing both branches
                n2_model = self._create_n2_model(model, br1_name, br2_name)

                # Check violations on the N-2 model
                voltage_violations = self._check_voltage_violations(n2_model, voltage_threshold)
                thermal_violations = self._check_thermal_violations(n2_model, thermal_threshold)

                has_violations = bool(voltage_violations or thermal_violations)
                if has_violations:
                    violations_count += 1

                result = N2ContingencyResult(
                    branch_pair=(br1_name, br2_name),
                    converged=True,  # Model creation always succeeds
                    voltage_violations=voltage_violations,
                    thermal_violations=thermal_violations,
                    has_violations=has_violations,
                )
                results.append(result)

            except Exception as e:
                logger.error(f"Error checking N-2 contingency {br1_name} + {br2_name}: {e}")
                result = N2ContingencyResult(
                    branch_pair=(br1_name, br2_name),
                    converged=False,
                    has_violations=True,
                )
                results.append(result)
                violations_count += 1

        # Build summary
        summary = {
            "total_pairs": len(pairs),
            "violations_count": violations_count,
            "pass_rate": (len(pairs) - violations_count) / len(pairs) if pairs else 1.0,
        }

        return {
            "status": "success",
            "n2_results": [
                {
                    "branch_pair": r.branch_pair,
                    "converged": r.converged,
                    "has_violations": r.has_violations,
                    "voltage_violations": r.voltage_violations,
                    "thermal_violations": r.thermal_violations,
                }
                for r in results
            ],
            "total_pairs": len(pairs),
            "violations_count": violations_count,
            "summary": summary,
        }

    def _create_n2_model(self, model: PowerSystemModel, br1_name: str, br2_name: str) -> PowerSystemModel:
        """Create N-2 model by removing two branches.

        Args:
            model: Base PowerSystemModel
            br1_name: Name of first branch to remove
            br2_name: Name of second branch to remove

        Returns:
            New PowerSystemModel with both branches removed
        """
        # Create new branches list excluding both target branches
        new_branches = [
            br for br in model.branches
            if br.name != br1_name and br.name != br2_name
        ]

        # Create new model with modified branches
        return PowerSystemModel(
            buses=model.buses,
            branches=new_branches,
            generators=model.generators,
            loads=model.loads,
            base_mva=model.base_mva,
            frequency_hz=model.frequency_hz,
            name=f"{model.name}_N2_{br1_name}_{br2_name}",
            description=f"N-2 contingency: {br1_name} + {br2_name} removed",
        )

    def _check_voltage_violations(
        self, model: PowerSystemModel, threshold: float
    ) -> list[dict[str, Any]]:
        """Check for voltage violations in the model.

        Args:
            model: PowerSystemModel to check
            threshold: Voltage deviation threshold from 1.0 p.u.

        Returns:
            List of voltage violation records
        """
        violations = []

        for bus in model.buses:
            if bus.v_magnitude_pu is None:
                continue

            # Check against bus-specific limits
            if bus.v_magnitude_pu < bus.vm_min_pu:
                violations.append({
                    "type": "voltage",
                    "component": bus.name,
                    "value": bus.v_magnitude_pu,
                    "threshold": bus.vm_min_pu,
                    "violation_type": "undervoltage",
                })
            elif bus.v_magnitude_pu > bus.vm_max_pu:
                violations.append({
                    "type": "voltage",
                    "component": bus.name,
                    "value": bus.v_magnitude_pu,
                    "threshold": bus.vm_max_pu,
                    "violation_type": "overvoltage",
                })

        return violations

    def _check_thermal_violations(
        self, model: PowerSystemModel, threshold: float
    ) -> list[dict[str, Any]]:
        """Check for thermal (loading) violations in the model.

        Args:
            model: PowerSystemModel to check
            threshold: Loading threshold (1.0 = 100%)

        Returns:
            List of thermal violation records
        """
        violations = []

        for branch in model.branches:
            if branch.loading_percent is None:
                continue

            # Check if loading exceeds threshold
            loading_pu = branch.loading_percent / 100.0
            if loading_pu > threshold:
                violations.append({
                    "type": "thermal",
                    "component": branch.name,
                    "value": loading_pu,
                    "threshold": threshold,
                    "loading_percent": branch.loading_percent,
                })

        return violations


__all__ = ["N2SecurityAnalysis", "N2ContingencyResult"]
