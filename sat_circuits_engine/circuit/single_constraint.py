"""
TODO COMPLETE
"""

from qiskit import QuantumCircuit, QuantumRegister

class SingleConstraintBlock(QuantumCircuit):
    """
    `SingleConstraintBlock` object - a circuit implementation of a single constraint equation.
    To be integrated as a block in a `GroverConstriantsOperator` object.
    """

    def __init__(self, constraint_index: int, constraint_equation: str, mpl: bool=True) -> None:
        """
        Args:
            constraint_index (int): the index number of the constraint.
            constraint_equation (str): single constraint equation string.
                # See `interface/constraints_format.txt` for format details.
            mpl (bool): `True` for matplotlib circuit diagrams output, `False` for text output.
        """
        
        self.constraint_index = constraint_index
        self.constraint_equation = constraint_equation
        self.mpl = mpl

        # TODO COMPLETE
        self.parse_operator() # Setting of self.operator
        self.parse_sides() # Setting of self.right_side, and self.left_side
        self.calc_aux_qubits_needed() # Setting of self.aux_qubits_needed

        # Initializing Circuit
        self.left_reg = QuantumRegister(self.len_left, 'left_reg')
        self.right_reg = QuantumRegister(self.len_right, 'right_reg')
        self.aux_reg = QuantumRegister(self.aux_qubits_needed, 'aux_reg')
        self.out = QuantumRegister(1, 'out')
        super().__init__(self.left_reg, self.right_reg, self.aux_reg, self.out)

        # TODO COMPLETE
        self.assemble()
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.constraint_equation}'): {self.__dict__}"
    
    def parse_operator(self) -> None:
        """
        Given a single constraint equation, this method parses its operator,
        and saves it to the instance variable - `self.operator` (str).

        Raises:
            ValueError: if the operator parsed from `self.constraint_equation` is not '==' or '!='.
        """
        
        try:
            self.constraint_equation.index('==')
            self.operator = '=='
        except:
            try:
                self.constraint_equation.index('!=')
                self.operator = '!='
            except:
                raise ValueError('Only == and != operators are supported for now')
    
    def parse_sides(self) -> None:
        """
         Given a single constraint equation, this method parses the two sides of the equation,
         according to the format (constraints_format.txt).

         Defines the instance varaibles:
            `self.left_side` (List[int]): a list of indexes of qubits from the left
            side of `constraint_equation`.
            `self.right_side` (List[int]): a list of indexes of qubits from the right
            side of `constraint_equation`.

        """
                
        # TODO NEED TO BETTER ANNOTATE THIS METHOD

        LR = self.constraint_equation.split(self.operator)
        self.left_side = []
        self.right_side = []
        
        for side_num, side in enumerate(LR):
            i = 0
            while side.find('[', i) != -1:
                i = side.find('[', i) + 1
                ie = side.find(']', i)
                q_i = int(side[i:ie])
                
                # Isolating and appending the qubit index
                if side_num == 0:
                    self.left_side.append(q_i)
                elif side_num == 1:
                    self.right_side.append(q_i)
                    
    def calc_aux_qubits_needed(self) -> None:
        """
        Computes how many auxiliary qubits are needed to implement the given constraint equation,
        and saves the result to `self.aux_qubits_needed` (int).
        """
        
        #TODO DO WE NEED ALL THIS INSTANCE VARS? IF YES, NEED TO DOCUMENT

        self.len_left = len(self.left_side)
        self.len_right = len(self.right_side)
        self.min_len = min(self.len_left, self.len_right)
        self.max_len = max(self.len_left, self.len_right)

        # Case 1 - 1 qubit from each side = No auxiliary qubits needed
        if self.len_left == 1 and self.len_right == 1:
            self.aux_qubits_needed = 0

        #Case 2 - More than 1 qubit from either of the sides
        else:
            self.aux_qubits_needed = self.min_len
            if self.len_left != self.len_right: # Case 2.A - non-equal amount of qubits between sides
                self.aux_qubits_needed += 1

    def assemble(self) -> None:
        """
        # TODO MODIFY
        Assembles all the data gathered using the other methods of this class into a circuit implementation.
        Computes the specific setting of gates needed to implement the given constraint.
        """
                
        # Case 1 - no auxiliary qubits
        if self.aux_qubits_needed == 0:
            self.cx(self.left_reg, self.out)
            self.cx(self.right_reg, self.out)
            if self.operator == '==':
                self.x(self.out)
                   
        # Case 2 - with auxiliary qubits
        else:
            for i in range(self.min_len):
                self.cx(self.left_reg[i], self.aux_reg[i])
                self.cx(self.right_reg[i], self.aux_reg[i])
                self.x(self.aux_reg[i])
            
            #Case 2A - Different amount of qubits in left and right regs
            if self.len_left != self.len_right:
                if self.len_left > self.len_right:
                    diff = self.left_reg[self.min_len : self.max_len]
                else:
                    diff = self.right_reg[self.min_len : self.max_len]
                self.x(diff)
                self.mcx(diff, self.aux_reg[self.aux_qubits_needed - 1])
                self.x(diff)
            
            # Writing the overall combined result to the out qubit
            if self.operator == '!=':
                self.x(self.out)
            self.mcx(self.aux_reg, self.out)

        if self.mpl:
            self.name = f'Constraint {self.constraint_index}:\n{self.constraint_equation}'
        else:
            self.name = f'Constraint {self.constraint_index}'