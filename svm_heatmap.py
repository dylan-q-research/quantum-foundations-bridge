import numpy as np
import matplotlib.pyplot as plt
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

# 4 Data Points: 2 from Class A, 2 from Class B
data = [0.2, 0.4, 2.8, 3.0]
matrix = np.zeros((4, 4))

print("Calculating 4x4 Quantum Kernel Matrix...")
for i in range(4):
    for j in range(4):
        matrix[i, j] = get_similarity(data[i], data[j])

# Visualize as Heatmap
plt.imshow(matrix, cmap='viridis', interpolation='nearest')
plt.colorbar(label='Quantum Similarity')
plt.title('Quantum SVM Kernel Heatmap')
plt.xticks(range(4), ['A1', 'A2', 'B1', 'B2'])
plt.yticks(range(4), ['A1', 'A2', 'B1', 'B2'])
plt.show()