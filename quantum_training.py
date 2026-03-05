import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def get_probability(theta):
    qc = QuantumCircuit(1, 1)
    qc.ry(theta, 0)
    qc.measure(0, 0)
    sim = AerSimulator()
    counts = sim.run(transpile(qc, sim), shots=1000).result().get_counts()
    return counts.get('1', 0) / 1000

# Parameters
target = 0.5  # We want a 50/50 split
current_theta = 0.1  # Starting guess
learning_rate = 0.5
iterations = 10

print(f"Target Probability P(1): {target}")
print("-" * 30)

for i in range(iterations):
    prob = get_probability(current_theta)
    error = target - prob
    
    # Update theta based on the error (Gradient Descent)
    current_theta += learning_rate * error
    
    print(f"Iteration {i+1}: Theta = {current_theta:.3f}, P(1) = {prob:.3f}")

print("-" * 30)
print(f"Final trained Theta: {current_theta:.3f} (Expected ~1.57)")