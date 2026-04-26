# Smoke Test Improvement Checklist

Status on 2026-04-25: resolved for `cloudpss_skills_v2/tests`.

- Removed all `pytest.mark.smoke` and `pytest.mark.needs_improvement` usages from the v2 test suite.
- Added `cloudpss_skills_v2/tests/test_integration_quality_gate.py` to prevent those markers from returning.
- Added/kept the strict registry integration matrix so every registered skill is instantiated from `SkillRegistry`, validated, run, and checked for successful `SkillResult` outputs/artifacts.
- Replaced the weak DataLib integration file with real pandapower `case14` result conversion into `BusData`, `BranchData`, and `NetworkSummary`.
- Live CloudPSS tests are scoped to `http://166.111.60.76:50001` with `.cloudpss_token_internal`; public CloudPSS endpoints are intentionally outside the current test target.

Verification:

```bash
rg -n "pytest\\.mark\\.(smoke|needs_improvement)|smoke:|needs_improvement:" cloudpss_skills_v2/tests pytest.ini
timeout 300s python -m pytest -q cloudpss_skills_v2/tests/test_integration_quality_gate.py cloudpss_skills_v2/tests/test_integration_cloudpss.py cloudpss_skills_v2/tests/test_integration_registry_matrix.py
timeout 600s python -m pytest -q cloudpss_skills_v2/tests
```
