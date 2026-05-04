"""Test Voltage Stability Analysis with Unified PowerSystemModel.

Tests the refactored VoltageStabilityAnalysis skill that uses unified model methods.
"""

import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from cloudpss_skills_v2.core.system_model import (
    Bus,
    Branch,
    Load,
    PowerSystemModel,
)


def test_voltage_stability_runs_on_unified_model():
    """Test that VoltageStabilityAnalysis runs on unified PowerSystemModel."""
    from cloudpss_skills_v2.poweranalysis.voltage_stability import VoltageStabilityAnalysis

    print("\n" + "="*60)
    print("Test: VoltageStabilityAnalysis on Unified Model")
    print("="*60)

    # Create a simple test system with 2 buses
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK",
                v_magnitude_pu=1.0, v_angle_degree=0.0),
            Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ",
                v_magnitude_pu=0.98, v_angle_degree=-2.0),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="Line1", branch_type="LINE",
                   r_pu=0.01, x_pu=0.1, rate_a_mva=100.0)
        ],
        loads=[
            Load(bus_id=1, name="Load1", p_mw=50, q_mvar=10)
        ],
        base_mva=100.0
    )

    print(f"Created model: {len(model.buses)} buses, {len(model.branches)} branches, {len(model.loads)} loads")

    # Run voltage stability analysis
    analysis = VoltageStabilityAnalysis()
    result = analysis.run(model, {
        "load_scaling": [1.0, 1.2, 1.4, 1.6, 1.8, 2.0],
        "monitor_buses": ["Bus2"]
    })

    print(f"Result status: {result.get('status', 'unknown')}")
    print(f"Result keys: {list(result.keys())}")

    # Verify results
    assert result["status"] == "success", f"Expected status 'success', got '{result.get('status')}'"
    assert "pv_curve" in result, "Expected 'pv_curve' in result"
    assert "critical_point" in result, "Expected 'critical_point' in result"
    assert result["analysis_mode"] == "screening_proxy"
    assert result["confidence_level"] == "screening_proxy_not_cpf"
    assert result["limitations"]
    assert "continuation power-flow" in result["standard_basis"]

    # Print PV curve data
    pv_curve = result["pv_curve"]
    print(f"PV curve points: {len(pv_curve)}")
    for point in pv_curve[:3]:  # Print first 3 points
        print(f"  Scale {point.get('scale', '?'):.1f}x: V = {point.get('voltage', '?'):.4f} pu")

    print(f"Critical point: {result.get('critical_point', 'N/A')}")

    print("✅ VoltageStabilityAnalysis unified model test passed")


def test_voltage_stability_model_validation():
    """Test that VoltageStabilityAnalysis validates the model before running."""
    from cloudpss_skills_v2.poweranalysis.voltage_stability import VoltageStabilityAnalysis

    print("\n" + "="*60)
    print("Test: VoltageStabilityAnalysis Model Validation")
    print("="*60)

    # Create a model without slack bus (should fail validation)
    model_no_slack = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="PQ"),
            Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ"),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="Line1", branch_type="LINE",
                   r_pu=0.01, x_pu=0.1, rate_a_mva=100.0)
        ],
        loads=[
            Load(bus_id=1, name="Load1", p_mw=50, q_mvar=10)
        ],
        base_mva=100.0
    )

    analysis = VoltageStabilityAnalysis()
    result = analysis.run(model_no_slack, {
        "load_scaling": [1.0, 1.2],
        "monitor_buses": ["Bus2"]
    })

    # Should fail due to missing slack bus
    assert result["status"] == "error", f"Expected status 'error' for invalid model, got '{result.get('status')}'"
    assert "error" in result, "Expected 'error' key in result"

    print(f"Correctly detected missing slack bus: {result.get('error', 'unknown error')}")
    print("✅ VoltageStabilityAnalysis validation test passed")


def test_voltage_stability_collapse_detection():
    """Test that VoltageStabilityAnalysis detects voltage collapse point."""
    from cloudpss_skills_v2.poweranalysis.voltage_stability import VoltageStabilityAnalysis

    print("\n" + "="*60)
    print("Test: VoltageStabilityAnalysis Collapse Detection")
    print("="*60)

    # Create a heavily loaded system that will show voltage collapse
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK",
                v_magnitude_pu=1.0, v_angle_degree=0.0),
            Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ",
                v_magnitude_pu=0.95, v_angle_degree=-5.0),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="Line1", branch_type="LINE",
                   r_pu=0.02, x_pu=0.2, rate_a_mva=100.0)
        ],
        loads=[
            Load(bus_id=1, name="Load1", p_mw=80, q_mvar=20)  # Heavy load
        ],
        base_mva=100.0
    )

    analysis = VoltageStabilityAnalysis()
    result = analysis.run(model, {
        "load_scaling": [1.0, 1.5, 2.0, 2.5, 3.0],
        "monitor_buses": ["Bus2"],
        "collapse_threshold": 0.7
    })

    print(f"Result status: {result.get('status', 'unknown')}")
    print(f"Critical point: {result.get('critical_point', 'N/A')}")
    print(f"Max loadability: {result.get('max_loadability', 'N/A')}")

    # Should succeed and have PV curve data
    assert result["status"] == "success", f"Expected status 'success', got '{result.get('status')}'"
    assert "pv_curve" in result, "Expected 'pv_curve' in result"
    assert len(result["pv_curve"]) > 0, "Expected PV curve to have data points"

    print("✅ VoltageStabilityAnalysis collapse detection test passed")


def test_voltage_stability_marks_singular_ybus_screening_path():
    """Singular topology should be reported as approximate screening, not hidden."""
    from cloudpss_skills_v2.poweranalysis.voltage_stability import VoltageStabilityAnalysis

    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Slack", base_kv=230.0, bus_type="SLACK", v_magnitude_pu=1.0),
            Bus(bus_id=1, name="Load", base_kv=230.0, bus_type="PQ", v_magnitude_pu=0.98),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="ZeroZ", branch_type="LINE", r_pu=0.0, x_pu=0.0),
        ],
        loads=[Load(bus_id=1, name="L1", p_mw=30, q_mvar=5)],
        base_mva=100.0,
    )

    result = VoltageStabilityAnalysis().run(model, {"load_scaling": [1.0]})

    assert result["status"] == "success"
    assert result["used_singular_ybus_approximation"] is True
    assert result["analysis_mode"] == "screening_proxy"


def test_voltage_stability_can_run_pandapower_ac_scan():
    """Optional pandapower mode should use AC runpp results, not screening estimates."""
    from cloudpss_skills_v2.poweranalysis.voltage_stability import VoltageStabilityAnalysis

    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Slack", base_kv=110.0, bus_type="SLACK", v_magnitude_pu=1.0),
            Bus(bus_id=1, name="Load", base_kv=110.0, bus_type="PQ", v_magnitude_pu=0.99),
        ],
        branches=[
            Branch(
                from_bus=0,
                to_bus=1,
                name="Line1",
                branch_type="LINE",
                r_pu=0.01,
                x_pu=0.08,
                rate_a_mva=100.0,
            ),
        ],
        loads=[Load(bus_id=1, name="L1", p_mw=20, q_mvar=5)],
        base_mva=100.0,
    )

    result = VoltageStabilityAnalysis().run(
        model,
        {
            "method": "pandapower_ac",
            "load_scaling": [1.0, 1.2],
            "monitor_buses": ["Load"],
        },
    )

    assert result["status"] == "success"
    assert result["analysis_mode"] == "pandapower_ac_power_flow_scan"
    assert result["confidence_level"] == "ac_power_flow_scan_not_cpf"
    assert result["used_singular_ybus_approximation"] is False
    assert len(result["pv_curve"]) == 2
    assert all(point["source"] == "pandapower_ac" for point in result["pv_curve"])


def test_voltage_stability_matpower_cpf_reports_missing_runtime(monkeypatch):
    """MATPOWER CPF mode should fail explicitly when optional runtime is absent."""
    from cloudpss_skills_v2.poweranalysis.voltage_stability import VoltageStabilityAnalysis
    from cloudpss_skills_v2.powerapi.adapters.matpower_cpf import (
        MatpowerCPFAdapter,
        MatpowerCPFUnavailable,
    )

    def unavailable(_self, _model, *, target_scale=2.0, load_bus_ids=None):
        raise MatpowerCPFUnavailable("forced unavailable")

    model = PowerSystemModel(
        buses=[
            Bus(bus_id=1, name="Slack", base_kv=230.0, bus_type="SLACK", v_magnitude_pu=1.0),
            Bus(bus_id=2, name="Load", base_kv=230.0, bus_type="PQ", v_magnitude_pu=0.98),
        ],
        branches=[
            Branch(from_bus=1, to_bus=2, name="Line1", branch_type="LINE", r_pu=0.01, x_pu=0.1),
        ],
        loads=[Load(bus_id=2, name="L1", p_mw=50, q_mvar=10)],
        base_mva=100.0,
    )

    monkeypatch.setattr(MatpowerCPFAdapter, "run_cpf", unavailable)
    result = VoltageStabilityAnalysis().run(
        model,
        {"method": "matpower_cpf", "target_scale": 2.0, "monitor_buses": ["Load"]},
    )

    assert result["status"] == "error"
    assert result["analysis_mode"] == "matpower_cpf_unavailable"
    assert "MATPOWER" in result["standard_basis"]
    assert "matpower_runtime" in result


def test_voltage_stability_matpower_cpf_reports_solver_failure(monkeypatch):
    """MATPOWER runtime failures should not be reported as missing runtime."""
    from cloudpss_skills_v2.poweranalysis.voltage_stability import VoltageStabilityAnalysis
    from cloudpss_skills_v2.powerapi.adapters.matpower_cpf import MatpowerCPFAdapter

    def failed(_self, _model, *, target_scale=2.0, load_bus_ids=None):
        raise RuntimeError("forced solver failure")

    model = PowerSystemModel(
        buses=[
            Bus(bus_id=1, name="Slack", base_kv=230.0, bus_type="SLACK", v_magnitude_pu=1.0),
            Bus(bus_id=2, name="Load", base_kv=230.0, bus_type="PQ", v_magnitude_pu=0.98),
        ],
        branches=[
            Branch(from_bus=1, to_bus=2, name="Line1", branch_type="LINE", r_pu=0.01, x_pu=0.1),
        ],
        loads=[Load(bus_id=2, name="L1", p_mw=50, q_mvar=10)],
        base_mva=100.0,
    )

    monkeypatch.setattr(MatpowerCPFAdapter, "run_cpf", failed)
    result = VoltageStabilityAnalysis().run(
        model,
        {"method": "matpower_cpf", "target_scale": 2.0, "monitor_buses": ["Load"]},
    )

    assert result["status"] == "error"
    assert result["analysis_mode"] == "matpower_cpf_failed"
    assert "forced solver failure" in result["error"]


if __name__ == "__main__":
    test_voltage_stability_runs_on_unified_model()
    test_voltage_stability_model_validation()
    test_voltage_stability_collapse_detection()
    print("\n" + "="*60)
    print("All voltage stability unified tests passed!")
    print("="*60)
