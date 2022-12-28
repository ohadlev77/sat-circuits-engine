"""
Contains the methods regarding the user's interface.
"""

import numpy as np
from qiskit import QuantumCircuit, transpile, Aer, QuantumRegister, ClassicalRegister
from qiskit.visualization import plot_histogram

from engine import Constraint, Constraints, SAT_Circuit, DiffuserOp
import handle_solutions
import settings

def handle_inputs():  
    """
    Taking inputs from the user.
    In general, a naive assumption of the program is that the user enters valid inputs only.

    Args:
        None.

    Returns:
        A dictionary object containing the inputs.
    """
    
    # Taking amount of input qubits.
    n = int(input('Please enter the desired amount of input qubits:'))
    
    # Taking string of constraints.
    print()
    with open('constraints_format.txt') as cf:
        print(cf.read())
    constraints_string = str(input('Please enter a string of constraints:'))
    
    # Taking desired amount of shots.
    shots = int(input('\nPlease enter the amount of shots desired:'))
    
    # Taking expected amount of solutions.
    print('\nIf the expected amount of solutions is known, please enter it (it is the easiest and optimal case).')
    solutions_num = int(input('If the expected amount of solutions is unknown,\
                             please enter the value -1. In this case the program will look for an adequate\
                             (optimal or near optimal) number of iterations suited for the constraints\
                             (it is possible to halt after finding one solution, but in order to find a circuit that\
                             amplifies all solutions an iterative process is being implemented, it might take some time): '))
    
    return {'n': n, 'constraints_string': constraints_string, 'shots': shots, 'solutions_num': solutions_num}

def SAT(n=None, constraints_string=None, shots=None, solutions_num=None):
    """
    Runs the program and updates the user step-by-step.
    """
    
    # If the parameters aren't stated when calling the function (even one of them):
    # calling handle_inputs() to take care of user inputs.
    if n is None or constraints_string is None or shots is None or solutions_num is None:
        inputs = handle_inputs()
        n = inputs['n']
        constraints_string = inputs['constraints_string']
        shots = inputs['shots']
        solutions_num = inputs['solutions_num']
    
    # Identifying user's IDE.
    try: # Jupyter Notebbok case.
        IDE = get_ipython().__class__.__name__
    except NameError:
        IDE = 'Unknown'
    jupyter = False
    if IDE == 'ZMQInteractiveShell':
        jupyter = True

    # Constructing Grover's operator as `constraints_ob`.
    constraints_ob = Constraints(constraints_string, n, mpl=jupyter)

    # Obtaining the desired quantum circuit.
    if solutions_num == -1: # Unknown number of solutions.
        print('\nPlease wait while the system checks various solutions..')
        data = handle_solutions.find_iterations_unknown_k(n, constraints_ob, precision = 10)
        print(f"An adequate number of iterations found = {data['iterations']}\033[0m")
        qc = data['qc']
    else: # Known number of solutions.
        iterations = handle_solutions.calc_iterations(n, solutions_num)
        qc = SAT_Circuit(n, constraints_ob, iterations)
        qc.add_input_reg_measurement()

    # Running the circuit.
    print(f'\nThe system is running the circuit {shots} times, please wait..')
    job = settings.backend.run(transpile(qc, settings.backend, optimization_level = 0), shots = shots)
    results = job.result()
    counts = results.get_counts()
    counts_sorted = sorted(counts.items(), key=lambda x: x[1]) # Sorting results in an ascending order.

    # Output the results.
    print(f'\nThe results for {shots} shots are:')
    if jupyter:
        display(plot_histogram(counts, sort='value', figsize=(20,5)))
    print(counts_sorted)
    
    # Printing the circuit.
    print('\nThe high level circuit:')
    if jupyter:
        display(qc.draw(output='mpl', fold=-1))
    else:
        print(qc.draw('text'))
    
    # Printing the operator's circuit.
    print('\nThe operator:')
    if jupyter:
        display(constraints_ob.draw(output='mpl', fold=-1))
    else:
        print(constraints_ob.draw('text'))

    # Preparing the decomposed version of the operator's circuit.
    gates = list(dict(constraints_ob.count_ops()).keys())
    remove_list = ['x', 'h', 'mcx', 'ccx', 'mcx_gray']
    gates_to_decompose = GatesDecompositionSort(circuit_gates = gates, do_not_decompose_gates = remove_list)
    de_op_qc = constraints_ob.decompose(gates_to_decompose = gates_to_decompose)
    gates = list(dict(de_op_qc.count_ops()).keys())
    gates_to_decompose = GatesDecompositionSort(circuit_gates = gates, do_not_decompose_gates = remove_list)

    # Printing the decomposed version of the operator's circuit.
    print('\nThe operator - one level down:')
    final_de_op = de_op_qc.decompose(gates_to_decompose = gates_to_decompose)
    if jupyter:
        display(final_de_op.draw(output='mpl', fold=-1))
    else:
        print(final_de_op.draw('text'))
    
def GatesDecompositionSort(circuit_gates, do_not_decompose_gates):
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