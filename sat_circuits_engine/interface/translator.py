"""
TODO COMPLETE.
"""

from typing import Dict

class ConstraintsTranslator:
    """
    TODO COMPLETE.
    """

    def __init__(self, high_level_string: str, vars: Dict[str, int]) -> None:
        """
        Args:
            high_level_string (str): A string of constraints in a format defined in
            sat_circuits_engine.util.settings.CONSTRAINTS_FORMAT_PATH - "High level format" section.
            vars (Dict[str, int]): each key is a name of a variable, each value is its bits-length.
        """

        self.high_level_string = high_level_string
        self.vars = vars

    def translate(self) -> str:
        """
        Translates the combination of `self.high_level_string` and `vars` into a low-level
        constraints string to the level of bits indexes.
        See `sat_circuits_engine.util.settings.CONSTRAINTS_FORMAT_PATH` - "Low level format" section
        for information about the low level format.

        Returns:
            (str): a low-level constraints string.
        """

        low_level_string = self.high_level_string

        bits_sum = 0
        for var, bits_needed in vars.items():
            low_level_string = low_level_string.replace(
                var,
                self.generate_bits_bundle_string(bits_needed, bits_sum)
            )

            bits_sum += bits_needed

        return low_level_string

    def generate_bits_bundle_string(self, num_bits: int, existing_bits: int) -> str:
        """
        TODO COMPLETE
        """

        string = ""

        for i in reversed(range(num_bits)):
            string += f"[{existing_bits + i}]"

        return string

# TODO REMOVE
if __name__ == "__main__":
    vars = {
        'x0': 3,
        'x1': 1,
        'x2': 3,
        'x3': 4
    }
    string = "(x0 != 4),(x1 + x2 == x0),(x3 + x0 + x1 + x2 != 27)"

    t = ConstraintsTranslator(string, vars)

    print(string)
    print(t.translate())
    print(vars)