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

## Current Blocker: Jacobian Singularity

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

### Step1: Test with Proper Network (Unblock Convergence)
- Run validation with **actual Test System 1 network** (not simple chain)
- Add diagnostic prints to see voltages/currents at start of NR iteration
- If voltages are near zero, need to improve initial guess (maybe use power flow solution as starting point)

### Step2: Re-examine PSS Equations from Paper
- The power-factor equation `P*q_ref - Q*p_ref = 0` is likely wrong
- Paper Table 2: VSC3 PSS has P=-0.572, Q=0.403 → Q/P = -0.703
- Original Q_ref/P_ref = -0.023/-0.8 = 0.0288 → **Completely different!**
- **Need to find paper's exact PSS formulation for GS converter**

### Step3: Fix GFM-FSS Voltage Treatment
- Paper shows VSC1 GFM-FSS has U=0.556∠0° (voltage collapses)
- GFM-FSS should have 2 equations: `|I|² = I_max²` and some constraint on voltage
- Currently, GFM at slack bus has special treatment: only 1 equation (`|I|² = I_max²` or `|U| = u_ref`)
- Need to allow GFM voltage magnitude to vary in FSS

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
| Mode classification | ⚠️ Partial | PV→FSS fixed, GFM logic OK |
| PSS equations | ❌ Wrong | Power-factor equation not paper-faithful |
| FSS equations | ⚠️ Partial | Current limit OK, GFM-FSS incomplete |
| Initial guess | ❌ Broken | Causes singularity for saturated modes |
| Numerical reproduction | ❌ Failed | Convergence fails, no paper agreement |

## Estimated Effort
- Step 1 (warm start): 1-2 hours
- Step 2 (PSS equations): 2-4 hours (may need paper re-reading)
- Step 3 (GFM-FSS): 1-2 hours
- Step 4 (validation): 2-3 hours

**Total remaining**: 6-11 hours of focused debugging.

## Critical Dependencies
1. **Paper Section 2.2-2.4**: Need exact PSS/FSS/GFM equations
2. **Test System 1 network**: Need complete impedance data for blind reproduction
3. **Mode transition logic**: Need to match paper's iterative algorithm

## User Confirmation Needed
Before proceeding with Steps 1-4, please confirm:
1. Should I focus on **warm-start fix** first (to unblock convergence)?
2. Or should I **re-derive all PSS/FSS equations** from paper first?
3. Do you have **clearer paper excerpts** for PSS (GS converter) and GFM-FSS equations?

---
*Report generated: 2026-04-30*
*Next update: After fixing initial guess or obtaining paper equations*
