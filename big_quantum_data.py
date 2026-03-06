import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# 1. Generate 'Big Data': 1024 random features
# In a real Argonne project, this would be sensor data
vector_a = np.random.rand(1024)
vector_a /= np.linalg.norm(vector_a) # Must be normalized for Quantum States

# 2. Initialize a 10-qubit circuit
qc = QuantumCircuit(10)

# 3. Amplitude Encoding: Map 1024 classical numbers to 10 qubits
# This is the "Exponential Compression" of Quantum Computing
qc.prepare_state(vector_a)

# 4. Save the Statevector to verify the encoding
qc.save_statevector()

# 5. Execute
sim = AerSimulator()
state = sim.run(transpile(qc, sim)).result().get_statevector()

print(f"Successfully encoded 1024 features into 10 qubits.")
print(f"Statevector size: {len(state)}")