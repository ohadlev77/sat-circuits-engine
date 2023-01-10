"""
TODO COMPLETE
"""

from typing import List

from sat_circuits_engine.circuit import GroverConstraintsOperator

# TODO IN THE END CHANGE THIS TO A RELATIVE IMPORT
from classical_verifier import ClassicalVerifier

def solve_classically(num_input_qubits: int, constraints_string: str) -> List[str]:

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
    constraints = GroverConstraintsOperator(constraints_string, num_input_qubits)
    verifier = ClassicalVerifier(constraints)
    
    solutions = []
    for decmial_num in range(N):
        bitstring = bin(decmial_num)[2:].zfill(num_input_qubits)
        
        if verifier.verify(bitstring):
            solutions.append(bitstring)
    
    return solutions


################# TODO CONSIDER WHAT TO LEAVE IN THE END ################

import json

if __name__ == "__main__":
    
    with open("sat_circuits_engine/data/test_data.json", 'r') as f:
        test_data = json.load(f)

    for example_name, example_data in test_data.items():
        solutions_found_classically = solve_classically(
            example_data['num_input_qubits'],
            example_data['constraints_string']
        )
        solutions_equality = set(example_data['solutions']) == set(solutions_found_classically)

        if not solutions_equality:        
            print()
            print(f"{example_name}:")
            print(f"constraints_string = {example_data['constraints_string']}")
            print(f"num_input_qubits = {example_data['num_input_qubits']}")
            print(f"old solutions = {example_data['solutions']}")

            print(f"SOLUTIONS FOUND CLASSICALLY = {solutions_found_classically}")

            print(f"SOLUTIONS EQUALITY = {solutions_equality}")