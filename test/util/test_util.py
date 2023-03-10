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

"""Tests for `util.py` module."""

import unittest
from datetime import datetime

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from sat_circuits_engine.util import flatten_circuit, timestamp


class UtilTest(unittest.TestCase):

    def test_timestamp(self):
        """Test for the `timestamp` function."""

        self.assertEqual(timestamp(datetime(2022, 12, 3, 17, 0, 45, 0)), "D03.12.22_T17.00.45")

    def test_flatten_circuit(self):
        """Test for the `flatten_circuit` function."""

        bits_1 = 2
        bits_2 = 3
        qreg_1 = QuantumRegister(bits_1)
        qreg_2 = QuantumRegister(bits_2)
        creg_1 = ClassicalRegister(bits_1)
        creg_2 = ClassicalRegister(bits_2)
        circuit = QuantumCircuit(qreg_1, qreg_2, creg_1, creg_2)

        self.assertEqual(circuit.num_qubits, bits_1 + bits_2)
        self.assertEqual(circuit.num_clbits, bits_1 + bits_2)
        self.assertEqual(len(circuit.qregs), 2)
        self.assertEqual(len(circuit.cregs), 2)

        flat_circuit = flatten_circuit(circuit)

        self.assertEqual(flat_circuit.num_qubits, bits_1 + bits_2)
        self.assertEqual(flat_circuit.num_clbits, bits_1 + bits_2)
        self.assertEqual(len(flat_circuit.qregs), 1)
        self.assertEqual(len(flat_circuit.cregs), 1)

if __name__ == "__main__":
    unittest.main()
