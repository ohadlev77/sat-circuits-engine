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