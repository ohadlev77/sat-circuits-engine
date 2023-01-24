"""
This module contains the `SingleConstraintBlock` class.
"""

from typing import Union, Optional, List

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit import Qubit

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

        # Index 0 = left, 1 = right
        self.side_contents = [self.parsed_data.left_side_content, self.parsed_data.right_side_content]

        # Base container for this object's registers
        self.regs = {
            'inputs': [QuantumRegister(0, 'input_left'), QuantumRegister(0, 'input_right')],
            'sides_aux': [QuantumRegister(0, 'aux_left'), QuantumRegister(0, 'aux_right')],
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

        # TODO COMPLETE
        self.num_total_aux_qubits = len(self.regs['sides_aux'][0]) + len(self.regs['sides_aux'][1])

        if 'comparison_aux' in self.regs.keys():
            self.num_total_aux_qubits += len(self.regs['comparison_aux'][0])
    
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

        for side in [0, 1]:

            # Arithmetics needed
            if len(self.side_contents[side]) > 1:
                self.arith_blocks[side] = InnerConstraintArithmetic(self.side_contents[side])

                self.regs['inputs'][side] = QuantumRegister(
                    self.arith_blocks[side].total_operands_width,
                    self.regs['inputs'][side].name
                )

                self.regs['sides_aux'][side] = QuantumRegister(
                    self.arith_blocks[side].result_reg_width,
                    self.regs['sides_aux'][side].name
                )

            # Single qubits bundle
            elif isinstance(self.side_contents[side][0], list):
                self.regs['inputs'][side] = QuantumRegister(
                    len(self.side_contents[side][0]),
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
        for arith_block, input_reg, side_aux_reg, integer_flag, side_content in zip(
            self.arith_blocks,
            self.regs['inputs'],
            self.regs['sides_aux'],
            self.integer_flags,
            self. side_contents
        ):
            if arith_block is not None:
                self.append(arith_block, qargs=input_reg[:] + side_aux_reg[:])
                compare.append(side_aux_reg)
            else:
                if integer_flag:
                    compare.append(side_content[0])
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
        TOOD COMPLETE
        """

        self.add_out_reg()

        # Catching non-logical input
        assert len(int_bitstring) <= len(qubits_bundle), \
        "The integer length is longer than compared qubits, no solution."

        # In the case the equation is unbalanced, filling the integer with zeros from the left
        if len(int_bitstring) < len(qubits_bundle):
            int_bitstring = int_bitstring.zfill(len(qubits_bundle))

        flipping_zeros = QuantumCircuit(len(int_bitstring), name=f"{int_bitstring}_encoding")
        for digit, qubit in zip(reversed(int_bitstring), flipping_zeros.qubits):
            if digit == '0':
                flipping_zeros.x(qubit)

        self.append(flipping_zeros, qargs=qubits_bundle)

        # TODO IMPROVE MCX
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

        if len_1 == 1 and len_2 == 1:
            self.two_qubits_comparison(
                qubits_bundle_1,
                qubits_bundle_2,
                self.regs['out'][0],
                operator=operator
            )
            return

        # TODO NEEDED OR NOT?
        # Reversing for little-endian convention
        # qubits_bundle_1 = list(reversed(qubits_bundle_1))
        # qubits_bundle_2 = list(reversed(qubits_bundle_2))

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
        
        # TODO MCX
        # Checking the left bits in the longer bundle
        if left_trimmed_long:
            self.x(left_trimmed_long)

        # TODO ORGANIZE
        q = left_trimmed_long + self.regs['comparison_aux'][0][:]
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

        aux_reg = QuantumRegister(width, "aux_comparison")
        self.add_register(aux_reg)
        self.regs['comparison_aux'] = [aux_reg]

    def add_out_reg(self) -> None:
        """
        Appends a single-qubit "out" register to this object.
        Adds it also to self.regs under the key "out" (accessible via `self.regs['out'][0]).
        """
        
        out_reg = QuantumRegister(1, "out")
        self.add_register(out_reg)
        self.regs['out'] = [out_reg]

class InnerConstraintArithmetic(QuantumCircuit):
    """
    TODO COMPLETE
    """

    def __init__(
        self,
        single_sided_parsed_equation: List[Union[List[int], str]],
        block_name: Optional[str] = None
    ) -> None:
        """
        TODO COMPLETE
        """

        self.parsed_equation = single_sided_parsed_equation

        # Isolating the integer bitstring, if exists
        try:
            self.integer_bitstring = next(filter(lambda x: isinstance(x, str), self.parsed_equation))
        except StopIteration:
            self.integer_bitstring = None

        # Translating qubits bundles into a list of number of qubits in each bundle
        self.operands_widths = list(
            map(lambda x: len(x), filter(lambda x: isinstance(x, list), self.parsed_equation))
        )
        self.total_operands_width = sum(self.operands_widths)

        # Computing the necessary width for the results aux register
        self.result_reg_width = self.compute_addition_result_width(self.operands_widths, self.integer_bitstring)

        # Defining registers
        self.bundles_regs = list(
            map(lambda x: QuantumRegister(x[1], f"reg_bundle_{x[0]}"), enumerate(self.operands_widths))
        )
        self.result_reg = QuantumRegister(self.result_reg_width, "result_reg")

        # Initiazling circuit
        super().__init__(*self.bundles_regs, self.result_reg)

        # Assigning name to this block
        if block_name is None:
            block_name = f"Addition:{self.parsed_equation}"
        self.name = block_name
        
    def add_qubits_values(
        self,
        bundles_list: List[List[Qubit]],
        results_qubits: Union[List[Union[Qubit, QuantumRegister]], QuantumRegister],
        default_bitstring: Optional[str] = None
    ) -> None:
        """
        TODO COMPLETE
        RESULTS QUBITS NEEDED AS THE MAXIMUM VALUE OF ADDING ALL BUNDLES AND DEFAULT
        """

        # Assigning `default_bitstring` value to `results_qubits`
        if default_bitstring is not None:
            for digit, result_qubit in zip(reversed(default_bitstring), results_qubits):
                if digit == '1':
                    self.x(result_qubit)

        # Transforming `results_qubits` to Fourier basis TODO
        pass
        #TODO COMPLETE
        
        # Fourier addition of all bundles
        for qubits_bundle in bundles_list:
            self.fourier_add_single_bundle()
        
        # Transforming `results_qubits` back to the computational basis TODO
        pass
        #TODO COMPLETE

    def fourier_add_single_bundle(
        self,
        qubits_to_add: Union[List[Union[Qubit, QuantumRegister]], QuantumRegister],
        target_qubits: Union[List[Union[Qubit, QuantumRegister]], QuantumRegister]
    ) -> None:
        """
        TODO COMPLETE
        """

        pass
        #TODO COMPLETE

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

    scp = SingleConstraintParsed("([7] + [4][3][2] + [1][0] + 55 != [6][5] + 6)", 1)
    # scp = SingleConstraintParsed("([3][2] != [0])", 1)
    # scp = SingleConstraintParsed("37 == [5][4][3][2][1][0])", 1)
    # scp = SingleConstraintParsed("[3] || [2] || [1])", 1)
    # scp = SingleConstraintParsed("([19] != [0])", 1)
    # scp = SingleConstraintParsed("([2][1][0] == [5][4][3])", 1)
    # scp = SingleConstraintParsed("([2] + 2 != [4][3])", 1)
    # scp = SingleConstraintParsed("([2] + [5] + [4][3] == 3)", 1)
    # scp = SingleConstraintParsed("([917][6][4][3][2] == [1][0])", 1)
    print()
    print(scp)
    print(scp.left_side_content)
    print(scp.right_side_content)
    print()

    block = SingleConstraintBlock(scp)
    print(block.draw())
    # print(block.decompose(['000_encoding']).draw())
