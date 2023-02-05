"""
TODO COMPLETE
"""

import json
from typing import Set

from sat_circuits_engine.constraints_parse import ParsedConstraints
from sat_circuits_engine.classical_processing.classical_verifier import ClassicalVerifier
from sat_circuits_engine.util.settings import TEST_DATA_PATH

def solve_classically(num_input_qubits: int, constraints_string: str) -> Set[str]:
    """
    Given a set of constraints, solves a SAT problem classically.

    Args:
        num_input_qubits (int): number of input qubits.
        constraints_string (str): constraints string. TODO ELABORATE.

    Returns:
        (List[str]): a list of bitstrings that are solutions to the SAT problem.
    """

    # Total amount of optional states
    N = 2 ** num_input_qubits

    # TODO COMPLETE
    parsed_constraints = ParsedConstraints(constraints_string)
    verifier = ClassicalVerifier(parsed_constraints)
    
    solutions = set()
    for decmial_num in range(N):
        bitstring = bin(decmial_num)[2:].zfill(num_input_qubits)
        
        if verifier.verify(bitstring):
            solutions.add(bitstring)
    
    return solutions


################# TODO CONSIDER WHAT TO LEAVE IN THE END ################
if __name__ == "__main__":
    
    with open(TEST_DATA_PATH, 'r') as f:
        test_data = json.load(f)

    for example_name, example_data in test_data.items():
        solutions_found_classically = solve_classically(
            example_data['num_input_qubits'],
            example_data['constraints_string']
        )
        solutions_equality = set(example_data['solutions']) == solutions_found_classically

        print()
        print(f"{example_name}:")
        print(f"constraints_string = {example_data['constraints_string']}")
        print(f"num_input_qubits = {example_data['num_input_qubits']}")
        print(f"data_solutions = {example_data['solutions']}")
        print(f"SOLUTIONS FOUND CLASSICALLY = {solutions_found_classically}")
        print(f"VALID SOLUTIONS = {solutions_equality}")

    # n = 6
    # s = "([5][4] == [3][2][1]),([2][1] == 3)"
    # solutions_found_classically = solve_classically(n, s)
    # print(solutions_found_classically)