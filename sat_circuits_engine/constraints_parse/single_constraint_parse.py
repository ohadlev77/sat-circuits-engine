"""
TODO COMPLETE
"""

class SingleConstraintParsed:
    """
    TODO COMPLETE
    """

    def __init__(self, constraint_equation: str, constraint_index: int) -> None:
        """
        Args:
            constraint_index (int): the index number of the constraint.
            constraint_equation (str): single constraint equation string.
                # See `/interface/constraints_format.txt` for format details.
        """
        
        self.constraint_equation = constraint_equation
        self.constraint_index = constraint_index

        # TODO COMPLETE
        self.parse_operator() # Setting of self.operator
        self.parse_sides() # Setting of self.right_side, and self.left_side
        self.calc_aux_qubits_needed() # Setting of self.aux_qubits_needed
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.constraint_equation}')"
    
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
                raise ValueError('Only == and != operators are supported for now.')
    
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