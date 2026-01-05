from montecarlo_pi.utilities.util import get_accuracy

def test_identical_numbers():
    assert get_accuracy("3.1415", "3.1415") == 4
    assert get_accuracy(3.14159, 3.14159) == 5
    assert get_accuracy(3, 3) == 0
