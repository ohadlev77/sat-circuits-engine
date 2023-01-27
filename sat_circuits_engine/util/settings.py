from qiskit_aer import AerSimulator
from qiskit import IBMQ

# Default backend for this package
BACKEND = AerSimulator()
# provider = IBMQ.load_account()
# BACKEND = provider.get_backend('ibmq_qasm_simulator')

# Path to a txt file contains explanation about the supported constraints input format
CONSTRAINTS_FORMAT_PATH = "interface/constraints_format.txt"

##### Supported operators #####

# Valid only once in a single constraint
EQUALITY_OPERATORS = ("==", "!=") 

# `AND` is used to connect between constraints into a set of constraints
BINARY_OPERATOS =  ("AND") 

# Can be used for each operand, soldn't be used for more than 1 operand each
UNARY_OPERATOS = ("NOT", "+")

# TODO VERIFY IN THE END IT FITS
