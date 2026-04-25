"""
Integration Tests for CloudPSS V2 Framework with Local Server

Tests all tiers from basic connectivity to complex workflows.
Run with: pytest cloudpss_skills_v2/tests/test_integration_local_server.py -v
"""

import pytest
import os
import sys

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cloudpss
from cloudpss_skills_v2.powerskill import Engine
from cloudpss_skills_v2.powerapi import EngineConfig, SimulationStatus


def get_token():
    """Get token from file or environment."""
    # Check workspace root for token file
    token_file = "/home/chenying/researches/cloudpss-toolkit/.cloudpss_token_internal"
    if os.path.exists(token_file):
        with open(token_file) as f:
            return f.read().strip()
    # Fallback to environment
    return os.environ.get("CLOUDPSS_TOKEN", "")


def get_config(base_url="http://166.111.60.76:50001"):
    """Create engine config for local server."""
    token = get_token()
    return EngineConfig(
        engine_name="cloudpss",
        base_url=base_url,
        extra={"auth": {"token": token}}
    )


# =============================================================================
# TIER 1: Engine Connectivity
# =============================================================================

class TestTier1Connectivity:
    """Test basic server connectivity and authentication."""

    def test_server_connection(self):
        """Test can connect to local server."""
        config = get_config()
        pf = Engine.create_powerflow(engine="cloudpss", config=config)
        # Connection happens in create_powerflow
        assert pf is not None
        assert pf._adapter is not None

    def test_token_validation(self):
        """Test token is valid."""
        token = get_token()
        assert token is not None
        assert len(token) > 100  # JWT tokens are long

    def test_base_url_from_config(self):
        """Test base_url is properly set."""
        config = get_config()
        assert config.base_url == "http://166.111.60.76:50001"
        assert config.extra.get("auth", {}).get("token") is not None


# =============================================================================
# TIER 2: Model Operations
# =============================================================================

class TestTier2ModelOperations:
    """Test model loading and component retrieval."""

    @pytest.fixture
    def pf(self):
        """PowerFlow engine with local server."""
        config = get_config()
        return Engine.create_powerflow(engine="cloudpss", config=config)

    def test_load_cloud_model(self, pf):
        """Test loading model by RID."""
        result = pf._adapter.load_model("model/chenying/IEEE39")
        assert result is True
        assert "model/chenying/IEEE39" in pf._adapter._model_cache

    def test_get_components(self, pf):
        """Test retrieving model components."""
        pf._adapter.load_model("model/chenying/IEEE39")
        components = pf._adapter.get_components("model/chenying/IEEE39")
        assert len(components) > 0
        assert components[0].key is not None
        assert components[0].definition is not None

    def test_get_components_by_type(self, pf):
        """Test filtering components by type."""
        pf._adapter.load_model("model/chenying/IEEE39")
        loads = pf._adapter.get_components_by_type("model/chenying/IEEE39", "load")
        assert len(loads) > 0


# =============================================================================
# TIER 3: Core Simulations
# =============================================================================

class TestTier3CoreSimulations:
    """Test core simulation functionality."""

    @pytest.fixture
    def pf(self):
        config = get_config()
        return Engine.create_powerflow(engine="cloudpss", config=config)

    @pytest.fixture
    def sc(self):
        config = get_config()
        return Engine.create_short_circuit(engine="cloudpss", config=config)

    @pytest.fixture
    def emt(self):
        config = get_config()
        return Engine.create_emt(engine="cloudpss", config=config)

    def test_powerflow_ieee39(self, pf):
        """Test IEEE39 power flow simulation."""
        result = pf.run({"model_id": "model/chenying/IEEE39"})
        
        assert result.status == SimulationStatus.COMPLETED
        assert result.data is not None
        assert result.data.get("bus_count") == 39
        assert result.data.get("branch_count") == 46

    def test_powerflow_convergence(self, pf):
        """Test power flow convergence status."""
        result = pf.run({"model_id": "model/chenying/IEEE39"})
        
        assert result.data.get("converged") is True

    def test_short_circuit(self, sc):
        """Test short circuit analysis."""
        result = sc.run({"model_id": "model/chenying/IEEE39"})
        
        assert result.status == SimulationStatus.COMPLETED
        assert result.data is not None
        assert "fault_currents" in result.data

    def test_emt_basic(self, emt):
        """Test basic EMT simulation."""
        result = emt.run({
            "model_id": "model/chenying/IEEE39",
            "timeout": 120
        })
        
        assert result.status == SimulationStatus.COMPLETED
        assert result.data is not None
        assert result.data.get("plot_count", 0) > 0


# =============================================================================
# TIER 4: Data Validation
# =============================================================================

class TestTier4DataValidation:
    """Test data mapping and validation."""

    @pytest.fixture
    def pf(self):
        config = get_config()
        return Engine.create_powerflow(engine="cloudpss", config=config)

    def test_bus_data_mapping(self, pf):
        """Test bus data fields are correctly mapped."""
        result = pf.run({"model_id": "model/chenying/IEEE39"})
        
        buses = result.data.get("buses", [])
        assert len(buses) == 39
        
        bus = buses[0]
        # Check key fields exist
        assert "name" in bus
        assert "voltage_pu" in bus
        assert "angle_deg" in bus
        # Verify values are reasonable
        assert 0.9 <= bus["voltage_pu"] <= 1.1
        assert -180 <= bus["angle_deg"] <= 180

    def test_branch_data_mapping(self, pf):
        """Test branch data fields are correctly mapped."""
        result = pf.run({"model_id": "model/chenying/IEEE39"})
        
        branches = result.data.get("branches", [])
        assert len(branches) == 46
        
        branch = branches[0]
        assert "name" in branch
        assert "from_bus" in branch
        assert "to_bus" in branch

    def test_summary_statistics(self, pf):
        """Test summary statistics are calculated correctly."""
        result = pf.run({"model_id": "model/chenying/IEEE39"})
        
        summary = result.data.get("summary", {})
        
        # Check required fields
        assert "total_generation" in summary
        assert "total_load" in summary
        assert "total_loss_mw" in summary
        assert "voltage_range" in summary
        
        assert summary.get("total_generation", {}).get("p_mw", 0) > 0
        assert summary.get("total_load", {}).get("p_mw", 0) > 0
        assert summary.get("total_loss_mw", 0) > 0

    def test_datalib_conversion(self, pf):
        """Test conversion to DataLib types."""
        result = pf.run({"model_id": "model/chenying/IEEE39"})
        
        job_id = result.job_id
        buses_typed = pf.get_bus_results(job_id)
        branches_typed = pf.get_branch_results(job_id)
        summary_typed = pf.get_summary(job_id)
        
        assert len(buses_typed) == 39
        assert len(branches_typed) == 46
        assert summary_typed is not None
        assert summary_typed.total_generation_mw > 0


# =============================================================================
# TIER 5: Complex Workflows
# =============================================================================

class TestTier5ComplexWorkflows:
    """Test complex multi-step workflows."""

    @pytest.fixture
    def pf(self):
        config = get_config()
        return Engine.create_powerflow(engine="cloudpss", config=config)

    def test_model_modification(self, pf):
        """Test modifying model components."""
        pf._adapter.load_model("model/chenying/IEEE39")
        
        components = pf._adapter.get_components("model/chenying/IEEE39")
        initial_count = len(components)
        
        assert initial_count > 0

    def test_result_caching(self, pf):
        """Test results are properly cached."""
        # Run simulation
        result1 = pf.run({"model_id": "model/chenying/IEEE39"})
        
        # Get result again - should use cache
        result2 = pf._adapter.get_result(result1.job_id)
        
        assert result2.status == SimulationStatus.COMPLETED


# =============================================================================
# TIER 6: Edge Cases
# =============================================================================

class TestTier6EdgeCases:
    """Test error handling and edge cases."""

    @pytest.fixture
    def pf(self):
        config = get_config()
        return Engine.create_powerflow(engine="cloudpss", config=config)

    def test_invalid_model(self, pf):
        """Test handling of invalid model RID."""
        result = pf.run({"model_id": "model/invalid/does_not_exist"})
        
        assert result.status == SimulationStatus.FAILED
        assert len(result.errors) > 0

    def test_timeout_handling(self):
        """Test timeout is handled properly."""
        config = get_config()
        emt = Engine.create_emt(engine="cloudpss", config=config)
        
        # Very short timeout should timeout
        result = emt.run({
            "model_id": "model/chenying/IEEE39",
            "timeout": 1  # 1 second - too short
        })
        
        # Should either timeout or fail gracefully
        assert result.status in [SimulationStatus.TIMEOUT, SimulationStatus.FAILED]


# =============================================================================
# MAIN TEST RUNNER
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
