"""
This module contains the `SingleConstraintBlock` class.
"""

from typing import Union, Optional, List, Tuple
from numpy import pi

from qiskit import QuantumCircuit, QuantumRegister, transpile
from qiskit.circuit import Qubit
from qiskit.circuit.library import QFT

from sat_circuits_engine.constraints_parse import SingleConstraintParsed

class SingleConstraintBlock(QuantumCircuit):
    """
    `SingleConstraintBlock` object - a circuit implementation of a single constraint.
    To be integrated as a block in a `GroverConstriantsOperator` object.
    """

    def __init__(self, parsed_data: SingleConstraintParsed) -> None:
        """
        Args:
            parsed_data (SingleConstraintParsed): an object contains all necessary
            information for a single constraint, in a specific API (see `help(SingleConstraintParsed)`
            for API explanation).

            TODO - CONSIDER TO REMOVE THIS ARGUMENT AND REPLACE ITS FUNCTIONALITY WITH SOMETHING NICER.
            mpl (bool): `True` for matplotlib circuit diagrams output, `False` for text output.
        """
        
        self.parsed_data = parsed_data
        self.constraint_index = self.parsed_data.constraint_index

        # Index 0 = left, 1 = right
        # self.side_contents = [self.parsed_data.left_side_content, self.parsed_data.right_side_content]

        # Base container for this object's registers
        self.regs = {
            'inputs': [QuantumRegister(0, 'input_left'), QuantumRegister(0, 'input_right')],
            'sides_aux': [QuantumRegister(0, f"c{self.constraint_index}_aux_left"), QuantumRegister(0, f"c{self.constraint_index}_aux_right")]
        }

        # Performing arithmetics in either of the constraint's equation sides, if needed
        self.perform_arithmetics()

        # TODO SOMETHING MORE NEAT?
        # Transforming `self.regs` (dict) into a list
        regs_list = []
        for item in self.regs.values():
            regs_list.extend(item)

        # Initializing circuit
        super().__init__(*regs_list, name=parsed_data.constraint_string)

        # Assembling a circuit implementation of the given constraint
        self.assemble()

        # Saving a transpiled version of `self`
        self.transpiled = transpile(self, basis_gates=['u', 'cx'], optimization_level=3)
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}" \
               f"('{self.parsed_data.constraint_equation}'): {self.__dict__}"

    def perform_arithmetics(self) -> None:
        """
        Handles arithmetic operations from both sides of the constraint's equation, if needed.
        """

        # Index 0 = left, 1 = right
        self.arith_blocks = [None, None]
        self.integer_flags = [False, False]

        for side, (bit_indexes, int_bitstring) in enumerate(
            zip(self.parsed_data.sides_bit_indexes, self.parsed_data.sides_int_bitstrings)
        ):

            # Arithmetics needed
            if (len(bit_indexes) > 1) or (len(bit_indexes) == 1 and int_bitstring is not None):
                self.arith_blocks[side] = InnerConstraintArithmetic(bit_indexes, int_bitstring)

                self.regs['inputs'][side] = QuantumRegister(
                    self.arith_blocks[side].total_operands_width,
                    self.regs['inputs'][side].name
                )

                self.regs['sides_aux'][side] = QuantumRegister(
                    self.arith_blocks[side].result_reg_width,
                    self.regs['sides_aux'][side].name
                )

            # Single qubits bundle
            elif len(bit_indexes) == 1 and int_bitstring is None:
                self.regs['inputs'][side] = QuantumRegister(
                    len(bit_indexes[0]),
                    self.regs['inputs'][side].name
                )

            # Integer bitstring
            else:
                self.integer_flags[side] = True

    def assemble(self) -> None:
        """
        Assembles a complete circuit implementation of the the given constraint.
        """

        # TODO
        compare = []

        # Appending arithmetic blocks if needed TODO IMPROVE
        for arith_block, input_reg, side_aux_reg, integer_flag, int_bitstring in zip(
            self.arith_blocks,
            self.regs['inputs'],
            self.regs['sides_aux'],
            self.integer_flags,
            self.parsed_data.sides_int_bitstrings
        ):
            if arith_block is not None:
                # TODO CONSIDER [::-1]
                self.append(arith_block, qargs=input_reg[:] + side_aux_reg[::-1])
                compare.append(side_aux_reg)
            else:
                if integer_flag:
                    compare.append(int_bitstring)
                else:
                    compare.append(input_reg)

        if self.integer_flags[0]:
            self.qubits_int_comparison(compare[1], compare[0], operator=self.parsed_data.operator)
        elif self.integer_flags[1]:
            self.qubits_int_comparison(compare[0], compare[1], operator=self.parsed_data.operator)
        else:
            self.unbalanced_qubits_comparison(compare[0], compare[1], operator=self.parsed_data.operator)

    #### FROM HERE OPERATORS - CONSIDER EXPORTING

    def qubits_int_comparison(
        self,
        qubits_bundle: Union[List[Union[Qubit, QuantumRegister]], QuantumRegister],
        int_bitstring: str,
        *,
        operator: Optional[str] = "=="
    ) -> None:
        """
        NO AUX QUBITS NEEDED
        TODO COMPLETE
        """

        self.add_out_reg()

        # Catching non-logical input
        assert len(int_bitstring) <= len(qubits_bundle), \
        "The integer length is longer than compared qubits, no solution."

        # In the case the equation is unbalanced, filling the integer with zeros from the left
        if len(int_bitstring) < len(qubits_bundle):
            int_bitstring = int_bitstring.zfill(len(qubits_bundle))

        flipping_zeros = QuantumCircuit(len(int_bitstring), name=f"{int_bitstring}_encoding")
        for digit, qubit in zip(int_bitstring, flipping_zeros.qubits):
            if digit == '0':
                flipping_zeros.x(qubit)

        self.append(flipping_zeros, qargs=qubits_bundle)

        # TODO IMPROVE MCX anc rccx hook
        if len(qubits_bundle) == 2:
            self.rccx(qubits_bundle[0], qubits_bundle[1], self.regs['out'][0])
        else:
            self.mcx(qubits_bundle, self.regs['out'][0])

        # Flipping for !=
        if operator == "!=":
            self.x(self.regs['out'][0])

        # Uncomputing        
        self.append(flipping_zeros, qargs=qubits_bundle)

    def unbalanced_qubits_comparison(
        self,
        qubits_bundle_1: Union[List[Union[Qubit, QuantumRegister]], QuantumRegister],
        qubits_bundle_2: Union[List[Union[Qubit, QuantumRegister]], QuantumRegister],
        # aux_qubits: Union[List[Union[Qubit, QuantumRegister]], QuantumRegister],
        # out_qubit: Union[Qubit, QuantumRegister],
        *,
        operator: Optional[str] = "=="
    ) -> None:
        """
        AUX QUBITS NEEDED AS THE LENGTH OF SHORT QUBIT BUNDLE
        TODO COMPLETE
        """

        # TODO MAYBE REMOVE IN THE END
        len_1 = len(qubits_bundle_1)
        len_2 = len(qubits_bundle_2)

        # TODO COMPLETE
        if len_1 > 1 or len_2 > 1:
            self.add_comparison_aux_reg(min(len_1, len_2))
        self.add_out_reg()

        # TODO NEEDED OR NOT? SEEMS TO BE TAKEN CARE BY THE GroverConstraintsOperator class
        # Reversing for little-endian convention
        # qubits_bundle_1 = list(reversed(qubits_bundle_1))
        # qubits_bundle_2 = list(reversed(qubits_bundle_2))

        if len_1 == 1 and len_2 == 1:
            self.two_qubits_comparison(
                qubits_bundle_1,
                qubits_bundle_2,
                self.regs['out'][0],
                operator=operator
            )
            return
        

        if len_1 > len_2:
            long = qubits_bundle_1
            short = qubits_bundle_2
            right_trimmed_long = qubits_bundle_1[-len_2:]
        else:
            long = qubits_bundle_2
            short = qubits_bundle_1
            right_trimmed_long = qubits_bundle_2[-len_1:]
        
        len_short = len(short)
        len_long = len(long)
        left_trimmed_long = long[:len_long - len_short]

        # Comparing the rightmost bits in the longer bundle to the bits of the shorter bundle
        self.balanced_qubits_comparison(short, right_trimmed_long, self.regs['comparison_aux'][0][:len_short])
        
        # Checking the left bits in the longer bundle
        if left_trimmed_long:
            self.x(left_trimmed_long)

        # TODO MCX and RCCX HOOK
        # TODO ORGANIZE
        q = left_trimmed_long + self.regs['comparison_aux'][0][:]
        if len(q) == 2:
            self.rccx(q[0], q[1], self.regs['out'][0])
        else:
            self.mcx(q, self.regs['out'][0])

        # Flipping for !=
        if operator == "!=":
            self.x(self.regs['out'][0])

        # Uncomputing
        if left_trimmed_long:
            self.x(left_trimmed_long)

    def balanced_qubits_comparison(
        self,
        qubits_bundle_1: Union[List[Union[Qubit, QuantumRegister]], QuantumRegister],
        qubits_bundle_2: Union[List[Union[Qubit, QuantumRegister]], QuantumRegister],
        aux_qubits: Union[List[Union[Qubit, QuantumRegister]], QuantumRegister],
        out_qubit: Optional[Union[Qubit, QuantumRegister]] = None,
        *,
        operator: Optional[str] = "=="
    ) -> None:
        """
        TODO COMPLETE
        AUX QUBITS NEEDED AS THE LENGTH OF QUBITS BUNDLES
        """

        # No auxilliary qubits = the case of comparing 1 single qubit from each side
        if len(aux_qubits) == 0:
            aux_qubits = out_qubit

        # Implementation of: qubits_bundle_1 == qubits_bundle_2
        # Comparing each pair of qubits and writing results to auxilliary qubits
        for q1, q2, aux in zip(qubits_bundle_1, qubits_bundle_2, aux_qubits):
            self.two_qubits_comparison(q1, q2, aux, operator="==")

        # TODO IMPROVE MCX IMPLEMENTATION
        # Writing overall result to out_qubit if not None
        if out_qubit is not None:
            if len(aux) == 2:
                self.rccx(aux[0], aux[1], out_qubit)
            else:
                self.mcx(aux, out_qubit)
        
        # Fliiping out qubit for implementation of: qubits_bundle_1 != qubits_bundle_2
        if operator == "!=":
            self.x(out_qubit)

    def two_qubits_comparison(
        self,
        qubit_1: Union[Qubit, QuantumRegister],
        qubit_2: Union[Qubit, QuantumRegister],
        qubit_result: Union[Qubit, QuantumRegister],
        *,
        operator: Optional[str] = "=="
    ) -> None:
        """
        TODO COMPLETE
        NO AUX QUBITS NEEDED
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

class InnerConstraintArithmetic(QuantumCircuit):
    """
    TODO COMPLETE
    """

    def __init__(
        self,
        single_side_bits_indexes: List[Tuple[List[int]]],
        single_side_integer_bitstring: Optional[str] = None,
        block_name: Optional[str] = None
    ) -> None:
        """
        TODO COMPLETE
        """

        self.bits_indexes = single_side_bits_indexes
        self.integer_bitstring = single_side_integer_bitstring

        # Translating qubits bundles into a list of number of qubits in each bundle
        self.operands_widths = list(map(lambda x: len(x), self.bits_indexes))
        self.total_operands_width = sum(self.operands_widths)

        # Computing the necessary width for the results aux register
        self.result_reg_width = self.compute_addition_result_width(
            self.operands_widths,
            self.integer_bitstring
        )

        # Defining registers
        self.bundles_regs = list(
            map(lambda x: QuantumRegister(x[1], f"reg_bundle_{x[0]}"), enumerate(self.operands_widths))
        )
        self.result_reg = QuantumRegister(self.result_reg_width, "result_reg")

        # Initiazling circuit
        super().__init__(*self.bundles_regs, self.result_reg)

        # TODO DEFAULT VALUE TRY
        self.add_qubits_values(self.result_reg, self.integer_bitstring)

        # Assigning name to this block
        if block_name is None:
            block_name = f"Addition:{self.bits_indexes} + {self.integer_bitstring}"
        self.name = block_name
        
    def add_qubits_values(
        self,
        results_qubits: Union[List[Union[Qubit, QuantumRegister]], QuantumRegister],
        default_bitstring: Optional[str] = None
    ) -> None:
        """
        TODO COMPLETE
        RESULTS QUBITS NEEDED AS THE MAXIMUM VALUE OF ADDING ALL BUNDLES AND DEFAULT
        NOTE: SUPPORTS ONLY NOT-REPEATED BITS ADDITION (VALID = [3][2] + [1] + 5, NOT VALID = [3][2] + [2][1])
        """

        # Assigning `default_bitstring` value to `results_qubits`
        if default_bitstring is None:
            default_bitstring = ''.zfill(self.result_reg_width)
        else:
            default_bitstring = default_bitstring.zfill(self.result_reg_width)
            for digit, result_qubit in zip(reversed(default_bitstring), results_qubits):
                if digit == '1':
                    self.x(result_qubit)

        default_added_operand_index = self.default_addition(default_bitstring)
        if default_added_operand_index is not None:
            self.bundles_regs.pop(default_added_operand_index)

        if self.bundles_regs:
            # Transforming `results_qubits` to Fourier basis TODO
            self.append(QFT(self.result_reg_width), qargs=self.result_reg)
            
            # Fourier addition of all bundles
            for reg in self.bundles_regs:
                self.fourier_add_single_bundle(reg, self.result_reg)
            
            # Transforming `results_qubits` back to the computational basis TODO
            self.append(QFT(self.result_reg_width, inverse=True), qargs=self.result_reg)
    
    def default_addition(self, bitstring: str) -> int:
        """
        Performing in place bit-to-bit addition if possible.

        TODO COMPLETE

        Returns:
            (int): the index of the operang that has been added.
        """

        # Counting the number of trailing zeros (i.e, number of available bits to copy values into)
        try:
            trailing_zeros_num = bitstring[::-1].index('1')
        except ValueError:
            trailing_zeros_num = self.result_reg_width

        # Finding the best operand to copy its value (the longest one that shorter or equal
        # in length to the number of trailing zeros)
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
            # TODO consider [::-1]
            self.cx(self.bundles_regs[operand_index], self.result_reg[:trailing_zeros_num][::-1])

        return operand_index

    def fourier_add_single_bundle(
        self,
        qubits_to_add: Union[List[Union[Qubit, QuantumRegister]], QuantumRegister],
        target_qubits: Union[List[Union[Qubit, QuantumRegister]], QuantumRegister]
    ) -> None:
        """
        TODO COMPLETE
        """

        # TODO ORGANIZE AND FIX
        for control_index, control_q in enumerate(qubits_to_add):
            for target_index, target_q in enumerate(target_qubits):

                k = len(target_qubits) - target_index
                phase = (2 * pi * (2 ** control_index)) / (2 ** k)

                # Phase shifts of 2pi multiples are indistinguishable = Breaking from the inner loop
                if phase == 2 * pi:
                    break

                self.cp(theta=phase, control_qubit=control_q, target_qubit=target_q)

    @staticmethod
    def compute_addition_result_width(
        regs_widths: List[int],
        default_bitstring: Optional[str] = None
    ) -> int:
        """
        TODO COMPLETE
        """

        if default_bitstring is None:
            default_bitstring = '0'

        # Just 1 operand = no addition
        if len(regs_widths) == 1 and default_bitstring == '0':
            return 0

        # The maximum possible sum integer value
        max_sum = sum(map(lambda x: (2 ** x) - 1, regs_widths)) + int(default_bitstring, 2)

        # Returning the bitstring length of that sum
        return len(bin(max_sum)[2:])


# TODO REMOVE
if __name__ == '__main__':

    from sat_circuits_engine.constraints_parse import SingleConstraintParsed

    # scp = SingleConstraintParsed("([1][0] != [3][2])", 1)
    # scp = SingleConstraintParsed("([3][2] != [0])", 1)
    # scp = SingleConstraintParsed("37 == [5][4][3][2][1][0])", 1)
    # scp = SingleConstraintParsed("[3] || [2] || [1])", 1)
    # scp = SingleConstraintParsed("([19] != [0])", 1)
    # scp = SingleConstraintParsed("([2][1][0] == [5][4][3])", 1)
    # scp = SingleConstraintParsed("([2] + 2 + [4][3][2] != [4][3])", 1)
    # scp = SingleConstraintParsed("([2] + [5] + [4][3] == 3)", 1)
    # scp = SingleConstraintParsed("([917][6][4][3][2] == [1][0])", 1)
    # scp = SingleConstraintParsed("([3][2][1] != 6)", 1)
    # scp = SingleConstraintParsed("([2] + [6][5][4][3][2] + 8 + [4][3][2] != [4][3])", 1)
    scp = SingleConstraintParsed("([2] + [1][0] + 2 != [4][3])", 1)

    print()
    print(scp)
    # print(scp.left_side_content)
    # print(scp.right_side_content)
    print()

    block = SingleConstraintBlock(scp)
    print(block.draw())
    print(block.decompose(["Addition:([2], [1, 0]) + 10"]).draw())
    # print(block.decompose(['110_encoding']).draw())
