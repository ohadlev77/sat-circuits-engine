"""
SATInterface class.
"""

import os
import json
from typing import List, Tuple, Union, Optional, Dict, Any
from sys import stdout
from datetime import datetime
from hashlib import sha256

from qiskit import transpile, QuantumCircuit, qpy
from qiskit.result.counts import Counts
from qiskit.visualization.circuit.text import TextDrawing
from qiskit.providers.backend import Backend
from qiskit.transpiler.passes import RemoveBarriers
from IPython import display
from matplotlib.figure import Figure

from sat_circuits_engine.util import timer_dec, timestamp
from sat_circuits_engine.util.settings import DATA_PATH
from sat_circuits_engine.circuit import GroverConstraintsOperator, SATCircuit
from sat_circuits_engine.constraints_parse import ParsedConstraints
from sat_circuits_engine.interface.circuit_decomposition import decompose_operator
from sat_circuits_engine.interface.counts_visualization import plot_histogram
from sat_circuits_engine.interface.translator import ConstraintsTranslator
from sat_circuits_engine.classical_processing import (
    find_iterations_unknown,
    calc_iterations,
    ClassicalVerifier
)
from sat_circuits_engine.interface.interactive_inputs import (
    interactive_operator_inputs,
    interactive_solutions_num_input,
    interactive_run_input,
    interactive_backend_input,
    interactive_shots_input
)

IFRAME_WIDTH = "100%"
IFRAME_HEIGHT = "500"

class SATInterface:
    """
    An interface for building, running and mining data from n-SAT problems quantum circuits.
    There are 2 options to use this class:
        (1) Using an interactive interface (intuitive but somewhat limited) - for this
        just initiate a bare instance of this class: `SATInterface()`.
        (2) Using the API defined by this class, that includes the following methods:
            * The following descriptions are partial, for full explanations see the methods' docstrings.
            - `__init__`: an instance must be initiated with the `num_input_qubits` and
            `constraints_string` args. Otherwise the interactive interface will be called.
            - `obtain_grover_operator`:
            - `save_display_grover_operator`:
            - `obtain_overall_circuit`:
            - `save_display_overall_circuit:
            - `run_overall_circuit`:
            - `save_display_results`:

        TODO COMPLETE
    """

    def __init__(
        self,
        num_input_qubits: Optional[int] = None,
        constraints_string: Optional[str] = None,
        high_level_constraints_string: Optional[str] = None,
        high_level_vars: Optional[Dict[str, int]] = None,
        name: Optional[str] = None,
        save_data: Optional[bool] = True
    ) -> None:
        """
        Args:
            # TODO COMPLETE ARGS
            num_input_qubits (Optional[int] = None):
                - Number of input qubits.
                - If None (default) - it's a sign to launch an interactive user interface and
                get the input from there.
            constraints_string (Optional[str] = None):
                - A string of constraints, defined in a specific format (TODO FORMAT EXPLANATION).
                - If None (default) - it's a sign to launch an interactive user interface and
                get the input from there.
        """

        if name is None:
            name = "SAT"
        self.name = name

        # Creating a directory for data to be saved
        if save_data:
            self.time_created = timestamp(datetime.now())
            self.dir_path = f"{DATA_PATH}{self.time_created}_{self.name}/"
            os.mkdir(self.dir_path)
            print(f"Data will be saved into '{self.dir_path}'.")

            # Initial metadata, more to be added by this class' `save_XXX` methods
            self.metadata = {
                "name": self.name,
                "datetime": self.time_created,
                "num_input_qubits": num_input_qubits,
                "constraints_string": constraints_string,
                "high_level_constraints_string": high_level_constraints_string,
                "high_level_vars": high_level_vars
            }
            self.update_metadata()

        self.identify_platform()

        # TODO EXPLAIN WHAT NEEDED TO BE PROVIDED
        # If `num_input_qubits` or `constraints_string` aren't stated - 
        # Calling `interactive_inputs()` to take care of user inputs.
        if (
            (num_input_qubits is None or constraints_string is None)
            and
            (high_level_constraints_string is None or high_level_vars is None)
        ):
            self.interactive_interface()
        else:
            self.high_level_constraints_string = high_level_constraints_string
            self.high_level_vars = high_level_vars

            if num_input_qubits is None or constraints_string is None:
                self.num_input_qubits = sum(self.high_level_vars.values())
                self.constraints_string = ConstraintsTranslator(
                    self.high_level_constraints_string,
                    self.high_level_vars
                ).translate()

            elif num_input_qubits is not None and constraints_string is not None:
                self.num_input_qubits = num_input_qubits
                self.constraints_string = constraints_string

            else:
                raise SyntaxError(
                    "SATInterface accepts the combination of paramters:" \
                    "(high_level_constraints_string + high_level_vars) or (num_input_qubits + constraints_string). "\
                    "Exactly one combination is accepted, not both."
                )

            self.parsed_constraints = ParsedConstraints(
                self.constraints_string,
                self.high_level_constraints_string
            )

    def update_metadata(self, update_metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        TODO COMPLETE
        """

        if update_metadata is not None:
            self.metadata.update(update_metadata)    

        with open(f"{self.dir_path}metadata.json", "w") as metadata_file:
            json.dump(self.metadata, metadata_file, indent=4)

    def identify_platform(self) -> None:
        """
        Identifies user's platform.
        Writes True to `self.jupyter` for Jupyter notebook, False for terminal.
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
        output_jupyter: Union[Figure, str],
        display_both_on_jupyter: Optional[bool] = False
    ) -> None:
        """
        TODO COMPLETE
        """

        print()
        print(title)

        if self.jupyter:
            if isinstance(output_jupyter, str):
                display.display(
                    display.IFrame(output_jupyter, width=IFRAME_WIDTH, height=IFRAME_HEIGHT)
                )
            elif isinstance(output_jupyter, Figure):
                display.display(output_jupyter)
            else:
                raise TypeError(
                    "output_jupyter must be an str (path to image file) or a Figure object."
                )

            if display_both_on_jupyter:
                print(output_terminal)
        else:
            print(output_terminal)

    def interactive_interface(self) -> None:
        """
        TODO COMPLETE
        """

        # Handling operator part
        operator_inputs = interactive_operator_inputs()
        self.num_input_qubits = operator_inputs['num_input_qubits']
        self.constraints_string = operator_inputs['constraints_string']
        self.high_level_constraints_string = operator_inputs['high_level_constraints_string']
        self.high_level_vars = operator_inputs['high_level_vars']

        self.parsed_constraints = ParsedConstraints(
            self.constraints_string,
            self.high_level_constraints_string
        )
        
        self.update_metadata({
            "num_input_qubits": self.num_input_qubits,
            "constraints_string": self.constraints_string,
            "high_level_constraints_string": self.high_level_constraints_string,
            "high_level_vars": self.high_level_vars
        })

        obtain_grover_operator_output = self.obtain_grover_operator()
        self.save_display_grover_operator(obtain_grover_operator_output)

        # Handling overall circuit part
        solutions_num = interactive_solutions_num_input()

        if solutions_num is not None:
            backend = None
            if solutions_num == -1:
                backend = interactive_backend_input()

            overall_circuit_data = self.obtain_overall_sat_circuit(
                obtain_grover_operator_output['operator'],
                solutions_num,
                backend
            )
            self.save_display_overall_circuit(overall_circuit_data)

            # Handling circuit execution part
            if interactive_run_input():
                if backend is None:
                    backend = interactive_backend_input()

                shots = interactive_shots_input()

                counts_parsed = self.run_overall_sat_circuit(
                    overall_circuit_data['circuit'],
                    backend,
                    shots
                )
                self.save_display_results(counts_parsed)

        print()
        print(f"Done saving data into '{self.dir_path}'.")

    def obtain_grover_operator(
        self,
        transpile_kwargs: Optional[Dict[str, Union[Backend, List[str], int]]] = None
    ) -> Dict[str, Union[GroverConstraintsOperator, QuantumCircuit]]:
        """
        TODO COMPLETE
        # Constructing Grover's operator as `grover_constraints_operator`.
        """

        print()
        print(
            "The system synthesizes and transpiles a Grover's " \
            "operator for the given constraints. Please wait.."
        )

        # Setting default kwargs for transpiling the operator with qiskit's `transpile` function
        if transpile_kwargs is None:
            transpile_kwargs = {'basis_gates': ['u', 'cx'], 'optimization_level': 3}
        self.transpile_kwargs = transpile_kwargs

        operator = GroverConstraintsOperator(
            self.parsed_constraints,
            self.num_input_qubits,
            insert_barriers=True
        )
        decomposed_operator = decompose_operator(operator)
        no_baerriers_operator = RemoveBarriers()(operator)
        transpiled_operator = transpile(no_baerriers_operator, **transpile_kwargs)

        print("Done.")

        return {
            'operator': operator,
            'decomposed_operator': decomposed_operator,
            'transpiled_operator': transpiled_operator,
        }


    def save_display_grover_operator(
        self,
        obtain_grover_operator_output: Dict[str, Union[GroverConstraintsOperator, QuantumCircuit]],
        display: Optional[bool] = True
    ) -> None:
        """
        TODO COMPLETE
        """

        # Creating a directory to save operator's data
        operator_dir_path = f"{self.dir_path}grover_operator/"
        os.mkdir(operator_dir_path)

        # Titles for displaying objects, by order of `obtain_grover_operator_output`
        titles = [
            "The operator diagram - high level blocks:",
            "The operator diagram - decomposed:",
            f"The transpiled operator diagram saved into '{operator_dir_path}'.\n" \
            f"It's not presented here due to its complexity.\n" \
            f"Please note that barriers appear in the high-level diagrams above only for convenient\n" \
            f"visual separation between constraints.\n" \
            f"Before transpilation all barriers are removed to avoid redundant inefficiencies."
        ]

        for index, (op_name, op_obj) in enumerate(obtain_grover_operator_output.items()):

            # Generic path and name for files to be saved
            files_path = f"{operator_dir_path}{op_name}"

            # Generating a circuit diagrams figure
            figure_path = f"{files_path}.pdf"
            op_obj.draw('mpl', filename=figure_path, fold=-1)

            # Generating a QPY serialization file for the circuit object
            qpy_file_path = f"{files_path}.qpy"
            with open(qpy_file_path, "wb") as qpy_file:
                qpy.dump(op_obj, qpy_file)

            # Original high-level operator and decomposed operator
            if index < 2 and display:

                # Displaying to user
                self.output_to_platform(
                    title=titles[index],
                    output_terminal=op_obj.draw('text'),
                    output_jupyter=figure_path
                )

            # Transpiled operator
            elif index == 2:

                # Output to user, not including the circuit diagram
                print()
                print(titles[index])

                print()
                print(f"The transpilation kwargs are: {self.transpile_kwargs}.")
                transpiled_operator_depth = op_obj.depth()
                transpiled_operator_gates_count = op_obj.count_ops()
                print(f"Transpiled operator depth: {transpiled_operator_depth}.")
                print(f"Transpiled operator gates count: {transpiled_operator_gates_count}.")
                print(f"Total number of qubits: {op_obj.num_qubits}.")

                # TODO NEED TO SOLVE QASM 2.0 empty registers issue
                # Generating QASM 2.0 file only for the tranpsiled operator
                qasm_file_path = f"{files_path}.qasm"
                op_obj.qasm(filename=qasm_file_path)
            
        print()
        print(
            f"Saved into '{operator_dir_path}':\n",
            f"  Circuit diagrams for all levels.\n",
            f"  QPY serialization exports for all levels.\n",
            f"  QASM 2.0 export only for the transpiled level."
        )

        with open(f"{operator_dir_path}operator.qpy", "rb") as qpy_file:
            operator_qpy_sha256 = sha256(qpy_file.read()).hexdigest()

        self.update_metadata({
            "transpile_kwargs": self.transpile_kwargs,
            "transpiled_operator_depth": transpiled_operator_depth,
            "transpiled_operator_gates_count": transpiled_operator_gates_count,
            "operator_qpy_sha256": operator_qpy_sha256,
        })

    def obtain_overall_sat_circuit(
        self,
        grover_operator: GroverConstraintsOperator,
        solutions_num: int,
        backend: Optional[Backend] = None
    ) -> Dict[str, SATCircuit]:
        """
        TODO COMPLETE
        """

        # -1 = Unknown number of solutions - compute classically
        print()
        if solutions_num == -1:
            assert backend is not None, "Need to specify a backend if `solutions_num == -1`."

            print("Please wait while the system checks various solutions..")

            circuit, iterations = find_iterations_unknown(
                self.num_input_qubits,
                grover_operator,
                self.parsed_constraints,
                precision=10,
                backend=backend
            )
            print()
            print(f"An adequate number of iterations found = {iterations}.")
        
        # -2 = Unknown number of solutions - implement a dynamic circuit
        # TODO this functionality isn't fully implemented yet
        elif solutions_num == -2:
            print("The system builds a dynamic circuit..")

            circuit = SATCircuit(self.num_input_qubits, grover_operator, iterations=None)
            circuit.add_input_reg_measurement()

        # Known number of solutions
        else:
            print("The system builds the overall circuit..")

            iterations = calc_iterations(self.num_input_qubits, solutions_num)
            print(f"\nFor {solutions_num} solutions, {iterations} iterations needed.")

            # TODO DECIDE ON BARRIERS
            circuit = SATCircuit(self.num_input_qubits, grover_operator, iterations, barriers=False)
            circuit.add_input_reg_measurement()

        # Obtaining a SATCircuit object with one iteration for concise representation
        concise_circuit = SATCircuit(self.num_input_qubits, grover_operator, iterations=1)
        concise_circuit.add_input_reg_measurement()

        self.iterations = iterations

        return {'circuit': circuit, 'concise_circuit': concise_circuit}

    def save_display_overall_circuit(
        self,
        obtain_overall_sat_circuit_output: Dict[str, SATCircuit],
        display: Optional[bool] = True
    ) -> None:
        """
        TODO COMPLETE
        """

        circuit = obtain_overall_sat_circuit_output['circuit']
        concise_circuit = obtain_overall_sat_circuit_output['concise_circuit']

        # Creating a directory to save overall circuit's data
        overall_circuit_dir_path = f"{self.dir_path}overall_circuit/"
        os.mkdir(overall_circuit_dir_path)

        # Generating a figure of the overall SAT circuit with just 1 iteration (i.e "concise")
        concise_circuit_fig_path = f"{overall_circuit_dir_path}overall_circuit_1_iteration.pdf"
        concise_circuit.draw('mpl', filename=concise_circuit_fig_path ,fold=-1)

        # Displaying the concise circuit to user
        if display:
            self.output_to_platform(
                title= (
                    f"The high level circuit contains {self.iterations}" \
                    f"iterations of the following form:"
                ),
                output_terminal=concise_circuit.draw("text"),
                output_jupyter=concise_circuit_fig_path
            )

        print()
        print("Exporting the full high-level overall SAT circuit object to a QPY file..")
        qpy_file_path = f"{overall_circuit_dir_path}overall_circuit.qpy"
        with open(qpy_file_path, "wb") as qpy_file:
            qpy.dump(circuit, qpy_file)

        print()
        print(
            f"Saved into '{overall_circuit_dir_path}':\n",
            f"  A concised (1 iteration) circuit diagram of the high-level overall SAT circuit.\n",
            f"  QPY serialization export for the full overall SAT circuit object."
        )

        self.update_metadata({
            "num_total_qubits": circuit.num_qubits,
            "num_iterations": circuit.iterations,
        })
        
    @timer_dec("Circuit simulation execution time = ")
    def run_overall_sat_circuit(
        self,
        circuit: QuantumCircuit,
        backend: Backend,
        shots: int
    ) -> Dict[str, Union[Counts, set]]:
        """
        TODO COMPLETE
        """

        self.backend = backend

        print()
        print(f"The system is running the circuit {shots} times on {backend}, please wait..")
        print("This process might take a while.")

        job = backend.run(transpile(circuit, backend), shots=shots)
        counts = job.result().get_counts()
        parsed_counts = self.parse_counts(counts)

        self.shots = shots
        return parsed_counts

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
            if not verifier.verify(count_item[0]):
                break
            distilled_solutions.add(count_item[0])

        return {
            'counts': counts,
            'counts_sorted': counts_sorted,
            'distilled_solutions': distilled_solutions
        }
    
    def save_display_results(
        self,
        run_overall_sat_circuit_output: Dict[str, Union[set, Counts, List[Tuple[Union[str, int]]]]],
        display: Optional[bool] = True
    ) -> None:
        """
        TODO COMPLETE
        """
        
        counts = run_overall_sat_circuit_output['counts']
        counts_sorted = run_overall_sat_circuit_output['counts_sorted']
        distilled_solutions = run_overall_sat_circuit_output['distilled_solutions']

        # Creating a directory to save results data
        results_dir_path = f"{self.dir_path}results/"
        os.mkdir(results_dir_path)

        histogram_path = f"{results_dir_path}histogram.pdf"

        # Defining custiom dimensions for the custom `plot_histogram` of this package
        histogram_fig_width = max((len(counts) * self.num_input_qubits * (10 / 72)), 7)
        histogram_fig_height = 5
        histogram_figsize = (histogram_fig_width, histogram_fig_height)

        plot_histogram(
            counts,
            figsize=histogram_figsize,
            sort='value_desc',
            filename=histogram_path
        )

        if display:
            output_text = f"\nDistilled solutions ({len(distilled_solutions)} total):\n" \
                          f"{distilled_solutions}\n\n" \
                          f"All counts:\n{counts_sorted}"
                          
            self.output_to_platform(
                title=f"The results for {self.shots} shots are:",
                output_terminal=output_text,
                output_jupyter=histogram_path,
                display_both_on_jupyter=True
            )

        results_dict = {'solutions': list(distilled_solutions), 'counts': counts}
        with open(f"{results_dir_path}results.json", "w") as results_file:
            json.dump(results_dict, results_file, indent=4)

        self.update_metadata({
            "num_solutions": len(distilled_solutions),
            "backend": self.backend.__str__(),
            "shots": self.shots
        })

################  REMOVE
if __name__ == "__main__":
    SATInterface()