import pytest
import numpy as np
from cloudpss_skills_v2.poweranalysis.frequency_response import (
    FrequencyResponseAnalysis,
)


class TestFrequencyResponseAnalysis:
    def test_import(self):
        assert FrequencyResponseAnalysis is not None

    def test_instantiation(self):
        instance = FrequencyResponseAnalysis()
        assert instance is not None

    def test_has_name_attribute(self):
        instance = FrequencyResponseAnalysis()
        assert instance.name == "frequency_response"

    def test_has_config_schema(self):
        instance = FrequencyResponseAnalysis()
        schema = instance.config_schema
        assert isinstance(schema, dict)
        assert "disturbance" in schema["properties"]

    def test_get_default_config_is_valid(self):
        instance = FrequencyResponseAnalysis()
        config = instance.get_default_config()
        valid, errors = instance.validate(config)
        assert valid, errors
        assert config["engine"] == "pandapower"
        assert config["model"]["rid"] == "case14"
        assert config["disturbance"]["type"] == "step_load_change"

    def test_validate_empty_config(self):
        instance = FrequencyResponseAnalysis()
        valid, errors = instance.validate({})
        assert valid is False

    def test_validate_missing_rid(self):
        instance = FrequencyResponseAnalysis()
        config = {"model": {}}
        valid, errors = instance.validate(config)
        assert valid is False

    def test_validate_missing_disturbance(self):
        instance = FrequencyResponseAnalysis()
        config = {"model": {"rid": "test"}}
        valid, errors = instance.validate(config)
        assert valid is False

    def test_validate_missing_frequency_trace(self):
        instance = FrequencyResponseAnalysis()
        config = {"model": {"rid": "test"}, "disturbance": {"type": "load_shedding"}}
        valid, errors = instance.validate(config)
        assert valid is False
        assert "frequency_trace.time and frequency_trace.frequency_hz are required" in errors

    def test_validate_valid_config(self):
        instance = FrequencyResponseAnalysis()
        config = {
            "model": {"rid": "test"},
            "disturbance": {"type": "load_shedding"},
            "frequency_trace": {"time": [0, 1], "frequency_hz": [50.0, 49.9]},
        }
        valid, errors = instance.validate(config)
        assert valid is True

    def test_validate_valid_step_load(self):
        instance = FrequencyResponseAnalysis()
        config = {
            "model": {"rid": "test"},
            "disturbance": {"type": "step_load_change", "magnitude": 0.1},
            "frequency_trace": {"time": [0, 1], "frequency_hz": [50.0, 49.9]},
        }
        valid, errors = instance.validate(config)
        assert valid is True

    def test_calculate_nadir(self):
        instance = FrequencyResponseAnalysis()
        freq = np.array([50.0, 49.9, 49.85, 49.95, 50.0])
        nadir = instance._calculate_nadir(freq)
        assert nadir == 49.85

    def test_calculate_nadir_empty(self):
        instance = FrequencyResponseAnalysis()
        freq = np.array([])
        nadir = instance._calculate_nadir(freq)
        assert nadir == 50.0

    def test_calculate_rocof(self):
        instance = FrequencyResponseAnalysis()
        freq = np.array([50.0, 49.95, 49.9])
        time = np.array([0.0, 0.1, 0.2])
        rocof = instance._calculate_rocof(freq, time)
        assert rocof > 0.0

    def test_calculate_recovery_time(self):
        instance = FrequencyResponseAnalysis()
        freq = np.array([50.0, 49.9, 49.95, 49.98, 50.0])
        time = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
        recovery = instance._calculate_recovery_time(freq, time, 50.0)
        assert recovery >= 0.0

    def test_run_returns_skill_result(self):
        instance = FrequencyResponseAnalysis()
        result = instance.run(
            {
                "engine": "pandapower",
                "model": {"rid": "case14", "source": "local"},
                "disturbance": {"type": "load_shedding"},
                "frequency_trace": {
                    "time": [0, 1, 2, 3],
                    "frequency_hz": [50.0, 49.8, 49.9, 50.0],
                },
            }
        )
        assert result is not None
        assert hasattr(result, "skill_name")
        assert result.data["data_source"] == "frequency_trace"
        assert result.data["nadir"] == 49.8

    def test_run_with_invalid_config(self):
        instance = FrequencyResponseAnalysis()
        result = instance.run({})
        assert result.status.value == "failed" or result.status.name == "failed"

    def test_has_log_method(self):
        instance = FrequencyResponseAnalysis()
        assert hasattr(instance, "_log")
        assert callable(instance._log)
