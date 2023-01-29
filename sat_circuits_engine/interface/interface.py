"""
TODO CHANGE?
Contains the methods regarding the user's interface.
"""

from copy import deepcopy
from typing import List, Tuple, Dict, Union, Optional
from sys import stdout
from IPython.display import display

from qiskit import transpile, QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit.result.counts import Counts
from qiskit.visualization.circuit.text import TextDrawing
from matplotlib.figure import Figure

from sat_circuits_engine.util import timer_dec
from sat_circuits_engine.util.settings import BACKEND, CONSTRAINTS_FORMAT_PATH
from sat_circuits_engine.circuit import GroverConstraintsOperator, SATCircuit
from sat_circuits_engine.classical_processing import find_iterations_unknown, calc_iterations, ClassicalVerifier
from sat_circuits_engine.constraints_parse import SingleConstraintParsed, ParsedConstraints

from .interactive_inputs import interactive_inputs

# ORGINZE THIS HOOK
# from qiskit import IBMQ
# provider = IBMQ.load_account()
# BACKEND_CLOUD = provider.get_backend('ibmq_qasm_simulator')

from qiskit_aer import AerSimulator
BACKEND_LOCAL = AerSimulator()

class SATInterface:
    """
    TODO COMPLETE
    """

    def __init__(
        self,
        num_input_qubits: Optional[int] = None,
        constraints_string: Optional[str] = None,  
    ) -> None:
        """
        TODO COMPLETE
        """

        self.identify_platform()

        # If the parameters aren't stated when calling the function (even one of them) - 
        # calling `interactive_inputs()` to take care of user inputs.
        if num_input_qubits is None or constraints_string is None:
            self.interactive_interface()
        else:
            self.num_input_qubits = num_input_qubits
            self.constraints_string = constraints_string
            self.parsed_constraints = ParsedConstraints(constraints_string)

            # TODO WHAT TO DO
            self.build_grover_constraints_operator()

    def interactive_interface(self):
        """
        TODO COMPLETE
        """

        # Taking inputs
        inputs = interactive_inputs()
        self.num_input_qubits = inputs['num_input_qubits']
        self.constraints_string = inputs['constraints_string']
        self.shots = inputs['shots']
        self.solutions_num = inputs['solutions_num']
        self.parsed_constraints = ParsedConstraints(self.constraints_string)

        # Creating and displaying circuits
        self.build_grover_constraints_operator()
        overall_sat_circuit = self.obtain_overall_sat_circuit(self.solutions_num)
        self.display_circuits(overall_sat_circuit)

        # Running `overall_sat_circuit` and displaying the results
        counts_parsed = self.run_overall_sat_circuit(overall_sat_circuit, self.shots)
        self.display_results(
            overall_sat_circuit,
            self.shots,
            counts_parsed['counts'],
            counts_parsed['counts_sorted'],
            counts_parsed['distilled_solutions']
        )


    def build_grover_constraints_operator(self):
        """
        TODO COMPLETE
        # Constructing Grover's operator as `grover_constraints_operator`.
        """

        self.grover_constraints_operator = GroverConstraintsOperator(
            self.parsed_constraints,
            self.num_input_qubits,
        )

    def identify_platform(self) -> None:
        """
        TODO COMPLETE
        """
        
        # If True then the platform is a terminal/command line/shell
        if stdout.isatty():
            self.jupyter = False
        # If False, we assume the platform is a Jupyter notebook
        else:
            self.jupyter = True

    def output_to_platform(
        self,
        *,
        title: str,
        output_terminal: TextDrawing,
        output_jupyter: Figure,
        display_both_on_jupyter: Optional[bool] = False
    ) -> None:
        """
        TODO COMPLETE
        """

        print()
        print(title)

        if self.jupyter:
            display(output_jupyter)

            if display_both_on_jupyter:
                print(output_terminal)
        else:
            print(output_terminal)

    def obtain_overall_sat_circuit(self, solutions_num: int) -> SATCircuit:
        """
        TODO COMPLETE
        # Obtaining the desired quantum circuit
        """
        # -1 = Unknown number of solutions - compute classically
        print()
        if solutions_num == -1:
            print('Please wait while the system checks various solutions..')

            qc, iterations = find_iterations_unknown(
                self.num_input_qubits,
                self.grover_constraints_operator,
                self.parsed_constraints,
                precision=10
            )
            
            print()
            print(f"An adequate number of iterations found = {iterations}")
        
        # -2 = Unknown number of solutions - implement a dynamic circuit
        elif solutions_num == -2:
            print('The system builds a dynamic circuit..')

            qc = SATCircuit(self.num_input_qubits, self.grover_constraints_operator, iterations=None)
            qc.add_input_reg_measurement() # TODO WHY, consider change

        # Known number of solutions
        else:
            print('The system builds the circuit..')

            iterations = calc_iterations(self.num_input_qubits, solutions_num)
            print(f"\nFor {solutions_num} solutions, {iterations} iterations needed.")

            qc = SATCircuit(self.num_input_qubits, self.grover_constraints_operator, iterations)
            qc.add_input_reg_measurement() # TODO WHY, consider change

        return qc
    
    @timer_dec("Circuit execution time = ")
    def run_overall_sat_circuit(self, qc: QuantumCircuit, shots: int) -> Tuple[Counts, List[Tuple[Union[str, int]]]]:
        """
        TODO COMPLETE
        """

        print()
        print(f"The system is running the circuit {shots} times, please wait..")

        job = BACKEND_LOCAL.run(transpile(qc, BACKEND_LOCAL), shots=shots)
        results = job.result()
        counts = results.get_counts()
        
        return self.parse_counts(counts)

    def parse_counts(self, counts):
        """
        TODO COMPLETE
        """

        # Sorting results in an a descending order
        counts_sorted = sorted(counts.items(), key=lambda x: x[1], reverse=True)

        # Generating a set of distilled verified-only solutions
        verifier = ClassicalVerifier(self.parsed_constraints)
        distilled_solutions = set()
        for count_item in counts_sorted:
            if verifier.verify(count_item[0]):
                distilled_solutions.add(count_item[0])
            else:
                break

        return {
            'counts': counts,
            'counts_sorted': counts_sorted,
            'distilled_solutions': distilled_solutions
        }

    def display_circuits(self, qc) -> None:
        """
        TODO COMPLETE
        """

        self.output_to_platform(
            title="The high level circuit:",
            output_terminal=qc.draw('text'),
            output_jupyter=qc.draw('mpl', fold=-1)
        )
    
        self.output_to_platform(
            title="The operator:",
            output_terminal=self.grover_constraints_operator.draw('text'),
            output_jupyter=self.grover_constraints_operator.draw('mpl', fold=-1)
        )

        # Preparing the decomposed version of the operator's circuit
        decomposed_operator = decompose_operator(self.grover_constraints_operator)

        # Printing the decomposed version of the operator's circuit.
        self.output_to_platform(
            title="The operator - decomposed:",
            output_terminal=decomposed_operator.draw('text'),
            output_jupyter=decomposed_operator.draw('mpl', fold=-1)
        )

        # TODO CONSIDER TO REMOVE THIS
        print()
        print(f"Operator depth: {decomposed_operator.depth()}")
        print(f"Operator gates counts: {decomposed_operator.count_ops()}")
        print()

        transpiled_operator = transpile(decomposed_operator, basis_gates=['u', 'cx'], optimization_level=3)
        print(f"Decomposed operator depth: {transpiled_operator.depth()}")
        print(f"Decomposed operator gates counts: {transpiled_operator.count_ops()}")
        print()
    
    def display_results(self, qc, shots, counts, counts_sorted, distilled_solutions) -> None:
        """
        TODO COMPLETE
        # Output the results.
        """

        output_text = f"Distilled solutions:\n{distilled_solutions}\n\nAll counts:\n{counts_sorted}"
        self.output_to_platform(
            title=f"The results for {shots} shots are:",
            output_terminal=output_text,
            output_jupyter=plot_histogram(counts, sort='value_desc', figsize=(20,5)),
            display_both_on_jupyter=True
        )

##### Consider move the following functions to another module #####

def decompose_operator(operator: GroverConstraintsOperator):
    """
    TODO COMPLETE
    # Preparing the decomposed version of the operator's circuit
    """
    
    existing_gates = list(dict(operator.count_ops()))
    gates_to_leave_untouched = [
        'x', 'h', 'mcx', 'ccx', 'rccx', 'mcx_gray', 'Uncomputation', 'QFT', 'IQFT_dg'
    ]

    # TODO IMPROVE AND REMOVE DOUBLING
    gates_to_decompose = gates_decomposition_sort(
        circuit_gates=deepcopy(existing_gates),
        do_not_decompose_gates=gates_to_leave_untouched
    )

    while True:
        operator = operator.decompose(gates_to_decompose)

        existing_gates = list(dict(operator.count_ops()))
        # TODO IMPROVE AND REMOVE DOUBLING
        gates_to_decompose_1 = gates_decomposition_sort(
            circuit_gates=deepcopy(existing_gates),
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