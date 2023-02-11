import json
import unittest

from sat_circuits_engine.util.settings import TEST_DATA_PATH
from sat_circuits_engine.classical_processing import calc_iterations, find_iterations_unknown
from sat_circuits_engine.circuit import GroverConstraintsOperator
from sat_circuits_engine.constraints_parse import ParsedConstraints

class InterfaceTest(unittest.TestCase):


    @classmethod
    def setUpClass(cls) -> None:
        with open(TEST_DATA_PATH, "r") as test_data_file:
            cls.test_data = json.load(test_data_file)

    def test_calc_iterations(self):
        for example_name, example_data in self.test_data.items():

            print(f"Test calc_iterations for {example_name}")

            self.assertEqual(
                calc_iterations(example_data['num_input_qubits'], example_data['num_solutions']),
                example_data['num_iterations']
            )

    def test_find_iterations_unknown(self):
        for example_name, example_data in self.test_data.items():

            if example_data['perform_test']:
                print(f"Test find_iterations_unknown for {example_name}")

                parsed_constraints = ParsedConstraints(example_data['constraints_string'])
                _, iterations = find_iterations_unknown(
                    num_input_qubits=example_data['num_input_qubits'],
                    grover_constraints_operator=GroverConstraintsOperator(
                        parsed_constraints,
                        example_data['num_input_qubits'],
                        insert_barriers=False
                    ),
                    parsed_constraints=parsed_constraints
                )

                self.assertAlmostEqual(
                    iterations,
                    example_data['num_iterations'],
                    delta=max(2, 0.1*example_data['num_iterations'])
                )
            else:
                print(f"Not testing {example_name} (`perform_test` is defined False).")
    
    def test_is_circuit_match(self):
        pass

    def test_randint_exclude(self):
        pass

if __name__ == "__main__":
    unittest.main()