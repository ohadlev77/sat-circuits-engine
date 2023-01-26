import numpy as np

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import QFT
from qiskit.quantum_info import Pauli
from qiskit_aer import AerSimulator

def fourier_add(reg1_qubits, reg2_qubits):
    '''
        Creates a QuantumCircuit object that performs {|reg1> + |reg2> (mod |reg2>)} in Fourier basis.

        Args:
            reg1_qubits (int) - Number of qubits in `reg1`.
            reg2_qubits (int) - Number of qubits in `reg2`.

        Returns:
            (QuantumCircuit) - A quantum circuit with the gates needed to write the result into `reg2`.
    '''
    
    # Initializing
    reg1 = QuantumRegister(reg1_qubits, 'reg1')
    reg2 = QuantumRegister(reg2_qubits, 'reg2')
    qc = QuantumCircuit(reg1, reg2)
    qc.name = 'Fourier addition'
    
    # Applying the controlled phase shifts to create addition
    for control_q in range(reg1_qubits):
        for target_q in range(reg2_qubits):
            k = reg2_qubits - target_q
            phase = (2 * np.pi * (2 ** control_q)) / (2 ** k)
            if phase == 2 * np.pi: # Phase shifts of 2pi multiples are indistinguishable = Breaking from the inner loop
                break
            qc.cp(theta = phase, control_qubit = reg1[control_q], target_qubit = reg2[target_q])
            
    return qc

def bitstring_to_pauli_string(bitstring: str) -> str:

    bitstring = bitstring.replace('1', 'X')
    bitstring = bitstring.replace('0', 'I')

    return bitstring

input_reg = QuantumRegister(3, "input_reg")
addition_reg = QuantumRegister(3, "addition_reg")
results = ClassicalRegister(3, "results")
qc = QuantumCircuit(input_reg, addition_reg, results)

# Setting value to input_reg
qc.append(Pauli(bitstring_to_pauli_string('110')), qargs=input_reg)

# Transforming addition_reg to Fourier basis
qc.append(QFT(3), qargs=addition_reg)
qc.barrier()

# Adding
qc.append(fourier_add(3,3), qargs=input_reg[:] + addition_reg[:])
qc.barrier()

# Transforming back to the computational basis
qc.append(QFT(3, inverse=True, qargs=addition_reg))
qc.barrier()

qc.measure(addition_reg, results)
counts = AerSimulator().run(qc).result().get_counts()

print(counts)
qc.draw()
qc.decompose().draw()