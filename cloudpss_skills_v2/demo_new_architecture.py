"""Demo: New Architecture End-to-End Workflow

This script demonstrates the complete workflow of the new architecture:
1. Create PowerSystemModel with DataClass
2. Register engine capabilities
3. Use hierarchical configuration
4. Archive results to HDF5
5. Query and compare results
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure we use the correct module path (handle worktree situation)
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import tempfile

import numpy as np

from cloudpss_skills_v2.core import (
    # System Model
    Bus,
    Branch,
    Generator,
    Load,
    PowerSystemModel,
    # Engine Capabilities
    EngineCapabilities,
    EngineRegistry,
    SimulationType,
    ParameterSpec,
    # Config Store
    ConfigStore,
    BaseConfig,
    ProjectConfig,
    StudyConfig,
    # Result Archive
    ResultArchive,
)


def demo_1_create_system_model():
    """Demo 1: Create a power system model with DataClass validation."""
    print("\n" + "="*60)
    print("DEMO 1: Create PowerSystemModel with DataClass")
    print("="*60)

    # Create IEEE 14-bus system (simplified subset)
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
               r_pu=0.01938, x_pu=0.05917, rate_a_mva=100.0,
               p_from_mw=156.88, loading_percent=65.2),
        Branch(from_bus=1, to_bus=5, name="Line 1-5",
               r_pu=0.05403, x_pu=0.22304, rate_a_mva=80.0,
               p_from_mw=75.52, loading_percent=52.8),
        Branch(from_bus=2, to_bus=3, name="Line 2-3",
               r_pu=0.04699, x_pu=0.19797, rate_a_mva=80.0,
               p_from_mw=73.62, loading_percent=55.4),
        Branch(from_bus=2, to_bus=4, name="Line 2-4",
               r_pu=0.05811, x_pu=0.17632, rate_a_mva=60.0,
               p_from_mw=56.06, loading_percent=62.1),
        Branch(from_bus=2, to_bus=5, name="Line 2-5",
               r_pu=0.05695, x_pu=0.17388, rate_a_mva=60.0,
               p_from_mw=41.42, loading_percent=45.3),
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

    # Build model with automatic validation
    model = PowerSystemModel(
        buses=buses,
        branches=branches,
        generators=generators,
        loads=loads,
        base_mva=100.0,
        name="IEEE 14-Bus Test System (Subset)",
        source_engine="demo"
    )

    print(f"✅ Created model: {model.name}")
    print(f"   Buses: {len(model.buses)}")
    print(f"   Branches: {len(model.branches)}")
    print(f"   Generators: {len(model.generators)}")
    print(f"   Loads: {len(model.loads)}")

    # Demonstrate physical validation
    print("\n   Physical validation checks:")
    print(f"   - Slack bus: {model.get_slack_bus().name}")
    print(f"   - Total generation: {model.total_generation_mw():.2f} MW")
    print(f"   - Total load: {model.total_load_mw():.2f} MW")

    # Check for violations
    voltage_violations = model.get_voltage_violations()
    print(f"   - Voltage violations: {len(voltage_violations)}")

    thermal_violations = model.get_thermal_violations()
    print(f"   - Thermal violations: {len(thermal_violations)}")

    return model


def demo_2_engine_capabilities():
    """Demo 2: Define and register engine capabilities."""
    print("\n" + "="*60)
    print("DEMO 2: Engine Capabilities Declaration")
    print("="*60)

    # Define CloudPSS capabilities
    cloudpss_caps = EngineCapabilities(
        engine_name="cloudpss",
        engine_version="2.0.0",
        vendor="CloudPSS",
        description="Cloud-based power system simulation platform",

        supported_simulations=[
            SimulationType.POWER_FLOW_AC,
            SimulationType.SHORT_CIRCUIT_3PH,
            SimulationType.EMT_TRANSIENT,
            SimulationType.TRANSIENT_STABILITY,
            SimulationType.CONTINGENCY_ANALYSIS,
        ],
        supported_model_formats=["cloudpss_rid", "json"],

        max_buses=10000,
        max_branches=20000,
        supports_parallel=True,

        supports_reactive_power=True,
        supports_tap_changers=True,
        supports_phase_shifters=True,
        supports_hvdc=True,

        simulation_parameters={
            SimulationType.POWER_FLOW_AC: [
                ParameterSpec(
                    name="algorithm",
                    param_type="enum",
                    description="Power flow solution algorithm",
                    default="newton_raphson",
                    choices=["newton_raphson", "fast_decoupled", "gauss_seidel"]
                ),
                ParameterSpec(
                    name="tolerance",
                    param_type="float",
                    description="Convergence tolerance",
                    default=1e-6,
                    min_value=1e-10,
                    max_value=1e-2,
                ),
                ParameterSpec(
                    name="max_iterations",
                    param_type="int",
                    description="Maximum iterations",
                    default=100,
                    min_value=10,
                    max_value=1000,
                ),
            ],
        }
    )

    print("✅ Defined CloudPSS capabilities:")
    print(f"   Supported simulations: {len(cloudpss_caps.supported_simulations)}")
    for sim_type in cloudpss_caps.supported_simulations:
        print(f"     - {sim_type.value}")

    print(f"\n   Max system size: {cloudpss_caps.max_buses} buses")
    print(f"   Parallel execution: {'Yes' if cloudpss_caps.supports_parallel else 'No'}")

    # Check capability support
    print("\n   Capability checks:")
    print(f"   - Supports AC Power Flow: {cloudpss_caps.supports(SimulationType.POWER_FLOW_AC)}")
    print(f"   - Supports OPF: {cloudpss_caps.supports(SimulationType.OPTIMAL_POWER_FLOW)}")

    # Define Pandapower capabilities
    pandapower_caps = EngineCapabilities(
        engine_name="pandapower",
        engine_version="2.13.0",
        vendor="PandaPower Team",
        description="Open source power system analysis",

        supported_simulations=[
            SimulationType.POWER_FLOW_AC,
            SimulationType.POWER_FLOW_DC,
            SimulationType.OPTIMAL_POWER_FLOW,
            SimulationType.SHORT_CIRCUIT_3PH,
            SimulationType.SHORT_CIRCUIT_1PH,
        ],
        supported_model_formats=["pandapower_net", "matpower", "excel"],

        max_buses=None,  # Memory limited
        supports_parallel=True,

        simulation_parameters={
            SimulationType.POWER_FLOW_AC: [
                ParameterSpec(
                    name="algorithm",
                    param_type="enum",
                    description="Power flow algorithm",
                    default="nr",
                    choices=["nr", "iwamoto_nr", "gs", "fdbx", "fdxb"]
                ),
                ParameterSpec(
                    name="numba",
                    param_type="bool",
                    description="Use Numba acceleration",
                    default=True,
                ),
            ],
        }
    )

    print("\n✅ Defined Pandapower capabilities:")
    print(f"   Supported simulations: {len(pandapower_caps.supported_simulations)}")
    print(f"   Max system size: Unlimited (memory constrained)")

    return cloudpss_caps, pandapower_caps


def demo_3_configuration_management(temp_dir: Path):
    """Demo 3: Hierarchical configuration management."""
    print("\n" + "="*60)
    print("DEMO 3: Hierarchical Configuration (base → project → study)")
    print("="*60)

    # Create configuration store
    config_path = temp_dir / "config_store"
    store = ConfigStore(config_path)

    # Level 1: Base configuration
    print("\n1. Creating base configuration...")
    base = BaseConfig(
        name="production_base",
        description="Production environment base configuration",
        default_engine="cloudpss",
        default_tolerance=1e-6,
        default_max_iterations=100,
        default_timeout_seconds=300,
        default_output_format="hdf5",
        default_output_path="./results",
        default_voltage_limits=(0.9, 1.1),
        default_thermal_limit=1.0,
        engine_profiles={
            "cloudpss": {
                "base_url": "https://www.cloudpss.net/",
                "auth_token_env": "CLOUDPSS_TOKEN",
            },
            "pandapower": {
                "numba": True,
                "tolerance": 1e-6,
            },
        },
        parallel_jobs=4,
    )
    store.save_base_config(base)
    print(f"   ✅ Saved base: {base.name}")

    # High-precision base variant
    high_precision = BaseConfig(
        name="high_precision",
        description="High precision analysis configuration",
        default_tolerance=1e-10,
        default_max_iterations=200,
    )
    store.save_base_config(high_precision)
    print(f"   ✅ Saved base: {high_precision.name}")

    # Level 2: Project configuration
    print("\n2. Creating project configuration...")
    project = ProjectConfig(
        name="transmission_planning_2024",
        description="Transmission system planning studies for 2024",
        inherits_from="production_base",
        project_id="TP2024",
        project_path=str(temp_dir / "projects" / "TP2024"),
        model_library={
            "IEEE14": "model/holdme/IEEE14",
            "IEEE39": "model/holdme/IEEE39",
            "IEEE118": "model/holdme/IEEE118",
        },
        output_organization="by_date",
        output_naming_pattern="{study_name}_{date}_{timestamp}",
    )
    store.save_project_config(project)
    print(f"   ✅ Saved project: {project.name}")

    # Level 3: Study configurations
    print("\n3. Creating study configurations...")

    study_pf = StudyConfig(
        name="ieee39_base_powerflow",
        description="IEEE 39-bus base case power flow",
        inherits_from="transmission_planning_2024",
        study_type="power_flow",
        model_id="model/holdme/IEEE39",
        model_source="cloud",
        analysis_type="power_flow",
        tags=["base_case", "ieee39", "power_flow"],
    )
    store.save_study_config("transmission_planning_2024", study_pf)
    print(f"   ✅ Saved study: {study_pf.name}")

    study_n1 = StudyConfig(
        name="ieee39_n1_security",
        description="IEEE 39-bus N-1 security analysis",
        inherits_from="transmission_planning_2024",
        study_type="n1_security",
        model_id="model/holdme/IEEE39",
        analysis_type="n1_security",
        analysis_config={
            "check_voltage": True,
            "check_thermal": True,
            "voltage_threshold": 0.05,
            "thermal_threshold": 1.0,
            "contingency_filter": "all_branches",
        },
        tags=["n1", "security", "ieee39"],
    )
    store.save_study_config("transmission_planning_2024", study_n1)
    print(f"   ✅ Saved study: {study_n1.name}")

    # Demonstrate configuration resolution
    print("\n4. Resolving effective configuration...")
    effective = store.get_effective_config(
        study_id="ieee39_n1_security",
        project_id="transmission_planning_2024",
    )

    print(f"\n   Effective configuration:")
    print(f"   - Study: {effective.name}")
    print(f"   - Type: {effective.study_type}")
    print(f"   - Engine: {effective.engine}")
    print(f"   - Tolerance: {effective.tolerance}")
    print(f"   - Max iterations: {effective.max_iterations}")
    print(f"   - Output format: {effective.output_format}")
    print(f"   - Parallel jobs: {effective.parallel_jobs}")

    print(f"\n   Source configuration IDs:")
    for level, config_id in effective.source_config_ids.items():
        print(f"     - {level}: {config_id}")

    return store, effective


def demo_4_result_archival(temp_dir: Path, model: PowerSystemModel):
    """Demo 4: Archive results to HDF5."""
    print("\n" + "="*60)
    print("DEMO 4: Result Archival (HDF5)")
    print("="*60)

    # Create archive
    archive_path = temp_dir / "results" / "archive.h5"
    archive = ResultArchive(archive_path)

    # Archive multiple results
    print("\n1. Archiving simulation results...")

    results = []
    for scenario in ["base_case", "high_load", "n1_branch_3_4"]:
        # Modify model slightly for each scenario
        if scenario == "base_case":
            mod_model = model
            metrics = {
                "max_voltage_pu": 1.045,
                "min_voltage_pu": 0.987,
                "max_loading_percent": 78.5,
                "total_losses_mw": 12.34,
            }
        elif scenario == "high_load":
            # Simulate high load scenario
            metrics = {
                "max_voltage_pu": 1.032,
                "min_voltage_pu": 0.952,
                "max_loading_percent": 95.2,
                "total_losses_mw": 18.76,
            }
        else:  # n1 scenario
            metrics = {
                "max_voltage_pu": 1.051,
                "min_voltage_pu": 0.923,
                "max_loading_percent": 112.3,
                "total_losses_mw": 15.42,
                "n1_violations": 2,
            }

        archive_id = archive.archive_result(
            study_id=f"transmission_planning_2024/ieee39_{scenario}",
            study_name=f"ieee39_{scenario}",
            project_id="transmission_planning_2024",
            system_model=mod_model,
            summary_metrics=metrics,
            study_config={
                "model_id": "model/holdme/IEEE39",
                "engine": "cloudpss",
                "scenario": scenario,
            },
            tags=[scenario, "ieee39", "power_flow"],
            engine_type="cloudpss",
            engine_version="2.0.0",
            execution_time_seconds=np.random.uniform(10, 60),
        )
        results.append(archive_id)
        print(f"   ✅ Archived {scenario}: {archive_id[:50]}...")

    # Query results
    print("\n2. Querying archived results...")
    all_results = archive.list_archives()
    print(f"   Total archives: {len(all_results)}")

    # Query by tag
    n1_results = archive.query(tags=["n1"])
    print(f"   N-1 results: {len(n1_results)}")

    # Query by project
    project_results = archive.query(project_id="transmission_planning_2024")
    print(f"   Project results: {len(project_results)}")

    # Load and compare
    print("\n3. Loading and comparing results...")
    base_id = results[0]
    compare_ids = results[1:]

    comparison = archive.compare_results(base_id, compare_ids)

    print(f"\n   Comparison results:")
    for archive_id in compare_ids:
        if archive_id in comparison.metric_differences:
            diffs = comparison.metric_differences[archive_id]
            print(f"\n   vs {archive_id[:30]}...")
            for metric, diff in diffs.items():
                print(f"     {metric}: {diff:+.3f}")

    if comparison.has_significant_changes(threshold=5.0):
        print("\n   ⚠️  Significant changes detected!")

    # Export to DataFrame for analysis
    print("\n4. Exporting to DataFrame...")
    df = archive.export_to_dataframe()
    print(f"   DataFrame shape: {df.shape}")
    print(f"   Columns: {list(df.columns)}")

    return archive, results


def demo_5_model_operations(model: PowerSystemModel):
    """Demo 5: Model operations (N-1 modifications)."""
    print("\n" + "="*60)
    print("DEMO 5: Model Operations (N-1 Modifications)")
    print("="*60)

    print("\n1. Original model:")
    print(f"   Buses: {len(model.buses)}")
    print(f"   Branches: {len(model.branches)}")

    # Create N-1 model by removing a branch
    print("\n2. Creating N-1 model (remove 'Line 2-3')...")
    n1_model = model.with_branch_removed("Line 2-3")

    print(f"   New model name: {n1_model.name}")
    print(f"   Buses: {len(n1_model.buses)} (unchanged)")
    print(f"   Branches: {len(n1_model.branches)} (was {len(model.branches)})")

    # Verify branch was removed
    removed_branch_exists = any(
        br.name == "Line 2-3" for br in n1_model.branches
    )
    print(f"   Removed branch exists: {removed_branch_exists}")

    # DataFrame views for analysis
    print("\n3. DataFrame views:")
    print(f"   Buses DataFrame shape: {model.buses_df.shape}")
    print(f"   Branches DataFrame shape: {model.branches_df.shape}")

    # Voltage statistics
    voltages = model.buses_df["v_magnitude_pu"].dropna()
    print(f"\n   Voltage statistics:")
    print(f"     Mean: {voltages.mean():.4f} p.u.")
    print(f"     Std:  {voltages.std():.4f} p.u.")
    print(f"     Min:  {voltages.min():.4f} p.u.")
    print(f"     Max:  {voltages.max():.4f} p.u.")


def main():
    """Run all demos."""
    print("\n" + "="*60)
    print("New Architecture Demonstration")
    print("CloudPSS Skills V2 - DataClass-based Design")
    print("="*60)

    # Create temporary directory for demo
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        try:
            # Run demos
            model = demo_1_create_system_model()
            cloudpss_caps, pandapower_caps = demo_2_engine_capabilities()
            store, effective = demo_3_configuration_management(temp_path)
            archive, results = demo_4_result_archival(temp_path, model)
            demo_5_model_operations(model)

            print("\n" + "="*60)
            print("✅ All demos completed successfully!")
            print("="*60)
            print("\nKey benefits demonstrated:")
            print("  1. Type-safe DataClass model with physical validation")
            print("  2. Engine capability declaration and discovery")
            print("  3. Hierarchical configuration (base → project → study)")
            print("  4. HDF5-based result archival with querying")
            print("  5. Model modifications for N-1 analysis")
            print("\nArchitecture ready for implementation!")

        except Exception as e:
            print(f"\n❌ Demo failed: {e}")
            import traceback
            traceback.print_exc()
            return 1

    return 0


if __name__ == "__main__":
    exit(main())
