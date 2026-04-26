"""Tests for cloudpss_skills_v2.tools.model_validator."""

from cloudpss_skills_v2.core import SkillStatus
from cloudpss_skills_v2.tools.model_builder import ModelBuilderTool
from cloudpss_skills_v2.tools.model_validator import ModelValidatorTool


def _trusted_test_case_config():
    return {
        "base_model": {
            "rid": "inline/two_bus",
            "components": [
                {"id": "bus1", "type": "bus", "parameters": {"vn_kv": 110}},
                {"id": "bus2", "type": "bus", "parameters": {"vn_kv": 110}},
                {
                    "id": "line12",
                    "type": "line",
                    "from_bus": "bus1",
                    "to_bus": "bus2",
                    "parameters": {"length_km": 10},
                },
            ],
        },
        "operations": [
            {
                "action": "add",
                "component": {
                    "id": "pv_bus2",
                    "type": "pv",
                    "bus": "bus2",
                    "parameters": {"p_mw": "50"},
                },
                "schema": {"p_mw": "float"},
            }
        ],
    }


def test_model_validator_is_distinct_from_model_builder():
    assert ModelValidatorTool.name == "model_validator"
    assert ModelValidatorTool is not ModelBuilderTool


def test_model_builder_output_passes_local_structure_topology_parameters():
    builder = ModelBuilderTool()
    validator = ModelValidatorTool()
    built = builder.run(_trusted_test_case_config())

    result = validator.run(
        {
            "model": built.data["model"],
            "validation": {"phases": ["structure", "topology", "parameters"]},
            "expectations": {
                "components_present": ["pv_bus2"],
                "component_count": 4,
            },
        }
    )

    assert result.status == SkillStatus.SUCCESS
    assert result.data["status"] == "pass"
    assert result.data["component_count"] == 4
    assert result.data["issues"] == []


def test_model_validator_rejects_unconnected_renewable_component():
    validator = ModelValidatorTool()
    result = validator.run(
        {
            "model": {
                "components": [
                    {"id": "bus1", "type": "bus"},
                    {"id": "pv1", "type": "pv", "parameters": {"p_mw": 50}},
                ]
            },
            "validation": {"phases": ["structure", "topology", "parameters"]},
        }
    )

    assert result.status == SkillStatus.FAILED
    assert any(issue["type"] == "source_unconnected" for issue in result.data["issues"])
    assert any(
        issue["type"] == "renewable_missing_connection"
        for issue in result.data["issues"]
    )


def test_model_validator_rejects_missing_required_component_parameter():
    validator = ModelValidatorTool()
    result = validator.run(
        {
            "model": {
                "components": [
                    {"id": "bus1", "type": "bus"},
                    {"id": "bus2", "type": "bus"},
                    {"id": "line12", "type": "line", "from_bus": "bus1", "to_bus": "bus2"},
                ]
            },
            "validation": {"phases": ["parameters"]},
            "component_requirements": {"line12": ["length_km"]},
        }
    )

    assert result.status == SkillStatus.FAILED
    assert any(
        issue["type"] == "missing_required_parameter"
        and issue["component"] == "line12"
        and issue["parameter"] == "length_km"
        for issue in result.data["issues"]
    )


def test_model_validator_requires_explicit_study_results_for_powerflow_phase():
    builder = ModelBuilderTool()
    validator = ModelValidatorTool()
    built = builder.run(_trusted_test_case_config())

    result = validator.run(
        {
            "model": built.data["model"],
            "validation": {"phases": ["structure", "powerflow"]},
        }
    )

    assert result.status == SkillStatus.FAILED
    assert any(
        issue["type"] == "missing_explicit_study_result"
        for issue in result.data["issues"]
    )


def test_model_validator_accepts_explicit_powerflow_study_result():
    builder = ModelBuilderTool()
    validator = ModelValidatorTool()
    built = builder.run(_trusted_test_case_config())

    result = validator.run(
        {
            "model": built.data["model"],
            "validation": {"phases": ["structure", "powerflow"]},
            "study_results": {"powerflow": {"converged": True}},
        }
    )

    assert result.status == SkillStatus.SUCCESS
    assert result.data["phases"][1]["data_source"] == "study_results.powerflow"
