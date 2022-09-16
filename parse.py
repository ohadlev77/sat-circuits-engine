'''
    This module contains all methods regarding the parsing of the constraints as defined by the user, and their derived computations.
'''

import numpy as np

from qiskit import QuantumCircuit, transpile, Aer, QuantumRegister, ClassicalRegister
import circuit

def IsolatingOperatorFromConstraint(c):
    '''
        Functionality:
            This function parses the constraint's equation and extracts the equation's operator.
        Paramters:
            c (str) - single constraint equation.
        Returns:
            op (str) - the operator.
    '''
    
    try:
        c.index('==')
        op = '=='
    except:
        try:
            c.index('!=')
            op = '!='
        except:
            raise ValueError('Only == and != operators are supported for now')
            
    return op

def ParseSidesFromConstraint(c, op):
    '''
        Functionality:
            This function parses a single constraint equation and returns the relevant data.
        Paramters:
            c (str) - a single constraint equation.
            op (str) - a single constraint operator.
        Returns:
            A dictionary of the form {left (list), right (list)}:
                a list of qubits indexes (int) in the right/left side of the constraint's equation.    
    '''

    sides = list()
    side_num = 0 # Left is 0, Right is 1
    LR = c.split(op)
    for side in LR:
        if side.find('[') == -1: # This is the case where there is an integer phrase on that side
            i = side.find('(') + 1
            ie = side.find(op)
            num = int(side[i:ie]) # Isolating the integer
            bin_num = bin(num)[2:] # Translating to binary string
            sides.append(bin_num)
        else: # This is the case where there is a qubit indexes phrase on that side
            sides.append([]) # Appending a list (that will contain indexes of qubits) for that specific side
            i = 0
            while side.find('[',i) != -1:
                i = side.find('[',i) + 1
                ie = side.find(']',i)
                sides[side_num].append(int(side[i:ie])) # Isolating and appending the qubit index
        side_num += 1
    
    return {'left': sides[0], 'right': sides[1]}

def CalcAuxNeeded(left, right):
    '''
        Functionality:
            This function calculates the amount of auxiliary qubits needed for computing a given constraint.
        Paramters:
            left, right (list) - a list of qubits indexes in the right/left side of the constraint equation.
        Returns:
            amount (int) - The amount of auxiliary qubits needed.
    '''
    
    len_left = len(left)
    len_right = len(right)
    min_len = min(len_left, len_right)
    
    # Case 1 - 1 qubit from each side = No auxiliary qubits needed
    if len_left == 1 and len_right == 1:
        amount = 0        
    
    #Case 2 - More than 1 qubit from either of the sides
    else:
        amount = min_len
        if len_left != len_right: # Case 2.A - non-equal amount of qubits between sides
            amount += 1
    
    return amount

def ParseConstraints(constraints):
    '''
        Functionality:
            This function parses the string of constraints inserted by a user.
            Computations are made according to the explanations in the file - `constraints_format.txt`
        Parameters:
            constraints (str) - a string that describes a set of boolean arithmetic constraints written in a specific format.
                # A full explanation regarding the format is provided in the file `constraints_format.txt`.          
        Returns:
            data (list of dictioneries) - a dict for eact constraint, every dict contains all the information for a single constraint.
                # Form: {c_index, constraint, operator, left_side, right_side, aux_qubits_amount}:
                    c_index (int) - constraint's index.
                    constraint (str) - the constraint as inserted by the user.
                    operator (str) - the constraint's operator, either '==' or '!=' (for now).
                    left_side, right_side (list) - a list of qubits indexes (int) in the right/left side of the constraint's equation.
                    aux_qubits_amount (int) - amount of auxiliary qubits needed for processing a specific constraint
                        # The minimum amount is 0 - in that case actions will be performed directly on the out qubit of the constraint.
    '''
    
    data = []
    constraints_list = constraints.split(",")
    
    c_index = 0
    for c in constraints_list:
        c_dict = {}
        
        # Inserting constraint index
        c_dict.update({'c_index': c_index})
        
        # Inserting the constraint as typed by the user
        c_dict.update({'constraint': c})
        
        # Isoltaing and inserting the constraint's operator
        op = IsolatingOperatorFromConstraint(c)
        c_dict.update({'operator': op})
        
        # Isoltaing and parsing the left and right sides of the constraint's equation
        sides = ParseSidesFromConstraint(c, op)
        c_dict.update({'left_side': sides['left']})
        c_dict.update({'right_side': sides['right']})
        
        # Calculating the necessary amount of quxillary qubits for computing that constraint
        aux_qubits_amount = CalcAuxNeeded(left = sides['left'], right = sides['right'])
        c_dict.update({'aux_qubits_amount': aux_qubits_amount})
        
        data.append(c_dict)
        c_index += 1
    
    return data