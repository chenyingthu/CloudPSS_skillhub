# Phase 5 CLI and Workflow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add CLI and workflow support for the unified PowerSystemModel architecture, enabling command-line access to all analysis skills.

**Architecture:** CLI module provides commands: list, run, analyze, compare; Workflow module chains multiple analyses.

**Tech Stack:** Python, argparse, PowerSystemModel, PowerAnalysis

---

## File Structure

| File | Responsibility | Action |
|------|---------------|--------|
| `cloudpss_skills_v2/cli/__init__.py` | CLI module init | Create |
| `cloudpss_skills_v2/cli/main.py` | Main CLI entry point | Create |
| `cloudpss_skills_v2/cli/commands/list.py` | List skills command | Create |
| `cloudpss_skills_v2/cli/commands/run.py` | Run analysis command | Create |
| `cloudpss_skills_v2/cli/commands/compare.py` | Compare engines command | Create |
| `cloudpss_skills_v2/workflow/__init__.py` | Workflow module init | Create |
| `cloudpss_skills_v2/workflow/chain.py` | Analysis chaining | Create |
| `cloudpss_skills_v2/workflow/pipeline.py` | Pipeline execution | Create |
| `cloudpss_skills_v2/tests/test_cli.py` | CLI tests | Create |
| `cloudpss_skills_v2/tests/test_workflow.py` | Workflow tests | Create |
| `cloudpss_skills_v2/__main__.py` | Module entry point | Create |

---

## Task 1: Create CLI Module Structure

**Files:**
- Create: `cloudpss_skills_v2/cli/__init__.py`
- Create: `cloudpss_skills_v2/cli/main.py`
- Create: `cloudpss_skills_v2/cli/commands/__init__.py`
- Create: `cloudpss_skills_v2/__main__.py`
- Test: `cloudpss_skills_v2/tests/test_cli.py` (create new)

- [ ] **Step 1: Write failing test for CLI module**

```python
def test_cli_module_exists():
    """Test CLI module can be imported."""
    from cloudpss_skills_v2.cli import main
    assert main is not None

def test_cli_main_function():
    """Test CLI main function exists."""
    from cloudpss_skills_v2.cli.main import main
    assert callable(main)

def test_cli_entry_point():
    """Test CLI entry point works."""
    import subprocess
    result = subprocess.run(
        ["python", "-m", "cloudpss_skills_v2", "--help"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "CloudPSS Skills v2" in result.stdout
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest cloudpss_skills_v2/tests/test_cli.py -v
```

- [ ] **Step 3: Create CLI module**

In `cloudpss_skills_v2/cli/__init__.py`:
```python
"""CloudPSS Skills v2 - CLI Module.

Command-line interface for power system analysis using unified PowerSystemModel.
"""

from .main import main

__all__ = ["main"]
```

In `cloudpss_skills_v2/cli/main.py`:
```python
"""Main CLI entry point for CloudPSS Skills v2."""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from .commands import list_cmd, run_cmd, compare_cmd


def create_parser() -> argparse.ArgumentParser:
    """Create CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="cloudpss-skills-v2",
        description="CloudPSS Skills v2 - Power System Analysis CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s list                    # List all available skills
  %(prog)s run n1_security         # Run N-1 security analysis
  %(prog)s compare --engines cloudpss,pandapower  # Compare engines
        """
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 2.0.0"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # List command
    list_parser = subparsers.add_parser(
        "list",
        help="List available analysis skills"
    )
    list_parser.add_argument(
        "--type",
        choices=["all", "security", "stability", "powerflow"],
        default="all",
        help="Filter by skill type"
    )
    list_parser.set_defaults(func=list_cmd.execute)
    
    # Run command
    run_parser = subparsers.add_parser(
        "run",
        help="Run an analysis skill"
    )
    run_parser.add_argument(
        "skill",
        help="Skill name to run (e.g., n1_security, voltage_stability)"
    )
    run_parser.add_argument(
        "--model",
        required=True,
        help="Model identifier (e.g., model/holdme/IEEE39)"
    )
    run_parser.add_argument(
        "--engine",
        choices=["cloudpss", "pandapower"],
        default="cloudpss",
        help="Simulation engine to use"
    )
    run_parser.add_argument(
        "--config",
        type=str,
        help="JSON string or path to config file"
    )
    run_parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Output file path"
    )
    run_parser.set_defaults(func=run_cmd.execute)
    
    # Compare command
    compare_parser = subparsers.add_parser(
        "compare",
        help="Compare results from different engines"
    )
    compare_parser.add_argument(
        "--engines",
        required=True,
        help="Comma-separated list of engines (e.g., cloudpss,pandapower)"
    )
    compare_parser.add_argument(
        "--model",
        required=True,
        help="Model identifier"
    )
    compare_parser.add_argument(
        "--analysis",
        default="powerflow",
        help="Analysis type to compare"
    )
    compare_parser.set_defaults(func=compare_cmd.execute)
    
    return parser


def main(args: Optional[List[str]] = None) -> int:
    """Main CLI entry point.
    
    Args:
        args: Command-line arguments (defaults to sys.argv[1:])
        
    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    
    if not parsed_args.command:
        parser.print_help()
        return 0
    
    try:
        return parsed_args.func(parsed_args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

In `cloudpss_skills_v2/__main__.py`:
```python
"""Entry point for running cloudpss_skills_v2 as a module."""

from cloudpss_skills_v2.cli import main

if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Create commands package**

In `cloudpss_skills_v2/cli/commands/__init__.py`:
```python
"""CLI commands package."""

from . import list_cmd
from . import run_cmd
from . import compare_cmd

__all__ = ["list_cmd", "run_cmd", "compare_cmd"]
```

In `cloudpss_skills_v2/cli/commands/list_cmd.py`:
```python
"""List command - show available analysis skills."""

import argparse
import sys
from typing import List

from cloudpss_skills_v2.poweranalysis import (
    N1SecurityAnalysis,
    ParameterSensitivityAnalysis,
    ShortCircuitAnalysis,
    VoltageStabilityAnalysis,
    TransientStabilityAnalysis,
    SmallSignalStabilityAnalysis,
)


SKILL_REGISTRY = {
    "n1_security": N1SecurityAnalysis,
    "parameter_sensitivity": ParameterSensitivityAnalysis,
    "short_circuit": ShortCircuitAnalysis,
    "voltage_stability": VoltageStabilityAnalysis,
    "transient_stability": TransientStabilityAnalysis,
    "small_signal_stability": SmallSignalStabilityAnalysis,
}


def execute(args: argparse.Namespace) -> int:
    """Execute list command.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Exit code
    """
    skill_type = args.type
    
    print("\nAvailable Analysis Skills")
    print("=" * 60)
    
    skills = []
    for name, skill_class in SKILL_REGISTRY.items():
        try:
            skill = skill_class()
            skills.append((name, skill))
        except Exception:
            continue
    
    if not skills:
        print("No skills available")
        return 0
    
    for name, skill in sorted(skills, key=lambda x: x[0]):
        print(f"\n  {name}")
        print(f"    Description: {skill.description}")
        print(f"    Unified Model: {hasattr(skill, 'run') and 'model' in skill.run.__code__.co_varnames}")
    
    print(f"\nTotal: {len(skills)} skills")
    return 0
```

- [ ] **Step 5: Run test to verify it passes**

```bash
pytest cloudpss_skills_v2/tests/test_cli.py -v
```

- [ ] **Step 6: Commit**

```bash
git add cloudpss_skills_v2/cli/ cloudpss_skills_v2/__main__.py cloudpss_skills_v2/tests/test_cli.py
git commit -m "feat: Add CLI module structure with list command"
```

---

## Task 2: Implement Run Command

**Files:**
- Create: `cloudpss_skills_v2/cli/commands/run_cmd.py`
- Modify: `cloudpss_skills_v2/cli/commands/list_cmd.py` (share SKILL_REGISTRY)
- Test: `cloudpss_skills_v2/tests/test_cli_run.py` (create new)

- [ ] **Step 1: Write failing test for run command**

```python
def test_run_command_exists():
    """Test run command module exists."""
    from cloudpss_skills_v2.cli.commands import run_cmd
    assert hasattr(run_cmd, 'execute')

def test_run_command_with_mock_model():
    """Test run command with mock model."""
    import argparse
    from unittest.mock import patch, MagicMock
    from cloudpss_skills_v2.cli.commands.run_cmd import execute
    
    args = argparse.Namespace(
        skill="parameter_sensitivity",
        model="test-model",
        engine="pandapower",
        config=None,
        output=None
    )
    
    # Mock the analysis execution
    with patch('cloudpss_skills_v2.cli.commands.run_cmd._run_analysis') as mock_run:
        mock_run.return_value = {"status": "success", "result": "test"}
        result = execute(args)
        assert result == 0
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest cloudpss_skills_v2/tests/test_cli_run.py -v
```

- [ ] **Step 3: Implement run command**

In `cloudpss_skills_v2/cli/commands/run_cmd.py`:
```python
"""Run command - execute analysis skills."""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Optional

from cloudpss_skills_v2.core.system_model import PowerSystemModel
from cloudpss_skills_v2.powerapi import EngineConfig
from cloudpss_skills_v2.powerskill import Engine

from .list_cmd import SKILL_REGISTRY


def execute(args: argparse.Namespace) -> int:
    """Execute run command.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Exit code
    """
    skill_name = args.skill
    model_rid = args.model
    engine_name = args.engine
    config_str = args.config
    output_path = args.output
    
    # Validate skill
    if skill_name not in SKILL_REGISTRY:
        print(f"Error: Unknown skill '{skill_name}'", file=sys.stderr)
        print(f"Available skills: {', '.join(SKILL_REGISTRY.keys())}", file=sys.stderr)
        return 1
    
    # Parse config
    config = _parse_config(config_str)
    
    try:
        # Run analysis
        result = _run_analysis(skill_name, model_rid, engine_name, config)
        
        # Output result
        if output_path:
            with open(output_path, 'w') as f:
                json.dump(result, f, indent=2, default=str)
            print(f"Result saved to: {output_path}")
        else:
            print(json.dumps(result, indent=2, default=str))
        
        return 0 if result.get("status") == "success" else 1
        
    except Exception as e:
        print(f"Error running analysis: {e}", file=sys.stderr)
        return 1


def _parse_config(config_str: Optional[str]) -> dict:
    """Parse configuration from string or file."""
    if not config_str:
        return {}
    
    # Try to parse as JSON
    try:
        return json.loads(config_str)
    except json.JSONDecodeError:
        pass
    
    # Try to load from file
    config_path = Path(config_str)
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    
    return {}


def _run_analysis(skill_name: str, model_rid: str, engine_name: str, config: dict) -> dict:
    """Run analysis with unified model.
    
    Args:
        skill_name: Name of the skill to run
        model_rid: Model identifier
        engine_name: Engine to use (cloudpss or pandapower)
        config: Analysis configuration
        
    Returns:
        Analysis results
    """
    # Import skill class
    skill_class = SKILL_REGISTRY[skill_name]
    skill = skill_class()
    
    # Create engine and run power flow to get unified model
    engine = Engine.create_powerflow_for_skill(
        engine=engine_name,
        base_url=config.get("base_url"),
        auth=config.get("auth", {})
    )
    
    # Run power flow to get unified model
    sim_result = engine.run_power_flow(
        model_id=model_rid,
        source=config.get("source", "cloud"),
        auth=config.get("auth", {})
    )
    
    if not sim_result.is_success:
        return {
            "status": "error",
            "errors": sim_result.errors or ["Power flow failed"]
        }
    
    # Get unified model
    unified_model = None
    if hasattr(engine, 'get_system_model'):
        unified_model = engine.get_system_model(sim_result.job_id)
    if unified_model is None and hasattr(sim_result, 'system_model'):
        unified_model = sim_result.system_model
    
    if unified_model is None:
        return {
            "status": "error",
            "errors": ["Could not extract unified model from results"]
        }
    
    # Run analysis on unified model
    analysis_config = config.get("analysis", {})
    result = skill.run(unified_model, analysis_config)
    
    return result
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest cloudpss_skills_v2/tests/test_cli_run.py -v
```

- [ ] **Step 5: Commit**

```bash
git add cloudpss_skills_v2/cli/commands/run_cmd.py cloudpss_skills_v2/tests/test_cli_run.py
git commit -m "feat: Add CLI run command for unified model analysis"
```

---

## Task 3: Implement Compare Command

**Files:**
- Create: `cloudpss_skills_v2/cli/commands/compare_cmd.py`
- Test: `cloudpss_skills_v2/tests/test_cli_compare.py` (create new)

- [ ] **Step 1: Write failing test for compare command**

```python
def test_compare_command_exists():
    """Test compare command module exists."""
    from cloudpss_skills_v2.cli.commands import compare_cmd
    assert hasattr(compare_cmd, 'execute')
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest cloudpss_skills_v2/tests/test_cli_compare.py -v
```

- [ ] **Step 3: Implement compare command**

In `cloudpss_skills_v2/cli/commands/compare_cmd.py`:
```python
"""Compare command - compare results from different engines."""

import argparse
import json
from typing import List

from .run_cmd import _run_analysis


def execute(args: argparse.Namespace) -> int:
    """Execute compare command.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Exit code
    """
    engines = args.engines.split(',')
    model_rid = args.model
    analysis_type = args.analysis
    
    if len(engines) < 2:
        print("Error: At least 2 engines required for comparison", file=argparse.sys.stderr)
        return 1
    
    print(f"\nComparing {analysis_type} across engines: {', '.join(engines)}")
    print("=" * 60)
    
    results = {}
    for engine in engines:
        print(f"\nRunning with {engine}...")
        try:
            result = _run_analysis(analysis_type, model_rid, engine, {})
            results[engine] = result
            status = result.get("status", "unknown")
            print(f"  Status: {status}")
        except Exception as e:
            print(f"  Error: {e}")
            results[engine] = {"status": "error", "error": str(e)}
    
    # Compare results
    comparison = _compare_results(results)
    
    print("\n" + "=" * 60)
    print("Comparison Summary")
    print("=" * 60)
    print(json.dumps(comparison, indent=2))
    
    return 0


def _compare_results(results: dict) -> dict:
    """Compare results from different engines."""
    engines = list(results.keys())
    
    comparison = {
        "engines": engines,
        "all_succeeded": all(r.get("status") == "success" for r in results.values()),
        "differences": {}
    }
    
    # Compare specific metrics if available
    for engine, result in results.items():
        if result.get("status") == "success":
            # Extract key metrics for comparison
            metrics = {}
            if "sensitivities" in result:
                metrics["sensitivity_count"] = len(result["sensitivities"])
            if "pv_curve" in result:
                metrics["pv_points"] = len(result["pv_curve"])
            comparison["differences"][engine] = metrics
    
    return comparison
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest cloudpss_skills_v2/tests/test_cli_compare.py -v
```

- [ ] **Step 5: Commit**

```bash
git add cloudpss_skills_v2/cli/commands/compare_cmd.py cloudpss_skills_v2/tests/test_cli_compare.py
git commit -m "feat: Add CLI compare command for cross-engine comparison"
```

---

## Task 4: Create Workflow Module

**Files:**
- Create: `cloudpss_skills_v2/workflow/__init__.py`
- Create: `cloudpss_skills_v2/workflow/chain.py`
- Create: `cloudpss_skills_v2/workflow/pipeline.py`
- Test: `cloudpss_skills_v2/tests/test_workflow.py` (create new)

- [ ] **Step 1: Write failing test for workflow**

```python
def test_workflow_module_exists():
    """Test workflow module can be imported."""
    from cloudpss_skills_v2.workflow import AnalysisChain
    assert AnalysisChain is not None

def test_analysis_chain():
    """Test chaining multiple analyses."""
    from cloudpss_skills_v2.workflow.chain import AnalysisChain
    from cloudpss_skills_v2.poweranalysis import ParameterSensitivityAnalysis
    
    chain = AnalysisChain()
    chain.add_step("sensitivity", ParameterSensitivityAnalysis(), {"target_parameter": "load.p_mw"})
    
    assert len(chain.steps) == 1
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest cloudpss_skills_v2/tests/test_workflow.py -v
```

- [ ] **Step 3: Implement workflow module**

In `cloudpss_skills_v2/workflow/__init__.py`:
```python
"""Workflow module for chaining multiple analyses."""

from .chain import AnalysisChain
from .pipeline import AnalysisPipeline

__all__ = ["AnalysisChain", "AnalysisPipeline"]
```

In `cloudpss_skills_v2/workflow/chain.py`:
```python
"""Analysis chain - sequential execution of multiple analyses."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List

from cloudpss_skills_v2.core.system_model import PowerSystemModel
from cloudpss_skills_v2.poweranalysis.base import PowerAnalysis


@dataclass
class ChainStep:
    """Single step in analysis chain."""
    name: str
    analysis: PowerAnalysis
    config: dict


class AnalysisChain:
    """Chain multiple analyses to run sequentially.
    
    Each step receives the unified model and can pass results
    to subsequent steps via the context.
    """
    
    def __init__(self):
        self.steps: List[ChainStep] = []
        self.results: dict = {}
    
    def add_step(self, name: str, analysis: PowerAnalysis, config: dict = None) -> "AnalysisChain":
        """Add analysis step to chain.
        
        Args:
            name: Step identifier
            analysis: Analysis instance
            config: Step configuration
            
        Returns:
            Self for method chaining
        """
        self.steps.append(ChainStep(
            name=name,
            analysis=analysis,
            config=config or {}
        ))
        return self
    
    def run(self, model: PowerSystemModel, context: dict = None) -> dict:
        """Run all steps in chain.
        
        Args:
            model: Unified PowerSystemModel
            context: Optional shared context between steps
            
        Returns:
            Dictionary of all step results
        """
        context = context or {}
        all_results = {"steps": {}, "context": context}
        
        for step in self.steps:
            # Merge step config with context
            config = {**context, **step.config}
            
            # Run analysis
            result = step.analysis.run(model, config)
            all_results["steps"][step.name] = result
            
            # Update context with results for next steps
            if result.get("status") == "success":
                context[f"{step.name}_result"] = result
            else:
                # Stop chain on failure
                all_results["status"] = "failed"
                all_results["failed_at"] = step.name
                return all_results
        
        all_results["status"] = "success"
        return all_results
```

In `cloudpss_skills_v2/workflow/pipeline.py`:
```python
"""Analysis pipeline - parallel execution of independent analyses."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List

from cloudpss_skills_v2.core.system_model import PowerSystemModel
from cloudpss_skills_v2.poweranalysis.base import PowerAnalysis


class AnalysisPipeline:
    """Pipeline for running multiple analyses in parallel.
    
    Useful when analyses are independent and can run concurrently.
    """
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.analyses: List[tuple[str, PowerAnalysis, dict]] = []
    
    def add_analysis(self, name: str, analysis: PowerAnalysis, config: dict = None) -> "AnalysisPipeline":
        """Add analysis to pipeline.
        
        Args:
            name: Analysis identifier
            analysis: Analysis instance
            config: Analysis configuration
            
        Returns:
            Self for method chaining
        """
        self.analyses.append((name, analysis, config or {}))
        return self
    
    def run(self, model: PowerSystemModel) -> dict:
        """Run all analyses in parallel.
        
        Args:
            model: Unified PowerSystemModel
            
        Returns:
            Dictionary of all analysis results
        """
        results = {"status": "success", "analyses": {}}
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all analyses
            futures = {
                executor.submit(analysis.run, model, config): name
                for name, analysis, config in self.analyses
            }
            
            # Collect results
            for future in futures:
                name = futures[future]
                try:
                    result = future.result()
                    results["analyses"][name] = result
                    if result.get("status") != "success":
                        results["status"] = "partial_failure"
                except Exception as e:
                    results["analyses"][name] = {"status": "error", "error": str(e)}
                    results["status"] = "partial_failure"
        
        return results
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest cloudpss_skills_v2/tests/test_workflow.py -v
```

- [ ] **Step 5: Commit**

```bash
git add cloudpss_skills_v2/workflow/ cloudpss_skills_v2/tests/test_workflow.py
git commit -m "feat: Add workflow module for analysis chaining and pipelines"
```

---

## Task 5: Create End-to-End Example

**Files:**
- Create: `cloudpss_skills_v2/examples/cli_workflow_example.py`
- Create: `cloudpss_skills_v2/examples/README.md`

- [ ] **Step 1: Create CLI workflow example**

```python
#!/usr/bin/env python
"""End-to-end example: CLI and Workflow usage.

This example demonstrates:
1. Using CLI commands programmatically
2. Chaining multiple analyses with workflow
3. Comparing results across engines
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss_skills_v2.core.system_model import PowerSystemModel, Bus, Branch, Load, Generator
from cloudpss_skills_v2.workflow.chain import AnalysisChain
from cloudpss_skills_v2.poweranalysis import (
    ParameterSensitivityAnalysis,
    VoltageStabilityAnalysis,
    N1SecurityAnalysis,
)


def create_test_model() -> PowerSystemModel:
    """Create a simple test model."""
    return PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK",
                v_magnitude_pu=1.0, v_angle_degree=0.0),
            Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ",
                v_magnitude_pu=0.98, v_angle_degree=-2.0),
            Bus(bus_id=2, name="Bus3", base_kv=230.0, bus_type="PQ",
                v_magnitude_pu=0.95, v_angle_degree=-4.0),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="Line1-2", branch_type="LINE",
                   r_pu=0.01, x_pu=0.1, rate_a_mva=100.0),
            Branch(from_bus=1, to_bus=2, name="Line2-3", branch_type="LINE",
                   r_pu=0.015, x_pu=0.12, rate_a_mva=80.0),
        ],
        loads=[
            Load(bus_id=1, name="Load2", p_mw=50, q_mvar=10),
            Load(bus_id=2, name="Load3", p_mw=30, q_mvar=5),
        ],
        generators=[
            Generator(bus_id=0, name="Gen1", p_gen_mw=80, in_service=True),
        ],
        base_mva=100.0
    )


def example_1_basic_cli():
    """Example 1: Basic CLI usage."""
    print("\n" + "=" * 60)
    print("Example 1: Basic CLI Usage")
    print("=" * 60)
    
    from cloudpss_skills_v2.cli.main import main
    
    # List available skills
    print("\n$ cloudpss-skills-v2 list")
    main(["list"])


def example_2_analysis_chain():
    """Example 2: Chaining multiple analyses."""
    print("\n" + "=" * 60)
    print("Example 2: Analysis Chain")
    print("=" * 60)
    
    model = create_test_model()
    
    # Create analysis chain
    chain = AnalysisChain()
    chain.add_step(
        "sensitivity",
        ParameterSensitivityAnalysis(),
        {"target_parameter": "load.p_mw", "delta": 0.01}
    )
    chain.add_step(
        "voltage_stability",
        VoltageStabilityAnalysis(),
        {"load_scaling": [1.0, 1.2, 1.4, 1.6]}
    )
    chain.add_step(
        "n1_security",
        N1SecurityAnalysis(),
        {"check_voltage": True, "check_thermal": True}
    )
    
    # Run chain
    print("\nRunning analysis chain...")
    results = chain.run(model)
    
    print(f"\nChain status: {results['status']}")
    for step_name, result in results['steps'].items():
        status = result.get('status', 'unknown')
        print(f"  {step_name}: {status}")


def example_3_workflow_with_context():
    """Example 3: Workflow with shared context."""
    print("\n" + "=" * 60)
    print("Example 3: Workflow with Context Sharing")
    print("=" * 60)
    
    model = create_test_model()
    
    # Create context with base configuration
    context = {
        "voltage_threshold": 0.05,
        "thermal_threshold": 1.0,
        "base_mva": model.base_mva
    }
    
    chain = AnalysisChain()
    chain.add_step(
        "voltage_stability",
        VoltageStabilityAnalysis(),
        {"load_scaling": [1.0, 1.5, 2.0]}
    )
    
    # Run with context
    results = chain.run(model, context)
    
    print("\nContext after workflow:")
    for key, value in results['context'].items():
        if not key.endswith('_result'):
            print(f"  {key}: {value}")


if __name__ == "__main__":
    example_1_basic_cli()
    example_2_analysis_chain()
    example_3_workflow_with_context()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)
```

- [ ] **Step 2: Create examples README**

```markdown
# CloudPSS Skills v2 Examples

This directory contains examples demonstrating the unified PowerSystemModel architecture.

## CLI Examples

### List available skills
```bash
python -m cloudpss_skills_v2 list
```

### Run an analysis
```bash
python -m cloudpss_skills_v2 run n1_security \
  --model model/holdme/IEEE39 \
  --engine cloudpss
```

### Compare engines
```bash
python -m cloudpss_skills_v2 compare \
  --engines cloudpss,pandapower \
  --model model/holdme/IEEE39 \
  --analysis powerflow
```

## Workflow Examples

See `cli_workflow_example.py` for programmatic usage examples.

```python
from cloudpss_skills_v2.workflow.chain import AnalysisChain
from cloudpss_skills_v2.poweranalysis import (
    ParameterSensitivityAnalysis,
    VoltageStabilityAnalysis,
)

chain = AnalysisChain()
chain.add_step("sensitivity", ParameterSensitivityAnalysis(), {...})
chain.add_step("voltage_stability", VoltageStabilityAnalysis(), {...})

results = chain.run(unified_model)
```
```

- [ ] **Step 3: Commit**

```bash
git add cloudpss_skills_v2/examples/
git commit -m "docs: Add CLI and workflow examples"
```

---

## Verification Checklist

After all tasks complete:

- [ ] CLI module imports successfully
- [ ] `python -m cloudpss_skills_v2 list` works
- [ ] `python -m cloudpss_skills_v2 run --help` works
- [ ] All CLI tests pass: `pytest cloudpss_skills_v2/tests/test_cli*.py -v`
- [ ] All workflow tests pass: `pytest cloudpss_skills_v2/tests/test_workflow.py -v`
- [ ] Examples run without errors: `python cloudpss_skills_v2/examples/cli_workflow_example.py`
- [ ] All commits follow conventional commit format

---

## Execution Handoff

**Plan complete and saved to `docs/superpowers/plans/2026-05-03-phase5-cli-and-workflow.md`.**

**Recommended execution approach:** Use superpowers:subagent-driven-development
- Fresh subagent per task
- Two-stage review after each task
- Tasks 1-4 can run in parallel

**Total estimated time:** 25-30 minutes (5 tasks × 5-6 minutes each)
