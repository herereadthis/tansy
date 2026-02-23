from decimal import Decimal
from montecarlo_pi.utilities.util import get_decimal_precision, get_accuracy


def test_no_precision():
    """test numbers with no decimal places"""
    assert get_decimal_precision(Decimal("3")) == 0


def test_decimal_precision():
    """test numbers with decimal places"""
    assert get_decimal_precision(Decimal("3.14")) == 2


def test_trailing_zeros():
    """test numbers with trailing zeros"""
    assert get_decimal_precision(Decimal("1.00")) == 2


def test_zero_with_decimals():
    """test zero with decimal places"""
    assert get_decimal_precision(Decimal("0.0")) == 1

def test_identical_numbers():
    """test identical numbers have full accuracy"""
    assert get_accuracy("3.1415", "3.1415") == 4
    assert get_accuracy(3.14159, 3.14159) == 5
    assert get_accuracy(3, 3) == 0

def test_partial_match():
    """test numbers with partial decimal match"""
    assert get_accuracy(3.1415926, 3.1419) == 3


def test_total_mismatch():
    """test numbers with no decimal match"""
    assert get_accuracy(1.1, 1.2) == 0
