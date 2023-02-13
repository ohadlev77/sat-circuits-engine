
# Constraints String Format

The program accepts a string of constraints in a *low-level* defined format. It is also possible to generate low-level constraints string from a *high-level* setting.

## Supported features
The program accepts:

* Multiple constraints combined into a single string. Each constraint must reside inside round brackets and must be separated from neighboring constraints by commas. A general description: __"(--CONSTRAINT_1--),(--CONSTRAINT_2--),...,(--CONSTRAINT_N--)"__.
* Each single constraint can be either an *arithmetic constraint* or a *boolean constraint*.
* An arithmetic constraint must contain one *comparison operator* - that is "==" (EQUAL) or "!=" (NOT EQUAL), and may contain the "+" (PLUS) *arithmetic operator* along with variables or natural numbers. A general description: __"(--LEFT_OPERAND-- --ARITHMETIC_OPERATOR-- --RIGHT_OPERAND--)"__. Each operand can possibly be a sum of sub-operands (variables or natural numbers).
* A boolean constraint must contain *binary variables* (i.e single-bit long) only, along with *boolean operators*: that can be binary - "||" (OR) and "&&" (AND), or unary - "\~" (NOT). For now, a mixture of binary boolean operators is not allowed - i.e a single constraint can contain either "&&" or "||" operators. The "~" unary operator is always allowed. A general description: __"(--VAR_0-- && --~VAR_1-- && --VAR_2--)"__ or __"(--VAR_0-- || --~VAR_1-- || --VAR_2--)"__.

The features listed above are accessible via a high-level setting or a low-level format.

## Low-level format
The low-level format specifies explicitly the bit-indexes of each variable, in a little-endian fashion (the most significant bit is the leftmost bit). Each bit index must reside inside square brackets, and natural numbers must be bare.

### Low-level examples of arithmetic constraints (each example is a single constraint):

* ([3][2] != [0])
* ([6] == [5])
* ([6][5][4] == [3])
* ([2] + 2 != [4][3])
* ([0] + [1] + [2] + [6][5][4] == 7)

### Low-level examples of boolean constraints (each example is a single constraint):

* ([7] || ~[1] || ~[0])
* ([7] && ~[1] && ~[0])
* ([3] || [2] || [1] || [0])

## High-level setting
It is possible to define constraints with variables and not worry about bits-indexing issues, using a high-level simple API defined by the class `sat_circuits_engine.interface.translator.ConstraintsTranslator`. It is required to set as inputs the constraints string with variables named as you like, along with a dictionary object that specifies how many bits each variable requires. Then the `translate` method will return a suitable low-level string.

For example, for the given code:

    vars = {'x0': 3, 'x1': 1, 'x2': 3, 'x3': 4}
    high_level_string = "(x0 != 4),(x1 + x2 == x0),(x3 + x0 + x1 + x2 != 27)"

    translator = ConstraintsTranslator(high_level_string, vars)
    low_level_string = translator.translate()

    print(low_level_string)

The output is:

    ([2][1][0] != 4),([3] + [6][5][4] == [2][1][0]),([10][9][8][7] + [2][1][0] + [3] + [6][5][4] != 27)

## Important Notes

1. Many examples may be found in [test_data.json](sat_circuits_engine/data/test_data.json).
2. The program usually naively assumes valid user inputs, i.e disobeying the defined format will probably lead to an error or wrong results.