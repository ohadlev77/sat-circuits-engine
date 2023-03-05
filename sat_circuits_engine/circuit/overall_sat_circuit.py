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
SATCircuit class.
"""

from typing import Optional

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

from sat_circuits_engine.circuit.grover_constraints_operator import GroverConstraintsOperator
from sat_circuits_engine.circuit.grover_diffuser import GroverDiffuser

class SATCircuit(QuantumCircuit):
    """
    Assembles an overall circuit for the given SAT problem from the building blocks:
        - Input state preparation.
        - Grover's iterator - consists of:
            * `GroverConstraintsOperator` object (Grover's operator).
            * `GroverDiffuser` object (Grover's diffuser).
        - Measurement.
    """

    def __init__(
        self,
        num_input_qubits: int,
        grover_constraints_operator: GroverConstraintsOperator,
        iterations: Optional[int] = None,
        insert_barriers: Optional[bool] = True
    ) -> None:
        """
        Args:
            num_input_qubits (int): the number of qubits in the input register.
            grover_constraints_operator (GroverConstraintsOperator): a child object of `QuantumCircuit`
            which is Grover's operator implementation for the specific constraints entered by the user.
            iterations (Optional[int] = None): number of required iterations over Grover's iterator.
                # If `None` (default) - the number of iterations is unknown and a dynamic
                circuit approach should be applied (TODO THIS IS A FUTURE FEATURE).
            insert_barriers (Optional[bool] = True): if True, barriers will be inserted
            to separate between segments and iterations.
        """

        self.num_input_qubits = num_input_qubits
        self.operator = grover_constraints_operator
        self.iterations = iterations
        self.insert_barriers = insert_barriers

        # Total number of auxiliary qubits (of all kinds)
        self.total_aux_width = (
            self.operator.comparison_aux_width +
            self.operator.left_aux_width +
            self.operator.right_aux_width
        )

        self.input_reg = QuantumRegister(num_input_qubits, "input_reg")
        self.aux_reg = QuantumRegister(self.total_aux_width, "aux_reg")
        self.out_reg = QuantumRegister(self.operator.out_qubits_amount, "out_reg")
        self.ancilla = QuantumRegister(1, "ancilla")
        self.results = ClassicalRegister(num_input_qubits, "results")

        # Input, auxiliary and out Qubit objects stacked in one list
        self.input_aux_out_qubits = (
            self.input_reg[:] +
            self.aux_reg[:] +
            self.out_reg[:]
        )

        self.diffuser = GroverDiffuser(
            num_input_qubits=num_input_qubits,
            num_ancilla_qubits=len(self.input_aux_out_qubits) - num_input_qubits
        )

        # No `iterations` specified = dynamic circuit
        # TODO this feature is not supported yet and shouldn't be used
        if iterations is None:

            # Register to apply weak measurements with
            self.probe = QuantumRegister(1, "probe")
            self.probe_result = ClassicalRegister(1, "probe_result")

            super().__init__(
                self.input_reg,
                self.aux_reg,
                self.out_reg,
                self.ancilla,
                self.probe,
                self.results,
                self.probe_result
            )

            # Initializing input state
            self.set_init_state()

            # Applying dynamic while loop over Grover's iterator coditioned by `probe`
            self.dynamic_loop()
            
        # `iterations` specified = static circuit
        else:
            super().__init__(
                self.input_reg,
                self.aux_reg,
                self.out_reg,
                self.ancilla,
                self.results,
            )

            # Initializing input state
            self.set_init_state()

            # Appending `iterations` iterations over Grover's iterator
            for _ in range(iterations):
                self.add_iteration()

    def dynamic_loop(self) -> None:
        """
        TODO this feature is not supported yet and shouldn't be used.
        """

        condition = (self.probe_result, 0)
        qargs_with_probe = self.input_aux_out_qubits[:] + self.probe[:]

        with self.while_loop(condition):
            self.append(self.diffuser, qargs=self.input_aux_out_qubits)
            self.add_iteration()
            self.append(self.operator, qargs=qargs_with_probe)
            self.measure(self.probe, self.probe_result)

    def set_init_state(self) -> None:
        """
        Setting the input register to 2^(self.num_input_qubits) = N equal superposition of states,
        and the ancilla to an eigenstate of the NOT gate: |->.
        """

        self.h(self.input_reg)

        self.x(self.ancilla)
        self.h(self.ancilla)

        if self.insert_barriers:
            self.barrier()
    
    def add_iteration(self) -> None:
        """
        Appends an iteration over Grover's iterator (`operator` + `diffuser`) to `self`.
        """

        qargs_with_ancilla = self.input_aux_out_qubits[:] + self.ancilla[:]

        self.append(self.operator, qargs=qargs_with_ancilla)
        self.append(self.diffuser, qargs=self.input_aux_out_qubits)

        if self.insert_barriers:
            self.barrier()

    def add_input_reg_measurement(self) -> None:
        """
        Appends a final measurement of the input register to `self`.
        """

        self.measure(self.input_reg, self.results)