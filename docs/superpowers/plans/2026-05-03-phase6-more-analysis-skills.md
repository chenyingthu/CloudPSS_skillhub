# Phase 6 More Analysis Skills Migration Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate 5 more critical analysis skills to unified PowerSystemModel architecture.

**Architecture:** Each skill inherits from `PowerAnalysis` base class.

**Tech Stack:** Python, PowerSystemModel, PowerAnalysis

---

## File Structure

| File | Responsibility | Action |
|------|---------------|--------|
| `cloudpss_skills_v2/poweranalysis/loss_analysis.py` | Network loss analysis | Refactor |
| `cloudpss_skills_v2/poweranalysis/n2_security.py` | N-2 security analysis | Refactor |
| `cloudpss_skills_v2/poweranalysis/thevenin_equivalent.py` | Thevenin equivalent | Refactor |
| `cloudpss_skills_v2/poweranalysis/contingency_analysis.py` | Contingency analysis | Refactor |
| `cloudpss_skills_v2/poweranalysis/harmonic_analysis.py` | Harmonic analysis | Refactor |
| `cloudpss_skills_v2/tests/test_loss_analysis_unified.py` | Unified model tests | Create |
| `cloudpss_skills_v2/tests/test_n2_security_unified.py` | Unified model tests | Create |
| `cloudpss_skills_v2/tests/test_thevenin_equivalent_unified.py` | Unified model tests | Create |
| `cloudpss_skills_v2/tests/test_contingency_analysis_unified.py` | Unified model tests | Create |
| `cloudpss_skills_v2/tests/test_harmonic_analysis_unified.py` | Unified model tests | Create |

---

## Task 1: Refactor Loss Analysis

**Files:**
- Modify: `cloudpss_skills_v2/poweranalysis/loss_analysis.py`
- Create: `cloudpss_skills_v2/tests/test_loss_analysis_unified.py`

- [ ] **Step 1: Write failing test**

```python
def test_loss_analysis_runs_on_unified_model():
    from cloudpss_skills_v2.poweranalysis.loss_analysis import LossAnalysis
    from cloudpss_skills_v2.core.system_model import PowerSystemModel, Bus, Branch, Generator, Load
    
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK",
                v_magnitude_pu=1.0, v_angle_degree=0.0),
            Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ",
                v_magnitude_pu=0.98, v_angle_degree=-2.0),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="Line1-2", branch_type="LINE",
                   r_pu=0.01, x_pu=0.1, rate_a_mva=100.0,
                   p_from_mw=50, p_to_mw=-49),  # 1MW loss
        ],
        generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=100)],
        loads=[Load(bus_id=1, name="Load1", p_mw=50)],
        base_mva=100.0
    )
    
    analysis = LossAnalysis()
    result = analysis.run(model, {"detail_level": "branch"})
    
    assert result["status"] == "success"
    assert "total_loss_mw" in result
    assert "branch_losses" in result
```

- [ ] **Step 2: Run test to verify it fails**

- [ ] **Step 3: Modify LossAnalysis to inherit from PowerAnalysis**

Key changes:
- Inherit from `PowerAnalysis`
- Add `run(self, model: PowerSystemModel, config: dict) -> dict` method
- Calculate branch losses from p_from_mw - p_to_mw
- Calculate transformer losses if applicable
- Return total loss and per-branch breakdown

- [ ] **Step 4: Run test to verify it passes**

- [ ] **Step 5: Commit**

```bash
git add cloudpss_skills_v2/poweranalysis/loss_analysis.py cloudpss_skills_v2/tests/test_loss_analysis_unified.py
git commit -m "feat: LossAnalysis uses unified PowerSystemModel"
```

---

## Task 2: Refactor N-2 Security Analysis

**Files:**
- Modify: `cloudpss_skills_v2/poweranalysis/n2_security.py`
- Create: `cloudpss_skills_v2/tests/test_n2_security_unified.py`

- [ ] **Step 1: Write failing test**

```python
def test_n2_security_runs_on_unified_model():
    from cloudpss_skills_v2.poweranalysis.n2_security import N2SecurityAnalysis
    from cloudpss_skills_v2.core.system_model import PowerSystemModel, Bus, Branch
    
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ"),
            Bus(bus_id=2, name="Bus3", base_kv=230.0, bus_type="PQ"),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="Line1", branch_type="LINE", r_pu=0.01, x_pu=0.1, rate_a_mva=100),
            Branch(from_bus=1, to_bus=2, name="Line2", branch_type="LINE", r_pu=0.01, x_pu=0.1, rate_a_mva=100),
            Branch(from_bus=0, to_bus=2, name="Line3", branch_type="LINE", r_pu=0.02, x_pu=0.2, rate_a_mva=100),
        ],
        base_mva=100.0
    )
    
    analysis = N2SecurityAnalysis()
    result = analysis.run(model, {"check_pairs": []})  # Check all pairs
    
    assert result["status"] == "success"
    assert "n2_results" in result
    assert "total_pairs" in result
```

- [ ] **Step 2: Run test to verify it fails**

- [ ] **Step 3: Modify N2SecurityAnalysis**

Key changes:
- Inherit from `PowerAnalysis`
- Implement `run(self, model: PowerSystemModel, config: dict)` method
- Generate all branch pairs (N-2 contingencies)
- Use model.with_branches_removed() for each pair
- Check violations for each contingency
- Return summary of all N-2 violations

- [ ] **Step 4: Run test to verify it passes**

- [ ] **Step 5: Commit**

```bash
git add cloudpss_skills_v2/poweranalysis/n2_security.py cloudpss_skills_v2/tests/test_n2_security_unified.py
git commit -m "feat: N2SecurityAnalysis uses unified PowerSystemModel"
```

---

## Task 3: Refactor Thevenin Equivalent Analysis

**Files:**
- Modify: `cloudpss_skills_v2/poweranalysis/thevenin_equivalent.py`
- Create: `cloudpss_skills_v2/tests/test_thevenin_equivalent_unified.py`

- [ ] **Step 1: Write failing test**

```python
def test_thevenin_equivalent_runs_on_unified_model():
    from cloudpss_skills_v2.poweranalysis.thevenin_equivalent import TheveninEquivalentAnalysis
    from cloudpss_skills_v2.core.system_model import PowerSystemModel, Bus, Branch
    
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK", v_magnitude_pu=1.0),
            Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ", v_magnitude_pu=0.98),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="Line1", branch_type="LINE", r_pu=0.01, x_pu=0.1),
        ],
        base_mva=100.0
    )
    
    analysis = TheveninEquivalentAnalysis()
    result = analysis.run(model, {"target_bus": "Bus2"})
    
    assert result["status"] == "success"
    assert "thevenin_voltage_pu" in result
    assert "thevenin_impedance_pu" in result
```

- [ ] **Step 2: Run test to verify it fails**

- [ ] **Step 3: Modify TheveninEquivalentAnalysis**

Key changes:
- Inherit from `PowerAnalysis`
- Add `run(self, model: PowerSystemModel, config: dict)` method
- For target bus, calculate Thevenin equivalent:
  - V_th = Open circuit voltage at target bus
  - Z_th = Equivalent impedance looking into network from target bus
- Can use simplified calculation based on network admittance matrix

- [ ] **Step 4: Run test to verify it passes**

- [ ] **Step 5: Commit**

```bash
git add cloudpss_skills_v2/poweranalysis/thevenin_equivalent.py cloudpss_skills_v2/tests/test_thevenin_equivalent_unified.py
git commit -m "feat: TheveninEquivalentAnalysis uses unified PowerSystemModel"
```

---

## Task 4: Refactor Contingency Analysis

**Files:**
- Modify: `cloudpss_skills_v2/poweranalysis/contingency_analysis.py`
- Create: `cloudpss_skills_v2/tests/test_contingency_analysis_unified.py`

- [ ] **Step 1: Write failing test**

```python
def test_contingency_analysis_runs_on_unified_model():
    from cloudpss_skills_v2.poweranalysis.contingency_analysis import ContingencyAnalysis
    from cloudpss_skills_v2.core.system_model import PowerSystemModel, Bus, Branch, Generator
    
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ"),
            Bus(bus_id=2, name="Bus3", base_kv=230.0, bus_type="PQ"),
        ],
        branches=[
            Branch(from_bus=0, to_bus=1, name="Line1", branch_type="LINE", rate_a_mva=100),
            Branch(from_bus=1, to_bus=2, name="Line2", branch_type="LINE", rate_a_mva=80),
        ],
        generators=[Generator(bus_id=0, name="Gen1", p_gen_mw=100)],
        base_mva=100.0
    )
    
    analysis = ContingencyAnalysis()
    result = analysis.run(model, {
        "contingency_type": "n1",
        "check_violations": ["thermal", "voltage"]
    })
    
    assert result["status"] == "success"
    assert "contingencies" in result
    assert "summary" in result
```

- [ ] **Step 2: Run test to verify it fails**

- [ ] **Step 3: Modify ContingencyAnalysis**

Key changes:
- Inherit from `PowerAnalysis`
- Add `run(self, model: PowerSystemModel, config: dict)` method
- Support different contingency types: n1, n2, n1_1 (N-1-1)
- For each contingency:
  - Create modified model with component removed
  - Check for violations (thermal, voltage)
- Return contingency results with severity assessment

- [ ] **Step 4: Run test to verify it passes**

- [ ] **Step 5: Commit**

```bash
git add cloudpss_skills_v2/poweranalysis/contingency_analysis.py cloudpss_skills_v2/tests/test_contingency_analysis_unified.py
git commit -m "feat: ContingencyAnalysis uses unified PowerSystemModel"
```

---

## Task 5: Refactor Harmonic Analysis

**Files:**
- Modify: `cloudpss_skills_v2/poweranalysis/harmonic_analysis.py`
- Create: `cloudpss_skills_v2/tests/test_harmonic_analysis_unified.py`

- [ ] **Step 1: Write failing test**

```python
def test_harmonic_analysis_runs_on_unified_model():
    from cloudpss_skills_v2.poweranalysis.harmonic_analysis import HarmonicAnalysis
    from cloudpss_skills_v2.core.system_model import PowerSystemModel, Bus
    
    model = PowerSystemModel(
        buses=[
            Bus(bus_id=0, name="Bus1", base_kv=230.0, bus_type="SLACK"),
            Bus(bus_id=1, name="Bus2", base_kv=230.0, bus_type="PQ"),
        ],
        base_mva=100.0
    )
    
    analysis = HarmonicAnalysis()
    result = analysis.run(model, {
        "harmonic_orders": [3, 5, 7],
        "sources": [{"bus": "Bus2", "order": 5, "magnitude": 0.05}]
    })
    
    assert result["status"] == "success"
    assert "harmonic_voltages" in result
    assert "thd" in result  # Total Harmonic Distortion
```

- [ ] **Step 2: Run test to verify it fails**

- [ ] **Step 3: Modify HarmonicAnalysis**

Key changes:
- Inherit from `PowerAnalysis`
- Add `run(self, model: PowerSystemModel, config: dict)` method
- For each harmonic order:
  - Build harmonic impedance matrix
  - Calculate harmonic voltage at each bus
- Calculate THD (Total Harmonic Distortion) at each bus
- Return harmonic voltages and distortion levels

- [ ] **Step 4: Run test to verify it passes**

- [ ] **Step 5: Commit**

```bash
git add cloudpss_skills_v2/poweranalysis/harmonic_analysis.py cloudpss_skills_v2/tests/test_harmonic_analysis_unified.py
git commit -m "feat: HarmonicAnalysis uses unified PowerSystemModel"
```

---

## Verification Checklist

After all tasks complete:

- [ ] All tests passing: `pytest cloudpss_skills_v2/tests/test_*_unified.py -v`
- [ ] Loss Analysis: `pytest cloudpss_skills_v2/tests/test_loss_analysis_unified.py -v`
- [ ] N-2 Security: `pytest cloudpss_skills_v2/tests/test_n2_security_unified.py -v`
- [ ] Thevenin Equivalent: `pytest cloudpss_skills_v2/tests/test_thevenin_equivalent_unified.py -v`
- [ ] Contingency Analysis: `pytest cloudpss_skills_v2/tests/test_contingency_analysis_unified.py -v`
- [ ] Harmonic Analysis: `pytest cloudpss_skills_v2/tests/test_harmonic_analysis_unified.py -v`
- [ ] All skills inherit from PowerAnalysis
- [ ] All commits follow conventional commit format

---

## Execution Handoff

**Plan complete and saved to `docs/superpowers/plans/2026-05-03-phase6-more-analysis-skills.md`.**

**Recommended execution approach:** Use superpowers:subagent-driven-development
- Fresh subagent per task
- Tasks 1-5 can run in parallel

**Total estimated time:** 30-35 minutes (5 tasks × 6-7 minutes each)
