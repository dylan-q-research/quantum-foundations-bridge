from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import numpy as np

# 1. Define a 'Weight' (Rotation Angle in Radians)
# Let's start with pi/4 (45 degrees)
theta = np.pi / 4 

# 2. Create a 1-qubit circuit
qc = QuantumCircuit(1, 1)

# 3. The "Quantum Neuron": A parametrized Y-axis rotation
# This 'learns' by adjusting the theta value
qc.ry(theta, 0)

# 4. Measure
qc.measure(0, 0)

# 5. Execute 1024 trials
sim = AerSimulator()
counts = sim.run(transpile(qc, sim), shots=1024).result().get_counts()

print(f"\n--- Quantum Neuron Output (theta = {theta:.2f}) ---")
print(f"Results: {counts}")