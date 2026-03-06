"""
Research Project: Quantum Phase Estimation (QPE)
Researcher: Dylan Cabrera Giler
Objective: Implementing a precision phase-estimation protocol to derive 
the eigenvalues of a Unitary operator via the Inverse QFT.
"""

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def inverse_qft(n):
    """
    Constructs an Inverse Quantum Fourier Transform circuit.
    This acts as the 'decoder' for phase information stored in the Fourier basis.
    """
    qc = QuantumCircuit(n)
    for j in range(n//2):
        qc.swap(j, n-j-1)
    for j in range(n):
        for m in range(j):
            qc.cp(-np.pi/float(2**(j-m)), m, j)
        qc.h(j)
    return qc

# 3 Precision Qubits (Counting register) + 1 Target Qubit
n_count = 3
qpe = QuantumCircuit(n_count + 1, n_count)

# --- STEP 1: INITIALIZATION ---
# Prepare the target qubit in the |1> state (Eigenstate of the T-gate)
qpe.x(n_count)
for qubit in range(n_count):
    qpe.h(qubit)

# --- STEP 2: CONTROLLED UNITARY OPERATIONS ---
# Applying U^(2^j) where U is the T-gate (rotation by pi/4)
angle = 2 * np.pi / 8
for i in range(n_count):
    # Successive controlled rotations to encode the phase
    for _ in range(2**i):
        qpe.cp(angle, i, n_count)

# --- STEP 3: INVERSE QFT ---
qpe.barrier()
qpe.append(inverse_qft(n_count), range(n_count))
qpe.barrier()
qpe.measure(range(n_count), range(n_count))

# --- STEP 4: SIMULATION ---
sim = AerSimulator()
results = sim.run(transpile(qpe, sim), shots=1024).result().get_counts()

# Binary to Decimal conversion: 001 = 1/8 = 0.125
print(f"--- QPE Phase Discovery Results ---")
print(f"Measured Register States: {results}")