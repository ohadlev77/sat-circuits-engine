#    Copyright 2022-2023 Ohad Lev.

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0,
#    or in the root directory of this package("LICENSE.txt").

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

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