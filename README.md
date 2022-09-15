# SAT Circuits Synthesis Engine

This Qiskit-based program builds and runs quantum circuits for satisfiability problems according to user-defined constraints.

## Motivation

Today's current quantum software stack is pretty thin. Quantum programming is being performed mostly at the level of qubits and logic gates.  While for low amounts of qubits that might be sufficient, as technology advances and quantum processors scale up it becomes infeasible to design quantum programs and algorithms for increasing amounts of qubits.  Some adequate layers of abstraction are needed for really exploit the power of future's quantum computers.

## Intention

This program is a proof-of-concept for automatic quantum program synthesis. Many aspects needed to be taken into account when designing quantum circuits - I chose a few of them for the proof-of-concept purpose.

## A Quantum Speed-Up
[Grover's algorithm](https://en.wikipedia.org/wiki/Grover%27s_algorithm) is a well-known quantum unstructured search algorithm that provides a quadratic speed-up compared to equivalent classical algorithms.  This program uses Grover's algorithm principles and sub-routines in order to find solutions to satisfiability problems.

## Key Features

### User's Input:

 1. Total amount of input qubits.
 2. A list of constraints involving the input qubits - Right now the supported types of constraints are:
	 - Equivalency / Inequivalency of qubits' states.
	 - Equivalency / Inequivalency of qubits with integers.
3.  A basic hardware-oriented constraint - Whether uncomputation of auxiliary qubits is desired or not (By uncomputing and reusing qubits the program consumes fewer qubits in exchange for additional gate operations needed for the uncomputation process, i.e deeper circuits are provided).

### The Program's output:
1. A `QuantumCircuit` object that solves the SAT problem.
2. A basic representation of the results obtained by running the circuit.

## Future Improvements Needed

1. Optimizing $MCX$ gates cost.
2. Adding more supported constraints (addition operators between qubits for example).
3. Adding more optimization parameters - Such as maximum amount of qubits available, maximum desired circuit depth, maximum allowed amount of $CX$ gates, etc.
