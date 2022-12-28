"""
Contains the functions handling issues arises from the role of the solutions in Grover's algorithm and its generalizations.
"""

import numpy as np
import random
import copy

from qiskit import transpile

import settings
from engine import SAT_Circuit


def calc_iterations(num_qubits, num_solutions):
    """
    Simple classical calculation of the number of iterations when the number of solutions is known.

    Args:
        num_qubits (int): number of qubits.
        num_solutions (int): known number of solutions.

    Returns:
        (int): the exact number of iterations needed for the given SAT problem.
    """
    
    # N is the dimension of the Hilbert space spanned by `num_qubits`
    N = 2 ** num_qubits

    iterations = int((np.pi / 4) * np.sqrt(N / num_solutions))
    return iterations     
        
def find_iterations_unknown_k(n, constraints_ob, precision=10):
    """
    Finds an adequate (optimal or near optimal) number of iterations suitable for a given SAT problem when `k` is unknown.
    The method being used is described in https://arxiv.org/pdf/quant-ph/9605034.pdf (section 4).
        # The method isn't exactly the same - we intentionally iterate over the described method.
        # We could have halt after finding one solution.
        # Using the iterative method we can build a circuit that amplifies all solutions - in excahnge for computational cost.
        # We demand `precision` good answers for any possible amount of iterations being checked.
        # If we can't find `precision` good answers - we reduce `precision` and iterate over the process again.
        # `precision` can be thought as the degree of accuracy - for large values of `precision` more optimal results will be obtained.

    Args:
        n (int): amount of input qubits.
        contraints (str): string of constraints.
        precision (int): amount of 'good answers' we demand.

    Returns: {'qc': (SAT_Circuit object), 'iterations': (int)}
        (SAT_Circuit object): the overall SAT circuit obtained after optimizing the iterations.
        (int): the calculated amount of iterations for the given SAT problem.
    """

    N = 2 ** n
    lamda = 6 / 5 # In each attempt to find `iterations` we increment by a multiply of `lamda`.
    qc_storage = {}

    # If precision == 0 then probably there is no solution.
    while precision > 0:
        m = 1
        exclude_list = []
        # For each level of precision we are looking for an adequate number of iterations.
        while m <= np.sqrt(N):
            
            # Figuring a guess for the number of iterations.
            iterations = False
            while iterations == False:
                m = lamda * m
                iterations = randint_exclude(start = 0, end = int(m), exclude = set(exclude_list))
            print(f"Checking iterations = {iterations}, precision = {precision}")

            # Obtaining the necessary SAT_Circuit object (preferably from the `qc_storage`)
            try:
                qc = qc_storage[iterations]
            except KeyError:
                exclude_list.append(iterations)
                qc = SAT_Circuit(n, constraints_ob, iterations)
                qc.add_input_reg_measurement()
                qc_storage[iterations] = copy.deepcopy(qc)

            job = settings.backend.run(transpile(qc, settings.backend), shots = precision, memory = True)
            outcomes = job.result().get_memory()

            # In `outcomes` we have `precision` results - If all of them are solutions, we have a match.
            match = True
            for o in outcomes:
                match = check_solution(o, constraints_ob.constraints)
                if not match:
                    break

            if match:
                return {'qc': qc, 'iterations': iterations}
        
        # Degrading precision if failed to find an adequate number of iterations.
        precision -= 2
        if precision <= 0:
            raise Exception("Didn't find any solution. Probably the entered SAT problem has no solution.")
  
def randint_exclude(start, end, exclude):
    """
    Guessing a number of iterations which haven't been tried yet.
    if it fails (`count >= 50`), returns False.
    """

    randint = random.randint(start, end)
    count = 0
    while randint in exclude:
        randint = random.randint(start, end)
        count += 1
        if count >= 50:
            return False

    return randint

def check_solution(solution, data):
    """
    Classical check of a single solution correctness.

    Args:
        solution (str) - a possible solution bit-string.
        data (list of dict) - a parsed constraints data.

    Returns:
        True - if `solution` is indeed a solution to the given SAT problem. False otherwise.
    """
    
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