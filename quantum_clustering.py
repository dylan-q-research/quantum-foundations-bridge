import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def get_similarity(x1, x2):
    qc = QuantumCircuit(3, 1)
    qc.ry(x1, 1)
    qc.ry(x2, 2)
    qc.h(0)
    qc.cswap(0, 1, 2)
    qc.h(0)
    qc.measure(0, 0)
    sim = AerSimulator()
    counts = sim.run(transpile(qc, sim), shots=1024).result().get_counts()
    return counts.get('0', 0) / 1024

# Unlabeled Data: Scrambled points
raw_data = [3.1, 0.1, 2.9, 0.3]
threshold = 0.85
clusters = []

print("--- Unsupervised Quantum Clustering ---")
for point in raw_data:
    placed = False
    for cluster in clusters:
        # Compare current point to the first point in each cluster
        if get_similarity(point, cluster[0]) > threshold:
            cluster.append(point)
            placed = True
            break
    if not placed:
        clusters.append([point])

# Output the discovered groups
for i, cluster in enumerate(clusters):
    print(f"Cluster {i+1} discovered: {cluster}")