"""
Functions for decomposing QuantumCircuit objects into specific set of blocks.
"""

from copy import deepcopy
from typing import List

from sat_circuits_engine.circuit import GroverConstraintsOperator

# Those blocks sholdn't be decomposed any farther
BLOCKS =  [
    'x', 'h', 'mcx', 'cx', 'cp', 'ccx', 'rccx', 'rccx_dg', 'mcx_gray', 'Uncomputation', 'QFT', 'IQFT_dg'
]

def decompose_operator(operator: GroverConstraintsOperator) -> GroverConstraintsOperator:
    """
    TODO COMPLETE
    # Preparing the decomposed version of the operator's circuit
    """
    
    existing_gates = list(dict(operator.count_ops()))

    # TODO IMPROVE AND REMOVE DOUBLING
    gates_to_decompose = gates_decomposition_sort(circuit_gates=deepcopy(existing_gates))

    while True:
        operator = operator.decompose(gates_to_decompose)

        existing_gates = list(dict(operator.count_ops()))
        # TODO IMPROVE AND REMOVE DOUBLING
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
        do_not_decompose_gates (list) - A list of gate types to remove from `circuit_gates`.
        
    Returns:
        Altered `circuit_gates` list.
    """
    
    for g in BLOCKS:
        if g in circuit_gates:
            circuit_gates.remove(g)
        
    return circuit_gates