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
| `thevenin_equivalent` | Used fixed `0.01 + j0.05` pu impedance after a power-flow run and reported SCC/SCR as if derived from the model. | Requires explicit `equivalent.z_th_pu.real/imag` from a trusted upstream Thevenin or short-circuit study; output declares `data_source`, `confidence_level`, and assumptions. | Target tests reject missing impedance; registry matrix supplies explicit impedance; quality gate blocks the old fixed constants. |
| `power_quality_analysis` | Generated harmonic voltages and unbalance internally from harmonic order numbers. | Requires explicit `measurements.harmonic_voltages` and `measurements.phase_voltages_pu`; output declares measurement data source and assumptions. | Target tests reject missing measurements; registry matrix supplies explicit measurements; quality gate blocks the old synthetic formulas. |
| `fault_clearing_scan` | Classified stability with fixed `ct < 0.15` logic, which looked like a time-domain stability result. | Requires explicit `stability_results[].clearing_time/stable`; output declares simulation/trace-derived data source. | Target tests reject missing stability results; registry matrix supplies explicit stability results; quality gate blocks the old fixed cutoff. |
| `transient_stability_margin` | Estimated CCT from target margin when no CCT was supplied. | Requires explicit `fault_scenarios[].cct` and `clearing_time`; output declares CCT data source. | Target tests reject missing CCT and verify margin from supplied values; quality gate blocks `_estimate_cct`. |
| `renewable_integration` | Filled LVRT profile and capacity series with internal defaults, so energy/LVRT conclusions could exceed supplied evidence. | Requires explicit `renewable.capacity_series_mw`, `harmonics.orders`, and `lvrt.profile`; output declares per-check data sources. | Target tests reject missing series; registry matrix/default config supply explicit series/profile. |
| `protection_coordination` | Could synthesize relay definitions from model branches or fixed feeder defaults. | Requires explicit `relays` with positive load and fault current; output declares explicit relay settings as data source. | Target tests reject missing relays; dead fallback generation removed; registry matrix supplies relays. |
| `reactive_compensation_design` | Filled missing SCR, voltage, and reactance with defaults when sizing compensation. | Requires each weak bus to provide `scr`, `voltage_pu`, and `x_pu`; output declares formula-derived explicit weak-bus input. | Target tests reject missing `x_pu` and verify sizing uses supplied reactance; registry matrix supplies `x_pu`. |

## Current Risk Map

| Skill | Class | Notes |
| --- | --- | --- |
| `power_flow`, `batch_powerflow`, `contingency_analysis`, `n1_security`, `n2_security`, `maintenance_security`, `loss_analysis`, `voltage_stability`, `param_scan`, `parameter_sensitivity`, `dudv_curve`, `vsi_weak_bus` | `REAL_ENGINE` / `NEEDS_REVIEW` | Driven by pandapower/CloudPSS power-flow paths. Remaining review should focus on whether each metric is computed from the correct result fields and whether thresholds match intended engineering standards. |
| `short_circuit` | `REAL_ENGINE` | Uses pandapower short-circuit or CloudPSS short-circuit adapter. Peak-current normalization was fixed earlier. |
| `emt_n1_screening`, `emt_simulation`, `harmonic_analysis` | `REAL_ENGINE` / `TRACE_DRIVEN` | Live EMT path targets `http://166.111.60.76:50001`; harmonic analysis can also operate on explicit waveform data. |
| `frequency_response`, `disturbance_severity`, `transient_stability`, `small_signal_stability`, `emt_fault_study` | `TRACE_DRIVEN` | No longer generates hidden synthetic dynamic data. Correctness now depends on caller-provided traces/matrices coming from a trusted simulation or measurement pipeline. |
| `fault_clearing_scan`, `transient_stability_margin` | `TRACE_DRIVEN` / `FORMULA_DRIVEN` | Now require explicit stability/CCT inputs. Correctness depends on the upstream time-domain or stability study that produced those inputs. |
| `fault_severity_scan` | `FORMULA_DRIVEN` / `HEURISTIC` | Bounded deterministic scans over explicit inputs. Should be documented as screening/estimation until connected to short-circuit or EMT results. |
| `power_quality_analysis`, `renewable_integration`, `reactive_compensation_design`, `thevenin_equivalent`, `protection_coordination` | `FORMULA_DRIVEN` | Use deterministic formulas over explicit measurements/settings. They are not hidden simulations; output now marks source/confidence. |
| `orthogonal_sensitivity` | `FORMULA_DRIVEN` / `NEEDS_REVIEW` | Uses configured engineering inputs. Needs domain validation against known cases before claiming full professional-grade correctness. |

## Next Correctness Work

1. Build a shared trusted-analysis metadata contract so all professional outputs consistently expose `data_source`, `confidence_level`, `assumptions`, `limitations`, and `standard_basis`.
2. Connect `thevenin_equivalent`, `fault_clearing_scan`, and `transient_stability_margin` directly to CloudPSS/pandapower short-circuit or EMT/time-domain result adapters where possible, so callers do not need to supply intermediate values manually.
3. Validate protection coordination curves and margins against known IEC/IEEE examples.
4. Validate renewable integration, reactive compensation, and orthogonal sensitivity formulas against known engineering cases and document their standards basis.
5. Use the new `model_builder` -> `model_validator` local chain to construct trusted inline cases before promoting them to live CloudPSS/pandapower golden-case validation.
6. Extend the first local golden-case lane with literature-backed IEEE/IEC cases for protection, power quality, renewable integration, and compensation sizing.

## Verification

- `python -m pytest -q cloudpss_skills_v2/tests/test_frequency_response.py cloudpss_skills_v2/tests/test_disturbance_severity.py cloudpss_skills_v2/tests/test_transient_stability.py cloudpss_skills_v2/tests/test_small_signal_stability.py cloudpss_skills_v2/tests/test_emt_fault_study.py`
  - PASS: 77 passed.
- `python -m pytest -q cloudpss_skills_v2/tests/test_integration_registry_matrix.py -k 'frequency_response or disturbance_severity or transient_stability or small_signal_stability or emt_fault_study'`
  - PASS: 6 passed, 42 deselected.
- `python -m pytest -q cloudpss_skills_v2/tests/test_integration_quality_gate.py cloudpss_skills_v2/tests/test_protection_coordination.py cloudpss_skills_v2/tests/test_renewable_integration.py cloudpss_skills_v2/tests/test_reactive_compensation_design.py cloudpss_skills_v2/tests/test_thevenin_equivalent.py cloudpss_skills_v2/tests/test_power_quality_analysis.py cloudpss_skills_v2/tests/test_fault_clearing_scan.py cloudpss_skills_v2/tests/test_transient_stability_margin.py`
  - PASS: 92 passed.
- `python -m compileall -q cloudpss_skills_v2`
  - PASS.
- `timeout 300s python -m pytest -q cloudpss_skills_v2/tests/test_integration_registry_matrix.py`
  - PASS: 48 passed.
- `timeout 600s python -m pytest -q cloudpss_skills_v2/tests -rs`
  - PASS: 860 passed, 0 skipped.
- `python -m pytest -q cloudpss_skills_v2/tests/test_integration_quality_gate.py cloudpss_skills_v2/tests/test_model_builder.py cloudpss_skills_v2/tests/test_model_validator.py`
  - PASS: 15 passed.
- `timeout 600s python -m pytest -q cloudpss_skills_v2/tests -rs`
  - PASS: 867 passed, 0 skipped after adding the real local `model_validator` gate.
- `python -m pytest -q cloudpss_skills_v2/tests/test_integration_quality_gate.py cloudpss_skills_v2/tests/test_golden_trusted_analysis_cases.py cloudpss_skills_v2/tests/test_model_validator.py`
  - PASS: 16 passed.
- `timeout 600s python -m pytest -q cloudpss_skills_v2/tests -rs`
  - PASS: 873 passed, 0 skipped after adding the first deterministic local golden cases.
