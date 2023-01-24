"""
This module contains the `SingleConstraintParsed` class.
"""

from typing import List, Union

class SingleConstraintParsed:
    """
    Provides an interface for converting a string of single constraint, written in a specific
    format to a `SingleConstraintParsed` object that defines a specific API.
     - See `sat_circuits_engine/interface/constraints_format.txt` for format details.

    The API is defined by the instance attributes for a single constraint generated by this class:
        constraint_index (int): the index number of the constraint.
        constraint_string (str): the constraint's equation.
        operator (str): the comparison operator of the constraint.
        left_side_content, right_side_content (List[Union[int, str, Dict[str, [REPEAT RECURSIVELY]]]]):
            - the parsed content of the left or right side of the constraint's equation.
            - (int) are bit indexes.
            - (str) are bitstrings represent some numeric decimal value ('11' = 3)
            - (Dict) represents an arithmetic operation - while the key is the arithmetic operator, and
            the values are the operands, which can be integers, strings or dictionaries, with the same
            logic applies recursively.
        composed_list_flag (Dict[str, bool]): {'left': (bool), 'right': (bool)}
            - True if either of the sides contains an addition operation, False otherwise
    """
    
    def __init__(self, constraint_string: str, constraint_index: int) -> None:
        """
        Args:
            constraint_index (int): the index number of the constraint.
            constraint_string (str): single constraint equation string.
                # See `/interface/constraints_format.txt` for format details.
        """
        
        self.constraint_string = constraint_string
        self.constraint_index = constraint_index

        # Parsing and setting `self.operator`
        self.parse_operator()

        # Parsing and setting of `self.left_side_content` and `self.right_side_content`
        self.parse_sides() 
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.constraint_string}')"
    
    def parse_operator(self) -> None:
        """
        TODO FIX
        Given a single constraint string, this method parses its operator,
        and saves it to the instance variable - `self.operator` (str).

        Raises:
            ValueError: if the operator parsed from `self.constraint_string` is not '==' or '!='.
        """
                
        if "==" in self.constraint_string:
            self.operator = "=="
        elif "!=" in self.constraint_string:
            self.operator = "!="
        elif "||" in self.constraint_string:
            self.parse_boolean_constraint()
        else:
            raise ValueError("Not a valid constraint string - an operator is missing.")
            
    def parse_boolean_constraint(self) -> None:
        """
        TODO COMPLETE
        """

        splitted_constraint = self.constraint_string.split("||")
        not_equal_to_string = 0

        for bit_index, var in enumerate(splitted_constraint):
            if "~" in var:
                not_equal_to_string += 2 ** ((len(splitted_constraint) - 1) - bit_index)

        self.constraint_string = f"{self.constraint_string.replace('||', '')} != {not_equal_to_string}"
        self.parse_operator()


    def parse_sides(self) -> None:
        """
         Given a single constraint string equation, this method parses the two sides of the string,
         according to the defined format (see class docstrings).

         Defines the instance varaibles:
            `self.left_side` (List[int]): a list of indexes of qubits from the left
            side of `constraint_string`.
            `self.right_side` (List[int]): a list of indexes of qubits from the right
            side of `constraint_string`.

        # TODO HANDLE
        List[Dict[str, List[Union[int, str]]]]

        """
        
        # Stripping off parentheses
        stripped_string = self.constraint_string.strip('()')
        
        # Splitting the constraint into its two sides
        splitted_equation = stripped_string.split(self.operator)

        # Initiating 
        self.left_side_content = []
        self.right_side_content = []
        
        for side_content, side_string in zip([self.left_side_content, self.right_side_content], splitted_equation):
            
            # Checking for internal operators in each side TODO ADD COMMENTS
            if side_string.count('+') == 0:
                side_content.append(self.parse_operand(side_string))
            else:
                for operand in side_string.split('+'):
                    side_content.append(self.parse_operand(operand))
    
    def parse_operand(self, operand_string: str) -> Union[List[int], str]:
        """
        Parses a single operand's string.

        Args:
            operand_string (str): a single operand's string.

        Returns:
            (Union[List[int], str]):
                - A list of integers for bit indexes.
                - A string for binary value of a bare integer value.
        """

        # The case where the operand is a bare integer
        if operand_string.count("[") == 0:
            return bin(int(operand_string))[2:]

        # The case where the operand is a collection of 1 or more bit indexes
        else:
            bit_indexes = []

            for part in operand_string.split("["):
                
                # TODO FIX PROBLEM WITH SPACES

                if len(part) > 1:
                    end_index = part.index("]")
                    bit_indexes.append(int(part[:end_index]))
            
            return bit_indexes


# TODO REMOVE
if __name__ == "__main__":

    # pc = SingleConstraintParsed("([4][3][2] != [0])", 1)
    # pc = SingleConstraintParsed("(~[4] || [0] || ~[2])", 1)
    # pc = SingleConstraintParsed("([2] == [0])", 1)
    pc = SingleConstraintParsed("([33][2] + [1][0] == 4)", 1)

    print(pc.constraint_string)
    print(pc.left_side_content)
    print(pc.right_side_content)