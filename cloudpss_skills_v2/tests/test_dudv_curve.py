import pytest
import numpy as np
from cloudpss_skills_v2.poweranalysis.dudv_curve import DUDVCurveAnalysis


class TestDUDVCurveAnalysis:
    def test_import(self):
        assert DUDVCurveAnalysis is not None

    def test_instantiation(self):
        instance = DUDVCurveAnalysis()
        assert instance is not None

    def test_has_name_attribute(self):
        instance = DUDVCurveAnalysis()
        assert instance.name == "dudv_curve"

    def test_has_description(self):
        instance = DUDVCurveAnalysis()
        assert hasattr(instance, "description")

    def test_has_config_schema(self):
        instance = DUDVCurveAnalysis()
        schema = instance.config_schema
        assert schema is not None
        assert schema["type"] == "object"

    def test_has_validate_method(self):
        instance = DUDVCurveAnalysis()
        assert hasattr(instance, "validate")
        assert callable(instance.validate)

    def test_has_run_method(self):
        instance = DUDVCurveAnalysis()
        assert hasattr(instance, "run")
        assert callable(instance.run)

    def test_validate_empty_config(self):
        instance = DUDVCurveAnalysis()
        valid, errors = instance.validate({})
        assert valid is False
        assert len(errors) > 0

    def test_validate_missing_rid(self):
        instance = DUDVCurveAnalysis()
        config = {"model": {}}
        valid, errors = instance.validate(config)
        assert valid is False
        assert "model.rid" in "".join(errors)

    def test_validate_valid_config(self):
        instance = DUDVCurveAnalysis()
        config = {"model": {"rid": "test_model"}}
        valid, errors = instance.validate(config)
        assert valid is True
        assert len(errors) == 0

    def test_compute_dudv_points_basic(self):
        instance = DUDVCurveAnalysis()
        v_base = 1.0
        v_range = [0.9, 1.1]
        num_points = 5
        result = instance._compute_dudv_points(v_base, v_range, num_points)
        assert len(result) == num_points
        assert "voltage" in result[0]
        assert "dU" in result[0]
        assert "dV" in result[0]

    def test_compute_dudv_points_zero_at_steady(self):
        instance = DUDVCurveAnalysis()
        v_base = 1.0
        v_range = [0.9, 1.1]
        num_points = 5
        result = instance._compute_dudv_points(v_base, v_range, num_points)
        voltages = [r["voltage"] for r in result]
        idx = np.argmin(np.abs(np.array(voltages) - v_base))
        dV_at_base = result[idx]["dV"]
        assert abs(dV_at_base) < 0.01

    def test_extract_dudv_from_result(self):
        instance = DUDVCurveAnalysis()
        bus_voltage = 1.05
        v_base = 1.0
        result = instance._extract_dudv_from_result(bus_voltage, v_base)
        assert result["voltage"] == 1.05
        assert "dU" in result
        assert "dV" in result

    def test_extract_dudv_low_voltage(self):
        instance = DUDVCurveAnalysis()
        bus_voltage = 0.85
        v_base = 1.0
        result = instance._extract_dudv_from_result(bus_voltage, v_base)
        assert result["dV"] < 0

    def test_extract_dudv_high_voltage(self):
        instance = DUDVCurveAnalysis()
        bus_voltage = 1.15
        v_base = 1.0
        result = instance._extract_dudv_from_result(bus_voltage, v_base)
        assert result["dV"] > 0

    def test_identify_stability_boundary_with_crossing(self):
        instance = DUDVCurveAnalysis()
        voltages = [0.8, 0.9, 1.0, 1.1, 1.2]
        dVs = [10.0, 5.0, 0.0, -3.0, -8.0]
        result = instance._identify_stability_boundary(voltages, dVs)
        assert result["boundary_voltage"] is not None

    def test_identify_stability_boundary_no_crossing(self):
        instance = DUDVCurveAnalysis()
        voltages = [0.95, 0.97, 0.99, 1.01, 1.03]
        dVs = [2.0, 1.0, 0.5, 0.2, 0.1]
        result = instance._identify_stability_boundary(voltages, dVs)
        assert result["boundary_voltage"] is not None

    def test_identify_stability_boundary_empty(self):
        instance = DUDVCurveAnalysis()
        result = instance._identify_stability_boundary([], [])
        assert result["boundary_voltage"] is None

    def test_run_returns_skill_result(self):
        instance = DUDVCurveAnalysis()
        config = {"model": {"rid": "test"}}
        result = instance.run(config)
        assert result is not None
        assert hasattr(result, "skill_name")
        assert hasattr(result, "status")

    def test_run_with_invalid_config(self):
        instance = DUDVCurveAnalysis()
        result = instance.run({})
        assert result.status.value == "failed" or result.status.name == "failed"

    def test_has_log_method(self):
        instance = DUDVCurveAnalysis()
        assert hasattr(instance, "_log")
        assert callable(instance._log)
