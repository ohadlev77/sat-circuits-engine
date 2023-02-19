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
interactive_XXXX_inputs functions, to be used by the SATInterface class:
    1. interactive_operator_inputs.
    2. interactive_solutions_num_input.
    3. interactive_run_input.
    4. interactive_backend_input.
    5. interactive_shots_input.
"""

from typing import Dict, Union, Optional, List

from qiskit.providers.backend import Backend

from sat_circuits_engine.util.settings import BACKENDS
from sat_circuits_engine.interface.translator import ConstraintsTranslator

def interactive_operator_inputs() -> Dict[str, Union[int, str, Dict[str, int], Dict[str, List[int]]]]:
    """
    In an interactive interface manner, taking the necessary inputs for constructing
    GroverConstraintsOperator from the user - either in a high-level format or a low-level format.
    Annotations about "high-level" and "low-level" formats may be found in:
    sat_circuits_engine.util.settings.CONSTRAINTS_FORMAT_PATH (a pointer to a markdown annotation file).

    Returns:
        (Dict[str, Union[int, str, Dict[str, int], Dict[str, List[int]]]]):
            'num_input_qubits' (int): number of input qubits.
            'high_to_low_map' (Dict[str, List[int]]): a map of high-level variables
            with their allocated bit-indexes.
            'constraints_string' (str): a string of constraints in a "low-level" format.
            'high_level_constraints_string' (Optional[str] = None): a string of constraints
            in a "high-level" format, default is None.
            'high_level_vars' (Optional[Dict[str, int]] = None): a dictionary that configures
            the high-level variables - keys are names and values are bits-lengths. Default is None.
    """

    print()
    high_level_setting = bool(int(input(
        "For a low-level setting of constraints, enter '0'. For a high level setting, enter '1': "
    )))

    high_level_constraints_string = None
    high_level_vars = None

    # High-level constraints input
    if high_level_setting:
        print()
        high_level_constraints_string = input("Enter a high-level constraints string: ")

        print()
        high_level_vars = eval(input(
            "Enter a dictionary of variables setting in a Python syntax, " \
            "while keys are variables-names and values are bits-lengths (Dict[var, num_bits]): "
        ))

        # Translating high-level format into handleable low-level format
        num_input_qubits = sum(high_level_vars.values())
        translator = ConstraintsTranslator(high_level_constraints_string, high_level_vars)
        high_to_low_map, constraints_string = translator.translate()

    # Low-level constraints input
    else:
        print()
        num_input_qubits = int(input("Please enter the number of input qubits: "))
        
        print()
        constraints_string = str(input("Please enter a string of constraints: "))

    return {
        'num_input_qubits': num_input_qubits,
        'high_to_low_map': high_to_low_map,
        'constraints_string': constraints_string,
        'high_level_constraints_string': high_level_constraints_string,
        'high_level_vars': high_level_vars
    }

def interactive_solutions_num_input() -> Optional[int]:
    """
    In an interactive interface manner, finds out whether the user is interested in
    obtatining the overall circuit for the SAT problem. If so, takes user's input for the
    expected number of solutions to the SAT problem.

    Returns:
        (Optional[int]):
            - If None - that means the user isn't interested in the overall SAT cirucit.
            - (int): user's input for number of solutions the the SAT problem.
    """

    print()
    obtain_overall_circuit = bool(int(input(
        "To stop here, enter '0'. " \
        "For obtaining also the overall circuit, enter '1': "
    )))

    if obtain_overall_circuit:

        print()
        print(
            "If the expected amount of solutions is known, please enter it" \
            " (it is the easiest and optimal case)."
        )
        print()
        solutions_num = int(input(
            "If the expected amount of solutions is unknown, please enter the value '-1'.\n" \
            "In this case the program will look for an adequate (optimal or near optimal)\n" \
            "number of iterations for the given SAT problem, using an iterative stochastic process.\n"\
            "This process might cause significant overheads and might take some time.\n" \
            "Another option is using a dynamic circuit layout (this feature is in BETA version,\n" \
            "and suffers from bugs and poor scaling) - for this option enter the value '-2.\n" \
            "Please enter the expected number of solutions ('-1' or '-2' for unknown): "
        ))

        return solutions_num

def interactive_run_input() -> bool:
    """
    Finds out whether the user is intersted in running the overall circuit.

    Returns:
        (bool): True if the user is intersted, False otherwise.
    """

    print()
    run_circuit = bool(int(input(
        "To stop here, enter '0'. " \
        "For running the overall circuit and obtain data, enter '1': "
    )))

    return bool(int(run_circuit))

def interactive_backend_input() -> Backend:
    """
    Takes user's input for the desired backend to run the circuit upon.
    The interface defined by this function limits the user to choose from
    backends that are recognized by the BACKENDS (global-constant-like) function.
    For full flexibility a user should use the API provided by `SATInterface` rather
    than this interactive CLI.

    Returns:
        (Backend): backend object to run the circuit upon.
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

def interactive_shots_input() -> int:
    """
    Takes user's input for the desired number of execution shots.

    Returns:
        (int): user's input for number of shots.
    """

    print()
    shots = int(input("Please enter the number of shots desired: "))

    return shots