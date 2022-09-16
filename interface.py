'''
    This module contains the methods regarding the user's interface and the actual running of the algorithm.
'''

import numpy as np
from qiskit import QuantumCircuit, transpile, Aer, QuantumRegister, ClassicalRegister
from qiskit.visualization import plot_histogram

import circuit
import parse

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
    input_qubits = int(input('Please enter the desired amount of input qubits: '))
    
    # Taking string of constraints
    print()
    with open('constraints_format.txt') as cf:
        print(cf.read())
    constraints = str(input('Please enter a string of constraints: '))
    
    # Taking desired amount of shots
    print()
    shots = int(input('Please enter the amount of shots desired: '))
    
    # Taking expected amount of solutions
    # TODO - Remove that and replace it with methods to run the Grover SAT algorithm without former knowledge of k
    print()
    k = int(input('Please enter the expected amount of solutions k = '))
    
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
    # TODO - Remove `k` and replace it with methods to run the Grover SAT algorithm without former knowledge of k
    qc = circuit.Overall_SAT_Circuit(input_qubits = inputs['input_qubits'], constraints = inputs['constraints'], k = inputs['k'])
    
    # Printing the circuit
    print()
    print('The high level circuit:')
    display(qc.draw('mpl'))

    # Running the program on a local simulator
    sim = Aer.get_backend('aer_simulator')
    job = sim.run(transpile(qc, sim, optimization_level = 3), shots = inputs['shots'])
    results = job.result()
    counts = results.get_counts()
    counts_sorted = sorted(counts.items(), key =  lambda x: x[1]) # Sorting results in an ascending order

    # Output the results
    print()
    print(f'The results for {inputs["shots"]} shots are:')
    display(plot_histogram(counts, sort = 'value', figsize = (20,5)))
    print(counts_sorted)
