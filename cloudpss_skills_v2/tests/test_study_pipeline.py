"""Tests for cloudpss_skills_v2.tools.study_pipeline."""

from __future__ import annotations

import importlib.util
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pytest

from cloudpss_skills_v2.core import SkillResult, SkillStatus

_MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "study_pipeline.py"
_SPEC = importlib.util.spec_from_file_location(
    "cloudpss_skills_v2.tools.study_pipeline_test_module", _MODULE_PATH
)
assert _SPEC is not None and _SPEC.loader is not None
_MODULE = importlib.util.module_from_spec(_SPEC)
sys.modules.setdefault(_SPEC.name, _MODULE)
_SPEC.loader.exec_module(_MODULE)
StudyPipelineTool = _MODULE.StudyPipelineTool


@dataclass
class DummySkill:
    name: str
    status: SkillStatus = SkillStatus.SUCCESS
    result_data: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    calls: list[dict[str, Any]] = field(default_factory=list)

    def run(self, config: dict[str, Any]) -> SkillResult:
        self.calls.append(config)
        return SkillResult(
            skill_name=self.name,
            status=self.status,
            data=self.result_data,
            error=self.error,
        )


@pytest.fixture
def instance() -> StudyPipelineTool:
    return StudyPipelineTool()


def test_validate_rejects_unsupported_features(instance: StudyPipelineTool):
    valid, errors = instance.validate(
        {
            "pipeline": [
                {"name": "loop", "skill": "power_flow", "for_each": [1, 2]},
                {"name": "nested", "skill": "n1_security", "pipeline": []},
            ]
        }
    )

    assert valid is False
    assert any("for_each" in error for error in errors)
    assert any("nested pipeline" in error for error in errors)


def test_expand_pipeline_adds_default_names(instance: StudyPipelineTool):
    expanded = instance._expand_pipeline(
        [{"skill": "power_flow", "config": {"value": 1}}, {"name": "two", "skill": "n1_security"}],
        {},
    )

    assert expanded[0]["name"] == "step_1"
    assert expanded[1]["name"] == "two"
    assert expanded[1]["config"] == {}


def test_resolve_var_path_supports_nested_dicts_and_lists(instance: StudyPipelineTool):
    context = {
        "input": {"models": [{"rid": "m1"}]},
        "step1": {"result": {"network": {"rid": "derived"}}},
    }

    assert instance._resolve_var_path("input.models.0.rid", context) == "m1"
    assert instance._resolve_var_path("step1.result.network.rid", context) == "derived"
    assert instance._resolve_var_path("step1.result.missing", context) is None


def test_resolve_config_replaces_strings_and_embedded_values(instance: StudyPipelineTool):
    context = {
        "input": {"model": {"rid": "base-model"}},
        "step1": {"result": {"case": "N-1"}},
        "context": {"region": "east"},
    }

    resolved = instance._resolve_config(
        {
            "model": "${input.model}",
            "label": "case-${step1.result.case}",
            "tags": ["${context.region}", "fixed"],
        },
        context,
    )

    assert resolved == {
        "model": {"rid": "base-model"},
        "label": "case-N-1",
        "tags": ["east", "fixed"],
    }


def test_evaluate_condition_supports_comparisons_and_boolean_ops(instance: StudyPipelineTool):
    context = {
        "step1": {"status": "success", "result": {"score": 92, "converged": True}},
        "input": {"threshold": 90},
    }

    assert instance._evaluate_condition("${step1.status} == 'success'", context) is True
    assert instance._evaluate_condition("${step1.result.score} > ${input.threshold}", context) is True
    assert instance._evaluate_condition(
        "${step1.status} == 'success' and not (${step1.result.score} < 90)",
        context,
    ) is True
    assert instance._evaluate_condition("${step1.result.converged} and ${step1.result.score} < 50", context) is False


def test_get_ready_steps_returns_next_eligible_step(instance: StudyPipelineTool):
    pipeline = [
        {"name": "step1", "skill": "power_flow"},
        {"name": "step2", "skill": "n1_security", "if": "${step1.status} == 'success'"},
        {"name": "step3", "skill": "report_generator", "if": "${step2.status} == 'success'"},
    ]
    context = {"step1": {"status": "success"}, "step2": {"status": "failed"}}

    assert instance._get_ready_steps(pipeline, ["step1"], context, False) == [pipeline[1]]
    assert instance._get_ready_steps(pipeline, ["step1", "step2"], context, False) == []


def test_run_executes_steps_sequentially_and_passes_resolved_results(
    instance: StudyPipelineTool, monkeypatch: pytest.MonkeyPatch
):
    skills = {
        "power_flow": DummySkill(
            name="power_flow",
            result_data={"model": {"rid": "derived-model"}, "score": 95},
        ),
        "n1_security": DummySkill(
            name="n1_security",
            result_data={"passed": True, "model": {"rid": "security-model"}},
        ),
        "report_generator": DummySkill(
            name="report_generator",
            result_data={"report_id": "r-1"},
        ),
    }
    monkeypatch.setattr(instance, "_load_skill", skills.__getitem__)

    result = instance.run(
        {
            "input": {"model": {"rid": "base-model"}},
            "context": {"owner": "ops"},
            "pipeline": [
                {
                    "name": "step1",
                    "skill": "power_flow",
                    "config": {"model": "${input.model}", "owner": "${context.owner}"},
                },
                {
                    "name": "step2",
                    "skill": "n1_security",
                    "if": "${step1.status} == 'success' and ${step1.result.score} > 90",
                    "config": {"model": "${step1.result.model}", "source": "step1"},
                },
                {
                    "name": "step3",
                    "skill": "report_generator",
                    "config": {
                        "summary": "${step2.result.passed}",
                        "model": "${step2.result.model.rid}",
                    },
                },
            ],
        }
    )

    assert result.status == SkillStatus.SUCCESS
    assert [step["name"] for step in result.data["steps"]] == ["step1", "step2", "step3"]
    assert skills["power_flow"].calls == [{"model": {"rid": "base-model"}, "owner": "ops"}]
    assert skills["n1_security"].calls == [{"model": {"rid": "derived-model"}, "source": "step1"}]
    assert skills["report_generator"].calls == [{"summary": True, "model": "security-model"}]
    assert result.data["context"]["step2"]["result"]["passed"] is True
    assert result.metrics["failed_steps"] == 0


def test_run_skips_step_when_condition_is_false(
    instance: StudyPipelineTool, monkeypatch: pytest.MonkeyPatch
):
    power_flow = DummySkill(name="power_flow", result_data={"score": 10})
    reporter = DummySkill(name="report_generator", result_data={"done": True})
    monkeypatch.setattr(
        instance,
        "_load_skill",
        {"power_flow": power_flow, "report_generator": reporter}.__getitem__,
    )

    result = instance.run(
        {
            "pipeline": [
                {"name": "step1", "skill": "power_flow", "config": {}},
                {
                    "name": "step2",
                    "skill": "report_generator",
                    "if": "${step1.result.score} > 90",
                    "config": {"value": "should-not-run"},
                },
            ]
        }
    )

    assert result.status == SkillStatus.SUCCESS
    assert reporter.calls == []
    assert result.data["skipped_steps"] == ["step2"]
    assert result.data["context"]["step2"]["status"] == "skipped"


def test_run_stops_on_failure_by_default(instance: StudyPipelineTool, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(
        instance,
        "_load_skill",
        {
            "power_flow": DummySkill(name="power_flow", result_data={"score": 95}),
            "n1_security": DummySkill(
                name="n1_security",
                status=SkillStatus.FAILED,
                error="security analysis failed",
                result_data={"success": False},
            ),
            "report_generator": DummySkill(name="report_generator", result_data={"done": True}),
        }.__getitem__,
    )

    result = instance.run(
        {
            "pipeline": [
                {"name": "step1", "skill": "power_flow", "config": {}},
                {"name": "step2", "skill": "n1_security", "config": {}},
                {"name": "step3", "skill": "report_generator", "config": {}},
            ]
        }
    )

    assert result.status == SkillStatus.FAILED
    assert result.data["failed_step"] == "step2"
    assert result.error == "security analysis failed"
    assert [step["name"] for step in result.data["steps"]] == ["step1", "step2"]


def test_run_continues_on_failure_when_enabled(
    instance: StudyPipelineTool, monkeypatch: pytest.MonkeyPatch
):
    skills = {
        "power_flow": DummySkill(name="power_flow", result_data={"score": 95}),
        "n1_security": DummySkill(
            name="n1_security",
            status=SkillStatus.FAILED,
            error="security analysis failed",
            result_data={"success": False},
        ),
        "report_generator": DummySkill(name="report_generator", result_data={"done": True}),
    }
    monkeypatch.setattr(instance, "_load_skill", skills.__getitem__)

    result = instance.run(
        {
            "continue_on_failure": True,
            "pipeline": [
                {"name": "step1", "skill": "power_flow", "config": {}},
                {"name": "step2", "skill": "n1_security", "config": {}},
                {"name": "step3", "skill": "report_generator", "config": {}},
            ],
        }
    )

    assert result.status == SkillStatus.FAILED
    assert skills["report_generator"].calls == [{}]
    assert result.metrics["failed_steps"] == 1
    assert result.data["executed_steps"] == ["step1", "step2", "step3"]


def test_run_handles_unknown_skill_as_failure(instance: StudyPipelineTool):
    result = instance.run(
        {"pipeline": [{"name": "step1", "skill": "definitely_missing", "config": {}}]}
    )

    assert result.status == SkillStatus.FAILED
    assert result.data["failed_step"] == "step1"
    assert "unknown skill" in result.error
