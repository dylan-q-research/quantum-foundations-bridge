import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

def get_noisy_probability(theta, noise_level=0.03):
    qc = QuantumCircuit(1, 1)
    qc.ry(theta, 0)
    qc.measure(0, 0)
    
    # Create noise for the single-qubit gate
    noise_model = NoiseModel()
    error = depolarizing_error(noise_level, 1)
    noise_model.add_all_qubit_quantum_error(error, ['ry'])
    
    sim = AerSimulator(noise_model=noise_model)
    counts = sim.run(transpile(qc, sim), shots=1000).result().get_counts()
    return counts.get('1', 0) / 1000

# Training Parameters
target = 0.5
current_theta = 0.1
learning_rate = 0.6
iterations = 10

print(f"Training Noisy Neuron (3% Error) to Target P(1) = {target}")
for i in range(iterations):
    prob = get_noisy_probability(current_theta)
    error = target - prob
    current_theta += learning_rate * error
    print(f"Iteration {i+1}: P(1) = {prob:.3f}, Theta = {current_theta:.3f}")