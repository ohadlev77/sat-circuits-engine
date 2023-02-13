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
`ClassicalVerifier` class.
"""

from typing import List, Dict, Union

from sat_circuits_engine.constraints_parse import ParsedConstraints, SingleConstraintParsed

class ClassicalVerifier:
    """
    An interface for verifying if bitstrings satisfy a set of constraints.
    """

    def __init__(self, constraints: ParsedConstraints) -> None:
        """
        Args:
            constraints (ParsedConstraints): an object that contains the already parsed
            data from a set of constraints.
        """

        self.constraints = constraints.values()

    def verify(self, bitstring: str) -> bool:
        """
        Verifies whether `bitstring` satisfies all constraints, i.e if it's
        a solution for the SAT problem.

        Args:
            bitstring (str): the bitstring to check.

        Returns:
            (bool): True if `bitstring` is indeed a solution, False otherwise.
        """

        # Reversing the checked bitstring for little-endianess    
        reversed_bitstring = bitstring[::-1]

        # A flag that indicates that all constraints checked so far (right now 0) are satisfied
        still_satisfied = True

        for constraint in self.constraints:
            sides_sum = []

            # Summing values for each side of the constraint's equation
            for bit_indexes, int_bitstring  in zip(
                constraint.sides_bit_indexes,
                constraint.sides_int_bitstrings
            ):
                sum = 0

                # Integer value
                if int_bitstring is not None:
                    sum += int(int_bitstring, 2)

                # Bits values
                for bundle in bit_indexes:
                    bits_values = ''.join(list(map(lambda x: reversed_bitstring[x], bundle)))
                    sum += int(bits_values, 2)
                
                sides_sum.append(sum)
            
            # Writing True to still_satisfied if the constraint has been satisfied, False otherwise
            still_satisfied = sides_sum[0] == sides_sum[1]
            if constraint.operator == '!=':
                still_satisfied = not still_satisfied
            
            # Latest constraint is not satisfied
            if not still_satisfied:
                return False
        
        # Went over all constraints, all satisfied
        return True