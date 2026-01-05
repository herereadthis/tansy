"""
Utility functions
"""

from decimal import Decimal

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

    decimal_accuracy = 0

    if len(true_value_decimals) != 0 and len(estimated_value_decimals) != 0:
        for true_decimal_digit, estimated_decimal_digit in zip(true_value_decimals, estimated_value_decimals):
            if true_decimal_digit == estimated_decimal_digit:
                decimal_accuracy += 1
            else:
                break

    return decimal_accuracy
