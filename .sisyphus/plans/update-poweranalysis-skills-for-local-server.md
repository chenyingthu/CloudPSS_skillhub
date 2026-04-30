# Plan: Update PowerAnalysis Skills to Use `create_*_for_skill()` Factory Methods

## Goal

Update all poweranalysis skills that use `Engine.create_powerflow()` (and similar) to use the new `*_for_skill()` factory methods so they properly route API calls through `base_url` from config. Skip skills that use `engine="pandapower"` (those don't need local server support).

## Background

The `Engine` class now has `*_for_skill()` factory methods that accept `base_url` and `auth` directly:
- `create_powerflow_for_skill(engine, base_url, auth)`
- `create_short_circuit_for_skill(engine, base_url, auth)`
- `create_emt_for_skill(engine, base_url, auth)`

The auth config is passed to each skill via `config.get("auth", {})`. The `base_url` is extracted from `auth.get("base_url")` which points to the internal test server.

## Files to Update

### Inline pattern (try block, direct call):
- [ ] `poweranalysis/batch_powerflow.py` — line 179: `create_powerflow(engine=engine)` → `create_powerflow_for_skill(engine=engine, base_url=auth.get("base_url"), auth=auth)`
- [ ] `poweranalysis/fault_clearing_scan.py` — line 125
- [ ] `poweranalysis/transient_stability.py` — line 112
- [ ] `poweranalysis/frequency_response.py` — line 127
- [ ] `poweranalysis/disturbance_severity.py` — line 166
- [ ] `poweranalysis/power_quality_analysis.py` — line 124
- [ ] `poweranalysis/maintenance_security.py` — line 123
- [ ] `poweranalysis/n2_security.py` — line 108
- [ ] `poweranalysis/thevenin_equivalent.py` — line 116

### _get_api() helper pattern:
- [ ] `poweranalysis/loss_analysis.py` — line 186: `Engine.create_powerflow(engine=engine)` → `Engine.create_powerflow_for_skill(engine=engine, base_url=auth.get("base_url"), auth=auth)` with auth extracted from config first
- [ ] `poweranalysis/short_circuit.py` — line 185: `Engine.create_short_circuit(engine=engine)` → `Engine.create_short_circuit_for_skill(engine=engine, base_url=auth.get("base_url"), auth=auth)`
- [ ] `poweranalysis/base.py` — line 92: `Engine.create_powerflow(engine=engine)` → same pattern

### Dual API (create_powerflow + create_emt):
- [ ] `poweranalysis/emt_n1_screening.py` — lines 150-151: both `create_powerflow` and `create_emt`

### Pandapower (SKIP — no local server needed):
- `poweranalysis/param_scan.py` — engine="pandapower"
- `poweranalysis/small_signal_stability.py` — engine="pandapower"
- `poweranalysis/renewable_integration.py` — engine="pandapower"
- `poweranalysis/vsi_weak_bus.py` — engine="pandapower"
- `poweranalysis/protection_coordination.py` — engine="pandapower"
- `poweranalysis/parameter_sensitivity.py` — engine="pandapower"
- `poweranalysis/dudv_curve.py` — engine="pandapower"

## Change Pattern

### Inline pattern (try block):
```python
# BEFORE (inside try block):
engine = config.get("engine", "cloudpss")
api = Engine.create_powerflow(engine=engine)

# AFTER:
engine = config.get("engine", "cloudpss")
auth = config.get("auth", {})
api = Engine.create_powerflow_for_skill(
    engine=engine,
    base_url=auth.get("base_url"),
    auth=auth,
)
```

### _get_api() helper pattern:
```python
# BEFORE:
def _get_api(self, config: dict[str, Any]) -> PowerFlow:
    engine = config.get("engine", "cloudpss")
    return Engine.create_powerflow(engine=engine)

# AFTER:
def _get_api(self, config: dict[str, Any]) -> PowerFlow:
    engine = config.get("engine", "cloudpss")
    auth = config.get("auth", {})
    return Engine.create_powerflow_for_skill(
        engine=engine,
        base_url=auth.get("base_url"),
        auth=auth,
    )
```

### Dual API pattern:
```python
# BEFORE:
engine = config.get("engine", "cloudpss")
pf_api = Engine.create_powerflow(engine=engine)
emt_api = Engine.create_emt(engine=engine)

# AFTER:
engine = config.get("engine", "cloudpss")
auth = config.get("auth", {})
pf_api = Engine.create_powerflow_for_skill(
    engine=engine,
    base_url=auth.get("base_url"),
    auth=auth,
)
emt_api = Engine.create_emt_for_skill(
    engine=engine,
    base_url=auth.get("base_url"),
    auth=auth,
)
```

## Non-Goals

- Do NOT modify pandapower engine skills
- Do NOT change any logic beyond the factory method call
- Do NOT remove the `engine` parameter — it still matters for engine selection