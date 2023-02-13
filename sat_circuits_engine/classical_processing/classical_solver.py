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