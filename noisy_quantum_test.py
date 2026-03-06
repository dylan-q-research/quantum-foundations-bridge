from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
import matplotlib.pyplot as plt

# 1. Create a 2-qubit Bell State (Simple enough to see noise)
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

# 2. Build a "Synthetic" Noise Model
# Every CX gate has a 5% chance of flipping a bit (Entropy)
noise_model = NoiseModel()
error_cx = depolarizing_error(0.05, 2)
noise_model.add_all_qubit_quantum_error(error_cx, ['cx'])

# 3. Execute with vs without noise
sim_ideal = AerSimulator()
sim_noisy = AerSimulator(noise_model=noise_model)

counts_ideal = sim_ideal.run(qc, shots=1024).result().get_counts()
counts_noisy = sim_noisy.run(qc, shots=1024).result().get_counts()

print(f"Ideal Results: {counts_ideal}")
print(f"Noisy Results (5% CX Error): {counts_noisy}")