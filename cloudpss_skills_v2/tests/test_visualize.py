import os
import pytest
import tempfile
from pathlib import Path

import h5py
from cloudpss_skills_v2.tools.visualize import VisualizeTool
from cloudpss_skills_v2.tools.visualize import validate_data_path


class TestVisualizeTool:
    def test_validate_data_path_accepts_allowed_json_file(self, tmp_path, monkeypatch):
        allowed_home = tmp_path / "home"
        monkeypatch.setattr(Path, "home", lambda: allowed_home)

        data_dir = allowed_home / "cloudpss_data"
        data_dir.mkdir(parents=True)
        data_file = data_dir / "result.json"
        data_file.write_text('{"time": [1, 2], "values": [3, 4]}', encoding="utf-8")

        assert validate_data_path(str(data_file)) == data_file.resolve()

    def test_validate_data_path_rejects_path_traversal_attack(self, tmp_path, monkeypatch):
        allowed_home = tmp_path / "home"
        monkeypatch.setattr(Path, "home", lambda: allowed_home)

        attack_path = "/data/../../../etc/passwd"

        with pytest.raises(ValueError, match="outside allowed directories"):
            validate_data_path(attack_path)

    def test_validate_data_path_rejects_non_absolute_path(self, tmp_path, monkeypatch):
        allowed_home = tmp_path / "home"
        monkeypatch.setattr(Path, "home", lambda: allowed_home)

        with pytest.raises(ValueError, match="absolute path"):
            validate_data_path("relative/data.json")

    def test_validate_data_path_rejects_directory(self, tmp_path, monkeypatch):
        allowed_home = tmp_path / "home"
        monkeypatch.setattr(Path, "home", lambda: allowed_home)

        data_dir = allowed_home / "cloudpss_data"
        data_dir.mkdir(parents=True)

        with pytest.raises(ValueError, match="must point to a file"):
            validate_data_path(str(data_dir))

    def test_validate_data_path_rejects_disallowed_extension(self, tmp_path, monkeypatch):
        allowed_home = tmp_path / "home"
        monkeypatch.setattr(Path, "home", lambda: allowed_home)

        data_dir = allowed_home / "cloudpss_data"
        data_dir.mkdir(parents=True)
        script_file = data_dir / "script.py"
        script_file.write_text("print('unsafe')", encoding="utf-8")

        with pytest.raises(ValueError, match="Unsupported data file extension"):
            validate_data_path(str(script_file))

    def test_validate_data_path_rejects_missing_file(self, tmp_path, monkeypatch):
        allowed_home = tmp_path / "home"
        monkeypatch.setattr(Path, "home", lambda: allowed_home)

        missing_file = allowed_home / "cloudpss_data" / "missing.json"

        with pytest.raises(ValueError, match="does not exist"):
            validate_data_path(str(missing_file))

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

    def test_load_data_from_data_file_json(self, tmp_path, monkeypatch):
        allowed_home = tmp_path / "home"
        monkeypatch.setattr(Path, "home", lambda: allowed_home)

        data_dir = allowed_home / "cloudpss_data"
        data_dir.mkdir(parents=True)
        data_file = data_dir / "result.json"
        data_file.write_text('{"bus_voltages": {"B1": 1.0}}', encoding="utf-8")

        instance = VisualizeTool()
        data = instance._load_data({"source": {"data_file": str(data_file)}})

        assert data == {"bus_voltages": {"B1": 1.0}}

    def test_load_data_from_data_file_csv(self, tmp_path, monkeypatch):
        allowed_home = tmp_path / "home"
        monkeypatch.setattr(Path, "home", lambda: allowed_home)

        data_dir = allowed_home / "cloudpss_data"
        data_dir.mkdir(parents=True)
        data_file = data_dir / "result.csv"
        data_file.write_text("time,value\n1,10\n2,20\n", encoding="utf-8")

        instance = VisualizeTool()
        data = instance._load_data({"source": {"data_file": str(data_file)}})

        assert data == {"rows": [{"time": "1", "value": "10"}, {"time": "2", "value": "20"}]}

    def test_load_data_from_data_file_hdf5(self, tmp_path, monkeypatch):
        allowed_home = tmp_path / "home"
        monkeypatch.setattr(Path, "home", lambda: allowed_home)

        data_dir = allowed_home / "cloudpss_data"
        data_dir.mkdir(parents=True)
        data_file = data_dir / "result.h5"
        with h5py.File(data_file, "w") as handle:
            handle.create_dataset("values", data=[1.0, 2.0, 3.0])

        instance = VisualizeTool()
        data = instance._load_data({"source": {"data_file": str(data_file)}})

        assert data == {"values": [1.0, 2.0, 3.0]}

    def test_load_data_from_data_file_rejects_path_traversal(self, tmp_path, monkeypatch):
        allowed_home = tmp_path / "home"
        monkeypatch.setattr(Path, "home", lambda: allowed_home)

        instance = VisualizeTool()

        with pytest.raises(ValueError, match="outside allowed directories"):
            instance._load_data({"source": {"data_file": "/data/../../../etc/passwd"}})

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
