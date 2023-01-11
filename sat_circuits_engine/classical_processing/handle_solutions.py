"""
Contains the functions handling issues arises from the role of the solutions in Grover's algorithm and its generalizations.
"""

import os
import random
import copy
import time
import numpy as np
from typing import Tuple, List, Optional, Union

from qiskit import transpile, QuantumCircuit

from sat_circuits_engine.util import timer_dec
from sat_circuits_engine.util.settings import backend
from sat_circuits_engine.circuit import SATCircuit

from .classical_verifier import ClassicalVerifier

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

# def is_qc_x_iterations_a_match(qc, precision, constraints_data, iterations=None):
def is_qc_x_iterations_a_match(qc: QuantumCircuit, verifier: ClassicalVerifier, precision: int) -> bool:
    """
    Checks classically whether running `qc` `precision` times gives `precision` correct solutions.
    
    Args:
        qc (QuantumCircuit object): the quantum circuit to run.
        precision (int): number of correct solutions required.
        constraints_data: a list of `engine.Constraint` objects.
    """

    job = backend.run(transpile(qc, backend), shots=precision, memory=True)
    outcomes = job.result().get_memory()

    # In `outcomes` we have `precision` results - If all of them are solutions, we have a match.
    match = True
    for outcome in outcomes:
        match = verifier.verify(outcome)
        if not match:
            break

    return match

@timer_dec
def find_iterations_unknown(
    num_input_qubits: int,
    grover_constraints_operator,
    parsed_constraints,
    precision: Optional[int] = 10
) -> Tuple[str, Union[SATCircuit, int]]:
    """
    Finds an adequate (optimal or near optimal) number of iterations suitable for a given SAT problem
    when the number of "solutions" or "marked states" is unknown.
    # TODO IMPROVE THIS EXPLANATION AND MAYBE THE ENTIRE METHOD
    The method being used is described in https://arxiv.org/pdf/quant-ph/9605034.pdf (section 4).
        - The method isn't exactly the same - we intentionally iterate over the described method.
        - We could have halt after finding one solution.
        - Using the iterative method we can build a circuit that amplifies all solutions, but in a price
        of a computational overhead.
        - We demand `precision` good answers for any possible number of iterations being checked.
        - If we can't find `precision` good answers - we decrement `precision`
        and iterate over the process again.
        - `precision` can be thought as the degree of accuracy - for large values of `precision`
        more optimal results will be obtained.

    Args:
        num_input_qubits (int): number of input qubits.
        grover_constraints_operator (): # TODO COMPLETE.
        precision (int): number of "good answers" which is enough to determine the number of iterations.

    Returns: Tuple[Union[SATCircuit, int]]:
        (SATCircuit): the overall SAT circuit obtained after optimizing the iterations.
        (int): the calculated amount of iterations for the given SAT problem.

    Raises:
        # TODO COMPLETE
    """

    # TODO EXPLAIN
    verifier = ClassicalVerifier(parsed_constraints)

    # TODO COMPLETE WHAT IS THIS
    N = 2 ** num_input_qubits
    lamda = 6 / 5 # In each attempt to find `iterations` we increment by a multiply of `lamda`.
    qc_storage = {}

    # If precision == 0 then probably there is no solution
    while precision > 0:
        # TODO COMPLETE WHAT ARE THESE
        m = 1
        exclude_list = []

        print(f"\nChecking iterations for precision = {precision}:")

        # For each level of precision we are looking for an adequate number of iterations
        # TODO COMPLETE WHY m <= np.sqrt(N)
        while m <= np.sqrt(N):
            
            # Figuring a guess for the number of iterations.
            # TODO COMPLETE WHAT IS THIS
            iterations = False
            while iterations == False:
                m = lamda * m
                iterations = randint_exclude(start = 0, end = int(m), exclude = set(exclude_list))
            print(f"    Checking iterations = {iterations}")

            # Obtaining the necessary SATCircuit object (preferably from the `qc_storage`)
            try:
                qc = qc_storage[iterations]
            except KeyError:
                exclude_list.append(iterations)
                qc = SATCircuit(num_input_qubits, grover_constraints_operator, iterations)
                qc.add_input_reg_measurement()
                qc_storage[iterations] = copy.deepcopy(qc)

            match = is_qc_x_iterations_a_match(qc, verifier, precision)

            if match:
                return qc, iterations
        
        # Degrading precision if failed to find an adequate number of iterations.
        precision -= 2
        if precision <= 0:
            raise Exception("Didn't find any solution. Probably the SAT problem has no solution.")
  
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

#################### TODO REMOVE ################

# def check_solution(solution: str, data: List[str]) -> bool:
#     """
#     Classical check of a single solution correctness.

#     Args:
#         solution (str) - a possible solution bit-string.
#         data (list of dict) - a parsed constraints data.

#     Returns:
#         True - if `solution` is indeed a solution to the given SAT problem. False otherwise.
#     """
    
#     solution = solution[::-1] # Reversing oreder for conveniency
#     match = True
    
#     # Going over the constraints
#     for c in data:
#         l = c.left_side
#         r = c.right_side
#         op = c.operator
        
#         l_len = len(l)
#         r_len = len(r)
#         if r_len <  l_len:
#             min_len = len(r)
#             max_len = len(l)
#         else:
#             min_len = len(l)
#             max_len = len(r)

#         if op == '==': # The case of op = '==' is an AND case
#             for i in range(min_len):
#                 if solution[l[i]] != solution[r[i]]:
#                     match = False
#                     break
            
#             # Handling the case where op == '==' and an different amount of qubits are compared
#             for i in range(min_len, max_len):
#                 try:
#                     if solution[l[i]] != '0':
#                         match = False
#                         break
#                 except:
#                     if solution[r[i]] != '0':
#                         match = False
#                         break
                
#         else: # The case of op = '!=' is an OR case
#             count = 0
#             for i in range(min_len):
#                 if solution[l[i]] == solution[r[i]]:
#                     count += 1
#             if count == min_len:
#                 # Handling the case where op == '!=' and an different amount of qubits are compared
#                 for i in range(min_len, max_len):
#                     try:
#                         if solution[l[i]] == '0':
#                             count += 1
#                     except:
#                         if solution[r[i]] == '0':
#                             count += 1
#                 if count == max_len:
#                     match = False
        
#         # If at least 1 constraint is False - return False
#         if match == False:
#             return match
        
#     # If we got this far then match = True and the string being checked is indeed a solution
#     return match