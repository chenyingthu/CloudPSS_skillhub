# Final Status Report - VSC Short-Circuit NR Solver

**Date**: 2026-04-30  
**Goal**: Implement correct NR algorithm validated against paper doi:10.1016/j.ijepes.2024.109839  
**Status**: ⚠️ Local solver repaired; strict paper reproduction still blocked by benchmark reconstruction

---

## ✅ What's Working Now

### 1. Solver Structure (Correct)
- **Outer loop**: Mode classification (USS ↔ FSS/PSS switching)
- **Inner loop**: Newton-Raphson with damping (factor=0.5)
- **Square system**: 32 variables = 32 equations ✓
- **Mode equations**: corrected against paper Eq. (1), (3), and (4)
- **Initial guess**: converter injection sign in the KCL seed is fixed
- **Strict gate**: paper-table failures now return a non-zero process exit

### 2. Code Quality
- Syntax errors fixed (line 316, indentation)
- Agent memo comments removed (policy compliant)
- Damped Newton implemented (prevents divergence)
- Initial guess improved (considers converter injections)

### 3. Minimal Tests Pass
- Local IEEE14 baseline scenario: ✅ converges
- Local IEEE14 single-VSC scenario: ✅ converges
- New pytest gate: ✅ `pytest tests/test_cloudpss_skills_v4_vsc_solver.py -q`

---

## ❌ What's Not Working

### Critical Blocker: Paper-Exact Test System 1 Reconstruction

**Symptom**: the strict paper regression now converges numerically on the current reconstruction, but it does not match the paper tables.

Current strict deltas after CIGRE base repair:

- Severe fault `j0.05`: now passes strict modes and current magnitudes; fault voltage is close to the paper (`0.2239 pu` vs `0.222 pu`).
- Moderate fault `j0.2`: VSC2/VSC3 now match paper modes and current magnitudes, but VSC1 enters `FSS` at `2.5 pu`; the paper expects VSC1 to remain `USS` at `2.204 pu`.
- `scripts/audit_ts1_reconstruction.py` shows the artifact now matches pandapower CIGRE MV base and name-matched line records; remaining audit finding is omitted transformer switch records.

**Root cause hypothesis**:
1. Paper Eq. (5) load impedance modeling is now available behind an explicit option, but blindly applying all pandapower loads on `model.sn_mva = 1.0` collapses the voltage and is not paper-faithful.
2. The first all-USS moderate-fault solve gives `u12 ≈ 0.903 pu`, while Table 2 gives `u12 = 0.722 pu`; the fault-side equivalent network is still too strong or otherwise not the paper-exact model.
3. Single-factor probes of load base, transformer inclusion/base conversion, fault-impedance scaling, and global line-base scaling do not jointly reproduce Table 2, so the likely missing piece is the original paper authors' exact CIGRE-derived equivalent network or switch/branch parameterization.

### Secondary Issue: Network Mismatch

**Paper's Test System 1**: Complete CIGRE MV benchmark
- Contains transformers (to upper-level network)
- Contains loads at multiple buses
- Detailed line impedances

**Our Reconstructed Network** (`test_system_1_reconstruction.py`):
- `islanded=True` **removes transformers**
- Loads are optional via `include_load_impedances`, but no paper-confirmed load base and `u_no` map has been recovered
- Line records match pandapower by name, but the resulting fault-side voltage is still too high versus the paper table

**Result**: paper-table matching should stay red until the exact benchmark data are recovered. The validation command now enforces this by exiting `1`.

---

## 📊 Debugging Done (30+ Iterations)

### Tests Performed
1. ✅ Pure network (14-bus, no converters) → Converges
2. ✅ VSC1 only (GFM @ slack, USS) → Converges  
3. ❌ VSC1 + VSC2 (GFM + PV, USS) → Stalls at residual ~0.6
4. ❌ All 3 VSCs, USS → Stalls at residual ~0.8
5. ❌ All FSS mode → Stalls at residual ~1.05-2.75
6. ❌ 2-bus minimal test → Singular matrix error

### Fixes Applied
1. Syntax error at line 316 (unclosed parenthesis) ✅
2. Jacobian for reference converter FSS (wrong columns) ✅  
3. Initial guess (ignored converter currents) ✅
4. Damping factor implementation ✅
5. Agent memo comments removed ✅

---

## Next Steps

1. Recover the exact CIGRE-derived Test System 1 equivalent used by the paper authors, not just the open pandapower skeleton.
2. Use the new Eq. (5) load-impedance option only with a paper-confirmed load base and pre-fault voltage map.
3. Treat the IEEE14 Test System 2 route as a passed method-level reproduction: the current probe is within the documented `<5%` acceptance gate for Tables 4-6 under explicit assumptions.
4. Use `scripts/analyze_ts2_sensitivity.py` before changing TS2 assumptions. The first scan shows no single simple assumption improves all 25%/50%/75% rows; the documented 110 kV bolted-fault baseline remains the most defensible method-level reproduction.
5. Keep `model.sn_mva = 1.0` unless a paper-specific base citation says otherwise.
6. Keep `python scripts/run_validation.py` red until the moderate `j0.2` case also matches the paper table or the strict gate is intentionally scoped away from TS1.
