#    Copyright 2022-2023 Ohad Lev.

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0,
#    or in the root directory of this package("LICENSE.txt").

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

"""
GroverDiffuser class.
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
        
        self.name = "Diffuser"
        self.to_gate()