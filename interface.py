'''
    This module contains the methods regarding the user's interface and the actual running of the algorithm.
'''

import numpy as np
from qiskit import QuantumCircuit, transpile, Aer, QuantumRegister, ClassicalRegister
from qiskit.visualization import plot_histogram

import circuit
import parse
import handle_solutions
import settings

def HandleInputs():
    
    '''
        Functionality:
            Taking inputs from the user.
            In general, a naive assumption of the program is that the user enter valid inputs only.
        Parameters:
            None.
        Returns:
            A dictionary object containing the inputs.
    '''
    
    # Annoucements
    print('This program builds and runs quantum circuits for SAT problems.')
    print('The program assumes naviely valid user inputs - invalid input formats would probably result in an error.')
    
    # Taking amount of input qubits
    print()
    input_qubits = int(input('\033[1mPlease enter the desired amount of input qubits: \033[0m'))
    
    # Taking string of constraints
    print()
    with open('constraints_format.txt') as cf:
        print(cf.read())
    constraints = str(input('\033[1mPlease enter a string of constraints: \033[0m'))
    
    # Taking desired amount of shots
    print()
    shots = int(input('\033[1mPlease enter the amount of shots desired: \033[0m'))
    
    # Taking expected amount of solutions
    print()
    print('\033[1mIf the expected amount of solutions is known, please enter it (it is the easiest and optimal case).\033[1m')
    k = int(input('\033[1mIf the expected amount of solutions is unknown, please enter the value -1.\033[0m In this case the program will look for an adequate (optimal or near optimal) number of iterations suited for the constraints (it is possible to halt after finding one solution, but in order to find a circuit that amplifies all solutions an iterative process is being implemented, it might take some time): '))
    
    return {'input_qubits': input_qubits, 'constraints': constraints, 'shots': shots, 'k': k}

def RunProgram():
    
    '''
        Functionality:
            First line to the user.
            Running the circuit and presenting the results to the user.
        Parameters:
            None.
        Returns:
            None.
    '''
    
    # User's inputs
    inputs = HandleInputs()
    
    # Obtaining the desired quantum circuit
    if inputs['k'] == -1:
        print()
        print('Please wait while the system checks various solutions..')
        iterations = handle_solutions.FindIterationsUnknown_k(n = inputs['input_qubits'], constraints = inputs['constraints'], x = 10)
        print(f'\033[1mAn adequate number of iterations found = {iterations}\033[0m')
    else:
        iterations = handle_solutions.CalcIterationsKnown_k(N = 2 ** inputs['input_qubits'], k = inputs['k'])
    circuit_data = circuit.Overall_SAT_Circuit(input_qubits = inputs['input_qubits'], constraints = inputs['constraints'], iterations = iterations)
    qc = circuit_data['sat_qc']

    # Running the program on a local simulator
    print()
    print(f'The system is running the circuit {inputs["shots"]} times, please wait..')
    job = settings.backend.run(transpile(qc, settings.backend, optimization_level = 3), shots = inputs['shots'])
    results = job.result()
    counts = results.get_counts()
    counts_sorted = sorted(counts.items(), key =  lambda x: x[1]) # Sorting results in an ascending order

    # Output the results
    print()
    print(f'\033[1mThe results for {inputs["shots"]} shots are: \033[0m')
    display(plot_histogram(counts, sort = 'value', figsize = (20,5)))
    print(counts_sorted)
    
    # Printing the circuit
    print()
    print('\033[1mThe high level circuit: \033[0m')
    display(qc.draw('mpl'))
    
    # Printing the operator's circuit
    op_qc = circuit_data['sat_op']
    print()
    print('\033[1mThe operator: \033[0m')
    display(op_qc.draw('mpl'))

    # Preparing the decomposed version of the operator's circuit
    gates = list(dict(op_qc.count_ops()).keys())
    remove_list = ['x', 'h', 'mcx', 'ccx', 'mcx_gray']
    for r in remove_list:
        try:
            gates.remove(r)
        except:
            pass
    de_op_qc = op_qc.decompose(gates_to_decompose = gates)
    gates = list(dict(de_op_qc.count_ops()).keys())
    for r in remove_list:
        try:
            gates.remove(r)
        except:
            pass

    # Printing the decomposed version of the operator's circuit
    print()
    print('\033[1mThe operator - one level down: \033[0m')
    display(de_op_qc.decompose(gates_to_decompose = gates).draw('mpl'))