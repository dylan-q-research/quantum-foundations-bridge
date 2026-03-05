from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_bloch_multivector
import matplotlib.pyplot as plt

# 1. Create 2 qubits
qc = QuantumCircuit(2)

# 2. Put Qubit 0 in superposition and Qubit 1 in the |1> state
qc.h(0)
qc.x(1)
qc.h(1)

# 3. Apply CNOT - This is where the "Kickback" happens
# The phase of the target (q1) kicks back to the control (q0)
qc.cx(0, 1)

# 4. Final Hadamard on q0 to see the result
qc.h(0)

# 5. Draw the circuit in the terminal to verify the layout
print(qc.draw(output='text'))

# 6. Execute to see the state change
sim = AerSimulator()
qc.save_statevector()
state = sim.run(transpile(qc, sim)).result().get_statevector()
print(f"\nFinal Statevector: {state}")