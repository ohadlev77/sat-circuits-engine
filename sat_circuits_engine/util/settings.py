"""
Global constants and settings.
"""

from qiskit.providers.backend import Backend
from qiskit import IBMQ
from qiskit_aer import AerSimulator

def BACKENDS(index: int) -> Backend:
    """
    Returns a backend object according to `index`.
    This "constants" are assembled as a function in order to avoid errors that may raise
    from an `IBMQ.load_account()` command if an IBMQ API token isn't saved on the machine.

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

# Paths constants
CONSTRAINTS_FORMAT_PATH = "sat_circuits_engine/data/constraints_format.md"
DATA_PATH = "sat_circuits_engine/data/generated_data/"
TEST_DATA_PATH = "sat_circuits_engine/data/test_data.json"

# Default kwargs for Qiskit's transpile
TRANSPILE_KWARGS = {'basis_gates': ['u', 'cx'], 'optimization_level': 3}