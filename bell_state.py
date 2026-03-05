import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

# 1. Initialize a circuit with 2 qubits and 2 classical bits
qc = QuantumCircuit(2, 2)

# 2. Apply a Hadamard gate (H) to qubit 0
qc.h(0)

# 3. Apply a Controlled-NOT gate (CNOT) 
qc.cx(0, 1)

# 4. Measure the qubits
qc.measure([0, 1], [0, 1])

# 5. Execute using the Aer Simulator
simulator = AerSimulator()
result = simulator.run(qc).result()
counts = result.get_counts()

# 6. Print the results
print(f"\nQuantum Entanglement Results: {counts}\n")

# 7. Visualize
plot_histogram(counts)
plt.show()