"""Tests for CloudPSS PowerFlow adapter - table parsing, normalization, and adapter logic."""

import pytest
from unittest.mock import MagicMock, patch

from cloudpss_skills_v2.powerapi import EngineConfig, SimulationResult, SimulationStatus
from cloudpss_skills_v2.powerapi.adapters.cloudpss.powerflow import (
    CloudPSSPowerFlowAdapter,
    _strip_html,
    _normalize_bus_row,
    _normalize_branch_row,
    _parse_cloudpss_table,
    _generate_pf_summary,
    _as_float,
)


class TestStripHtml:
    def test_simple(self):
        assert _strip_html("<i>V</i><sub>m</sub> / pu") == "Vm / pu"

    def test_no_html(self):
        assert _strip_html("Bus") == "Bus"

    def test_nested_tags(self):
        assert _strip_html("<b>Bold</b> text") == "Bold text"

    def test_empty_string(self):
        assert _strip_html("") == ""


class TestAsFloat:
    def test_numeric(self):
        assert _as_float(3.14) == 3.14

    def test_string(self):
        assert _as_float("2.5") == 2.5

    def test_none(self):
        assert _as_float(None) == 0.0

    def test_empty_string(self):
        assert _as_float("") == 0.0

    def test_custom_default(self):
        assert _as_float(None, 1.0) == 1.0

    def test_invalid_string(self):
        assert _as_float("abc") == 0.0


class TestNormalizeBusRow:
    def test_maps_html_keys(self):
        raw = {
            "Bus": "B1",
            "<i>V</i><sub>m</sub> / pu": 1.02,
            "<i>P</i><sub>g</sub> / MW": 100.0,
            "<i>Q</i><sub>g</sub> / MVar": 20.0,
        }
        result = _normalize_bus_row(raw)
        assert result["name"] == "B1"
        assert result["voltage_pu"] == 1.02
        assert result["generation_mw"] == 100.0
        assert result["generation_mvar"] == 20.0

    def test_adds_defaults(self):
        raw = {"Bus": "B2"}
        result = _normalize_bus_row(raw)
        assert result["voltage_kv"] == 230
        assert result["bus_type"] == "pq"

    def test_preserves_unknown_keys(self):
        raw = {"Bus": "B3", "custom_field": "value"}
        result = _normalize_bus_row(raw)
        assert result["custom_field"] == "value"


class TestNormalizeBranchRow:
    def test_maps_keys(self):
        raw = {
            "Branch": "L1",
            "From bus": "B1",
            "To bus": "B2",
            "Ploss / MW": 0.5,
        }
        result = _normalize_branch_row(raw)
        assert result["name"] == "L1"
        assert result["from_bus"] == "B1"
        assert result["to_bus"] == "B2"
        assert result["power_loss_mw"] == 0.5


class TestParseCloudpssTable:
    def test_none_returns_empty(self):
        assert _parse_cloudpss_table(None) == []

    def test_columnar_format(self):
        table = {
            "data": {
                "columns": [
                    {"name": "Bus", "data": ["B1", "B2"]},
                    {"name": "Vm / pu", "data": [1.02, 0.98]},
                ]
            }
        }
        rows = _parse_cloudpss_table(table)
        assert len(rows) == 2
        assert rows[0]["Bus"] == "B1"
        assert rows[0]["Vm / pu"] == 1.02

    def test_list_format(self):
        table = [{"name": "B1", "Vm": 1.02}]
        rows = _parse_cloudpss_table(table)
        assert len(rows) == 1
        assert rows[0]["name"] == "B1"


class TestGeneratePfSummary:
    def test_basic_summary(self):
        buses = [
            {
                "generation_mw": 100.0,
                "generation_mvar": 20.0,
                "load_mw": 98.0,
                "load_mvar": 19.0,
                "voltage_pu": 1.02,
            },
            {
                "generation_mw": 50.0,
                "generation_mvar": 10.0,
                "load_mw": 48.0,
                "load_mvar": 9.0,
                "voltage_pu": 0.95,
            },
        ]
        branches = [{"power_loss_mw": 2.0}, {"power_loss_mw": 1.5}]
        summary = _generate_pf_summary(buses, branches)
        assert summary["total_generation"]["p_mw"] == 150.0
        assert summary["total_load"]["p_mw"] == 146.0
        assert summary["total_loss_mw"] == 3.5
        assert summary["voltage_range"]["min_pu"] == 0.95
        assert summary["voltage_range"]["max_pu"] == 1.02


class TestCloudPSSPowerFlowAdapter:
    def test_engine_name(self):
        adapter = CloudPSSPowerFlowAdapter()
        assert adapter.engine_name == "cloudpss"

    def test_supported_simulations(self):
        adapter = CloudPSSPowerFlowAdapter()
        from cloudpss_skills_v2.powerapi import SimulationType

        assert SimulationType.POWER_FLOW in adapter.get_supported_simulations()

    def test_validate_config_missing_model(self):
        adapter = CloudPSSPowerFlowAdapter()
        result = adapter._do_validate_config({})
        assert not result.valid

    def test_validate_config_with_model(self):
        adapter = CloudPSSPowerFlowAdapter()
        result = adapter._do_validate_config({"model_id": "test"})
        assert result.valid

    def test_validate_config_bad_algorithm(self):
        adapter = CloudPSSPowerFlowAdapter()
        result = adapter._do_validate_config(
            {"model_id": "test", "algorithm": "invalid"}
        )
        assert not result.valid

    def test_run_no_model_id(self):
        adapter = CloudPSSPowerFlowAdapter()
        adapter._connected = True
        result = adapter._do_run_simulation({})
        assert result.status == SimulationStatus.FAILED

    def test_get_result_not_cached(self):
        adapter = CloudPSSPowerFlowAdapter()
        result = adapter._do_get_result("nonexistent-job")
        assert result.status == SimulationStatus.FAILED

    def test_enriches_rows_from_cloudpss_model_components(self):
        class FakeComponent:
            def __init__(self, definition, args, pins=None):
                self.definition = definition
                self.args = args
                self.pins = pins or {}

        class FakeModel:
            def getAllComponents(self):
                return {
                    "bus_a": FakeComponent(
                        "model/CloudPSS/_newBus_3p",
                        {"VBase": "500", "Freq": "60"},
                        {"0": "node-a"},
                    ),
                    "branch_1": FakeComponent(
                        "model/CloudPSS/TransmissionLine",
                        {
                            "R1pu": {"source": "0.0012"},
                            "X1pu": {"source": "0.0123"},
                            "B1pu": {"source": "0.0456"},
                            "Sbase": {"source": "100"},
                            "Vbase": {"source": "500"},
                            "Name": "line-a-b",
                        },
                    ),
                    "xf_1": FakeComponent(
                        "model/CloudPSS/_newTransformer_3p2w",
                        {
                            "Rl": {"source": "0.002"},
                            "Xl": {"source": "0.08"},
                            "Tmva": {"source": "200"},
                            "InitTap": {"source": "1.02"},
                        },
                    ),
                }

        adapter = CloudPSSPowerFlowAdapter()
        bus_rows = [{"name": "bus_a", "Node": "node-a", "voltage_kv": 230}]
        branch_rows = [
            {"name": "branch_1", "branch_type": "line"},
            {"name": "xf_1", "branch_type": "line"},
        ]

        inventory = adapter._enrich_rows_from_model_components(
            FakeModel(),
            bus_rows,
            branch_rows,
        )

        assert bus_rows[0]["voltage_kv"] == 500.0
        assert branch_rows[0]["r_pu"] == 0.0012
        assert branch_rows[0]["x_pu"] == 0.0123
        assert branch_rows[0]["b_pu"] == 0.0456
        assert branch_rows[0]["parameter_source"] == "cloudpss_model_component"
        assert branch_rows[1]["branch_type"] == "transformer"
        assert branch_rows[1]["x_pu"] == 0.08
        assert branch_rows[1]["rate_a_mva"] == 200.0
        assert branch_rows[1]["tap_ratio"] == 1.02
        assert inventory is not None
        diagnostics = inventory.diagnostics()
        assert diagnostics["status"] == "pass"
        assert diagnostics["component_type_counts"]["bus"] == 1
        assert diagnostics["parameter_coverage"]["transformer_with_x_count"] == 1

    def test_unified_conversion_uses_enriched_branch_type(self):
        adapter = CloudPSSPowerFlowAdapter()
        model = adapter._to_unified_model(
            [
                {"name": "B1", "voltage_pu": 1.0, "angle_deg": 0.0, "voltage_kv": 500.0},
                {"name": "B2", "voltage_pu": 0.99, "angle_deg": -1.0, "voltage_kv": 20.0},
            ],
            [
                {
                    "name": "xf",
                    "from_bus": "B1",
                    "to_bus": "B2",
                    "branch_type": "transformer",
                    "r_pu": 0.002,
                    "x_pu": 0.08,
                    "rate_a_mva": 200.0,
                    "tap_ratio": 1.02,
                }
            ],
        )

        assert model.branches[0].branch_type == "TRANSFORMER"
        assert model.branches[0].x_pu == 0.08
        assert model.branches[0].rate_a_mva == 200.0
        assert model.branches[0].tap_ratio == 1.02
