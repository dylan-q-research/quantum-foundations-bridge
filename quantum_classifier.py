from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import numpy as np

def classify_data(input_data, weight):
    qc = QuantumCircuit(1, 1)
    
    # 1. Feature Map: Encode classical data into the qubit
    qc.ry(input_data, 0)
    
    # 2. Ansatz: The 'Brain' of the classifier (Parametrized Layer)
    qc.ry(weight, 0)
    
    qc.measure(0, 0)
    sim = AerSimulator()
    counts = sim.run(transpile(qc, sim), shots=100).result().get_counts()
    
    # If the majority of shots are '1', we classify it as 'Class B'
    return 1 if counts.get('1', 0) > 50 else 0

# Test Data
data_points = [0.1, 3.1] # Low value vs High value
current_weight = 0.5

print("--- Quantum Classification Results ---")
for point in data_points:
    label = classify_data(point, current_weight)
    class_name = "High-Energy" if label == 1 else "Low-Energy"
    print(f"Input: {point} -> Classified as: {class_name}")