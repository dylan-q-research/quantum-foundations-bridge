import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector

# 1. Initialize 1 qubit
qc = QuantumCircuit(1)

# 2. Step One: Put it on the Equator (Hadamard)
qc.h(0)

# 3. Step Two: Rotate it by 90 degrees (pi/2) around the Z-axis
# This is a Phase Gate (P gate)
import math
qc.p(math.pi / 2, 0)

# 4. Capture the Statevector to see the new "Phase"
state = Statevector.from_instruction(qc)

# 5. Visualize on the Bloch Sphere
print("Rotating qubit phase by 90 degrees...")
plot_bloch_multivector(state)
plt.show()