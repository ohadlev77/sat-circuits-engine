"""
TODO COMPLETE
"""

from qiskit import QuantumCircuit, QuantumRegister

from sat_circuits_engine.constraints_parse import ParsedConstraints
from .single_constraint import SingleConstraintBlock


class GroverConstraintsOperator(QuantumCircuit):
    """
    A quantum circuit implementation of Grover's operator constructed
    for a specific string of constraints entered by a user.
    """

    def __init__(
        self,
        parsed_constraints: ParsedConstraints,
        num_input_qubits: int,
        mpl: bool = True
    ) -> None:
        """
        Args:
            constraints_string (str):
                # A string that describes a set of boolean arithmetic constraints
                written in a specific format.
                # A full explanation about the format is provided in the file
                `/interface/constraints_format.txt`.
            num_input_qubits (int): number of qubits in the input register.
            mpl (bool): `True` for matplotlib circuit diagrams output, `False` for text output. # TODO CONSIDER TO REMOVE
        """

        self.num_input_qubits = num_input_qubits
        self.parsed_constraints = list(parsed_constraints.values())
        self.mpl = mpl

        # Transforming `constraints_string` into a list of `SingleConstraintBlock` objects. A few more
        # instance variables defined within `self.constraints_build`, see its docstrings for details.
        self.constraints_blocks_build()

        # Initializing the quantum circuit that implements the Grover operator we seek for
        self.input_reg = QuantumRegister(self.num_input_qubits, 'input_reg')
        self.aux_reg = QuantumRegister(self.total_aux_qubits_needed, 'aux_reg')
        self.out_reg = QuantumRegister(self.out_qubits_amount, 'out_reg')
        self.out_aux_reg = QuantumRegister(1, 'out_aux_reg')
        self.ancilla = QuantumRegister(1, 'ancilla')
        super().__init__(self.input_reg, self.aux_reg, self.out_reg, self.out_aux_reg, self.ancilla)
        
        # Assembling `self` to a complete Grover operator
        self.assemble()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.constraints_string}')"

    def constraints_blocks_build(self) -> None:
        """
        Parses the `self.constraints_string` varaible and defines the instance variables:
            # `self.single_constraints_list` (List[str]): a list of single constraints strings.
            # `self.single_constraints_objects` (List[SingleConstraintBlock]): a list of
            `SingleConstraintBlock` objects, each built from a single constraint string.
            # `self.total_aux_qubits_needed` (int): total number of auxiliary qubits needed.
            # `self.aux_qubits_needed_list` (List[int]): a list of auxiliary qubits needed
            for implementing each constraint.
            # `self.out_qubits_amount` (int): the number of "out qubits" needed, while each "out qubit"
            is used to write the result of applying a single constraint into (|1> if the constraint is 
            satisfied, |0> otherwise).
        """

        # Initializing an empty list for appending the `SingleConstraintBlock` objects to
        self.single_constraints_objects = []

        # Initializing the track on the auxiliary qubits that are needed to implement each constraint
        self.total_aux_qubits_needed = 0
        self.aux_qubits_needed_list = []

        # For each constraint we build a `SingleConstraintBlock` object and calculate
        # the number of auxiliary qubits needed to implement it
        # (i.e, how many auxiliary qubits each `SingleConstraintBlock` object uses).
        for parsed_constraint in self.parsed_constraints:
            self.single_constraints_objects.append(
                SingleConstraintBlock(parsed_constraint, mpl=self.mpl)
            )

            self.aux_qubits_needed_list.append(parsed_constraint.aux_qubits_needed)
            self.total_aux_qubits_needed += parsed_constraint.aux_qubits_needed

        # For each constraint, one "out qubit" is needed
        self.out_qubits_amount = len(self.single_constraints_objects)

    def assemble(self) -> None:
        """
        Assembles a whole Grover operator (`self`) by performing the following steps:
            (1) Assembles all the `SingleConstraintBlock` objects (self.single_constraints_objects) and
            allocates auxiliary and "out" qubits for each constraint as needed.
            (2) Appends the "marking" operation of the desired states.
            (3) Appends an uncomputation of the entire operation assembled in (1).
        """

        # Looping over the constraints, appending one `SingleConstraintBlock` object in each iteration
        for index, (constraint_block, parsed_constraint) in \
            enumerate(zip(self.single_constraints_objects, self.parsed_constraints)):
            
            # Defining the `qargs` (`qargs` is a parameter of the `QuantumCircuit.append` method)
            # before appending `single_constraint_object` to `self`. The `qargs` parameter should
            # get a list of `Qubit` objects for appending the `instruction` (another parameter of the
            # `QuantumCircuit.append` method) to. In the following lines we build the `qargs` list in
            # the following order: [left_side qubits, right_side qubits, aux qubits, out qubit]. Note
            # that aux qubits are optional, as explained in the next comment.
            qargs = (
                self.input_reg[parsed_constraint.left_side] +
                self.input_reg[parsed_constraint.right_side]
            )

            # Handling the case where auxiliary qubits is needed (i.e for any constraint that involves
            # with more than 2 qubits).
            if parsed_constraint.aux_qubits_needed != 0:

                # Defining the range of the auxiliary qubits that is allocated for each constraint -
                # `aux_bottom` is the start qubit index, and `aux_top` is the end qubit index.
                aux_bottom = sum(
                    self.aux_qubits_needed_list[0:parsed_constraint.constraint_index]
                )
                aux_top = (
                    aux_bottom +
                    self.aux_qubits_needed_list[parsed_constraint.constraint_index]
                )

                qargs += self.aux_reg[aux_bottom:aux_top]

            # TODO BETTER WAY?
            # TODO need to fix the bug of one constraint only produces an error
            intermidate_flag = True

            # First constraint
            if index == 0:    
                qargs.append(self.out_reg[index])
                self.append(instruction=constraint_block, qargs=qargs)

                intermidate_flag = False

            # Last constraint
            if index == len(self.single_constraints_objects) - 1:
                qargs.append(self.out_aux_reg)
                self.append(instruction=constraint_block, qargs=qargs)

                self.barrier()
                qc_dagger = self.inverse()
                qc_dagger.name = 'Uncomputation'
                
                self.ccx(self.out_aux_reg, self.out_reg[index - 1], self.ancilla)

                intermidate_flag = False
                
            # Intermidate constraints
            if intermidate_flag:
                qargs.append(self.out_aux_reg)
                
                self.append(instruction=constraint_block, qargs=qargs)
                self.rccx(self.out_aux_reg, self.out_reg[index - 1], self.out_reg[index])
                self.append(instruction=constraint_block.inverse(), qargs=qargs)

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