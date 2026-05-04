# CloudPSS SkillHub V2 Examples

This directory contains end-to-end examples demonstrating the CloudPSS SkillHub V2 API usage patterns, including CLI operations, analysis chaining, and workflow context sharing.

## Files

- `cli_workflow_example.py` - Complete CLI and workflow examples

## Quick Start

```bash
# Run all examples
python cli_workflow_example.py

# Run specific example
python cli_workflow_example.py --example 1
python cli_workflow_example.py --example 2
python cli_workflow_example.py --example 3

# List available examples
python cli_workflow_example.py --list
```

## Examples Overview

### Example 1: Basic CLI Usage

Demonstrates CLI-style command patterns for common operations.

**Features:**
- Command pattern implementation
- Configuration initialization
- Running simulations
- Listing available skills
- Validating configurations

**Usage:**
```bash
python cli_workflow_example.py --example 1
```

**Code Snippet:**
```python
from cloudpss_skills_v2.examples.cli_workflow_example import CLICommand

# Create CLI commands
commands = [
    CLICommand("list", args={}, options={"verbose": False}),
    CLICommand("init", args={"skill": "power_flow", "output": "pf_config.yaml"}),
    CLICommand("validate", args={"config": "pf_config.yaml"}),
    CLICommand("run", args={"config": "pf_config.yaml"}, options={"output": "./results"}),
]

# Execute commands
for cmd in commands:
    result = cmd.execute()
    print(f"Result: {result}")
```

### Example 2: Analysis Chain

Shows how to chain multiple analyses together with dependency management.

**Features:**
- Multi-step analysis chains
- Dependency management between steps
- Context passing between analyses
- Result aggregation

**Workflow:**
```
Base Power Flow
    ↓
Voltage Analysis (depends on power flow)
    ↓
Thermal Analysis (depends on power flow)
    ↓
N-1 Security (depends on voltage and thermal)
```

**Usage:**
```bash
python cli_workflow_example.py --example 2
```

**Code Snippet:**
```python
from cloudpss_skills_v2.examples.cli_workflow_example import AnalysisChain, AnalysisStep

# Create analysis chain
chain = AnalysisChain("Power System Security Assessment")

# Add steps with dependencies
chain.add_step(AnalysisStep(
    name="base_power_flow",
    skill="power_flow",
    config={"algorithm": "newton_raphson"},
))

chain.add_step(AnalysisStep(
    name="voltage_analysis",
    skill="voltage_profile",
    config={"check_limits": True},
    depends_on=["base_power_flow"],
))

chain.add_step(AnalysisStep(
    name="n1_security",
    skill="n1_security",
    config={"contingency_filter": "all_branches"},
    depends_on=["voltage_analysis", "thermal_analysis"],
))

# Execute chain
result = chain.execute()
```

### Example 3: Workflow with Context Sharing

Demonstrates a complete workflow with shared context between steps.

**Features:**
- Workflow pattern with multiple steps
- Shared context between steps
- State management across execution
- Report generation

**Workflow Steps:**
1. **Model Load** - Load or create power system model
2. **Configure** - Set up analysis configuration
3. **Run Simulation** - Execute simulation
4. **Analyze Results** - Process and analyze output
5. **Generate Report** - Create summary report

**Usage:**
```bash
python cli_workflow_example.py --example 3
```

**Code Snippet:**
```python
from cloudpss_skills_v2.examples.cli_workflow_example import (
    Workflow, ModelLoadStep, ConfigureStep,
    RunSimulationStep, AnalyzeResultsStep, GenerateReportStep
)

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

# Access context data
context = result['context']
report = context['data']['report']
```

## Helper Functions

### create_test_model()

Creates a simple test power system model for examples.

```python
from cloudpss_skills_v2.examples.cli_workflow_example import create_test_model

model = create_test_model("My Test System")
print(f"Buses: {len(model.buses)}")
print(f"Branches: {len(model.branches)}")
```

**Returns:**
- `PowerSystemModel` with 5 buses, 5 branches, 3 generators, and 2 loads

### Voltage Stability Evidence Modes

`voltage_stability` defaults to a fast screening proxy. For an AC power-flow
validation scan, pass `method: "pandapower_ac"` when running on a unified
`PowerSystemModel`:

```python
from cloudpss_skills_v2.poweranalysis.voltage_stability import VoltageStabilityAnalysis

result = VoltageStabilityAnalysis().run(model, {
    "method": "pandapower_ac",
    "load_scaling": [1.0, 1.2, 1.4],
    "monitor_buses": ["Load"],
})

assert result["analysis_mode"] == "pandapower_ac_power_flow_scan"
```

This mode uses repeated pandapower AC `runpp` calculations. It is stronger than
the default screening estimate, but it is still a discrete load-scaling scan and
not a continuous CPF solver.

## Architecture Patterns

### Command Pattern (Example 1)

The CLI example uses the Command pattern to encapsulate operations:

```python
@dataclass
class CLICommand:
    command: str
    args: dict[str, Any]
    options: dict[str, Any]

    def execute(self) -> dict:
        # Command execution logic
        return result
```

### Chain of Responsibility (Example 2)

The analysis chain uses dependency-based execution:

```python
class AnalysisChain:
    def add_step(self, step: AnalysisStep) -> "AnalysisChain":
        self.steps.append(step)
        return self

    def execute(self) -> dict:
        for step in self.steps:
            # Check dependencies
            # Execute step
            # Update context
```

### Workflow Pattern (Example 3)

The workflow example demonstrates stateful execution:

```python
class Workflow:
    def __init__(self, name: str):
        self.context = WorkflowContext.create()
        self.steps = []

    def execute(self) -> dict:
        for step in self.steps:
            result = step.execute(self.context)
            # Context is shared across all steps
```

## Integration with Core API

All examples integrate with the CloudPSS SkillHub V2 core API:

```python
from cloudpss_skills_v2.core import (
    PowerSystemModel,
    Bus, Branch, Generator, Load,
    ConfigStore, BaseConfig, ProjectConfig, StudyConfig,
    ResultArchive,
)

from cloudpss_skills_v2.powerapi import (
    EngineAdapter,
    EngineConfig,
    SimulationStatus,
    SimulationType,
    SimulationResult,
)
```

## Customization

### Creating Custom Workflow Steps

```python
from cloudpss_skills_v2.examples.cli_workflow_example import WorkflowStep, WorkflowContext

class CustomStep(WorkflowStep):
    def execute(self, context: WorkflowContext) -> dict:
        # Access context data
        model = context.get("model")

        # Perform custom logic
        result = {"custom_data": "value"}

        # Store in context
        context.set("custom_result", result)

        return {"step": self.name, "status": "success"}
```

### Creating Custom Analysis Steps

```python
from cloudpss_skills_v2.examples.cli_workflow_example import AnalysisStep

class MyAnalysisStep(AnalysisStep):
    def run(self, context: dict) -> dict:
        # Access dependency results
        dep_result = context.get("previous_step")

        # Execute analysis
        result = super().run(context)

        # Add custom metrics
        result["custom_metric"] = 42

        return result
```

## Testing

Run examples as part of your test suite:

```python
import unittest
from cloudpss_skills_v2.examples.cli_workflow_example import (
    example_1_basic_cli,
    example_2_analysis_chain,
    example_3_workflow_with_context,
)

class TestExamples(unittest.TestCase):
    def test_example_1(self):
        results = example_1_basic_cli()
        self.assertEqual(len(results), 4)
        self.assertTrue(all(r.get("success") for r in results))

    def test_example_2(self):
        result = example_2_analysis_chain()
        self.assertEqual(result["steps_completed"], 4)
        self.assertIn("base_power_flow", result["context_keys"])

    def test_example_3(self):
        result = example_3_workflow_with_context()
        self.assertTrue(result["all_success"])
        self.assertIn("report", result["context"]["data"])
```

## Further Reading

- [Core API Documentation](../docs/)
- [PowerAPI Reference](../powerapi/)
- [PowerSkill Guide](../powerskill/)
