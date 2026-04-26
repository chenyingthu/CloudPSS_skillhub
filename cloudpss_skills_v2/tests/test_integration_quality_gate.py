"""Quality gates that prevent fake integration coverage from returning."""

from __future__ import annotations

from pathlib import Path

import cloudpss_skills_v2  # noqa: F401 - populate registry
from cloudpss_skills_v2 import SkillRegistry
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
