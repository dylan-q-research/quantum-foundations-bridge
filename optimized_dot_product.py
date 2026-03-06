import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import time

# Generate two 1024-feature vectors
v_a = np.random.rand(1024)
v_a /= np.linalg.norm(v_a)

qc = QuantumCircuit(21, 1)
qc.prepare_state(v_a, range(1, 11))
qc.prepare_state(v_a, range(11, 21))
qc.h(0)
for i in range(10):
    qc.cswap(0, i + 1, i + 11)
qc.h(0)
qc.measure(0, 0)

sim = AerSimulator()

# --- THE OPTIMIZATION STEP ---
start_time = time.time()
# optimization_level=3 performs heavy gate-fusion
optimized_circuit = transpile(qc, sim, optimization_level=3)
end_time = time.time()

print(f"Transpilation (Level 3) completed in {end_time - start_time:.4f} seconds.")
print(f"Original Gate Count: {len(qc.data)}")
print(f"Optimized Gate Count: {len(optimized_circuit.data)}")

# Run the optimized circuit
result = sim.run(optimized_circuit, shots=512).result()
print(f"Result: {result.get_counts()}")