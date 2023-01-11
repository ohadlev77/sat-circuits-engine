"""
TODO COMPLETE
"""

from .single_constraint_parse import SingleConstraintParsed

class ParsedConstraints(dict):
    """
    TODO COMPLETE
    """

    def __init__(self, constraints_string: str) -> None:
        """
        TODO COMPLETE
        """

        self.constraints_string = constraints_string

        super().__init__()

        self.constraints_string_to_dict()
    
    def constraints_string_to_dict(
        self,
    ) -> None:
        """
            TODO COMPLETE
        """

        for constraint_index, single_constraint_string in enumerate(self.constraints_string.split(',')):
            self[single_constraint_string] = SingleConstraintParsed(
                single_constraint_string,
                constraint_index,
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