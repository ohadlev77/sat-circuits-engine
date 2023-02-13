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

"""
`SingleConstraintBlock` and `ArithmeticExprBlock` classes.
"""

from typing import Union, Optional, List, Dict, Any
import numpy as np

from qiskit import QuantumCircuit, QuantumRegister, transpile
from qiskit.circuit import Qubit
from qiskit.circuit.library import QFT

from sat_circuits_engine.constraints_parse import SingleConstraintParsed
from sat_circuits_engine.util.settings import TRANSPILE_KWARGS

class SingleConstraintBlock(QuantumCircuit):
    """
    A quantum circuit implementation of a single constraint.
    To be integrated as a block in a `GroverConstriantsOperator` object.
    """

    def __init__(
        self,
        parsed_data: SingleConstraintParsed,
        transpile_kwargs: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Args:
            parsed_data (SingleConstraintParsed): an object contains all necessary
            information for a single constraint, in a specific API (see `help(SingleConstraintParsed)`
            for API annotation).
            transpile_kwargs (Optional[Dict[str, Any]] = None): keyword arguments for self-transpilation
            that takes place in this class. If None (default) - `TRANSPILE_KWARGS` constant is used.
        """
        
        self.parsed_data = parsed_data
        self.constraint_index = self.parsed_data.constraint_index

        if transpile_kwargs is None:
            transpile_kwargs = TRANSPILE_KWARGS
        self.transpile_kwargs = transpile_kwargs

        # Handling arithmetic expressions and constructing a container with quantum register - `self.regs`
        self.handle_arithmetics()

        # Creating a unified list of registers to unpack as args for `super().__init__`
        regs_list = []
        for item in self.regs.values():
            regs_list.extend(item)

        # Initializing circuit
        super().__init__(*regs_list, name=self.parsed_data.string_to_show)

        # Assembling a circuit implementation of the given constraint
        self.assemble()

        # Saving a transpiled version of `self`.
        # Used by `GroverConstraintsOperator` to set the order of constraints.
        self.transpiled = transpile(self, **self.transpile_kwargs)
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}" \
               f"('{self.parsed_data.string_to_show}')"

    def handle_arithmetics(self) -> None:
        """
        Handles arithmetic operations from both sides of the constraint's equation, if needed.
        Initiates some of the quantum registers that compose the circuit (`self`).
        The left side of the constraint's equation is indexed as 0, and the right side is inexed as 1.
        Defines attributes:
            self.regs (Dict[str, List[QuantumRegister]]): container for quantum registers.
            self.arith_blocks (List[Optioanl[ArithmeticExprBlock] = None]): Indexed containter for
            `ArithmeticExprBlock` objects. None (default) - if no artihmetic performed in a specific side.
            self.integer_flags (List[bool]): Indexed container for boolean values. True for a side
            that contains bare integer only, otherwise False.
        """

        self.regs = {
            # Initializing empty input registers
            'inputs': [
                QuantumRegister(0, "input_left"),
                QuantumRegister(0, "input_right")
            ],

            # Initializing empty auxiliary register for performing arithmetics
            'sides_aux': [
                QuantumRegister(0, f"c{self.constraint_index}_aux_left"),
                QuantumRegister(0, f"c{self.constraint_index}_aux_right")
            ]
        }

        self.arith_blocks = [None, None]
        self.integer_flags = [False, False]

        # Iterating over the 2 sides of the constraint's equation and constructing the needed registers
        for side, (bit_indexes, int_bitstring) in enumerate(
            zip(self.parsed_data.sides_bit_indexes, self.parsed_data.sides_int_bitstrings)
        ):

            # Case A - arithmetic expression
            if (len(bit_indexes) > 1) or (len(bit_indexes) == 1 and int_bitstring is not None):

                # Case A.1 -the other side of the equations is a bare integer
                compared_value = None
                if (
                    not self.parsed_data.sides_bit_indexes[side ^ 1]
                    and
                    self.parsed_data.sides_int_bitstrings[side ^ 1]
                ):
                    compared_value = int(self.parsed_data.sides_int_bitstrings[side ^ 1], 2)

                # Generating the arithmetic expression block
                self.arith_blocks[side] = ArithmeticExprBlock(
                    bit_indexes,
                    int_bitstring,
                    compared_value=compared_value
                )

                # Creating an input register that fits with the arithmetic expression block
                self.regs['inputs'][side] = QuantumRegister(
                    self.arith_blocks[side].total_operands_width,
                    self.regs['inputs'][side].name
                )

                # Creating an auxiliary register for arithmetics
                self.regs['sides_aux'][side] = QuantumRegister(
                    self.arith_blocks[side].result_reg_width,
                    self.regs['sides_aux'][side].name
                )

            # Case B - single variable expression
            elif len(bit_indexes) == 1 and int_bitstring is None:
                self.regs['inputs'][side] = QuantumRegister(
                    len(bit_indexes[0]),
                    self.regs['inputs'][side].name
                )

            # Case C - bare integer expression
            else:
                self.integer_flags[side] = True

    def assemble(self) -> None:
        """
        Assembles a complete circuit implementation of the given constraint.
        """

        compare_operands = []

        # Figuring the compared operand for each of the contraint's equation sides
        for arith_block, input_reg, side_aux_reg, integer_flag, int_bitstring in zip(
            self.arith_blocks,
            self.regs['inputs'],
            self.regs['sides_aux'],
            self.integer_flags,
            self.parsed_data.sides_int_bitstrings
        ):

            # Arithmetic block operand
            if arith_block is not None:

                # Appeding the arithmetic block to the `self`
                self.append(arith_block, qargs=input_reg[:] + side_aux_reg[::-1])

                compare_operands.append(side_aux_reg)
            else:

                # Integer bitstring operand
                if integer_flag:
                    compare_operands.append(int_bitstring)

                # A bundle of qubits (from the input register) operand
                else:
                    compare_operands.append(input_reg)

        # Applying the methods for the necessary comparison
        if self.integer_flags[0]:
            self.qubits_int_comparison(
                qubits_bundle=compare_operands[1],
                int_bitstring=compare_operands[0],
                operator=self.parsed_data.operator,
            )
        elif self.integer_flags[1]:
            self.qubits_int_comparison(
                qubits_bundle=compare_operands[0],
                int_bitstring=compare_operands[1],
                operator=self.parsed_data.operator
            )
        else:
            self.unbalanced_qubits_comparison(
                qubits_bundle_1=compare_operands[0],
                qubits_bundle_2=compare_operands[1],
                operator=self.parsed_data.operator
            )

    def qubits_int_comparison(
        self,
        qubits_bundle: Union[List[Union[Qubit, int]], QuantumRegister],
        int_bitstring: str,
        *,
        operator: Optional[str] = "=="
    ) -> None:
        """
        Compares a bundle of qubits to an integer.

        Args:
            qubits_bundle (Union[List[Union[Qubit, int]], QuantumRegister]): compared qubits.
            int_bitstring (str): compared integer (in a bitstring form).
            operator (Optional[str] = "=="): comparison operator, default is "==",
            and the other option is "!=".

        Raises:
            AssertionError: If `int_bitstring` is an integer larger than any integer
            that can be possibly represented by `qubits_bundle`.
        """

        # Adding an "out" qubit to write the result into
        self.add_out_reg() 

        # Creating pointers for convenience
        len_int = len(int_bitstring)
        len_qubits_bundle = len(qubits_bundle)

        # Catching non-logical input
        assert len_int <= len_qubits_bundle, \
        f"The integer ({int_bitstring}) length is longer than compared" \
        f"qubits ({qubits_bundle}), no solution."

        # In the case the equation is unbalanced, filling the integer with zeros from the left
        if len_int < len_qubits_bundle:
            int_bitstring = int_bitstring.zfill(len_qubits_bundle)

            # Setting `len_int` again after filling `int_bitstring` with zeros from the left
            len_int = len(int_bitstring)

        # Flipping bits in `qubits_bundle` in order to compare them to '0' digits in `int_bitstring`
        flipping_zeros = QuantumCircuit(len_int, name=f"{int_bitstring}_encoding")
        for digit, qubit in zip(int_bitstring, flipping_zeros.qubits):
            if digit == '0':
                flipping_zeros.x(qubit)
        self.append(flipping_zeros, qargs=qubits_bundle)

        # Writing results to the "out" qubit
        # TODO need to generalize RCCX and RCCCX to the n-control qubits case
        if len_qubits_bundle == 2:
            self.rccx(qubits_bundle[0], qubits_bundle[1], self.regs['out'][0])
        elif len_qubits_bundle == 3:
            self.rcccx(qubits_bundle[0], qubits_bundle[1], qubits_bundle[2], self.regs['out'][0])
        else:
            self.mcx(qubits_bundle, self.regs['out'][0])

        # Flipping outcome in the case the operator is "!="
        if operator == "!=":
            self.x(self.regs['out'][0])

        # Uncomputing flipped bits 
        self.append(flipping_zeros, qargs=qubits_bundle)

    def unbalanced_qubits_comparison(
        self,
        qubits_bundle_1: Union[List[Union[Qubit, int]], QuantumRegister],
        qubits_bundle_2: Union[List[Union[Qubit, int]], QuantumRegister],
        *,
        operator: Optional[str] = "=="
    ) -> None:
        """
        The most general case of comparing 2 bundles of qubits.
        The bundles might be of the same length ("balanced") or not ("unbalanced").

        Args:
            qubits_bundle_1, qubits_bundle_2 (Union[List[Union[Qubit, int]], QuantumRegister]):
                - Qubits of bundle_1 are compared to qubits of bundle_2.
            operator (Optional[str] = "=="): comparison operator, default is "==",
            and the other option is "!=".
        """

        # Creating pointers for convenience
        len_bundle_1 = len(qubits_bundle_1)
        len_bundle_2 = len(qubits_bundle_2)

        # The case where a comparison aux register is needed
        if len_bundle_1 > 1 or len_bundle_2 > 1:
            self.add_comparison_aux_reg(min(len_bundle_1, len_bundle_2))

        # Adding an "out" qubit to write the result into
        self.add_out_reg()

        # In this case, only 2 qubits comparison is needed, and then the method's execution halts
        if len_bundle_1 == 1 and len_bundle_2 == 1:
            self.two_qubits_comparison(
                qubits_bundle_1,
                qubits_bundle_2,
                self.regs['out'][0],
                operator=operator
            )
            return
        
        # Setting short and long bundles and cutting the long bundle to 2 parts.
        # The right part of the long bundle is comparble to the short bundle.
        if len_bundle_1 > len_bundle_2:
            long = qubits_bundle_1
            short = qubits_bundle_2
            long_right_cut = qubits_bundle_1[-len_bundle_2:]
        else:
            long = qubits_bundle_2
            short = qubits_bundle_1
            long_right_cut = qubits_bundle_2[-len_bundle_1:]

        len_short = len(short)
        len_long = len(long)
        long_left_cut = long[:len_long - len_short]

        # Comparing the rightmost bits in the longer bundle to the bits of the shorter bundle
        self.balanced_qubits_comparison(
            short,
            long_right_cut,
            self.regs['comparison_aux'][0][:len_short]
        )
        
        # Flipping the left bits in the longer bundle (in order to check whether they all zeros)
        if long_left_cut:
            self.x(long_left_cut)

        # Writing results to the "out" qubit
        # TODO need to generalize RCCX and RCCCX to the n-control qubits case
        q = long_left_cut + self.regs['comparison_aux'][0][:]
        if len(q) == 2:
            self.rccx(q[0], q[1], self.regs['out'][0])
        elif len(q) == 3:
            self.rcccx(q[0], q[1], q[2], self.regs['out'][0])
        else:
            self.mcx(q, self.regs['out'][0])

        # Flipping outcome in the case the operator is "!="
        if operator == "!=":
            self.x(self.regs['out'][0])

        # Uncomputing flipping left bits in the longer bundle
        if long_left_cut:
            self.x(long_left_cut)

    def balanced_qubits_comparison(
        self,
        qubits_bundle_1: Union[List[Union[Qubit, int]], QuantumRegister],
        qubits_bundle_2: Union[List[Union[Qubit, int]], QuantumRegister],
        aux_qubits: Union[List[Union[Qubit, int]], QuantumRegister],
        out_qubit: Optional[Union[Qubit, QuantumRegister, int]] = None,
        *,
        operator: Optional[str] = "=="
    ) -> None:
        """
        Comparing 2 bundles of qubits.
        The bundles must be of the same length ("balanced").

        Args:
            qubits_bundle_1, qubits_bundle_2 (Union[List[Union[Qubit, int]], QuantumRegister]):
                - Qubits of bundle_1 are compared to qubits of bundle_2.
            aux_qubits (Union[List[Union[Qubit, int]], QuantumRegister]): auxiliary qubits for
            comparing `qubits_bundle_1` with `qubits_bundle_2`.
            out_qubit (Optional[Union[Qubit, QuantumRegister, int]] = None): A qubit
            to write the result into. If None - not writing result, probably the method
            is being used by another method and not intended to write results.
            operator (Optional[str] = "=="): comparison operator, default is "==",
            and the other option is "!=".
        """

        # No auxilliary qubits = the case of comparing 1 single qubit from each side
        if len(aux_qubits) == 0:
            aux_qubits = out_qubit

        # Implementation of: qubits_bundle_1 == qubits_bundle_2.
        # Comparing each pair of qubits and writing results to auxilliary qubits.
        for q1, q2, aux in zip(qubits_bundle_1, qubits_bundle_2, aux_qubits):
            self.two_qubits_comparison(q1, q2, aux, operator="==")

        if out_qubit is not None:

            # Writing overall outcome to the "out" qubit
            # TODO need to generalize RCCX and RCCCX to the n-control qubits case
            if len(aux) == 2:
                self.rccx(aux[0], aux[1], out_qubit)
            elif len(aux) == 3:
                self.rcccx(aux[0], aux[1], aux[2], out_qubit)
            else:
                self.mcx(aux, out_qubit)
        
            # Flipping outcome in the case the operator is "!="
            if operator == "!=":
                self.x(out_qubit)

    def two_qubits_comparison(
        self,
        qubit_1: Union[Qubit, QuantumRegister, int],
        qubit_2: Union[Qubit, QuantumRegister, int],
        qubit_result: Union[Qubit, QuantumRegister, int],
        *,
        operator: Optional[str] = "=="
    ) -> None:
        """
        Compares values of 2 qubits.

        Args:
            qubit_1 (Union[Qubit, QuantumRegister, int]): first qubit to compare.
            qubit_2 (Union[Qubit, QuantumRegister, int]): second qubit to compare.
            qubit_result (Union[Qubit, QuantumRegister, int]): qubit to write the results to.
            operator (Optional[str] = "=="): comparison operator, default is "==",
            and the other option is "!=".
        """

        # XOR implementaion for qubit_1 != qubit_2
        self.cx(qubit_1, qubit_result)
        self.cx(qubit_2, qubit_result)

        # Flipping the result for qubit_1 == qubit_2
        if operator == "==":
            self.x(qubit_result)

    def add_comparison_aux_reg(self, width: int) -> None:
        """
        Appends an auxilliary register for the comparison (between sides of equation) operations.
        Adds it also to self.regs under the key "comparison_aux" (accessible
        via `self.regs['comparison_aux'][0]).

        Args:
            width (int): number of qubits in the register.
        """

        aux_reg = QuantumRegister(width, f"c{self.constraint_index}_aux_comparison")
        self.add_register(aux_reg)
        self.regs['comparison_aux'] = [aux_reg]

    def add_out_reg(self) -> None:
        """
        Appends a single-qubit "out" register to this object.
        Adds it also to self.regs under the key "out" (accessible via `self.regs['out'][0]).
        """
        
        out_reg = QuantumRegister(1, f"c{self.constraint_index}_out")
        self.add_register(out_reg)
        self.regs['out'] = [out_reg]

class ArithmeticExprBlock(QuantumCircuit):
    """
    A quantum circuit implementation of an arithmetic expression.
    To be integrated as a block in a `SingleConstraintBlock` object.
    """

    def __init__(
        self,
        single_side_bits_indexes: List[List[int]],
        single_side_integer_bitstring: Optional[str] = None,
        compared_value: int = None,
        block_name: Optional[str] = None
    ) -> None:
        """
        Args:
            single_side_bits_indexes (List[List[int]]): A list of lists, each list contains bit
            indexes that form a single bundle.
            single_side_integer_bitstring (Optional[str] = None): If exists, the binary string
            of the integer in an arithmetic expression.
            compared_value (int = None):
                - An integer value that the arithmetic expression is compared to (in the "other side"
                of the constraint's equation).
                - If defined - this class will try to reduce the width of its results
                register using modular addition, after negating collisions possibilities.
            block_name (Optional[str] = None): a name for this circuit block. If None, a meaningful
            name is given by this class automatically.
        """

        self.bits_indexes = single_side_bits_indexes
        self.integer_bitstring = single_side_integer_bitstring

        # Translating qubits bundles into a list of number of qubits in each bundle
        self.operands_widths = list(map(lambda x: len(x), self.bits_indexes))
        self.total_operands_width = sum(self.operands_widths)

        # Computing the necessary width for the results aux register
        self.result_reg_width = self.compute_addition_result_width(
            self.operands_widths,
            self.integer_bitstring,
            compared_value
        )

        # Defining registers
        self.bundles_regs = list(
            map(lambda x: QuantumRegister(x[1], f"reg_bundle_{x[0]}"), enumerate(self.operands_widths))
        )
        self.result_reg = QuantumRegister(self.result_reg_width, "result_reg")

        # Initiazling circuit
        super().__init__(*self.bundles_regs, self.result_reg)

        # Performing addition of all operands
        self.add()

        # Assigning name to this circuit block
        if block_name is None:
            block_name = f"Addition:{self.bits_indexes} + {self.integer_bitstring}"
        self.name = block_name
        
    def add(self) -> None:
        """
        Performing addition of all operands.
        NOTE: Supports only non-repeated values (VALID = [3][2] + [1] + 5, NOT VALID = [3][2] + [2][1]).
        """

        # Assigning `default_bitstring` value to `results_qubits`
        if self.integer_bitstring is None:
            self.integer_bitstring = ''.zfill(self.result_reg_width)
        else:
            self.integer_bitstring = self.integer_bitstring.zfill(self.result_reg_width)
            for digit, result_qubit in zip(reversed(self.integer_bitstring), self.result_reg):
                if digit == '1':
                    self.x(result_qubit)

        # Performing "default addition" (= copying values of each bit with CNOTS) of one
        # operand (the most suitable one) to `self.result_reg`, if possible (Before applying QFT).
        default_added_operand_index = self.default_addition()
        if default_added_operand_index is not None:
            self.bundles_regs.pop(default_added_operand_index)

        if self.bundles_regs:
            # Transforming `results_qubits` to Fourier basis
            self.append(QFT(self.result_reg_width), qargs=self.result_reg)
            
            # Fourier addition of all bundles
            for reg in self.bundles_regs:
                self.fourier_add_single_bundle(reg, self.result_reg)
            
            # Transforming `results_qubits` back to the computational basis
            self.append(QFT(self.result_reg_width, inverse=True), qargs=self.result_reg)
    
    def default_addition(self) -> int:
        """
        Performs in bit-to-bit addition of one of the operands to `self.result_reg` if possible.

        Returns:
            (int): the index of the operand that has been added.
        """

        # Counting the number of trailing zeros (i.e, number of available bits to copy values into)
        try:
            trailing_zeros_num = self.integer_bitstring[::-1].index('1')
        except ValueError:
            trailing_zeros_num = self.result_reg_width

        # Finding the best operand to copy its value (the longest one that's shorter
        # or equal in length to the number of trailing zeros).
        operand_index = None
        for num_zeros in reversed(range(1, trailing_zeros_num + 1)):
            try:
                operand_index = self.operands_widths.index(num_zeros)
                trailing_zeros_num = num_zeros
                break
            except ValueError:
                pass
        
        # If possible, performing the optimal bit-to-bit addition
        if operand_index is not None:
            self.cx(self.bundles_regs[operand_index], self.result_reg[:trailing_zeros_num][::-1])

        return operand_index

    def fourier_add_single_bundle(
        self,
        qubits_to_add: Union[List[Union[Qubit, int]], QuantumRegister],
        target_qubits: Union[List[Union[Qubit, int]], QuantumRegister]
    ) -> None:
        """
        Perform an addition in Fourier basis.

        Args:
            qubits_to_add (Union[List[Union[Qubit, int]], QuantumRegister]): a bundle of qubits
            to sum their values.
            target_qubits (Union[List[Union[Qubit, int]], QuantumRegister]): qubits to write the result
            into, must be already in Fourier basis.
        """

        # `qubits_to_add` are reversed due to bits ordering issues (consistency with little-endian)
        for control_index, control_q in enumerate(reversed(qubits_to_add)):
            for target_index, target_q in enumerate(target_qubits):

                k = len(target_qubits) - target_index
                phase = (2 * np.pi * (2 ** control_index)) / (2 ** k)

                # Phase shifts of 2pi multiples are indistinguishable = Breaking from the inner loop
                if phase == 2 * np.pi:
                    break

                self.cp(theta=phase, control_qubit=control_q, target_qubit=target_q)

    @staticmethod
    def compute_addition_result_width(
        regs_widths: List[int],
        default_bitstring: Optional[str] = None,
        compared_value: Optional[int] = None
    ) -> int:
        """
        Calculates `width` - the (minimal) width of the register that should
        contain the sum of values of the registers (whose widths are stored in `regs_width`)
        with `default_bitstring`.

        Args:
            regs_widths (List[int]): number of bits in each of the summed registers.
            default_bitstring (Optional[str] = None): integer bitstring operand.
            compared_value (Optional[int] = None):
                - An integer value that the arithmetic expression is compared to (in the "other side"
                of the constraint's equation).
        
        Returns:
            (int) - `width`.
        """

        if default_bitstring is None:
            default_bitstring = '0'

        # Just 1 operand = no addition
        if len(regs_widths) == 1 and default_bitstring == '0':
            return 0

        # The maximum possible sum integer value
        max_sum = sum(map(lambda x: (2 ** x) - 1, regs_widths)) + int(default_bitstring, 2)

        # The bitstring length of the maximum possible sum
        width = len(bin(max_sum)[2:])

        # Trying to reduce width if modular addition can't cause collisions w.r.t to `compared_value`
        if compared_value is not None:
            if max_sum - compared_value < compared_value and width > len(bin(compared_value)[2:]):
                width -= 1
                
        return width