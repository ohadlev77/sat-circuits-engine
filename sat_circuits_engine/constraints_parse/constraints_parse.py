"""
`ParsedConstraints` and `SATNoSolutionError` classes.
"""

from typing import Optional

from sat_circuits_engine.constraints_parse.single_constraint_parse import SingleConstraintParsed

class ParsedConstraints(dict):
    """
    A dictionary-like object to store `SingleConstraintParsed` objects as values,
    and "low-level" constraints string as keys.
    """

    def __init__(
        self,
        constraints_string: str,
        high_level_constraints_string: Optional[str] = None
    ) -> None:
        """
        Args:
            constraints_string (str): string of constraints in a "low-level" format.
            high_level_constraints_string (str): string of constraints in a "high-level" format.
                - this data is "piped" through this class for visualization purposes.
        """

        self.constraints_string = constraints_string
        self.high_level_constraints_string = high_level_constraints_string

        super().__init__()

        self.constraints_string_to_dict()
    
    def constraints_string_to_dict(self) -> None:
        """
        Fills the dictionary with low-level constraints strings as keys
        and `SingleConstraintParsed` objects as values.
        """

        constraints_list = self.constraints_string.split(',')

        if self.high_level_constraints_string is not None:
            high_level_constraints_list = self.high_level_constraints_string.split(',')
        else:
            high_level_constraints_list = [None for _ in range(len(constraints_list))]

        for index, (single_string, single_high_level_string) in enumerate(zip(
            constraints_list,
            high_level_constraints_list
        )):
            self[single_string] = SingleConstraintParsed(
                constraint_string=single_string,
                constraint_index=index,
                high_level_constraint_string=single_high_level_string
            )

class SATNoSolutionError(Exception):
    """
    Exception to be raised when the SAT problem has no solution.
    """

    def __init__(self, message) -> None:
        super().__init__(message)