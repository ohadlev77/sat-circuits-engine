from qiskit_aer import AerSimulator

# Default backend for this package
BACKEND = AerSimulator()

# Path to a txt file contains explanation about the supported constraints input format
CONSTRAINTS_FORMAT_PATH = "sat_circuits_engine/interface/constraints_format.txt"

##### Supported operators #####

# Valid only once in a single constraint
EQUALITY_OPERATORS = ("==", "!=") 

# `AND` is used to connect between constraints into a set of constraints
BINARY_OPERATOS =  ("AND") 

# Can be used for each operand, soldn't be used for more than 1 operand each
UNARY_OPERATOS = ("NOT", "+")

# TODO VERIFY IN THE END IT FITS
