# CloudPSS SkillHub V2 Integration Test Governance Plan

## Objective

Prove which `cloudpss_skills_v2` modules are actually usable through real integration tests, then fix every reproducible and locally correctable defect. Keep unresolved items explicit for human judgment.

## Non-Negotiable Test Rules

1. No mock, fake, or patched engine call counts may be counted as integration coverage.
2. Import-only, instantiation-only, attribute-only, and `result is not None` tests are smoke tests, not integration tests.
3. Tests that accept both success and failure do not prove functionality.
4. Live CloudPSS tests must use real token/config, real model RID, real SDK calls, and assert domain-shaped outputs.
5. Pandapower tests may be real integration tests when they run actual pandapower cases and assert physical/result invariants.
6. If an external service/model/token is unavailable, record `BLOCKED_EXTERNAL` rather than marking the feature passed.
7. Every failed integration test gets an issue record with module, command, failure, likely cause, fix status, and retest evidence.
8. The loop is: test -> record -> fix locally correctable defects -> retest -> repeat until green or blocked.

## Module Matrix

### PowerAPI / PowerSkill

- CloudPSS adapters: power flow, EMT, short circuit via EMT.
- Pandapower adapters: power flow, short circuit.
- PowerSkill facades: `PowerFlow`, `EMT`, `ShortCircuit`, model handle operations.
- Engine factory and adapter registry.

### Simulation Presets

- `power_flow`
- `emt_simulation`

### PowerAnalysis Skills

- Security/contingency: `n1_security`, `n2_security`, `contingency_analysis`, `maintenance_security`.
- Stability: `voltage_stability`, `transient_stability`, `transient_stability_margin`, `small_signal_stability`, `frequency_response`, `vsi_weak_bus`, `dudv_curve`.
- Fault/short-circuit: `short_circuit`, `emt_fault_study`, `emt_n1_screening`, `fault_clearing_scan`, `fault_severity_scan`, `disturbance_severity`.
- Study/scan/math: `batch_powerflow`, `param_scan`, `parameter_sensitivity`, `orthogonal_sensitivity`, `loss_analysis`, `thevenin_equivalent`, `power_quality_analysis`, `harmonic_analysis`, `reactive_compensation_design`, `renewable_integration`, `protection_coordination`.

### Tools

- Model operations: `model_builder`, `model_hub`, `model_parameter_extractor`, `component_catalog`, `topology_check`, `auto_channel_setup`, `auto_loop_breaker`.
- Batch/workflow: `batch_task_manager`, `config_batch_runner`, `study_pipeline`.
- Result processing/export: `waveform_export`, `comtrade_export`, `hdf5_export`, `result_compare`, `compare_visualization`, `visualize`, `report_generator`.

## Execution Strategy

### Phase 1: Inventory and Triage

- Enumerate registered skills and current integration test files.
- Flag existing integration tests that are actually smoke/fake tests and remove
  the weak markers once stronger coverage exists.
- Run existing integration suites with hard timeouts to avoid hangs.
- Split failures into:
  - `CODE_DEFECT`: reproducible local code bug.
  - `TEST_DEFECT`: test is fake, too weak, or invalid.
  - `ENV_BLOCKED`: dependency/token/server/model unavailable.
  - `DESIGN_GAP`: feature lacks a real engine path or known input contract.

### Phase 2: Build Real Integration Harness

- Add/repair fixtures for:
  - Pandapower local engine cases (`case9`, `case14`, `case30`) with domain assertions.
  - CloudPSS live endpoint fixed to `http://166.111.60.76:50001` for this
    campaign.
  - Token from `.cloudpss_token_internal`.
- Add gating that skips only with explicit external-block reason.
- Add per-test timeouts or bounded polling for live tests.

### Phase 3: Module-by-Module Integration Coverage

- For each module, create at least one real integration path:
  - Engine-backed skills: run actual simulation or model operation.
  - Result-processing tools: consume real output from a prior engine run or a committed realistic fixture from real output.
  - Pure algorithm/data modules: use deterministic real-case outputs, not mocks.
- Assert invariants: status, required schema, non-empty typed fields, physical bounds, artifact existence/content where relevant.

### Phase 4: Fix and Retest Loop

- Fix all `CODE_DEFECT` and `TEST_DEFECT` items that are locally correctable.
- Rerun the exact failing command after each fix.
- Rerun the affected module group.
- Rerun the full integration matrix at the end.

### Phase 5: Final Report

- Produce final issue register.
- List modules proven usable, modules blocked externally, and modules needing product/design decisions.
- Include exact commands and passing/failing evidence.

## Initial Commands

```bash
python -m pytest -q cloudpss_skills_v2/tests/test_integration_pandapower.py
python -m pytest -q cloudpss_skills_v2/tests/test_integration_short_circuit.py
python -m pytest -q cloudpss_skills_v2/tests/test_integration_powerskill.py
python -m pytest -q cloudpss_skills_v2/tests/test_integration_skill_flow.py
python -m pytest -q cloudpss_skills_v2/tests/test_integration_tools.py
python -m pytest -q cloudpss_skills_v2/tests/test_integration_cloudpss.py
python -m pytest -q cloudpss_skills_v2/tests/test_integration_local_server.py
python -m pytest -q cloudpss_skills_v2/tests/test_integration_poweranalysis.py
```

Use external `timeout` for every command until test-level timeouts are available.
