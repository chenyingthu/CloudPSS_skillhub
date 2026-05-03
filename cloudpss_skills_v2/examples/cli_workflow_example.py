#!/usr/bin/env python3
"""
CloudPSS SkillHub V2 - CLI and Workflow Examples

This module demonstrates end-to-end usage of the CloudPSS SkillHub V2 API,
including CLI-style operations, analysis chaining, and workflow context sharing.

Examples:
    - Example 1: Basic CLI usage with command patterns
    - Example 2: Analysis chain (Power Flow -> N-1 Security)
    - Example 3: Workflow with shared context between steps

Usage:
    python cli_workflow_example.py              # Run all examples
    python cli_workflow_example.py --example 1  # Run specific example
    python cli_workflow_example.py --list       # List available examples
"""

from __future__ import annotations

import argparse
import sys
import tempfile
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from cloudpss_skills_v2.core import (
    Bus,
    Branch,
    Generator,
    Load,
    PowerSystemModel,
    ConfigStore,
    BaseConfig,
    ProjectConfig,
    StudyConfig,
    ResultArchive,
)
from cloudpss_skills_v2.powerapi import (
    SimulationStatus,
    SimulationType,
    ValidationResult,
    EngineAdapter,
    EngineConfig,
)


# =============================================================================
# Helper Functions
# =============================================================================

def create_test_model(name: str = "Test System") -> PowerSystemModel:
    """
    Create a simple test power system model for examples.

    Returns:
        PowerSystemModel with 5 buses, 5 branches, 3 generators, and 2 loads.
    """
    buses = [
        Bus(bus_id=1, name="Bus 1", base_kv=69.0, bus_type="SLACK",
            v_magnitude_pu=1.060, v_angle_degree=0.0,
            p_injected_mw=232.4, q_injected_mvar=-16.9,
            vm_max_pu=1.1, vm_min_pu=0.9),
        Bus(bus_id=2, name="Bus 2", base_kv=69.0, bus_type="PV",
            v_magnitude_pu=1.045, p_injected_mw=40.0,
            vm_max_pu=1.1, vm_min_pu=0.9),
        Bus(bus_id=3, name="Bus 3", base_kv=69.0, bus_type="PV",
            v_magnitude_pu=1.010, p_injected_mw=0.0,
            vm_max_pu=1.1, vm_min_pu=0.9),
        Bus(bus_id=4, name="Bus 4", base_kv=69.0, bus_type="PQ",
            p_injected_mw=-47.8, q_injected_mvar=-3.9),
        Bus(bus_id=5, name="Bus 5", base_kv=69.0, bus_type="PQ",
            p_injected_mw=-7.6, q_injected_mvar=-1.6),
    ]

    branches = [
        Branch(from_bus=1, to_bus=2, name="Line 1-2",
               r_pu=0.01938, x_pu=0.05917, rate_a_mva=100.0),
        Branch(from_bus=1, to_bus=5, name="Line 1-5",
               r_pu=0.05403, x_pu=0.22304, rate_a_mva=80.0),
        Branch(from_bus=2, to_bus=3, name="Line 2-3",
               r_pu=0.04699, x_pu=0.19797, rate_a_mva=80.0),
        Branch(from_bus=2, to_bus=4, name="Line 2-4",
               r_pu=0.05811, x_pu=0.17632, rate_a_mva=60.0),
        Branch(from_bus=2, to_bus=5, name="Line 2-5",
               r_pu=0.05695, x_pu=0.17388, rate_a_mva=60.0),
    ]

    generators = [
        Generator(bus_id=1, name="Gen 1", p_gen_mw=232.4,
                  q_gen_mvar=-16.9, p_max_mw=500.0, p_min_mw=0.0),
        Generator(bus_id=2, name="Gen 2", p_gen_mw=40.0,
                  q_gen_mvar=50.0, p_max_mw=200.0, p_min_mw=0.0),
        Generator(bus_id=3, name="Gen 3", p_gen_mw=0.0,
                  q_gen_mvar=40.0, p_max_mw=150.0, p_min_mw=0.0),
    ]

    loads = [
        Load(bus_id=4, name="Load 4", p_mw=47.8, q_mvar=3.9),
        Load(bus_id=5, name="Load 5", p_mw=7.6, q_mvar=1.6),
    ]

    return PowerSystemModel(
        buses=buses,
        branches=branches,
        generators=generators,
        loads=loads,
        base_mva=100.0,
        name=name,
        source_engine="demo"
    )


# =============================================================================
# Example 1: Basic CLI Usage
# =============================================================================

@dataclass
class CLICommand:
    """Represents a CLI command with arguments and options."""
    command: str
    args: dict[str, Any] = field(default_factory=dict)
    options: dict[str, Any] = field(default_factory=dict)

    def execute(self) -> dict[str, Any]:
        """Execute the command and return results."""
        print(f"\n  Executing: {self.command}")
        print(f"    Args: {self.args}")
        print(f"    Options: {self.options}")

        # Simulate command execution
        result = {
            "command": self.command,
            "success": True,
            "timestamp": datetime.now().isoformat(),
        }

        if self.command == "run":
            result["job_id"] = f"job_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            result["status"] = "completed"
        elif self.command == "list":
            result["items"] = ["power_flow", "n1_security", "short_circuit", "emt"]
        elif self.command == "init":
            result["config_path"] = self.args.get("output", "./config.yaml")
        elif self.command == "validate":
            result["valid"] = True
            result["errors"] = []

        return result


def example_1_basic_cli():
    """
    Example 1: Basic CLI Usage Patterns

    Demonstrates:
        - Command pattern for CLI operations
        - Configuration initialization
        - Running simulations
        - Listing available skills
        - Validating configurations
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Basic CLI Usage")
    print("=" * 70)

    # Simulate CLI commands
    commands = [
        # cloudpss-skills list
        CLICommand("list", args={}, options={"verbose": False}),

        # cloudpss-skills init power_flow --output pf_config.yaml
        CLICommand("init", args={"skill": "power_flow", "output": "pf_config.yaml"},
                   options={"engine": "cloudpss"}),

        # cloudpss-skills validate --config pf_config.yaml
        CLICommand("validate", args={"config": "pf_config.yaml"},
                   options={"strict": True}),

        # cloudpss-skills run --config pf_config.yaml --output ./results
        CLICommand("run", args={"config": "pf_config.yaml"},
                   options={"output": "./results", "format": "json"}),
    ]

    results = []
    for cmd in commands:
        result = cmd.execute()
        results.append(result)
        print(f"    Result: {result}")

    print("\n  Summary:")
    print(f"    Commands executed: {len(results)}")
    print(f"    Successful: {sum(1 for r in results if r.get('success'))}")

    return results


# =============================================================================
# Example 2: Analysis Chain
# =============================================================================

@dataclass
class AnalysisStep:
    """Represents a single step in an analysis chain."""
    name: str
    skill: str
    config: dict[str, Any]
    depends_on: list[str] = field(default_factory=list)
    result: Optional[dict] = None

    def run(self, context: dict) -> dict:
        """Execute this analysis step with the given context."""
        print(f"\n  Step: {self.name}")
        print(f"    Skill: {self.skill}")
        print(f"    Dependencies: {self.depends_on}")

        # Merge context into config
        merged_config = {**self.config}
        for dep in self.depends_on:
            if dep in context:
                merged_config[f"{dep}_result"] = context[dep]

        # Simulate execution
        self.result = {
            "step": self.name,
            "skill": self.skill,
            "status": "completed",
            "timestamp": datetime.now().isoformat(),
            "metrics": self._generate_metrics(),
        }

        print(f"    Status: {self.result['status']}")
        print(f"    Metrics: {self.result['metrics']}")

        return self.result

    def _generate_metrics(self) -> dict:
        """Generate simulated metrics for this step."""
        import random
        return {
            "execution_time": round(random.uniform(0.5, 5.0), 2),
            "memory_usage_mb": round(random.uniform(50, 500), 1),
        }


class AnalysisChain:
    """Manages a chain of analysis steps."""

    def __init__(self, name: str):
        self.name = name
        self.steps: list[AnalysisStep] = []
        self.context: dict = {}

    def add_step(self, step: AnalysisStep) -> "AnalysisChain":
        """Add a step to the chain."""
        self.steps.append(step)
        return self

    def execute(self) -> dict:
        """Execute all steps in the chain."""
        print(f"\n  Executing chain: {self.name}")
        print(f"  Total steps: {len(self.steps)}")

        results = []
        for step in self.steps:
            # Check dependencies
            missing_deps = [d for d in step.depends_on if d not in self.context]
            if missing_deps:
                raise ValueError(f"Missing dependencies: {missing_deps}")

            # Execute step
            result = step.run(self.context)
            results.append(result)

            # Update context
            self.context[step.name] = result

        return {
            "chain_name": self.name,
            "steps_completed": len(results),
            "context_keys": list(self.context.keys()),
            "results": results,
        }


def example_2_analysis_chain():
    """
    Example 2: Analysis Chain (Power Flow -> N-1 Security)

    Demonstrates:
        - Chaining multiple analyses together
        - Dependency management between steps
        - Context passing between analyses
        - Result aggregation
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Analysis Chain")
    print("=" * 70)

    # Create a test model
    model = create_test_model("IEEE 14-Bus Test System")
    print(f"\n  Model: {model.name}")
    print(f"    Buses: {len(model.buses)}")
    print(f"    Branches: {len(model.branches)}")

    # Create analysis chain
    chain = AnalysisChain("Power System Security Assessment")

    # Step 1: Base Case Power Flow
    chain.add_step(AnalysisStep(
        name="base_power_flow",
        skill="power_flow",
        config={
            "model": model,
            "algorithm": "newton_raphson",
            "tolerance": 1e-6,
        },
    ))

    # Step 2: Voltage Analysis (depends on power flow)
    chain.add_step(AnalysisStep(
        name="voltage_analysis",
        skill="voltage_profile",
        config={
            "check_limits": True,
            "v_min": 0.95,
            "v_max": 1.05,
        },
        depends_on=["base_power_flow"],
    ))

    # Step 3: Thermal Loading Analysis (depends on power flow)
    chain.add_step(AnalysisStep(
        name="thermal_analysis",
        skill="thermal_loading",
        config={
            "check_limits": True,
            "thermal_limit": 1.0,
        },
        depends_on=["base_power_flow"],
    ))

    # Step 4: N-1 Security Analysis (depends on voltage and thermal)
    chain.add_step(AnalysisStep(
        name="n1_security",
        skill="n1_security",
        config={
            "contingency_filter": "all_branches",
            "voltage_threshold": 0.05,
        },
        depends_on=["voltage_analysis", "thermal_analysis"],
    ))

    # Execute the chain
    result = chain.execute()

    print("\n  Chain Results:")
    print(f"    Chain: {result['chain_name']}")
    print(f"    Steps completed: {result['steps_completed']}")
    print(f"    Context keys: {result['context_keys']}")

    return result


# =============================================================================
# Example 3: Workflow with Context Sharing
# =============================================================================

@dataclass
class WorkflowContext:
    """Shared context for workflow steps."""
    workflow_id: str
    created_at: datetime
    data: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(cls) -> "WorkflowContext":
        """Create a new workflow context."""
        return cls(
            workflow_id=f"wf_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            created_at=datetime.now(),
        )

    def set(self, key: str, value: Any) -> None:
        """Set a value in the context."""
        self.data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the context."""
        return self.data.get(key, default)

    def to_dict(self) -> dict:
        """Convert context to dictionary."""
        return {
            "workflow_id": self.workflow_id,
            "created_at": self.created_at.isoformat(),
            "data": self.data,
            "metadata": self.metadata,
        }


class WorkflowStep:
    """Base class for workflow steps."""

    def __init__(self, name: str):
        self.name = name

    def execute(self, context: WorkflowContext) -> dict:
        """Execute this step with the given context."""
        raise NotImplementedError


class ModelLoadStep(WorkflowStep):
    """Step to load a power system model."""

    def execute(self, context: WorkflowContext) -> dict:
        print(f"\n  [{self.name}] Loading model...")

        # Load or create model
        model = create_test_model("Workflow Test Model")

        # Store in context
        context.set("model", model)
        context.set("model_name", model.name)

        return {
            "step": self.name,
            "status": "success",
            "model_name": model.name,
            "buses": len(model.buses),
            "branches": len(model.branches),
        }


class ConfigureStep(WorkflowStep):
    """Step to configure the analysis."""

    def execute(self, context: WorkflowContext) -> dict:
        print(f"\n  [{self.name}] Configuring analysis...")

        # Get model from context
        model = context.get("model")
        if not model:
            return {"step": self.name, "status": "error", "error": "No model in context"}

        # Create configuration
        config = {
            "model_name": model.name,
            "analysis_type": "power_flow",
            "engine": "cloudpss",
            "parameters": {
                "tolerance": 1e-6,
                "max_iterations": 100,
            },
        }

        # Store in context
        context.set("config", config)

        return {
            "step": self.name,
            "status": "success",
            "config": config,
        }


class RunSimulationStep(WorkflowStep):
    """Step to run a simulation."""

    def execute(self, context: WorkflowContext) -> dict:
        print(f"\n  [{self.name}] Running simulation...")

        # Get config from context
        config = context.get("config")
        if not config:
            return {"step": self.name, "status": "error", "error": "No config in context"}

        # Simulate simulation
        import random
        result = {
            "job_id": f"sim_{datetime.now().strftime('%H%M%S')}",
            "status": "completed",
            "converged": True,
            "iterations": random.randint(3, 10),
            "execution_time": round(random.uniform(1.0, 10.0), 2),
        }

        # Store in context
        context.set("simulation_result", result)

        return {
            "step": self.name,
            "status": "success",
            "result": result,
        }


class AnalyzeResultsStep(WorkflowStep):
    """Step to analyze simulation results."""

    def execute(self, context: WorkflowContext) -> dict:
        print(f"\n  [{self.name}] Analyzing results...")

        # Get results from context
        sim_result = context.get("simulation_result")
        model = context.get("model")

        if not sim_result or not model:
            return {"step": self.name, "status": "error", "error": "Missing data in context"}

        # Perform analysis
        violations = model.get_voltage_violations()

        analysis = {
            "converged": sim_result.get("converged", False),
            "voltage_violations": len(violations),
            "iterations": sim_result.get("iterations", 0),
            "execution_time": sim_result.get("execution_time", 0),
        }

        # Store in context
        context.set("analysis", analysis)

        return {
            "step": self.name,
            "status": "success",
            "analysis": analysis,
        }


class GenerateReportStep(WorkflowStep):
    """Step to generate a report."""

    def execute(self, context: WorkflowContext) -> dict:
        print(f"\n  [{self.name}] Generating report...")

        # Get all data from context
        model_name = context.get("model_name", "Unknown")
        analysis = context.get("analysis", {})
        config = context.get("config", {})

        # Generate report
        report = {
            "title": f"Analysis Report: {model_name}",
            "generated_at": datetime.now().isoformat(),
            "workflow_id": context.workflow_id,
            "summary": {
                "model": model_name,
                "analysis_type": config.get("analysis_type", "unknown"),
                "converged": analysis.get("converged", False),
                "voltage_violations": analysis.get("voltage_violations", 0),
                "execution_time": analysis.get("execution_time", 0),
            },
        }

        # Store in context
        context.set("report", report)

        return {
            "step": self.name,
            "status": "success",
            "report": report,
        }


class Workflow:
    """Manages a workflow with multiple steps."""

    def __init__(self, name: str):
        self.name = name
        self.steps: list[WorkflowStep] = []
        self.context = WorkflowContext.create()

    def add_step(self, step: WorkflowStep) -> "Workflow":
        """Add a step to the workflow."""
        self.steps.append(step)
        return self

    def execute(self) -> dict:
        """Execute all workflow steps."""
        print(f"\n  Starting workflow: {self.name}")
        print(f"  Workflow ID: {self.context.workflow_id}")
        print(f"  Steps: {len(self.steps)}")

        results = []
        for step in self.steps:
            try:
                result = step.execute(self.context)
                results.append(result)

                if result.get("status") == "error":
                    print(f"    ERROR: {result.get('error')}")
                    break
            except Exception as e:
                print(f"    EXCEPTION: {e}")
                results.append({"step": step.name, "status": "exception", "error": str(e)})
                break

        return {
            "workflow_name": self.name,
            "workflow_id": self.context.workflow_id,
            "steps_completed": len(results),
            "all_success": all(r.get("status") == "success" for r in results),
            "context": self.context.to_dict(),
            "step_results": results,
        }


def example_3_workflow_with_context():
    """
    Example 3: Workflow with Shared Context

    Demonstrates:
        - Workflow pattern with multiple steps
        - Shared context between steps
        - Context passing and data sharing
        - State management across workflow execution
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Workflow with Context Sharing")
    print("=" * 70)

    # Create workflow
    workflow = Workflow("Power System Analysis Workflow")

    # Add steps
    workflow.add_step(ModelLoadStep("load_model"))
    workflow.add_step(ConfigureStep("configure"))
    workflow.add_step(RunSimulationStep("run_simulation"))
    workflow.add_step(AnalyzeResultsStep("analyze"))
    workflow.add_step(GenerateReportStep("generate_report"))

    # Execute workflow
    result = workflow.execute()

    print("\n  Workflow Results:")
    print(f"    Workflow: {result['workflow_name']}")
    print(f"    Workflow ID: {result['workflow_id']}")
    print(f"    Steps completed: {result['steps_completed']}")
    print(f"    All successful: {result['all_success']}")

    print("\n  Context Data Keys:")
    for key in result['context']['data'].keys():
        print(f"    - {key}")

    print("\n  Generated Report:")
    report = result['context']['data'].get('report', {})
    if report:
        print(f"    Title: {report.get('title')}")
        print(f"    Summary: {report.get('summary')}")

    return result


# =============================================================================
# Main Entry Point
# =============================================================================

def run_all_examples():
    """Run all examples."""
    print("\n" + "=" * 70)
    print("CloudPSS SkillHub V2 - CLI and Workflow Examples")
    print("=" * 70)

    results = {
        "example_1": example_1_basic_cli(),
        "example_2": example_2_analysis_chain(),
        "example_3": example_3_workflow_with_context(),
    }

    print("\n" + "=" * 70)
    print("All Examples Completed")
    print("=" * 70)

    for name, result in results.items():
        print(f"\n  {name}:")
        if isinstance(result, list):
            print(f"    Items: {len(result)}")
        elif isinstance(result, dict):
            print(f"    Keys: {list(result.keys())}")

    return results


def main():
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description="CloudPSS SkillHub V2 CLI and Workflow Examples"
    )
    parser.add_argument(
        "--example",
        type=int,
        choices=[1, 2, 3],
        help="Run specific example (1, 2, or 3)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available examples",
    )

    args = parser.parse_args()

    if args.list:
        print("\nAvailable Examples:")
        print("  1 - Basic CLI Usage")
        print("     Demonstrates CLI command patterns")
        print()
        print("  2 - Analysis Chain")
        print("     Chains multiple analyses (Power Flow -> N-1 Security)")
        print()
        print("  3 - Workflow with Context")
        print("     Shares context between workflow steps")
        return 0

    if args.example == 1:
        example_1_basic_cli()
    elif args.example == 2:
        example_2_analysis_chain()
    elif args.example == 3:
        example_3_workflow_with_context()
    else:
        run_all_examples()

    return 0


if __name__ == "__main__":
    exit(main())
