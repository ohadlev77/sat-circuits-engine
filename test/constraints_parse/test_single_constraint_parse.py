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