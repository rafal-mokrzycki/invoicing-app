""" to run: python -m pytest -vv tests\test_formatters.py -s
add --pdb to debug in command line
use VScode test tools reccomended (the beaker) """
import repackage

repackage.up()
from scripts.formatters import format_number, format_percentages

CURRENCY = "PLN"


def test_format_number():
    assert format_number(2.5) == "2.50 PLN"


def test_format_percentages():
    assert format_percentages(0.23) == "23%"


def test_get_number_of_objects_in_table():
    pass
