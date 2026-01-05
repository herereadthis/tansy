from decimal import Decimal

def get_decimal_precision(value):
    """
    Returns the number of decimal places in the given Decimal value.
    """
    # convert the value to a string
    value_str = format(value, 'f')
    if '.' in value_str:
        return len(value_str.split('.')[1])
    else:
        return 0
    
def get_decimal_difference(value1, value2, format_result=True):
    """
    Returns the absolute difference between two Decimal values.
    """
    difference = Decimal(value1) - Decimal(value2)
    if format_result:
        return format(difference, 'f')
    else:
        return difference
