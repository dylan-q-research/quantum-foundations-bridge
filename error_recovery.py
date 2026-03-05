from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# 1. Initialize 3 qubits
qc = QuantumCircuit(3)

# 2. Encode
qc.cx(0, 1)
qc.cx(0, 2)

# 3. Introduce the Error (Bit-flip on q0)
qc.x(0)
qc.barrier()

# 4. Syndrome Detection
qc.cx(0, 1)
qc.cx(0, 2)

# 5. Recovery: The Toffoli Gate (CCX)
# If q1 and q2 are both 1, flip q0 back to its original state
qc.ccx(1, 2, 0)

# 6. Verify: Save the statevector
qc.save_statevector()
sim = AerSimulator()
state = sim.run(transpile(qc, sim)).result().get_statevector()

print(f"Final Corrected State: {state}")