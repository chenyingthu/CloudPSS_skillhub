# New Architecture Usage Example

This document demonstrates how to use the new architecture components.

## 1. Define a Power System Model (DataClass)

```python
from cloudpss_skills_v2.core import Bus, Branch, Generator, PowerSystemModel

# Create buses with type safety
buses = [
    Bus(bus_id=1, name="Bus1", base_kv=345.0, bus_type="SLACK",
        v_magnitude_pu=1.0, v_angle_degree=0.0),
    Bus(bus_id=2, name="Bus2", base_kv=345.0, bus_type="PV",
        v_magnitude_pu=1.02, p_injected_mw=150.0),
    Bus(bus_id=3, name="Bus3", base_kv=345.0, bus_type="PQ",
        p_injected_mw=-100.0, q_injected_mvar=-50.0),
]

# Create branches
branches = [
    Branch(from_bus=1, to_bus=2, name="Line1-2",
           r_pu=0.01, x_pu=0.05, rate_a_mva=500.0,
           loading_percent=45.0),
    Branch(from_bus=2, to_bus=3, name="Line2-3",
           r_pu=0.015, x_pu=0.08, rate_a_mva=400.0,
           loading_percent=62.0),
]

# Create generators
generators = [
    Generator(bus_id=1, name="Gen1", p_gen_mw=100.0,
              p_max_mw=200.0, p_min_mw=50.0),
    Generator(bus_id=2, name="Gen2", p_gen_mw=150.0,
              p_max_mw=300.0, p_min_mw=0.0),
]

# Build system model with validation
model = PowerSystemModel(
    buses=buses,
    branches=branches,
    generators=generators,
    base_mva=100.0,
    source_engine="cloudpss"
)

# Physical validation happens automatically
# - Checks voltage ranges (0.5 - 1.5 p.u.)
# - Validates bus connections
# - Ensures generator limits consistency
```

## 2. Engine Registration and Discovery

```python
from cloudpss_skills_v2.core import (
    EngineRegistry, EngineCapabilities, SimulationType, ParameterSpec
)

# Define engine capabilities
cloudpss_caps = EngineCapabilities(
    engine_name="cloudpss",
    engine_version="2.0",
    vendor="CloudPSS",
    description="Cloud-based power system simulation",

    supported_simulations=[
        SimulationType.POWER_FLOW_AC,
        SimulationType.SHORT_CIRCUIT_3PH,
        SimulationType.EMT_TRANSIENT,
    ],
    supported_model_formats=["cloudpss_rid", "json"],

    max_buses=10000,
    supports_parallel=True,

    simulation_parameters={
        SimulationType.POWER_FLOW_AC: [
            ParameterSpec(
                name="algorithm",
                param_type="enum",
                description="Solution algorithm",
                default="newton_raphson",
                choices=["newton_raphson", "fast_decoupled"]
            ),
            ParameterSpec(
                name="tolerance",
                param_type="float",
                description="Convergence tolerance",
                default=1e-6,
                min_value=1e-10,
                max_value=1e-2,
            ),
        ]
    }
)

# Register engine (typically done in engine __init__.py)
EngineRegistry.register("cloudpss", CloudPSSAdapter)

# Discover available engines
all_engines = EngineRegistry.list_engines()
# ['cloudpss', 'pandapower']

# Find engines supporting specific simulation
pf_engines = EngineRegistry.list_engines(SimulationType.POWER_FLOW_AC)
# ['cloudpss', 'pandapower']

# Get engine capabilities
caps = EngineRegistry.get_capabilities("cloudpss")
print(caps.supports(SimulationType.POWER_FLOW_AC))  # True
```

## 3. Hierarchical Configuration

```python
from cloudpss_skills_v2.core import (
    ConfigStore, BaseConfig, ProjectConfig, StudyConfig
)

# Create configuration store
store = ConfigStore("./config_store")

# Level 1: Base configuration (global defaults)
base = BaseConfig(
    name="high_precision",
    default_engine="cloudpss",
    default_tolerance=1e-10,
    default_max_iterations=200,
    engine_profiles={
        "cloudpss": {"base_url": "https://www.cloudpss.net/"},
        "pandapower": {"numba": True},
    }
)
store.save_base_config(base)

# Level 2: Project configuration
project = ProjectConfig(
    name="transmission_studies",
    inherits_from="high_precision",  # From base
    project_id="TS_2024",
    model_library={
        "IEEE39": "model/holdme/IEEE39",
        "IEEE118": "model/holdme/IEEE118",
    },
    output_organization="by_date",
    # Override base settings
    tolerance=1e-8,  # Slightly relaxed from base
)
store.save_project_config(project)

# Level 3: Study configuration
study = StudyConfig(
    name="ieee39_n1_security",
    inherits_from="transmission_studies",  # From project
    study_type="n1_security",
    model_id="model/holdme/IEEE39",
    analysis_type="n1_security",
    analysis_config={
        "check_voltage": True,
        "voltage_threshold": 0.05,
        "thermal_threshold": 1.0,
    },
    tags=["n1", "security", "ieee39"],
)
store.save_study_config("transmission_studies", study)

# Resolve effective configuration
effective = store.get_effective_config(
    study_id="ieee39_n1_security",
    project_id="transmission_studies",
    environment="production",
)

# effective now contains merged values:
# - tolerance: 1e-8 (from project, overrides base 1e-10)
# - default_engine: "cloudpss" (from base)
# - model_id: "model/holdme/IEEE39" (from study)
# - analysis_config: {...} (from study)
```

## 4. Result Archival (HDF5)

```python
from cloudpss_skills_v2.core import ResultArchive
from datetime import datetime

# Create archive
archive = ResultArchive("./results/archive.h5")

# Archive a simulation result
archive_id = archive.archive_result(
    study_id="transmission_studies/ieee39_n1_security",
    study_name="ieee39_n1_security",
    project_id="transmission_studies",
    system_model=model,  # PowerSystemModel
    summary_metrics={
        "n1_pass_rate": 95.5,
        "max_voltage_violation": 0.03,
        "total_contingencies": 46,
        "failed_contingencies": 2,
    },
    study_config={"model_id": "model/holdme/IEEE39", "engine": "cloudpss"},
    tags=["n1", "security", "ieee39"],
    engine_type="cloudpss",
    engine_version="2.0",
    execution_time_seconds=125.3,
)

# Query archived results
results = archive.query(
    project_id="transmission_studies",
    tags=["n1"],
    date_range=("2024-01-01", "2024-12-31"),
)

# Load archived model
archived_model = archive.load_system_model(archive_id)

# Compare results
comparison = archive.compare_results(
    base_archive_id="transmission_studies_ieee39_n1_security_20240115_143022_a1b2c3d4",
    compare_archive_ids=[
        "transmission_studies_ieee39_n1_security_20240116_091522_e5f6g7h8",
        "transmission_studies_ieee39_n1_security_20240117_102233_i9j0k1l2",
    ]
)

if comparison.has_significant_changes(threshold=0.01):
    print("Significant changes detected:")
    for archive_id, diffs in comparison.metric_differences.items():
        print(f"  {archive_id}:")
        for metric, diff in diffs.items():
            print(f"    {metric}: {diff:+.2f}")
```

## 5. Engine-Agnostic Analysis

```python
# Analysis code works with unified model, no engine-specific logic

from cloudpss_skills_v2.core import PowerSystemModel, SeverityLevel

def analyze_voltage_violations(model: PowerSystemModel) -> list[dict]:
    """Analyze voltage violations - works with any engine."""
    violations = []

    for bus in model.buses:
        if bus.v_magnitude_pu is None:
            continue

        if bus.v_magnitude_pu < bus.vm_min_pu:
            violations.append({
                "bus_name": bus.name,
                "bus_id": bus.bus_id,
                "type": "undervoltage",
                "actual": bus.v_magnitude_pu,
                "limit": bus.vm_min_pu,
                "severity": SeverityLevel.CRITICAL
                        if bus.v_magnitude_pu < 0.85
                        else SeverityLevel.WARNING,
            })
        elif bus.v_magnitude_pu > bus.vm_max_pu:
            violations.append({
                "bus_name": bus.name,
                "bus_id": bus.bus_id,
                "type": "overvoltage",
                "actual": bus.v_magnitude_pu,
                "limit": bus.vm_max_pu,
                "severity": SeverityLevel.CRITICAL
                        if bus.v_magnitude_pu > 1.15
                        else SeverityLevel.WARNING,
            })

    return violations

# Works with CloudPSS results
cloudpss_model = run_with_engine("cloudpss", study_config)
violations = analyze_voltage_violations(cloudpss_model)

# Works with Pandapower results (same code!)
pandapower_model = run_with_engine("pandapower", study_config)
violations = analyze_voltage_violations(pandapower_model)

# Compare results directly
cloudpss_df = cloudpss_model.buses_df
pandapower_df = pandapower_model.buses_df

voltage_diff = cloudpss_df["v_magnitude_pu"] - pandapower_df["v_magnitude_pu"]
max_diff = voltage_diff.abs().max()
print(f"Max voltage difference between engines: {max_diff:.6f} p.u.")
```

## 6. N-1 Analysis with Model Modification

```python
def run_n1_security_analysis(model: PowerSystemModel, dispatcher) -> dict:
    """Run N-1 security analysis using unified model."""

    base_result = dispatcher.run_power_flow(model)
    if not base_result.success:
        raise RuntimeError("Base case failed to converge")

    results = []

    for branch in model.branches:
        # Create N-1 scenario by removing branch
        n1_model = model.with_branch_removed(branch.name)

        # Run power flow on modified model
        n1_result = dispatcher.run_power_flow(n1_model)

        # Analyze results (same code for all engines)
        violations = analyze_voltage_violations(n1_result.system_model)
        thermal_violations = analyze_thermal_violations(n1_result.system_model)

        results.append({
            "removed_branch": branch.name,
            "converged": n1_result.success,
            "voltage_violations": violations,
            "thermal_violations": thermal_violations,
            "severity": determine_severity(violations, thermal_violations),
        })

    return {
        "base_case_converged": True,
        "contingencies": results,
        "pass_rate": sum(1 for r in results if r["severity"] == "normal") / len(results),
    }
```

## 7. Unified Model Integration Example

### Basic Usage

The unified PowerSystemModel enables seamless cross-engine analysis workflows:

```python
from cloudpss_skills_v2.powerskill.powerflow import PowerFlow
from cloudpss_skills_v2.poweranalysis.n1_security import N1SecurityAnalysis
from cloudpss_skills_v2.powerapi import EngineConfig

# Step 1: Run power flow with any engine
skill = PowerFlow()
result = skill.run({
    "engine": "cloudpss",
    "model": {"rid": "model/holdme/IEEE39"},
    "auth": {"token_file": ".cloudpss_token"}
})

# Step 2: Access unified model from result
unified_model = result.get('unified_model')
print(f"System has {len(unified_model.buses)} buses, {len(unified_model.branches)} branches")

# Step 3: Run analysis directly on unified model
analysis = N1SecurityAnalysis()
n1_result = analysis.run(unified_model, {
    "contingency_level": 1,
    "check_voltage": True,
    "check_thermal": True,
    "voltage_threshold": 0.05,
    "thermal_threshold": 1.0
})

# Step 4: Process analysis results
print(f"Secure: {n1_result['secure']}")
print(f"Total contingencies: {n1_result['contingency_count']}")
print(f"Violations found: {n1_result['violation_count']}")
for violation in n1_result['violations']:
    print(f"  - {violation['type']} on {violation['branch']}")
```

### Cross-Engine Analysis

The same unified model enables direct comparison between engines:

```python
# Run same case on different engines
cloudpss_config = {
    "engine": "cloudpss",
    "model": {"rid": "model/holdme/IEEE39"},
    "auth": {"token_file": ".cloudpss_token"}
}

pandapower_config = {
    "engine": "pandapower",
    "model": {"source": "builtin", "name": "case39"}
}

cloudpss_result = skill.run(cloudpss_config)
pandapower_result = skill.run(pandapower_config)

# Extract unified models
cloudpss_model = cloudpss_result.get('unified_model')
pandapower_model = pandapower_result.get('unified_model')

# Compare results using unified model DataFrame views
import pandas as pd

cloudpss_buses = cloudpss_model.buses_df
pandapower_buses = pandapower_model.buses_df

# Calculate differences
voltage_diff = cloudpss_buses['v_magnitude_pu'] - pandapower_buses['v_magnitude_pu']
angle_diff = cloudpss_buses['v_angle_degree'] - pandapower_buses['v_angle_degree']

print(f"Max voltage difference: {voltage_diff.abs().max():.4f} p.u.")
print(f"Max angle difference: {angle_diff.abs().max():.2f} degrees")

# Differences indicate:
# - Solver convergence tolerances
# - Model conversion approximations
# - Numerical precision variations
```

### Unified Model Caching

PowerFlow skill caches the unified model for subsequent analysis:

```python
# Run power flow
result = skill.run_power_flow(model_id="model/holdme/IEEE39")

# Model is automatically cached
if skill.has_unified_model():
    cached_model = skill.get_unified_model()
    print(f"Cached model: {len(cached_model.buses)} buses")

# Run multiple analyses without re-simulating
from cloudpss_skills_v2.poweranalysis.n1_security import N1SecurityAnalysis
from cloudpss_skills_v2.poweranalysis.parameter_sensitivity import ParameterSensitivityAnalysis

n1_analysis = N1SecurityAnalysis()
sensitivity_analysis = ParameterSensitivityAnalysis()

# Both use the same cached model
n1_result = n1_analysis.run(cached_model, {"contingency_level": 1})
sens_result = sensitivity_analysis.run(cached_model, {"parameter": "load_p_mw"})
```

### Benefits of Unified Model Architecture

1. **Engine Independence**: Analysis code works with any engine (CloudPSS, pandapower, etc.)
2. **Type Safety**: PowerSystemModel provides structured data with IDE support
3. **Cross-Engine Validation**: Compare results from different engines using same model
4. **Simplified Analysis**: Analysis classes work directly with unified model, no engine-specific code
5. **Consistent API**: Same interface regardless of underlying simulation engine
6. **Data Preservation**: Full system state available for post-processing and visualization

## Benefits of New Architecture

1. **Type Safety**: DataClass ensures correct types at construction
2. **Physical Validation**: Automatic checks for voltage/angle ranges
3. **Engine Independence**: Analysis code works with any engine
4. **Configuration Inheritance**: Reduce duplication with base → project → study
5. **Long-term Storage**: HDF5 archive supports years of result history
6. **Comparison**: Easy A/B testing across engines and time
