"""
Contains the functions handling issues arises from the role of the solutions in Grover's algorithm and its generalizations.
"""

import os
import random
import copy
import time
import numpy as np
from multiprocessing import get_context

from qiskit import transpile

from sat_circuits_engine.util import backend, timer_dec
from sat_circuits_engine.circuit import SAT_Circuit

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
def is_qc_x_iterations_a_match(args_dict):
    """
    Checks classically whether running `qc` `precision` times gives `precision` correct solutions.
    
    Args:
        qc (QuantumCircuit object): the quantum circuit to run.
        precision (int): number of correct solutions required.
        constraints_data: a list of `engine.Constraint` objects.
    """

    job = backend.run(transpile(args_dict['qc'], backend), shots=args_dict['precision'], memory=True)
    outcomes = job.result().get_memory()

    # In `outcomes` we have `precision` results - If all of them are solutions, we have a match.
    match = True
    for outcome in outcomes:
        match = check_solution(outcome, args_dict['constraints_data'])
        if not match:
            break

    return match

@timer_dec
def find_iterations_unknown(num_qubits, constraints_ob, precision=10, multiprocessing=True):
    """
    Finds an adequate (optimal or near optimal) number of iterations suitable for a given SAT problem
    when the number of "solutions" or "marked states is unknown.
    The method being used is described in https://arxiv.org/pdf/quant-ph/9605034.pdf (section 4).
        # The method isn't exactly the same - we intentionally iterate over the described method.
        # We could have halt after finding one solution.
        # Using the iterative method we can build a circuit that amplifies all solutions, but in a price
        of a computational overhead.
        # We demand `precision` good answers for any possible number of iterations being checked.
        # If we can't find `precision` good answers - we decrement `precision`
        and iterate over the process again.
        # `precision` can be thought as the degree of accuracy - for large values of `precision`
        more optimal results will be obtained.

    Args:
        num_qubits (int): number of input qubits.
        constraints_ob # TODO COMPLETE.
        precision (int): number of "good answers" which is enough to determine the number of iterations.
        multiprocessing (bool, optinal):
            # `True` (default) = use multiprocessing to enhace computation's speed (with maximum cores).
            # `False` = do not use multiprocessing.

    Returns: {'qc': (SAT_Circuit object), 'iterations': (int)}
        (SAT_Circuit object): the overall SAT circuit obtained after optimizing the iterations.
        (int): the calculated amount of iterations for the given SAT problem.
    """

    # TODO COMPLETE WHAT IS THIS
    N = 2 ** num_qubits
    lamda = 6 / 5 # In each attempt to find `iterations` we increment by a multiply of `lamda`.
    qc_storage = {}

    # Used in the case of multiprocessing
    cores = os.cpu_count()
    tasks = []
    start_time = time.time() # TODO REMOVE DEBUG

    # If precision == 0 then probably there is no solution.
    while precision > 0:
        # TODO COMPLETE WHAT ARE THESE
        m = 1
        exclude_list = []

        print(f"\nChecking iterations for precision = {precision}:")

        # For each level of precision we are looking for an adequate number of iterations.
        # TODO COMPLETE WHY m <= np.sqrt(N)
        while m <= np.sqrt(N):
            
            # Figuring a guess for the number of iterations.
            # TODO COMPLETE WHAT IS THIS
            iterations = False
            while iterations == False:
                m = lamda * m
                iterations = randint_exclude(start = 0, end = int(m), exclude = set(exclude_list))
            print(f"    Checking iterations = {iterations}")

            # Obtaining the necessary SAT_Circuit object (preferably from the `qc_storage`)
            try:
                qc = qc_storage[iterations]
            except KeyError:
                exclude_list.append(iterations)
                qc = SAT_Circuit(num_qubits, constraints_ob, iterations)
                qc.add_input_reg_measurement()
                qc_storage[iterations] = copy.deepcopy(qc)

            if multiprocessing == True:
                tasks.append({'qc': qc, 'precision': precision,
                'constraints_data': constraints_ob.constraints, 'iterations': iterations})
                
                if len(tasks) == cores:
                    print(f"It took {time.time() - start_time} seconds to start multiprocessing pool") # TODO REMOVE FLAG
                    with get_context("spawn").Pool(processes=4) as pool:
                        results = pool.imap_unordered(is_qc_x_iterations_a_match, tasks)
                        
                        for index, result in enumerate(results):
                            print(f"Checking result {index}") # TODO REMOVE
                            if result:
                                return {'qc': tasks[index]['qc'], 'iterations': tasks[index]['iterations']}

                    tasks.clear()
                    start_time = time.time() # TODO REMOVE FLAG
            else:
                match = is_qc_x_iterations_a_match({'qc': qc, 'precision': precision,
                'constraints_data': constraints_ob.single_constraints_objects})
                if match:
                    return {'qc': qc, 'iterations': iterations}
        
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