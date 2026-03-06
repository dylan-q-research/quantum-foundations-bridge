"""
Research Project: Quantum Generative Adversarial Network (QGAN)
Researcher: Dylan Cabrera Giler
Objective: Synchronous training of Generator and Discriminator circuits 
to reach a Nash Equilibrium in Quantum State Synthesis.
"""

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# Initialize AerSimulator for high-fidelity statevector emulation
sim = AerSimulator()

def generator(theta):
    """
    Parametrized Quantum Circuit (PQC) acting as the Generative model.
    Encodes a latent variable into a unitary rotation on the Bloch Sphere.
    """
    qc = QuantumCircuit(1)
    qc.ry(theta, 0) # Mapping theta to a specific probability amplitude
    return qc

def discriminator(target_qc, weight):
    """
    Evaluates the 'Fidelity' of the input state against the ground-truth |1>.
    Acts as a binary classifier in Hilbert Space.
    """
    qc = target_qc.copy()
    qc.ry(weight, 0) # Trainable measurement basis rotation
    qc.measure_all()
    
    # Extracting expectation values from shot-based measurement collapse
    result = sim.run(transpile(qc, sim), shots=500).result().get_counts()
    
    # Return P(1): The Discriminator's confidence that the state is 'Real'
    return result.get('1', 0) / 500

# Hyperparameters for Stochastic Gradient Descent (SGD)
g_theta, d_weight = 0.1, 0.1
learning_rate = 0.2

print("--- Initiating Adversarial Optimization Protocol ---")
for i in range(10):
    # 1. Discriminator Update: Maximizing classification accuracy between 
    # the target state |1> and the Generator's synthetic output.
    real_score = discriminator(generator(np.pi), d_weight) # Target: |1>
    fake_score = discriminator(generator(g_theta), d_weight)
    
    # Calculating the gradient of the binary cross-entropy loss
    d_weight += learning_rate * (real_score - fake_score)
    
    # 2. Generator Update: Minimizing the Discriminator's ability to 
    # distinguish synthetic states from the ground-truth.
    g_theta += learning_rate * (1.0 - fake_score)
    
    print(f"Epoch {i+1}: G_Theta={g_theta:.3f} | Convergence Metric: {fake_score:.3f}")