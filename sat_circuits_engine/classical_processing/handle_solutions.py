"""
Functions that finds the number of iterations over Grover's iterator (operator + diffuser),
according to the number of input qubits nad the knonwn or unknown number of solutions. 
"""

import random
import copy
import numpy as np
from typing import Tuple, Optional, Union

from qiskit import transpile, QuantumCircuit
from qiskit.providers.backend import Backend

from sat_circuits_engine.util import timer_dec
from sat_circuits_engine.util.settings import BACKENDS
from sat_circuits_engine.circuit import SATCircuit, GroverConstraintsOperator
from sat_circuits_engine.classical_processing.classical_verifier import ClassicalVerifier
from sat_circuits_engine.constraints_parse import ParsedConstraints

def calc_iterations(num_input_qubits: int, num_solutions: int) -> int:
    """
    Simple classical calculation of the number of iterations when the number of solutions is known.

    Args:
        num_input_qubits (int): number of qubits.
        num_solutions (int): known number of solutions.

    Returns:
        (int): the exact number of iterations needed for the given SAT problem.
    """
    
    # N is the dimension of the Hilbert space spanned by `num_qubits`
    N = 2 ** num_input_qubits

    iterations = int(
        (np.pi / 4) * np.sqrt(N / num_solutions)
    )
    return iterations

def is_qc_x_iterations_a_match(
    qc: QuantumCircuit,
    verifier: ClassicalVerifier,
    precision: int,
    backend: Backend
) -> bool:
    """
    Checks classically whether running `qc` `precision` times gives `precision` correct solutions.
    
    Args:
        qc (QuantumCircuit): the quantum circuit to run.
        verifier (ClassicalVerifier): TODO COMPLETE.
        precision (int): number of correct solutions required.
        backend (Backend): TODO COMPLETE.

    Returns:
        (bool): TODO COMPLETE.
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

@timer_dec("Found number of iterations in ")
def find_iterations_unknown(
    num_input_qubits: int,
    grover_constraints_operator: GroverConstraintsOperator,
    parsed_constraints: ParsedConstraints,
    precision: Optional[int] = 10,
    backend: Optional[Backend] = BACKENDS(0)
) -> Tuple[SATCircuit, int]:
    """
    Finds an adequate (optimal or near optimal) number of iterations suitable for a given SAT problem
    when the number of "solutions" or "marked states" is unknown.
    TODO IMPROVE THIS EXPLANATION AND MAYBE THE ENTIRE METHOD
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
        grover_constraints_operator (GroverConstraintsOperator): TODO COMPLETE.
        parsed_constraints (ParsedConstraints): TODO COMPLETE.
        precision (Optional[int] = 10): number of "good answers" which is enough to determine the number of iterations.
        backend (Optional[Backend] = BACKENDS(0)): TODO COMPLETE.

    Returns: Tuple[SATCircuit, int]:
        (SATCircuit): the overall SAT circuit obtained after optimizing the iterations.
        (int): the calculated amount of iterations for the given SAT problem.

    Raises:
        TODO COMPLETE
    """

    # TODO EXPLAIN
    verifier = ClassicalVerifier(parsed_constraints)

    # TODO COMPLETE WHAT IS THIS
    N = 2 ** num_input_qubits
    step = 6 / 5 # In each attempt to find `iterations` we increment by a multiply of `step`.
    qc_storage = {}

    # If precision == 0 then probably there is no solution
    while precision > 0:

        # TODO COMPLETE WHAT IS THIS
        m = 1

        # For each level of precision we check all over again
        checked_iterations = set()

        # For each level of precision we are looking for an adequate number of iterations
        # TODO COMPLETE WHY m <= np.sqrt(N)
        print(f"\nChecking iterations for precision = {precision}:")
        while m <= np.sqrt(N):
            
            # Figuring a guess for the number of iterations.
            # TODO COMPLETE WHAT IS THIS
            iterations = False
            while iterations == False:
                m = step * m
                iterations = randint_exclude(start=0, end=int(m), exclude=checked_iterations)
            print(f"    Checking iterations = {iterations}")

            # Obtaining the necessary SATCircuit object (preferably from the `qc_storage`)
            try:
                qc = qc_storage[iterations]
            except KeyError:
                qc = SATCircuit(num_input_qubits, grover_constraints_operator, iterations)
                qc.add_input_reg_measurement()
                qc_storage[iterations] = copy.deepcopy(qc)

            match = is_qc_x_iterations_a_match(qc, verifier, precision, backend)

            if match:
                return qc, iterations
            checked_iterations.add(iterations)
        
        # Degrading precision if failed to find an adequate number of iterations.
        precision -= 2
        if precision <= 0:
            raise Exception(
                "Didn't find an suitable number of iterations." \
                "Probably the SAT problem has no solution."
            )
  
def randint_exclude(start, end, exclude):
    """
    Guessing a number of iterations which haven't been tried yet.
    If it fails (`count >= 50`), returns False.
    """

    # TODO REMOVE
    # print("=========")
    # print(exclude)
    # print("=========")

    randint = random.randint(start, end)
    count = 0
    while randint in exclude:
        randint = random.randint(start, end)
        count += 1
        if count >= 50:
            return False

    return randint