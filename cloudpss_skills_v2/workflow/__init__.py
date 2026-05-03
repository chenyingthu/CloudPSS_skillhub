"""Workflow Module - Analysis chaining and parallel execution.

This module provides classes for orchestrating multiple power system analyses:

- AnalysisChain: Sequential execution with context sharing between steps
- AnalysisPipeline: Parallel execution using ThreadPoolExecutor
- ChainResult: Results from a chain execution
- PipelineResult: Results from a pipeline execution

Example - Sequential Chain:
    >>> from cloudpss_skills_v2.workflow import AnalysisChain
    >>> from cloudpss_skills_v2.poweranalysis import PowerFlowAnalysis, N1SecurityAnalysis
    >>>
    >>> chain = AnalysisChain(name="security_assessment")
    >>> chain.add_step("pf", PowerFlowAnalysis())
    ...        .add_step("n1", N1SecurityAnalysis())
    >>> result = chain.run(model)
    >>> print(result.success)
    True

Example - Parallel Pipeline:
    >>> from cloudpss_skills_v2.workflow import AnalysisPipeline
    >>> from cloudpss_skills_v2.poweranalysis import (
    ...     VoltageStabilityAnalysis,
    ...     TransientStabilityAnalysis,
    ... )
    >>>
    >>> pipeline = AnalysisPipeline(name="stability_check", max_workers=4)
    >>> pipeline.add_analysis("voltage", VoltageStabilityAnalysis())
    ...           .add_analysis("transient", TransientStabilityAnalysis())
    >>> result = pipeline.run(model)
    >>> print(f"Completed {result.successful_count} analyses")
    2
"""

from cloudpss_skills_v2.workflow.chain import AnalysisChain, ChainResult
from cloudpss_skills_v2.workflow.pipeline import AnalysisPipeline, PipelineResult

__all__ = [
    # Core classes
    "AnalysisChain",
    "AnalysisPipeline",
    # Result classes
    "ChainResult",
    "PipelineResult",
]
