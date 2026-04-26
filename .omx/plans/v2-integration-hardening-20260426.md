# CloudPSS SkillHub V2 Integration Hardening Plan

## Requirements Summary

The current priority is not adding new skills. It is turning the newly proven
`cloudpss_skills_v2` integration work into a maintainable baseline:

- Keep fake/smoke integration tests out of the proof path.
- Separate private live CloudPSS coverage from CI-safe local coverage.
- Keep project evidence documents synchronized with actual test commands.
- Deepen assertions for high-value skills before expanding scope.

## Decision

Use a two-lane test strategy:

1. **Default v2 lane**: compile, quality gates, pandapower/local integrations,
   DataLib conversion, and the strict registered-skill matrix. Private CloudPSS
   entries in the matrix may skip when `.cloudpss_token_internal` or
   `166.111.60.76:50001` is unavailable.
2. **Private live lane**: full local-server CloudPSS tests, enabled only when
   the private token and server route are available.

## Acceptance Criteria

- A maintainer can run a documented CI-safe v2 command that does not require
  the private CloudPSS server.
- A maintainer can run a documented private live command that exercises
  `http://166.111.60.76:50001`.
- Project evidence docs distinguish legacy mainline evidence from v2 skill
  registry evidence.
- No `smoke` / `needs_improvement` pytest markers return to
  `cloudpss_skills_v2/tests`.
- Full v2 suite remains green on the current workstation.

## Implementation Steps

1. Add v2 test marker documentation and command recipes.
2. Add CI workflow coverage for v2 compile, quality gate, and CI-safe matrix.
3. Keep private live tests opt-in through repository secrets.
4. Update mainline evidence documents with the latest v2 integration evidence
   and boundaries.
5. Preserve `.omx/reports/integration-issues-20260425.md` as the detailed
   issue register.

## Risks

- **Private server unavailable in CI**: mitigated by live-only skip gates and
  an opt-in private-live job.
- **Evidence drift**: mitigated by documenting exact commands in both the
  smoke cleanup checklist and mainline evidence register.
- **Overclaiming correctness**: mitigated by explicitly separating "runs and
  returns valid shape" from deeper engineering/algorithm validation.

## Verification

```bash
python -m compileall -q cloudpss_skills_v2
rg -n "pytest\\.mark\\.(smoke|needs_improvement)|smoke:|needs_improvement:" cloudpss_skills_v2/tests pytest.ini
timeout 300s python -m pytest -q cloudpss_skills_v2/tests/test_integration_quality_gate.py cloudpss_skills_v2/tests/test_integration_registry_matrix.py
timeout 600s python -m pytest -q cloudpss_skills_v2/tests
```

## Follow-Up Backlog

1. Add deeper physical/business assertions for priority skills:
   `n1_security`, `contingency_analysis`, `voltage_stability`,
   `short_circuit`, `emt_n1_screening`, `waveform_export`,
   `model_parameter_extractor`.
2. Review repaired algorithms with domain criteria:
   `orthogonal_sensitivity`, `transient_stability_margin`,
   `emt_fault_study`, `fault_severity_scan`.
3. Decide whether true CloudPSS-vs-pandapower numerical cross-engine
   comparison is a product goal; do not treat current pandapower interface
   tests as that comparison.
