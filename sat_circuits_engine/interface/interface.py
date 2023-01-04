"""
TODO CHANGE?
Contains the methods regarding the user's interface.
"""

from qiskit import transpile
from qiskit.visualization import plot_histogram

from sat_circuits_engine.util import backend
from sat_circuits_engine.circuit import GroverConstraintsOperator, SAT_Circuit
from sat_circuits_engine.classical_processing import find_iterations_unknown, calc_iterations

def handle_inputs():  
    """
    Taking inputs from the user.
    In general, a naive assumption of the program is that the user enters valid inputs only.

    Args:
        None.

    Returns:
        A dictionary object containing the inputs.
    """
    
    # Taking amount of input qubits
    num_qubits = int(input('Please enter the desired amount of input qubits: '))
    
    # Taking string of constraints
    with open("interface/constraints_format.txt", "r") as constraints_format:
        print() # TODO IMPROVE?
        print(constraints_format.read())
    constraints_string = str(input('Please enter a string of constraints: '))
    
    # Taking desired amount of shots
    # TODO is it really useful?
    shots = int(input('\nPlease enter the amount of shots desired: '))
    
    # Taking expected amount of solutions.
    # TODO FORMAT?
    print('\nIf the expected amount of solutions is known, please enter it (it is the easiest and optimal case).')
    solutions_num = int(input(f"""If the expected amount of solutions is unknown,\
 please enter the value -1.
In this case the program will look for an adequate (optimal or near optimal) number of iterations\
 suited for the constraints.
It is possible to halt after finding one solution, but in order to find a circuit that\
 amplifies all solutions an iterative process is being implemented.
It might take some time. Your input: """))
    
    return {'num_qubits': num_qubits, 'constraints_string': constraints_string,
    'shots': shots, 'solutions_num': solutions_num}

def SAT(num_qubits=None, constraints_string=None, shots=None, solutions_num=None):
    """
    Runs the program and updates the user step-by-step.
    TODO IMPROVE
    """
    
    # If the parameters aren't stated when calling the function (even one of them):
    # calling handle_inputs() to take care of user inputs.
    if num_qubits is None or constraints_string is None or shots is None or solutions_num is None:
        inputs = handle_inputs()
        num_qubits = inputs['num_qubits']
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
    constraints_ob = GroverConstraintsOperator(constraints_string, num_qubits, mpl=jupyter)

    # Obtaining the desired quantum circuit.
    if solutions_num == -1: # Unknown number of solutions.

        # TODO REMOVE
        check_m = input('For MULTIPROCESSING enter "YES", otherwise enter "NO": ')
        if check_m == 'NO':
            multiprocessing = False
        else:
            multiprocessing = True

        print('\nPlease wait while the system checks various solutions..')
        data = find_iterations_unknown(num_qubits, constraints_ob, precision = 10,
        multiprocessing=multiprocessing)
        
        print(f"\nAn adequate number of iterations found = {data['iterations']}")
        qc = data['qc']
    else: # Known number of solutions.
        iterations = calc_iterations(num_qubits, solutions_num)
        print(f"\nFor {solutions_num} solutions, {iterations} iterations needed.")
        qc = SAT_Circuit(num_qubits, constraints_ob, iterations)
        qc.add_input_reg_measurement()

    # Running the circuit.
    print(f'\nThe system is running the circuit {shots} times, please wait..')
    job = backend.run(transpile(qc, backend, optimization_level = 0), shots = shots)
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