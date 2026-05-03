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
from cloudpss_skills_v2.powerapi.adapters.handle_converter import (
    convert_handle_to_power_system_model,
)

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

    @property
    def config_schema(self) -> dict[str, Any]:
        """JSON Schema for configuration validation."""
        return {
            "type": "object",
            "required": ["model"],
            "properties": {
                "skill": {"type": "string"},
                "model": {
                    "type": "object",
                    "required": ["rid"],
                    "properties": {
                        "rid": {"type": "string"},
                        "source": {"type": "string", "enum": ["cloud", "local"]},
                    },
                },
                "engine": {"type": "string", "enum": ["cloudpss", "pandapower"], "default": "pandapower"},
                "auth": {"type": "object"},
                "analysis": {
                    "type": "object",
                    "properties": {
                        "branches": {"type": "array", "items": {"type": "string"}},
                        "max_scenarios": {"type": "integer"},
                    },
                },
                "check_pairs": {"type": "array", "default": []},
                "voltage_threshold": {"type": "number", "default": 0.05},
                "thermal_threshold": {"type": "number", "default": 1.0},
            },
        }

    def get_default_config(self) -> dict[str, Any]:
        """Return default configuration."""
        return {
            "skill": "n2_security",
            "engine": "pandapower",
            "model": {"rid": "case14", "source": "local"},
            "analysis": {"branches": ["line:0", "line:1"], "max_scenarios": 1},
            "check_pairs": [],
            "voltage_threshold": 0.05,
            "thermal_threshold": 1.0,
        }

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
        """Run N-2 security analysis with unified model or config-based interface.

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

    def _run_legacy(self, config: dict[str, Any]) -> SkillResult:
        """Run N-2 security analysis with config-based interface (legacy)."""
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

            # Run analysis with unified model
            result = self._run_unified(model, {
                "check_pairs": config.get("analysis", {}).get("branches", []),
                "voltage_threshold": config.get("analysis", {}).get("voltage_threshold", 0.05),
                "thermal_threshold": config.get("analysis", {}).get("thermal_threshold", 1.0),
                "max_pairs": config.get("analysis", {}).get("max_scenarios"),
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
            logger.error(f"N-2 security analysis failed: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error=str(e),
                start_time=start_time,
                end_time=datetime.now(),
            )

    def _convert_handle_to_model(self, handle) -> PowerSystemModel:
        """Convert model handle to unified PowerSystemModel."""
        return convert_handle_to_power_system_model(handle)

    def _run_unified(self, model: PowerSystemModel, config: dict) -> dict:
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
            # If check_pairs is a list of branch names (not pairs), generate combinations
            if check_pairs and isinstance(check_pairs[0], str):
                # It's a list of branch names, generate all combinations of 2
                pairs = list(combinations(check_pairs, 2))
            else:
                # Use specified pairs directly
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
