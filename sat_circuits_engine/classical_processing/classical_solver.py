"""
`solve_classically` function.
"""

from typing import Set

from sat_circuits_engine.constraints_parse import ParsedConstraints
from sat_circuits_engine.classical_processing.classical_verifier import ClassicalVerifier

def solve_classically(num_input_qubits: int, constraints_string: str) -> Set[str]:
    """
    Given a set of constraints, solves a SAT problem classically.

    Args:
        num_input_qubits (int): number of input qubits.
        constraints_string (str): a "low-level" format constraints string,
        as defined in "constraints_format.md" (in the main directory).

    Returns:
        (SEt[str]): all bitstrings that are solutions to the SAT problem.
    """

    # Total amount of optional states
    N = 2 ** num_input_qubits

    parsed_constraints = ParsedConstraints(constraints_string)
    verifier = ClassicalVerifier(parsed_constraints)    
    solutions = set()

    # Iterating over all possible states and checking them one-by-one
    for decmial_num in range(N):
        bitstring = bin(decmial_num)[2:].zfill(num_input_qubits)
        
        if verifier.verify(bitstring):
            solutions.add(bitstring)
    
    return solutions