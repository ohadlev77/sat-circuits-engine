"""
The `constraints_parse` sub-package contains modules, classes and functions for parsing
constraints strings in a "low-level" format (see constraints_format.md in the main directory),
into objects implementing a specific API.
"""

from .single_constraint_parse import SingleConstraintParsed
from .constraints_parse import ParsedConstraints, SATNoSolutionError