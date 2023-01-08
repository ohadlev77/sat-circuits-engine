"""
TODO COMPLETE
"""

from qiskit import QuantumCircuit, QuantumRegister

from .single_constraint import SingleConstraintBlock

class GroverConstraintsOperator(QuantumCircuit):
    """
    A quantum circuit implementation of Grover's operator constructed
    for a specific string of constraints entered by a user.
    """

    def __init__(
        self,
        constraints_string: str,
        num_input_qubits: int,
        probe: bool=True,
        mpl: bool=True
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
            # TODO COMPLETE probe
        """

        # Assigning the basic instance variables
        self.num_input_qubits = num_input_qubits
        self.constraints_string = constraints_string        
        self.mpl = mpl
        
        # Transforming `constraints_string` into a list of `SingleConstraintBlock` objects. A few more
        # instance variables defined within `self.constraints_build`, see its docstrings for details.
        self.constraints_build()

        # Initializing the quantum circuit that implements the Grover operator we seek for
        self.input_reg = QuantumRegister(self.num_input_qubits, 'input_reg')
        self.aux_reg = QuantumRegister(self.total_aux_qubits_needed, 'aux_reg')
        self.out_reg = QuantumRegister(self.out_qubits_amount, 'out_reg')
        self.ancilla = QuantumRegister(1, 'ancilla')
        super().__init__(self.input_reg, self.aux_reg, self.out_reg, self.ancilla)
        
        # Assembling `self` to a complete Grover operator
        self.assemble()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.constraints_string}')"

    def constraints_build(self) -> None:
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

        # Transforming a string with multiple constraints to a list of single constraints strings
        self.single_constraints_list = self.constraints_string.split(",")

        # Initializing an empty list for appending the `SingleConstraintBlock` objects to
        self.single_constraints_objects = []

        # Initializing the track on the auxiliary qubits that are needed to implement each constraint
        self.total_aux_qubits_needed = 0
        self.aux_qubits_needed_list = []

        # For each constraint we build a `SingleConstraintBlock` object and calculate
        # the number of auxiliary qubits needed to implement it
        # (i.e, how many auxiliary qubits each `SingleConstraintBlock` object uses).
        for constraint_index, single_constraint_string in enumerate(self.single_constraints_list):
            self.single_constraints_objects.append(
                SingleConstraintBlock(constraint_index, single_constraint_string, mpl=self.mpl)
            )

            self.total_aux_qubits_needed += (
                self.single_constraints_objects[constraint_index].aux_qubits_needed
            )

            self.aux_qubits_needed_list.append(
                self.single_constraints_objects[constraint_index].aux_qubits_needed
            )


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
        for single_constraint_object in self.single_constraints_objects:
            
            # Defining the `qargs` (`qargs` is a parameter of the `QuantumCircuit.append` method)
            # before appending `single_constraint_object` to `self`. The `qargs` parameter should
            # get a list of `Qubit` objects for appending the `instruction` (another parameter of the
            # `QuantumCircuit.append` method) to. In the following lines we build the `qargs` list in
            # the following order: [left_side qubits, right_side qubits, aux qubits, out qubit]. Note
            # that aux qubits are optional, as explained in the next comment.
            qargs = (
                self.input_reg[single_constraint_object.left_side] +
                self.input_reg[single_constraint_object.right_side]
            )

            # Handling the case where auxiliary qubits is needed (i.e for any constraint that involves
            # with more than 2 qubits).
            if single_constraint_object.aux_qubits_needed != 0:

                # Defining the range of the auxiliary qubits that is allocated for each constraint -
                # `aux_bottom` is the start qubit index, and `aux_top` is the end qubit index.
                aux_bottom = sum(
                    self.aux_qubits_needed_list[0:single_constraint_object.constraint_index]
                )
                aux_top = (
                    aux_bottom +
                    self.aux_qubits_needed_list[single_constraint_object.constraint_index]
                )

                qargs += self.aux_reg[aux_bottom:aux_top]
    
            qargs.append(self.out_reg[single_constraint_object.constraint_index])

            self.append(instruction=single_constraint_object, qargs=qargs)
            self.barrier()
        
        # Saving all actions until now for uncomputation
        qc_dagger = self.inverse()
        qc_dagger.name = 'Uncomputation'
        
        # If all terms met, applying NOT to the ancilla (which is in the eigenstate |-> beforehand).
        # This is the basic operation of Grover's operator which marks the desired states.

        # OPTION 1 - DEFAULT
        self.mcx(control_qubits=self.out_reg, target_qubit=self.ancilla)

        # OPTION 2 - TODO - TRYING TO OPTIMIZE BY AVOIDING MCX
        # self.x(self.out_reg[1:])
        # for index in range(self.out_reg.size - 1):
        #     self.cx(self.out_reg[index], self.out_reg[index + 1])
        # qc_dagger = self.inverse()
        # qc_dagger.name = 'Uncomputation'
        # self.cx(self.out_reg[self.out_reg.size - 1], self.ancilla)
        
        # Uncomputation
        self.append(instruction=qc_dagger, qargs=self.qubits)
        
        self.name = 'Operator'