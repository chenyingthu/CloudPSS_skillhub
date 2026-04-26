"""Tests for cloudpss_skills_v2.poweranalysis.reactive_compensation_design."""
import pytest
from cloudpss_skills_v2.poweranalysis.reactive_compensation_design import ReactiveCompensationDesignAnalysis


class TestReactiveCompensationDesignAnalysis:

    def test_import(self):
        """module and class can be imported."""
        assert ReactiveCompensationDesignAnalysis is not None

    def test_instantiation(self):
        """class can be instantiated."""
        instance = ReactiveCompensationDesignAnalysis()
        assert instance is not None

    def test_has_name_attribute(self):
        """instance has expected attributes."""
        instance = ReactiveCompensationDesignAnalysis()
        assert hasattr(instance, 'name') or hasattr(instance, 'run')

    def test_requires_explicit_weak_bus_measurements(self):
        instance = ReactiveCompensationDesignAnalysis()
        valid, errors = instance.validate(
            {
                "model": {"rid": "case14"},
                "weak_buses": [{"bus": "bus:3", "scr": 2.5, "voltage_pu": 0.92}],
            }
        )
        assert valid is False
        assert any(".x_pu is required" in error for error in errors)

    def test_run_uses_explicit_x_pu_for_q_sizing(self):
        instance = ReactiveCompensationDesignAnalysis()
        result = instance.run(
            {
                "model": {"rid": "case14"},
                "weak_buses": [
                    {"bus": "bus:3", "scr": 2.5, "voltage_pu": 0.92, "x_pu": 0.25}
                ],
            }
        )
        assert result.is_success
        assert result.data["data_source"] == "weak_buses"
        rec = result.data["compensation_recommendations"][0]
        assert rec["x_pu"] == 0.25
        assert rec["required_q_mvar"] == 0.29
