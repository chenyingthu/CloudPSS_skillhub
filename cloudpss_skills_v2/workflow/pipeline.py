"""Analysis Pipeline Module - Parallel execution of power system analyses.

This module provides the AnalysisPipeline class for running multiple analyses
in parallel using a ThreadPoolExecutor, enabling faster execution of
independent analyses.

Example:
    >>> pipeline = AnalysisPipeline(name="my_pipeline", max_workers=4)
    >>> pipeline.add_analysis("pf", PowerFlowAnalysis())
    ...           .add_analysis("n1", N1SecurityAnalysis())
    >>> result = pipeline.run(model)
    >>> print(result.successful_count)
    2
"""

from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import Any, Iterator

from cloudpss_skills_v2.core.system_model import PowerSystemModel
from cloudpss_skills_v2.poweranalysis.base import PowerAnalysis

logger = logging.getLogger(__name__)


@dataclass
class AnalysisTask:
    """A single analysis task in a pipeline.

    Attributes:
        name: Unique identifier for this analysis
        analysis: The PowerAnalysis instance to run
        config: Configuration dictionary passed to the analysis
    """

    name: str
    analysis: PowerAnalysis
    config: dict[str, Any] = field(default_factory=dict)


@dataclass
class PipelineResult:
    """Result of running an AnalysisPipeline.

    Attributes:
        pipeline_name: Name of the pipeline that produced this result
        success: Whether all analyses completed successfully
        results: Dictionary mapping analysis names to their results
        execution_time: Time taken to execute all analyses (seconds)
    """

    pipeline_name: str | None
    success: bool
    results: dict[str, Any] = field(default_factory=dict)
    execution_time: float = 0.0

    @property
    def analysis_count(self) -> int:
        """Return the total number of analyses in the pipeline."""
        errors = self.results.get("errors", [])
        return len(self.results) - (1 if errors else 0)

    @property
    def successful_count(self) -> int:
        """Return the number of successfully completed analyses."""
        errors = self.results.get("errors", [])
        failed_names = {e.get("analysis") for e in errors}
        return len([k for k in self.results.keys() if k not in ("errors",) and k not in failed_names])

    @property
    def failed_count(self) -> int:
        """Return the number of failed analyses."""
        errors = self.results.get("errors", [])
        return len(errors)

    @property
    def successful_analyses(self) -> list[str]:
        """Return list of successfully completed analysis names."""
        errors = self.results.get("errors", [])
        failed_names = {e.get("analysis") for e in errors}
        return [k for k in self.results.keys() if k not in ("errors",) and k not in failed_names]

    @property
    def failed_analyses(self) -> list[str]:
        """Return list of failed analysis names."""
        errors = self.results.get("errors", [])
        return [e.get("analysis") for e in errors if e.get("analysis")]


class AnalysisPipeline:
    """Parallel pipeline for power system analyses.

    The AnalysisPipeline allows you to run multiple independent analyses
    concurrently using a thread pool. This is useful when you have several
    analyses that don't depend on each other and can be executed in parallel.

    Attributes:
        name: Optional name for this pipeline
        analyses: List of AnalysisTask objects
        max_workers: Maximum number of parallel threads

    Example:
        >>> pipeline = AnalysisPipeline(name="parallel_security", max_workers=4)
        >>> pipeline.add_analysis("n1", N1SecurityAnalysis())
        ...           .add_analysis("n2", N2SecurityAnalysis())
        ...           .add_analysis("voltage", VoltageStabilityAnalysis())
        >>> result = pipeline.run(model)
    """

    def __init__(self, name: str | None = None, max_workers: int | None = None):
        """Initialize an empty analysis pipeline.

        Args:
            name: Optional name for identification
            max_workers: Maximum number of worker threads. If None,
                        defaults to min(32, (os.cpu_count() or 1) + 4)
        """
        self.name = name
        self.analyses: list[AnalysisTask] = []
        self.max_workers = max_workers
        self._analysis_names: set[str] = set()

    def add_analysis(
        self, name: str, analysis: PowerAnalysis, config: dict[str, Any] | None = None
    ) -> AnalysisPipeline:
        """Add an analysis to the pipeline.

        This method returns self to enable method chaining (fluent interface).

        Args:
            name: Unique identifier for this analysis
            analysis: The PowerAnalysis instance to execute
            config: Optional configuration dictionary for this analysis

        Returns:
            self for method chaining

        Raises:
            ValueError: If name is empty or an analysis with this name already exists

        Example:
            >>> pipeline.add_analysis("pf", PowerFlowAnalysis(), {"iterations": 100})
            ...            .add_analysis("n1", N1SecurityAnalysis())
        """
        if not name:
            raise ValueError("Analysis name cannot be empty")

        if name in self._analysis_names:
            raise ValueError(f"Analysis '{name}' already exists in pipeline")

        task = AnalysisTask(name=name, analysis=analysis, config=config or {})
        self.analyses.append(task)
        self._analysis_names.add(name)

        logger.debug(f"Added analysis '{name}' to pipeline '{self.name}'")
        return self

    def run(self, model: PowerSystemModel) -> PipelineResult:
        """Execute all analyses in the pipeline in parallel.

        Analyses are executed concurrently using a ThreadPoolExecutor.
        Each analysis receives the model and its configured config dict.

        Args:
            model: The PowerSystemModel to analyze

        Returns:
            PipelineResult containing all analysis results and success status

        Example:
            >>> result = pipeline.run(model)
            >>> print(f"Completed {result.successful_count}/{result.analysis_count}")
        """
        import time

        if not self.analyses:
            logger.debug("Running empty pipeline")
            return PipelineResult(
                pipeline_name=self.name,
                success=True,
                results={},
                execution_time=0.0,
            )

        # Validate model before running
        validation_errors = self._validate_model(model)
        if validation_errors:
            error_result = {
                "errors": [
                    {
                        "analysis": "validation",
                        "exception": "ModelValidationError",
                        "message": "; ".join(validation_errors),
                    }
                ]
            }
            return PipelineResult(
                pipeline_name=self.name,
                success=False,
                results=error_result,
                execution_time=0.0,
            )

        results: dict[str, Any] = {}
        errors: list[dict[str, Any]] = []

        start_time = time.time()

        # Use ThreadPoolExecutor for parallel execution
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_task = {}
            for task in self.analyses:
                future = executor.submit(self._run_analysis, task, model)
                future_to_task[future] = task

            # Collect results as they complete
            for future in as_completed(future_to_task):
                task = future_to_task[future]
                try:
                    task_result = future.result()
                    results[task.name] = task_result
                    logger.debug(f"Analysis '{task.name}' completed successfully")
                except Exception as e:
                    logger.error(f"Analysis '{task.name}' failed: {e}")
                    errors.append(
                        {
                            "analysis": task.name,
                            "exception": type(e).__name__,
                            "message": str(e),
                        }
                    )

        execution_time = time.time() - start_time

        # Add errors to results if any
        if errors:
            results["errors"] = errors

        # Determine overall success
        success = len(errors) == 0

        logger.info(
            f"Pipeline '{self.name}' completed: "
            f"{len(results) - (1 if errors else 0)}/{len(self.analyses)} successful, "
            f"{execution_time:.2f}s"
        )

        return PipelineResult(
            pipeline_name=self.name,
            success=success,
            results=results,
            execution_time=execution_time,
        )

    def _run_analysis(self, task: AnalysisTask, model: PowerSystemModel) -> Any:
        """Run a single analysis task.

        Args:
            task: The AnalysisTask to execute
            model: The PowerSystemModel to analyze

        Returns:
            The result of the analysis
        """
        logger.info(f"Running analysis '{task.name}' in pipeline '{self.name}'")
        return task.analysis.run(model, dict(task.config))

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

    def __iter__(self) -> Iterator[AnalysisTask]:
        """Allow iteration over analyses."""
        return iter(self.analyses)

    def __len__(self) -> int:
        """Return the number of analyses."""
        return len(self.analyses)

    def __str__(self) -> str:
        """String representation of the pipeline."""
        name_str = f"'{self.name}'" if self.name else "(unnamed)"
        analysis_count = len(self.analyses)
        return f"AnalysisPipeline({name_str}, {analysis_count} analysis{'es' if analysis_count != 1 else ''})"

    def __repr__(self) -> str:
        """Detailed representation of the pipeline."""
        return f"AnalysisPipeline(name={self.name!r}, analyses={[a.name for a in self.analyses]!r}, max_workers={self.max_workers!r})"
