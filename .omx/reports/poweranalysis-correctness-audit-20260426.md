# PowerAnalysis Correctness Audit

Date: 2026-04-26

## Classification

- `REAL_ENGINE`: Uses CloudPSS or pandapower calculation outputs as the primary data source.
- `TRACE_DRIVEN`: Uses explicit user/test supplied traces, matrices, or scenario measurements; no hidden synthetic data.
- `FORMULA_DRIVEN`: Uses deterministic engineering formulas over explicit inputs; useful but not a full engine simulation.
- `HEURISTIC`: Uses simplified approximations or scan rules; must not be represented as full physical simulation.
- `NEEDS_REVIEW`: Output semantics require domain review before claiming engineering correctness.

## High-Risk Fixes Completed

| Skill | Previous Risk | Current Guardrail | Evidence |
| --- | --- | --- | --- |
| `frequency_response` | Used an internal fixed frequency array after a power-flow call, so results looked like dynamic response without dynamic data. | Requires `frequency_trace.time` and `frequency_trace.frequency_hz`; output declares `data_source: frequency_trace`. | Target tests require missing trace validation failure and trace-derived nadir. |
| `disturbance_severity` | Used an internal fixed voltage trace after a power-flow call. | Requires `voltage_trace.time` and `voltage_trace.voltage_pu`; output declares `data_source: voltage_trace`. | Target tests require missing trace validation failure and trace-derived voltage dip. |
| `transient_stability` | Used hard-coded rotor angles and reported transient stability. | Requires `rotor_angle_trace.angles_deg`; output declares `data_source: rotor_angle_trace`. | Target tests require missing angle validation failure and trace-derived stability. |
| `small_signal_stability` | Used a hard-coded state matrix and reported eigenvalue stability. | Requires numeric non-empty square `state_matrix`; output declares `data_source: state_matrix`. | Target tests require missing matrix validation failure and matrix-derived eigenvalues. |
| `emt_fault_study` | Inferred scenario severity from scenario names/default deviations. | Requires explicit `voltage_deviation` or prefault/minimum voltage measurements for enabled scenarios. | Target tests reject unmeasured scenarios and verify measurement-derived deviation. |

## Current Risk Map

| Skill | Class | Notes |
| --- | --- | --- |
| `power_flow`, `batch_powerflow`, `contingency_analysis`, `n1_security`, `n2_security`, `maintenance_security`, `loss_analysis`, `voltage_stability`, `param_scan`, `parameter_sensitivity`, `dudv_curve`, `vsi_weak_bus` | `REAL_ENGINE` / `NEEDS_REVIEW` | Driven by pandapower/CloudPSS power-flow paths. Remaining review should focus on whether each metric is computed from the correct result fields and whether thresholds match intended engineering standards. |
| `short_circuit` | `REAL_ENGINE` | Uses pandapower short-circuit or CloudPSS short-circuit adapter. Peak-current normalization was fixed earlier. |
| `emt_n1_screening`, `emt_simulation`, `harmonic_analysis` | `REAL_ENGINE` / `TRACE_DRIVEN` | Live EMT path targets `http://166.111.60.76:50001`; harmonic analysis can also operate on explicit waveform data. |
| `frequency_response`, `disturbance_severity`, `transient_stability`, `small_signal_stability`, `emt_fault_study` | `TRACE_DRIVEN` | No longer generates hidden synthetic dynamic data. Correctness now depends on caller-provided traces/matrices coming from a trusted simulation or measurement pipeline. |
| `fault_clearing_scan`, `fault_severity_scan`, `transient_stability_margin` | `FORMULA_DRIVEN` / `HEURISTIC` | Bounded deterministic scans over explicit inputs. They should be documented as screening/estimation tools until connected to EMT/time-domain simulations. |
| `power_quality_analysis`, `renewable_integration`, `reactive_compensation_design`, `thevenin_equivalent`, `protection_coordination`, `orthogonal_sensitivity` | `FORMULA_DRIVEN` / `NEEDS_REVIEW` | Use formulas or configured engineering inputs. Need domain validation against standards and known cases before claiming full professional-grade correctness. |

## Next Correctness Work

1. Replace `thevenin_equivalent` fixed impedance estimate with adapter-provided short-circuit/Thevenin data or explicit validated inputs.
2. Connect `fault_clearing_scan` and `transient_stability_margin` to EMT/time-domain results, or rename/document them as estimation-only.
3. Review `power_quality_analysis` harmonic/unbalance sources; current THD can be formula-driven but should use waveform/harmonic measurements when available.
4. Validate protection coordination curves and margins against known IEC examples.
5. Add per-skill `data_source` fields consistently where output could otherwise be mistaken for engine-derived physical results.

## Verification

- `python -m pytest -q cloudpss_skills_v2/tests/test_frequency_response.py cloudpss_skills_v2/tests/test_disturbance_severity.py cloudpss_skills_v2/tests/test_transient_stability.py cloudpss_skills_v2/tests/test_small_signal_stability.py cloudpss_skills_v2/tests/test_emt_fault_study.py`
  - PASS: 77 passed.
- `python -m pytest -q cloudpss_skills_v2/tests/test_integration_registry_matrix.py -k 'frequency_response or disturbance_severity or transient_stability or small_signal_stability or emt_fault_study'`
  - PASS: 6 passed, 42 deselected.
