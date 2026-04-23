import pytest
from cloudpss_skills_v2.tools.topology_check import TopologyCheckTool


class TestTopologyCheckTool:
    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_import(self):
        assert TopologyCheckTool is not None

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_instantiation(self):
        instance = TopologyCheckTool()
        assert instance is not None

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_has_name_attribute(self):
        instance = TopologyCheckTool()
        assert instance.name == "topology_check"

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_has_description(self):
        instance = TopologyCheckTool()
        assert hasattr(instance, "description")

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_has_config_schema(self):
        instance = TopologyCheckTool()
        schema = instance.config_schema
        assert schema is not None
        assert schema["type"] == "object"

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_validate_empty_config(self):
        instance = TopologyCheckTool()
        valid, errors = instance.validate({})
        assert valid is False

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_validate_missing_rid(self):
        instance = TopologyCheckTool()
        config = {"model": {}}
        valid, errors = instance.validate(config)
        assert valid is False

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_validate_valid_config(self):
        instance = TopologyCheckTool()
        config = {"model": {"rid": "test_model"}}
        valid, errors = instance.validate(config)
        assert valid is True

    def test_build_adjacency_single_branch(self):
        instance = TopologyCheckTool()
        buses = ["B1", "B2", "B3"]
        branches = [{"from_bus": "B1", "to_bus": "B2"}]
        adj = instance._build_adjacency(buses, branches)
        assert "B1" in adj
        assert "B2" in adj
        assert "B3" in adj
        assert "B2" in adj["B1"]
        assert "B1" in adj["B2"]

    def test_build_adjacency_multiple_branches(self):
        instance = TopologyCheckTool()
        buses = ["B1", "B2", "B3", "B4"]
        branches = [
            {"from_bus": "B1", "to_bus": "B2"},
            {"from_bus": "B2", "to_bus": "B3"},
        ]
        adj = instance._build_adjacency(buses, branches)
        assert len(adj["B1"]) == 1
        assert len(adj["B2"]) == 2
        assert len(adj["B3"]) == 1
        assert len(adj["B4"]) == 0

    def test_build_adjacency_with_from_bus_name(self):
        instance = TopologyCheckTool()
        buses = ["B1", "B2"]
        branches = [{"from_bus_name": "B1", "to_bus_name": "B2"}]
        adj = instance._build_adjacency(buses, branches)
        assert "B2" in adj["B1"]
        assert "B1" in adj["B2"]

    def test_build_adjacency_ignores_invalid(self):
        instance = TopologyCheckTool()
        buses = ["B1", "B2"]
        branches = [{"from_bus": "B1", "to_bus": "B99"}]
        adj = instance._build_adjacency(buses, branches)
        assert "B99" not in adj

    def test_find_islands_single_island(self):
        instance = TopologyCheckTool()
        adj = {"B1": ["B2"], "B2": ["B1", "B3"], "B3": ["B2"]}
        islands = instance._find_islands(adj)
        assert len(islands) == 1

    def test_find_islands_multiple_islands(self):
        instance = TopologyCheckTool()
        adj = {"B1": ["B2"], "B2": ["B1"], "B3": ["B4"], "B4": ["B3"]}
        islands = instance._find_islands(adj)
        assert len(islands) == 2

    def test_find_islands_single_node(self):
        instance = TopologyCheckTool()
        adj = {"B1": [], "B2": ["B3"], "B3": ["B2"]}
        islands = instance._find_islands(adj)
        assert len(islands) == 2

    def test_find_islands_empty(self):
        instance = TopologyCheckTool()
        adj = {}
        islands = instance._find_islands(adj)
        assert islands == []

    def test_find_dangling_buses_none(self):
        instance = TopologyCheckTool()
        buses = ["B1", "B2"]
        adj = {"B1": ["B2"], "B2": ["B1"]}
        dangling = instance._find_dangling_buses(buses, adj)
        assert dangling == []

    def test_find_dangling_buses_with_dangling(self):
        instance = TopologyCheckTool()
        buses = ["B1", "B2", "B3"]
        adj = {"B1": ["B2"], "B2": ["B1"], "B3": []}
        dangling = instance._find_dangling_buses(buses, adj)
        assert "B3" in dangling

    def test_find_dangling_buses_multiple(self):
        instance = TopologyCheckTool()
        buses = ["B1", "B2", "B3", "B4"]
        adj = {"B1": [], "B2": [], "B3": ["B4"], "B4": ["B3"]}
        dangling = instance._find_dangling_buses(buses, adj)
        assert len(dangling) == 2

    def test_find_isolated_generators_none(self):
        instance = TopologyCheckTool()
        buses = ["B1", "B2"]
        generators = [
            {"name": "G1", "bus": "B1"},
            {"name": "G2", "bus": "B2"},
        ]
        adj = {"B1": ["B2"], "B2": ["B1"]}
        isolated = instance._find_isolated_generators(buses, generators, adj)
        assert isolated == []

    def test_find_isolated_generators_with_isolated(self):
        instance = TopologyCheckTool()
        buses = ["B1", "B2", "B3"]
        generators = [
            {"name": "G1", "bus": "B1"},
            {"name": "G2", "bus": "B3"},
        ]
        adj = {"B1": ["B2"], "B2": ["B1"], "B3": []}
        isolated = instance._find_isolated_generators(buses, generators, adj)
        assert "G2" in isolated

    def test_find_isolated_generators_bus_not_in_adj(self):
        instance = TopologyCheckTool()
        buses = ["B1", "B2"]
        generators = [{"name": "G1", "bus": "B99"}]
        adj = {"B1": ["B2"], "B2": ["B1"]}
        isolated = instance._find_isolated_generators(buses, generators, adj)
        assert "G1" in isolated

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_has_run_method(self):
        instance = TopologyCheckTool()
        assert hasattr(instance, "run")
        assert callable(instance.run)

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_has_log_method(self):
        instance = TopologyCheckTool()
        assert hasattr(instance, "_log")
        assert callable(instance._log)
