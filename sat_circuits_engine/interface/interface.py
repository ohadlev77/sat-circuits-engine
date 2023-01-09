"""
TODO CHANGE?
Contains the methods regarding the user's interface.
"""

import copy
from typing import List, Tuple, Dict, Union, Optional

from qiskit import transpile, QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit.result.counts import Counts

from sat_circuits_engine.util import timer_dec
from sat_circuits_engine.util.settings import backend, CONSTRAINTS_FORMAT_PATH
from sat_circuits_engine.circuit import GroverConstraintsOperator, SATCircuit
from sat_circuits_engine.classical_processing import find_iterations_unknown, calc_iterations

def interactive_inputs() -> Dict[str, Union[int, str]]:
    f"""
    Taking inputs from the user.
    In general, a naive assumption of the program is that the user enters valid inputs only.

    Returns:
        (Dict[str, Union[int, str]]): A dictionary object containing the inputs:
            'num_input_qubits' (int): number of input qubits.
            'constraints_string' (str): a string of constraints following a specific format.
                - The format is defined in `sat_circuits_engine.util.settings.CONSTRAINTS_FORMAT_PATH`.
            'shots' (int): number of shots to run the circuit.
            'solutions_num' (int): expected number of solutions.
                - Can take also specific negative values, that indicates that the number of solutions
                is unknown, and:
                    ####### TODO COMPLETE EXPLANATION #######
                    `-1` = Solve the problem with a classical iterative process.
                    `-2` = Solve the problen using a dynamic circuit design.
    """
    
    # Taking amount of input qubits
    num_input_qubits = int(input('Please enter the desired amount of input qubits: '))
    
    # Taking a string of constraints
    with open(CONSTRAINTS_FORMAT_PATH, "r") as constraints_format:
        print()
        print(constraints_format.read())
    constraints_string = str(input('Please enter a string of constraints: '))
    
    # Taking desired amount of shots
    # TODO is it really useful?
    print()
    shots = int(input('Please enter the amount of shots desired: '))
    
    # Taking expected amount of solutions
    print()
    print(
        "If the expected amount of solutions is known, please enter it" \
        " (it is the easiest and optimal case)."
    )
    print()
    # TODO REPHRASE THE FOLLOWING TEXT
    solutions_num = int(input(
        "If the expected amount of solutions is unknown, please enter the value -1.\n" \
        "In this case the program will look for an adequate (optimal or near optimal)" \
        " number of iterations for the given constraints.\n" \
        "It is possible to halt after finding one solution," \
        " but in order to find a circuit that amplifies all solutions,\n" \
        "an iterative process is being implemented.\n" \
        "It might take some time. Your input: "
    ))
    
    return {
        'num_input_qubits': num_input_qubits,
        'constraints_string': constraints_string,
        'shots': shots,
        'solutions_num': solutions_num
    }

def sat_interface(
    num_input_qubits: Optional[int] = None,
    constraints_string: Optional[str] = None,
    shots: Optional[int] = None,
    solutions_num: Optional[int] = None
) -> None:
    """
    TODO COMPLETE
    """
    
    # If the parameters aren't stated when calling the function (even one of them):
    # calling `interactive_inputs()`` to take care of user inputs.
    if num_input_qubits is None or constraints_string is None or shots is None or solutions_num is None:
        inputs = interactive_inputs()
        num_input_qubits = inputs['num_input_qubits']
        constraints_string = inputs['constraints_string']
        shots = inputs['shots']
        solutions_num = inputs['solutions_num']
    
    # TODO IMPROVE?
    # Identifying user's IDE.
    try: # Jupyter Notebbok case.
        IDE = get_ipython().__class__.__name__
    except NameError:
        IDE = 'Unknown'
    jupyter = False
    if IDE == 'ZMQInteractiveShell':
        jupyter = True

    # Constructing Grover's operator as `grover_constraints_operator`.
    grover_constraints_operator = GroverConstraintsOperator(
        constraints_string,
        num_input_qubits,
        mpl=jupyter
    )

    # Obtaining the desired quantum circuit
    # -1 = Unknown number of solutions - compute classically
    print()
    if solutions_num == -1:
        print('Please wait while the system checks various solutions..')

        qc, iterations = find_iterations_unknown(
            num_input_qubits,
            grover_constraints_operator,
            precision=10
        )
        
        print()
        print(f"An adequate number of iterations found = {iterations}")
    
    # -2 = Unknown number of solutions - implement a dynamic circuit
    elif solutions_num == -2:
        print('The system builds a dynamic circuit..')

        qc = SATCircuit(num_input_qubits, grover_constraints_operator, iterations=None)
        qc.add_input_reg_measurement() # TODO WHY, consider change

    # Known number of solutions
    else:
        print('The system builds the circuit..')

        iterations = calc_iterations(num_input_qubits, solutions_num)
        print(f"\nFor {solutions_num} solutions, {iterations} iterations needed.")

        qc = SATCircuit(num_input_qubits, grover_constraints_operator, iterations)
        qc.add_input_reg_measurement() # TODO WHY, consider change

    # Printing the circuit
    print()
    print('The high level circuit:')
    if jupyter:
        display(qc.draw(output='mpl', fold=-1))
    else:
        print(qc.draw('text'))
    
    # Printing the operator's circuit
    print()
    print('The operator:')
    if jupyter:
        display(grover_constraints_operator.draw(output='mpl', fold=-1))
    else:
        print(grover_constraints_operator.draw('text'))

    # Preparing the decomposed version of the operator's circuit
    decomposed_operator = decompose_operator(grover_constraints_operator)

    # Printing the decomposed version of the operator's circuit.
    print('\nThe operator - one level down:')
    if jupyter:
        display(decomposed_operator.draw(output='mpl', fold=-1))
    else:
        print(decomposed_operator.draw('text'))

    # Running the circuit.
    print()
    print(f'The system is running the circuit {shots} times, please wait..')
    counts, counts_sorted = run_circuit(qc, shots)

    # Output the results.
    print()
    print(f'The results for {shots} shots are:')
    if jupyter:
        display(plot_histogram(counts, sort='value', figsize=(20,5)))
    print(counts_sorted)

    print()
    print(f"Operator depth: {decomposed_operator.depth()}")
    print(f"Operator gates counts: {decomposed_operator.count_ops()}")
    print()

    deep_decomposed_operator = decomposed_operator.decompose(reps=2)
    print(f"Decomposed operator depth: {deep_decomposed_operator.depth()}")
    print(f"Decomposed operator gates counts: {deep_decomposed_operator.count_ops()}")
    print()

def decompose_operator(operator: GroverConstraintsOperator):
    """
    TODO COMPLETE
    # Preparing the decomposed version of the operator's circuit
    """
    
    existing_gates = list(dict(operator.count_ops()))
    gates_to_leave_untouched = ['x', 'h', 'mcx', 'ccx', 'rccx', 'mcx_gray', 'Uncomputation']

    # TODO IMPROVE AND REMOVE DOUBLING
    gates_to_decompose = gates_decomposition_sort(
        circuit_gates=copy.deepcopy(existing_gates),
        do_not_decompose_gates=gates_to_leave_untouched
    )

    while True:
        operator = operator.decompose(gates_to_decompose)

        existing_gates = list(dict(operator.count_ops()))
        # TODO IMPROVE AND REMOVE DOUBLING
        gates_to_decompose_1 = gates_decomposition_sort(
            circuit_gates=copy.deepcopy(existing_gates),
            do_not_decompose_gates=gates_to_leave_untouched
        )

        if gates_to_decompose_1 == gates_to_decompose:
            break
        else:
            gates_to_decompose = gates_to_decompose_1

    return operator

def gates_decomposition_sort(circuit_gates, do_not_decompose_gates):
    """
    Removes chosen gates from a list of gate types.

    Args:
        circuit_gates (list) - A list gate types.
        do_not_decompose_gates (list) - A list of gate types to remove from `circuit_gates`.
        
    Returns:
        Altered `circuit_gates` list.
    """
    
    for g in do_not_decompose_gates:
        try:
            circuit_gates.remove(g)
        except ValueError:
            pass
        
    return circuit_gates

@timer_dec
def run_circuit(qc: QuantumCircuit, shots: int) -> Tuple[Counts, List[Tuple[Union[str, int]]]]:
    """
    TODO COMPLETE
    """

    job = backend.run(transpile(qc, backend, optimization_level = 0), shots = shots)
    results = job.result()
    counts = results.get_counts()
    counts_sorted = sorted(counts.items(), key=lambda x: x[1]) # Sorting results in an ascending order.

    return counts, counts_sorted