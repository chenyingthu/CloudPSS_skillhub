# CloudPSS SkillHub V2 - System Design & Integration Test Plan

## 1. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      USER LAYER                                 │
│  Skills (48), CLI, API, Notebook                                │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                   POWERSKILL LAYER                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │  PowerFlow   │  │     EMT      │  │ ShortCircuit │        │
│  │   (API)      │  │    (API)     │  │    (API)     │        │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘        │
│         │                 │                 │                 │
│         └────────────┬────┴────────┬───────┘                 │
│                      ▼                                      │
│              Engine Factory (create_*)                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                    POWERAPI LAYER                              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              EngineAdapter (Abstract)                  │   │
│  │  - connect() / disconnect()                            │   │
│  │  - load_model() / get_components()                     │   │
│  │  - run_simulation() / get_result()                     │   │
│  └─────────────────────┬───────────────────────────────────┘   │
│                       │                                        │
│  ┌────────────────────▼───────────────────────────────────┐   │
│  │       CloudPSSPowerFlowAdapter                        │   │
│  │       CloudPSSShortCircuitAdapter                     │   │
│  │       CloudPSSEMTAdapter                              │   │
│  └─────────────────────┬───────────────────────────────────┘   │
└────────────────────────────┬─────────────────────────────────��──┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                 ENGINE LAYER (CloudPSS SDK)                    │
│  - Model.fetch(model_id, baseUrl=...)                         │
│  - model.runPowerFlow(baseUrl=...)                           │
│  - model.runEMT(baseUrl=...)                                 │
│  - model.fetchTopology(implementType, baseUrl=...)          │
└───────────────────────────────────────────────────────────────┘
```

### Key Components

| Layer | Module | Responsibility |
|-------|--------|-----------------|
| User | `skills/` | 48 skill implementations |
| PowerSkill | `powerskill/` | Engine-agnostic API facade (`PowerFlow`, `EMT`, etc.) |
| PowerAPI | `powerapi/` | Engine adapter (`EngineAdapter` implementations) |
| Engine | `cloudpss` SDK | Native CloudPSS API |

### Data Flow

```
User Input → Skill → PowerFlow.run({model_id}) 
         → Engine.create_powerflow()
         → CloudPSSPowerFlowAdapter.run_simulation()
         → model.runPowerFlow(**kwargs)
         → CloudPSS Server (local/remote)
         → Result parsing → DataLib types → User
```

## 2. Supported Configurations

### Server Endpoints

| Server | URL | Token Required | Notes |
|--------|-----|---------------|-------|
| **CloudPSS.net** | `https://www.cloudpss.net/` | Yes | Production |
| **Local Server** | `http://166.111.60.76:50001` | Yes | Internal testing |
| **Internal** | `https://internal.cloudpss.com` | Yes | Dev environment |

### Engine Adapters

| Adapter | Simulation Type | Status |
|----------|-----------------|--------|
| `CloudPSSPowerFlowAdapter` | Power Flow | ✅ Working |
| `CloudPSSShortCircuitAdapter` | Short Circuit (via EMT) | ✅ Working |
| `CloudPSSEMTAdapter` | EMT Transient | ✅ Working |
| `PandapowerPowerFlowAdapter` | Power Flow | ✅ Working; returns `SimulationResult.system_model` |
| `PandapowerShortCircuitAdapter` | Short Circuit | 🔶 Requires testing |

### Shared ModelHandle Conversion

Config-based poweranalysis skills that need a fallback model conversion use
`powerapi.adapters.convert_handle_to_power_system_model()` instead of keeping
local `_convert_handle_to_model` implementations. The converter currently maps:

| Source component | Unified representation | Notes |
|------------------|------------------------|-------|
| `bus` | `Bus` | Supports `bus:0`, `"0"`, and integer IDs |
| `source` | Slack bus marker | Uses explicit `bus` reference only |
| `branch` | `Branch(branch_type="LINE")` | Uses `args` first, then `properties` |
| `transformer` | `Branch(branch_type="TRANSFORMER")` | Preserves `sn_mva`, tap ratio, and phase shift when provided |
| `load` | `Load` | Requires an explicit resolvable `bus` |
| `generator` | `Generator` | Requires an explicit resolvable `bus` |
| `shunt` | `Load` equivalent | Mapped as negative `q_mvar` at the resolved bus |

The converter is conservative by design: branches and transformers with missing,
unknown, or self-loop endpoints are skipped rather than connected to fabricated
buses. Analysis modules may keep `_convert_handle_to_model` as a compatibility
wrapper, but new conversion behavior should be added in the shared adapter.

### Voltage Stability Analysis Modes

`voltage_stability` supports explicit evidence levels:

| Method | `analysis_mode` | Evidence boundary |
|--------|-----------------|-------------------|
| default / `screening_proxy` | `screening_proxy` | Fast impedance/load voltage-drop screening; not an AC CPF calculation |
| `pandapower_ac` | `pandapower_ac_power_flow_scan` | Repeated pandapower AC `runpp` load-scaling scan; stronger than screening, still not a continuous CPF solver |
| `matpower_cpf` / `cpf` | `matpower_continuation_power_flow` | MATPOWER `runcpf` full AC continuation power-flow path when Octave/MATLAB and the Python MATPOWER bridge are installed |

The `pandapower_ac` mode converts the unified `PowerSystemModel` to a
pandapower network and reads bus voltages from AC power-flow results at each
load-scaling point. It is intended as a validation scan before a dedicated CPF
engine is available, not as an operational voltage-collapse certificate.

The `matpower_cpf` mode converts the unified `PowerSystemModel` to MATPOWER
base and target cases and calls `runcpf`. This runtime is optional and external:
without the Python `matpower` bridge plus Octave/`oct2py` or MATLAB Engine, the
skill returns `analysis_mode: "matpower_cpf_unavailable"` with runtime status
instead of falling back to a screening approximation.

## 3. Integration Test Tiers

### Tier 1: Engine Connectivity

| Test | Description | Expected |
|------|-------------|----------|
| `test_server_connection` | Connect to server | Success |
| `test_token_validation` | Validate token | Valid |
| `test_base_url_handling` | Set custom base URL | Applied |

### Tier 2: Model Operations

| Test | Description | Expected |
|------|-------------|----------|
| `test_load_cloud_model` | Load model by RID | Model object |
| `test_load_local_model` | Load local file | Model object |
| `test_get_components` | List model components | Component list |
| `test_get_components_by_type` | Filter by type | Filtered list |

### Tier 3: Core Simulations

| Test | Description | Expected |
|------|-------------|----------|
| `test_powerflow_ieee39` | Run IEEE39 power flow | 39 buses, 46 branches |
| `test_powerflow_convergence` | Check convergence | converged=True |
| `test_short_circuit` | Run short circuit analysis | Results populated |
| `test_emt_basic` | Run EMT simulation | Plots generated |

### Tier 4: Data Validation

| Test | Description | Expected |
|------|-------------|----------|
| `test_bus_data_mapping` | Verify bus field names | Correct fields |
| `test_branch_data_mapping` | Verify branch fields | Correct fields |
| `test_summary_statistics` | Verify summary stats | Non-zero values |
| `test_datalib_conversion` | Convert to DataLib types | Valid objects |

### Tier 5: Complex Workflows

| Test | Description | Expected |
|------|-------------|----------|
| `test_batch_powerflow` | Multiple models | All succeed |
| `test_n1_analysis` | N-1 contingency | Results for each |
| `test_param_scan` | Parameter sweep | Results vary |
| `test_fault_study` | Fault locations | All locations |

### Tier 6: Edge Cases

| Test | Description | Expected |
|------|-------------|----------|
| `test_invalid_token` | Bad token | Auth error |
| `test_invalid_model` | Invalid RID | Load error |
| `test_timeout_handling` | Long simulation | Timeout error |
| `test_network_error` | Network failure | Retry/error handling |

## 4. Test Configuration

### Environment Variables

```bash
# Required for integration tests
export CLOUDPSS_TOKEN="your_token_here"

# Optional - use local server
export CLOUDPSS_BASE_URL="http://166.111.60.76:50001"

# Test models
export TEST_MODEL_IEEE39="model/chenying/IEEE39"
export TEST_MODEL_IEEE3="model/chenying/IEEE3"
```

### Test Fixtures

```python
@pytest.fixture
def local_server_config():
    return EngineConfig(
        engine_name="cloudpss",
        base_url="http://166.111.60.76:50001",
        extra={"auth": {"token": token}}
    )

@pytest.fixture
def cloud_server_config():
    return EngineConfig(
        engine_name="cloudpss",
        base_url="https://www.cloudpss.net/",
        extra={"auth": {"token": token}}
    )
```

## 5. Known Issues & Mitigations

| Issue | Root Cause | Workaround | Status |
|-------|-----------|------------|--------|
| `baseUrl` not passed to SDK | Missing `**kwargs` | Pass to `run*`, `fetch*` calls | ✅ Fixed |
| List-wrapped table response | SDK format difference | Unwrap list before parsing | ✅ Fixed |
| Summary nested format | Adapter output mismatch | Use flat format | ✅ Fixed |
| PowerFlow model loading 401 | `CloudPSSAdapter` created without token in `_do_connect` | Recreate adapter with token in `_do_connect` | ✅ Fixed |
| Component classifier missing BUS | `_classify_component` only returns BRANCH/TRANSFORMER/GENERATOR/LOAD/OTHER | Use classified types like "load", not "bus" | ⚠️ Design |
| SkillResult field naming | `started_at` vs `start_time` in different layers | Added property aliases for consistency | ✅ Fixed |
| AnalysisBase confusion | Two AnalysisBase classes in different modules | Renamed to `PowerAnalysisBase` with backward compat alias | ✅ Fixed |

## 6. Running Tests

### Full Integration Suite

```bash
# Using local server
pytest cloudpss_skills_v2/tests/test_integration_cloudpss.py \
    --base-url=http://166.111.60.76:50001 \
    -v

# Using cloud server
pytest cloudpss_skills_v2/tests/test_integration_cloudpss.py \
    --base-url=https://www.cloudpss.net/ \
    -v

# Specific tier
pytest cloudpss_skills_v2/tests/ -k "test_tier3" -v
```

### Quick Smoke Test

```bash
# Core simulations only
pytest cloudpss_skills_v2/tests/test_integration_powerskill.py -v
```

## 7. Coverage Targets

| Tier | Current | Target |
|------|---------|--------|
| Tier 1-3 | 100% | 100% |
| Tier 4 | 100% | 95% |
| Tier 5 | 50% | 80% |
| Tier 6 | 100% | 50% |

## 8. Test Results (2026-04-25)

All 18 integration tests now pass with local server (`http://166.111.60.76:50001`):

| Tier | Tests | Passed | Failed | Notes |
|------|-------|--------|--------|-------|
| Tier 1: Connectivity | 3 | 3 | 0 | Server connection, token, base_url |
| Tier 2: Model Ops | 3 | 3 | 0 | Load model, components, type filter |
| Tier 3: Simulations | 4 | 4 | 0 | PowerFlow, ShortCircuit, EMT |
| Tier 4: Data Validation | 4 | 4 | 0 | Bus/Branch mapping, summary, datalib |
| Tier 5: Complex Workflows | 2 | 2 | 0 | Model modification, result caching |
| Tier 6: Edge Cases | 2 | 2 | 0 | Invalid model, timeout |

**Total: 18 passed, 0 failed** in ~81 seconds.

### Key Bugs Fixed During Testing

1. **PowerFlow adapter token not passed** (`powerflow.py:_do_connect`): The `CloudPSSAdapter` was created without a token in `__init__`, and `_do_connect` only called `connect()` without passing the token. Fixed by setting `self._cloud_pss_adapter.token = token` in `_do_connect`.

2. **Component type "bus" returns empty**: `_classify_component` doesn't classify any type as "bus". Test updated to use "load" instead.

3. **Test fixture `components` undefined**: `test_model_modification` referenced undefined `components` variable. Fixed by fetching components first.

---

---

## 9. Migration Guide (V1 → V2)

### 9.1 SkillResult Field Naming

**Before (V1)**:
```python
# Inconsistent naming between layers
simulation_result.started_at  # PowerAPI layer
skill_result.start_time       # PowerSkill layer
```

**After (V2)**:
```python
# Consistent naming with aliases
simulation_result.start_time  # Alias for started_at
skill_result.started_at       # Alias for start_time
```

Both names work in both classes for backward compatibility.

### 9.2 AnalysisBase Renaming

**Before (V1)**:
```python
from cloudpss_skills_v2.poweranalysis.base import AnalysisBase
# Could be confused with cloudpss_skills_v2.base.AnalysisBase
```

**After (V2)**:
```python
from cloudpss_skills_v2.poweranalysis.base import PowerAnalysisBase
# Recommended: use PowerAnalysisBase for clarity
# AnalysisBase still works as alias for backward compatibility
```

### 9.3 Conversion Methods

```python
from cloudpss_skills_v2.core.skill_result import SkillResult
from cloudpss_skills_v2.powerapi.base import SimulationResult

# Convert SimulationResult to SkillResult format
sim_result = SimulationResult(...)
skill_dict = sim_result.to_skill_result_dict()

# Convert SkillResult to SimulationResult format
skill_result = SkillResult(...)
sim_dict = skill_result.to_simulation_result_dict()
```

---

*Document Version: 1.2*
*Last Updated: 2026-04-30*
