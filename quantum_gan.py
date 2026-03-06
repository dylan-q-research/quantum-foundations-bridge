import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

sim = AerSimulator()

def generator(theta):
    qc = QuantumCircuit(1)
    qc.ry(theta, 0)
    return qc

def discriminator(target_qc, weight):
    # Combine the input state with the discriminator's logic
    qc = target_qc.copy()
    qc.ry(weight, 0)
    qc.measure_all()
    result = sim.run(transpile(qc, sim), shots=500).result().get_counts()
    # P(1) is the 'Probability of being Real'
    return result.get('1', 0) / 500

# Training params
g_theta, d_weight = 0.1, 0.1
lr = 0.2

print("--- Starting Quantum GAN Training ---")
for i in range(10):
    # 1. Train Discriminator: Distinguish Real (|1>) from Fake (G(theta))
    real_score = discriminator(generator(np.pi), d_weight) # Pi = |1>
    fake_score = discriminator(generator(g_theta), d_weight)
    
    # D wants real_score to be 1 and fake_score to be 0
    d_weight += lr * (real_score - fake_score)
    
    # 2. Train Generator: Fool the Discriminator
    # G wants fake_score to be 1
    g_theta += lr * (1.0 - fake_score)
    
    print(f"Epoch {i+1}: G_Theta={g_theta:.3f}, D_Score_on_Fake={fake_score:.3f}")