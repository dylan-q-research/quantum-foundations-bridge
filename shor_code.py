from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# 1. Initialize a 1-qubit circuit with 1 classical bit for measurement
qc = QuantumCircuit(1, 1)

# 2. Apply Hadamard (H) gate
# This creates a coherent superposition: |psi> = 1/sqrt(2) (|0> + |1>)
qc.h(0)

# 3. Collapse the Wave-Function
# The universe makes a non-deterministic choice here.
qc.measure(0, 0)

# 4. Execute the simulation on your local Aer engine
sim = AerSimulator()
result = sim.run(qc, shots=1, memory=True).result()
flip = result.get_memory()[0]

# 5. Output the result
print("\n--- Quantum Coin Flip ---")
print(f"The Universe chose: {'HEADS (0)' if flip == '0' else 'TAILS (1)'}")
print("--------------------------\n")