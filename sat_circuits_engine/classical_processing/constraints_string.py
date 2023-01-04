"""

TODO COMPLETE

"""

from sat_circuits_engine.circuit import Constraint
def parse_constraints_string(constraints_string: str) -> None:
    """
    TOOD COMPLETE
    """

    constraints_list = constraints_string.split(",")
    constraints = []
    total_aux_qubits_needed = 0
    aux_qubits_needed_list = []

    for c_index, c in enumerate(constraints_list):
        constraints.append(Constraint(c_index=c_index, c_eq=c, mpl=mpl))
        total_aux_qubits_needed += constraints[c_index].aux_qubits_needed
        aux_qubits_needed_list.append(constraints[c_index].aux_qubits_needed)
        
    out_qubits_amount = len(constraints)