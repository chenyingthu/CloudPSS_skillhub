"""Tests for CLI Compare Command.

CLI 比较命令测试。
"""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from cloudpss_skills_v2.cli.commands.compare_cmd import (
    EngineComparator,
    add_parser,
    execute,
)
from cloudpss_skills_v2.powerapi.base import SimulationResult, SimulationStatus


class TestEngineComparator:
    """Test EngineComparator class."""

    def test_init(self):
        """Test EngineComparator initialization."""
        comparator = EngineComparator(
            engines=["cloudpss", "pandapower"],
            model_id="test_model",
            analysis_type="power_flow",
        )
        assert comparator.engines == ["cloudpss", "pandapower"]
        assert comparator.model_id == "test_model"
        assert comparator.analysis_type == "power_flow"
        assert comparator.results == {}
        assert comparator.errors == {}

    @patch("cloudpss_skills_v2.cli.commands.compare_cmd.registry")
    def test_run_single_engine_not_supported(self, mock_registry):
        """Test running on engine that doesn't support analysis type."""
        mock_registry.get.return_value = None

        comparator = EngineComparator(
            engines=["cloudpss"],
            model_id="test_model",
            analysis_type="power_flow",
        )

        result = comparator._run_single_engine("cloudpss")

        assert result is None
        assert "cloudpss" in comparator.errors
        assert "does not support" in comparator.errors["cloudpss"]

    @patch("cloudpss_skills_v2.cli.commands.compare_cmd.registry")
    def test_run_single_engine_success(self, mock_registry):
        """Test successful run on single engine."""
        mock_adapter_cls = MagicMock()
        mock_adapter = MagicMock()
        mock_result = MagicMock()
        mock_result.status = SimulationStatus.COMPLETED
        mock_result.duration_seconds = 1.5
        mock_result.data = {"buses": 10, "branches": 15}
        mock_result.errors = []
        mock_result.warnings = []

        mock_adapter_cls.return_value = mock_adapter
        mock_adapter.load_model.return_value = True
        mock_adapter.run_simulation.return_value = mock_result

        mock_registry.get.return_value = mock_adapter_cls

        comparator = EngineComparator(
            engines=["cloudpss"],
            model_id="test_model",
            analysis_type="power_flow",
        )

        result = comparator._run_single_engine("cloudpss")

        assert result == mock_result
        assert "cloudpss" not in comparator.errors
        mock_adapter.connect.assert_called_once()
        mock_adapter.load_model.assert_called_once_with("test_model")
        mock_adapter.run_simulation.assert_called_once()
        mock_adapter.disconnect.assert_called_once()

    @patch("cloudpss_skills_v2.cli.commands.compare_cmd.registry")
    def test_run_single_engine_load_model_failure(self, mock_registry):
        """Test engine when model loading fails."""
        mock_adapter_cls = MagicMock()
        mock_adapter = MagicMock()

        mock_adapter_cls.return_value = mock_adapter
        mock_adapter.load_model.return_value = False

        mock_registry.get.return_value = mock_adapter_cls

        comparator = EngineComparator(
            engines=["cloudpss"],
            model_id="test_model",
            analysis_type="power_flow",
        )

        result = comparator._run_single_engine("cloudpss")

        assert result is None
        assert "cloudpss" in comparator.errors
        assert "Failed to load model" in comparator.errors["cloudpss"]

    @patch("cloudpss_skills_v2.cli.commands.compare_cmd.registry")
    def test_run_single_engine_exception(self, mock_registry):
        """Test engine when exception occurs."""
        mock_adapter_cls = MagicMock()
        mock_adapter = MagicMock()
        mock_adapter.connect.side_effect = Exception("Connection failed")

        mock_adapter_cls.return_value = mock_adapter
        mock_registry.get.return_value = mock_adapter_cls

        comparator = EngineComparator(
            engines=["cloudpss"],
            model_id="test_model",
            analysis_type="power_flow",
        )

        result = comparator._run_single_engine("cloudpss")

        assert result is None
        assert "cloudpss" in comparator.errors
        assert "Connection failed" in comparator.errors["cloudpss"]

    def test_compare_data_with_differences(self):
        """Test data comparison with differences."""
        result1 = SimulationResult(
            job_id="test1",
            status=SimulationStatus.COMPLETED,
            data={"buses": 10, "branches": 15, "losses": 100.5},
        )
        result2 = SimulationResult(
            job_id="test2",
            status=SimulationStatus.COMPLETED,
            data={"buses": 12, "branches": 15, "losses": 95.3},
        )

        comparator = EngineComparator(
            engines=["cloudpss", "pandapower"],
            model_id="test_model",
            analysis_type="power_flow",
        )

        results = {"cloudpss": result1, "pandapower": result2}
        comparison = comparator._compare_data(results)

        assert comparison["engines_compared"] == ["cloudpss", "pandapower"]
        assert "buses" in comparison["common_keys"]
        assert "branches" in comparison["common_keys"]
        assert len(comparison["differences"]) == 2  # buses and losses differ

        # Check that differences include buses
        bus_diffs = [d for d in comparison["differences"] if d["key"] == "buses"]
        assert len(bus_diffs) == 1
        assert bus_diffs[0]["values"]["cloudpss"] == 10
        assert bus_diffs[0]["values"]["pandapower"] == 12

    def test_compare_data_no_differences(self):
        """Test data comparison with no differences."""
        result1 = SimulationResult(
            job_id="test1",
            status=SimulationStatus.COMPLETED,
            data={"buses": 10, "branches": 15},
        )
        result2 = SimulationResult(
            job_id="test2",
            status=SimulationStatus.COMPLETED,
            data={"buses": 10, "branches": 15},
        )

        comparator = EngineComparator(
            engines=["cloudpss", "pandapower"],
            model_id="test_model",
            analysis_type="power_flow",
        )

        results = {"cloudpss": result1, "pandapower": result2}
        comparison = comparator._compare_data(results)

        assert len(comparison["differences"]) == 0
        assert comparison["common_keys"] == ["branches", "buses"]

    def test_compare_data_engine_specific_keys(self):
        """Test data comparison with engine-specific keys."""
        result1 = SimulationResult(
            job_id="test1",
            status=SimulationStatus.COMPLETED,
            data={"buses": 10, "cloudpss_specific": "value1"},
        )
        result2 = SimulationResult(
            job_id="test2",
            status=SimulationStatus.COMPLETED,
            data={"buses": 10, "pandapower_specific": "value2"},
        )

        comparator = EngineComparator(
            engines=["cloudpss", "pandapower"],
            model_id="test_model",
            analysis_type="power_flow",
        )

        results = {"cloudpss": result1, "pandapower": result2}
        comparison = comparator._compare_data(results)

        assert comparison["common_keys"] == ["buses"]
        assert "cloudpss" in comparison["engine_specific_keys"]
        assert "pandapower" in comparison["engine_specific_keys"]
        assert "cloudpss_specific" in comparison["engine_specific_keys"]["cloudpss"]
        assert "pandapower_specific" in comparison["engine_specific_keys"]["pandapower"]

    @patch("cloudpss_skills_v2.cli.commands.compare_cmd.registry")
    def test_generate_comparison_report(self, mock_registry):
        """Test generating comparison report."""
        mock_adapter_cls = MagicMock()
        mock_adapter = MagicMock()
        mock_result = MagicMock()
        mock_result.status = SimulationStatus.COMPLETED
        mock_result.duration_seconds = 1.5
        mock_result.data = {"buses": 10}
        mock_result.errors = []
        mock_result.warnings = []

        mock_adapter_cls.return_value = mock_adapter
        mock_adapter.load_model.return_value = True
        mock_adapter.run_simulation.return_value = mock_result
        mock_registry.get.return_value = mock_adapter_cls

        comparator = EngineComparator(
            engines=["cloudpss", "pandapower"],
            model_id="test_model",
            analysis_type="power_flow",
        )

        # Manually set results to simulate run
        comparator.results = {
            "cloudpss": mock_result,
            "pandapower": mock_result,
        }

        report = comparator._generate_comparison_report()

        assert report["model_id"] == "test_model"
        assert report["analysis_type"] == "power_flow"
        assert report["engines"] == ["cloudpss", "pandapower"]
        assert report["status_summary"]["total"] == 2
        assert report["status_summary"]["success"] == 2
        assert report["status_summary"]["failed"] == 0


class TestExecuteFunction:
    """Test execute function."""

    def test_execute_single_engine_fails(self):
        """Test execute with single engine fails."""
        args = argparse.Namespace(
            engines="cloudpss",
            model="test_model",
            analysis="power_flow",
            output=None,
        )

        result = execute(args)

        assert result == 1  # Should fail with less than 2 engines

    def test_execute_invalid_analysis_type(self):
        """Test execute with invalid analysis type."""
        args = argparse.Namespace(
            engines="cloudpss,pandapower",
            model="test_model",
            analysis="invalid_type",
            output=None,
        )

        result = execute(args)

        assert result == 1  # Should fail with invalid analysis type

    @patch("cloudpss_skills_v2.cli.commands.compare_cmd.EngineComparator")
    def test_execute_all_success(self, mock_comparator_cls):
        """Test execute when all engines succeed."""
        mock_comparator = MagicMock()
        mock_comparator.run_comparison.return_value = {
            "status_summary": {"total": 2, "success": 2, "failed": 0},
        }
        mock_comparator_cls.return_value = mock_comparator

        args = argparse.Namespace(
            engines="cloudpss,pandapower",
            model="test_model",
            analysis="power_flow",
            output=None,
        )

        result = execute(args)

        assert result == 0  # All succeeded
        mock_comparator_cls.assert_called_once_with(
            ["cloudpss", "pandapower"], "test_model", "power_flow"
        )
        mock_comparator.run_comparison.assert_called_once()

    @patch("cloudpss_skills_v2.cli.commands.compare_cmd.EngineComparator")
    def test_execute_partial_success(self, mock_comparator_cls):
        """Test execute when some engines succeed."""
        mock_comparator = MagicMock()
        mock_comparator.run_comparison.return_value = {
            "status_summary": {"total": 3, "success": 2, "failed": 1},
        }
        mock_comparator_cls.return_value = mock_comparator

        args = argparse.Namespace(
            engines="cloudpss,pandapower,psse",
            model="test_model",
            analysis="power_flow",
            output=None,
        )

        result = execute(args)

        assert result == 1  # Partial success

    @patch("cloudpss_skills_v2.cli.commands.compare_cmd.EngineComparator")
    def test_execute_all_failed(self, mock_comparator_cls):
        """Test execute when all engines fail."""
        mock_comparator = MagicMock()
        mock_comparator.run_comparison.return_value = {
            "status_summary": {"total": 2, "success": 0, "failed": 2},
        }
        mock_comparator_cls.return_value = mock_comparator

        args = argparse.Namespace(
            engines="cloudpss,pandapower",
            model="test_model",
            analysis="power_flow",
            output=None,
        )

        result = execute(args)

        assert result == 2  # All failed

    @patch("cloudpss_skills_v2.cli.commands.compare_cmd.EngineComparator")
    def test_execute_with_output_file(self, mock_comparator_cls):
        """Test execute with output file."""
        mock_comparator = MagicMock()
        mock_comparator.run_comparison.return_value = {
            "status_summary": {"total": 2, "success": 2, "failed": 0},
        }
        mock_comparator_cls.return_value = mock_comparator

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            output_path = f.name

        try:
            args = argparse.Namespace(
                engines="cloudpss,pandapower",
                model="test_model",
                analysis="power_flow",
                output=output_path,
            )

            result = execute(args)

            assert result == 0

            # Verify file was created with JSON content
            with open(output_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                assert data["status_summary"]["success"] == 2
        finally:
            Path(output_path).unlink(missing_ok=True)


class TestAddParser:
    """Test add_parser function."""

    def test_add_parser_creates_subparser(self):
        """Test that add_parser creates compare subparser."""
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()

        add_parser(subparsers)

        # Parse a compare command to verify it works
        args = parser.parse_args(["compare", "--engines", "cloudpss,pandapower",
                                   "--model", "test", "--analysis", "power_flow"])

        assert args.engines == "cloudpss,pandapower"
        assert args.model == "test"
        assert args.analysis == "power_flow"
        assert hasattr(args, "func")
        assert args.func == execute

    def test_add_parser_required_args(self):
        """Test that required arguments are enforced."""
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()

        add_parser(subparsers)

        # Missing --engines should fail
        with pytest.raises(SystemExit):
            parser.parse_args(["compare", "--model", "test", "--analysis", "power_flow"])

        # Missing --model should fail
        with pytest.raises(SystemExit):
            parser.parse_args(["compare", "--engines", "cloudpss", "--analysis", "power_flow"])

        # Missing --analysis should fail
        with pytest.raises(SystemExit):
            parser.parse_args(["compare", "--engines", "cloudpss", "--model", "test"])

    def test_add_parser_analysis_choices(self):
        """Test that analysis type choices are enforced."""
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()

        add_parser(subparsers)

        # Valid analysis types should work
        for analysis_type in ["power_flow", "emt", "short_circuit", "harmonic", "dynamic"]:
            args = parser.parse_args(["compare", "--engines", "cloudpss,pandapower",
                                       "--model", "test", "--analysis", analysis_type])
            assert args.analysis == analysis_type

        # Invalid analysis type should fail
        with pytest.raises(SystemExit):
            parser.parse_args(["compare", "--engines", "cloudpss", "--model", "test",
                               "--analysis", "invalid_type"])


class TestIntegrationStyle:
    """Integration-style tests with mocked dependencies."""

    @patch("cloudpss_skills_v2.cli.commands.compare_cmd.registry")
    def test_full_comparison_workflow(self, mock_registry):
        """Test full comparison workflow with mocked adapters."""
        # Setup mock adapters
        mock_cloudpss_adapter = MagicMock()
        mock_cloudpss_result = MagicMock()
        mock_cloudpss_result.status = SimulationStatus.COMPLETED
        mock_cloudpss_result.duration_seconds = 2.0
        mock_cloudpss_result.data = {
            "buses": 10,
            "branches": 15,
            "losses_mw": 50.5,
        }
        mock_cloudpss_result.errors = []
        mock_cloudpss_result.warnings = []

        mock_pandapower_adapter = MagicMock()
        mock_pandapower_result = MagicMock()
        mock_pandapower_result.status = SimulationStatus.COMPLETED
        mock_pandapower_result.duration_seconds = 1.5
        mock_pandapower_result.data = {
            "buses": 10,
            "branches": 15,
            "losses_mw": 51.2,
        }
        mock_pandapower_result.errors = []
        mock_pandapower_result.warnings = []

        mock_cloudpss_adapter.load_model.return_value = True
        mock_cloudpss_adapter.run_simulation.return_value = mock_cloudpss_result

        mock_pandapower_adapter.load_model.return_value = True
        mock_pandapower_adapter.run_simulation.return_value = mock_pandapower_result

        mock_cloudpss_cls = MagicMock(return_value=mock_cloudpss_adapter)
        mock_pandapower_cls = MagicMock(return_value=mock_pandapower_adapter)

        def mock_get(engine, analysis):
            if engine == "cloudpss":
                return mock_cloudpss_cls
            elif engine == "pandapower":
                return mock_pandapower_cls
            return None

        mock_registry.get = mock_get

        # Run comparison
        comparator = EngineComparator(
            engines=["cloudpss", "pandapower"],
            model_id="IEEE14",
            analysis_type="power_flow",
        )

        report = comparator.run_comparison()

        # Verify results
        assert report["model_id"] == "IEEE14"
        assert report["analysis_type"] == "power_flow"
        assert report["status_summary"]["total"] == 2
        assert report["status_summary"]["success"] == 2
        assert report["status_summary"]["failed"] == 0

        # Verify comparison found the losses difference
        differences = report["comparison"].get("differences", [])
        losses_diff = [d for d in differences if d["key"] == "losses_mw"]
        assert len(losses_diff) == 1
        assert losses_diff[0]["values"]["cloudpss"] == 50.5
        assert losses_diff[0]["values"]["pandapower"] == 51.2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
