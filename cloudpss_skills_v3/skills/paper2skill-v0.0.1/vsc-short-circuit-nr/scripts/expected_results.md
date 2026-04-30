# Validation Scope

This package currently validates two things:

- the local standalone solver runs on an IEEE 14-bus admittance model without external tooling
- the solver exposes the paper-faithful two-level structure of an outer mode loop and an inner Newton-Raphson solve
- the package preserves paper-native scenario targets that were recovered from the paper text
- the package surfaces an explicit missing-parameter inventory for unreconstructed benchmark data
- the package exposes a first explicit Test System 1 reconstruction artifact and its benchmark carry-over assumptions

# Expected Runner Behavior

Running `python scripts/run_validation.py` now has two layers:

1. It prints the standalone package validation JSON.
2. It runs a strict Test System 1 regression against the paper tables.

The command must return a non-zero exit code while strict paper reproduction remains unresolved. This is intentional: previous versions printed `SOME FAILURES` while still exiting successfully, which allowed false-green handoffs between agents.

The first JSON report should contain:

- `paper_targets.test_system_1` with bus 12 and fault impedances `j0.2 pu` and `j0.05 pu`
- `paper_targets.test_system_2` with 8 VSCs and penetration levels `0.25`, `0.5`, `0.75`
- `missing_reproduction_parameters` grouped by test system
- `test_system_1_reconstruction` with artifact summary, bus index mapping, and direct solver readiness metadata
- a converged `baseline_case`
- a converged `vsc_case` for the local validation scenario
- `outer_iterations` and `inner_iterations`
- `mode_history` for the VSC case
- a difference between baseline and VSC fault current magnitude
- an explicit `limitations` list

The strict regression output should contain `strict_paper_regression` with:

- `passed: false` until paper-exact Test System 1 network/base data are recovered
- one case record for `moderate_fault`
- one case record for `severe_fault`
- per-converter mode checks and current-magnitude checks
- the blocking reason: paper-exact Test System 1 network/base data are not yet reconstructed well enough for numerical reproduction

Current expected strict status:

- local IEEE14 validation: pass
- Test System 1 numerical reproduction: fail
- `python scripts/run_validation.py`: exit code `1`

Current TS1 reconstruction audit:

- `python scripts/audit_ts1_reconstruction.py` should report `model.sn_mva = 1.0`, matching `pandapower.networks.create_cigre_network_mv(with_der=False)`.
- Name-matched line records should have no mismatch against the pandapower CIGRE MV reference.
- The remaining expected audit finding is the omitted transformer switch records; this is bookkeeping until transformer/islanded semantics are added.
- The severe `j0.05` strict case currently passes modes and current magnitudes; the moderate `j0.2` case remains red because VSC1 enters FSS early.
- Eq. (5) load impedance conversion is available as an explicit reconstruction option, but remains off by default because the paper-confirmed load base and pre-fault `u_no` map are still missing.

Current TS2 method-level reproduction:

- `test_system_2_probe` should be present in `python scripts/run_validation.py` output.
- It should use Figure 4 VSC buses `[2, 3, 6, 8, 10, 12, 13, 14]` and fault bus `11`.
- It should converge for the `25%`, `50%`, and `75%` capacity cases.
- It should return `passed: true` because all three table-current errors are below the documented `5%` method-level acceptance threshold.
- It should still include `strict_reproduction_gap` because VSC transformer impedances and the paper's PowerFactory kA voltage-base convention remain unrecovered.
- `python scripts/analyze_ts2_sensitivity.py` should complete a compact screening scan. The current expected baseline is `1.7316 / 1.7505 / 1.7245 kA` versus paper `1.706 / 1.820 / 1.761 kA`, with mean error about `2.46%`.
- The sensitivity scan is diagnostic only. It supports the current method-level acceptance boundary, but must not be used to bless a PowerFactory-strict pass unless a source-backed PowerFactory/IEEE14 modeling convention explains the selected assumptions.

# Non-Claims

This package does not currently claim:

- exact numerical agreement with the paper's published result tables
- complete reconstruction of all paper test-system parameters
- a complete machine-readable extraction of every paper mode-switching rule or appendix table
- PowerFactory-strict reproduction of Test System 2 transformer and voltage-base implementation details
