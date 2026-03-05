import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# 1. Weights for two different neurons
weights = np.array([np.pi/3, np.pi/6]) 

# 2. 2-qubit Variational Circuit
qc = QuantumCircuit(2, 2)

# 3. Layer 1: Parametrized Rotations (The Neurons)
qc.ry(weights[0], 0)
qc.ry(weights[1], 1)

# 4. Layer 2: Entanglement (The Correlation)
# This allows Neuron 0 to influence Neuron 1
qc.cx(0, 1)

# 5. Measure both
qc.measure([0, 1], [0, 1])

# 6. Execute
sim = AerSimulator()
counts = sim.run(transpile(qc, sim), shots=1024).result().get_counts()

print(f"\n--- Entangled Quantum Layer Output ---")
print(f"Weights: {weights}")
print(f"Joint Probabilities: {counts}")