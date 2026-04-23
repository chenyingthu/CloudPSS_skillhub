"""Tests for cloudpss_skills_v2.poweranalysis.thevenin_equivalent."""

import math

import pytest

from cloudpss_skills_v2.poweranalysis.thevenin_equivalent import (
    TheveninEquivalentAnalysis,
)


class TestTheveninEquivalentAnalysis:
    @pytest.fixture
    def instance(self):
        return TheveninEquivalentAnalysis()

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_import(self):
        assert TheveninEquivalentAnalysis is not None

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_class_attributes(self):
        assert hasattr(TheveninEquivalentAnalysis, "name")
        assert TheveninEquivalentAnalysis.name == "thevenin_equivalent"
        assert hasattr(TheveninEquivalentAnalysis, "description")

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_config_schema(self):
        instance = TheveninEquivalentAnalysis()
        schema = instance.config_schema
        assert isinstance(schema, dict)
        assert "properties" in schema

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_instantiation(self):
        instance = TheveninEquivalentAnalysis()
        assert instance is not None

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_instance_attributes(self):
        instance = TheveninEquivalentAnalysis()
        assert hasattr(instance, "logs")
        assert hasattr(instance, "artifacts")
        assert hasattr(instance, "run")
        assert hasattr(instance, "validate")
        assert hasattr(instance, "_calculate_impedance_magnitude")
        assert hasattr(instance, "_calculate_scc")
        assert hasattr(instance, "_calculate_scr")


class TestCalculateImpedanceMagnitude:
    @pytest.fixture
    def instance(self):
        return TheveninEquivalentAnalysis()

    def test_pure_resistive(self, instance):
        result = instance._calculate_impedance_magnitude(r=3.0, x=0.0)
        assert result == 3.0

    def test_pure_reactive(self, instance):
        result = instance._calculate_impedance_magnitude(r=0.0, x=4.0)
        assert result == 4.0

    def test_combined_impedance(self, instance):
        result = instance._calculate_impedance_magnitude(r=3.0, x=4.0)
        assert result == 5.0

    def test_typical_values(self, instance):
        r = 0.01
        x = 0.05
        expected = math.sqrt(0.01**2 + 0.05**2)
        result = instance._calculate_impedance_magnitude(r=r, x=x)
        assert math.isclose(result, expected, rel_tol=1e-10)

    def test_zero_impedance(self, instance):
        result = instance._calculate_impedance_magnitude(r=0.0, x=0.0)
        assert result == 0.0

    def test_high_r_low_x(self, instance):
        result = instance._calculate_impedance_magnitude(r=0.1, x=0.01)
        expected = math.sqrt(0.1**2 + 0.01**2)
        assert math.isclose(result, expected, rel_tol=1e-10)

    def test_high_x_low_r(self, instance):
        result = instance._calculate_impedance_magnitude(r=0.01, x=0.1)
        expected = math.sqrt(0.01**2 + 0.1**2)
        assert math.isclose(result, expected, rel_tol=1e-10)


class TestCalculateSCC:
    @pytest.fixture
    def instance(self):
        return TheveninEquivalentAnalysis()

    def test_standard_case(self, instance):
        voltage_kv = 110.0
        z_pu = 0.05
        base_mva = 100.0
        result = instance._calculate_scc(voltage_kv, z_pu, base_mva)
        assert math.isclose(result, 2000.0, rel_tol=1e-6)

    def test_ten_percent_impedance(self, instance):
        result = instance._calculate_scc(voltage_kv=110.0, z_pu=0.10, base_mva=100.0)
        assert math.isclose(result, 1000.0, rel_tol=1e-6)

    def test_twenty_percent_impedance(self, instance):
        result = instance._calculate_scc(voltage_kv=110.0, z_pu=0.20, base_mva=100.0)
        assert math.isclose(result, 500.0, rel_tol=1e-6)

    def test_inf_on_zero_impedance(self, instance):
        result = instance._calculate_scc(voltage_kv=110.0, z_pu=0.0, base_mva=100.0)
        assert result == float("inf")

    def test_inf_on_negative_impedance(self, instance):
        result = instance._calculate_scc(voltage_kv=110.0, z_pu=-0.05, base_mva=100.0)
        assert result == float("inf")

    def test_different_voltage(self, instance):
        result_110 = instance._calculate_scc(
            voltage_kv=110.0, z_pu=0.05, base_mva=100.0
        )
        result_220 = instance._calculate_scc(
            voltage_kv=220.0, z_pu=0.05, base_mva=100.0
        )
        assert math.isclose(result_110, result_220, rel_tol=1e-6)

    def test_different_base_mva(self, instance):
        result = instance._calculate_scc(voltage_kv=110.0, z_pu=0.05, base_mva=50.0)
        assert math.isclose(result, 1000.0, rel_tol=1e-6)

    def test_very_low_impedance(self, instance):
        result = instance._calculate_scc(voltage_kv=110.0, z_pu=0.01, base_mva=100.0)
        assert math.isclose(result, 10000.0, rel_tol=1e-6)


class TestCalculateSCR:
    @pytest.fixture
    def instance(self):
        return TheveninEquivalentAnalysis()

    def test_standard_case(self, instance):
        result = instance._calculate_scr(scc_mva=2000.0, rated_power_mw=1000.0)
        assert result == 2.0

    def test_strong_grid(self, instance):
        result = instance._calculate_scr(scc_mva=5000.0, rated_power_mw=1000.0)
        assert result == 5.0

    def test_weak_grid(self, instance):
        result = instance._calculate_scr(scc_mva=1000.0, rated_power_mw=1000.0)
        assert result == 1.0

    def test_moderate_grid(self, instance):
        result = instance._calculate_scr(scc_mva=2500.0, rated_power_mw=1000.0)
        assert result == 2.5

    def test_inf_on_zero_rated_power(self, instance):
        result = instance._calculate_scr(scc_mva=2000.0, rated_power_mw=0.0)
        assert result == float("inf")

    def test_inf_on_negative_rated_power(self, instance):
        result = instance._calculate_scr(scc_mva=2000.0, rated_power_mw=-1000.0)
        assert result == float("inf")

    def test_high_scc_low_load(self, instance):
        result = instance._calculate_scr(scc_mva=10000.0, rated_power_mw=500.0)
        assert result == 20.0

    def test_scc_equals_load(self, instance):
        result = instance._calculate_scr(scc_mva=1000.0, rated_power_mw=1000.0)
        assert result == 1.0


class TestValidate:
    @pytest.fixture
    def instance(self):
        return TheveninEquivalentAnalysis()

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_valid_config(self, instance):
        config = {
            "model": {"rid": "test_model"},
            "pcc": {"bus": "BUS1"},
        }
        valid, errors = instance.validate(config)
        assert valid is True
        assert len(errors) == 0

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_missing_model(self, instance):
        config = {
            "pcc": {"bus": "BUS1"},
        }
        valid, errors = instance.validate(config)
        assert valid is False
        assert len(errors) > 0

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_missing_model_rid(self, instance):
        config = {
            "model": {},
            "pcc": {"bus": "BUS1"},
        }
        valid, errors = instance.validate(config)
        assert valid is False
        assert any("model.rid" in e for e in errors)

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_missing_pcc(self, instance):
        config = {
            "model": {"rid": "test_model"},
        }
        valid, errors = instance.validate(config)
        assert valid is False
        assert len(errors) > 0

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_missing_pcc_bus(self, instance):
        config = {
            "model": {"rid": "test_model"},
            "pcc": {},
        }
        valid, errors = instance.validate(config)
        assert valid is False
        assert any("pcc.bus" in e for e in errors)

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_none_config(self, instance):
        valid, errors = instance.validate(None)
        assert valid is False
        assert len(errors) > 0

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_empty_config(self, instance):
        valid, errors = instance.validate({})
        assert valid is False
        assert len(errors) > 0

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_valid_with_base_mva(self, instance):
        config = {
            "model": {"rid": "test_model"},
            "pcc": {"bus": "BUS1", "base_mva": 50},
        }
        valid, errors = instance.validate(config)
        assert valid is True

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_valid_with_engine(self, instance):
        config = {
            "model": {"rid": "test_model"},
            "pcc": {"bus": "BUS1"},
            "engine": "pandapower",
        }
        valid, errors = instance.validate(config)
        assert valid is True
