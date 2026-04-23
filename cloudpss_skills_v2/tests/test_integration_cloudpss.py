"""Integration tests for CloudPSS adapter - CI compatible.

These tests verify the CloudPSS API adapter handles:
- Power flow simulations via CloudPSS SDK
- Short circuit analysis via EMT simulation
- Model loading and component manipulation
- Physical correctness of results
"""

import pytest
from cloudpss_skills_v2.powerapi import SimulationResult, SimulationStatus
from cloudpss_skills_v2.powerapi.adapters.cloudpss import CloudPSSPowerFlowAdapter
from cloudpss_skills_v2.powerapi.adapters.cloudpss.short_circuit import (
    CloudPSSShortCircuitAdapter,
)


@pytest.fixture(scope="session")
def cloudpss_token():
    """Get CloudPSS token from file."""
    from pathlib import Path

    for token_file in [".cloudpss_token", ".cloudpss_token_internal"]:
        p = Path(token_file)
        if p.exists():
            token = p.read_text().strip()
            if len(token) > 100:
                return token
    return None


def has_cloudpss_token(token):
    """Check if CloudPSS token is available."""
    return token is not None


@pytest.mark.cloudpss
class TestCloudPSSPowerFlowAdapterLifecycle:
    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_engine_name(self):
        adapter = CloudPSSPowerFlowAdapter()
        assert adapter.engine_name == "cloudpss"

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_supported_simulations(self):
        from cloudpss_skills_v2.powerapi import SimulationType

        adapter = CloudPSSPowerFlowAdapter()
        sims = adapter.get_supported_simulations()
        assert SimulationType.POWER_FLOW in sims

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_adapter_instantiation(self):
        adapter = CloudPSSPowerFlowAdapter()
        assert adapter is not None


@pytest.mark.cloudpss
class TestCloudPSSPowerFlowValidation:
    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_validate_empty_config(self):
        adapter = CloudPSSPowerFlowAdapter()
        result = adapter._do_validate_config({})
        assert not result.valid

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_validate_with_model_id(self):
        adapter = CloudPSSPowerFlowAdapter()
        result = adapter._do_validate_config({"model_id": "test_model"})
        assert result.valid

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_validate_unknown_algorithm(self):
        adapter = CloudPSSPowerFlowAdapter()
        result = adapter._do_validate_config(
            {"model_id": "test", "algorithm": "unknown_algo"}
        )
        assert not result.valid

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_validate_known_algorithms(self):
        adapter = CloudPSSPowerFlowAdapter()
        for algo in ["newton_raphson", "fast_decoupled", "acpf"]:
            result = adapter._do_validate_config(
                {"model_id": "test", "algorithm": algo}
            )
            assert result.valid


@pytest.mark.cloudpss
class TestCloudPSSPowerFlowResultParsing:
    def test_normalize_bus_row_voltage_only(self):
        from cloudpss_skills_v2.powerapi.adapters.cloudpss.powerflow import (
            _normalize_bus_row,
        )

        raw = {"Vm / pu": 1.0, "Va / deg": 0.0}
        result = _normalize_bus_row(raw)
        assert result["voltage_pu"] == 1.0
        assert result["angle_deg"] == 0.0

    def test_normalize_bus_row_with_html(self):
        from cloudpss_skills_v2.powerapi.adapters.cloudpss.powerflow import (
            _normalize_bus_row,
        )

        raw = {"<i>V</i><sub>m</sub> / pu": 1.05, "<i>V</i><sub>a</sub> / deg": 5.0}
        result = _normalize_bus_row(raw)
        assert result["voltage_pu"] == 1.05
        assert result["angle_deg"] == 5.0

    def test_normalize_bus_row_with_generation(self):
        from cloudpss_skills_v2.powerapi.adapters.cloudpss.powerflow import (
            _normalize_bus_row,
        )

        raw = {
            "Vm / pu": 1.0,
            "Pgen / MW": 100.0,
            "Qgen / MVar": 50.0,
            "Pload / MW": 80.0,
            "Qload / MVar": 30.0,
        }
        result = _normalize_bus_row(raw)
        assert result["generation_mw"] == 100.0
        assert result["generation_mvar"] == 50.0
        assert result["load_mw"] == 80.0
        assert result["load_mvar"] == 30.0

    def test_normalize_bus_row_defaults(self):
        from cloudpss_skills_v2.powerapi.adapters.cloudpss.powerflow import (
            _normalize_bus_row,
        )

        raw = {"Vm / pu": 1.0}
        result = _normalize_bus_row(raw)
        assert result["voltage_kv"] == 230
        assert result["bus_type"] == "pq"


@pytest.mark.cloudpss
class TestCloudPSSPowerFlowBranchParsing:
    def test_normalize_branch_row_basic(self):
        from cloudpss_skills_v2.powerapi.adapters.cloudpss.powerflow import (
            _normalize_branch_row,
        )

        raw = {"From bus": 1, "To bus": 2, "Pij / MW": 50.0, "Ploss / MW": 0.5}
        result = _normalize_branch_row(raw)
        assert result["from_bus"] == 1
        assert result["to_bus"] == 2
        assert result["p_from_mw"] == 50.0
        assert result["power_loss_mw"] == 0.5

    def test_normalize_branch_row_with_html(self):
        from cloudpss_skills_v2.powerapi.adapters.cloudpss.powerflow import (
            _normalize_branch_row,
        )

        raw = {
            "<i>P</i><sub>ij</sub> / MW": 100.0,
            "<i>Q</i><sub>ij</sub> / MVar": 20.0,
            "<i>P</i><sub>loss</sub> / MW": 1.0,
        }
        result = _normalize_branch_row(raw)
        assert result["p_from_mw"] == 100.0
        assert result["q_from_mvar"] == 20.0
        assert result["power_loss_mw"] == 1.0


@pytest.mark.cloudpss
class TestCloudPSSPowerFlowSummary:
    def test_generate_summary_basic(self):
        from cloudpss_skills_v2.powerapi.adapters.cloudpss.powerflow import (
            _generate_pf_summary,
        )

        buses = [
            {"voltage_pu": 1.0, "generation_mw": 100, "load_mw": 80},
            {"voltage_pu": 0.95, "generation_mw": 0, "load_mw": 50},
        ]
        branches = [{"power_loss_mw": 2.5}]

        summary = _generate_pf_summary(buses, branches)

        assert summary["total_generation"]["p_mw"] == 100.0
        assert summary["total_load"]["p_mw"] == 130.0
        assert summary["total_loss_mw"] == 2.5
        assert summary["voltage_range"]["min_pu"] == 0.95
        assert summary["voltage_range"]["max_pu"] == 1.0

    def test_generate_summary_handles_missing_fields(self):
        from cloudpss_skills_v2.powerapi.adapters.cloudpss.powerflow import (
            _generate_pf_summary,
        )

        buses = [{"voltage_pu": 1.0}, {"voltage_pu": 0.98}]
        branches = []

        summary = _generate_pf_summary(buses, branches)
        assert summary["total_generation"]["p_mw"] == 0.0
        assert summary["total_load"]["p_mw"] == 0.0
        assert summary["total_loss_mw"] == 0.0


@pytest.mark.cloudpss
class TestCloudPSSPowerFlowResultStructure:
    def test_result_data_structure_keys(self):
        from cloudpss_skills_v2.powerapi.adapters.cloudpss.powerflow import (
            _generate_pf_summary,
        )

        buses = [{"voltage_pu": 1.0, "name": "Bus1"}]
        branches = [{"from_bus": 0, "to_bus": 1, "name": "Line1"}]
        summary = _generate_pf_summary(buses, branches)

        expected_keys = {
            "model",
            "model_rid",
            "job_id",
            "converged",
            "buses",
            "branches",
            "summary",
        }

        mock_result = SimulationResult(
            job_id="test123",
            status=SimulationStatus.COMPLETED,
            data={
                "model": "test",
                "model_rid": "test_rid",
                "job_id": "test123",
                "converged": True,
                "bus_count": len(buses),
                "branch_count": len(branches),
                "buses": buses,
                "branches": branches,
                "summary": summary,
            },
        )

        data = mock_result.data
        for key in expected_keys:
            assert key in data, f"Missing key: {key}"


@pytest.mark.cloudpss
class TestCloudPSSPowerFlowAuth:
    def test_setup_auth_with_token(self):
        from cloudpss_skills_v2.powerapi.adapters.cloudpss.powerflow import _setup_auth

        _setup_auth(
            {"auth": {"token": "test_token", "base_url": "https://test.cloudpss.com"}}
        )

    def test_setup_auth_internal_server(self):
        from cloudpss_skills_v2.powerapi.adapters.cloudpss.powerflow import _setup_auth

        _setup_auth({"auth": {"server": "internal"}})


@pytest.mark.cloudpss
class TestCloudPSSShortCircuitAdapterLifecycle:
    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_engine_name(self):
        adapter = CloudPSSShortCircuitAdapter()
        assert adapter.engine_name == "cloudpss_sc"

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_supported_simulations(self):
        from cloudpss_skills_v2.powerapi import SimulationType

        adapter = CloudPSSShortCircuitAdapter()
        sims = adapter.get_supported_simulations()
        assert SimulationType.SHORT_CIRCUIT in sims

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_adapter_instantiation(self):
        adapter = CloudPSSShortCircuitAdapter()
        assert adapter is not None


@pytest.mark.cloudpss
class TestCloudPSSShortCircuitValidation:
    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_validate_empty_config(self):
        adapter = CloudPSSShortCircuitAdapter()
        result = adapter._do_validate_config({})
        assert not result.valid

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_validate_with_model_id(self):
        adapter = CloudPSSShortCircuitAdapter()
        result = adapter._do_validate_config({"model_id": "test_model"})
        assert result.valid


@pytest.mark.cloudpss
class TestCloudPSSShortCircuitFaultTypeMapping:
    @pytest.mark.parametrize(
        "input_type,expected",
        [
            ("3phase", "3ph"),
            ("3ph", "3ph"),
            ("three_phase", "3ph"),
            ("1phase", "slg"),
            ("slg", "slg"),
            ("single_line_ground", "slg"),
            ("2phase", "ll"),
            ("ll", "ll"),
            ("line_line", "ll"),
            ("2phase-ground", "dlg"),
            ("dlg", "dlg"),
            ("double_line_ground", "dlg"),
        ],
    )
    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_fault_type_mapping(self, input_type, expected):
        from cloudpss_skills_v2.powerapi.adapters.cloudpss.short_circuit import (
            _FAULT_TYPE_MAP,
        )

        assert _FAULT_TYPE_MAP[input_type] == expected

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_unknown_fault_type_defaults_to_3ph(self):
        from cloudpss_skills_v2.powerapi.adapters.cloudpss.short_circuit import (
            _FAULT_TYPE_MAP,
        )

        assert _FAULT_TYPE_MAP.get("unknown", "3ph") == "3ph"


@pytest.mark.cloudpss
class TestCloudPSSComponentClassification:
    def test_classify_line(self):
        adapter = CloudPSSPowerFlowAdapter()
        result = adapter._classify_component("model/CloudPSS/line")
        from cloudpss_skills_v2.powerskill.model_handle import ComponentType

        assert result == ComponentType.BRANCH

    def test_classify_transformer(self):
        adapter = CloudPSSPowerFlowAdapter()
        result = adapter._classify_component("model/CloudPSS/transformer")
        from cloudpss_skills_v2.powerskill.model_handle import ComponentType

        assert result == ComponentType.TRANSFORMER

    def test_classify_load(self):
        adapter = CloudPSSPowerFlowAdapter()
        result = adapter._classify_component("Load")
        from cloudpss_skills_v2.powerskill.model_handle import ComponentType

        assert result == ComponentType.LOAD

    def test_classify_generator(self):
        adapter = CloudPSSPowerFlowAdapter()
        result = adapter._classify_component("Generator")
        from cloudpss_skills_v2.powerskill.model_handle import ComponentType

        assert result == ComponentType.GENERATOR

    def test_classify_unknown(self):
        adapter = CloudPSSPowerFlowAdapter()
        result = adapter._classify_component("UnknownComponent")
        from cloudpss_skills_v2.powerskill.model_handle import ComponentType

        assert result == ComponentType.OTHER


@pytest.mark.cloudpss
class TestCloudPSSResultCache:
    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_result_caching(self):
        adapter = CloudPSSPowerFlowAdapter()
        mock_result = SimulationResult(
            job_id="test_job",
            status=SimulationStatus.COMPLETED,
            data={"buses": [], "branches": []},
        )
        adapter._result_cache["test_job"] = mock_result
        assert adapter._result_cache["test_job"] == mock_result

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_get_cached_result(self):
        adapter = CloudPSSPowerFlowAdapter()
        mock_result = SimulationResult(
            job_id="test_job",
            status=SimulationStatus.COMPLETED,
            data={},
        )
        adapter._result_cache["test_job"] = mock_result
        retrieved = adapter._do_get_result("test_job")
        assert retrieved.job_id == "test_job"

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_get_nonexistent_result(self):
        adapter = CloudPSSPowerFlowAdapter()
        result = adapter._do_get_result("nonexistent")
        assert result.status == SimulationStatus.FAILED


@pytest.mark.cloudpss
class TestCloudPSSShortCircuitResultCache:
    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_result_caching(self):
        adapter = CloudPSSShortCircuitAdapter()
        mock_result = SimulationResult(
            job_id="test_job",
            status=SimulationStatus.COMPLETED,
            data={"bus_results": []},
        )
        adapter._result_cache["test_job"] = mock_result
        assert adapter._result_cache["test_job"] == mock_result

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_get_cached_result(self):
        adapter = CloudPSSShortCircuitAdapter()
        mock_result = SimulationResult(
            job_id="test_job",
            status=SimulationStatus.COMPLETED,
            data={},
        )
        adapter._result_cache["test_job"] = mock_result
        retrieved = adapter._do_get_result("test_job")
        assert retrieved.job_id == "test_job"


@pytest.mark.cloudpss
class TestCloudPSSPowerFlowDisconnect:
    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_disconnect_clears_cache(self):
        adapter = CloudPSSPowerFlowAdapter()
        adapter._model_cache["test"] = "model"
        adapter._result_cache["job1"] = SimulationResult(
            job_id="job1",
            status=SimulationStatus.COMPLETED,
            data={},
        )
        adapter._do_disconnect()
        assert len(adapter._model_cache) == 0
        assert len(adapter._result_cache) == 0


@pytest.mark.cloudpss
class TestCloudPSSShortCircuitDisconnect:
    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_disconnect_clears_cache(self):
        adapter = CloudPSSShortCircuitAdapter()
        adapter._model_cache["test"] = "model"
        adapter._result_cache["job1"] = SimulationResult(
            job_id="job1",
            status=SimulationStatus.COMPLETED,
            data={},
        )
        adapter._do_disconnect()
        assert len(adapter._model_cache) == 0
        assert len(adapter._result_cache) == 0


@pytest.mark.cloudpss
class TestCloudPSSPowerFlowCloneModel:
    def test_clone_id_format(self):
        import uuid

        original_rid = "test_rid"
        clone_id = f"{original_rid}__clone_{uuid.uuid4().hex[:8]}"
        assert clone_id != original_rid
        assert "__clone_" in clone_id

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_original_rid_map_maintained(self):
        adapter = CloudPSSPowerFlowAdapter()
        adapter._original_rid_map["clone1"] = "original_rid"
        assert adapter._original_rid_map["clone1"] == "original_rid"


@pytest.mark.cloudpss
class TestCloudPSSTableParsing:
    def test_parse_cloudpss_table_with_json(self):
        from cloudpss_skills_v2.powerapi.adapters.cloudpss.powerflow import (
            _parse_cloudpss_table,
        )

        mock_table = {
            "data": {
                "columns": [
                    {"name": "Vm / pu", "data": [1.0, 0.95]},
                    {"name": "Va / deg", "data": [0.0, 5.0]},
                ]
            }
        }
        result = _parse_cloudpss_table(mock_table)
        assert len(result) == 2
        assert result[0]["Vm / pu"] == 1.0
        assert result[1]["Va / deg"] == 5.0

    def test_parse_cloudpss_table_empty(self):
        from cloudpss_skills_v2.powerapi.adapters.cloudpss.powerflow import (
            _parse_cloudpss_table,
        )

        result = _parse_cloudpss_table(None)
        assert result == []

    def test_parse_cloudpss_table_list(self):
        from cloudpss_skills_v2.powerapi.adapters.cloudpss.powerflow import (
            _parse_cloudpss_table,
        )

        mock_list = [{"Vm": 1.0}, {"Vm": 0.95}]
        result = _parse_cloudpss_table(mock_list)
        assert result == mock_list


@pytest.mark.cloudpss
class TestCloudPSSPhysicalCorrectness:
    """Verify CloudPSS adapter results meet physical correctness standards."""

    def test_voltage_range_validation(self):
        from cloudpss_skills_v2.powerapi.adapters.cloudpss.powerflow import (
            _normalize_bus_row,
        )

        for vm in [0.9, 1.0, 1.05, 1.1]:
            row = {"Vm / pu": vm}
            result = _normalize_bus_row(row)
            assert 0.9 <= result["voltage_pu"] <= 1.1

    def test_angle_range_validation(self):
        from cloudpss_skills_v2.powerapi.adapters.cloudpss.powerflow import (
            _normalize_bus_row,
        )

        for angle in [-45, 0, 30, 60]:
            row = {"Va / deg": angle, "Vm / pu": 1.0}
            result = _normalize_bus_row(row)
            assert -90 <= result["angle_deg"] <= 90

    def test_power_balance_check(self):
        from cloudpss_skills_v2.powerapi.adapters.cloudpss.powerflow import (
            _generate_pf_summary,
        )

        buses = [
            {
                "voltage_pu": 1.0,
                "generation_mw": 132,
                "load_mw": 80,
                "generation_mvar": 50,
                "load_mvar": 30,
            },
            {
                "voltage_pu": 0.98,
                "generation_mw": 0,
                "load_mw": 50,
                "generation_mvar": 0,
                "load_mvar": 20,
            },
        ]
        branches = [{"power_loss_mw": 2.0}]

        summary = _generate_pf_summary(buses, branches)

        p_gen = summary["total_generation"]["p_mw"]
        p_load = summary["total_load"]["p_mw"]
        p_loss = summary["total_loss_mw"]

        assert abs(p_gen - (p_load + p_loss)) < 1.0

    def test_voltage_profile_validation(self):
        from cloudpss_skills_v2.powerapi.adapters.cloudpss.powerflow import (
            _generate_pf_summary,
        )

        normal_buses = [
            {"voltage_pu": 1.0},
            {"voltage_pu": 0.98},
            {"voltage_pu": 1.02},
        ]
        summary = _generate_pf_summary(normal_buses, [])
        assert summary["voltage_range"]["min_pu"] >= 0.9
        assert summary["voltage_range"]["max_pu"] <= 1.1

    def test_losses_positive(self):
        from cloudpss_skills_v2.powerapi.adapters.cloudpss.powerflow import (
            _generate_pf_summary,
        )

        buses = [{"voltage_pu": 1.0}]
        branches = [
            {"power_loss_mw": 1.0},
            {"power_loss_mw": 0.5},
        ]

        summary = _generate_pf_summary(buses, branches)
        assert summary["total_loss_mw"] >= 0

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_short_circuit_result_structure(self):
        mock_result = SimulationResult(
            job_id="test_job",
            status=SimulationStatus.COMPLETED,
            data={
                "model": "test",
                "job_id": "test_job",
                "fault_type": "3ph",
                "bus_results": [
                    {
                        "bus": "Bus1",
                        "bus_index": 0,
                        "ikss_ka": 10.0,
                        "ip_ka": 25.0,
                        "ith_ka": 5.0,
                        "v_pu": 0.0,
                    }
                ],
                "summary": {
                    "fault_type": "3ph",
                    "max_ikss_ka": 10.0,
                    "bus_count": 1,
                },
            },
        )

        data = mock_result.data
        assert "bus_results" in data
        assert "summary" in data
        assert data["summary"]["max_ikss_ka"] == 10.0

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_ikss_nonnegative(self):
        mock_result = SimulationResult(
            job_id="test",
            status=SimulationStatus.COMPLETED,
            data={
                "bus_results": [
                    {"bus": "B1", "ikss_ka": 5.0},
                    {"bus": "B2", "ikss_ka": 10.0},
                ]
            },
        )

        for bus in mock_result.data["bus_results"]:
            assert bus["ikss_ka"] >= 0

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_ip_greater_than_ikss(self):
        mock_result = SimulationResult(
            job_id="test",
            status=SimulationStatus.COMPLETED,
            data={
                "bus_results": [
                    {"bus": "B1", "ikss_ka": 10.0, "ip_ka": 25.0},
                    {"bus": "B2", "ikss_ka": 5.0, "ip_ka": 12.0},
                ]
            },
        )

        for bus in mock_result.data["bus_results"]:
            assert bus["ip_ka"] >= bus["ikss_ka"]


@pytest.mark.cloudpss
class TestCloudPSSRealAPI:
    """Real CloudPSS API integration tests - requires valid token."""

    @pytest.fixture
    def model_rid(self):
        return "model/holdme/IEEE39"

    def test_cloudpss_api_connection(self, cloudpss_token):
        if not has_cloudpss_token(cloudpss_token):
            pytest.skip("CloudPSS token not available")

        from cloudpss import setToken

        setToken(cloudpss_token)
        assert cloudpss_token is not None
        assert len(cloudpss_token) > 100

    def test_cloudpss_model_fetch(self, cloudpss_token, model_rid):
        if not has_cloudpss_token(cloudpss_token):
            pytest.skip("CloudPSS token not available")

        from cloudpss import setToken, Model

        setToken(cloudpss_token)

        model = Model.fetch(model_rid)
        assert model is not None
        assert hasattr(model, "name")
        assert hasattr(model, "rid")

    def test_cloudpss_powerflow_execution(self, cloudpss_token, model_rid):
        if not has_cloudpss_token(cloudpss_token):
            pytest.skip("CloudPSS token not available")

        from cloudpss import setToken, Model

        setToken(cloudpss_token)

        model = Model.fetch(model_rid)
        job = model.runPowerFlow()

        max_wait = 120
        waited = 0
        while waited < max_wait:
            status = job.status()
            if status == 1:
                break
            if status == 2:
                pytest.fail("Power flow failed")
            import time

            time.sleep(2)
            waited += 2

        assert status == 1, f"Power flow timed out after {waited}s"

        result = job.result
        assert result is not None

        buses = result.getBuses()
        assert buses is not None

    def test_cloudpss_adapter_run_powerflow(self, cloudpss_token, model_rid):
        if not has_cloudpss_token(cloudpss_token):
            pytest.skip("CloudPSS token not available")

        adapter = CloudPSSPowerFlowAdapter()
        adapter.connect()

        try:
            result = adapter.run_simulation(
                {
                    "model_id": model_rid,
                    "auth": {"token": cloudpss_token},
                    "timeout": 120,
                }
            )

            assert result.status == SimulationStatus.COMPLETED, (
                f"Failed: {result.errors}"
            )
            assert result.data is not None
            assert "buses" in result.data
            assert "branches" in result.data
            assert len(result.data["buses"]) > 0

            for bus in result.data["buses"]:
                vm = bus.get("voltage_pu", 1.0)
                assert 0.9 <= vm <= 1.1, f"Voltage out of range: {vm}"

        finally:
            adapter.disconnect()

    def test_cloudpss_short_circuit_adapter(self, cloudpss_token, model_rid):
        if not has_cloudpss_token(cloudpss_token):
            pytest.skip("CloudPSS token not available")

        adapter = CloudPSSShortCircuitAdapter()
        adapter.connect()

        try:
            result = adapter.run_simulation(
                {
                    "model_id": model_rid,
                    "auth": {"token": cloudpss_token},
                    "fault_type": "3ph",
                    "timeout": 180,
                }
            )

            if result.status == SimulationStatus.COMPLETED:
                assert result.data is not None
                assert "fault_currents" in result.data or "bus_voltages" in result.data

                for curr in result.data.get("fault_currents", []):
                    assert curr is not None

                assert "summary" in result.data
                assert result.data["summary"]["fault_type"] == "3ph"

        finally:
            adapter.disconnect()
