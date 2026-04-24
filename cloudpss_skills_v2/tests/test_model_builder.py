"""Tests for cloudpss_skills_v2.tools.model_builder."""

from cloudpss_skills_v2.tools.model_builder import ModelBuilderTool


class TestModelBuilderTool:
    def test_scalar_coercion(self):
        tool = ModelBuilderTool()
        assert tool._coerce_scalar_value("5", "int") == 5
        assert tool._coerce_scalar_value("1.5", "float") == 1.5
        assert tool._coerce_scalar_value("true", "bool") is True
        assert tool._coerce_scalar_value(123, "string") == "123"

    def test_lookup_helpers(self):
        tool = ModelBuilderTool()
        assert tool._normalize_lookup_value(" Bus-1 ") == "bus_1"
        assert tool._first_present({"a": None, "b": 2}, ["a", "b"]) == 2

    def test_validate_operations(self):
        tool = ModelBuilderTool()
        valid, errors = tool.validate({"base_model": {}, "operations": [{"action": "add"}]})
        assert valid is False
        assert "component is required for add" in errors[0]

    def test_run_add_modify_delete_components(self):
        tool = ModelBuilderTool()
        config = {
            "base_model": {"components": [{"id": "bus1", "name": "Bus1", "parameters": {"kv": 110}}]},
            "operations": [
                {
                    "action": "add",
                    "component": {"id": "gen1", "name": "Gen1", "parameters": {"p_set": "100", "enabled": "true"}},
                    "schema": {"p_set": "float", "enabled": "bool"},
                },
                {
                    "action": "modify",
                    "id": "gen1",
                    "updates": {"parameters": {"p_set": "120", "enabled": "false"}},
                    "schema": {"p_set": "float", "enabled": "bool"},
                },
                {"action": "delete", "id": "bus1"},
            ],
        }
        result = tool.run(config)

        assert result.status.value == "success"
        components = result.data["model"]["components"]
        assert len(components) == 1
        assert components[0]["id"] == "gen1"
        assert components[0]["parameters"]["p_set"] == 120.0
        assert components[0]["parameters"]["enabled"] is False
        assert result.metrics["operation_count"] == 3

    def test_run_fails_when_target_missing(self):
        tool = ModelBuilderTool()
        result = tool.run({"base_model": {"components": []}, "operations": [{"action": "delete", "id": "missing"}]})
        assert result.status.value == "failed"
        assert result.error is not None
        assert "not found" in result.error
