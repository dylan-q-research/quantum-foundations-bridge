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

# ADAM Parameters
target, theta = 0.5, 0.1
learning_rate = 0.1
beta1, beta2 = 0.9, 0.999 # Standard ADAM defaults
m, v = 0, 0 # First and second moments
epsilon = 1e-8 # Prevents division by zero

print(f"Training with ADAM Optimizer to Target P(1) = {target}")
for i in range(1, 11):
    prob = get_noisy_probability(theta)
    grad = target - prob
    
    # Update Moments
    m = beta1 * m + (1 - beta1) * grad
    v = beta2 * v + (1 - beta2) * (grad**2)
    
    # Bias Correction (Crucial for early iterations)
    m_hat = m / (1 - beta1**i)
    v_hat = v / (1 - beta2**i)
    
    # Update Theta: theta = theta + alpha * (m_hat / (sqrt(v_hat) + eps))
    theta += learning_rate * (m_hat / (np.sqrt(v_hat) + epsilon))
    
    print(f"Iteration {i}: P(1) = {prob:.3f}, Theta = {theta:.3f}")