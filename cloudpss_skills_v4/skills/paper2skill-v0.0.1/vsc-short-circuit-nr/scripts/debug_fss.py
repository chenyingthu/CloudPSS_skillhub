"""Debug why FSS mode fails to converge."""
import sys
sys.path.insert(0, '.')

from scripts.vsc_nr_solver import PaperFaithfulShortCircuitSolver, VSCConverterSpec
import numpy as np

# Build a minimal 2-bus test: slack=bus0 (GFM VSC1), fault at bus1 (VSC2)
# GFM converter at bus0 in FSS mode
converters = [
    VSCConverterSpec(bus=0, p_ref=0.0, q_ref=0.0, i_max=2.5, control_mode="GFM"),
    VSCConverterSpec(bus=1, p_ref=-0.794, q_ref=0.0, i_max=1.0, control_mode="PV"),
]

# Simple 2-bus network: 10 pu impedance
Y = np.array([
    [10.0 - 50.0j, -10.0 + 50.0j],
    [-10.0 + 50.0j, 10.0 - 50.0j],
], dtype=np.complex128)

solver = PaperFaithfulShortCircuitSolver(tolerance=1e-6, max_iter=20)

# Force FSS mode for converter 0 (GFM)
modes = ["FSS", "FSS"]
print(f"Testing FSS mode: modes={modes}")
print(f"Converters: {[(c.bus, c.control_mode, c.i_max) for c in converters]}")

result = solver._solve_given_modes_nr(
    network_matrix=Y,
    slack_bus=0,
    slack_voltage=1.0 + 0.0j,
    converters=converters,
    modes=modes,
    layout=solver._build_layout(2, 0, converters),
    previous_state=None,
)

print(f"\nResult: converged={result.converged}, iterations={result.iterations}")
print(f"Max residual: {result.max_residual}")
print(f"Voltages: {result.voltages}")
print(f"Currents: {result.current_injections}")

# Check each residual component
from scripts.vsc_nr_solver import NewtonStateLayout
layout = solver._build_layout(2, 0, converters)
residual = solver._evaluate_residual(
    state_vector=result.internal_state_vector if result.internal_state_vector is not None else np.zeros(2*2 + 2*2),
    network_matrix=Y,
    slack_bus=0,
    slack_voltage=1.0 + 0.0j,
    converters=converters,
    modes=modes,
    layout=layout,
)
print(f"\nResidual vector (first 10): {residual[:10]}")
print(f"Residual max: {np.max(np.abs(residual))}")

# Decode solution
if result.internal_state_vector is not None:
    voltages, currents = solver._decode_solution(result.internal_state_vector, layout)
    print(f"\nDecoded voltages: {voltages}")
    print(f"Decoded active currents (I_r, I_i): {currents}")
    for i, c in enumerate(converters):
        print(f"  Converter {i} @ bus {c.bus}: I={currents[i]:.6f}, |I|={abs(currents[i]):.6f}, I_max={c.i_max}")
        print(f"    Voltage @ bus {c.bus}: {voltages[c.bus]:.6f}, |V|={abs(voltages[c.bus]):.6f}")
