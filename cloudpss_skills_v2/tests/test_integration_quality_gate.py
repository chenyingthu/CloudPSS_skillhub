"""Quality gates that prevent fake integration coverage from returning."""

from __future__ import annotations

import json
from pathlib import Path

import cloudpss_skills_v2  # noqa: F401 - populate registry
from cloudpss_skills_v2 import SkillRegistry
from cloudpss_skills_v2.tests.golden_cases import TRUSTED_GOLDEN_CASES
from cloudpss_skills_v2.tools.model_validator import ModelValidatorTool


def test_no_weak_test_labels_remain():
    tests_root = Path(__file__).parent
    weak_a = "smo" + "ke"
    weak_b = "needs" + "_" + "improvement"
    forbidden = (
        "pytest.mark." + weak_a,
        "pytest.mark." + weak_b,
        weak_a + " test",
        "Smo" + "ke test",
        weak_b,
    )
    offenders: list[str] = []

    for path in sorted(tests_root.glob("test*.py")):
        if path.name == Path(__file__).name:
            continue
        text = path.read_text()
        for marker in forbidden:
            if marker in text:
                offenders.append(f"{path.name}: {marker}")

    assert offenders == []


def test_live_cloudpss_fixtures_target_local_server(
    cloudpss_api_url: str, cloudpss_model_rid: str
):
    assert cloudpss_api_url == "http://166.111.60.76:50001"
    assert cloudpss_model_rid.startswith("model/chenying/")


def test_trusted_analysis_rejects_hidden_synthetic_physical_data():
    project_root = Path(__file__).parents[1]
    forbidden_snippets = (
        "z_th_real = 0.01",
        "z_th_imag = 0.05",
        "0.01 * (h % 3 + 1)",
        "unbalance = 0.02",
        "ct < 0.15",
        "def _estimate_cct",
        "primary_feeder",
        "backup_feeder",
    )
    offenders: list[str] = []

    for path in sorted((project_root / "poweranalysis").glob("*.py")):
        text = path.read_text()
        for snippet in forbidden_snippets:
            if snippet in text:
                offenders.append(f"{path.relative_to(project_root)}: {snippet}")

    assert offenders == []


def test_model_validator_is_registered_as_real_validator():
    assert SkillRegistry.get("model_validator") is ModelValidatorTool


def test_trusted_golden_cases_carry_source_or_derivation_metadata():
    missing: list[str] = []

    for case_name, case in TRUSTED_GOLDEN_CASES.items():
        reference = case.get("reference")
        if not isinstance(reference, dict):
            missing.append(f"{case_name}: reference")
            continue
        for key in ("standard_basis", "formula", "limitations", "sources"):
            if not reference.get(key):
                missing.append(f"{case_name}: reference.{key}")

        sources = reference.get("sources", [])
        if not isinstance(sources, list) or not sources:
            missing.append(f"{case_name}: reference.sources")
            continue
        for idx, source in enumerate(sources):
            if not isinstance(source, dict) or not source.get("title"):
                missing.append(f"{case_name}: reference.sources[{idx}].title")
                continue
            if not source.get("url") and not (
                source.get("source_kind") == "derivation" and source.get("derivation")
            ):
                missing.append(f"{case_name}: reference.sources[{idx}].url_or_derivation")

    assert missing == []


def test_golden_config_artifacts_do_not_claim_unverified_engine_support():
    golden_config_dir = Path(__file__).parent / "golden_configs"
    violations: list[str] = []

    for path in sorted(golden_config_dir.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        capability = data.get("capability")
        if not isinstance(capability, dict):
            violations.append(f"{path.name}: missing capability")
            continue
        if capability.get("skill_runnable") is not True:
            violations.append(f"{path.name}: skill_runnable must be true")
        if capability.get("engine_runnable") is not False:
            violations.append(f"{path.name}: engine_runnable must remain false until a real engine benchmark exists")
        if capability.get("engine_claim") != "none":
            violations.append(f"{path.name}: engine_claim must be none")
        if not capability.get("engine_notes"):
            violations.append(f"{path.name}: engine_notes is required")

    assert violations == []


def test_engine_golden_cases_require_engine_artifacts_and_expected_results():
    engine_case_dir = Path(__file__).parent / "golden_engine_cases"
    violations: list[str] = []

    for path in sorted(engine_case_dir.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        capability = data.get("capability")
        if not isinstance(capability, dict):
            violations.append(f"{path.name}: missing capability")
            continue
        if capability.get("engine_runnable") is not True:
            violations.append(f"{path.name}: engine_runnable must be true")
        if capability.get("engine") != "pandapower":
            violations.append(f"{path.name}: only pandapower engine cases are currently supported")
        if not data.get("model"):
            violations.append(f"{path.name}: model artifact is required")
        expected = data.get("expected")
        if not isinstance(expected, dict):
            violations.append(f"{path.name}: expected results are required")
            continue
        if not expected.get("power_flow") or not expected.get("short_circuit"):
            violations.append(f"{path.name}: power_flow and short_circuit expected results are required")

    assert violations == []
