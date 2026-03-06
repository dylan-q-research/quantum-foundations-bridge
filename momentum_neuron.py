import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

def get_noisy_probability(theta):
    qc = QuantumCircuit(1, 1)
    qc.ry(theta, 0)
    qc.measure(0, 0)
    noise_model = NoiseModel()
    noise_model.add_all_qubit_quantum_error(depolarizing_error(0.03, 1), ['ry'])
    sim = AerSimulator(noise_model=noise_model)
    counts = sim.run(transpile(qc, sim), shots=1000).result().get_counts()
    return counts.get('1', 0) / 1000

# Momentum Parameters
target = 0.5
theta = 0.1
learning_rate = 0.4
beta = 0.8  # The "Momentum" factor (0.0 to 1.0)
velocity = 0

print(f"Training with Momentum (Beta={beta}) to Target P(1) = {target}")
for i in range(10):
    prob = get_noisy_probability(theta)
    gradient = target - prob
    
    # Update Velocity: V = (Beta * V) + (Learning_Rate * Gradient)
    velocity = (beta * velocity) + (learning_rate * gradient)
    theta += velocity
    
    print(f"Iteration {i+1}: P(1) = {prob:.3f}, Theta = {theta:.3f}, Velocity = {velocity:.3f}")