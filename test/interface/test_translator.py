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

"""Tests for `translator.py` module."""

import unittest
import json

from sat_circuits_engine.util.settings import TEST_DATA_PATH
from sat_circuits_engine.interface.translator import ConstraintsTranslator

class ConstraintsTranslatorTest(unittest.TestCase):
    """Tests for `ConstraintsTranslator` class"""

    def setUp(self):
        """
        Loads test data and filters just the examples with high-level constraints definitions.
        Saves the filtered output to `self.examples_to_test`.
        """

        with open(TEST_DATA_PATH, 'r') as data_file:
            self.test_data = json.load(data_file)
        
        self.examples_to_test = filter(
            lambda x: "high_level_vars" in x[1].keys(),
            self.test_data.items()
        )

    def test_translate(self):
        """Test for the `translate` method."""

        print("Tests `ConstraintsTranslator.translate` method:")
        for example_name, example in self.examples_to_test:    
            print(f"Tests {example_name}.")
            
            translator = ConstraintsTranslator(
                example['high_level_constraints_string'],
                example['high_level_vars']
            )

            self.assertEqual(
                translator.translate(), example['constraints_string'], f"Fail in {example_name}."
            )

if __name__ == "__main__":
    unittest.main()