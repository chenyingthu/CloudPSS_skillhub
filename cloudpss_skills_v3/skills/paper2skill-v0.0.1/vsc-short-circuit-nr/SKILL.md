---
name: vsc-short-circuit-nr
title: "A short-circuit calculation solver for power systems with power electronics converters"
version: 0.0.1
engine: paper2skill-v0.0.1
license: MIT
url: "https://doi.org/10.1016/j.ijepes.2024.109839"
keywords: [Short-Circuit, VSC, Newton-Raphson, Current Saturation, Power Electronics]
description: "Extended Newton-Raphson solver for steady-state short-circuit calculation in power systems with voltage source converters, considering converter operation limits and current saturation states."
---

# VSC Short-Circuit Calculation with Extended NR Solver

Modern power systems increasingly use power electronics converters (VSCs) for renewable integration, HVDC, and battery storage. These converters behave differently from synchronous generators during faults—their current can saturate, and their control modes affect the short-circuit current. Traditional short-circuit methods that model converters as simple current sources don't capture this complexity.

This skill provides an extended Newton-Raphson (NR) solver that computes steady-state short-circuit equilibrium points considering VSC operation limits and current saturation states. It avoids the need for detailed dynamic simulations while maintaining accuracy.

## Core Concept

The key insight is that VSCs operate in different modes (PSSin which active power control, and FSS where reactive power is prioritized), and their current saturation changes the system behavior during faults. The extended NR solver:

1. **Models VSC steady-state control equations** within the system formulation
2. **Identifies current saturation states** through an iterative algorithm
3. **Computes the short-circuit equilibrium point** considering converter limits

## Architecture Overview

- **VSC Steady-State Model**: Models converters with their control modes (P/Q control, voltage control)
- **Current Saturation Detection**: Iteratively identifies saturated vs. linear operating states
- **Extended NR Solver**: Solves for equilibrium considering converter limits
- **Dynamic Validation**: Compares results with EMT simulation for verification

## Implementation Steps

### Step 1: Define VSC Steady-State Model

```python
import numpy as np

class VSCOperatingPoint:
    """Represents VSC operating state during fault"""
    def __init__(self, v_sc, i_max, p_ref, q_ref, mode='PSS'):
        self.v_sc = v_sc          # Converter voltage
        self.i_max = i_max        # Current limit
        self.p_ref = p_ref        # Active power reference
        self.q_ref = q_ref        # Reactive power reference
        self.mode = mode          # 'PSS' or 'FSS'

    def compute_current(self, v_grid):
        """Compute converter current based on control mode"""
        i_p = self.p_ref / v_grid if v_grid > 0 else 0
        i_q = self.q_ref / v_grid if v_grid > 0 else 0
        i_mag = np.sqrt(i_p**2 + i_q**2)

        if i_mag > self.i_max:
            return self._saturate(i_p, i_q, i_mag)
        return i_p, i_q

    def _saturate(self, i_p, i_q, i_mag):
        """Apply current saturation"""
        scale = self.i_max / i_mag
        if self.mode == 'FSS':
            # Reactive power prioritized
            i_q_sat = self.i_max
            i_p_sat = np.sqrt(self.i_max**2 - i_q**2)
        else:
            i_p_sat = i_p * scale
            i_q_sat = i_q * scale
        return i_p_sat, i_q_sat
```

### Step 2: Extended NR Solver for Short-Circuit

```python
def extended_nr_short_circuit(Y_bus, v_sc, v_g, converters, tolerance=1e-6, max_iter=50):
    """
    Extended Newton-Raphson for short-circuit with VSCs

    Args:
        Y_bus: System admittance matrix
        v_sc: Fault location bus
        v_g: Generator voltages (dict of bus: voltage)
        converters: List of VSC operating points
        tolerance: Convergence tolerance
        max_iter: Maximum iterations

    Returns:
        V: Bus voltages after convergence
        converged: Boolean indicating convergence
    """
    n = len(Y_bus)
    V = np.ones(n, dtype=complex)  # Initial voltage guess

    for iteration in range(max_iter):
        # Build Jacobian
        J = build_jacobian(Y_bus, V, converters)

        # Compute mismatch
        S_inj = V * np.conj(Y_bus @ V)
        S_target = {bus: converters[bus].p_ref + 1j*converters[bus].q_ref
                   for bus in converters}
        mismatch = compute_mismatch(S_inj, S_target, v_sc)

        # Solve NR update
        delta_V = np.linalg.solve(J, mismatch)
        V = V - delta_V

        if np.linalg.norm(delta_V) < tolerance:
            return V, True

    return V, False
```

### Step 3: Current Saturation Identification

```python
def identify_saturation(V, converters, v_grid):
    """
    Iteratively identify converter current saturation states

    Returns:
        saturated: List of buses where converters are saturated
        linear: List of buses where converters operate linearly
    """
    saturated = []
    linear = []

    for bus, vsc in converters.items():
        i_p, i_q = vsc.compute_current(V[bus])
        i_mag = np.sqrt(i_p**2 + i_q**2)

        if i_mag >= vsc.i_max * 0.99:
            saturated.append(bus)
        else:
            linear.append(bus)

    return saturated, linear
```

## Practical Guidance

### When to Use

- Power systems with high VSC penetration (renewable integration, HVDC)
- Protection setting calculations for modern power systems
- Short-circuit studies requiring accurate converter contribution
- Comparing steady-state vs. dynamic simulation results

### When NOT to Use

- Conventional systems without power electronics
- When detailed transient response is needed (use EMT)
- Systems where converter saturation is not a concern

### Hyperparameters

| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| `i_max` | Converter current limit (pu) | 1.1–1.5 |
| tolerance | NR convergence tolerance | 1e-6–1e-4 |
| max_iter | Maximum NR iterations | 20–50 |

### Common Pitfalls

1. **Ignoring saturation**: Always run saturation identification after initial solution
2. **Mode confusion**: PSS (active power) vs FSS (reactive power) modes behave differently
3. **Initialization**: Start with flat voltage profile (1.0 pu) for better convergence

## Reference

- Paper: *A short-circuit calculation solver for power systems with power electronics converters*
- DOI: https://doi.org/10.1016/j.ijepes.2024.109839
- Authors: Jie Song, Josep Fanals-Batllori, Leonardo Marín, et al.
- Test Cases: IEEE 9-bus, IEEE 39-bus with VSC additions