import unittest
import json

from sat_circuits_engine.constraints_parse import SingleConstraintParsed

class TestSingleConstraintParsed(unittest.TestCase):
    """
    TODO COMPLETE

    Methods:
        SingleConstraintParsed.__init__
        SingleConstraintParsed.parse_format
        SingleConstraintParsed.parse_equation
        SingleConstraintParsed.parse_boolean_format
        SingleConstraintParsed.parse_operand

    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        TODO COMPLETE
        """

        with open("test/constraints_parse/single_constraint_parse_test_data.json", "r") as data_file:
            cls.test_data = json.load(data_file)
        
    def test_init(self):
        """
        TODO COMPLETE
        """

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