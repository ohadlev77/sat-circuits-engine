"""
GroverConstraintsOperator class.
"""

from itertools import chain
from typing import Optional

from qiskit import QuantumCircuit, QuantumRegister

from sat_circuits_engine.constraints_parse import ParsedConstraints
from sat_circuits_engine.circuit.single_constraint import SingleConstraintBlock

class GroverConstraintsOperator(QuantumCircuit):
    """
    A quantum circuit implementation of Grover's operator constructed
    for a specific combination of constraints entered by a user.
    """

    def __init__(
        self,
        parsed_constraints: ParsedConstraints,
        num_input_qubits: int,
        insert_barriers: Optional[bool] = True
    ) -> None:
        """
        Args:
            parsed_constraints (ParsedConstraints): a dict-like object that associates every (single)
            constraint string (the keys) with its `SingleConstraintParsed` object (the values).
            num_input_qubits (int): number of qubits in the input register.
        """

        self.num_input_qubits = num_input_qubits
        self.parsed_constraints = list(parsed_constraints.values())
        self.insert_barriers = insert_barriers

        # Transforming `constraints_string` into a list of `SingleConstraintBlock` objects. A few more
        # instance variables defined within `self.constraints_build`, see its docstrings for details.
        self.constraints_blocks_build()

        # Initializing the quantum circuit that implements the Grover operator we seek for
        self.input_reg = QuantumRegister(self.num_input_qubits, 'input_reg')
        self.comparison_aux_reg = QuantumRegister(self.comparison_aux_width, 'comparison_aux_reg')
        self.left_aux_reg = QuantumRegister(self.left_aux_width, 'left_aux_reg')
        self.right_aux_reg = QuantumRegister(self.right_aux_width, 'right_aux_reg')
        self.out_reg = QuantumRegister(self.out_qubits_amount, 'out_reg')
        self.ancilla = QuantumRegister(1, 'ancilla')

        super().__init__(
            self.input_reg,
            self.left_aux_reg,
            self.right_aux_reg,
            self.comparison_aux_reg,
            self.out_reg,
            self.ancilla
        )

        # Assembling `self` to a complete Grover operator
        self.assemble()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.constraints_string}')"

    def constraints_blocks_build(self) -> None:
        """
        Parses the `self.parsed_constraints` attribute and defines the attributes:
            - `self.single_constraints_objects` (List[SingleConstraintBlock]): a list of
            `SingleConstraintBlock` objects, each built from a single constraint string.
            - `sum(self.comparison_aux_qubits_needed)` (int): total number of auxiliary qubits needed.
            - `self.aux_qubits_needed_list` (List[int]): a list of auxiliary qubits needed
            for implementing each constraint.
            - `self.out_qubits_amount` (int): the number of "out qubits" needed, while each "out qubit"
            is used to write the result of applying a single constraint into (|1> if the constraint is 
            satisfied, |0> otherwise).
        """

        self.single_constraints_objects = []
        self.comparison_aux_qubits_needed = []
        self.left_aux_qubits_needed = []
        self.right_aux_qubits_needed = []

        # For each constraint we build a `SingleConstraintBlock` object and count
        # the number of auxiliary qubits needed to implement it
        # (i.e, how many auxiliary qubits each `SingleConstraintBlock` object uses).

        # Sorting the constraints such that the most costly ones will be the first and last
        # (First and last constraint are not uncomputed - only when the wholde operator is uncomputed)
        constraints_blocks = list(map(SingleConstraintBlock, self.parsed_constraints))
        constraints_blocks.sort(key=lambda x: x.transpiled.count_ops()['cx'], reverse=True)
        constraints_blocks.append(constraints_blocks[0])
        constraints_blocks.pop(0)

        for constraint_block in constraints_blocks:
            self.single_constraints_objects.append(constraint_block)

            if 'comparison_aux' in constraint_block.regs.keys():
                self.comparison_aux_qubits_needed.append(len(constraint_block.regs['comparison_aux'][0]))
            else:
                self.comparison_aux_qubits_needed.append(0)
            
            self.left_aux_qubits_needed.append(len(constraint_block.regs['sides_aux'][0]))
            self.right_aux_qubits_needed.append(len(constraint_block.regs['sides_aux'][1]))

        self.comparison_aux_width = sum(self.comparison_aux_qubits_needed)
        self.left_aux_width = sum(self.left_aux_qubits_needed)
        self.right_aux_width = sum(self.right_aux_qubits_needed)

        # For each constraint, one "out qubit" is needed
        self.out_qubits_amount = len(self.single_constraints_objects)

    def assemble(self) -> None:
        """
        TODO STILL NEED TO IMPROVE THIS METHOD
        Assembles a whole Grover operator (`self`) by performing the following steps:
            (1) Assembles all the `SingleConstraintBlock` objects (self.single_constraints_objects) and
            allocates auxiliary and "out" qubits for each constraint as needed.
            (2) Appends the "marking" operation of the desired states.
            (3) Appends an uncomputation of the entire operation assembled in (1).
        """

        # Looping over the constraints, appending one `SingleConstraintBlock` object in each iteration
        for count, constraint_block in enumerate(self.single_constraints_objects):

            # Defining the `qargs` (`qargs` is a parameter of the `QuantumCircuit.append` method)
            # before appending `single_constraint_object` to `self`. The `qargs` parameter should
            # get a list of `Qubit` objects for appending the `instruction` (another parameter of the
            # `QuantumCircuit.append` method) to. In the following lines we build the `qargs` list in
            # the following order: [left_side qubits, right_side qubits, aux qubits, out qubit]. Note
            # that aux qubits are optional, as explained in the next comment.

            qargs = []

            # TODO IMPROVE
            left_input_qubits = list(chain(*constraint_block.parsed_data.sides_bit_indexes[0]))
            if left_input_qubits:
                qargs += self.input_reg[left_input_qubits]

            right_input_qubits = list(chain(*constraint_block.parsed_data.sides_bit_indexes[1]))
            if right_input_qubits:
                qargs += self.input_reg[right_input_qubits]

            # TODO UNIFY ALL 3
            # Handling the case where left auxiliary qubits is needed
            if self.left_aux_qubits_needed[count] != 0:

                # Defining the range of the auxiliary qubits that is allocated for each constraint -
                # `aux_bottom` is the start qubit index, and `aux_top` is the end qubit index.
                l_aux_bottom = sum(
                    self.left_aux_qubits_needed[0:count]
                )
                l_aux_top = (
                    l_aux_bottom +
                    self.left_aux_qubits_needed[count]
                )

                # TODO TEST [::-1]
                qargs += self.left_aux_reg[l_aux_bottom:l_aux_top][::-1]

            # TODO UNIFY ALL 3
            # Handling the case where left auxiliary qubits is needed
            if self.right_aux_qubits_needed[count] != 0:

                # Defining the range of the auxiliary qubits that is allocated for each constraint -
                # `aux_bottom` is the start qubit index, and `aux_top` is the end qubit index.
                r_aux_bottom = sum(
                    self.right_aux_qubits_needed[0:count]
                )
                r_aux_top = (
                    r_aux_bottom +
                    self.right_aux_qubits_needed[count]
                )

                # TODO TEST [::-1]
                qargs += self.right_aux_reg[r_aux_bottom:r_aux_top][::-1]

            # TODO UNIFY ALL 3
            # Handling the case where comparison auxiliary qubits is needed
            if self.comparison_aux_qubits_needed[count] != 0:

                # Defining the range of the auxiliary qubits that is allocated for each constraint -
                # `aux_bottom` is the start qubit index, and `aux_top` is the end qubit index.
                a_aux_bottom = sum(
                    self.comparison_aux_qubits_needed[0:count]
                )
                a_aux_top = (
                    a_aux_bottom +
                    self.comparison_aux_qubits_needed[count]
                )

                # TODO TEST [::-1]
                qargs += self.comparison_aux_reg[a_aux_bottom:a_aux_top][::-1]

            # TODO BETTER WAY?
            # TODO need to fix the bug of one constraint only produces an error
            intermidate_flag = True

            # First constraint
            if count == 0:
                qargs.append(self.out_reg[count])
                self.append(instruction=constraint_block, qargs=qargs)
                
                # Only one constraint
                if self.out_qubits_amount == 1:
                    qc_dagger = self.inverse()
                    qc_dagger.name = 'Uncomputation'

                    self.cx(self.out_reg[count], self.ancilla)

            # Last constraint
            elif count == len(self.single_constraints_objects) - 1:
                qargs.append(self.out_reg[count])
                self.append(instruction=constraint_block, qargs=qargs)

                # TODO NEED TO FIX INEFFICIENCIES IN TRANSPILATION CAUSED BY BARRIERES
                if self.insert_barriers:
                    self.barrier()

                qc_dagger = self.inverse()
                qc_dagger.name = 'Uncomputation'
                
                self.ccx(self.out_reg[count - 1], self.out_reg[count], self.ancilla)
                
            # Intermidate constraints
            else:
                qargs.append(self.out_reg[count + 1])

                self.append(instruction=constraint_block, qargs=qargs)
                self.rccx(self.out_reg[count + 1], self.out_reg[count - 1], self.out_reg[count])
                self.append(instruction=constraint_block.inverse(), qargs=qargs)

            # TODO NEED TO FIX INEFFICIENCIES IN TRANSPILATION CAUSED BY BARRIERES
            if self.insert_barriers:
                self.barrier()
            
            # Appending the entire constraint block
            # self.append(instruction=single_constraint_object, qargs=qargs)

            # TODO IMPROVE using `self.out_aux_reg` to CONTROL WHATEVER
        
        # TODO
        # Saving all actions until now for uncomputation
        # qc_dagger = self.inverse()
        # qc_dagger.name = 'Uncomputation'
        
        # If all terms met, applying NOT to the ancilla (which is in the eigenstate |-> beforehand).
        # This is the basic operation of Grover's operator which marks the desired states.
        # TODO - OLD GOOD WAY
        # self.mcx(control_qubits=self.out_reg, target_qubit=self.ancilla)
        
        # Uncomputation
        self.append(instruction=qc_dagger, qargs=self.qubits)
        
        self.name = 'Operator'

if __name__ == "__main__":

    # pc = ParsedConstraints("([4][3][2] != [0]),([2] == [3]),([3] == [4]),([0] != [1]),([2] + [4] + 5 != 11 + [3]")
    # # pc = ParsedConstraints("([0] != [1]),([4][3] != [5]),([1] != [4][3]),([4][3] != [6]),([6] != [7]),([0] != [2]),([1] != [6]),([5] != [7]),([4][3] == 2)")
    # pc = ParsedConstraints(
    #     "([0] != [1]),([2] + 2 != [4][3]),([4][3] != [5]),([1] != [4][3]),([4][3] != [6])," \
    #     "([6] != [7]),([0] != [2]),([1] != [6]),([5] != [7]),([4][3] == 2),([2] + [5] + [4][3] == 3)"
    # )
    # pc = ParsedConstraints(
    #     "([0] != [1]),([2] + 2 != [4][3]),([4][3] != [5]),([1] != [4][3]),([4][3] != [6])," \
    #     "([6] != [7]),([0] != [2]),([1] != [6]),([5] != [7]),([4][3] == 2)"
    # )
    pc = ParsedConstraints("([0] != [1]),([2] + 2 != [4][3]),([4][3] != [5]),([1] != [4][3]),([4][3] != [6]),([6] != [7]),([0] != [2]),([1] != [6]),([5] != [7]),([4][3] == 2)")
    # pc = ParsedConstraints("([4][3][2] == [1][0]),([2] + 2 != [4][3])")
    # pc = ParsedConstraints("([2] + [5] + [4][3][1] == 9),(~[0] || ~[1])")

    gco = GroverConstraintsOperator(pc, 8)
    print(gco.draw())
    # decgco = gco.decompose(["([2] + [5] + [4][3] == 3)"])
    # print(decgco.draw())
    # print(decgco.decompose(["Addition:([2], [5], [4, 3]) + None"]).draw())