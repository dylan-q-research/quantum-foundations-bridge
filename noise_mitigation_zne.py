"""
Research Project: Zero-Noise Extrapolation (ZNE)
Researcher: Dylan Cabrera Giler
Objective: Implementing error mitigation to recover ideal expectation values 
from noisy NISQ-era hardware simulations.
"""

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

def get_noisy_result(circuit, noise_factor):
    # Create a depolarizing noise model
    noise_model = NoiseModel()
    error = depolarizing_error(0.01 * noise_factor, 1)
    noise_model.add_all_qubit_quantum_error(error, ['u1', 'u2', 'u3'])
    
    sim = AerSimulator(noise_model=noise_model)
    result = sim.run(transpile(circuit, sim), shots=2048).result().get_counts()
    return result.get('0', 0) / 2048

# Simple Circuit: H-gate to create superposition
qc = QuantumCircuit(1)
qc.h(0)
qc.h(0) # Ideal result should be |0> (Probability 1.0)

# Measure at different noise scales
scales = [1, 2, 3]
results = [get_noisy_result(qc, s) for s in scales]

# Linear Extrapolation to noise=0
# y = mx + c -> c is the value at x=0
m, c = np.polyfit(scales, results, 1)

print(f"--- Zero-Noise Extrapolation (ZNE) Results ---")
for s, r in zip(scales, results):
    print(f"Noise Scale {s}: Measured P(0) = {r:.4f}")

print(f"\nMitigated (Extrapolated) P(0): {c:.4f}")
print(f"Ideal Theoretical P(0): 1.0000")