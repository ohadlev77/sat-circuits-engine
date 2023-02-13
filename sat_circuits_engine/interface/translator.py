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
`ConstraintsTranslator` class.
"""

from typing import Dict

class ConstraintsTranslator:
    """
    A translation interface - from "high-level" formats to a "low-level" (handleable) format.
    Annotations about "high-level" and "low-level" formats may be found in:
    sat_circuits_engine.util.settings.CONSTRAINTS_FORMAT_PATH (a pointer to a markdown annotation file).
    """

    def __init__(self, high_level_string: str, variables: Dict[str, int]) -> None:
        """
        Args:
            high_level_string (str): A string of constraints in a format defined in
            sat_circuits_engine.util.settings.CONSTRAINTS_FORMAT_PATH - "High level format" section.
            variables (Dict[str, int]): each key is a name of a variable, each value is its bits-length.
        """

        self.high_level_string = high_level_string
        self.variables = variables

    def translate(self) -> str:
        """
        Translates the combination of `self.high_level_string` and `variables`
        into a low-level constraints stringץ
        See `sat_circuits_engine.util.settings.CONSTRAINTS_FORMAT_PATH` - "Low level format" section
        for information about the low level format.

        Returns:
            (str): a low-level constraints string.
        """

        low_level_string = self.high_level_string

        bits_sum = 0
        for var, bits_needed in self.variables.items():
            low_level_string = low_level_string.replace(
                var,
                self.generate_bits_bundle_string(bits_needed, bits_sum)
            )

            bits_sum += bits_needed

        return low_level_string

    def generate_bits_bundle_string(self, num_bits: int, first_bit_index: int) -> str:
        """
        Generates a low-level format operand, a.k.a a bundle of bit-indexes in a little-endian style.

        Args:
            num_bits (int): number of bits in the bundle.
            first_bit_index (int): index number to start from.
        """

        string = ""

        for i in reversed(range(num_bits)):
            string += f"[{first_bit_index + i}]"

        return string