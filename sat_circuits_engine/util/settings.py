import qiskit
from qiskit import IBMQ
from qiskit_aer import AerSimulator

def BACKENDS(index: int) -> qiskit.providers.backend.Backend:
    """
    Returns a backend object according to `index`.
    This "constants" are assembled as a function in order to avoid errors that may raise
    from `IBMQ.load_account()` if an IBMQ API token isn't saved on the machine.

    Raises:
        (ValueError) - if the index entered isn't associated with a backend.
    """

    if index == 0:
        return AerSimulator()
    elif index == 1:
        provider = IBMQ.load_account()
        return provider.get_backend('ibmq_qasm_simulator')
    else:
        raise ValueError(f"No backends are defined for index {index}.")

# Path to a txt file contains explanation about the supported constraints input format
CONSTRAINTS_FORMAT_PATH = "sat_circuits_engine/data/constraints_format.txt"

# Path to data directory
DATA_PATH = "sat_circuits_engine/data/generated_data/"

##### Supported operators #####
# TODO REMOVE

# Valid only once in a single constraint
EQUALITY_OPERATORS = ("==", "!=") 

# `AND` is used to connect between constraints into a set of constraints
BINARY_OPERATOS =  ("AND") 

# Can be used for each operand, soldn't be used for more than 1 operand each
UNARY_OPERATOS = ("NOT", "+")

# TODO VERIFY IN THE END IT FITS
