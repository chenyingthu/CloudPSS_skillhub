# Validation Scope

This package currently validates two things:

- the local standalone solver runs on an IEEE 14-bus admittance model without external tooling
- the solver exposes the paper-faithful two-level structure of an outer mode loop and an inner Newton-Raphson solve
- the package preserves paper-native scenario targets that were recovered from the paper text
- the package surfaces an explicit missing-parameter inventory for unreconstructed benchmark data
- the package exposes a first explicit Test System 1 reconstruction artifact and its benchmark carry-over assumptions

# Expected Runner Behavior

Running `python scripts/run_validation.py` should produce JSON containing:

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

# Non-Claims

This package does not currently claim:

- exact numerical agreement with the paper's published result tables
- complete reconstruction of all paper test-system parameters
- a complete machine-readable extraction of every paper mode-switching rule or appendix table
