"""
Research Project: 3-Qubit Phase-Flip Error Correction Code
Researcher: Dylan Cabrera Giler
Objective: Implementing a Phase-Repetition code to protect against 
Z-axis decoherence using Basis Transformation (H-gates).
"""

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def run_phase_qec():
    # 3 Qubits for the logical state
    qc = QuantumCircuit(3, 1)

    # --- STEP 1: ENCODING ---
    # Prepare the |+> state and entangle
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(0, 2)
    
    # Transform to the X-basis (The 'Phase' Protection)
    qc.h([0, 1, 2])
    qc.barrier()

    # --- STEP 2: STOCHASTIC PHASE ERROR ---
    # Simulate a Z-error (Phase flip) on Qubit 0
    qc.z(0) 
    qc.barrier()

    # --- STEP 3: RECOVERY ---
    # Transform back from X-basis to Z-basis to reveal the error
    qc.h([0, 1, 2])
    
    # Majority Vote Logic (Simplified for 3 qubits)
    qc.cx(0, 1)
    qc.cx(0, 2)
    qc.ccx(2, 1, 0)
    
    qc.measure(0, 0)

    sim = AerSimulator()
    return sim.run(transpile(qc, sim), shots=1024).result().get_counts()

print("--- Testing Phase-Flip Error Correction ---")
results = run_phase_qec()
print(f"Phase-Flip Recovery Results: {results}")