import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def quantum_kernel_entry(x1, x2):
    """Calculates the similarity between two data points in Hilbert Space"""
    qc = QuantumCircuit(3, 1)
    
    # Encode Feature 1 into Qubit 1
    qc.ry(x1, 1)
    # Encode Feature 2 into Qubit 2
    qc.ry(x2, 2)
    
    # Swap Test (The Kernel)
    qc.h(0)
    qc.cswap(0, 1, 2)
    qc.h(0)
    qc.measure(0, 0)
    
    sim = AerSimulator()
    result = sim.run(transpile(qc, sim), shots=1024).result()
    # High '0' count = High Similarity
    return result.get_counts().get('0', 0) / 1024

# Data: Two distinct classes (Low Energy vs High Energy)
class_a = [0.2, 0.4] 
class_b = [2.8, 3.0]

print("--- Quantum SVM Kernel Matrix (Partial) ---")
# Compare a point to itself (Should be 1.0)
print(f"Self-Similarity (A1, A1): {quantum_kernel_entry(class_a[0], class_a[0]):.3f}")
# Compare two points in the same class (Should be High)
print(f"Intra-Class Similarity (A1, A2): {quantum_kernel_entry(class_a[0], class_a[1]):.3f}")
# Compare points in different classes (Should be Low)
print(f"Inter-Class Similarity (A1, B1): {quantum_kernel_entry(class_a[0], class_b[0]):.3f}")