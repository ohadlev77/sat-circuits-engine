import json
from unittest import TestCase, main

from sat_circuits_engine.interface import SATInterface
from sat_circuits_engine.util.settings import BACKENDS

class SATInterfaceTest(TestCase):

    def setUp(self) -> None:
        with open("sat_circuits_engine/data/test_data.json", 'r') as data_file:
            self.test_data = json.load(data_file)

    def test_run_overall_sat_circuit(self):

        for example_name, example in self.test_data.items():
            if example['perform_test']:
                print(f"\nTesting {example_name}:")

                interface = SATInterface(
                    num_input_qubits=example['num_input_qubits'],
                    constraints_string=example['constraints_string'],
                    save_data=False
                )

                operator = interface.obtain_grover_operator()['operator']
                qc = interface.obtain_overall_sat_circuit(operator, example['num_solutions'])['circuit']
                distilled_solutions = interface.run_overall_sat_circuit(qc, BACKENDS(0) ,1024)['distilled_solutions']
                error_message = (
                    f"\nFor {example_name} - distilled solutions are different from data:\n" \
                    f"Data solutions = {example['solutions']}\n" \
                    f"Distilled solutions = {distilled_solutions}"
                )

                self.assertEqual(
                    set(example['solutions']),
                    distilled_solutions,
                    error_message
                )
            else:
                print(f"\nNot testing {example_name} (`perform_test` is defined False).")
    

if __name__ == "__main__":
    # SATInterfaceTest()
    main()