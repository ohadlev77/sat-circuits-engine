"""
TODO COMPLETE
"""

import numpy as np
from qiskit import QuantumCircuit

class GroverDiffuser(QuantumCircuit):
    """
    Implementation of Grover's diffuser operator.
    """

    def __init__(self, num_input_qubits: int) -> None:
        """
        Initializes a `QuantumCircuit` object.
        Implements the gate-combination needed for Grover's diffuser operator.

        Args:
            num_input_qubits (int): number of input qubits.
        """

        super().__init__(num_input_qubits)
        
        self.h(self.qubits)
        self.x(self.qubits)

        self.mcp(
            np.pi,
            control_qubits=[q for q in range(num_input_qubits - 1)],
            target_qubit=num_input_qubits - 1
        )

        self.x(self.qubits)
        self.h(self.qubits)
        
        self.name = 'Diffuser'
        self.to_gate() # TODO DECIDE