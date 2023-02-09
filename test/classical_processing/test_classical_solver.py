import unittest
import json

from sat_circuits_engine.util.settings import TEST_DATA_PATH
from sat_circuits_engine.classical_processing import solve_classically

class ClassicalSolverTest(unittest.TestCase):
    """
    Tests for `sat_circuits_engine/classical_processing/classical_solver.py` module.
    Cover also the `sat_circuits_engine/classical_processing/classical_verifier.py` module -
    if this tests go well, `classical_verifier` can be considered as tested as well.
    """

    def setUp(self) -> None:
        """
        Loads test data to test against.
        """

        with open(TEST_DATA_PATH, "r") as test_data_file:
            self.test_data = json.load(test_data_file)

    def test_solve_classically(self) -> None:
        """
        Tests `solve_calssically` fucntion.
        """

        for example_name, example_data in self.test_data.items():

            print(f"Test classical solver for {example_name}")
            self.assertEqual(
                solve_classically(example_data['num_input_qubits'], example_data['constraints_string']),
                set(example_data['solutions'])
            )

# TODO how to run tests
if __name__ == "__main__":
    unittest.main()