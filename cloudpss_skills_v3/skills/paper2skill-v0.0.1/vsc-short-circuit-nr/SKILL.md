---
name: vsc-short-circuit-nr
title: "A short-circuit calculation solver for power systems with power electronics converters"
version: 0.0.1
engine: paper2skill-v0.0.1
license: MIT
url: "https://doi.org/10.1016/j.ijepes.2024.109839"
keywords: [Short-Circuit, VSC, Newton-Raphson, Current Saturation, Power Electronics]
description: "Standalone paper-oriented short-circuit skill package for VSC-rich systems, now upgraded to an outer saturation-state loop plus inner Newton-Raphson solve, with explicit limits around paper-table reproduction."
---

# vsc-short-circuit-nr

This skill packages a standalone short-circuit workflow for systems with voltage source converters and current saturation. It is derived from the paper’s problem structure and preserves the paper-native validation scenarios that were recoverable in the current environment, while keeping a strict boundary between what the paper proves and what the local implementation currently reproduces.

The underlying paper solves a piecewise nonlinear short-circuit equilibrium problem with an inner Jacobian-based Newton-Raphson solve and an outer saturation-state update loop. The packaged code now follows that two-level structure in a standalone form, while still avoiding any false claim of full numerical reproduction of the paper’s published tables.

## Core Concept

The paper’s key idea is that short-circuit calculation in VSC-rich systems depends on converter operating state, not just passive network impedance. A faithful formulation must track whether each converter remains unsaturated or switches into a current-limited mode such as PSS or FSS, because that changes the algebraic constraints imposed at the converter bus.

This package therefore combines three deliverables: a local solver implementation, paper-derived regression targets that can be replayed without external tooling, and an executable validation runner that states exactly what is and is not verified.

## Architecture Overview

- **Local solver module**: `scripts/vsc_nr_solver.py` now implements an outer converter-mode update loop wrapped around an inner Newton-Raphson residual and Jacobian solve.
- **Scenario definitions**: `scripts/scenarios.py` stores the recoverable paper-native validation targets, regression-grade table values, missing-parameter inventory, and the local IEEE 14-bus admittance builder.
- **Validation runner**: `scripts/run_validation.py` executes baseline and VSC-enabled cases and prints a machine-readable report.
- **Validation contract**: `scripts/expected_results.md` defines what the runner output should contain and which claims remain intentionally out of scope.
- **Benchmark reconstruction artifact**: `scripts/test_system_1_network.json` stores the first explicit Test System 1 skeleton, separating benchmark carry-over from paper-exact converter and fault data.

## Implementation

```text
scripts/
├── expected_results.md
├── run_validation.py
├── scenarios.py
├── test_system_1_network.json
├── test_system_1_reconstruction.py
└── vsc_nr_solver.py
```

Run the packaged validation flow with:

```bash
python scripts/run_validation.py
```

The current package runner verifies that the local solver executes on a standalone IEEE 14-bus admittance model, that converter saturation states are surfaced in the result, and that the paper-derived scenario targets plus missing-parameter inventory remain attached to the skill package.

## Validation

The paper-native scenario targets currently preserved in this package are:

- **Test System 1**: CIGRE European MV based system, fault at bus 12, with fault impedances `j0.2 pu` and `j0.05 pu`, a reported valid state resolution of `VSC1 = USS`, `VSC2 = FSS`, `VSC3 = PSS`, and iteration-by-iteration table values for voltages, converter currents, and feasibility.
- **Test System 2**: IEEE 14-bus based system with 8 VSCs connected through transformers, tested at penetration levels `25%`, `50%`, and `75%`, including explicit short-circuit current comparison tables at each penetration level.

The current environment did yield a substantial set of paper-native tables and appendix values, and those are now embedded in the package. What remains incomplete is the benchmark network definition needed to drive blind end-to-end reproduction from inputs alone, so the validation runner is still an execution and traceability artifact rather than a final regression proof against the paper.

The package now also includes a first explicit **Test System 1 reconstruction artifact** based on the open CIGRE MV benchmark skeleton, with paper-specific converter/fault targets attached and benchmark carry-over assumptions called out in metadata.

## Practical Guidance

### When to use

- Use this package when you need a standalone short-circuit skill artifact derived from a paper and want the local implementation, scenario targets, and runnable validation flow kept together.
- Use it when converter saturation mode changes are part of the study and a plain passive-fault model is not enough.
- Use it as a standalone implementation of the paper’s two-level solver structure when you need explicit mode histories, current-limited branches, and a runnable local validation path.

### Limitations

- The packaged solver now follows the paper’s outer-loop plus inner-NR structure, but some mode-switching details are still derived from recoverable paper structure plus local assumptions rather than a complete machine-readable extraction of every paper equation.
- Exact network reconstruction data for the paper benchmarks is still incomplete even though many target tables are now embedded.
- This package should not be described as fully numerically validated against the paper until those embedded targets are paired with a reconstructed benchmark model and checked directly.
- The new `test_system_1_network.json` artifact is a reconstruction starting point, not yet a paper-certified executable model.

### Parameters

| Parameter | Description | Recommended value |
|-----------|-------------|-------------------|
| `fault_impedance` | Per-unit fault impedance used in the local runner | `0.01` for local replay, `j0.2` and `j0.05` as paper targets |
| `i_max` | Converter current limit in per unit | scenario dependent |
| `tolerance` | Inner Newton-Raphson convergence threshold | `1e-8` |
| `max_iter` | Maximum inner Newton-Raphson iterations | `30` |
| `max_outer_iter` | Maximum saturation-state update iterations | `12` |
| `saturation_preference` | Preferred limiting branch when saturation is detected | `PSS` or `FSS` |

### Output files

- `scripts/run_validation.py` prints the current package validation report.
- `scripts/expected_results.md` defines the expected report shape and its non-claims.
- `scripts/scenarios.py` stores the paper-derived scenario targets, extracted regression tables, and the missing-parameter inventory for unresolved benchmark inputs.
- `scripts/test_system_1_network.json` captures the current Test System 1 reconstruction skeleton and benchmark carry-over notes.

## Reference

- Paper: *A short-circuit calculation solver for power systems with power electronics converters*
- DOI: https://doi.org/10.1016/j.ijepes.2024.109839
- Authors: Jie Song, Josep Fanals-Batllori, Leonardo Marín, et al.
- Validation context recovered from the paper: CIGRE European MV based test system and an IEEE 14-bus based system with 8 VSCs
