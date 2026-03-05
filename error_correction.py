from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# 1. 3 qubits (1 logical, 2 for parity) and 2 classical bits
qc = QuantumCircuit(3, 2)

# 2. Encode: Entangle q1 and q2 with q0
qc.cx(0, 1)
qc.cx(0, 2)
qc.barrier()

# 3. Simulate a "Bit-Flip Error" (Pretend q0 flipped)
qc.x(0) 
qc.barrier()

# 4. Error Detection: Syndrome Measurement
qc.cx(0, 1)
qc.cx(0, 2)

# 5. Measure the parity qubits
qc.measure([1, 2], [0, 1])

# 6. Execute to see the "Syndrome"
sim = AerSimulator()
counts = sim.run(qc).result().get_counts()
print(f"Error Syndrome detected: {counts}")