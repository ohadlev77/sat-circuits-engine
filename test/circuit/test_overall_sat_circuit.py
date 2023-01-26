import json
from unittest import TestCase, main

from qiskit import transpile

from sat_circuits_engine.constraints_parse import ParsedConstraints
from sat_circuits_engine.circuit import SATCircuit, GroverConstraintsOperator
from sat_circuits_engine.util.settings import BACKEND

class SATInterfaceTest(TestCase):

    def setUp(self) -> None:
        with open("sat_circuits_engine/data/test_data.json", 'r') as data_file:
            self.test_data = json.load(data_file)

    def test_run_overall_sat_circuit(self):

        for example_name, example in self.test_data.items():
            if example['perform_test']:
                print(f"\nTesting {example_name}:")

                parsed_constraints = ParsedConstraints(example['constraints_string'])
                operator = GroverConstraintsOperator(parsed_constraints, example['num_input_qubits'])

                circuit = SATCircuit(
                    num_input_qubits=example['num_input_qubits'],
                    grover_constraints_operator=operator,
                    iterations=example['num_iterations']
                )
                circuit.add_input_reg_measurement()

                counts = BACKEND.run(transpile(circuit, BACKEND)).result().get_counts()
                counts_sorted = sorted(counts.items(), key=lambda x: x[1], reverse=True)
                counts_trimmed = counts_sorted[:example['num_solutions']]
                distilled_bitstrings = list(map(lambda x: x[0], counts_trimmed))

                # TODO REMOVE    
                # print()
                # print()
                # print(circuit.draw())
                # print(operator.draw())

                # l = list(operator.count_ops().keys())
                # try:
                #     l.remove('ccx')
                #     l.remove('Uncomputation')
                #     l.remove('rccx')
                # except ValueError:
                #     pass

                # print()
                # print(operator.decompose(gates_to_decompose=l).decompose(gates_to_decompose=['110_encoding']).draw())
                # print()
                # print()

                print(example['constraints_string'])
                print()
                
                # print(counts)
                # print()
                print(f"counts_sorted = {counts_sorted}")
                print()
                print(f"counts_trimmed = {counts_trimmed}")

                # print()
                # print(f"data_solutions = {example['solutions']}")

                for solution in example['solutions']:
                    self.assertIn(solution, distilled_bitstrings)
            else:
                print(f"\nNot testing {example_name} (`perform_test` is defined False).")
    

if __name__ == "__main__":
    main()