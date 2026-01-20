"""
Utility functions
"""

from contextlib import contextmanager
import time
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)

def get_decimal_precision(value):
    """
    Returns the number of decimal places in the given Decimal value.
    """
    # convert the value to a string
    value_str = format(value, 'f')
    if '.' in value_str:
        return len(value_str.split('.')[1])

    return 0

def get_accuracy(true_value, estimated_value):
    """
    Gets accuracy between 2 numbers by counting matching decimal places.
    """
    true_value_decimal = Decimal(str(true_value))
    estimated_value_decimal = Decimal(str(estimated_value))

    true_value_decimals = str(true_value_decimal).split(".")[1] if "." in str(true_value_decimal) else ""
    estimated_value_decimals = str(estimated_value_decimal).split(".")[1] if "." in str(estimated_value_decimal) else ""
    max_decimal_places = max(len(true_value_decimals), len(estimated_value_decimals))

    decimal_accuracy = max_decimal_places
    for decimal_places in range(max_decimal_places + 1):
        true_rounded = round(true_value_decimal, decimal_places)
        estimated_rounded = round(estimated_value_decimal, decimal_places)

        if true_rounded != estimated_rounded:
            decimal_accuracy = max(0, decimal_places - 1)
            break
    return decimal_accuracy

def get_readable_time_diff(start_time, end_time):
    """
    Returns a human-readable time difference between two timestamps.
    """
    elapsed_time = end_time - start_time

    if elapsed_time < 60:
        time_diff = f"{elapsed_time:.3f} seconds"
    else:
        time_diff = f"{elapsed_time / 60:.3f} minutes"

    return time_diff

@contextmanager
def timer():
    """
    Use context manager to measure time.
    see https://docs.python.org/3/library/contextlib.html#examples-and-recipes
    """
    start = time.perf_counter()
    elapsed = {}
    try:
        yield elapsed
    finally:
        elapsed['seconds'] = time.perf_counter() - start
