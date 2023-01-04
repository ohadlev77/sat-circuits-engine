"""
TODO COMPLETE
"""

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
        iterations: int
    ) -> None:
        """
        Args:
            num_input_qubits(int) - the number of qubits in the input register.
            constraints(`GroverConstraintsOperator` object) - a child object of `QuantumCircuit` which is Grover's operator implementation
            for the specific constraints entered by the user.
            iterations(int) - number of required iterations over Grover's iterator.
        """

        # Building blocks
        self.sat_op = grover_constraints_operator
        self.diffuser = GroverDiffuser(num_input_qubits)
        
        # Initializing Circuit
        self.input_reg = QuantumRegister(num_input_qubits, 'input_reg')
        self.aux_reg = QuantumRegister(self.sat_op.total_aux_qubits_needed, 'aux_reg')
        self.out_reg = QuantumRegister(self.sat_op.out_qubits_amount, 'out_reg')
        self.ancilla = QuantumRegister(1, 'ancilla')
        self.results = ClassicalRegister(num_input_qubits, 'results')
        super().__init__(self.input_reg, self.aux_reg, self.out_reg, self.ancilla, self.results)

        # Initializing input state
        self.set_init_state()

        # Appending `iterations` iterations of the algorithm
        for i in range(iterations):
            self.add_iteration()
        
        # NOTE: We are not adding measurements now, in order to leave the number of iterations flexible

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

        self.append(self.sat_op, qargs=self.qubits)
        self.append(self.diffuser, qargs=self.input_reg)
        self.barrier()

    def add_input_reg_measurement(self) -> None:
        """
        Appends a final measurement of the input register to `self`.
        """

        self.measure(self.input_reg, self.results)