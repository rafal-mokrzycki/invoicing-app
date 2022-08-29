""" to run: python -m pytest -vv tests\test_invoice.py -s
add --pdb to debug in command line
use VScode test tools reccomended (the beaker) """

from scripts.invoice import count_gross


def test_count_gross():
    count_gross(1, 0.9)
