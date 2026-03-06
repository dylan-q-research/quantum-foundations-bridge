"""
Research Project: Unsupervised Quantum Clustering via Kernel Estimation
Researcher: Dylan Cabrera Giler
Objective: Utilizing the Swap Test to derive an Overlap Integral, effectively 
partitioning a non-labeled dataset into discrete Hilbert Space neighborhoods.
"""

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def get_similarity(x1, x2):
    """
    Calculates the 'Inner Product' between two quantum feature vectors.
    High similarity indicates a proximity in the underlying metric space.
    """
    qc = QuantumCircuit(3, 1)
    qc.ry(x1, 1) # Feature Map: Encoding Scalar 1
    qc.ry(x2, 2) # Feature Map: Encoding Scalar 2
    
    # --- SWAP TEST PROTOCOL ---
    # Measuring the overlap |<psi|phi>|^2 via destructive interference
    qc.h(0)
    qc.cswap(0, 1, 2) 
    qc.h(0)
    qc.measure(0, 0)
    
    sim = AerSimulator()
    # Expectation value of the Ancilla Qubit (q0)
    counts = sim.run(transpile(qc, sim), shots=1024).result().get_counts()
    return counts.get('0', 0) / 1024

# Scrambled Data: Points representing distinct probability distributions
raw_data = [3.1, 0.1, 2.9, 0.3]
# Convergence Threshold: Similarity required for 'Neighborhood' inclusion
threshold = 0.85
clusters = []

print("--- Executing Autonomous Quantum Neighborhood Discovery ---")
for point in raw_data:
    placed = False
    for cluster in clusters:
        # Comparative Analysis against the Cluster Centroid
        if get_similarity(point, cluster[0]) > threshold:
            cluster.append(point)
            placed = True
            break
    if not placed:
        # Initializing a new Cluster Manifold
        clusters.append([point])

for i, cluster in enumerate(clusters):
    print(f"Cluster Manifold {i+1} localized: {cluster}")