# c = '([0] != [1]),([2] + 2 != [4][3]),([4][3] != [5]),([1] != [4][3]),([4][3] != [6]),([6] != [7]),' \
#     '([0] != [2]),([1] != [6]),([5] != [7]),([4][3] == 2),([2] + [5] + [4][3] == 3)'


def parse_operand(operand_string: str):
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
        
c = "([2] + [5] + [4][3] + 36567523 == 3 + [8][7][6][5] + [1])"

stripped_string = c.strip('()')
splitted_equation = stripped_string.split("==")

# Initiating
sides_bit_indexes = []
sides_int_bitstrings = []

for side_num, side_string in enumerate(splitted_equation):
    
    operands = side_string.split('+')

    sides_bit_indexes.append(
        tuple(
            map(parse_operand, filter(lambda x: isinstance(parse_operand(x), list), operands))
        )
    )

    sides_int_bitstrings.append(
        tuple(
            map(parse_operand, filter(lambda x: isinstance(parse_operand(x), str), operands))
        )
    )
    
print(sides_bit_indexes)
print()
print(sides_int_bitstrings)
    #
    # for operand in side_string.split('+'):
    #     print(parse_operand(operand))
    # else:
    #     print('AAA')
        
    # Checking for internal operators in each side TODO ADD COMMENTS
    # if side_string.count('+') == 0:
    #     side_content.append(self.parse_operand(side_string))
    # else:
    #     for operand in side_string.split('+'):
    #         side_content.append(self.parse_operand(operand))