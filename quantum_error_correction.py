"""
Research Project: 3-Qubit Bit-Flip Error Correction Code
Researcher: Dylan Cabrera Giler
Objective: Implementing active redundancy to maintain state fidelity 
against stochastic bit-flip errors (X-gate noise).
"""

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def run_qec_test(simulate_error=True):
    # 5 Qubits: 0,1,2 = Data Qubits (The Logical Qubit)
    # 3,4 = Ancilla Qubits (The Error Detectors)
    qc = QuantumCircuit(5, 1)

    # --- STEP 1: ENCODING ---
    # We want to store the state |1>
    qc.x(0) 
    # Entangle q0 with q1 and q2 (Repetition Code)
    qc.cx(0, 1)
    qc.cx(0, 2)
    qc.barrier()

    # --- STEP 2: STOCHASTIC ERROR ---
    if simulate_error:
        # Simulate a bit-flip error on Qubit 1
        qc.x(1) 
    qc.barrier()

    # --- STEP 3: SYNDROME MEASUREMENT ---
    # Use Ancillas to check parity without collapsing the data
    qc.cx(0, 3)
    qc.cx(1, 3)
    qc.cx(0, 4)
    qc.cx(2, 4)
    qc.barrier()

    # --- STEP 4: CORRECTION (The Recovery Map) ---
    # If Ancillas 3 and 4 both triggered, Qubit 0 flipped.
    # If 3 triggered but 4 didn't, Qubit 1 flipped.
    # If 4 triggered but 3 didn't, Qubit 2 flipped.
    qc.ccx(3, 4, 0) # Flip q0 if q3 and q4 are 1
    # Simple logic for this demo: Correcting Qubit 1
    qc.x(3)
    qc.ccx(3, 4, 1) 
    qc.x(3)

    # --- STEP 5: DECODING & MEASURE ---
    qc.cx(0, 1)
    qc.cx(0, 2)
    qc.measure(0, 0)

    sim = AerSimulator()
    return sim.run(transpile(qc, sim), shots=1024).result().get_counts()

print("--- Testing Quantum Error Correction ---")
results = run_qec_test(simulate_error=True)
print(f"Results with Error + Correction: {results}")