from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import numpy as np

def swap_test(angle1, angle2):
    # 3 Qubits: 0 = Ancilla, 1 = Data A, 2 = Data B
    qc = QuantumCircuit(3, 1)
    
    # Encode Data A and Data B
    qc.ry(angle1, 1)
    qc.ry(angle2, 2)
    qc.barrier()
    
    # The Swap Test
    qc.h(0)
    qc.cswap(0, 1, 2) # Swap q1 and q2 conditioned on q0
    qc.h(0)
    
    qc.measure(0, 0)
    sim = AerSimulator()
    counts = sim.run(transpile(qc, sim), shots=1024).result().get_counts()
    return counts.get('0', 0) / 1024

# Compare: Same vs Different
similarity_same = swap_test(1.57, 1.57) # pi/2 vs pi/2
similarity_diff = swap_test(0.0, 3.14)  # 0 vs pi

print(f"\nSimilarity (Same): {similarity_same:.3f}")
print(f"Similarity (Opposite): {similarity_diff:.3f}")