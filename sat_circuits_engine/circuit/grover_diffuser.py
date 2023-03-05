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

from typing import Optional
from qiskit import QuantumCircuit, QuantumRegister

class GroverDiffuser(QuantumCircuit):
    """
    Implementation of Grover's diffuser operator.
    """

    def __init__(self, num_input_qubits: int, num_ancilla_qubits: Optional[int] = 0) -> None:
        """
        Initializes a `QuantumCircuit` object.
        Implements the gate-combination needed for Grover's diffuser operator.

        Args:
            num_input_qubits (int): number of input qubits.
            num_ancilla_qubits (Optional[int] = 0): number of ancilla qubits available, for the
            purpose of decomposing the MCX gate needed for implementing Grover's diffuser, in
            an efficient and shallow-as-possible manner.
        """

        input_reg = QuantumRegister(num_input_qubits, "input_reg")
        ancilla_reg = QuantumRegister(num_ancilla_qubits, "ancilla_reg")
        super().__init__(input_reg, ancilla_reg, name="Diffuser")
        
        # Pre-settings. Choosing the shallowest possible MCX decomposing mode
        target_qubit = input_reg[num_input_qubits - 1]
        if num_ancilla_qubits == 0:
            mode = "noancilla"
        elif num_ancilla_qubits < num_input_qubits - 2:
            mode = "recursion"
        else:
            mode = "v-chain"

        # Diffuser implementation
        self.h(input_reg)
        self.x(input_reg)        
        self.h(target_qubit)
        self.mcx(
            control_qubits=input_reg[list(range(num_input_qubits - 1))],
            target_qubit=target_qubit,
            ancilla_qubits=ancilla_reg,
            mode=mode
        )
        self.h(target_qubit)
        self.x(input_reg)
        self.h(input_reg)