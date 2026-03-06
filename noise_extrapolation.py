import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

def run_bell_with_noise(prob):
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    
    noise_model = NoiseModel()
    error_cx = depolarizing_error(prob, 2)
    noise_model.add_all_qubit_quantum_error(error_cx, ['cx'])
    
    sim = AerSimulator(noise_model=noise_model)
    counts = sim.run(qc, shots=2000).result().get_counts()
    # Return the probability of being in the 'correct' Bell states (00 or 11)
    return (counts.get('00', 0) + counts.get('11', 0)) / 2000

# 1. Measure at Noise Level X (5%) and 2X (10%)
y1 = run_bell_with_noise(0.05)
y2 = run_bell_with_noise(0.10)

# 2. Richardson Extrapolation: f(0) ≈ 2*f(x) - f(2x)
zero_noise_estimate = 2 * y1 - y2

print(f"Fidelity at 5% Noise: {y1:.4f}")
print(f"Fidelity at 10% Noise: {y2:.4f}")
print(f"--- Extrapolated Zero-Noise Fidelity: {zero_noise_estimate:.4f} ---")