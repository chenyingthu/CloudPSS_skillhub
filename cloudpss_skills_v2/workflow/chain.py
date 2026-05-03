"""Analysis Chain Module - Sequential execution of power system analyses.

This module provides the AnalysisChain class for chaining multiple analyses
together in sequential order, with context sharing between steps.

Example:
    >>> chain = AnalysisChain(name="my_analysis")
    >>> chain.add_step("power_flow", PowerFlowAnalysis(), {"iterations": 100})
    ...        .add_step("n1_security", N1SecurityAnalysis())
    >>> result = chain.run(model)
    >>> print(result.success)
    True
    >>> print(result.results["power_flow"])
    {...}
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Iterator

from cloudpss_skills_v2.core.system_model import PowerSystemModel
from cloudpss_skills_v2.poweranalysis.base import PowerAnalysis

logger = logging.getLogger(__name__)


@dataclass
class Step:
    """A single step in an analysis chain.

    Attributes:
        name: Unique identifier for this step
        analysis: The PowerAnalysis instance to run
        config: Configuration dictionary passed to the analysis
    """

    name: str
    analysis: PowerAnalysis
    config: dict[str, Any] = field(default_factory=dict)


@dataclass
class ChainResult:
    """Result of running an AnalysisChain.

    Attributes:
        chain_name: Name of the chain that produced this result
        success: Whether all steps completed successfully
        results: Dictionary mapping step names to their results
        error_info: Error information if the chain failed
    """

    chain_name: str | None
    success: bool
    results: dict[str, Any] = field(default_factory=dict)
    error_info: dict[str, Any] | None = None

    @property
    def step_count(self) -> int:
        """Return the total number of steps in the chain."""
        return len(self.results) - (1 if "error" in self.results else 0)

    @property
    def completed_steps(self) -> list[str]:
        """Return list of successfully completed step names."""
        if "error" in self.results:
            # Find the step that failed
            failed_step = self.results["error"].get("step", "")
            return [k for k in self.results.keys() if k not in ("error", failed_step)]
        return list(self.results.keys())

    @property
    def failed_step(self) -> str | None:
        """Return the name of the failed step, if any."""
        if "error" in self.results:
            return self.results["error"].get("step")
        return None


class AnalysisChain:
    """Sequential chain of power system analyses.

    The AnalysisChain allows you to define a sequence of analyses that run
    one after another, with optional context sharing between steps. Each
    step can access the results of previous steps through the context.

    Attributes:
        name: Optional name for this chain
        steps: List of Step objects in execution order
        continue_on_error: Whether to continue after a step fails

    Example:
        >>> chain = AnalysisChain(name="security_assessment")
        >>> chain.add_step("pf", PowerFlowAnalysis())
        ...        .add_step("n1", N1SecurityAnalysis())
        ...        .add_step("stability", TransientStabilityAnalysis())
        >>> result = chain.run(model)
    """

    def __init__(self, name: str | None = None, continue_on_error: bool = False):
        """Initialize an empty analysis chain.

        Args:
            name: Optional name for identification
            continue_on_error: If True, continue executing after a step fails
        """
        self.name = name
        self.steps: list[Step] = []
        self.continue_on_error = continue_on_error
        self._step_names: set[str] = set()

    def add_step(
        self, name: str, analysis: PowerAnalysis, config: dict[str, Any] | None = None
    ) -> AnalysisChain:
        """Add a step to the chain.

        This method returns self to enable method chaining (fluent interface).

        Args:
            name: Unique identifier for this step
            analysis: The PowerAnalysis instance to execute
            config: Optional configuration dictionary for this step

        Returns:
            self for method chaining

        Raises:
            ValueError: If name is empty or a step with this name already exists

        Example:
            >>> chain.add_step("pf", PowerFlowAnalysis(), {"iterations": 100})
            ...        .add_step("n1", N1SecurityAnalysis())
        """
        if not name:
            raise ValueError("Step name cannot be empty")

        if name in self._step_names:
            raise ValueError(f"Step '{name}' already exists in chain")

        step = Step(name=name, analysis=analysis, config=config or {})
        self.steps.append(step)
        self._step_names.add(name)

        logger.debug(f"Added step '{name}' to chain '{self.name}'")
        return self

    def run(
        self, model: PowerSystemModel, context: dict[str, Any] | None = None
    ) -> ChainResult:
        """Execute all steps in the chain sequentially.

        Steps are executed in the order they were added. Each step receives
        the model and a config dictionary that includes any user-provided
        config plus a "context" key containing results from previous steps.

        Args:
            model: The PowerSystemModel to analyze
            context: Optional initial context to pass to first step

        Returns:
            ChainResult containing all step results and success status

        Example:
            >>> result = chain.run(model, context={"custom": "data"})
            >>> if result.success:
            ...     print(result.results["step1"])
        """
        if not self.steps:
            logger.debug("Running empty chain")
            return ChainResult(chain_name=self.name, success=True, results={})

        # Validate model before running
        validation_errors = self._validate_model(model)
        if validation_errors:
            error_info = {
                "step": "validation",
                "exception": "ModelValidationError",
                "message": "; ".join(validation_errors),
            }
            return ChainResult(
                chain_name=self.name,
                success=False,
                results={"error": error_info},
                error_info=error_info,
            )

        results: dict[str, Any] = {}
        shared_context = dict(context) if context else {}
        previous_results: list[dict[str, Any]] = []

        for step in self.steps:
            try:
                # Build config with context for this step
                step_config = dict(step.config)
                step_config["context"] = {
                    **shared_context,
                    "previous_results": previous_results.copy(),
                    "current_step": step.name,
                }

                logger.info(f"Running step '{step.name}' in chain '{self.name}'")

                # Execute the analysis
                step_result = step.analysis.run(model, step_config)

                # Store result
                results[step.name] = step_result
                previous_results.append({step.name: step_result})

                logger.debug(f"Step '{step.name}' completed successfully")

            except Exception as e:
                logger.error(f"Step '{step.name}' failed: {e}")

                error_info = {
                    "step": step.name,
                    "exception": type(e).__name__,
                    "message": str(e),
                }
                results["error"] = error_info

                if not self.continue_on_error:
                    return ChainResult(
                        chain_name=self.name,
                        success=False,
                        results=results,
                        error_info=error_info,
                    )
                # Continue to next step if continue_on_error is True

        # Determine overall success
        success = "error" not in results

        return ChainResult(
            chain_name=self.name,
            success=success,
            results=results,
            error_info=results.get("error"),
        )

    def _validate_model(self, model: PowerSystemModel) -> list[str]:
        """Validate the model before running analyses.

        Args:
            model: The PowerSystemModel to validate

        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []

        if not model.buses:
            errors.append("Model has no buses")

        # Check for slack bus
        has_slack = any(
            hasattr(bus, "bus_type") and bus.bus_type == "SLACK" for bus in model.buses
        )
        if not has_slack:
            errors.append("Model has no slack bus")

        return errors

    def __iter__(self) -> Iterator[Step]:
        """Allow iteration over steps."""
        return iter(self.steps)

    def __len__(self) -> int:
        """Return the number of steps."""
        return len(self.steps)

    def __str__(self) -> str:
        """String representation of the chain."""
        name_str = f"'{self.name}'" if self.name else "(unnamed)"
        step_count = len(self.steps)
        return f"AnalysisChain({name_str}, {step_count} step{'s' if step_count != 1 else ''})"

    def __repr__(self) -> str:
        """Detailed representation of the chain."""
        return f"AnalysisChain(name={self.name!r}, steps={[s.name for s in self.steps]!r})"
