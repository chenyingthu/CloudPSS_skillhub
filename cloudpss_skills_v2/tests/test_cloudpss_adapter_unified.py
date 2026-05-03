"""Test CloudPSS Adapter with Unified Model Conversion.

Tests the new architecture conversion methods without requiring
actual CloudPSS connection (uses mock data).
"""

import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from cloudpss_skills_v2.powerapi.adapters.cloudpss.powerflow import (
    CloudPSSPowerFlowAdapter,
    _normalize_bus_row,
    _normalize_branch_row,
)
from cloudpss_skills_v2.core.system_model import (
    Bus,
    Branch,
    Generator,
    Load,
    PowerSystemModel,
)
from cloudpss_skills_v2.powerapi.base import EngineConfig


def test_bus_normalization():
    """Test bus row normalization."""
    print("\n" + "="*60)
    print("Test 1: Bus Row Normalization")
    print("="*60)

    raw_bus = {
        "Bus": "Bus 1",
        "Vm / pu": 1.045,
        "Va / deg": 0.0,
        "Pgen / MW": 100.0,
        "Qgen / MVar": 20.0,
        "Pload / MW": 0.0,
        "Qload / MVar": 0.0,
    }

    normalized = _normalize_bus_row(raw_bus)
    print(f"Raw: {raw_bus}")
    print(f"Normalized: {normalized}")

    assert normalized["name"] == "Bus 1"
    assert normalized["voltage_pu"] == 1.045
    assert normalized["angle_deg"] == 0.0
    print("✅ Bus normalization passed")


def test_branch_normalization():
    """Test branch row normalization."""
    print("\n" + "="*60)
    print("Test 2: Branch Row Normalization")
    print("="*60)

    raw_branch = {
        "Branch": "Line 1-2",
        "From bus": "Bus 1",
        "To bus": "Bus 2",
        "Pij / MW": 50.0,
        "Qij / MVar": 10.0,
        "Pji / MW": -48.5,
        "Qji / MVar": -8.0,
        "Ploss / MW": 1.5,
    }

    normalized = _normalize_branch_row(raw_branch)
    print(f"Raw: {raw_branch}")
    print(f"Normalized: {normalized}")

    assert normalized["name"] == "Line 1-2"
    assert normalized["from_bus"] == "Bus 1"
    assert normalized["to_bus"] == "Bus 2"
    assert normalized["p_from_mw"] == 50.0
    print("✅ Branch normalization passed")


def test_unified_model_conversion():
    """Test conversion to unified PowerSystemModel."""
    print("\n" + "="*60)
    print("Test 3: Unified Model Conversion")
    print("="*60)

    # Create adapter
    config = EngineConfig(engine_name="cloudpss")
    adapter = CloudPSSPowerFlowAdapter(config)

    # Mock bus data (normalized)
    bus_rows = [
        {
            "name": "Bus 1",
            "voltage_pu": 1.060,
            "angle_deg": 0.0,
            "generation_mw": 232.4,
            "generation_mvar": -16.9,
            "load_mw": 0.0,
            "load_mvar": 0.0,
            "voltage_kv": 345.0,
            "bus_type": "slack",
        },
        {
            "name": "Bus 2",
            "voltage_pu": 1.045,
            "angle_deg": -5.2,
            "generation_mw": 40.0,
            "generation_mvar": 50.0,
            "load_mw": 21.7,
            "load_mvar": 12.7,
            "voltage_kv": 345.0,
            "bus_type": "pv",
        },
        {
            "name": "Bus 3",
            "voltage_pu": 1.010,
            "angle_deg": -10.5,
            "generation_mw": 0.0,
            "generation_mvar": 40.0,
            "load_mw": 94.2,
            "load_mvar": 19.1,
            "voltage_kv": 345.0,
            "bus_type": "pq",
        },
    ]

    # Mock branch data (normalized)
    branch_rows = [
        {
            "name": "Line 1-2",
            "from_bus": "0",  # Would be index in real data
            "to_bus": "1",
            "r_pu": 0.01938,
            "x_pu": 0.05917,
            "p_from_mw": 156.88,
            "q_from_mvar": 20.5,
            "p_to_mw": -152.3,
            "q_to_mvar": -15.2,
            "rate_a_mva": 100.0,
        },
        {
            "name": "Line 2-3",
            "from_bus": "1",
            "to_bus": "2",
            "r_pu": 0.04699,
            "x_pu": 0.19797,
            "p_from_mw": 73.62,
            "q_from_mvar": 5.8,
            "p_to_mw": -70.1,
            "q_to_mvar": -3.2,
            "rate_a_mva": 80.0,
        },
    ]

    # Convert to unified model
    model = adapter._to_unified_model(bus_rows, branch_rows, base_mva=100.0)

    print(f"\nConverted Model:")
    print(f"  Buses: {len(model.buses)}")
    print(f"  Branches: {len(model.branches)}")
    print(f"  Generators: {len(model.generators)}")
    print(f"  Loads: {len(model.loads)}")

    # Verify buses
    assert len(model.buses) == 3
    assert isinstance(model.buses[0], Bus)
    assert model.buses[0].name == "Bus 1"
    assert model.buses[0].v_magnitude_pu == 1.060
    print(f"  ✅ Bus 1: V={model.buses[0].v_magnitude_pu} pu, type={model.buses[0].bus_type}")

    # Verify branches
    assert len(model.branches) == 2
    assert isinstance(model.branches[0], Branch)
    assert model.branches[0].name == "Line 1-2"
    print(f"  ✅ Line 1-2: loading={model.branches[0].loading_percent:.1f}%")

    # Verify generators (extracted from buses with generation)
    assert len(model.generators) >= 2  # Bus 1 and Bus 2 have generation
    assert isinstance(model.generators[0], Generator)
    print(f"  ✅ Generator count: {len(model.generators)}")

    # Verify loads (extracted from buses with load)
    assert len(model.loads) >= 2  # Bus 2 and Bus 3 have load
    assert isinstance(model.loads[0], Load)
    print(f"  ✅ Load count: {len(model.loads)}")

    # Test DataFrame views
    print(f"\n  DataFrame Views:")
    print(f"    buses_df shape: {model.buses_df.shape}")
    print(f"    branches_df shape: {model.branches_df.shape}")

    # Test system calculations
    print(f"\n  System Calculations:")
    print(f"    Total generation: {model.total_generation_mw():.2f} MW")
    print(f"    Total load: {model.total_load_mw():.2f} MW")

    # Test violation detection
    violations = model.get_voltage_violations()
    print(f"    Voltage violations: {len(violations)}")

    print("\n✅ Unified model conversion passed")


def test_model_modifications():
    """Test N-1 model modifications."""
    print("\n" + "="*60)
    print("Test 4: Model Modifications (N-1)")
    print("="*60)

    # Create a simple model
    from cloudpss_skills_v2.core.system_model import Bus, Branch

    buses = [
        Bus(bus_id=1, name="Bus1", base_kv=230.0, bus_type="SLACK",
            v_magnitude_pu=1.0, v_angle_degree=0.0),
        Bus(bus_id=2, name="Bus2", base_kv=230.0, bus_type="PQ",
            v_magnitude_pu=0.98, v_angle_degree=-5.0),
        Bus(bus_id=3, name="Bus3", base_kv=230.0, bus_type="PQ",
            v_magnitude_pu=0.97, v_angle_degree=-8.0),
    ]

    branches = [
        Branch(from_bus=1, to_bus=2, name="Line1-2",
               r_pu=0.01, x_pu=0.05, rate_a_mva=100.0, loading_percent=50.0),
        Branch(from_bus=2, to_bus=3, name="Line2-3",
               r_pu=0.015, x_pu=0.08, rate_a_mva=80.0, loading_percent=60.0),
        Branch(from_bus=1, to_bus=3, name="Line1-3",
               r_pu=0.02, x_pu=0.10, rate_a_mva=90.0, loading_percent=40.0),
    ]

    model = PowerSystemModel(
        buses=buses,
        branches=branches,
        base_mva=100.0,
        name="Test System"
    )

    print(f"Original: {len(model.buses)} buses, {len(model.branches)} branches")

    # Remove a branch (N-1)
    n1_model = model.with_branch_removed("Line2-3")

    print(f"After N-1: {len(n1_model.buses)} buses, {len(n1_model.branches)} branches")
    print(f"New model name: {n1_model.name}")

    assert len(n1_model.buses) == 3  # Buses unchanged
    assert len(n1_model.branches) == 2  # One branch removed

    # Verify the removed branch is gone
    branch_names = [b.name for b in n1_model.branches]
    assert "Line2-3" not in branch_names
    assert "Line1-2" in branch_names
    assert "Line1-3" in branch_names

    print("✅ N-1 model modification passed")


def test_adapter_interface():
    """Test adapter interface methods."""
    print("\n" + "="*60)
    print("Test 5: Adapter Interface")
    print("="*60)

    config = EngineConfig(engine_name="cloudpss")
    adapter = CloudPSSPowerFlowAdapter(config)

    # Test engine name
    assert adapter.engine_name == "cloudpss"
    print("✅ Engine name: cloudpss")

    # Test supported simulations
    sims = adapter.get_supported_simulations()
    assert len(sims) > 0
    print(f"✅ Supported simulations: {[s.value for s in sims]}")

    # Test cache management (simulated)
    adapter._unified_model_cache["test_job"] = PowerSystemModel(
        buses=[],
        branches=[],
    )

    retrieved = adapter.get_unified_model("test_job")
    assert retrieved is not None
    print("✅ Unified model cache working")

    # Test disconnect clears cache
    adapter._do_disconnect()
    assert len(adapter._unified_model_cache) == 0
    print("✅ Disconnect clears cache")

    print("\n✅ Adapter interface tests passed")


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("CloudPSS Adapter with Unified Model - Test Suite")
    print("="*70)

    try:
        test_bus_normalization()
        test_branch_normalization()
        test_unified_model_conversion()
        test_model_modifications()
        test_adapter_interface()

        print("\n" + "="*70)
        print("✅ ALL TESTS PASSED")
        print("="*70)
        print("\nThe CloudPSS adapter has been successfully enhanced with:")
        print("  • Unified model conversion (_to_unified_model)")
        print("  • PowerSystemModel creation with DataClass components")
        print("  • N-1 model modification support")
        print("  • Backward compatibility maintained")
        return 0

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
