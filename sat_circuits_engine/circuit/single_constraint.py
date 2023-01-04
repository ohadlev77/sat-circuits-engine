from qiskit import QuantumCircuit, QuantumRegister

class SingleConstraintBlock(QuantumCircuit):
    """
    `SingleConstraintBlock` object - a circuit implementation of a single constraint equation.
    TODO IMPROVE
    """

    def __init__(self, c_index: int, c_eq: str, mpl: bool=True) -> None:
        """
        Args:
            c_index(int) - ID of constraint.
            c_qe(str) - Single constraint equation (see `constraints_format.txt` for format details).
            mpl(bool) - `True` for matplotlib circuit diagrams output, `False` for text output.
        """
        
        self.c_index = c_index
        self.c_eq = c_eq
        self.mpl = mpl

        self.parse_operator() # Setting of self.operator
        self.parse_sides() # Setting of self.right_side, and self.left_side
        self.calc_aux_needed() # Setting of self.aux_qubits_needed

        self.left_reg = QuantumRegister(self.len_left, 'left_reg')
        self.right_reg = QuantumRegister(self.len_right, 'right_reg')
        self.aux_reg = QuantumRegister(self.aux_qubits_needed, 'aux_reg')
        self.out = QuantumRegister(1, 'out')
        super().__init__(self.left_reg, self.right_reg, self.aux_reg, self.out)

        self.assemble()
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.c_eq}'): {self.__dict__}"
    
    def parse_operator(self) -> None:
        """
        Given a single constraint equation, this method parses its operator.
        """
        
        try:
            self.c_eq.index('==')
            self.operator = '=='
        except:
            try:
                self.c_eq.index('!=')
                self.operator = '!='
            except:
                raise ValueError('Only == and != operators are supported for now')
    
    def parse_sides(self) -> None:
        """
         Given a single constraint equation, this method parses the two sides of the equation
         according to the format (constraints_format.txt).
        """
                
        LR = self.c_eq.split(self.operator)
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
                    
    def calc_aux_needed(self) -> None:
        """
        Computes how many auxiliary qubits are needed to implement the given constraint equation.
        """
        
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
            self.name = f'Constraint {self.c_index}:\n{self.c_eq}'
        else:
            self.name = f'Constraint {self.c_index}'