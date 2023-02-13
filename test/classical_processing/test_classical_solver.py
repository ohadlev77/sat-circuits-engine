"""
Tests for the `classical_solver` module.
Covers also the tests needed for the `classical_verifier.py` module -
if this tests go well, `classical_verifier` can be considered tested as well.
"""

import unittest
import json

from sat_circuits_engine.util.settings import TEST_DATA_PATH
from sat_circuits_engine.classical_processing import solve_classically

class ClassicalSolverTest(unittest.TestCase):
    """
    Tests for the `ClassicalSolver` class.
    """

    def setUp(self):
        """
        Loads test data into `self.test_data`.
        """

        with open(TEST_DATA_PATH, "r") as test_data_file:
            self.test_data = json.load(test_data_file)

    def test_solve_classically(self) -> None:
        """
        Tests `solve_classically` fucntion.
        """

        print("Tests classical solver and verifier:")
        for example_name, example_data in self.test_data.items():

            print(f"Tests {example_name}.")
            self.assertEqual(
                solve_classically(example_data['num_input_qubits'], example_data['constraints_string']),
                set(example_data['solutions'])
            )

if __name__ == "__main__":
    unittest.main()