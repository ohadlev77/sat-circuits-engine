"""Tests for the `single_constraints_parse` module.`"""

import unittest
import json

from sat_circuits_engine.constraints_parse import SingleConstraintParsed

class TestSingleConstraintParsed(unittest.TestCase):
    """Tests for the SingleConstraintParsed class."""

    def setUp(self):
        """
        Loads test data into `self.test_data`.
        """

        with open("test/constraints_parse/single_constraint_parse_test_data.json", "r") as data_file:
            self.test_data = json.load(data_file)
        
    def test_init(self):
        """
        The whole functionality of the `SingleConstraintParsed` class and its methods
        is encapsulated in this test, due to the structure of the `SingleConstraintParsed` class.
        """

        print("Tests `SingleConstraintParsed` class:")
        for test_name, test_case in self.test_data.items():
            print(f"Tests {test_name}.")
                
            self.assertEqual(
                SingleConstraintParsed(
                    test_case['constraint_string'],
                    0,
                    test_case['string_to_show']
                ).__dict__,
                test_case
            )

if __name__ == "__main__":
    unittest.main()