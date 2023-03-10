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
Contains decorator functions to be used throughout the package:
    1. timer_dec.
"""

import time
from typing import Optional, Any


def timer_dec(message_prefix: Optional[str] = None) -> Any:
    """
    Measures an execution time (in seconds) of a function and prints it.
    To be used as a decorator.

    Args:
        message_prefix (Optional[str]): A prefix to the message printed by this function,
        while the format message is: "{PREFIX}{TIME_TAKEN} seconds."

    Returns:
        (Any): returns the value that `func_to_measure` returns, can be of any type.
    """

    if message_prefix is None:
        message_prefix = "Execution time = "

    def decorator(func_to_measure):
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            func_value = func_to_measure(*args, **kwargs)

            time_taken = round(time.perf_counter() - start_time, 2)
            print(f"{message_prefix}{time_taken} seconds.")

            return func_value

        return wrapper

    return decorator
