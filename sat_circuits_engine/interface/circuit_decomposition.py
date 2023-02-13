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
Functions for decomposing QuantumCircuit objects into a specific set of blocks:
    1. decompose_operator.
    2. gates_decomposition_sort.

Constants:
    1. BLOCKS.
"""

from copy import deepcopy
from typing import List

from sat_circuits_engine.circuit import GroverConstraintsOperator

# These blocks shouldn't be decomposed any farther
BLOCKS = {
    'x',
    'h',
    'mcx',
    'cx',
    'cp',
    'ccx',
    'rccx',
    'rccx_dg',
    'rcccx',
    'rcccx_dg',
    'mcx_gray',
    'Uncomputation',
    'QFT',
    'IQFT_dg'
}

def decompose_operator(operator: GroverConstraintsOperator) -> GroverConstraintsOperator:
    """
    Generates the decomposed version of a QuantumCircuit object (for visualization purposes).
    The function is decomposing a circuit to its basic building blocks until no further
    decomposition is possible. The basic building blocks are those defined by Qiskit combined
    with the building blocks defined byt the set constant `BLOCKS`.

    Args:
        operator (GroverConstraintsOperator): the object to decompose. can be any QuantumCircuit object
        but intended for GroverConstraintsOperator objects (which are child-objects of QuantumCircuit).

    Returns:
        (GroverConstraintsOperator): the decomposed operator.
    """
    
    existing_gates = list(dict(operator.count_ops()))
    gates_to_decompose = gates_decomposition_sort(circuit_gates=deepcopy(existing_gates))

    while True:
        operator = operator.decompose(gates_to_decompose)
        existing_gates = list(dict(operator.count_ops()))
        
        gates_to_decompose_1 = gates_decomposition_sort(
            circuit_gates=deepcopy(existing_gates)
        )

        if gates_to_decompose_1 == gates_to_decompose:
            break
        else:
            gates_to_decompose = gates_to_decompose_1

    return operator

def gates_decomposition_sort(circuit_gates: List[str]) -> List[str]:
    """
    Removes chosen gates from a list of gate types.

    Args:
        circuit_gates (list) - A list gate types.
        
    Returns:
        Altered `circuit_gates` list.
    """
    
    for gate in BLOCKS:
        if gate in circuit_gates:
            circuit_gates.remove(gate)
        
    return circuit_gates