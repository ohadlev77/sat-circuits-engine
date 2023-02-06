"""
TODO COMPLETE
"""

from typing import Optional

from .single_constraint_parse import SingleConstraintParsed

class ParsedConstraints(dict):
    """
    TODO COMPLETE
    """

    def __init__(self, constraints_string: str, high_level_constraints_string: Optional[str] = None) -> None:
        """
        TODO COMPLETE
        """

        self.constraints_string = constraints_string
        self.high_level_constraints_string = high_level_constraints_string

        super().__init__()

        self.constraints_string_to_dict()
    
    def constraints_string_to_dict(
        self,
    ) -> None:
        """
            TODO COMPLETE
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

# class ParsedConstraints(list):
#     """
#     TODO COMPLETE
#     """

#     def __init__(self, constraints_string: str) -> None:
#         """
#         TODO COMPLETE
#         """

#         self.constraints_string = constraints_string

#         super().__init__()

#         self.constraints_string_to_list()

#     def __repr__(self):
#         new_repr_string = "List of constraints:\n"

#         for item in self:
#             new_repr_string += f"{item} \n"

#         return new_repr_string
    
#     def constraints_string_to_list(
#         self,
#     ) -> None:
#         """
#             TODO COMPLETE
#         """

#         for constraint_index, single_constraint_string in enumerate(self.constraints_string.split(',')):
#             self.append({
#                     f"{single_constraint_string}": \
#                     SingleConstraintParsed(constraint_index, single_constraint_string)
#             })