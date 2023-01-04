""" This module contains decorator functions to be used throughout the package. """

import time

def timer_dec(func_to_measure):
    """
    Measures exection time of a function `func_to_measure` and prints it.
    To be used as a decorator.

    Returns: (None).
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        value = func_to_measure(*args, **kwargs)
        print(f"Execution time = {time.time() - start_time} seconds")
        return value

    return wrapper