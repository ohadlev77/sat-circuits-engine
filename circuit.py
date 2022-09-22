'''
    This module contains all methods regarding the actual implementation of the circuit and its building blocks.
'''

import numpy as np
from qiskit import QuantumCircuit, transpile, Aer, QuantumRegister, ClassicalRegister

import parse

def ComputeConstraint(left_qubits_amount, right_qubits_amount, aux_qubits_amount, operator):
    '''
        Functionality:
            This function implements the necessary gates set for a single constraint.
        Parameters:
            left_qubits_amount (int) - amount of qubits in the left side of the constraint equation.
            right_qubits_amount (int) - amount of qubits in the right side of the constraint equation.
            aux_qubits_amount (int) - amount of auxillary qubits needed for implementing the constraint.
            operator (str) - constraint's operator - for now the available operators are '==' and '!=' only (more operators to come).
        Returns:
            qc (QuantumCircuit object) - a quantum operator that implements the desired constraint computation to be appended to a circuit.
    '''
    
    # Initializing registers and circuit
    left_reg = QuantumRegister(left_qubits_amount, 'left_reg')
    right_reg = QuantumRegister(right_qubits_amount, 'right_reg')
    aux_reg = QuantumRegister(aux_qubits_amount, 'aux_reg') # aux_qubits_amount can be also zero = there'll be no qubits in the register
    out = QuantumRegister(1, 'out') # Each constriant has exactly one `out` qubit which we write the result into
    qc = QuantumCircuit(left_reg, right_reg, aux_reg, out)
    
    # Define settings regarding the sizes of the left and right registers (will be used later)
    min_amount = left_qubits_amount
    is_diff = left_qubits_amount != right_qubits_amount    
    if is_diff:
        if left_qubits_amount > right_qubits_amount:
            bigger = 0 # left = 0
            max_amount = left_qubits_amount
            min_amount = right_qubits_amount
        else:
            bigger = 1 # right = 1
            max_amount = right_qubits_amount
            min_amount = left_qubits_amount
    
    # In the following code the specific setting of the gates is custom made for the different possible combinations of variables:
    # Operator type, amount of qubits in each register
    # In order to grasp it a carefull examination is needed
    # It's recommended to try running this function with different values in order to get intuition
    
    # Case 1 - no auxiliary qubits
    if aux_qubits_amount == 0:
        qc.cx(left_reg, out)
        qc.cx(right_reg, out)
        if operator == '==':
            qc.x(out)   
    # Case 2 - with auxiliary qubits
    else:
        for i in range(min_amount):
            qc.cx(left_reg[i], aux_reg[i])
            qc.cx(right_reg[i], aux_reg[i])
            qc.x(aux_reg[i])
        
        #Case 2A - Different amount of qubits in left and right regs
        if is_diff:
            if bigger == 0:
                diff = left_reg[min_amount:max_amount]
            else:
                diff = right_reg[min_amount:max_amount]
            qc.x(diff)
            qc.mcx(diff, aux_reg[aux_qubits_amount - 1])
            qc.x(diff)
        
        # Writing the overall combined result to the out qubit
        if operator == '!=':
            qc.x(out)
        qc.mcx(aux_reg, out)
    
    return qc

def Grover_SAT_Operator(input_qubits, data, aux_qubits_list):
    '''
        Functionality:
            This function creates the suitable Grover operator for the SAT problem defined by the user's constraints.
        Parameters:
            input_qubits (int) - the amount of qubits in the input register.
            data (list of dictioneries) - a dict for eact constraint, every dict contains all the information for a single constraint.
                # Form: {c_index, constraint, operator, left_side, right_side, aux_qubits_amount}:
                    c_index (int) - constraint's index.
                    constraint (str) - the constraint as inserted by the user.
                    operator (str) - the constraint's operator, either '==' or '!=' (for now).
                    left_side, right_side (list) - a list of qubits indexes (int) in the right/left side of the constraint's equation.
                    aux_qubits_amount (int) - amount of auxiliary qubits needed for processing a specific constraint
                        # The minimum amount is 0 - in that case actions will be performed directly on the out qubit of the constraint.
            aux_qubits_list  (list of int) - a list containing amounts of aux qubits needed for each constraint.
        Returns:
            qc (QuantumCircuit object) - the quantum circuit that assembles the Grover operator for the SAT problem.
    '''
    
    # Defining total amount of auxiliary and out qubits needed
    total_aux_qubits_needed = sum(aux_qubits_list)
    out_qubits_amount = len(data) # Each constraint has exactly one corresponding out qubit
    
    # Initializing necessary registers and circuit
    input_reg = QuantumRegister(input_qubits, 'input_reg')
    aux_reg = QuantumRegister(total_aux_qubits_needed, 'aux_reg')
    out_reg = QuantumRegister(out_qubits_amount, 'out_reg')
    ancilla = QuantumRegister(1, 'ancilla')
    qc = QuantumCircuit(input_reg, aux_reg, out_reg, ancilla)
    
    # Handling constraints
    for c in data:
        i = c['c_index'] # Constraint's index
        
        # Generating the constraint circuit block
        c_circuit = ComputeConstraint(left_qubits_amount = len(c['left_side']), right_qubits_amount = len(c['right_side']), aux_qubits_amount = c['aux_qubits_amount'], operator = c['operator'])
        c_circuit.name = 'Constraint ' + str(i) + ': \n' + c['constraint']
                
        # Defining the qargs before appending c_circuit to qc
        if c['aux_qubits_amount'] == 0:
            qargs = input_reg[c['left_side']] + input_reg[c['right_side']] + [out_reg[i]]
            # Format: [left, right, out]
        else:
            aux_bottom = sum(aux_qubits_list[0:i])
            aux_top = aux_bottom + aux_qubits_list[i]
            qargs = input_reg[c['left_side']] + input_reg[c['right_side']] + aux_reg[aux_bottom : aux_top] + [out_reg[i]] 
            # Format: [left, right, aux, out]
        
        qc.append(instruction = c_circuit, qargs = qargs)
        qc.barrier()
    
    # Saving all actions until now for uncomputation
    qc_dagger = qc.inverse()
    qc_dagger.name = 'Uncomputation'
    
    # If all terms met, applying NOT to the ancilla (which is in the eigenstate |-> beforehand)
    qc.mcx(control_qubits = out_reg, target_qubit = ancilla)
    
    # Uncomputation
    qc.append(instruction = qc_dagger, qargs = qc.qubits)
    
    qc.name = 'Operator'   
    return qc

def DiffuserGrover(n):
    '''
        Functionality:
            Implementation of grover's diffuser (nothing is unique for a specific problem in that case, unlike in the operator case).
        Parameters:
            n - amount of qubits in the input register.
        Returns:
            diffuser_gate (Gate object) - the diffuser.
    '''
    
    qc = QuantumCircuit(n)
    
    qc.h(qc.qubits)
    qc.x(qc.qubits)
    qc.mcp(np.pi, control_qubits = [q for q in range(n - 1)], target_qubit = n - 1)    
    qc.x(qc.qubits)
    qc.h(qc.qubits)
    
    qc.name = 'Diffuser'
    diffuser_gate = qc.to_gate()
    return diffuser_gate

def Overall_SAT_Circuit(input_qubits, constraints, iterations):
    '''
        Functionality:
            This functions assembles the building blocks generated by other methods to an overall circuit needed for the given SAT problem.
        Parameters:
            input_qubits (int) - the amount of qubits in the input register.
            constraints (str) - a string that describes a set of boolean arithmetic constraints written in a specific format.
                # A full explanation regarding the format is provided in the file `constraints_format.txt`.
            iterations (int) - number of required iterations over Grover's algorithm.
        Returns:
            (dict) {sat_qc, sat_op}
            sat_qc (QuantumCircuit object) - the overall quantum circuit needed for the SAT problem. Ready to run.
            sat_op (QuantumCircuit object) - the operator generated by the `Grover_SAT_Operator` function.
    '''
    
    # Parsing contstraints string
    # We should get a list of dictioneris (a single dict for each constraint) of the form:
    # {c_index, constraint, operator, left_side, right_side, aux_qubits_amount}
    data = parse.ParseConstraints(constraints = constraints)
    
    N = 2 ** input_qubits # Total amount of options
    
    # Creating aux_qubits_list
    aux_qubits_list = []
    for d in data:
        aux_qubits_list.append(d['aux_qubits_amount'])
    
    # Building blocks
    sat_op = Grover_SAT_Operator(input_qubits = input_qubits, data = data, aux_qubits_list = aux_qubits_list)
    diffuser = DiffuserGrover(n = input_qubits)
    
    # Defining total amount of auxiliary and out qubits needed
    total_aux_qubits_needed = sum(aux_qubits_list)
    out_qubits_amount = len(data)
    
    # Initializing Circuit
    input_reg = QuantumRegister(input_qubits, 'input_reg')
    aux_reg = QuantumRegister(total_aux_qubits_needed, 'aux_reg')
    out_reg = QuantumRegister(out_qubits_amount, 'out_reg')
    ancilla = QuantumRegister(1, 'ancilla')
    results = ClassicalRegister(input_qubits, 'results')
    sat_qc = QuantumCircuit(input_reg, aux_reg, out_reg, ancilla, results)
    
    # Setting the input register to 2^n = N equal superposition of states, and the ancilla to an eigenstate of the NOT gate: |->
    sat_qc.h(input_reg)
    sat_qc.x(ancilla)
    sat_qc.h(ancilla)
    sat_qc.barrier()
    
    # Applying the iterator (operator + diffuser)
    for i in range(iterations):
        sat_qc.append(sat_op, qargs = sat_qc.qubits)
        sat_qc.append(diffuser, qargs = input_reg)
        sat_qc.barrier()
    
    # Measurements
    sat_qc.measure(input_reg, results)
    
    return {'sat_qc': sat_qc, 'sat_op': sat_op}