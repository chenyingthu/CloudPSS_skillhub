import os
import pytest
import tempfile
from cloudpss_skills_v2.tools.visualize import VisualizeTool


class TestVisualizeTool:
    def test_import(self):
        assert VisualizeTool is not None

    def test_instantiation(self):
        instance = VisualizeTool()
        assert instance is not None

    def test_has_name_attribute(self):
        instance = VisualizeTool()
        assert instance.name == "visualize"

    def test_has_description(self):
        instance = VisualizeTool()
        assert hasattr(instance, "description")

    def test_has_config_schema(self):
        instance = VisualizeTool()
        schema = instance.config_schema
        assert schema is not None
        assert schema["type"] == "object"

    def test_validate_empty_config(self):
        instance = VisualizeTool()
        valid, errors = instance.validate({})
        assert valid is False

    def test_validate_missing_rid(self):
        instance = VisualizeTool()
        config = {"model": {}}
        valid, errors = instance.validate(config)
        assert valid is False

    def test_validate_valid_config(self):
        instance = VisualizeTool()
        config = {"model": {"rid": "test_model"}}
        valid, errors = instance.validate(config)
        assert valid is True

    def test_load_data_from_direct_data(self):
        instance = VisualizeTool()
        config = {"data": {"time": [1, 2, 3], "values": [10, 20, 30]}}
        data = instance._load_data(config)
        assert data["time"] == [1, 2, 3]
        assert data["values"] == [10, 20, 30]

    def test_load_data_from_result(self):
        instance = VisualizeTool()
        config = {"result": {"bus_voltages": {"B1": 1.0, "B2": 1.02}}}
        data = instance._load_data(config)
        assert "bus_voltages" in data
        assert data["bus_voltages"]["B1"] == 1.0

    def test_load_data_from_source(self):
        instance = VisualizeTool()
        config = {"source": {"data": {"time": [1, 2]}}}
        data = instance._load_data(config)
        assert data["time"] == [1, 2]

    def test_load_data_empty(self):
        instance = VisualizeTool()
        config = {}
        data = instance._load_data(config)
        assert data == {}

    def test_plot_time_series_with_valid_data(self):
        instance = VisualizeTool()
        data = {"time": [0, 1, 2, 3], "values": [10, 20, 15, 10]}
        with tempfile.TemporaryDirectory() as out_dir:
            paths = instance._plot_time_series(data, out_dir)
            assert "png" in paths
            assert os.path.exists(paths["png"])

    def test_plot_time_series_with_mismatched_lengths(self):
        instance = VisualizeTool()
        data = {"time": [0, 1], "values": [10, 20, 30, 40]}
        with tempfile.TemporaryDirectory() as out_dir:
            paths = instance._plot_time_series(data, out_dir)
            assert os.path.exists(paths["png"])

    def test_plot_time_series_empty_data(self):
        instance = VisualizeTool()
        data = {}
        with tempfile.TemporaryDirectory() as out_dir:
            paths = instance._plot_time_series(data, out_dir)
            assert paths == {}

    def test_plot_bus_voltages_with_valid_data(self):
        instance = VisualizeTool()
        data = {"bus_voltages": {"B1": 1.0, "B2": 1.02, "B3": 0.98}}
        with tempfile.TemporaryDirectory() as out_dir:
            paths = instance._plot_bus_voltages(data, out_dir)
            assert "png" in paths
            assert os.path.exists(paths["png"])

    def test_plot_bus_voltages_empty_data(self):
        instance = VisualizeTool()
        data = {}
        with tempfile.TemporaryDirectory() as out_dir:
            paths = instance._plot_bus_voltages(data, out_dir)
            assert paths == {}

    def test_plot_bus_voltages_invalid_type(self):
        instance = VisualizeTool()
        data = {"bus_voltages": "not_a_dict"}
        with tempfile.TemporaryDirectory() as out_dir:
            paths = instance._plot_bus_voltages(data, out_dir)
            assert paths == {}

    def test_plot_branch_flows_with_valid_data(self):
        instance = VisualizeTool()
        data = {"branch_flows": {"L1": 100, "L2": 150, "L3": 80}}
        with tempfile.TemporaryDirectory() as out_dir:
            paths = instance._plot_branch_flows(data, out_dir)
            assert "png" in paths
            assert os.path.exists(paths["png"])

    def test_plot_branch_flows_empty_data(self):
        instance = VisualizeTool()
        data = {}
        with tempfile.TemporaryDirectory() as out_dir:
            paths = instance._plot_branch_flows(data, out_dir)
            assert paths == {}

    def test_run_returns_skill_result(self):
        instance = VisualizeTool()
        result = instance.run(
            {"model": {"rid": "test"}, "data": {"time": [1, 2], "values": [10, 20]}}
        )
        assert result is not None
        assert hasattr(result, "skill_name")

    def test_run_with_invalid_config(self):
        instance = VisualizeTool()
        result = instance.run({})
        assert result.status.value == "failed" or result.status.name == "failed"

    def test_has_log_method(self):
        instance = VisualizeTool()
        assert hasattr(instance, "_log")
        assert callable(instance._log)
