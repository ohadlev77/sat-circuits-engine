'''
    This module contains all methods regarding the actual implementation of the circuit and its building blocks.
'''

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile, Aer

import parse

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