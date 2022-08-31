""" to run: python -m pytest -vv tests\test_invoice.py -s
add --pdb to debug in command line
use VScode test tools reccomended (the beaker) """

from scripts.invoice import calculate_gross, calculate_sum


def test_calculate_gross():
    result = calculate_gross(100, 0.23)
    assert result == 123.0


def test_calculate_sum():
    result = calculate_sum([1, 2, 3])
    assert result == 6
