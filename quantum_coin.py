from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)

sim = AerSimulator()
result = sim.run(qc, shots=1, memory=True).result()
flip = result.get_memory()[0]
print(f"The Universe chose: {'HEADS (0)' if flip == '0' else 'TAILS (1)'}")