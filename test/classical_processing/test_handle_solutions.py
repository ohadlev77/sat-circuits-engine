import os
import sys
sys.path.append(os.getcwd()) # '/home/ohad/work/SAT_Circuits_Engine/'
import json
from unittest import TestCase, main

from handle_solutions import (
    calc_iterations,
    find_iterations_unknown_k,
    check_solution
)
from engine import Constraints

class InterfaceTest(TestCase):

    def setUp(self):
        with open("test_data.json", 'r') as test_data:
            self.test_data = json.load(test_data)

    def test_calc_iterations(self):
        for example in self.test_data.values():
            self.assertEqual(calc_iterations(example['num_qubits'], example['num_solutions']),
            example['num_iterations'])

    def test_find_iterations_unknown_k(self):
        pass
        # TODO COMPLETE - COULD BE LING TEST AND INEXACT
    
    def test_check_solution(self):
        for example in self.test_data.values():
            is_solution_list = list(map(lambda bit_string: check_solution(bit_string,
            Constraints(example['constraints_string'], example['num_qubits']).constraints),
            example['solutions']))

            self.assertTrue(all(is_solution_list))

if __name__ == "__main__":
    main()


