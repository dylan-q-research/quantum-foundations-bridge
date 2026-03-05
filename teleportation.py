from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# 1. Initialize 3 qubits and 3 classical bits
# q0 = message, q1 = Alice's half, q2 = Bob's half
qc = QuantumCircuit(3, 3)

# 2. Prepare the state to teleport on q0 (Let's use a 90-degree rotation)
qc.h(0)
qc.p(3.14/2, 0) # Applying a Phase Shift
qc.barrier()

# 3. Create Entanglement between q1 and q2 (The shared resource)
qc.h(1)
qc.cx(1, 2)
qc.barrier()

# 4. Alice performs a Bell Measurement on q0 and q1
qc.cx(0, 1)
qc.h(0)
qc.barrier()

# 5. Measure q0 and q1
qc.measure([0, 1], [0, 1])
qc.barrier()

# 6. Bob applies "Corrections" to q2 based on Alice's measurements
# This is the "Teleportation" of the state
qc.cx(1, 2)
qc.cz(0, 2)

# 7. Bob measures his qubit to verify the state arrived
qc.measure(2, 2)

# 8. Draw the layout
print(qc.draw(output='text'))

# 9. Execute
sim = AerSimulator()
result = sim.run(transpile(qc, sim), shots=1024).result()
counts = result.get_counts()
plot_histogram(counts)
plt.show()