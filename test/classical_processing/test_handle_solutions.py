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

"""Tests for the `handle_solutions` module."""

import json
import unittest

from sat_circuits_engine.util.settings import TEST_DATA_PATH
from sat_circuits_engine.classical_processing import calc_iterations, find_iterations_unknown
from sat_circuits_engine.circuit import GroverConstraintsOperator
from sat_circuits_engine.constraints_parse import ParsedConstraints


class HandleSolutionsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """Loads test data into `self.test_data`."""

        with open(TEST_DATA_PATH, "r") as test_data_file:
            cls.test_data = json.load(test_data_file)

    def test_calc_iterations(self):
        """Tests the `calc_iterations` function."""

        print("Tests `calc_iterations`:")
        for example_name, example_data in self.test_data.items():
            print(f"Testing {example_name}")

            self.assertEqual(
                calc_iterations(example_data["num_input_qubits"], example_data["num_solutions"]),
                example_data["num_iterations"],
            )

    def test_find_iterations_unknown(self):
        """
        Tests the `find_iterations_unknown` function.
        In order to avoid heavy computations that might take much time, only circuits with less
        than 18 qubits total will be sampled from the test data.
        """

        light_examples = list(filter(lambda x: x[1]["num_total_qubits"] < 18, self.test_data.items()))
        num_light_examples = len(light_examples)
        fails_count = 0

        (f"Test `find_iterations_unknown`:")
        for example_name, example_data in light_examples:
            print(f"Testing {example_name}.")

            parsed_constraints = ParsedConstraints(example_data["constraints_string"])
            _, iterations = find_iterations_unknown(
                num_input_qubits=example_data["num_input_qubits"],
                grover_constraints_operator=GroverConstraintsOperator(
                    parsed_constraints, example_data["num_input_qubits"], insert_barriers=False
                ),
                parsed_constraints=parsed_constraints,
            )

            # Deviation of max(2 iterations, 10%) from the optimal number of iterations is allowed.
            try:
                self.assertAlmostEqual(
                    iterations,
                    example_data["num_iterations"],
                    delta=max(2, 0.1 * example_data["num_iterations"]),
                )
            # The process of finding an adequate number of iterations is a stochastic process, and also
            # the performance of Grover's algorithm w.r.t the number of iterations is somewhat
            # periodic - meaning that given an optimal number of iterations `t`, than there is some
            # period `p` such that `t + p`, `t + 2p`... are also optimal numbers of iterations.
            # So `find_iterations_unknown` function can sometimes yield `t + np` (n is a natural number),
            # which causes an AssertionError to be raised. The following exception considers that 20%
            # of exceptions still implies on an overall valid test for `find_iterations_unknown`.
            except AssertionError:
                fails_count += 1
                self.assertLess(
                    fails_count,
                    0.20 * num_light_examples,
                    "More than 20% of the examples tested failed."
                )

    def test_is_circuit_match(self):
        pass
        # TODO

    def test_randint_exclude(self):
        pass
        # TODO


if __name__ == "__main__":
    unittest.main()
