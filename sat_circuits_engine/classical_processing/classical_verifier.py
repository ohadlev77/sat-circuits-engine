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

        self.constraints = list(constraints.values())

    def verify(self, bitstring: str) -> bool:
        """
        Verifies whether `bitstring` satisfies all constraints, i.e if it's
        a solution for the SAT problem.

        Args:
            bitstring (str): the bitstring to check.

        Returns:
            (bool): True if `bitstring` is indeed a solution, False otherwise.
        """

        # Reversing the checked `bitstring` (a bitstring) for little-endianess    
        reversed_bitstring = bitstring[::-1]

        # A flag that indicates that all constraints checked so far (right now 0) are satisfied
        still_satisfied = True

        # Going over the constraints
        for constraint in self.constraints:

############################
            sides_sum = []

            for side, (bit_indexes, int_bitstring) in enumerate(
                zip(constraint.sides_bit_indexes, constraint.sides_int_bitstrings)
            ):

                sum = 0

                if int_bitstring is not None:
                    sum += int(int_bitstring, 2)

                for bundle in bit_indexes:
                    bits_values = ''.join(list(map(lambda x: reversed_bitstring[x], bundle)))
                    sum += int(bits_values, 2)
                
                sides_sum.append(sum)
                
            still_satisfied = sides_sum[0] == sides_sum[1]
            if constraint.operator == '!=':
                still_satisfied = not still_satisfied
            
            # Latest constraint is not satisfied
            if not still_satisfied:
                return False
        
        # Went through all constraints, all satisfied
        return True

    def identify_constraint_balanced(
        self,
        constraint: SingleConstraintParsed
    ) -> Union[bool, Dict[str, Union[List[int], int]]]:
        """
        For the case of an unbalnced constraint, this method identifies and parses the imbalance.

        Args:
            constraint (SingleConstraintBlock): a single constraint object.

        Returns:
            Union[bool, Dict[str, Union[List[int], int]]]:
                - True - if the constraint is balanced.
                - Dict[str, Union[List[int], int]]]:
                    'long_side_bits_indexes' (List[int]): indexes of long side's bits.
                    'short_side_bits_indexes' (List[int]): indexes of short side's bits.
                    'bits_difference' (int): the difference in the number of bits between the two sides.
        """

        num_bits_left = len(constraint.left_side)
        num_bits_right = len(constraint.right_side)

        if num_bits_left == num_bits_right:
            return True

        elif num_bits_left > num_bits_right:
            long_side_bits_indexes = constraint.left_side
            short_side_bits_indexes = constraint.right_side
            bits_difference = num_bits_left - num_bits_right

        else:
            long_side_bits_indexes = constraint.right_side
            short_side_bits_indexes = constraint.left_side
            bits_difference = num_bits_right - num_bits_left

        return {
            'long_side_bits_indexes': long_side_bits_indexes,
            'short_side_bits_indexes': short_side_bits_indexes,
            'bits_difference': bits_difference
        }

    def check_balanced_constraint(
        self,
        reversed_bitstring: str,
        *,
        left_bits_indexes: List[int],
        right_bits_indexes: List[int]
    ) -> bool:
        """
        TODO FIX
        For the case that the constraint involves with equal number of bits from
        both sides of the constraint's equation:
        This method checks whether a bundle of bits (`left_bits`) are equal (if `operator` == '==')
        or aren't equal (if `operator` == '!=') to another bundle of bits (`right_bits`).

        Args:
            reversed_bitstring (str): the bitstring to check, already reversed
            (consistency with little-endianess).
            left_bits_indexes (List[int]): a list of bit indexes, from the left side
            of the constriant's equation.
            right_bits_indexes (List[int]): a list of bit indexes, from the right side
            of the constriant's equation.

        Returns:
            (bool): True if equal for `operator` == '==',
            or not equal for operator == '!=', False otherwise.
        """

        for left_bit_index, right_bit_index in zip(left_bits_indexes, right_bits_indexes):
            #TODO REMOVE FLAG
            # print(f"left_bit_index = {left_bit_index}, right_bit_index = {right_bit_index}")

            if reversed_bitstring[left_bit_index] != reversed_bitstring[right_bit_index]:
                return False
        
        return True
    
    def check_unbalanced_constraint(
        self,
        reversed_bitstring: str,
        *,
        long_side_bits_indexes: List[int],
        short_side_bits_indexes: List[int],
        bits_difference: int
    ) -> bool:
        """
        For the case that the constraint involves with unequal number of bits from
        both sides of the constraint's equation:
        This method checks whether a bundle of bits (`left_bits`) are equal (if `operator` == '==')
        or aren't equal (if `operator` == '!=') to another bundle of bits (`right_bits`).

        Args:
            # TODO FIX
            reversed_bitstring (str): the bitstring to check, already reversed
            (consistency with little-endianess).
            left_bits_indexes (List[int]): a list of bit indexes, from the left side
            of the constriant's equation.
            right_bits_indexes (List[int]): a list of bit indexes, from the right side
            of the constriant's equation.

        Returns:
            (bool): True if the value of bits in the long side
            is equal to the value of bits in the short side.
        """

        for count, long_side_bit_index in enumerate(long_side_bits_indexes):
            
            # Redunant bits aren't zeros = fail
            if count < bits_difference:
                if reversed_bitstring[long_side_bit_index] != '0':
                    return False
            
            # In the remaining bits, performs a comparison
            else:
                short_side_bit_index = short_side_bits_indexes[count - bits_difference]
                if reversed_bitstring[long_side_bit_index] != reversed_bitstring[short_side_bit_index]:
                    return False
        
        return True

#####################

# TODO REMOVE

if __name__ == '__main__':
    p = ParsedConstraints(
        '([9][8][7] == [2][1][0]),([4][3] != [2][1]),([6] == [5]),([5] == [4]),([4] != [3]),([4] == [2])'
    )

    v = ClassicalVerifier(p)

    print(v.verify('11101110111'))