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

from typing import Dict, Tuple, List

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
            sat_circuits_engine.util.settings.CONSTRAINTS_FORMAT_PATH - "High-level format" section.
            variables (Dict[str, int]): each key is a name of a variable, each value is its bits-length.
        """

        self.high_level_string = high_level_string
        self.variables = variables

    def translate(self) -> Tuple[Dict[str, List[int]], str]:
        """
        Translates the combination of `self.high_level_string` and `variables`
        into a low-level constraints string.
        See `sat_circuits_engine.util.settings.CONSTRAINTS_FORMAT_PATH` - "Low-level format" section
        for information about the low level format.

        Returns - Tuple[Dict[str, List[int]], str]:
            (Dict[str, List[int]]): a map of high-level variables with their allocated bit-indexes.
            (str): a low-level constraints string.
        """

        low_level_string = self.high_level_string
        high_to_low_map = {}
        bits_sum = 0

        # Iterating over the variables by their name-length, in a descending order. This way
        # we handle the variables with the longer names first and avoiding misreplaces of strings.
        for var, bits_needed in sorted(self.variables.items(), key=lambda x: len(x[0]), reverse=True):

            bundle_list, bundle_string = self.generate_bits_bundle(bits_needed, bits_sum)

            low_level_string = low_level_string.replace(var, bundle_string)
            high_to_low_map[var] = bundle_list

            bits_sum += bits_needed

        return high_to_low_map, low_level_string

    def generate_bits_bundle(self, num_bits: int, first_bit_index: int) -> Tuple[List[int], str]:
        """
        Generates a low-level format operand, a.k.a a bundle of bit-indexes in a little-endian style.

        Args:
            num_bits (int): number of bits in the bundle.
            first_bit_index (int): index number to start from.

        Returns - Tuple[List[int], str]:
            (List[int]) - The bit indexes that form the bundle, as a list.
            (str) - The bit indexes that form the bundle, already in the low-level format string.
        """

        bundle_string = ""
        bundle_list = []

        for i in reversed(range(num_bits)):
            bit_index = first_bit_index + i

            bundle_string += f"[{bit_index}]"
            bundle_list.append(bit_index)

        return bundle_list, bundle_string