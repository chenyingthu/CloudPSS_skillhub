"""Tests for cloudpss_skills_v2.tools.waveform_export."""

import json

import pytest

from cloudpss_skills_v2.tools.waveform_export import WaveformExportTool


class TestWaveformExportTool:
    @pytest.fixture
    def instance(self):
        return WaveformExportTool()

    def test_import(self):
        assert WaveformExportTool is not None

    def test_class_attributes(self):
        assert hasattr(WaveformExportTool, "name")
        assert WaveformExportTool.name == "waveform_export"

    def test_instantiation(self):
        instance = WaveformExportTool()
        assert instance is not None

    def test_instance_attributes(self):
        instance = WaveformExportTool()
        assert hasattr(instance, "logs")
        assert hasattr(instance, "artifacts")
        assert hasattr(instance, "validate")
        assert hasattr(instance, "get_default_config")
        assert hasattr(instance, "_format_csv")
        assert hasattr(instance, "_format_json")


class TestGetDefaultConfig:
    @pytest.fixture
    def instance(self):
        return WaveformExportTool()

    def test_returns_dict(self, instance):
        result = instance.get_default_config()
        assert isinstance(result, dict)

    def test_has_skill(self, instance):
        result = instance.get_default_config()
        assert "skill" in result
        assert result["skill"] == "waveform_export"

    def test_has_source(self, instance):
        result = instance.get_default_config()
        assert "source" in result
        assert "job_id" in result["source"]

    def test_has_export(self, instance):
        result = instance.get_default_config()
        assert "export" in result

    def test_has_output(self, instance):
        result = instance.get_default_config()
        assert "output" in result
        assert "format" in result["output"]
        assert result["output"]["format"] == "csv"


class TestValidate:
    @pytest.fixture
    def instance(self):
        return WaveformExportTool()

    def test_missing_job_id(self, instance):
        config = {
            "source": {},
            "export": {"channels": []},
            "output": {"format": "csv"},
        }
        valid, errors = instance.validate(config)
        assert valid is False

    def test_empty_job_id(self, instance):
        config = {"source": {"job_id": ""}}
        valid, errors = instance.validate(config)
        assert valid is False

    def test_placeholder_job_id(self, instance):
        config = {"source": {"job_id": "your_job_id_here"}}
        valid, errors = instance.validate(config)
        assert valid is False

    def test_none_config(self, instance):
        valid, errors = instance.validate(None)
        assert valid is False

    def test_empty_config(self, instance):
        valid, errors = instance.validate({})
        assert valid is False


class TestFormatCSV:
    @pytest.fixture
    def instance(self):
        return WaveformExportTool()

    def test_empty_inputs(self, instance):
        result = instance._format_csv(time=None, data=None)
        assert result == ""

    def test_empty_time(self, instance):
        result = instance._format_csv(time=[], data={"ch1": [1, 2, 3]})
        assert result == ""

    def test_empty_data(self, instance):
        result = instance._format_csv(time=[1, 2, 3], data={})
        assert result == ""

    def test_single_channel(self, instance):
        time = [0.0, 0.1, 0.2]
        data = {"voltage": [1.0, 1.1, 1.2]}
        result = instance._format_csv(time=time, data=data)
        lines = result.split("\n")
        assert lines[0] == "time,voltage"
        assert lines[1] == "0.0,1.0"
        assert lines[2] == "0.1,1.1"
        assert lines[3] == "0.2,1.2"

    def test_multiple_channels(self, instance):
        time = [0.0, 0.1]
        data = {"voltage": [1.0, 1.1], "current": [0.5, 0.6]}
        result = instance._format_csv(time=time, data=data)
        lines = result.split("\n")
        assert "time,voltage,current" == lines[0]
        assert "0.0,1.0,0.5" == lines[1]
        assert "0.1,1.1,0.6" == lines[2]

    def test_mismatched_lengths(self, instance):
        time = [0.0, 0.1, 0.2]
        data = {"voltage": [1.0]}
        result = instance._format_csv(time=time, data=data)
        lines = result.split("\n")
        assert "0.0,1.0" == lines[1]
        assert "0.1," == lines[2]
        assert "0.2," == lines[3]


class TestFormatJSON:
    @pytest.fixture
    def instance(self):
        return WaveformExportTool()

    def test_basic_format(self, instance):
        time = [0.0, 0.1, 0.2]
        data = {"voltage": [1.0, 1.1, 1.2]}
        result = instance._format_json(time=time, data=data)
        parsed = json.loads(result)
        assert "time" in parsed
        assert "channels" in parsed
        assert parsed["time"] == [0.0, 0.1, 0.2]
        assert parsed["channels"]["voltage"] == [1.0, 1.1, 1.2]

    def test_multiple_channels(self, instance):
        time = [0.0, 0.1]
        data = {"voltage": [1.0, 1.1], "current": [0.5, 0.6]}
        result = instance._format_json(time=time, data=data)
        parsed = json.loads(result)
        assert "voltage" in parsed["channels"]
        assert "current" in parsed["channels"]

    def test_empty_data(self, instance):
        time = []
        data = {}
        result = instance._format_json(time=time, data=data)
        parsed = json.loads(result)
        assert parsed["time"] == []
        assert parsed["channels"] == {}
