"""Tests for workflow module - AnalysisChain and AnalysisPipeline.

This module tests the workflow chaining functionality for power system analyses.
"""

from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from cloudpss_skills_v2.core.system_model import Bus, PowerSystemModel
from cloudpss_skills_v2.poweranalysis.base import PowerAnalysis
from cloudpss_skills_v2.workflow.chain import AnalysisChain, ChainResult
from cloudpss_skills_v2.workflow.pipeline import AnalysisPipeline, PipelineResult


# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def sample_model():
    """Create a sample PowerSystemModel for testing."""
    slack_bus = Bus(
        bus_id=0,
        name="Slack",
        base_kv=110.0,
        bus_type="SLACK",
        v_magnitude_pu=1.0,
        v_angle_degree=0.0,
    )
    pv_bus = Bus(
        bus_id=1,
        name="PV",
        base_kv=110.0,
        bus_type="PV",
        v_magnitude_pu=1.02,
    )
    pq_bus = Bus(
        bus_id=2,
        name="PQ",
        base_kv=110.0,
        bus_type="PQ",
    )
    return PowerSystemModel(
        buses=[slack_bus, pv_bus, pq_bus],
        branches=[],
        generators=[],
        loads=[],
    )


class MockAnalysis(PowerAnalysis):
    """Mock analysis for testing."""

    def __init__(self, name: str = "mock", delay: float = 0.0, result_data: dict | None = None):
        self.name = name
        self.delay = delay
        self.result_data = result_data or {"value": 42, "name": name}

    def run(self, model: PowerSystemModel, config: dict) -> dict:
        if self.delay > 0:
            time.sleep(self.delay)
        return {"name": self.name, **self.result_data, "config": config}


class FailingAnalysis(PowerAnalysis):
    """Analysis that fails for testing error handling."""

    def __init__(self, name: str = "failing"):
        self.name = name

    def run(self, model: PowerSystemModel, config: dict) -> dict:
        raise ValueError(f"Analysis {self.name} failed")


class ContextDependentAnalysis(PowerAnalysis):
    """Analysis that depends on previous results in context."""

    def __init__(self, name: str = "context"):
        self.name = name

    def run(self, model: PowerSystemModel, config: dict) -> dict:
        # Access previous results from context
        previous_results = config.get("context", {}).get("previous_results", [])
        return {
            "name": self.name,
            "previous_count": len(previous_results),
            "depends_on": config.get("depends_on"),
        }


# =============================================================================
# AnalysisChain Tests
# =============================================================================


class TestAnalysisChain:
    """Test suite for AnalysisChain."""

    def test_chain_creation(self):
        """Test creating an empty chain."""
        chain = AnalysisChain()
        assert chain.name is None
        assert len(chain.steps) == 0

    def test_chain_with_name(self):
        """Test creating a named chain."""
        chain = AnalysisChain(name="test_chain")
        assert chain.name == "test_chain"

    def test_add_step_returns_self(self):
        """Test that add_step returns chain for fluent interface."""
        chain = AnalysisChain()
        analysis = MockAnalysis()

        result = chain.add_step("step1", analysis)

        assert result is chain
        assert len(chain.steps) == 1

    def test_add_step_stores_config(self):
        """Test that add_step stores analysis and config."""
        chain = AnalysisChain()
        analysis = MockAnalysis()
        config = {"param1": "value1"}

        chain.add_step("step1", analysis, config)

        assert chain.steps[0].name == "step1"
        assert chain.steps[0].analysis is analysis
        assert chain.steps[0].config == config

    def test_add_step_default_config(self):
        """Test that add_step uses empty dict as default config."""
        chain = AnalysisChain()
        analysis = MockAnalysis()

        chain.add_step("step1", analysis)

        assert chain.steps[0].config == {}

    def test_add_step_validates_name(self):
        """Test that add_step validates step name."""
        chain = AnalysisChain()
        analysis = MockAnalysis()

        with pytest.raises(ValueError, match="Step name cannot be empty"):
            chain.add_step("", analysis)

        with pytest.raises(ValueError, match="Step name cannot be empty"):
            chain.add_step(None, analysis)

    def test_add_step_prevents_duplicate_names(self):
        """Test that add_step prevents duplicate step names."""
        chain = AnalysisChain()
        analysis = MockAnalysis()

        chain.add_step("step1", analysis)

        with pytest.raises(ValueError, match="Step 'step1' already exists"):
            chain.add_step("step1", analysis)

    def test_run_single_step(self, sample_model):
        """Test running a chain with a single step."""
        chain = AnalysisChain()
        analysis = MockAnalysis("test_analysis", result_data={"value": 100})

        chain.add_step("step1", analysis)
        result = chain.run(sample_model)

        assert isinstance(result, ChainResult)
        assert result.success is True
        assert "step1" in result.results
        assert result.results["step1"]["value"] == 100

    def test_run_multiple_steps(self, sample_model):
        """Test running a chain with multiple steps."""
        chain = AnalysisChain()
        analysis1 = MockAnalysis("analysis1", result_data={"id": 1})
        analysis2 = MockAnalysis("analysis2", result_data={"id": 2})

        chain.add_step("step1", analysis1).add_step("step2", analysis2)
        result = chain.run(sample_model)

        assert result.success is True
        assert len(result.results) == 2
        assert result.results["step1"]["id"] == 1
        assert result.results["step2"]["id"] == 2

    def test_run_passes_config(self, sample_model):
        """Test that run passes config to each analysis."""
        chain = AnalysisChain()
        analysis = MockAnalysis()

        chain.add_step("step1", analysis, {"custom": "value"})
        result = chain.run(sample_model)

        assert result.results["step1"]["config"]["custom"] == "value"

    def test_run_context_sharing(self, sample_model):
        """Test that context is shared between chain steps."""
        chain = AnalysisChain()
        analysis1 = MockAnalysis("first")
        analysis2 = ContextDependentAnalysis("second")

        chain.add_step("first", analysis1).add_step("second", analysis2)
        result = chain.run(sample_model)

        # Second step should see results from first step
        assert result.results["second"]["previous_count"] == 1

    def test_run_step_failure(self, sample_model):
        """Test chain behavior when a step fails."""
        chain = AnalysisChain()
        analysis1 = MockAnalysis("good")
        analysis2 = FailingAnalysis("bad")
        analysis3 = MockAnalysis("skipped")

        chain.add_step("good", analysis1)
        chain.add_step("bad", analysis2)
        chain.add_step("skipped", analysis3)

        result = chain.run(sample_model)

        assert result.success is False
        assert "good" in result.results
        assert "error" in result.results
        assert result.results["error"]["step"] == "bad"
        assert "skipped" not in result.results

    def test_run_continue_on_error(self, sample_model):
        """Test chain with continue_on_error=True."""
        chain = AnalysisChain(continue_on_error=True)
        analysis1 = MockAnalysis("good")
        analysis2 = FailingAnalysis("bad")
        analysis3 = MockAnalysis("continues")

        chain.add_step("good", analysis1)
        chain.add_step("bad", analysis2)
        chain.add_step("continues", analysis3)

        result = chain.run(sample_model)

        assert result.success is False  # Overall failure
        assert "good" in result.results
        assert "continues" in result.results  # Continues after error

    def test_run_with_initial_context(self, sample_model):
        """Test running with initial context."""
        chain = AnalysisChain()
        analysis = ContextDependentAnalysis()

        chain.add_step("step1", analysis)
        initial_context = {"external": "data"}
        result = chain.run(sample_model, context=initial_context)

        # Context is passed in config, result contains the analysis output
        assert result.results["step1"]["previous_count"] == 0  # No previous results
        assert "depends_on" in result.results["step1"]

    def test_empty_chain_run(self, sample_model):
        """Test running an empty chain."""
        chain = AnalysisChain()
        result = chain.run(sample_model)

        assert result.success is True
        assert result.results == {}

    def test_chain_result_properties(self, sample_model):
        """Test ChainResult properties."""
        chain = AnalysisChain()
        analysis = MockAnalysis()

        chain.add_step("step1", analysis)
        result = chain.run(sample_model)

        assert result.step_count == 1
        assert result.completed_steps == ["step1"]
        assert result.failed_step is None

    def test_chain_result_with_failure(self, sample_model):
        """Test ChainResult properties with failure."""
        chain = AnalysisChain()
        chain.add_step("fails", FailingAnalysis())

        result = chain.run(sample_model)

        # With only one step that fails, step_count is 0 (no completed steps)
        # because the error entry doesn't count as a completed step
        assert result.step_count == 0
        assert result.completed_steps == []
        assert result.failed_step == "fails"

    def test_chain_iteration(self):
        """Test that chain is iterable."""
        chain = AnalysisChain()
        analysis1 = MockAnalysis("a1")
        analysis2 = MockAnalysis("a2")

        chain.add_step("step1", analysis1).add_step("step2", analysis2)

        steps = list(chain)
        assert len(steps) == 2
        assert steps[0].name == "step1"
        assert steps[1].name == "step2"

    def test_chain_length(self):
        """Test len() on chain."""
        chain = AnalysisChain()
        assert len(chain) == 0

        chain.add_step("step1", MockAnalysis())
        assert len(chain) == 1

        chain.add_step("step2", MockAnalysis())
        assert len(chain) == 2

    def test_chain_str(self):
        """Test string representation."""
        chain = AnalysisChain("my_chain")
        chain.add_step("step1", MockAnalysis())

        str_repr = str(chain)
        assert "my_chain" in str_repr
        assert "1 step" in str_repr


# =============================================================================
# AnalysisPipeline Tests
# =============================================================================


class TestAnalysisPipeline:
    """Test suite for AnalysisPipeline."""

    def test_pipeline_creation(self):
        """Test creating an empty pipeline."""
        pipeline = AnalysisPipeline()
        assert pipeline.name is None
        assert len(pipeline.analyses) == 0

    def test_pipeline_with_name(self):
        """Test creating a named pipeline."""
        pipeline = AnalysisPipeline(name="test_pipeline")
        assert pipeline.name == "test_pipeline"

    def test_add_analysis_returns_self(self):
        """Test that add_analysis returns pipeline for fluent interface."""
        pipeline = AnalysisPipeline()
        analysis = MockAnalysis()

        result = pipeline.add_analysis("analysis1", analysis)

        assert result is pipeline
        assert len(pipeline.analyses) == 1

    def test_add_analysis_stores_config(self):
        """Test that add_analysis stores analysis and config."""
        pipeline = AnalysisPipeline()
        analysis = MockAnalysis()
        config = {"param1": "value1"}

        pipeline.add_analysis("analysis1", analysis, config)

        assert pipeline.analyses[0].name == "analysis1"
        assert pipeline.analyses[0].analysis is analysis
        assert pipeline.analyses[0].config == config

    def test_add_analysis_validates_name(self):
        """Test that add_analysis validates analysis name."""
        pipeline = AnalysisPipeline()
        analysis = MockAnalysis()

        with pytest.raises(ValueError, match="Analysis name cannot be empty"):
            pipeline.add_analysis("", analysis)

    def test_add_analysis_prevents_duplicates(self):
        """Test that add_analysis prevents duplicate names."""
        pipeline = AnalysisPipeline()
        analysis = MockAnalysis()

        pipeline.add_analysis("a1", analysis)

        with pytest.raises(ValueError, match="Analysis 'a1' already exists"):
            pipeline.add_analysis("a1", analysis)

    def test_run_single_analysis(self, sample_model):
        """Test running a pipeline with single analysis."""
        pipeline = AnalysisPipeline()
        analysis = MockAnalysis("test", result_data={"value": 100})

        pipeline.add_analysis("analysis1", analysis)
        result = pipeline.run(sample_model)

        assert isinstance(result, PipelineResult)
        assert result.success is True
        assert "analysis1" in result.results

    def test_run_multiple_analyses(self, sample_model):
        """Test running multiple analyses in parallel."""
        pipeline = AnalysisPipeline()
        analysis1 = MockAnalysis("a1", result_data={"id": 1})
        analysis2 = MockAnalysis("a2", result_data={"id": 2})
        analysis3 = MockAnalysis("a3", result_data={"id": 3})

        pipeline.add_analysis("a1", analysis1)
        pipeline.add_analysis("a2", analysis2)
        pipeline.add_analysis("a3", analysis3)

        result = pipeline.run(sample_model)

        assert result.success is True
        assert len(result.results) == 3
        assert result.results["a1"]["id"] == 1
        assert result.results["a2"]["id"] == 2
        assert result.results["a3"]["id"] == 3

    def test_run_parallel_execution(self, sample_model):
        """Test that analyses run in parallel (faster than sequential)."""
        pipeline = AnalysisPipeline()

        # Each analysis takes 0.1s
        analysis1 = MockAnalysis("a1", delay=0.1)
        analysis2 = MockAnalysis("a2", delay=0.1)
        analysis3 = MockAnalysis("a3", delay=0.1)

        pipeline.add_analysis("a1", analysis1)
        pipeline.add_analysis("a2", analysis2)
        pipeline.add_analysis("a3", analysis3)

        start = time.time()
        result = pipeline.run(sample_model)
        elapsed = time.time() - start

        assert result.success is True
        # Parallel execution should take ~0.1s, not 0.3s
        assert elapsed < 0.25, f"Expected parallel execution < 0.25s, took {elapsed}s"

    def test_run_partial_failure(self, sample_model):
        """Test pipeline with some failing analyses."""
        pipeline = AnalysisPipeline()

        pipeline.add_analysis("good", MockAnalysis("good"))
        pipeline.add_analysis("bad", FailingAnalysis("bad"))
        pipeline.add_analysis("also_good", MockAnalysis("also_good"))

        result = pipeline.run(sample_model)

        assert result.success is False  # Overall failure
        assert "good" in result.results
        assert "also_good" in result.results
        assert "errors" in result.results
        assert len(result.results["errors"]) == 1
        assert result.results["errors"][0]["analysis"] == "bad"

    def test_run_all_fail(self, sample_model):
        """Test pipeline when all analyses fail."""
        pipeline = AnalysisPipeline()

        pipeline.add_analysis("fails1", FailingAnalysis("f1"))
        pipeline.add_analysis("fails2", FailingAnalysis("f2"))

        result = pipeline.run(sample_model)

        assert result.success is False
        assert len(result.results["errors"]) == 2

    def test_run_with_max_workers(self, sample_model):
        """Test pipeline with custom max_workers."""
        pipeline = AnalysisPipeline(max_workers=2)
        analysis = MockAnalysis()

        pipeline.add_analysis("a1", analysis)
        pipeline.add_analysis("a2", analysis)

        result = pipeline.run(sample_model)

        assert result.success is True

    def test_empty_pipeline_run(self, sample_model):
        """Test running an empty pipeline."""
        pipeline = AnalysisPipeline()
        result = pipeline.run(sample_model)

        assert result.success is True
        assert result.results == {}

    def test_pipeline_result_properties(self, sample_model):
        """Test PipelineResult properties."""
        pipeline = AnalysisPipeline()
        analysis1 = MockAnalysis("a1")
        analysis2 = MockAnalysis("a2")

        pipeline.add_analysis("a1", analysis1)
        pipeline.add_analysis("a2", analysis2)

        result = pipeline.run(sample_model)

        assert result.analysis_count == 2
        assert result.successful_count == 2
        assert result.failed_count == 0
        assert result.successful_analyses == ["a1", "a2"]

    def test_pipeline_result_with_failures(self, sample_model):
        """Test PipelineResult properties with failures."""
        pipeline = AnalysisPipeline()

        pipeline.add_analysis("good", MockAnalysis())
        pipeline.add_analysis("bad", FailingAnalysis())

        result = pipeline.run(sample_model)

        # analysis_count = successful_count + failed_count
        assert result.successful_count == 1
        assert result.failed_count == 1
        assert result.successful_analyses == ["good"]
        assert result.failed_analyses == ["bad"]

    def test_pipeline_iteration(self):
        """Test that pipeline is iterable."""
        pipeline = AnalysisPipeline()
        analysis1 = MockAnalysis("a1")
        analysis2 = MockAnalysis("a2")

        pipeline.add_analysis("a1", analysis1).add_analysis("a2", analysis2)

        analyses = list(pipeline)
        assert len(analyses) == 2
        assert analyses[0].name == "a1"
        assert analyses[1].name == "a2"

    def test_pipeline_length(self):
        """Test len() on pipeline."""
        pipeline = AnalysisPipeline()
        assert len(pipeline) == 0

        pipeline.add_analysis("a1", MockAnalysis())
        assert len(pipeline) == 1

        pipeline.add_analysis("a2", MockAnalysis())
        assert len(pipeline) == 2

    def test_pipeline_str(self):
        """Test string representation."""
        pipeline = AnalysisPipeline("my_pipeline")
        pipeline.add_analysis("a1", MockAnalysis())

        str_repr = str(pipeline)
        assert "my_pipeline" in str_repr
        assert "1 analysis" in str_repr


# =============================================================================
# Integration Tests
# =============================================================================


class TestWorkflowIntegration:
    """Integration tests for chain and pipeline together."""

    def test_chain_then_pipeline(self, sample_model):
        """Test using chain results as pipeline input."""
        # First, run a chain
        chain = AnalysisChain("preprocessing")
        chain.add_step("validate", MockAnalysis("validate", result_data={"valid": True}))
        chain.add_step("prepare", MockAnalysis("prepare", result_data={"prepared": True}))

        chain_result = chain.run(sample_model)
        assert chain_result.success is True

        # Then run pipeline on same model
        pipeline = AnalysisPipeline("parallel_analysis")
        pipeline.add_analysis("analyze1", MockAnalysis("a1"))
        pipeline.add_analysis("analyze2", MockAnalysis("a2"))

        pipeline_result = pipeline.run(sample_model)
        assert pipeline_result.success is True

    def test_pipeline_then_chain(self, sample_model):
        """Test using pipeline results in chain."""
        # First run pipeline
        pipeline = AnalysisPipeline("initial")
        pipeline.add_analysis("quick1", MockAnalysis())
        pipeline.add_analysis("quick2", MockAnalysis())

        pipeline_result = pipeline.run(sample_model)
        assert pipeline_result.success is True

        # Then run chain with context from pipeline
        chain = AnalysisChain("sequential")
        chain.add_step("step1", MockAnalysis())

        # Pass pipeline results as initial context
        context = {"pipeline_results": pipeline_result.results}
        chain_result = chain.run(sample_model, context=context)

        assert chain_result.success is True

    def test_nested_workflows(self, sample_model):
        """Test that chains and pipelines can be nested logically."""
        # Create multiple chains
        chain1 = AnalysisChain("chain1")
        chain1.add_step("c1_step", MockAnalysis())

        chain2 = AnalysisChain("chain2")
        chain2.add_step("c2_step", MockAnalysis())

        # Run both (sequentially)
        result1 = chain1.run(sample_model)
        result2 = chain2.run(sample_model)

        assert result1.success and result2.success

        # Create pipeline with analyses that use chain results
        pipeline = AnalysisPipeline("final")
        pipeline.add_analysis("final1", MockAnalysis())

        pipeline_result = pipeline.run(sample_model)
        assert pipeline_result.success is True


# =============================================================================
# Error Handling Tests
# =============================================================================


class TestErrorHandling:
    """Test error handling in workflows."""

    def test_chain_exception_handling(self, sample_model):
        """Test chain properly handles exceptions."""
        chain = AnalysisChain()
        chain.add_step("fails", FailingAnalysis())

        result = chain.run(sample_model)

        assert result.success is False
        assert "error" in result.results
        assert "exception" in result.results["error"]
        assert "message" in result.results["error"]

    def test_pipeline_exception_handling(self, sample_model):
        """Test pipeline properly handles exceptions."""
        pipeline = AnalysisPipeline()
        pipeline.add_analysis("fails", FailingAnalysis())

        result = pipeline.run(sample_model)

        assert result.success is False
        assert "errors" in result.results
        assert len(result.results["errors"]) == 1

    def test_chain_preserves_logs(self, sample_model):
        """Test chain preserves logs from analyses."""
        chain = AnalysisChain()

        class LoggingAnalysis(PowerAnalysis):
            def run(self, model: PowerSystemModel, config: dict) -> dict:
                return {"log": "test message"}

        chain.add_step("logging", LoggingAnalysis())
        result = chain.run(sample_model)

        assert result.results["logging"]["log"] == "test message"

    def test_chain_invalid_model(self):
        """Test chain with invalid model."""
        chain = AnalysisChain()
        chain.add_step("step1", MockAnalysis())

        # Empty model should fail validation
        empty_model = PowerSystemModel()
        result = chain.run(empty_model)

        assert result.success is False
