import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def get_quantum_similarity(vec1, vec2):
    # Normalize vectors
    vec1 = vec1 / np.linalg.norm(vec1)
    vec2 = vec2 / np.linalg.norm(vec2)
    
    # 21 Qubits: 0 = Ancilla, 1-10 = Reg A, 11-20 = Reg B
    qc = QuantumCircuit(21, 1)
    
    # Encode both 1024-feature vectors
    qc.prepare_state(vec1, range(1, 11))
    qc.prepare_state(vec2, range(11, 21))
    
    # Execute Swap Test on all 10 pairs simultaneously
    qc.h(0)
    for i in range(10):
        qc.cswap(0, i + 1, i + 11)
    qc.h(0)
    
    qc.measure(0, 0)
    
    sim = AerSimulator()
    # Using low shots for speed, increase to 1024 for Argonne-level precision
    counts = sim.run(transpile(qc, sim), shots=512).result().get_counts()
    return counts.get('0', 0) / 512

# Test: Same vs Random
v_a = np.random.rand(1024)
v_b = np.random.rand(1024)

sim_self = get_quantum_similarity(v_a, v_a)
sim_diff = get_quantum_similarity(v_a, v_b)

print(f"\nSimilarity (Self): {sim_self:.3f}")
print(f"Similarity (Random): {sim_diff:.3f}")