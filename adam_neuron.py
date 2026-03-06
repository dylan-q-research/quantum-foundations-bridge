"""
Research Project: Adaptive Moment Estimation (ADAM) in Noisy QML
Researcher: Dylan Cabrera Giler
Objective: Implementing a second-order stochastic optimizer to stabilize 
gradient descent in the presence of depolarizing quantum gate noise.
"""

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

def get_noisy_probability(theta):
    """
    Simulation of a Noisy Parametrized Quantum Circuit (PQC).
    Introduces 3% Depolarizing Error to emulate NISQ-era hardware decoherence.
    """
    qc = QuantumCircuit(1, 1)
    qc.ry(theta, 0) # Unitary rotation representing the 'Weight' of the neuron
    qc.measure(0, 0)
    
    # Stochastic Noise Model: Simulating Entropy Injection
    noise_model = NoiseModel()
    error = depolarizing_error(0.03, 1)
    noise_model.add_all_qubit_quantum_error(error, ['ry'])
    
    sim = AerSimulator(noise_model=noise_model)
    # Measurement collapse across 1000 shots to derive expectation value
    counts = sim.run(transpile(qc, sim), shots=1000).result().get_counts()
    return counts.get('1', 0) / 1000

# --- ADAM Hyperparameters: The 'Control System' for Optimization ---
target, theta = 0.5, 0.1
alpha = 0.1         # Step size (Learning Rate)
beta1 = 0.9         # Decay rate for First Moment (Mean Gradient)
beta2 = 0.999       # Decay rate for Second Moment (Uncentered Variance)
m, v = 0, 0         # Moment vectors (Homeostasis initialization)
epsilon = 1e-8      # Numerical stability constant

print(f"--- Initiating ADAM Optimization: Target P(1) = {target} ---")
for i in range(1, 11):
    prob = get_noisy_probability(theta)
    grad = target - prob # Calculating the Error Signal (The Gradient)
    
    # Update Momentum (m) and Scaling (v)
    m = beta1 * m + (1 - beta1) * grad
    v = beta2 * v + (1 - beta2) * (grad**2)
    
    # Bias Correction: Compensating for the initial 0-state 'Cold Start'
    m_hat = m / (1 - beta1**i)
    v_hat = v / (1 - beta2**i)
    
    # Weight Update: θ = θ + α * (m_hat / (sqrt(v_hat) + ε))
    # This acts as a 'Precision-Weighted' update to mitigate stochastic jitter.
    theta += alpha * (m_hat / (np.sqrt(v_hat) + epsilon))
    
    print(f"Iteration {i}: Expectation Value P(1)={prob:.3f} | Adjusted Theta={theta:.3f}")