'''
    This module contains all methods regarding the parsing of the constraints as defined by the user, and their derived computations.
'''

import numpy as np

from qiskit import QuantumCircuit, transpile, Aer, QuantumRegister, ClassicalRegister
import circuit

class Constraints:
    '''
        TODO COMPLETE
    '''
    
    def __init__(self, constraints_string):
        self.constraints_string = constraints_string
        self.constraints_list = constraints_string.split(",")
        
        self.constraints = []
        for c_index, c in enumerate(self.constraints_list):
            self.constraints.append(Constraint(c_index = c_index, c_eq = c))
            
    def __repr__(self):
        return f"Constraints('{self.constraints_string}')"

class Constraint:
    '''
        TODO COMPLETE
    '''

    # Class attributes
    count = 0
    
    def __init__(self, c_index, c_eq):
        self.c_index = c_index
        self.c_eq = c_eq
        self.parse_operator() # Setting of self.operator
        self.parse_sides() # Setting of self.right_side, and self.left_side
        self.calc_aux_needed() # Setting of self.aux_qubits_needed
    
    def __repr__(self):
        return f"Constraint('{self.c_eq}'): {self.__dict__}"
    
    def parse_operator(self):
        try:
            self.c_eq.index('==')
            self.operator = '=='
        except:
            try:
                self.c_eq.index('!=')
                self.operator = '!='
            except:
                raise ValueError('Only == and != operators are supported for now')
    
    def parse_sides(self):
        LR = self.c_eq.split(self.operator)
        self.left_side = []
        self.right_side = []
        
        for side_num, side in enumerate(LR):
            i = 0
            while side.find('[',i) != -1:
                i = side.find('[',i) + 1
                ie = side.find(']',i)
                q_i = int(side[i:ie])
                
                # Isolating and appending the qubit index
                if side_num == 0:
                    self.left_side.append(q_i)
                elif side_num == 1:
                    self.right_side.append(q_i)
                    
    def calc_aux_needed(self):
        len_left = len(self.left_side)
        len_right = len(self.right_side)
        min_len = min(len_left, len_right)

        # Case 1 - 1 qubit from each side = No auxiliary qubits needed
        if len_left == 1 and len_right == 1:
            amount = 0        
        #Case 2 - More than 1 qubit from either of the sides
        else:
            amount = min_len
            if len_left != len_right: # Case 2.A - non-equal amount of qubits between sides
                amount += 1

        self.aux_qubits_needed = amount