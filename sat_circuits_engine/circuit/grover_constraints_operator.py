"""
GroverConstraintsOperator class.
"""

from itertools import chain
from typing import Optional

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.transpiler.passes import RemoveBarriers

from sat_circuits_engine.constraints_parse import ParsedConstraints
from sat_circuits_engine.circuit.single_constraint import SingleConstraintBlock

class GroverConstraintsOperator(QuantumCircuit):
    """
    A quantum circuit implementation of Grover's operator constructed
    for a specific combination of constraints defined by a user.
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
            insert_barriers (Optional[bool] = True): if True, barriers will be inserted
            to separate between constraints.
        """

        self.num_input_qubits = num_input_qubits
        self.parsed_constraints = parsed_constraints
        self.insert_barriers = insert_barriers

        # Construction a `SingleConstraintBlock` object for every constraint. A few more
        # attributes defined within self.constraints_blocks_build(), see its docstrings for details.
        self.constraints_blocks_build()

        # Initializing the quantum circuit that implements the Grover operator we seek for
        self.input_reg = QuantumRegister(self.num_input_qubits, "input_reg")
        self.comparison_aux_reg = QuantumRegister(self.comparison_aux_width, "comparison_aux_reg")
        self.left_aux_reg = QuantumRegister(self.left_aux_width, "left_aux_reg")
        self.right_aux_reg = QuantumRegister(self.right_aux_width, "right_aux_reg")
        self.out_reg = QuantumRegister(self.out_qubits_amount, "out_reg")
        self.ancilla = QuantumRegister(1, "ancilla")

        super().__init__(
            self.input_reg,
            self.left_aux_reg,
            self.right_aux_reg,
            self.comparison_aux_reg,
            self.out_reg,
            self.ancilla,
            name = "Operator"
        )

        # Assembling `self` to a complete Grover operator
        self.assemble()

    def __repr__(self) -> str:
        if self.parsed_constraints.high_level_constraints_string is not None:
            repr_string = self.parsed_constraints.high_level_constraints_string
        else:
            repr_string = self.parsed_constraints.constraints_string
        
        return f"{self.__class__.__name__}('{repr_string}')"

    def constraints_blocks_build(self) -> None:
        """
        Parses the `self.parsed_constraints` attribute and defines the attributes:
            - `self.single_constraints_objects` (List[SingleConstraintBlock]): a list of
            `SingleConstraintBlock` objects, each built from a single constraint string.
            - `self.comparison_aux_qubits_needed` (List[int]): a list of auxiliary qubits needed
            for implementing the comparison between the two sides of the constraint's equation.
            - `self.left_aux_qubits_needed` (List[int]): a list of auxiliary qubits needed
            for implementing arithmetics on the left side of the constraint's equation.
            - `self.right_aux_qubits_needed` (List[int]): a list of auxiliary qubits needed
            for implementing arithmetics on the right side of the constraint's equation.
            - `self.comparison_aux_width` (int): Total number of comparison aux qubits.
            - `self.left_aux_width` (int): Total number of left aux qubits.
            - `self.right_aux_width` (int): Total number of right aux qubits.
            - `self.out_qubits_amount` (int): the number of "out qubits" needed, while each "out qubit"
            is used to write the result of applying a single constraint into (|1> if the constraint is
            satisfied, |0> otherwise).
        """

        # For each constraint we build a `SingleConstraintBlock` object
        self.single_constraints_objects = list(map(
            SingleConstraintBlock,
            self.parsed_constraints.values()
        ))

        # Sorting the constraints such that the most costly ones will be the first and last
        # (First and last constraint are not uncomputed - only when the whole operator is uncomputed).
        self.single_constraints_objects.sort(key=lambda x: x.transpiled.count_ops()['cx'], reverse=True)
        self.single_constraints_objects.append(self.single_constraints_objects[0])
        self.single_constraints_objects.pop(0)

        self.comparison_aux_qubits_needed = []
        self.left_aux_qubits_needed = []
        self.right_aux_qubits_needed = []

        # For each we count which and how many aux qubits are needed
        for constraint_block in self.single_constraints_objects:
            if 'comparison_aux' in constraint_block.regs.keys():
                self.comparison_aux_qubits_needed.append(len(
                    constraint_block.regs['comparison_aux'][0]
                ))
            else:
                self.comparison_aux_qubits_needed.append(0)
            
            self.left_aux_qubits_needed.append(len(constraint_block.regs['sides_aux'][0]))
            self.right_aux_qubits_needed.append(len(constraint_block.regs['sides_aux'][1]))

        # Total number of qubits for each type
        self.comparison_aux_width = sum(self.comparison_aux_qubits_needed)
        self.left_aux_width = sum(self.left_aux_qubits_needed)
        self.right_aux_width = sum(self.right_aux_qubits_needed)
        self.out_qubits_amount = len(self.single_constraints_objects)

    def assemble(self) -> None:
        """
        Assembles a whole Grover operator (`self`) by performing the following steps:
            (1) Allocating qubits for each `SingleConstraintBlock` object
            (from `self.single_constraints_objects`) - for input qubits, auxiliary qubits of
            all kinds and a single "out" qubit for each constraint.
            (2) Appending all the `SingleConstraintBlock` objects.
            (3) Applying a "marking" operation by applying some controlled-not gate to the
            ancilla qubit.
            (4) Appending an uncomputation of the entire operation assembled in (1) + (2).
        """

        # Iterating over constraints, appending one `SingleConstraintBlock` object in each iteration
        for count, constraint_block in enumerate(self.single_constraints_objects):

            # Defining the `qargs` paramater for the `constraint_block` to be appended to `self`
            qargs = []

            # Appending the input bits indexes from both sides of the constraint's equation to `qargs`
            left_input_qubits = list(chain(*constraint_block.parsed_data.sides_bit_indexes[0]))
            if left_input_qubits:
                qargs += self.input_reg[left_input_qubits]

            right_input_qubits = list(chain(*constraint_block.parsed_data.sides_bit_indexes[1]))
            if right_input_qubits:
                qargs += self.input_reg[right_input_qubits]

            # Appending the various aux bits indexes to `qargs`
            for aux_tuple in [
                (self.left_aux_qubits_needed, self.left_aux_reg),
                (self.right_aux_qubits_needed, self.right_aux_reg),
                (self.comparison_aux_qubits_needed, self.comparison_aux_reg)
            ]:
                if aux_tuple[0][count] != 0:
                    aux_bottom_index = sum(aux_tuple[0][0:count])
                    aux_top_index = (aux_bottom_index + aux_tuple[0][count])

                    qargs += aux_tuple[1][aux_bottom_index:aux_top_index][::-1]

            # Appending blocks of constraints to `self`
            # First constraint
            if count == 0:
                qargs.append(self.out_reg[count])
                self.append(instruction=constraint_block, qargs=qargs)
                
                # If there is only one constraint
                if self.out_qubits_amount == 1:

                    # Saving inverse for future uncomputation
                    qc_dagger = self.inverse()
                    qc_dagger.name = 'Uncomputation'

                    # "Marking" states by writing to ancilla
                    self.cx(self.out_reg[count], self.ancilla)

            # Last constraint
            elif count == len(self.single_constraints_objects) - 1:
                qargs.append(self.out_reg[count])
                self.append(instruction=constraint_block, qargs=qargs)

                # Barriers are used for visualization purposes and should be removed before transpiling
                if self.insert_barriers:
                    self.barrier()

                # Saving inverse for future uncomputation
                qc_dagger = RemoveBarriers()(self.inverse())
                qc_dagger.name = "Uncomputation"
                
                # "Marking" states by writing to ancilla
                self.ccx(self.out_reg[count - 1], self.out_reg[count], self.ancilla)
                
            # Intermidate constraints
            else:
                qargs.append(self.out_reg[count + 1])

                # Chaining constraints with RCCX gates, to avoid costly MCX gate all over the out qubits
                self.append(instruction=constraint_block, qargs=qargs)
                self.rccx(self.out_reg[count + 1], self.out_reg[count - 1], self.out_reg[count])
                self.append(instruction=constraint_block.inverse(), qargs=qargs)

            # Barriers are used for visualization purposes and should be removed before transpiling
            if self.insert_barriers:
                self.barrier()
        
        # Applying uncomputation
        self.append(instruction=qc_dagger, qargs=self.qubits)