#    Copyright 2022-2023 Ohad Lev.

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0,
#    or in the root directory of this package("LICENSE.txt").

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

"""
`calc_iterations`, `find_iterations_unknown` functions.
`is_circuit_match` and `randint_exclude` functions can be considered
as sub-functions of `find_iterations_unknown`.
"""

import random
import copy
from typing import Tuple, Optional
import numpy as np

from qiskit import transpile, QuantumCircuit
from qiskit.providers.backend import Backend

from sat_circuits_engine.util import timer_dec
from sat_circuits_engine.util.settings import BACKENDS
from sat_circuits_engine.circuit import SATCircuit, GroverConstraintsOperator
from sat_circuits_engine.classical_processing.classical_verifier import ClassicalVerifier
from sat_circuits_engine.constraints_parse import ParsedConstraints, SATNoSolutionError


def calc_iterations(num_input_qubits: int, num_solutions: int) -> int:
    """
    Simple classical calculation of the number of iterations over Grover's iterator
    when the number of solutions for the SAT problem is known.

    Args:
        num_input_qubits (int): number of input qubits.
        num_solutions (int): known number of solutions to the SAT problem.

    Returns:
        (int): the exact number of iterations needed for the given SAT problem.
    """

    # N is the dimension of the Hilbert space spanned by `num_input_qubits`
    N = 2**num_input_qubits

    # The formula for calculating the number of iterations
    iterations = int((np.pi / 4) * np.sqrt(N / num_solutions))

    return iterations


@timer_dec("Found number of iterations in ")
def find_iterations_unknown(
    num_input_qubits: int,
    grover_constraints_operator: GroverConstraintsOperator,
    parsed_constraints: ParsedConstraints,
    precision: Optional[int] = 10,
    backend: Optional[Backend] = BACKENDS(0),
    step: Optional[float] = 6 / 5,
) -> Tuple[SATCircuit, int]:
    """
    Finds an adequate (optimal or near optimal) number of iterations suitable for a given SAT problem
    when the number of "solutions" or "marked states" is unknown.
    The method being used is described in https://arxiv.org/pdf/quant-ph/9605034.pdf (section 4).
        - In short, the original method steps are:
            * Drawing a random number of iterations which is smaller than some number M.
            * Executing the circuit.
            * If a solution has been found (easy to verify classically) - done.
            * If not - M is being multiplied by a fixed step size.
            * Repeat.
        - Here we implement a variation of the described method above - with the goal of finding
        ad adequate number of iterations for the SAT problem, and not just a single solution.
            * Instead of exiting the process when finding a solution, we then
            execute the circuit `precision` times.
            * If `precision` execution shots gives 100% "good" solutions - done, we have found
            a number of iterations precise enough.
            * If not - we continue with the original method scheme.
            * If we couldn't find an adequate number of iterations for the given `precision`,
            the precision is decremented and we iterate over the process again with a lower precision.
            * If `precision` has been decremented to 0 - then we halt,
            and probably the SAT problem has no solution.
        - `precision` can be thought as the degree of accuracy - for large values of `precision`
        more optimal results will be obtained, in a price of extra computational overhead.

    Args:
        num_input_qubits (int): number of input qubits.
        grover_constraints_operator (GroverConstraintsOperator): Grover's operator for the SAT problem.
        parsed_constraints (ParsedConstraints): a series of constraints,
        already parsed to a specific format.
        precision (Optional[int] = 10): number of "valid solutions" which is
        enough to determine ad adequate number of iterations for the SAT problem.
        backend (Optional[Backend] = BACKENDS(0)): a backend to run the circuits upon.
        Default is the local AerSimulator (BACKENDS(0)).
        step (Optional[float] = 6/5): step size to increment M in each iteration.

    Returns: Tuple[SATCircuit, int]:
        (SATCircuit): the overall SAT circuit obtained after finding number of iterations.
        (int): the calculated number of iterations for the given SAT problem.

    Raises:
        SATNoSolutionError - if no adequate number of iterations has been found for
        any level of precision.
    """

    verifier = ClassicalVerifier(parsed_constraints)

    # Diemnsion of the Hilbert space spanned by the input qubits
    N = 2**num_input_qubits

    # A container for SATCircuit objects with various numbers of iterations
    qc_storage = {}

    # If `precision == 0`` then probably there is no solution
    while precision > 0:
        # M is the upper limit for drawing a random number of iterations
        M = 1

        checked_iterations = set()

        # For each level of precision we are looking for an adequate number of iterations
        print(f"\nChecking iterations for precision = {precision}:")
        while M <= np.sqrt(N):
            # Figuring a guess for the number of iterations
            iterations = False
            while not iterations:
                M = step * M
                iterations = randint_exclude(start=0, end=int(M), exclude=checked_iterations)
            print(f"    Checking iterations = {iterations}")

            # Obtaining the necessary SATCircuit object (preferably from the `qc_storage`)
            if iterations in qc_storage.keys():
                qc = qc_storage[iterations]
            else:
                qc = SATCircuit(num_input_qubits, grover_constraints_operator, iterations)
                qc.add_input_reg_measurement()
                qc_storage[iterations] = copy.deepcopy(qc)

            # Checking whether `qc` with `iterations` iterations gives 100% correct solutions (= match)
            match = is_circuit_match(qc, verifier, precision, backend)
            if match:
                return qc, iterations

            checked_iterations.add(iterations)

        # Degrading precision if failed to find an adequate number of iterations
        precision -= 2

        if precision <= 0:
            raise SATNoSolutionError(
                "Didn't find an suitable number of iterations."
                "Probably the SAT problem has no solution."
            )


def randint_exclude(start, end, exclude):
    """
    Guessing a number of iterations which haven't been tried yet.
    If it fails (`count >= 50`), returns False.
    """

    randint = random.randint(start, end)
    count = 0

    while randint in exclude:
        randint = random.randint(start, end)
        count += 1
        if count >= 50:
            return False

    return randint


def is_circuit_match(
    qc: QuantumCircuit, verifier: ClassicalVerifier, precision: int, backend: Backend
) -> bool:
    """
    Checks classically whether running `qc` `precision` times gives `precision` correct solutions.

    Args:
        qc (QuantumCircuit): the quantum circuit to run.
        verifier (ClassicalVerifier): classical verifier object to verify solutions with.
        precision (int): number of correct solutions required.
        backend (Backend): backend to run circuits upon.

    Returns:
        (bool): True if the execution of `qc` yielded 100% correct solutions (`precision` times).
        False otherwise.
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
