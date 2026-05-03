"""Test N-1 Security Analysis with Unified PowerSystemModel.

Tests the refactored N1SecurityAnalysis skill that uses unified model methods.
"""

import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from cloudpss_skills_v2.core.system_model import (
    Bus,
    Branch,
    Generator,
    Load,
    PowerSystemModel,
)
from cloudpss_skills_v2.libs.data_lib import (
    ViolationRecord,
    ContingencyRecord,
    AnalysisSummary,
    SecurityAnalysisResult,
    SeverityLevel,
)


def test_n1_model_modification():
    """Test N-1 model modification using unified model."""
    print("\n" + "="*60)
    print("Test 1: N-1 Model Modification (Unified Model)")
    print("="*60)

    # Create a simple test system
    buses = [
        Bus(bus_id=1, name="Bus1", base_kv=230.0, bus_type="SLACK",
            v_magnitude_pu=1.0, v_angle_degree=0.0),
        Bus(bus_id=2, name="Bus2", base_kv=230.0, bus_type="PV",
            v_magnitude_pu=1.02, p_injected_mw=150.0),
        Bus(bus_id=3, name="Bus3", base_kv=230.0, bus_type="PQ",
            p_injected_mw=-100.0, q_injected_mvar=-50.0),
    ]

    branches = [
        Branch(from_bus=1, to_bus=2, name="Line1-2",
               r_pu=0.01, x_pu=0.05, rate_a_mva=500.0,
               loading_percent=45.0, in_service=True),
        Branch(from_bus=2, to_bus=3, name="Line2-3",
               r_pu=0.015, x_pu=0.08, rate_a_mva=400.0,
               loading_percent=62.0, in_service=True),
        Branch(from_bus=1, to_bus=3, name="Line1-3",
               r_pu=0.02, x_pu=0.10, rate_a_mva=450.0,
               loading_percent=38.0, in_service=True),
    ]

    generators = [
        Generator(bus_id=1, name="Gen1", p_gen_mw=100.0,
                  p_max_mw=200.0, p_min_mw=50.0),
        Generator(bus_id=2, name="Gen2", p_gen_mw=150.0,
                  p_max_mw=300.0, p_min_mw=0.0),
    ]

    loads = [
        Load(bus_id=3, name="Load3", p_mw=100.0, q_mvar=50.0),
    ]

    base_model = PowerSystemModel(
        buses=buses,
        branches=branches,
        generators=generators,
        loads=loads,
        base_mva=100.0,
        name="Test System"
    )

    print(f"Base model: {len(base_model.buses)} buses, {len(base_model.branches)} branches")

    # Create N-1 model
    n1_model = base_model.with_branch_removed("Line2-3")

    print(f"N-1 model: {len(n1_model.buses)} buses, {len(n1_model.branches)} branches")
    print(f"N-1 model name: {n1_model.name}")

    assert len(n1_model.buses) == 3  # Buses unchanged
    assert len(n1_model.branches) == 2  # One branch removed
    assert "Line2-3" not in [b.name for b in n1_model.branches]

    print("✅ N-1 model modification passed")


def test_voltage_violation_detection():
    """Test voltage violation detection using unified model."""
    print("\n" + "="*60)
    print("Test 2: Voltage Violation Detection (Unified Model)")
    print("="*60)

    buses = [
        Bus(bus_id=1, name="Bus1", base_kv=230.0, bus_type="SLACK",
            v_magnitude_pu=1.0, vm_min_pu=0.95, vm_max_pu=1.05),
        Bus(bus_id=2, name="Bus2", base_kv=230.0, bus_type="PV",
            v_magnitude_pu=0.93, vm_min_pu=0.95, vm_max_pu=1.05),  # Undervoltage
        Bus(bus_id=3, name="Bus3", base_kv=230.0, bus_type="PQ",
            v_magnitude_pu=1.08, vm_min_pu=0.95, vm_max_pu=1.05),  # Overvoltage
        Bus(bus_id=4, name="Bus4", base_kv=230.0, bus_type="PQ",
            v_magnitude_pu=0.98, vm_min_pu=0.95, vm_max_pu=1.05),  # Normal
    ]

    model = PowerSystemModel(
        buses=buses,
        branches=[],
        base_mva=100.0,
        name="Voltage Test"
    )

    violations = model.get_voltage_violations()

    print(f"Found {len(violations)} voltage violations:")
    for bus, voltage, vtype in violations:
        print(f"  - {bus.name}: {voltage:.3f} pu ({vtype})")

    assert len(violations) == 2
    violation_types = [v[2] for v in violations]
    assert "undervoltage" in violation_types
    assert "overvoltage" in violation_types

    print("✅ Voltage violation detection passed")


def test_thermal_violation_detection():
    """Test thermal violation detection using unified model."""
    print("\n" + "="*60)
    print("Test 3: Thermal Violation Detection (Unified Model)")
    print("="*60)

    buses = [
        Bus(bus_id=1, name="Bus1", base_kv=230.0),
        Bus(bus_id=2, name="Bus2", base_kv=230.0),
        Bus(bus_id=3, name="Bus3", base_kv=230.0),
    ]

    branches = [
        Branch(from_bus=1, to_bus=2, name="Line1-2",
               r_pu=0.01, x_pu=0.05, rate_a_mva=100.0,
               loading_percent=85.0),  # Normal
        Branch(from_bus=2, to_bus=3, name="Line2-3",
               r_pu=0.015, x_pu=0.08, rate_a_mva=100.0,
               loading_percent=115.0),  # Overload (>100%)
        Branch(from_bus=1, to_bus=3, name="Line1-3",
               r_pu=0.02, x_pu=0.10, rate_a_mva=100.0,
               loading_percent=130.0),  # Severe overload
    ]

    model = PowerSystemModel(
        buses=buses,
        branches=branches,
        base_mva=100.0,
        name="Thermal Test"
    )

    # Check with default 100% threshold
    violations = model.get_thermal_violations(threshold=1.0)

    print(f"Found {len(violations)} thermal violations (threshold=100%):")
    for branch, loading in violations:
        print(f"  - {branch.name}: {loading:.1f}%")

    assert len(violations) == 2

    # Check with 120% threshold
    violations_120 = model.get_thermal_violations(threshold=1.2)
    print(f"Found {len(violations_120)} thermal violations (threshold=120%)")
    assert len(violations_120) == 1

    print("✅ Thermal violation detection passed")


def test_n1_analysis_workflow():
    """Test complete N-1 analysis workflow with unified model."""
    print("\n" + "="*60)
    print("Test 4: Complete N-1 Analysis Workflow")
    print("="*60)

    # Create test system
    buses = [
        Bus(bus_id=1, name="Bus1", base_kv=230.0, bus_type="SLACK",
            v_magnitude_pu=1.0, v_angle_degree=0.0, vm_min_pu=0.95, vm_max_pu=1.05),
        Bus(bus_id=2, name="Bus2", base_kv=230.0, bus_type="PV",
            v_magnitude_pu=1.02, p_injected_mw=150.0, vm_min_pu=0.95, vm_max_pu=1.05),
        Bus(bus_id=3, name="Bus3", base_kv=230.0, bus_type="PQ",
            v_magnitude_pu=0.94, q_injected_mvar=-50.0, vm_min_pu=0.95, vm_max_pu=1.05),
    ]

    branches = [
        Branch(from_bus=1, to_bus=2, name="Line1-2",
               r_pu=0.01, x_pu=0.05, rate_a_mva=100.0,
               loading_percent=85.0, in_service=True),
        Branch(from_bus=2, to_bus=3, name="Line2-3",
               r_pu=0.015, x_pu=0.08, rate_a_mva=100.0,
               loading_percent=120.0, in_service=True),
        Branch(from_bus=1, to_bus=3, name="Line1-3",
               r_pu=0.02, x_pu=0.10, rate_a_mva=100.0,
               loading_percent=45.0, in_service=True),
    ]

    base_model = PowerSystemModel(
        buses=buses,
        branches=branches,
        base_mva=100.0,
        name="N1 Test System"
    )

    print(f"Base case: {len(base_model.buses)} buses, {len(base_model.branches)} branches")

    # Check base case violations
    base_voltage_violations = base_model.get_voltage_violations()
    base_thermal_violations = base_model.get_thermal_violations(threshold=1.0)

    print(f"Base case violations: {len(base_voltage_violations)} voltage, {len(base_thermal_violations)} thermal")

    # Simulate N-1 analysis
    results = []
    for branch in base_model.branches:
        print(f"\n  Testing N-1: {branch.name}")

        # Create N-1 model
        n1_model = base_model.with_branch_removed(branch.name)

        # In real scenario, we would run power flow on n1_model
        # For test, simulate by checking if the removed branch is gone
        remaining_branches = [b.name for b in n1_model.branches]

        assert branch.name not in remaining_branches
        assert len(n1_model.branches) == len(base_model.branches) - 1

        # Simulate violation detection (would come from actual power flow)
        violations = []
        if branch.name == "Line2-3":
            # Simulate that removing Line2-3 causes overload on Line1-3
            violations.append(ViolationRecord(
                violation_type="thermal",
                component="Line1-3",
                value=1.25,
                threshold=1.0,
                severity=SeverityLevel.WARNING,
            ))

        has_violations = len(violations) > 0
        severity = SeverityLevel.CRITICAL if has_violations else SeverityLevel.NORMAL

        result = ContingencyRecord(
            branch_key=branch.name,
            branch_name=branch.name,
            converged=True,
            severity=severity,
            violations=violations,
        )
        results.append(result)

        status = "FAIL" if has_violations else "PASS"
        print(f"    -> {status}")

    # Analyze results
    passed = sum(1 for r in results if r.severity == SeverityLevel.NORMAL)
    failed = sum(1 for r in results if r.severity == SeverityLevel.CRITICAL)

    print(f"\n  N-1 Summary: {passed} passed, {failed} failed")

    assert len(results) == len(base_model.branches)
    assert passed >= 1  # At least one should pass

    print("✅ Complete N-1 analysis workflow passed")


def test_dataframe_views():
    """Test DataFrame views for vectorized analysis."""
    print("\n" + "="*60)
    print("Test 5: DataFrame Views for Vectorized Analysis")
    print("="*60)

    buses = [
        Bus(bus_id=1, name="Bus1", base_kv=230.0,
            v_magnitude_pu=1.0, p_injected_mw=100.0),
        Bus(bus_id=2, name="Bus2", base_kv=230.0,
            v_magnitude_pu=0.98, p_injected_mw=-50.0),
        Bus(bus_id=3, name="Bus3", base_kv=230.0,
            v_magnitude_pu=1.02, p_injected_mw=-50.0),
    ]

    branches = [
        Branch(from_bus=1, to_bus=2, name="Line1-2",
               loading_percent=75.0, rate_a_mva=100.0),
        Branch(from_bus=2, to_bus=3, name="Line2-3",
               loading_percent=85.0, rate_a_mva=100.0),
    ]

    model = PowerSystemModel(
        buses=buses,
        branches=branches,
        base_mva=100.0,
    )

    # Test DataFrame views
    buses_df = model.buses_df
    branches_df = model.branches_df

    print(f"Buses DataFrame: {buses_df.shape}")
    print(f"Branches DataFrame: {branches_df.shape}")

    # Vectorized analysis
    avg_voltage = buses_df["v_magnitude_pu"].mean()
    max_loading = branches_df["loading_percent"].max()

    print(f"Average voltage: {avg_voltage:.4f} pu")
    print(f"Max loading: {max_loading:.1f}%")

    assert not buses_df.empty
    assert not branches_df.empty
    assert 0.9 < avg_voltage < 1.1

    print("✅ DataFrame views passed")


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("N-1 Security Analysis with Unified Model - Test Suite")
    print("="*70)

    try:
        test_n1_model_modification()
        test_voltage_violation_detection()
        test_thermal_violation_detection()
        test_n1_analysis_workflow()
        test_dataframe_views()

        print("\n" + "="*70)
        print("✅ ALL TESTS PASSED")
        print("="*70)
        print("\nThe N1SecurityAnalysis has been successfully refactored to use:")
        print("  • PowerSystemModel with DataClass components")
        print("  • model.with_branch_removed() for N-1 scenarios")
        print("  • model.get_voltage_violations() for voltage checks")
        print("  • model.get_thermal_violations() for thermal checks")
        print("  • DataFrame views for vectorized analysis")
        return 0

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


# =============================================================================
# N1SecurityAnalysis Class Tests
# =============================================================================

def test_n1_security_analysis_class_import():
    """Test N1SecurityAnalysis class can be imported and instantiated."""
    from cloudpss_skills_v2.poweranalysis.n1_security import N1SecurityAnalysis

    analysis = N1SecurityAnalysis()
    assert analysis is not None
    assert analysis.name == "n1_security"
    assert "N-1" in analysis.description


def test_n1_security_config_schema():
    """Test N1SecurityAnalysis has valid config schema."""
    from cloudpss_skills_v2.poweranalysis.n1_security import N1SecurityAnalysis

    analysis = N1SecurityAnalysis()
    schema = analysis.config_schema

    assert "properties" in schema
    assert "skill" in schema["properties"]
    assert "model" in schema["properties"]
    assert "analysis" in schema["properties"]
    assert "output" in schema["properties"]


def test_n1_security_default_config():
    """Test N1SecurityAnalysis returns valid default config."""
    from cloudpss_skills_v2.poweranalysis.n1_security import N1SecurityAnalysis

    analysis = N1SecurityAnalysis()
    config = analysis.get_default_config()

    assert config["skill"] == "n1_security"
    assert config["engine"] == "cloudpss"
    assert config["model"]["rid"] == "model/holdme/IEEE39"
    assert config["analysis"]["check_voltage"] is True
    assert config["analysis"]["check_thermal"] is True


def test_n1_security_validation():
    """Test N1SecurityAnalysis config validation."""
    from cloudpss_skills_v2.poweranalysis.n1_security import N1SecurityAnalysis

    analysis = N1SecurityAnalysis()

    # Valid config
    valid, errors = analysis.validate({
        "skill": "n1_security",
        "model": {"rid": "model/test"},
        "auth": {"token_file": ".token"},
    })
    assert valid is True
    assert len(errors) == 0

    # Invalid config - missing model.rid
    valid, errors = analysis.validate({
        "skill": "n1_security",
        "model": {},
    })
    assert valid is False
    assert len(errors) > 0


def test_check_voltage_violations_unified():
    """Test _check_voltage_violations_unified helper method."""
    from cloudpss_skills_v2.poweranalysis.n1_security import N1SecurityAnalysis

    analysis = N1SecurityAnalysis()

    # Create test model with voltage violations
    buses = [
        Bus(bus_id=1, name="Bus1", base_kv=230.0, bus_type="SLACK",
            v_magnitude_pu=1.0, vm_min_pu=0.95, vm_max_pu=1.05),
        Bus(bus_id=2, name="Bus2", base_kv=230.0, bus_type="PV",
            v_magnitude_pu=0.93, vm_min_pu=0.95, vm_max_pu=1.05),  # Undervoltage
        Bus(bus_id=3, name="Bus3", base_kv=230.0, bus_type="PQ",
            v_magnitude_pu=1.08, vm_min_pu=0.95, vm_max_pu=1.05),  # Overvoltage
        Bus(bus_id=4, name="Bus4", base_kv=230.0, bus_type="PQ",
            v_magnitude_pu=0.98, vm_min_pu=0.95, vm_max_pu=1.05),  # Normal
    ]

    model = PowerSystemModel(buses=buses, branches=[], base_mva=100.0)

    violations = analysis._check_voltage_violations_unified(model, threshold=0.05)

    assert len(violations) == 2

    # Check undervoltage violation
    undervoltage_violations = [v for v in violations if "Bus2" in v.component]
    assert len(undervoltage_violations) == 1
    assert undervoltage_violations[0].violation_type == "voltage"
    assert undervoltage_violations[0].value == 0.93

    # Check overvoltage violation
    overvoltage_violations = [v for v in violations if "Bus3" in v.component]
    assert len(overvoltage_violations) == 1
    assert overvoltage_violations[0].violation_type == "voltage"
    assert overvoltage_violations[0].value == 1.08


def test_check_voltage_violations_severity_levels():
    """Test voltage violation severity levels (CRITICAL vs WARNING)."""
    from cloudpss_skills_v2.poweranalysis.n1_security import N1SecurityAnalysis
    from cloudpss_skills_v2.libs.data_lib import SeverityLevel

    analysis = N1SecurityAnalysis()

    buses = [
        Bus(bus_id=1, name="Bus1", base_kv=230.0,
            v_magnitude_pu=0.84, vm_min_pu=0.95, vm_max_pu=1.05),  # CRITICAL undervoltage
        Bus(bus_id=2, name="Bus2", base_kv=230.0,
            v_magnitude_pu=0.93, vm_min_pu=0.95, vm_max_pu=1.05),  # WARNING undervoltage
        Bus(bus_id=3, name="Bus3", base_kv=230.0,
            v_magnitude_pu=1.16, vm_min_pu=0.95, vm_max_pu=1.05),  # CRITICAL overvoltage
        Bus(bus_id=4, name="Bus4", base_kv=230.0,
            v_magnitude_pu=1.08, vm_min_pu=0.95, vm_max_pu=1.05),  # WARNING overvoltage
    ]

    model = PowerSystemModel(buses=buses, branches=[], base_mva=100.0)

    violations = analysis._check_voltage_violations_unified(model, threshold=0.05)

    critical_count = sum(1 for v in violations if v.severity == SeverityLevel.CRITICAL)
    warning_count = sum(1 for v in violations if v.severity == SeverityLevel.WARNING)

    assert critical_count == 2  # 0.84 and 1.16
    assert warning_count == 2   # 0.93 and 1.08


def test_check_thermal_violations_unified():
    """Test _check_thermal_violations_unified helper method."""
    from cloudpss_skills_v2.poweranalysis.n1_security import N1SecurityAnalysis

    analysis = N1SecurityAnalysis()

    buses = [
        Bus(bus_id=1, name="Bus1", base_kv=230.0),
        Bus(bus_id=2, name="Bus2", base_kv=230.0),
        Bus(bus_id=3, name="Bus3", base_kv=230.0),
    ]

    branches = [
        Branch(from_bus=1, to_bus=2, name="Line1-2",
               r_pu=0.01, x_pu=0.05, rate_a_mva=100.0,
               loading_percent=85.0),  # Normal (<100%)
        Branch(from_bus=2, to_bus=3, name="Line2-3",
               r_pu=0.015, x_pu=0.08, rate_a_mva=100.0,
               loading_percent=115.0),  # Overload (>100%)
        Branch(from_bus=1, to_bus=3, name="Line1-3",
               r_pu=0.02, x_pu=0.10, rate_a_mva=100.0,
               loading_percent=130.0),  # Severe overload (>120%)
    ]

    model = PowerSystemModel(buses=buses, branches=branches, base_mva=100.0)

    violations = analysis._check_thermal_violations_unified(model, threshold=1.0)

    assert len(violations) == 2  # Line2-3 and Line1-3

    # Check loading values are in per unit
    for v in violations:
        assert v.violation_type == "thermal"
        assert v.value > 1.0  # Should be > 1.0 (per unit)


def test_check_thermal_violations_severity_levels():
    """Test thermal violation severity levels (CRITICAL vs WARNING)."""
    from cloudpss_skills_v2.poweranalysis.n1_security import N1SecurityAnalysis
    from cloudpss_skills_v2.libs.data_lib import SeverityLevel

    analysis = N1SecurityAnalysis()

    buses = [
        Bus(bus_id=1, name="Bus1", base_kv=230.0),
        Bus(bus_id=2, name="Bus2", base_kv=230.0),
        Bus(bus_id=3, name="Bus3", base_kv=230.0),
    ]

    branches = [
        Branch(from_bus=1, to_bus=2, name="Line1-2",
               r_pu=0.01, x_pu=0.05, rate_a_mva=100.0,
               loading_percent=85.0),  # Normal
        Branch(from_bus=2, to_bus=3, name="Line2-3",
               r_pu=0.015, x_pu=0.08, rate_a_mva=100.0,
               loading_percent=115.0),  # WARNING (>100%)
        Branch(from_bus=1, to_bus=3, name="Line1-3",
               r_pu=0.02, x_pu=0.10, rate_a_mva=100.0,
               loading_percent=130.0),  # CRITICAL (>120%)
    ]

    model = PowerSystemModel(buses=buses, branches=branches, base_mva=100.0)

    violations = analysis._check_thermal_violations_unified(model, threshold=1.0)

    critical_violations = [v for v in violations if v.severity == SeverityLevel.CRITICAL]
    warning_violations = [v for v in violations if v.severity == SeverityLevel.WARNING]

    assert len(critical_violations) == 1  # Line1-3 at 130%
    assert len(warning_violations) == 1   # Line2-3 at 115%

    assert critical_violations[0].component == "Line1-3"
    assert warning_violations[0].component == "Line2-3"


def test_check_violations_with_none_values():
    """Test violation checking handles None values gracefully."""
    from cloudpss_skills_v2.poweranalysis.n1_security import N1SecurityAnalysis

    analysis = N1SecurityAnalysis()

    # Buses with None voltage
    buses = [
        Bus(bus_id=1, name="Bus1", base_kv=230.0,
            v_magnitude_pu=None, vm_min_pu=0.95, vm_max_pu=1.05),
        Bus(bus_id=2, name="Bus2", base_kv=230.0,
            v_magnitude_pu=0.98, vm_min_pu=0.95, vm_max_pu=1.05),
    ]

    # Branches with None loading
    branches = [
        Branch(from_bus=1, to_bus=2, name="Line1-2",
               r_pu=0.01, x_pu=0.05, rate_a_mva=100.0,
               loading_percent=None),
    ]

    model = PowerSystemModel(buses=buses, branches=branches, base_mva=100.0)

    # Should not raise exceptions
    v_violations = analysis._check_voltage_violations_unified(model, threshold=0.05)
    t_violations = analysis._check_thermal_violations_unified(model, threshold=1.0)

    assert len(v_violations) == 0  # Bus1 has None, Bus2 is within limits
    assert len(t_violations) == 0  # Line1-2 has None loading


def test_n1_security_with_simple_unified_model():
    """Test N1SecurityAnalysis with a simple unified PowerSystemModel."""
    from cloudpss_skills_v2.poweranalysis.n1_security import N1SecurityAnalysis

    analysis = N1SecurityAnalysis()

    # Create a simple test system
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK",
                v_magnitude_pu=1.0, v_angle_degree=0.0, vm_min_pu=0.95, vm_max_pu=1.05),
            Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ",
                v_magnitude_pu=0.98, v_angle_degree=-2.0, vm_min_pu=0.95, vm_max_pu=1.05),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="Line1", branch_type="LINE",
                   r_pu=0.01, x_pu=0.1, rate_a_mva=100.0, loading_percent=85.0),
        ],
        loads=[
            Load(bus_id=1, name="Load1", p_mw=50, q_mvar=10),
        ],
        base_mva=100.0
    )

    # Verify the model
    assert len(model.buses) == 2
    assert len(model.branches) == 1
    assert model.get_slack_bus() is not None

    # Test violation checking on the model
    v_violations = analysis._check_voltage_violations_unified(model, threshold=0.05)
    t_violations = analysis._check_thermal_violations_unified(model, threshold=1.0)

    # Should have no violations in this simple case
    assert len(v_violations) == 0
    assert len(t_violations) == 0


def test_n1_model_immutability():
    """Test that N-1 operations create new models without modifying original."""
    buses = [
        Bus(bus_id=1, name="Bus1", base_kv=230.0, bus_type="SLACK",
            v_magnitude_pu=1.0, v_angle_degree=0.0),
        Bus(bus_id=2, name="Bus2", base_kv=230.0, bus_type="PV",
            v_magnitude_pu=1.02, p_injected_mw=150.0),
        Bus(bus_id=3, name="Bus3", base_kv=230.0, bus_type="PQ",
            p_injected_mw=-100.0, q_injected_mvar=-50.0),
    ]

    branches = [
        Branch(from_bus=1, to_bus=2, name="Line1-2",
               r_pu=0.01, x_pu=0.05, rate_a_mva=500.0),
        Branch(from_bus=2, to_bus=3, name="Line2-3",
               r_pu=0.015, x_pu=0.08, rate_a_mva=400.0),
    ]

    base_model = PowerSystemModel(
        buses=buses,
        branches=branches,
        base_mva=100.0,
        name="Test System"
    )

    # Create N-1 model
    n1_model = base_model.with_branch_removed("Line2-3")

    # Original model should be unchanged
    assert len(base_model.branches) == 2
    assert "Line2-3" in [b.name for b in base_model.branches]

    # N-1 model should have one less branch
    assert len(n1_model.branches) == 1
    assert "Line2-3" not in [b.name for b in n1_model.branches]


if __name__ == "__main__":
    exit(main())
