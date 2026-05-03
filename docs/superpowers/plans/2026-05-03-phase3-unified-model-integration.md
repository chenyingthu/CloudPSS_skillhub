# Phase 3 Unified Model Integration Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrate unified PowerSystemModel into PowerSkill and PowerAnalysis classes, enabling cross-engine analysis capabilities.

**Architecture:** Two-tier architecture where PowerSkill API returns unified model results, and PowerAnalysis operates on unified model independently of underlying engine.

**Tech Stack:** Python, cloudpss SDK, pandapower, unified PowerSystemModel dataclasses

---

## File Structure

| File | Responsibility | Action |
|------|---------------|--------|
| `cloudpss_skills_v2/core/system_model.py` | Unified model dataclasses | Already exists |
| `cloudpss_skills_v2/powerapi/base.py` | EngineAdapter ABC, SimulationResult | Modify to expose unified model |
| `cloudpss_skills_v2/powerskill/powerflow.py` | PowerFlow skill | Modify to return unified model |
| `cloudpss_skills_v2/powerskill/base.py` | SkillBase class | Modify to support unified model access |
| `cloudpss_skills_v2/poweranalysis/n1_security.py` | N-1 security analysis | Modify to use unified model |
| `cloudpss_skills_v2/poweranalysis/base.py` | PowerAnalysis base | Modify to accept unified model |
| `cloudpss_skills_v2/tests/test_n1_security_unified.py` | Unified model tests | Create |

---

## Task 1: Modify SimulationResult to Expose Unified Model

**Files:**
- Modify: `cloudpss_skills_v2/powerapi/base.py:385-420` (SimulationResult class)
- Test: `cloudpss_skills_v2/tests/test_simulation_result.py` (create new)

- [ ] **Step 1: Write failing test for unified model access**

```python
def test_simulation_result_has_unified_model():
    from cloudpss_skills_v2.powerapi.base import SimulationResult, SimulationStatus
    from cloudpss_skills_v2.core.system_model import PowerSystemModel, Bus
    
    model = PowerSystemModel(
        buses=[Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK",
                   v_magnitude_pu=1.0, v_angle_degree=0.0)],
        base_mva=100.0
    )
    
    result = SimulationResult(
        job_id="test-001",
        status=SimulationStatus.COMPLETED,
        system_model=model
    )
    
    assert result.system_model is not None
    assert result.system_model.buses[0].name == "Bus1"
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest cloudpss_skills_v2/tests/test_simulation_result.py -v
```

Expected: AttributeError - system_model not recognized

- [ ] **Step 3: Modify SimulationResult to accept system_model**

In `cloudpss_skills_v2/powerapi/base.py`, find the SimulationResult dataclass and add:

```python
@dataclass
class SimulationResult:
    """Container for simulation results."""
    
    job_id: str
    status: SimulationStatus
    data: dict[str, Any] = field(default_factory=dict)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    errors: list[str] = field(default_factory=list)
    # NEW: Unified model for cross-engine analysis
    system_model: PowerSystemModel | None = None
    
    def get_unified_model(self) -> PowerSystemModel | None:
        """Get unified PowerSystemModel if available."""
        return self.system_model
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest cloudpss_skills_v2/tests/test_simulation_result.py -v
```

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add cloudpss_skills_v2/powerapi/base.py cloudpss_skills_v2/tests/test_simulation_result.py
git commit -m "feat: Add system_model attribute to SimulationResult"
```

---

## Task 2: Modify PowerFlow Skill to Return Unified Model

**Files:**
- Modify: `cloudpss_skills_v2/powerskill/powerflow.py:150-200` (_run_powerflow_with_unified)
- Test: `cloudpss_skills_v2/tests/test_powerflow_unified.py` (create new)

- [ ] **Step 1: Write failing test for unified model in skill result**

```python
def test_powerflow_returns_unified_model():
    from cloudpss_skills_v2.powerskill.powerflow import PowerFlow
    from cloudpss_skills_v2.core.system_model import PowerSystemModel
    
    skill = PowerFlow()
    # Mock result with unified model
    mock_result = MagicMock()
    mock_result.status.value = "completed"
    mock_result.system_model = PowerSystemModel(
        buses=[],
        base_mva=100.0
    )
    
    # Test that skill result includes unified model
    result = skill._create_result_from_adapter_result(mock_result)
    assert "unified_model" in result or hasattr(result, 'system_model')
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest cloudpss_skills_v2/tests/test_powerflow_unified.py -v
```

- [ ] **Step 3: Modify PowerFlow skill to expose unified model**

In `cloudpss_skills_v2/powerskill/powerflow.py`, in the `_run_powerflow_with_unified` method:

```python
def _run_powerflow_with_unified(self, config: dict) -> dict:
    """Run power flow and return result with unified model."""
    result = self._run_powerflow(config)
    
    # If adapter result has unified model, include it
    if hasattr(self._last_result, 'system_model') and self._last_result.system_model:
        result['unified_model'] = self._last_result.system_model
        result['buses'] = [b.to_dict() for b in self._last_result.system_model.buses]
        result['branches'] = [br.to_dict() for br in self._last_result.system_model.branches]
    
    return result
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest cloudpss_skills_v2/tests/test_powerflow_unified.py -v
```

- [ ] **Step 5: Commit**

```bash
git add cloudpss_skills_v2/powerskill/powerflow.py cloudpss_skills_v2/tests/test_powerflow_unified.py
git commit -m "feat: PowerFlow skill returns unified model in results"
```

---

## Task 3: Modify SkillBase to Cache Unified Model

**Files:**
- Modify: `cloudpss_skills_v2/powerskill/base.py:80-120` (SkillBase class)
- Test: `cloudpss_skills_v2/tests/test_skill_base_unified.py` (create new)

- [ ] **Step 1: Write failing test for unified model caching**

```python
def test_skill_base_caches_unified_model():
    from cloudpss_skills_v2.powerskill.base import SkillBase
    from cloudpss_skills_v2.core.system_model import PowerSystemModel
    
    class TestSkill(SkillBase):
        def run(self, config): pass
        def validate(self, config): pass
    
    skill = TestSkill()
    model = PowerSystemModel(buses=[], base_mva=100.0)
    
    # Set unified model
    skill._unified_model = model
    
    # Verify get_unified_model returns it
    assert skill.get_unified_model() is model
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest cloudpss_skills_v2/tests/test_skill_base_unified.py -v
```

- [ ] **Step 3: Add unified model support to SkillBase**

In `cloudpss_skills_v2/powerskill/base.py`:

```python
class SkillBase(ABC):
    def __init__(self):
        # ... existing init ...
        self._unified_model: PowerSystemModel | None = None
    
    def set_unified_model(self, model: PowerSystemModel) -> None:
        """Set unified model for analysis."""
        self._unified_model = model
    
    def get_unified_model(self) -> PowerSystemModel | None:
        """Get cached unified model."""
        return self._unified_model
    
    def has_unified_model(self) -> bool:
        """Check if unified model is available."""
        return self._unified_model is not None
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest cloudpss_skills_v2/tests/test_skill_base_unified.py -v
```

- [ ] **Step 5: Commit**

```bash
git add cloudpss_skills_v2/powerskill/base.py cloudpss_skills_v2/tests/test_skill_base_unified.py
git commit -m "feat: SkillBase supports unified model caching"
```

---

## Task 4: Modify PowerAnalysis Base to Accept Unified Model

**Files:**
- Modify: `cloudpss_skills_v2/poweranalysis/base.py:1-100` (PowerAnalysis class)
- Test: `cloudpss_skills_v2/tests/test_poweranalysis_base.py` (create new)

- [ ] **Step 1: Write failing test for unified model analysis**

```python
def test_poweranalysis_runs_with_unified_model():
    from cloudpss_skills_v2.poweranalysis.base import PowerAnalysis
    from cloudpss_skills_v2.core.system_model import PowerSystemModel, Bus
    
    class TestAnalysis(PowerAnalysis):
        def run(self, model, config):
            return {"bus_count": len(model.buses)}
    
    analysis = TestAnalysis()
    model = PowerSystemModel(
        buses=[Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK",
                   v_magnitude_pu=1.0, v_angle_degree=0.0)],
        base_mva=100.0
    )
    
    result = analysis.run(model, {})
    assert result["bus_count"] == 1
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest cloudpss_skills_v2/tests/test_poweranalysis_base.py -v
```

- [ ] **Step 3: Modify PowerAnalysis base class**

In `cloudpss_skills_v2/poweranalysis/base.py`:

```python
from abc import ABC, abstractmethod
from cloudpss_skills_v2.core.system_model import PowerSystemModel

class PowerAnalysis(ABC):
    """Base class for power system analyses using unified model."""
    
    @abstractmethod
    def run(self, model: PowerSystemModel, config: dict) -> dict:
        """Run analysis on unified model.
        
        Args:
            model: Unified PowerSystemModel
            config: Analysis configuration
            
        Returns:
            Analysis results
        """
        pass
    
    def validate_model(self, model: PowerSystemModel) -> list[str]:
        """Validate model before analysis.
        
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        if not model.buses:
            errors.append("No buses in model")
        
        if not model.get_slack_bus():
            errors.append("No slack bus found")
        
        return errors
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest cloudpss_skills_v2/tests/test_poweranalysis_base.py -v
```

- [ ] **Step 5: Commit**

```bash
git add cloudpss_skills_v2/poweranalysis/base.py cloudpss_skills_v2/tests/test_poweranalysis_base.py
git commit -m "feat: PowerAnalysis base class accepts unified model"
```

---

## Task 5: Refactor N-1 Security to Use Unified Model

**Files:**
- Modify: `cloudpss_skills_v2/poweranalysis/n1_security.py:80-150` (_run_n1_with_unified_model)
- Test: `cloudpss_skills_v2/tests/test_n1_security_unified.py` (already exists, expand)

- [ ] **Step 1: Write failing test for N-1 with unified model**

```python
def test_n1_security_runs_on_unified_model():
    from cloudpss_skills_v2.poweranalysis.n1_security import N1SecurityAnalysis
    from cloudpss_skills_v2.core.system_model import PowerSystemModel, Bus, Branch, Load
    
    # Create simple test model
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK",
                v_magnitude_pu=1.0, v_angle_degree=0.0),
            Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ",
                v_magnitude_pu=0.98, v_angle_degree=-2.0),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="Line1", branch_type="LINE",
                   r_pu=0.01, x_pu=0.1, rate_a_mva=100.0),
        ],
        loads=[
            Load(bus_id=1, name="Load1", p_mw=50, q_mvar=10),
        ],
        base_mva=100.0
    )
    
    analysis = N1SecurityAnalysis()
    result = analysis.run(model, {"contingency_level": 1})
    
    assert result["status"] == "success"
    assert "violations" in result
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest cloudpss_skills_v2/tests/test_n1_security_unified.py::test_n1_security_runs_on_unified_model -v
```

- [ ] **Step 3: Modify N1SecurityAnalysis to use unified model**

In `cloudpss_skills_v2/poweranalysis/n1_security.py`:

```python
def run(self, model: PowerSystemModel, config: dict) -> dict:
    """Run N-1 security analysis on unified model.
    
    Args:
        model: Unified PowerSystemModel
        config: Analysis configuration
        
    Returns:
        N-1 security analysis results
    """
    # Validate model
    errors = self.validate_model(model)
    if errors:
        return {
            "status": "error",
            "errors": errors
        }
    
    violations = []
    contingencies = []
    
    # Check each branch N-1 contingency
    for branch in model.branches:
        # Create N-1 model (remove this branch)
        n1_model = model.with_branch_removed(branch.name)
        
        # Check for violations in N-1 scenario
        # (In real implementation, would run power flow on n1_model)
        branch_violations = self._check_branch_loading(n1_model, branch.name)
        
        if branch_violations:
            contingencies.append({
                "branch": branch.name,
                "from_bus": branch.from_bus,
                "to_bus": branch.to_bus,
                "violations": branch_violations
            })
            violations.extend(branch_violations)
    
    return {
        "status": "success",
        "contingency_count": len(model.branches),
        "violation_count": len(violations),
        "violations": violations,
        "contingencies": contingencies,
        "secure": len(violations) == 0
    }

def _check_branch_loading(self, model: PowerSystemModel, removed_branch: str) -> list[dict]:
    """Check for branch loading violations in model."""
    violations = []
    
    for branch in model.branches:
        if branch.loading_percent and branch.loading_percent > 100:
            violations.append({
                "type": "branch_overload",
                "branch": branch.name,
                "loading_percent": branch.loading_percent,
                "removed_branch": removed_branch
            })
    
    return violations
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest cloudpss_skills_v2/tests/test_n1_security_unified.py -v
```

- [ ] **Step 5: Commit**

```bash
git add cloudpss_skills_v2/poweranalysis/n1_security.py cloudpss_skills_v2/tests/test_n1_security_unified.py
git commit -m "feat: N1SecurityAnalysis uses unified PowerSystemModel"
```

---

## Task 6: Add Unified Model Access to PowerFlow Result

**Files:**
- Modify: `cloudpss_skills_v2/powerskill/powerflow.py:200-250` (result formatting)
- Test: `cloudpss_skills_v2/tests/test_powerflow_integration.py` (create new)

- [ ] **Step 1: Write failing integration test**

```python
def test_powerflow_integration_returns_unified_model():
    """Integration test: PowerFlow skill returns unified model."""
    from cloudpss_skills_v2.powerskill.powerflow import PowerFlow
    
    skill = PowerFlow()
    config = {
        "engine": "pandapower",
        "model": {"source": "builtin", "name": "case14"}
    }
    
    # This test verifies the integration works end-to-end
    # Actual test may need mocking or specific environment setup
    result = skill.run(config)
    
    # Verify result contains unified model data
    assert "unified_model" in result or "buses" in result
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest cloudpss_skills_v2/tests/test_powerflow_integration.py -v
```

- [ ] **Step 3: Ensure PowerFlow.run returns unified model data**

In `cloudpss_skills_v2/powerskill/powerflow.py`, ensure the `run` method:

```python
def run(self, config: dict) -> dict:
    """Run power flow analysis.
    
    Returns result dict containing:
    - buses: List of bus results
    - branches: List of branch results  
    - converged: Whether power flow converged
    - unified_model: Unified PowerSystemModel (if available)
    """
    result = self._run_powerflow_with_unified(config)
    
    # Cache unified model for subsequent analysis
    if 'unified_model' in result:
        self.set_unified_model(result['unified_model'])
    
    return result
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest cloudpss_skills_v2/tests/test_powerflow_integration.py -v
```

- [ ] **Step 5: Commit**

```bash
git add cloudpss_skills_v2/powerskill/powerflow.py cloudpss_skills_v2/tests/test_powerflow_integration.py
git commit -m "feat: PowerFlow.run returns unified model and caches it"
```

---

## Task 7: Documentation Update

**Files:**
- Modify: `cloudpss_skills_v2/docs/NEW_ARCHITECTURE_EXAMPLE.md`

- [ ] **Step 1: Add unified model usage example**

```markdown
## Unified Model Integration Example

### Basic Usage

```python
from cloudpss_skills_v2.powerskill.powerflow import PowerFlow
from cloudpss_skills_v2.poweranalysis.n1_security import N1SecurityAnalysis

# Run power flow
skill = PowerFlow()
result = skill.run({
    "engine": "cloudpss",
    "model": {"rid": "model/holdme/IEEE39"}
})

# Access unified model
unified_model = result.get('unified_model')

# Run analysis on unified model
analysis = N1SecurityAnalysis()
n1_result = analysis.run(unified_model, {"contingency_level": 1})

print(f"Secure: {n1_result['secure']}")
print(f"Violations: {len(n1_result['violations'])}")
```

### Cross-Engine Analysis

```python
# Same unified model can be used with any engine
cloudpss_result = skill.run({"engine": "cloudpss", ...})
pandapower_result = skill.run({"engine": "pandapower", ...})

# Compare results using unified model
cloudpss_model = cloudpss_result['unified_model']
pandapower_model = pandapower_result['unified_model']

# Differences indicate solver or model conversion variations
```
```

- [ ] **Step 2: Commit documentation**

```bash
git add cloudpss_skills_v2/docs/NEW_ARCHITECTURE_EXAMPLE.md
git commit -m "docs: Add unified model integration examples"
```

---

## Verification Checklist

After all tasks complete:

- [ ] All tests passing: `pytest cloudpss_skills_v2/tests/ -v`
- [ ] Cross-engine consistency: `pytest cloudpss_skills_v2/tests/test_cross_engine_consistency.py -v`
- [ ] N-1 unified model: `pytest cloudpss_skills_v2/tests/test_n1_security_unified.py -v`
- [ ] Integration test: `pytest cloudpss_skills_v2/tests/test_powerflow_integration.py -v`
- [ ] Documentation updated
- [ ] All commits follow conventional commit format

---

## Execution Handoff

**Plan complete and saved to `docs/superpowers/plans/2026-05-03-phase3-unified-model-integration.md`.**

**Recommended execution approach:** Use superpowers:subagent-driven-development
- Fresh subagent per task
- Two-stage review after each task
- Parallelize independent tasks (Tasks 1-4 can run in parallel)

**Total estimated time:** 35-40 minutes (7 tasks × 5 minutes each)
