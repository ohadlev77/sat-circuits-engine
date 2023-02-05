"""
`interactive_inputs` function.
"""

from typing import Dict, Union

import qiskit

from sat_circuits_engine.util.settings import CONSTRAINTS_FORMAT_PATH, BACKENDS

def interactive_operator_inputs():
    """
    """

    # Taking number of input qubits
    print()
    num_input_qubits = int(input("Please enter the number of input qubits: "))
    
    # Taking a string of constraints
    print()
    constraints_string = str(input("Please enter a string of constraints: "))

    return {
        'num_input_qubits': num_input_qubits,
        'constraints_string': constraints_string
    }

def interactive_solutions_num_input():
    """
    """

    print()
    obtain_overall_circuit = bool(int(input(
        "To stop here, enter '0'. " \
        "For obtaining also the overall circuit, enter '1': "
    )))

    if obtain_overall_circuit:

        # Taking expected amount of solutions
        print()
        print(
            "If the expected amount of solutions is known, please enter it" \
            " (it is the easiest and optimal case)."
        )
        print()
        # TODO REPHRASE THE FOLLOWING TEXT FOR DYNAMIC CIRCUIT OPTION
        solutions_num = int(input(
            "If the expected amount of solutions is unknown, please enter the value '-1'.\n" \
            "In this case the program will look for an adequate (optimal or near optimal)\n" \
            "number of iterations for the given SAT problem, using an iterative stochastic process.\n"\
            "This process might cause significant overheads and might take some time.\n" \
            "Please enter the expected number of solutions ('-1' for unknown): "
        ))

        return solutions_num

def interactive_run_input():
    """
    """

    # Finding out whether the user is intersted in running the overall circuit
    print()
    run_circuit = bool(int(input(
        "To stop here, enter '0'. " \
        "For running the overall circuit and obtain data, enter '1': "
    )))

    return bool(int(run_circuit))

def interactive_backend_input():
    """
    """

    print()
    backend = BACKENDS(int(input(
        "For running the circuit on local `aer_simulator`, enter '0'.\n" \
        "For running the circuit on `ibmq_qasm_simulator` via cloud, enter '1'.\n" \
        "NOTE: A saved IBMQ API token need to be available on your machine for option '1'.\n" \
        "For other custom backends please use the API and not this interactive interface.\n" \
        "Your input: "
    )))

    print()
    print(f"Obtaining {backend}..")

    return backend

def interactive_shots_input():
    """
    """

    print()
    shots = int(input('Please enter the number of shots desired: '))

    return shots

def interactive_inputs() -> Dict[str, Union[int, str, qiskit.providers.backend.Backend, None]]:
    """
    Taking inputs from a user, in an interactive (though somewhat limited) manner.
    For no limits at all a user should use the API of `sat_circuits_engine.interface.SATInterface`.

    Returns:
        (Dict[str, Union[int, str, qiskit.providers.backend.Backend]]):
            'num_input_qubits' (int): number of input qubits.
            'constraints_string' (str): a string of constraints following a specific format.
                - The format is defined in `sat_circuits_engine.util.settings.CONSTRAINTS_FORMAT_PATH`.
            'solutions_num' (Optional[int] = None):
                - Expected number of solutions.
                - Can take also specific negative values, that indicates that the number of solutions
                is unknown, and:
                    `-1` = Solve the problem using a classical iterative stochastic process.
                    See `sat_circuits_engine.classical_processing.handle_solutions` for more details.
                - If None (default) = not defined by user.
            'backend' (Optional[qiskit.providers.backend.Backend] = None):
                - Backend to run the circuit onto.
                - If None (default) = not defined by user.
            'shots' (Optional[int] = None):
                - Number of shots to run the circuit.
                - If None (default) = not defined by user.
    """
    
    pass