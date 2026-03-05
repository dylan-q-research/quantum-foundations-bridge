from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# 1. 2 qubits
qc = QuantumCircuit(2)

# 2. Initialization: Superposition
qc.h([0, 1])

# 3. The Oracle: Mark the state |11> using a CZ gate
qc.cz(0, 1)

# 4. The Diffusion Operator (The "Amplifier")
qc.h([0, 1])
qc.z([0, 1])
qc.cz(0, 1)
qc.h([0, 1])

# 5. Measure
qc.measure_all()

# 6. Execute
sim = AerSimulator()
result = sim.run(transpile(qc, sim), shots=1024).result()
counts = result.get_counts()
print(f"Grover Search Result (Expected '11'): {counts}")

plot_histogram(counts)
plt.show()