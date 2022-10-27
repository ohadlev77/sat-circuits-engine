"""
Contains all building blocks for constructing the overall circuit for the problem.
"""

import numpy as np
from qiskit import QuantumCircuit, transpile, Aer, QuantumRegister, ClassicalRegister

class Constraints(QuantumCircuit):
    """
    Constraints object - turns constraints_string to a QuantumCircuit.
    """
    def __init__(self, constraints_string, n, mpl=True):
        """
        Parameters:
            constraints(str) - a string that describes a set of boolean arithmetic constraints written in a specific format.
                                # A full explanation regarding the format is provided in the file `constraints_format.txt`.
            n(int) - number of qubits.
        """

        self.n = n
        self.constraints_string = constraints_string
        self.constraints_list = constraints_string.split(",")
        self.mpl = mpl
        
        self.constraints = []
        self.total_aux_qubits_needed = 0
        self.aux_qubits_needed_list = []
        for c_index, c in enumerate(self.constraints_list):
            self.constraints.append(Constraint(c_index = c_index, c_eq = c, mpl=mpl))
            self.total_aux_qubits_needed += self.constraints[c_index].aux_qubits_needed
            self.aux_qubits_needed_list.append(self.constraints[c_index].aux_qubits_needed)
        self.out_qubits_amount = len(self.constraints)

        self.input_reg = QuantumRegister(self.n, 'input_reg')
        self.aux_reg = QuantumRegister(self.total_aux_qubits_needed, 'aux_reg')
        self.out_reg = QuantumRegister(self.out_qubits_amount, 'out_reg')
        self.ancilla = QuantumRegister(1, 'ancilla')
        super().__init__(self.input_reg, self.aux_reg, self.out_reg, self.ancilla)
            
        self.assemble()

    def __repr__(self):
        return f"Constraints('{self.constraints_string}')"

    def assemble(self):
        """
        Assembles Grover's operator.
        """

        # Handling constraints.
        for c in self.constraints:
            i = c.c_index # Constraint's index.
                    
            # Defining the qargs before appending c.
            if c.aux_qubits_needed == 0:
                qargs = self.input_reg[c.left_side] + self.input_reg[c.right_side] + [self.out_reg[i]]
                # Format: [left, right, out]
            else:
                aux_bottom = sum(self.aux_qubits_needed_list[0:i])
                aux_top = aux_bottom + self.aux_qubits_needed_list[i]
                qargs = self.input_reg[c.left_side] + self.input_reg[c.right_side] + self.aux_reg[aux_bottom : aux_top] + [self.out_reg[i]] 
                # Format: [left, right, aux, out].
            
            self.append(instruction = c, qargs = qargs)
            self.barrier()
        
        # Saving all actions until now for uncomputation.
        qc_dagger = self.inverse()
        qc_dagger.name = 'Uncomputation'
        
        # If all terms met, applying NOT to the ancilla (which is in the eigenstate |-> beforehand).
        self.mcx(control_qubits = self.out_reg, target_qubit = self.ancilla)
        
        # Uncomputation.
        self.append(instruction = qc_dagger, qargs = self.qubits)
        
        self.name = 'Operator'

class Constraint(QuantumCircuit):
    """
    Constraint object - turns a single constraint equation into a QuantumCircuit (a constraint operator).
    """
    def __init__(self, c_index, c_eq, mpl=True):
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

    def assemble(self):
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

class SAT_Circuit(QuantumCircuit):

    def __init__(self, n, constraints, iterations):
        # Building blocks
        self.sat_op = constraints
        self.diffuser = DiffuserOp(n)
        
        # Initializing Circuit
        self.input_reg = QuantumRegister(n, 'input_reg')
        self.aux_reg = QuantumRegister(self.sat_op.total_aux_qubits_needed, 'aux_reg')
        self.out_reg = QuantumRegister(self.sat_op.out_qubits_amount, 'out_reg')
        self.ancilla = QuantumRegister(1, 'ancilla')
        self.results = ClassicalRegister(n, 'results')
        super().__init__(self.input_reg, self.aux_reg, self.out_reg, self.ancilla, self.results)

        # Initializing input state
        self.set_init_state()

        # Appending `iterations` iterations of the algorithm
        for i in range(iterations):
            self.add_iteration()
        
        # NOTE: We are not adding measurements now, in oreder to leave the number of iterations flexible

    def set_init_state(self):
        # Setting the input register to 2^n = N equal superposition of states
        # and the ancilla to an eigenstate of the NOT gate: |->
        self.h(self.input_reg)
        self.x(self.ancilla)
        self.h(self.ancilla)
        self.barrier()
    
    def add_iteration(self):
        self.append(self.sat_op, qargs = self.qubits)
        self.append(self.diffuser, qargs = self.input_reg)
        self.barrier()

    def add_input_reg_measurement(self):
        self.measure(self.input_reg, self.results)

class DiffuserOp(QuantumCircuit):
    def __init__(self, n):
        super().__init__(n)
        
        self.h(self.qubits)
        self.x(self.qubits)
        self.mcp(np.pi, control_qubits = [q for q in range(n - 1)], target_qubit = n - 1)    
        self.x(self.qubits)
        self.h(self.qubits)
        
        self.name = 'Diffuser'
        self.to_gate()
