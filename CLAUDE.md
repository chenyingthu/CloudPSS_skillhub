# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Development Commands

```bash
# Install dependencies
pip install -e .

# Development mode with all dependencies
pip install -e ".[dev]"

# Run all tests (default unit tests, no network)
pytest

# Run integration tests (requires CloudPSS token)
pytest --run-integration -m integration

# Run integration tests excluding slow EMT tests
pytest --run-integration -m "integration and not slow_emt"

# Run specific test file
pytest tests/test_powerflow_result.py

# Run with coverage
pytest --cov=cloudpss_skills --cov-report=html

# Run example scripts directly
python examples/simulation/run_powerflow.py
python examples/analysis/emt_fault_study_example.py model/holdme/IEEE3
```

## Environment Setup

- **Token Configuration**: Create `.cloudpss_token` file with your CloudPSS API token
- **Environment Variables**:
  - `CLOUDPSS_TOKEN` - API token (alternative to file)
  - `TEST_MODEL_RID` - Test model ID (default: `model/holdme/IEEE39`)
  - `TEST_SAVE_KEY_PREFIX` - Enable live `model.save()` tests

## Architecture Overview

### Package Structure

```
cloudpss_skills/
├── __init__.py          # Main entry, exports core classes
├── __main__.py          # CLI entry point (cloudpss-run command)
├── core/
│   ├── base.py          # SkillBase ABC, SkillResult, ValidationResult
│   ├── config.py        # Configuration loading and validation
│   ├── registry.py      # Skill registration and discovery
│   └── cli.py           # Command-line interface
└── builtin/             # Built-in skills (10 validated)
    ├── power_flow.py    # Power flow calculation
    ├── emt_simulation.py # EMT transient simulation
    ├── n1_security.py   # N-1 security screening
    ├── param_scan.py    # Parameter scanning
    ├── batch_powerflow.py # Batch power flow studies
    ├── result_compare.py # Result comparison
    ├── visualize.py     # Visualization
    └── ...
```

### Core Abstractions

**SkillBase** (`core/base.py:106`): All skills inherit from this ABC
- `name` - Skill identifier (e.g., "power_flow", "emt_simulation")
- `description` - Human-readable description
- `config_schema` - JSON Schema for configuration validation
- `run(config)` - Execute the skill, returns `SkillResult`
- `validate(config)` - Validate configuration before execution

**SkillResult** (`core/base.py:43`): Execution result container
- `status` - SkillStatus (PENDING/RUNNING/SUCCESS/FAILED/CANCELLED)
- `data` - Result data dictionary
- `artifacts` - Output files (CSV, JSON, PNG, etc.)
- `logs` - Execution log entries
- `metrics` - Performance metrics

### Configuration-Driven Execution

Skills are executed via YAML configuration files:

```yaml
skill: power_flow
auth:
  token_file: .cloudpss_token
model:
  rid: model/holdme/IEEE39
  source: cloud  # or 'local' for YAML files
algorithm:
  type: newton_raphson
  tolerance: 1e-6
output:
  format: json
  path: ./results/
  prefix: power_flow
```

Run with: `python -m cloudpss_skills run --config config.yaml`

### Primary Workflows

**1. Power Flow Studies** (IEEE39 validated)
- Entry: `PowerFlowSkill` / `examples/simulation/run_powerflow.py`
- Engineering studies: line outage, generator voltage/P adjustment, load shift
- N-1 screening: `examples/analysis/powerflow_n1_screening_example.py`
- Batch studies: `examples/analysis/powerflow_batch_study_example.py`

**2. EMT Simulations** (IEEE3 validated)
- Entry: `EmtSimulationSkill` / `examples/simulation/run_emt_simulation.py`
- Prerequisites: EMT topology, fault components, measurement signals, output channels
- Preparation: `examples/basic/ieee3_emt_preparation_example.py`
- Voltage meter chain: `examples/basic/emt_voltage_meter_chain_example.py`

**3. Analysis Workflows**
- Fault studies: `emt_fault_study_example.py` (baseline/delayed/mild scenarios)
- Parameter scans: `emt_fault_clearing_scan_example.py`, `emt_fault_severity_scan_example.py`
- N-1 screening: `emt_n1_security_screening_example.py`
- Research reports: `emt_research_report_example.py`

### Test Framework

**Two Test Tiers** (`tests/README.md`):

1. **Unit Tests** (default): Local SDK boundary testing, no network
   - Run: `pytest tests/ -q`
   - Validates: config parsing, data serialization, script logic

2. **Integration Tests**: Real CloudPSS API calls
   - Run: `pytest --run-integration -m "integration and not slow_emt"`
   - Requires: valid token, network access
   - Default model: `model/holdme/IEEE39` (power flow), `model/holdme/IEEE3` (EMT)

**Key Test Files**:
- `tests/test_sdk_api.py` - Model/Job/Component API tests
- `tests/test_powerflow_result.py` - Power flow result validation (15+ live scenarios)
- `tests/test_emt_result.py` - EMT result validation (20+ live scenarios including N-1, reports)
- `tests/test_examples.py` - Example script boundary tests

### Documentation Structure

```
docs/
├── README.md                    # Main documentation index
├── api-inventory.md             # SDK API coverage matrix (auto-generated)
├── guides/
│   ├── research-workflow-core-apis.md      # Modeling → Power Flow → EMT pipeline
│   ├── model-building-workflow.md          # Model fetch/edit/save workflows
│   ├── powerflow-study-workflow.md         # Power flow study patterns
│   └── emt-study-workflow.md               # EMT simulation patterns
├── api-reference/
│   ├── model-api.md             # Model API (fetch, runPowerFlow, runEMT, save)
│   ├── job-api.md               # Job API (status, result, abort)
│   ├── powerflow-result-api.md  # PowerFlowResult API (getBuses, getBranches)
│   └── emtresult-api.md         # EMTResult API (getPlots, getPlotChannelData)
└── skills/
    ├── README.md                # Built-in skills documentation
    ├── config_reference.md      # Configuration reference
    └── user_manual.md           # User guide for skills
```

### Key Design Decisions

1. **Configuration-Driven**: Skills use YAML configs, not hardcoded parameters
2. **Local-First**: Examples work with local YAML files, not just cloud models
3. **Evidence-Based Testing**: Integration tests require real API calls, no mock results claimed as real
4. **Validated Scenarios Only**: Only documented scenarios with live verification are claimed as "supported"
5. **Two-Tier Testing**: Fast unit tests by default, explicit opt-in for slow integration tests

### Common Patterns

**Model Acquisition**:
```python
# From cloud
model = Model.fetch("model/holdme/IEEE39")

# From local YAML
model = Model.load("path/to/model.yaml")

# Create working copy
model = Model.fetch("model/holdme/IEEE39")
# ... make changes ...
model.save("new-branch-key")  # Creates new cloud branch
```

**Component Modification**:
```python
# Add component
model.addComponent(definition, label, args, pins)

# Modify component
model.updateComponent(key, **kwargs)

# Remove component
model.removeComponent(key)

# Get topology
topology = model.fetchTopology(implementType="emtp")
```

**Simulation Execution**:
```python
# Power flow
job = model.runPowerFlow()
status = job.status()  # 0=running, 1=done, 2=failed
result = job.result

# EMT
job = model.runEMT()
# Wait for completion...
result = job.result
plots = result.getPlots()
waveform = result.getPlotChannelData(plot_index, channel_name)
```
