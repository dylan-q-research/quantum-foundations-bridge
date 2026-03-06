"""
Title: NISQ-Era Depolarizing Noise Simulator
Researcher: Dylan Cabrera Giler
Objective: Characterize decoherence-induced bias in Quantum Circuits 
           using Stochastic Noise Modeling.
"""

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

class QuantumNoiseEngine:
    def __init__(self, p_error: float = 0.01):
        """
        Initialize a Noise Model representing gate-level decoherence.
        p_error: Probability of a depolarizing error occurring.
        """
        self.p_error = p_error
        self.noise_model = self._build_model()
        self.backend = AerSimulator(noise_model=self.noise_model)

    def _build_model(self):
        # 1-qubit gate error (e.g., Hadamard, Pauli-X)
        err_1 = depolarizing_error(self.p_error, 1)
        # 2-qubit gate error (CNOTs are physically more complex and noisier)
        err_2 = depolarizing_error(self.p_error * 10, 2)
        
        model = NoiseModel()
        model.add_all_qubit_quantum_error(err_1, ['h', 'x', 'u1', 'u2', 'u3'])
        model.add_all_qubit_quantum_error(err_2, ['cx'])
        return model

    def get_expectation_z(self, qc: QuantumCircuit):
        """Calculates the <Z> expectation value under noise."""
        qc.measure_all()
        t_qc = transpile(qc, self.backend)
        result = self.backend.run(t_qc, shots=1024).result()
        counts = result.get_counts()
        
        # Calculate <Z> = (Counts of 0 - Counts of 1) / Total Shots
        zero_counts = counts.get('00', 0) + counts.get('01', 0) # Focus on qubit 0
        one_counts = counts.get('10', 0) + counts.get('11', 0)
        return (zero_counts - one_counts) / 1024

if __name__ == "__main__":
    # Test Circuit: A simple rotation that should yield <Z> = 0.5
    test_circ = QuantumCircuit(1)
    test_circ.ry(np.pi/3, 0) 
    
    engine = QuantumNoiseEngine(p_error=0.05)
    noisy_val = engine.get_expectation_z(test_circ)
    
    print(f"--- Quantum Noise Engine Output ---")
    print(f"Simulated Error Rate: 5%")
    print(f"Measured Expectation <Z>: {noisy_val:.4f}")