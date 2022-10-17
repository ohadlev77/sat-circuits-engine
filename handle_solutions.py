'''
    This module contains the methods handling issues arises from the role of the solutions in Grover's algorithm and its generalizations.
'''

import numpy as np
import random
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

def FindIterationsUnknown_k(n, constraints, x = 1):
    '''
        Functionality:
            Finding an adequate (optimal or near optimal) number of iterations suitable for a given SAT problem when `k` is unknown.
            The method being used is described in https://arxiv.org/pdf/quant-ph/9605034.pdf (section 4).
                # The method isn't exactly the same - we intentionally iterate over the described method.
                # We could have halt after finding one solution.
                # Using the iterative method we can build a circuit that amplifies all solutions - in excahnge for computational cost.
                # We demand `x` good answers for any possible amount of iterations being checked.
                # If we can't find `x` good answers - we reduce `x` and iterate over the process again.
                # `x` can be thought as the degree of accuracy - for large values of `x` more optimal results will be obtained.
        Parameters:
            n (int) - amount of input qubits.
            contraints (str) - string of constraints.
            x (int) - amount of "good answers" we demand.
        Returns:
            iterations - the calculated amount of iterations for the given SAT problem.
    '''
    
    # Basic settings
    N = 2 ** n
    data = parse.Constraints(constraints).constraints # TODO NEED TO MERGE DUPLICATION WITH circuit.py
    
    # Initial conditions setting
    lamda = 6 / 5 # Each time we increment m such that m *= lamda
    
    # Going over through the possible options
    while x > 0:
        m = 1
        while m <= np.sqrt(N): # If there is one solution only, that is the case with maximum iterations needed

            next_m = lamda * m
            iterations = random.randint(0, int(next_m))

            qc = circuit.Overall_SAT_Circuit(input_qubits = n, constraints = constraints, iterations = iterations)['sat_qc']
            job = settings.backend.run(transpile(qc, settings.backend), shots = x, memory = True)
            outcomes = job.result().get_memory()

            match = True
            for o in outcomes:
                match = CheckSolution(solution = o, data = data)
                if not match:
                    break

            if match:
                return iterations

            m = next_m
        
        x -= 2 # Degrading precision if didn't found the amount of iterations
        
        
    
    
    
    