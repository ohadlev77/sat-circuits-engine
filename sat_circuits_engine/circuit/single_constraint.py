"""
TODO COMPLETE
"""

from qiskit import QuantumCircuit, QuantumRegister

from sat_circuits_engine.constraints_parse import SingleConstraintParsed

class SingleConstraintBlock(QuantumCircuit):
    """
    `SingleConstraintBlock` object - a circuit implementation of a single constraint equation.
    To be integrated as a block in a `GroverConstriantsOperator` object.
    """

    def __init__(self, parsed_single_constraint: SingleConstraintParsed, mpl: bool=True) -> None:
        """
        Args:
            constraint_index (int): the index number of the constraint.
            constraint_equation (str): single constraint equation string.
                # See `/interface/constraints_format.txt` for format details.
            mpl (bool): `True` for matplotlib circuit diagrams output, `False` for text output.
        """
        
        self.parsed_single_constraint = parsed_single_constraint
        self.mpl = mpl

        # Initializing Circuit
        self.left_reg = QuantumRegister(self.parsed_single_constraint.len_left, 'left_reg')
        self.right_reg = QuantumRegister(self.parsed_single_constraint.len_right, 'right_reg')
        self.aux_reg = QuantumRegister(self.parsed_single_constraint.aux_qubits_needed, 'aux_reg')
        self.out = QuantumRegister(1, 'out')
        super().__init__(self.left_reg, self.right_reg, self.aux_reg, self.out)

        # TODO COMPLETE
        self.assemble()
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}" \
               f"('{self.parsed_single_constraint.constraint_equation}'): {self.__dict__}"
    
    
    def assemble(self) -> None:
        """
        # TODO MODIFY
        Assembles all the data gathered using the other methods of this class into a circuit implementation.
        Computes the specific setting of gates needed to implement the given constraint.
        """
                
        # Case 1 - no auxiliary qubits
        if self.parsed_single_constraint.aux_qubits_needed == 0:
            self.two_qubits_equality()
                   
        # Case 2 - with auxiliary qubits
        # TODO MODULE THIS TO ANOTHER METHOD
        else:
            reversed_left_reg = list(reversed(self.left_reg))
            reversed_right_reg = list(reversed(self.right_reg))

            for i in range(self.parsed_single_constraint.min_len):
                self.cx(reversed_left_reg[i], self.aux_reg[i])
                self.cx(reversed_right_reg[i], self.aux_reg[i])
                self.x(self.aux_reg[i])
            
            #Case 2A - Different amount of qubits in left and right regs
            if self.parsed_single_constraint.len_left != self.parsed_single_constraint.len_right:
                if self.parsed_single_constraint.len_left > self.parsed_single_constraint.len_right:
                    diff = reversed_left_reg[self.parsed_single_constraint.min_len:self.parsed_single_constraint.max_len]
                else:
                    diff = reversed_right_reg[self.parsed_single_constraint.min_len:self.parsed_single_constraint.max_len]

                self.x(diff)
                # TODO HANDLE THIS FLAG
                if len(diff) == 2:
                    self.rccx(diff[0], diff[1], self.aux_reg[self.parsed_single_constraint.aux_qubits_needed - 1])
                else:
                    self.mcx(diff, self.aux_reg[self.parsed_single_constraint.aux_qubits_needed - 1])
                self.x(diff)
            
            # Writing the overall combined result to the out qubit
            if self.parsed_single_constraint.operator == '!=':
                self.x(self.out)
            
            # TODO HANDLE THIS FLAG
            if len(self.aux_reg) == 2:
                self.rccx(self.aux_reg[0], self.aux_reg[1], self.out)
            else:
                self.mcx(self.aux_reg, self.out)

        # TODO BETTER WAY?
        if self.mpl:
            self.name = f'Constraint {self.parsed_single_constraint.constraint_index}:\n{self.parsed_single_constraint.constraint_equation}'
        else:
            self.name = f'Constraint {self.parsed_single_constraint.constraint_index}'

    def two_qubits_equality(self):
        """
        TODO COMPLETE
        """

        self.cx(self.left_reg, self.out)
        self.cx(self.right_reg, self.out)

        if self.parsed_single_constraint.operator == '==':
            self.x(self.out)