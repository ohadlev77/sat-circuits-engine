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