"""
TODO COMPLETE
"""

from typing import Optional
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

from .grover_constraints_operator import GroverConstraintsOperator
from .grover_diffuser import GroverDiffuser

class SAT_Circuit(QuantumCircuit):
    """
    Assembles an overall circuit for the given SAT problem from the building blocks:
        # Input state preparation.
        # Grover's iterator - consists of:
            * `GroverConstraintsOperator` object (Grover's operator).
            * `GroverDiffuser` object (Grover's diffuser).
        # Measurement.
    """

    def __init__(
        self,
        num_input_qubits: int,
        grover_constraints_operator: GroverConstraintsOperator,
        iterations: Optional[int] = None
    ) -> None:
        """
        Args:
            num_input_qubits(int) - the number of qubits in the input register.
            constraints(`GroverConstraintsOperator` object) - a child object of `QuantumCircuit` which is Grover's operator implementation
            for the specific constraints entered by the user.
            iterations (Optional[int]) - number of required iterations over Grover's iterator.
                # If `None` (default) - the number of iterations is unknown and a dynamic circuit approach
                should be applied.
        """

        # TODO COMPLETE
        self.num_input_qubits = num_input_qubits

        # Building blocks
        self.sat_op = grover_constraints_operator
        self.diffuser = GroverDiffuser(num_input_qubits)
        
        # Initializing Circuit
        self.input_reg = QuantumRegister(num_input_qubits, 'input_reg')
        self.aux_reg = QuantumRegister(self.sat_op.total_aux_qubits_needed, 'aux_reg')
        self.out_reg = QuantumRegister(self.sat_op.out_qubits_amount, 'out_reg')
        self.ancilla = QuantumRegister(1, 'ancilla')
        self.results = ClassicalRegister(num_input_qubits, 'results')

        # No `iterations` specified = dynamic circuit
        if iterations is None:
            self.probe = QuantumRegister(1, 'probe')
            self.probe_result = ClassicalRegister(1, 'probe_result')

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

            # TODO IMPROVE Applying dynamic while loop over Grover's iterator + weak measurement
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

            # Appending `iterations` iterations of the algorithm
            for _ in range(iterations):
                self.add_iteration()
        
        # TODO IS THIS COMMENT AND METHOD GOOD?
        # NOTE: We are not adding measurements now, in order to leave the number of iterations flexible

    def dynamic_loop(self) -> None:
        """
        TODO COMPLETE
        """

        # Condition for the while loop below
        condition = (self.probe_result, 0)

        # TODO CHANGE NAME
        body = assemble_grover_iterator(self.sat_op, self.diffuser, self.num_input_qubits)

        # TODO EXPLAIN
        qubits_with_ancilla = self.input_reg[:] + self.aux_reg[:] + self.out_reg[:] + self.ancilla[:]
        qubits_with_probe = self.input_reg[:] + self.aux_reg[:] + self.out_reg[:] + self.probe[:]

        # TODO EXPLAIN
        with self.while_loop(condition):
            self.append(body, qargs=qubits_with_ancilla)
            self.append(self.sat_op, qargs=qubits_with_probe)
            self.measure(self.probe, self.probe_result)

    def set_init_state(self) -> None:
        """
        Setting the input register to 2^n = N equal superposition of states
        and the ancilla to an eigenstate of the NOT gate: |->.
        """

        self.h(self.input_reg)
        self.x(self.ancilla)
        self.h(self.ancilla)
        self.barrier()
    
    def add_iteration(self) -> None:
        """
        Appends an iteration over Grover's iterator (`sat_op` + `diffuser`) to `self`.
        """

        self.append(self.sat_op, qargs=self.qubits[0:self.num_qubits])
        self.append(self.diffuser, qargs=self.input_reg)
        self.barrier()

    def add_input_reg_measurement(self) -> None:
        """
        Appends a final measurement of the input register to `self`.
        """

        self.measure(self.input_reg, self.results)

def assemble_grover_iterator(operator: QuantumCircuit, diffuser: QuantumCircuit, num_input_qubits: int) -> QuantumCircuit:
    """
    TODO COMPLETE
    """

    operator.append(diffuser, qargs=[qubit_index for qubit_index in range(num_input_qubits)])

    return operator
