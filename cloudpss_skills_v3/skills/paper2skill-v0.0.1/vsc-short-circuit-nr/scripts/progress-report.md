# Progress Report - Test System 1 Numerical Reproduction

## Goal
Deliver a v3 cloudpss-skills package implementing paper doi:10.1016/j.ijepes.2024.109839 with outer saturation-state loop and inner Jacobian-based NR, achieving paper-faithful numerical reproduction for Test System 1/2.

## Completed Work

### 1. Structure Implementation ✓
- Built v3 skill package: `cloudpss_skills_v3/skills/paper2skill-v0.0.1/vsc-short-circuit-nr/`
- Implemented `PaperFaithfulShortCircuitSolver` with outer mode loop + inner NR
- Embedded paper validation targets (Table 2/3/10) in `scenarios.py`
- Reconstructed Test System 1 network artifact (`test_system_1_network.json`)
- Added converter-specific metadata: VSC1→GFM, VSC2→PV, VSC3→GS

### 2. Bug Fixes ✓
- Fixed Jacobian singularity from dead code (line 449)
- Fixed FSS residual: removed incorrect `|V|^2` multiplication
- Fixed PSS Jacobian: corrected `p_ref` sign errors
- Fixed FSS Jacobian: current-limit row should have zero voltage derivatives
- Updated mode classification: PV→FSS when saturated (not stuck in USS)

### 3. Professional Research ✓
- Researched GFM, USS, PSS, FSS principles via 3 librarian + 2 oracle sessions
- Understood PSS = active-power-priority saturation
- Understood FSS = reactive/fault-support priority saturation

## Current Status After 2026-04-30 Repair Pass

### What moved
- Re-read the local paper PDF with `pdftotext` and corrected the mode equations against Section 2.1:
  - PQ/GS PSS now regulates `|I|` and `Q`, not active power.
  - PV PSS regulates `|I|` and voltage magnitude.
  - PQ/PV/GS FSS now regulates `|I|` and `P=0`.
  - GFM FSS now regulates `|I|` and voltage angle.
- Fixed the initial-voltage KCL sign for converter current injections.
- Added a `verbose` flag so the solver no longer floods validation output by default.
- Converted the Test System 1 paper-table comparison from a print-only check into a strict, machine-readable regression gate.
- Added `tests/test_cloudpss_skills_v3_vsc_solver.py` to lock the local convergent validation case and the current strict red paper-reproduction state.

### Verification evidence
- `python3 -m py_compile ...` passed for the v3 solver, validation runner, reconstruction helper, and new pytest file.
- `pytest tests/test_cloudpss_skills_v3_vsc_solver.py -q` passed: `2 passed`.
- `python3 cloudpss_skills_v3/skills/paper2skill-v0.0.1/vsc-short-circuit-nr/scripts/run_validation.py` now exits with code `1`, as intended, because strict Test System 1 reproduction still fails.

### Current strict-regression deltas
- Moderate fault `j0.2`: solver converges, but VSC3 is `FSS` instead of paper `PSS`; VSC1 current is `0.5991 pu` vs paper `2.204 pu`.
- Severe fault `j0.05`: solver converges, but VSC1 remains `USS` instead of paper `FSS`; VSC1 current is `1.0720 pu` vs paper `2.5 pu`.
- VSC2/VSC3 current limits do hit `1.0 pu` in the converged strict cases, so the current-limit equations are no longer the primary blocker.

### Current blocker
The remaining blocker is paper-exact benchmark reconstruction, not generic NR execution. The recovered CIGRE skeleton, `test_system_1_network_corrected.json`, and `test_system_1_network_v3.json` were probed and all miss the paper tables by large margins. The next productive work is to recover or infer the exact Test System 1 network/base data used in the paper, including topology/switch semantics, load-as-impedance treatment, transformer/external-grid handling, and per-unit base mapping.

## Superseded Blocker: Jacobian Singularity

### Problem
Even after fixing equation bugs, NR solver fails with "Singular matrix" at iteration 1.

### Root Cause (Discovered via Diagnostics)
**Initial guess sets current I=0 for saturated converters.**

When converter is in FSS/PSS mode:
- Residual equation: `|I|^2 - I_max^2 = 0`
- Jacobian row: `d/dI_r = 2*I_r, d/dI_i = 2*I_i`
- **When I=0: ENTIRE ROW = 0 → Jacobian rank deficient**

Diagnostic output:
```
[DIAG] Singular matrix at iteration 1, modes=['FSS']
[DIAG] Jacobian shape=(30, 30), rank=28
[DIAG] Near-zero rows: [28 29]...
    Row 28: [0. 0. 0. 0.]...  (current-limit row)
    Row 29: [0. 0. 0. 0.]...  (second equation row)
```

### Why This Happens
1. `_initial_guess()` computes current from `I = conj(P_ref / V)` → for PV converter with `p_ref=-0.794`, if voltage is low (faulted), current could be large
2. But when mode switches from USS→FSS in outer loop, solver restarts from fresh initial guess
3. Fresh guess uses `p_ref=0.0` for FSS (since P=0 in FSS), resulting in I=0
4. **Even if we fix the guess, the first NR iteration will have I≈0, causing singularity**

## Paper Behavior vs Our Implementation

### Paper Table 2 (Moderate Fault, j0.2)
| Iteration | VSC1 | VSC2 | VSC3 | i_vsc2 | i_vsc3 |
|-----------|------|------|------|--------|--------|
| 1 | USS | USS | USS | 2.73 | 1.231 |
| 2 | USS | **FSS** | **PSS** | 1.0 | 1.0 |

### Paper Table 3 (Severe Fault, j0.05)
| Iteration | VSC1 | VSC2 | VSC3 | i_vsc1 | i_vsc2 | i_vsc3 |
|-----------|------|------|------|--------|--------|--------|
| 1 | USS | USS | USS | 4.507 | 6.254 | 2.294 |
| 2 | **FSS** | **FSS** | **FSS** | 2.5 | 1.0 | 1.0 |

### Key Observations
1. **VSC2 in FSS has P=0.0** (not P_ref=-0.794) → Confirms PV gives up active power
2. **VSC3 in PSS has P=-0.572** (not P_ref=-0.8) → Power factor changes
3. **VSC1 GFM in FSS has U=0.556∠0°** (not 1.0∠0°) → Voltage collapses

## Remaining Critical Issues

### 1. Initial Guess for Saturated Modes
**Problem**: When switching USS→FSS/PSS, must project previous solution onto limit surface.

**Solution** (from Oracle):
```python
def _warm_start_state(self, previous_state, previous_modes, new_modes, layout):
    # Keep voltages from previous solution
    # Project current onto limit circle: I_new = I_max * exp(j * angle(I_old))
    # For FSS: ensure P=0 by rotating current to align with voltage
    ...
```

### 2. PSS Second Equation Uncertainty
**Problem**: Paper doesn't explicitly give PSS equation for GS converter.

**Current implementation**: `P*q_ref - Q*p_ref = 0` (maintain power factor)
**Paper Table 2**: VSC3 PSS has P=-0.572, Q=0.403, which gives Q/P = -0.703
**Original**: q_ref/p_ref = -0.023/(-0.8) = 0.0288 → **Completely different!**

**Conclusion**: My PSS power-factor equation is NOT paper-faithful.

### 3. GFM-FSS Treatment
**Problem**: Paper shows VSC1 GFM-FSS has U=0.556∠0° (voltage collapses), but I still treat it as slack with fixed angle.

**Missing**: GFM-FSS should have 2 equations:
1. `|I|^2 = I_max^2`
2. Some constraint on voltage (paper shows magnitude collapses, angle stays at 0°)

## Root Cause Found (After 2+ Hours Debugging)

### Why Jacobian is Still Singular
**The test network was poorly constructed**, not the solver equations.

In my test with a simple 14-bus chain network:
- Added fault at bus 11: `ybus[11,11] += 1/(0.2j)`
- Initial guess gave **V[5] = 0j** (magnitude=0.0000)
- Because voltage is zero, current = conj(P_ref/V) → handled as 0j
- Current = 0 → Jacobian rows for converter become all zeros
- **This is NOT a bug in the solver equations!**

### Proper Test System 1 Network
The actual Test System 1 reconstruction (`test_system_1_reconstruction.py`) should have proper voltages.
The validation run with Test System 1 also gave singular matrix, but that might be due to:
1. Initial guess currents are huge (P_ref/V where V is low due to fault)
2. When mode switches to FSS/PSS, the current projection might not work correctly
3. The real network might have voltage collapse at converter buses

## Verified Fixes (Code Level)
1. ✅ FSS residual: removed incorrect `|V|²` multiplication
2. ✅ FSS Jacobian: current-limit row has zero voltage derivatives, 2*I_r and 2*I_i for current derivatives
3. ✅ PSS Jacobian: fixed p_ref sign errors in power-factor equation
4. ✅ Mode classification: PV converter now correctly switches to FSS (not stuck in USS)
5. ✅ Initial guess: attempts to project saturated converters onto limit circle

## Still Failing
- Solver still fails with "Singular matrix" for both simple and real networks
- The root cause in simple network is **zero voltage at converter bus** (test artifact)
- The root cause in real network is **unknown** (maybe similar, or maybe equations still wrong for PSS/GFM-FSS)

## Next Steps (Priority Order)

### Step1: Recover paper-exact Test System 1 data
- Confirm whether the benchmark is the open pandapower CIGRE MV network unchanged or a modified CIGRE-derived case.
- Confirm switch semantics from the paper Figure 1 before applying switch pruning in code.
- Add load impedances from pre-fault load data if the paper uses the equivalent-load model from Eq. (5).
- Confirm per-unit base values for the islanded system and VSC current bases.

### Step2: Keep strict regression red until paper agreement is real
- Do not mark `run_validation.py` successful while `strict_paper_regression.passed` is false.
- Use `evaluate_test_system_1_regression(verbose=False)` for programmatic checks.
- Only flip the red test after converter modes and currents match the paper tables within tolerance.

### Step3: Extend strict data coverage
- Once Test System 1 is resolved, add strict checks for Test System 2 fault-current tables at 25%, 50%, and 75% penetration.
- Keep source-backed targets in `scenarios.py`; do not rely on mock-only claims.

### Step4: Implement Warm-Start Properly
- When outer loop switches modes, reuse previous solution
- Project currents onto limit circle: `I_new = I_max * exp(j * angle(I_old))`
- Adjust for mode-specific second equation

### Step5: Test System 1 Validation
- After Steps 1-4, run full regression
- Compare iteration-by-iteration with paper Tables 2/3
- Aim for numerical agreement, not just structural correctness

## Verification Status

| Component | Status | Notes |
|-----------|--------|-------|
| Package structure | ✅ Complete | v3 format, SKILL.md, scripts/ |
| Test System 1 network | ⚠️ Partial | CIGRE MV skeleton, missing impedances |
| Paper targets embedded | ✅ Complete | Table 2/3/10 in scenarios.py |
| Solver structure | ✅ Complete | Outer loop + inner NR |
| Mode classification | ⚠️ Partial | Runs, but cannot be fully validated before paper-exact network recovery |
| PSS equations | ✅ Repaired | Aligned to paper Eq. (1)/(3): current plus Q or U |
| FSS equations | ✅ Repaired | Aligned to paper Eq. (1)/(3)/(4): current plus P=0 or theta |
| Initial guess | ✅ Repaired | Converter-current KCL sign fixed; local validation converges |
| Numerical reproduction | ❌ Failed | Convergence fails, no paper agreement |
| Strict validation exit code | ✅ Repaired | `run_validation.py` exits `1` while strict paper reproduction is false |

---
*Updated: 2026-04-30*
*Next update: after recovering paper-exact Test System 1 network/base data*
