""" This module contains decorator functions to be used throughout the package. """

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

# def timer_dec(func_to_measure):
#     """
#     Measures exection time of a function `func_to_measure` and prints it.
#     To be used as a decorator.

#     Returns: (None).
#     """

#     def wrapper(*args, **kwargs):
#         start_time = time.time()
#         value = func_to_measure(*args, **kwargs)
#         print(f"Execution time = {time.time() - start_time} seconds")
#         return value

#     return wrapper