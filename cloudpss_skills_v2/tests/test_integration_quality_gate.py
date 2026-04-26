"""Quality gates that prevent fake integration coverage from returning."""

from __future__ import annotations

from pathlib import Path


def test_no_smoke_or_needs_improvement_markers_remain():
    tests_root = Path(__file__).parent
    forbidden = ("pytest.mark." + "smoke", "pytest.mark." + "needs_improvement")
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
