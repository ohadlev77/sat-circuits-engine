"""
TODO COMPLETE   
"""

from typing import Dict, Union

from sat_circuits_engine.util.settings import CONSTRAINTS_FORMAT_PATH

def interactive_inputs() -> Dict[str, Union[int, str]]:
    """
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