"""Tests for `interface.py` module."""

import json
import unittest

from sat_circuits_engine.interface import SATInterface
from sat_circuits_engine.util.settings import BACKENDS, TEST_DATA_PATH

class SATInterfaceTest(unittest.TestCase):
    """Tests for the `SATInterface` class."""

    @classmethod
    def setUpClass(cls):
        """Loads test data into `self.test_data`."""

        with open(TEST_DATA_PATH, "r") as data_file:
            cls.test_data = json.load(data_file)

    def test_run_overall_sat_circuit(self):
        """
        Test for the `run_overall_sat_circuit` method.
        Tests for `obtain_grover_operator` and `obtain_overall_sat_circuit` are also
        integrated seemlessly into this method.
        """

        print("Tests `SATInterface`'s functionality and `SATInterface.run_overall_sat_circuit`:")
        for example_name, example in self.test_data.items():
            if example['perform_test']:
                print(f"Testing {example_name}:")

                interface = SATInterface(
                    num_input_qubits=example['num_input_qubits'],
                    constraints_string=example['constraints_string'],
                    save_data=False
                )

                operator = interface.obtain_grover_operator()['operator']
                qc = interface.obtain_overall_sat_circuit(operator, example['num_solutions'])['circuit']
                shots = min(example['num_solutions'] * 50, 4000)
                distilled_solutions = interface.run_overall_sat_circuit(
                    qc, BACKENDS(0), shots
                )['distilled_solutions']

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
    
        # TODO NEED TO ADD MORE TESTS ALSO FOR THE SAVE_DISPLAY_XXX METHODS

if __name__ == "__main__":
    unittest.main()