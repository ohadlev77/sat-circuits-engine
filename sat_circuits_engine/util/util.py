"""
Contains utility functions to be used throughout the package:
    1. timestamp.
"""

from datetime import datetime

def timestamp(datetime_obj: datetime) -> str:
    """
    Defines a timestamp format to be used in this library.

    Args:
        datetime_obj (datetime): the `datetime.datetime` object to format.

    Returns:
        (str): a timestamp of the format: "D%d.%m.%y_T%H.%M.%S". E.g, for 01/05/2023, 10:30:45,
        the formatted timestamp is "D01.01.2023_T10.30.45".
    """

    return datetime_obj.strftime("D%d.%m.%y_T%H.%M.%S")