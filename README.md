# SAT Circuits Synthesis Engine

This Qiskit-based program builds and runs quantum circuits for satisfiability problems according to user-defined constraints. The circuits built by the program are based on [Grover's algorithm](https://en.wikipedia.org/wiki/Grover%27s_algorithm) and its [amplitude amplification](https://en.wikipedia.org/wiki/Amplitude_amplification) sub-routine.

## Motivation

Today's current quantum software stack is pretty thin. Quantum programming is being performed mostly at the level of qubits and logic gates.  While for low amounts of qubits it might be sufficient, as technology advances and quantum processors scale up it becomes infeasible to design quantum programs and algorithms for increasing amounts of qubits.  Some adequate layers of abstraction are needed to really exploit the power of future's quantum computers.

## Intention

This program is a proof-of-concept for automatic quantum program synthesis. While it provides a layer of automation, still there are many aspects that are not covered (yet) by the engine - Such as extensive circuit depth optimization, hardware specifications, etc.

## Instructions
1. All the necessary files are in the main folder.
2. I would recommend downloading the entire directory ('Code -> Download ZIP' on the main page) and then running it on a Jupyter Notebook. Run the main file (ipynb file) and further instructions are included within it. No need to run anything but the main file.
3. In the file [test_data.txt](https://github.com/ohadlev77/SAT_Circuits_Engine/blob/main/test_data.txt) there are few tested examples that can be used easily, for convenience.


## Key Features

### User's Input:

 1. The total amount of input qubits ($n$ qubits create a $2^n$ solution space).
 2. A string of boolean arithmetic constraints involving the input qubits (see more [here](https://github.com/ohadlev77/SAT_Circuits_Engine/blob/main/constraints_format.txt "constraints_format.txt")).
3. The expected amount of results.
	a. NOTE: This of course feels pointless, however it is a necessary detail that affects the amount of iterations over the algorithm. This caveat can be solved by classical means and it will be updated in the next versions.

### The Program's output:
1. A `QuantumCircuit` object that solves the SAT problem.
2. A basic representation of the results obtained by running the circuit.

## Future Improvements Needed

1. Adding a classical layer that solves the issue of the expected amount of results.
2. Further optimizing  of $MCX$ gates cost.
3. Adding more supported constraints (addition operators between qubits, comparison of qubits and integers, etc).
4. Adding more optimization parameters - Such as maximum amount of qubits available, maximum desired circuit depth, maximum allowed amount of $CX$ gates, etc.
