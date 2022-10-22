'''
    This module contains the methods handling issues arises from the role of the solutions in Grover's algorithm and its generalizations.
'''

import numpy as np
import random
import copy
from qiskit import transpile

import interface
import parse
import circuit
import settings

def CheckSolution(solution, data):
    '''
        Functionality:
            Classical check of a single solution correctness.
        Parameters:
            solution (str) - a possible solution bit-string.
            data (list of dict) - a parsed constraints data.
        Returns:
            True - if `solution` is indeed a solution to the given SAT problem. False otherwise.
    '''
    
    solution = solution[::-1] # Reversing oreder for conveniency
    match = True
    
    # Going over the constraints
    for c in data:
        l = c.left_side
        r = c.right_side
        op = c.operator
        
        l_len = len(l)
        r_len = len(r)
        if r_len <  l_len:
            min_len = len(r)
            max_len = len(l)
        else:
            min_len = len(l)
            max_len = len(r)

        if op == '==': # The case of op = '==' is an AND case
            for i in range(min_len):
                if solution[l[i]] != solution[r[i]]:
                    match = False
                    break
            
            # Handling the case where op == '==' and an different amount of qubits are compared
            for i in range(min_len, max_len):
                try:
                    if solution[l[i]] != '0':
                        match = False
                        break
                except:
                    if solution[r[i]] != '0':
                        match = False
                        break
                
        else: # The case of op = '!=' is an OR case
            count = 0
            for i in range(min_len):
                if solution[l[i]] == solution[r[i]]:
                    count += 1
            if count == min_len:
                # Handling the case where op == '!=' and an different amount of qubits are compared
                for i in range(min_len, max_len):
                    try:
                        if solution[l[i]] == '0':
                            count += 1
                    except:
                        if solution[r[i]] == '0':
                            count += 1
                if count == max_len:
                    match = False
        
        # If at least 1 constraint is False - return False
        if match == False:
            return match
        
    # If we got this far then match = True and the string being checked is indeed a solution
    return match
    
def CalcIterationsKnown_k(N, k):
    '''
        Functionality:
            Simple classical calculation of the amount of iterations needed when `k` (amount of solutions) is known.
        Parameters:
            N = 2 ** n
            k (int) - known amount of solutions.
        Returns:
            iterations - the exact amount of iterations needed for the given SAT problem.
    '''
    
    iterations = int((np.pi / 4) * np.sqrt(N / k))
    return iterations     
        
def FindIterationsUnknown_k(n, constraints_ob, precision = 10):

    N = 2 ** n
    lamda = 6 / 5
    qc_storage = {}

    while precision > 0:
        m = 1
        exclude_list = []
        while m <= np.sqrt(N):
            
            iterations = False
            while iterations == False:
                m = lamda * m
                iterations = randint_exclude(start = 0, end = int(m), exclude = set(exclude_list))

            print(f"iterations = {iterations}, precision = {precision}") # TODO REMOVE THIS FLAG

            try:
                qc = qc_storage[iterations]
            except KeyError:
                exclude_list.append(iterations)
                qc = circuit.SAT_Circuit(n, constraints_ob, iterations)
                qc.add_input_reg_measurement()
                qc_storage[iterations] = copy.deepcopy(qc)

            job = settings.backend.run(transpile(qc, settings.backend), shots = precision, memory = True)
            outcomes = job.result().get_memory()

            match = True
            for o in outcomes:
                match = CheckSolution(o, constraints_ob.constraints)
                if not match:
                    break

            if match:
                return {'qc': qc, 'iterations': iterations}
        
        precision -= 2 # Degrading precision if failed to find an adequate number of iterations
        if precision <= 0:
            raise Exception("Didn't find any solution. Probably the entered SAT problem has no solution.")

    
def randint_exclude(start, end, exclude):

    randint = random.randint(start, end)
    count = 0
    while randint in exclude:
        randint = random.randint(start, end)
        count += 1
        if count >= 100:
            return False

    return randint